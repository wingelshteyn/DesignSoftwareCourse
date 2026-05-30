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
OTHER_DEFECT_CODE = "OTHER"


class UnknownPredictionLabelError(ValueError):
    """Raised when automatic detection returns an unsupported defect label."""


class InvalidManualDefectError(ValueError):
    """Raised when manual defect data violates domain rules."""


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
    def __init__(
        self,
        bbox: BoundingBox,
        confidence: float,
        source: str,
        custom_name: str,
        author: str,
        description: str | None = None,
    ) -> None:
        super().__init__(bbox, confidence, source)
        normalized_name = custom_name.strip()
        normalized_author = author.strip()
        if not normalized_name:
            raise InvalidManualDefectError("OtherDefect requires a non-empty custom_name.")
        if not normalized_author:
            raise InvalidManualDefectError("OtherDefect requires a non-empty author.")

        normalized_description = None
        if description is not None:
            stripped_description = description.strip()
            normalized_description = stripped_description or None

        self._custom_name = normalized_name
        self._author = normalized_author
        self._description = normalized_description

    @property
    def code(self) -> str:
        return OTHER_DEFECT_CODE

    @property
    def display_name(self) -> str:
        return self._custom_name

    def describe(self) -> str:
        details = (
            f"{self.display_name} [{self.code}] author={self._author} "
            f"confidence={self.confidence:.2f}"
        )
        if self.description:
            return f"{details} description={self._description}"
        return details
