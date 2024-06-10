from dataclasses import dataclass, asdict
from typing import List

@dataclass
class EditUserDto:
    email: str
    firstName: str
    lastName: str
    roles: List[str]

    def to_dict(self):
        return asdict(self)
