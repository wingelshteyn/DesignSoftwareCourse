from __future__ import annotations

from collections.abc import Iterable

from .defects import Defect, ModelPrediction
from .factories import DefectFactoryRegistry, build_default_registry
from .adapters import PredictionProvider


class DetectionResultBuilder:
    """
    Клиент (Client) паттерна Фабричный метод.
    Получает сырые предсказания ML и превращает их в доменные объекты Defect.
    """
    def __init__(self, registry: DefectFactoryRegistry | None = None) -> None:
        self.registry = registry or build_default_registry()

    def build_defects(self, predictions: Iterable[ModelPrediction]) -> list[Defect]:
        defects: list[Defect] = []

        for prediction in predictions:
            factory = self.registry.get_factory(prediction.label)
            defect = factory.register_prediction(prediction)
            defects.append(defect)

        return defects


class DetectionApplicationService:
    """
    Клиент (Client) паттерна Адаптер.
    Класс, который пользуется адаптером для получения предсказания с ML-серивса с непонятным интерфейсом.
    И затем использует Фабричный метод для преобразования этих предсказаний в доменные объекты Defect.
    """

    def __init__(
        self,
        prediction_provider: PredictionProvider,
        result_builder: DetectionResultBuilder | None = None,
    ) -> None:
        self.prediction_provider = prediction_provider
        self.result_builder = result_builder or DetectionResultBuilder()

    def detect(self, image_path: str, threshold: float = 0.5) -> list[Defect]:
        predictions = self.prediction_provider.get_predictions(
            image_path=image_path,
            threshold=threshold,
        )
        return self.result_builder.build_defects(predictions)