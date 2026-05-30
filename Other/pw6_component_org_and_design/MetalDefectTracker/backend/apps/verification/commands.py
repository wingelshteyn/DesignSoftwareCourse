from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from apps.detection.defects import BoundingBox, Defect

from .services import ManualDefectMarker, VerificationSession


@dataclass(slots=True)
class AuditEntry:
    control_record_id: int
    operator_id: int
    action_name: str
    description: str


class AuditLog(ABC):
    """Абстракция журнала аудита для принципа Инверсии зависимостей (DIP)."""

    @abstractmethod
    def add_entry(self, entry: AuditEntry) -> None:
        raise NotImplementedError


@dataclass(slots=True)
class VerificationAuditLog(AuditLog):
    entries: list[AuditEntry] = field(default_factory=list)

    def add_entry(self, entry: AuditEntry) -> None:
        self.entries.append(entry)


class NullAuditLog(AuditLog):
    """Пустая реализация журнала аудита."""

    def add_entry(self, entry: AuditEntry) -> None:
        return None


class VerificationCommand(ABC):
    """
    Абстрактная команда (Command) паттерна Команда.
    Описывает общий для всех команд интерфейс.
    """
    def __init__(self, session: VerificationSession) -> None:
        self.session = session

    @abstractmethod
    def execute(self) -> str:
        raise NotImplementedError

# Дальше идут конкретные команды паттерна Команда

class ConfirmDefectsCommand(VerificationCommand):
    def execute(self) -> str:
        self.session.confirm_defects()
        return "Operator confirmed detected defects."


class RejectDetectionCommand(VerificationCommand):
    def execute(self) -> str:
        self.session.reject_detection()
        return "Operator rejected automatic detection result."


class ExcludeDefectCommand(VerificationCommand):
    def __init__(self, session: VerificationSession, defect: Defect) -> None:
        super().__init__(session)
        self.defect = defect

    def execute(self) -> str:
        self.session.exclude_defect(self.defect)
        return f"Operator excluded defect {self.defect.code}."


class AddManualDefectCommand(VerificationCommand):
    def __init__(
        self,
        session: VerificationSession,
        marker: ManualDefectMarker,
        label: str,
        bbox: BoundingBox,
        custom_name: str | None = None,
        author: str | None = None,
        description: str | None = None,
    ) -> None:
        super().__init__(session)
        self.marker = marker
        self.label = label
        self.bbox = bbox
        self.custom_name = custom_name
        self.author = author
        self.description = description

    def execute(self) -> str:
        defect = self.marker.mark(
            label=self.label,
            bbox=self.bbox,
            confidence=1.0,
            custom_name=self.custom_name,
            author=self.author,
            description=self.description,
        )
        self.session.add_manual_defect(defect)
        return f"Operator added manual defect {defect.code}."


class VerificationCommandInvoker:
    """
    Отправитель (Invoker) паттерна Команда.
    Единая точка выполнения команд и записи аудита.
    """
    def __init__(self, audit_log: AuditLog | None = None) -> None:
        self.audit_log = audit_log
        self._command: VerificationCommand | None = None
    
    def set_command(self, command: VerificationCommand) -> None:
        self._command = command
    
    def execute_command(self) -> str:
        if not self._command:
            raise ValueError("No command set for execution.")
        result = self._command.execute()

        self.audit_log.add_entry(
            AuditEntry(
                control_record_id=self._command.session.control_record_id,
                operator_id=self._command.session.operator_id,
                action_name=self._command.__class__.__name__,
                description=result,
            )
        )
        return result
