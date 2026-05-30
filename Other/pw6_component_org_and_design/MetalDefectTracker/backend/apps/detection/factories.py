from abc import ABC, abstractmethod

from .defects import (
    BoundingBox,
    ModelPrediction,
    Defect,
    DefinedDefect,
    OtherDefect,
    DEFECT_MAP,
    InvalidManualDefectError,
    UnknownPredictionLabelError,
)


def _validate_confidence(confidence: float) -> None:
    if confidence < 0:
        raise ValueError("Confidence must be non-negative.")


def _normalize_bbox(bbox: BoundingBox) -> BoundingBox:
    if bbox.width <= 0 or bbox.height <= 0 or bbox.x < 0 or bbox.y < 0:
        return BoundingBox(
            x=max(0, bbox.x),
            y=max(0, bbox.y),
            width=max(1, bbox.width),
            height=max(1, bbox.height),
        )
    return bbox


class DefectFactory(ABC):
    """
    Создатель (Creator) паттерна Фабричный метод.
    Создаёт доменный объект Defect и имеет общую логику подготовки данных от модели к домену.
    """

    def register_prediction(self, prediction: ModelPrediction) -> Defect:
        prepared_prediction = self._prepare_prediction(prediction)
        return self.create_defect(prepared_prediction)
    
    def _validate_prediction(self, prediction: ModelPrediction) -> None:
        _validate_confidence(prediction.confidence)

    def _prepare_prediction(self, prediction: ModelPrediction) -> ModelPrediction:
        self._validate_prediction(prediction)
        prepared_bbox = _normalize_bbox(prediction.bbox)
        if prepared_bbox != prediction.bbox:
            return ModelPrediction(
                label=prediction.label,
                bbox=prepared_bbox,
                confidence=prediction.confidence,
                source=prediction.source,
            )
        return prediction
    
    @abstractmethod
    def create_defect(self, prediction: ModelPrediction) -> Defect:
        raise NotImplementedError


# Дальше идут конкретные создатели (Concrete Creator) паттерна Фабричный метод.
# А именно, конкретные фабрики для каждого типа дефекта.

class DefinedDefectFactory(DefectFactory):
    def create_defect(self, prediction: ModelPrediction) -> Defect:
        return DefinedDefect(
            bbox=prediction.bbox,
            confidence=prediction.confidence,
            source=prediction.source,
            code=prediction.label,
        )


class OtherDefectFactory(DefectFactory):
    def __init__(
        self,
        *,
        custom_name: str,
        author: str,
        description: str | None = None,
    ) -> None:
        self.custom_name = custom_name
        self.author = author
        self.description = description

    def create_defect(self, prediction: ModelPrediction) -> Defect:
        if prediction.source != "manual":
            raise InvalidManualDefectError("OtherDefectFactory only supports manual defects.")
        return OtherDefect(
            bbox=prediction.bbox,
            confidence=prediction.confidence,
            source=prediction.source,
            custom_name=self.custom_name,
            author=self.author,
            description=self.description,
        )


class DefectFactoryRegistry:
    """
    Вспомогательный класс (Реестр), который возвращает нужную фабрику на основе label
    """
    def __init__(self):
        self._factories: dict[str, DefectFactory] = {}

    def register(self, label: str, factory: DefectFactory) -> None:
        self._factories[label.upper()] = factory

    def get_factory(self, label: str) -> DefectFactory:
        factory = self._factories.get(label.upper())
        if factory is not None:
            return factory
        raise UnknownPredictionLabelError(
            f"Unsupported prediction label received from ML service: {label}"
        )


def build_default_registry() -> DefectFactoryRegistry:
    """Упрощённая сборка реестра."""
    registry = DefectFactoryRegistry()
    defined_factory = DefinedDefectFactory()

    for label in DEFECT_MAP:
        registry.register(label, defined_factory)

    return registry
