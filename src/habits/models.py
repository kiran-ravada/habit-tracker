from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Periodicity(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass(frozen=True)
class Habit:
    id: Optional[int]
    name: str
    task: str
    periodicity: Periodicity
    created_at: datetime


@dataclass(frozen=True)
class Completion:
    habit_id: int
    completed_at: datetime
