from abc import ABC, abstractmethod

from .defects import (
    BoundingBox,
    ModelPrediction,
    Defect,
    DefinedDefect,
    OtherDefect,
    DEFECT_MAP,
)


class DefectFactory(ABC):
    """
    Создатель (Creator) паттерна Фабричный метод.
    Создаёт доменный объект Defect и имеет общую логику подготовки данных от модели к домену.
    """

    def register_prediction(self, prediction: ModelPrediction) -> Defect:
        prepared_prediction = self._prepare_prediction(prediction)
        return self.create_defect(prepared_prediction)
    
    def _validate_prediction(self, prediction: ModelPrediction) -> None:
        if prediction.confidence < 0:
            raise ValueError("Confidence must be non-negative.")

    def _prepare_prediction(self, prediction: ModelPrediction) -> ModelPrediction:
        self._validate_prediction(prediction)
        bbox = prediction.bbox
        if bbox.width <= 0 or bbox.height <= 0 or bbox.x < 0 or bbox.y < 0:
            prepared_bbox = BoundingBox(
                x=max(0, bbox.x),
                y=max(0, bbox.y),
                width=max(1, bbox.width),
                height=max(1, bbox.height),
            )
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
    def create_defect(self, prediction: ModelPrediction) -> Defect:
        return OtherDefect(
            bbox=prediction.bbox,
            confidence=prediction.confidence,
            source=prediction.source,
        )


class DefectFactoryRegistry:
    """
    Вспомогательный класс (Реестр), который возвращает нужную фабрику на основе label
    """
    def __init__(self):
        self._defined_factory = DefinedDefectFactory()
        self._other_factory = OtherDefectFactory()

    def get_factory(self, label: str) -> DefectFactory:
        if label.upper() in DEFECT_MAP:
            return self._defined_factory
        return self._other_factory


def build_default_registry() -> DefectFactoryRegistry:
    """Упрощённая сборка реестра (только две фабрики)."""
    return DefectFactoryRegistry()