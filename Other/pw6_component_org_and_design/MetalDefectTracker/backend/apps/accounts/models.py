from dataclasses import dataclass


@dataclass(slots=True)
class RBACPolicy:
    """
    Stable access-control policy of the Accounts component.
    Used as a representative class for component dependency analysis.
    """

    def can_manage_system(self, role: str) -> bool:
        return role == "administrator"

    def can_verify(self, role: str) -> bool:
        return role in {"operator", "administrator"}

    def can_view_analytics(self, role: str) -> bool:
        return role in {"technologist", "administrator"}
