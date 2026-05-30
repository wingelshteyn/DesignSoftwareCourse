from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentDependency:
    upstream: str
    downstream: str
    reason: str


COMPONENT_DEPENDENCIES = [
    ComponentDependency("accounts", "friends", "friends uses the shared user identity model"),
    ComponentDependency("accounts", "characters", "characters checks ownership by user id"),
    ComponentDependency("accounts", "rooms", "rooms identifies members by user id"),
    ComponentDependency("accounts", "game_session", "session commands require authenticated actors"),
    ComponentDependency("rooms", "game_session", "session uses room roster and host policy"),
    ComponentDependency("characters", "game_session", "session uses character tokens and sheet data"),
    ComponentDependency("board", "game_session", "session applies board commands and snapshots"),
    ComponentDependency("dice", "game_session", "session publishes dice roll events"),
    ComponentDependency("accounts", "administration", "administration uses RBAC policy"),
]


def has_cycles() -> bool:
    graph: dict[str, list[str]] = {}
    for dependency in COMPONENT_DEPENDENCIES:
        graph.setdefault(dependency.downstream, []).append(dependency.upstream)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for next_node in graph.get(node, []):
            if visit(next_node):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)
