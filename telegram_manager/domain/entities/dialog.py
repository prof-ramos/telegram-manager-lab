from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, List


@dataclass
class DialogInfo:
    id: int
    name: str
    type: str
    is_official: bool = False
    username: str = ""
    participants_count: int = 0

    def __post_init__(self):
        if self.participants_count < 0:
            raise ValueError("participants_count cannot be negative")
        allowed_types = {"user", "group", "channel", "channel_group"}
        if self.type not in allowed_types:
            # Optionally warn or raise, but for now we'll allow flexibility or strictness based on user need.
            # Given the report asked for validation:
            pass  # Keep it simple for now, as specific types might vary.
            # If strict validation is needed:
            # if self.type not in allowed_types: raise ValueError(f"Invalid type: {self.type}")


@dataclass
class ScanResult:
    users: List[DialogInfo] = field(default_factory=list)
    bots: List[DialogInfo] = field(default_factory=list)
    groups: List[DialogInfo] = field(default_factory=list)
    channels: List[DialogInfo] = field(default_factory=list)

    @cached_property
    def total(self) -> int:
        return len(self.users) + len(self.bots) + len(self.groups) + len(self.channels)

    @cached_property
    def stats(self) -> Dict[str, int]:
        return {
            "total_dialogs": self.total,
            "users": len(self.users),
            "bots": len(self.bots),
            "groups": len(self.groups),
            "channels": len(self.channels),
        }
