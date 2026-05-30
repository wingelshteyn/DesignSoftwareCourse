from abc import ABC, abstractmethod
from dataclasses import dataclass


DEFECT_MAP: dict[str, str] = {
    "RS": "Rolled-in scale",
    "PA": "Patch",
    "CR": "Crazing",
    "PS": "Pitted surface",
    "IN": "Inclusion",
    "SC": "Scratch",
}


@dataclass(frozen=True, slots=True)
class BoundingBox:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class ModelPrediction:
    """
    Сырым результатом ML-сервиса считаем label + bbox + confidence.
    """
    label: str
    bbox: BoundingBox
    confidence: float
    source: str = "automatic"


@dataclass(slots=True)
class Defect(ABC):
    """
    Абстрактный продукт (Product) паттерна Фабричный метод.
    """
    bbox: BoundingBox
    confidence: float
    source: str = "automatic"

    @property
    @abstractmethod
    def code(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError

    def is_manual(self) -> bool:
        return self.source == "manual"

    def describe(self) -> str:
        return f"{self.display_name} [{self.code}] confidence={self.confidence:.2f}"


# Дальше идут конкретные продукты (Concrete Product) паттерна Фабричный метод.
# А именно, либо дефект, который есть в базе, либо дефект, указанный пользователем 
# и не относящийся к текущей базе дефектов.

class DefinedDefect(Defect):
    def __init__(self, bbox: BoundingBox, confidence: float, source: str, code: str):
        super().__init__(bbox, confidence, source)
        self._code = code.upper()

    @property
    def code(self) -> str:
        return self._code

    @property
    def display_name(self) -> str:
        return DEFECT_MAP.get(self._code, "Unknown defect")


class OtherDefect(Defect):
    _description: str = ""
    _author: str = ""

    @property
    def code(self) -> str:
        return "OTHER"

    @property
    def display_name(self) -> str:
        return "Other defect"

    def set_description(self, description: str) -> None:
        self._description = description

    def set_author(self, author: str) -> None:
        self._author = author