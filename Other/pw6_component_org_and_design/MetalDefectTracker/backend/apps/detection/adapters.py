from __future__ import annotations

from abc import ABC, abstractmethod

from .defects import BoundingBox, ModelPrediction
from .external_client import ExternalMLDetectionService


class PredictionProvider(ABC):
    """
    Клиентский интерфейс (Client Interface) паттерна Адаптер.
    Протокол, через который клиент может работать с любым адаптером
    """

    @abstractmethod
    def get_predictions(self, image_path: str, threshold: float) -> list[ModelPrediction]:
        raise NotImplementedError


class MLServiceAdapter(PredictionProvider):
    """
    Адаптер (Adapter) паттерна Адаптер.
    Получает предсказания от внешнего ML-сервиса и преобразует их из сырого 
    JSON формата в удобный формат для внутреннего домена.
    """

    def __init__(self, adaptee: ExternalMLDetectionService) -> None:
        self.adaptee = adaptee

    def get_predictions(self, image_path: str, threshold: float) -> list[ModelPrediction]:
        raw_response = self.adaptee.analyze_image(
            image_path=image_path,
            threshold=threshold,
        )
        return self._convert_response(raw_response)

    def _convert_response(self, raw_response: dict) -> list[ModelPrediction]:
        predictions: list[ModelPrediction] = []

        for item in raw_response["predictions"]:
            box = item["box"]

            bbox = BoundingBox(
                x=box["left"],
                y=box["top"],
                width=box["right"] - box["left"],
                height=box["bottom"] - box["top"],
            )

            prediction = ModelPrediction(
                label=item["class_code"],
                bbox=bbox,
                confidence=item["score"],
                source="automatic",
            )
            predictions.append(prediction)

        return predictions