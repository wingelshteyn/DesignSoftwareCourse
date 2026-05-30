from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from apps.detection.defects import (
    BoundingBox,
    Defect,
    ModelPrediction,
    DEFECT_MAP,
    OTHER_DEFECT_CODE,
    InvalidManualDefectError,
)
from apps.detection.factories import (
    DefectFactoryRegistry,
    OtherDefectFactory,
    build_default_registry,
)


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
    Сервис фабричного метода.
    Использует ранее реализованный Фабричный метод.
    Создаёт объект дефекта из ручной разметки оператора.
    """
    def __init__(self, registry: DefectFactoryRegistry | None = None) -> None:
        self.registry = registry or build_default_registry()

    def mark(
        self,
        label: str,
        bbox: BoundingBox,
        confidence: float = 1.0,
        custom_name: str | None = None,
        author: str | None = None,
        description: str | None = None,
    ) -> Defect:
        normalized_label = label.upper()

        if normalized_label in DEFECT_MAP:
            if any(value is not None for value in (custom_name, author, description)):
                raise InvalidManualDefectError(
                    "Defined defects cannot include custom_name, author, or description."
                )
            prediction = ModelPrediction(
                label=normalized_label,
                bbox=bbox,
                confidence=confidence,
                source="manual",
            )
            factory = self.registry.get_factory(normalized_label)
            return factory.register_prediction(prediction)

        if normalized_label == OTHER_DEFECT_CODE:
            if custom_name is None:
                raise InvalidManualDefectError("Manual OTHER defect requires custom_name.")
            if author is None:
                raise InvalidManualDefectError("Manual OTHER defect requires author.")
            prediction = ModelPrediction(
                label=normalized_label,
                bbox=bbox,
                confidence=confidence,
                source="manual",
            )
            factory = OtherDefectFactory(
                custom_name=custom_name,
                author=author,
                description=description,
            )
            return factory.register_prediction(prediction)

        raise InvalidManualDefectError(
            f"Manual defect label must be one of {sorted(DEFECT_MAP)} or {OTHER_DEFECT_CODE}."
        )
