from django.shortcuts import render

# Create your views here.

from apps.detection.defects import BoundingBox
from apps.verification.commands import (
    VerificationAuditLog,
    ConfirmDefectsCommand,
    RejectDetectionCommand,
    ExcludeDefectCommand,
    AddManualDefectCommand,
    VerificationCommandInvoker,
)
from apps.verification.services import ManualDefectMarker, VerificationSession

# тут мы играем роль клиента (создаём получателя, команды и отправителя)
session = VerificationSession(
    control_record_id=101,
    operator_id=7,
    defects=[],
)

marker = ManualDefectMarker()
audit_log = VerificationAuditLog()
invoker = VerificationCommandInvoker(audit_log=audit_log)

# Оператор добавил вручную пропущенный дефект
add_command = AddManualDefectCommand(
    session=session,
    marker=marker,
    label="RS",
    bbox=BoundingBox(x=20, y=30, width=50, height=18),
)
invoker.set_command(add_command)
invoker.execute_command()

# Затем подтвердил результат
confirm_command = ConfirmDefectsCommand(session=session)
invoker.set_command(confirm_command)
invoker.execute_command()

for entry in audit_log.entries:
    print(entry.action_name, "->", entry.description)
