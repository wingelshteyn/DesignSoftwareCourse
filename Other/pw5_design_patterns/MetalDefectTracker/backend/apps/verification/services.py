from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from apps.detection.defects import BoundingBox, Defect, ModelPrediction
from apps.detection.factories import DefectFactoryRegistry, build_default_registry


class VerificationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(slots=True)
class VerificationSession:
    """
    Получатель (Receiver) паттерна Команда.
    Содержит бизнес-логику для управления сессией верификации, 
    хранения текущего статуса и списка дефектов.
    """
    control_record_id: int
    operator_id: int
    defects: list[Defect] = field(default_factory=list)
    status: VerificationStatus = VerificationStatus.PENDING

    def confirm_defects(self) -> None:
        self.status = VerificationStatus.ACCEPTED

    def reject_detection(self) -> None:
        self.status = VerificationStatus.REJECTED

    def exclude_defect(self, defect: Defect) -> None:
        self.defects.remove(defect)

    def add_manual_defect(self, defect: Defect) -> None:
        self.defects.append(defect)


class ManualDefectMarker:
    """
    Использует ранее реализованный Фабричный метод.
    Создаёт объект дефекта из ручной разметки оператора.
    """
    def __init__(self, registry: DefectFactoryRegistry | None = None) -> None:
        self.registry = registry or build_default_registry()

    def mark(self, label: str, bbox: BoundingBox, confidence: float = 1.0) -> Defect:
        prediction = ModelPrediction(
            label=label,
            bbox=bbox,
            confidence=confidence,
            source="manual",
        )
        factory = self.registry.get_factory(label)
        return factory.create_defect(prediction)