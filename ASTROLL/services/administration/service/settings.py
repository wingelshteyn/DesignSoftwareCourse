from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeSettings:
    max_room_members: int = 8
    realtime_rate_limit_per_minute: int = 120
    autosave_interval_seconds: int = 30


class RuntimeSettingsService:
    def __init__(self, settings: RuntimeSettings | None = None) -> None:
        self._settings = settings or RuntimeSettings()

    def get_settings(self) -> RuntimeSettings:
        return self._settings
