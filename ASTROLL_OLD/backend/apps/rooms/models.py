from dataclasses import dataclass, field


@dataclass
class RoomMember:
    user_id: int
    readonly: bool = False


@dataclass
class Room:
    room_id: str
    host_id: int
    members: dict[int, RoomMember] = field(default_factory=dict)

    def add_member(self, user_id: int) -> None:
        self.members[user_id] = RoomMember(user_id=user_id)

    def set_readonly(self, user_id: int, readonly: bool) -> None:
        self.members[user_id].readonly = readonly

    def is_host(self, user_id: int) -> bool:
        return self.host_id == user_id
