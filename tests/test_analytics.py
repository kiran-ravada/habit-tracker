from datetime import datetime

from habits.analytics import longest_streak_for_habit
from habits.models import Habit, Completion, Periodicity


def test_daily_streak_simple():
    habit = Habit(id=1, name="H", task="T", periodicity=Periodicity.DAILY, created_at=datetime.now())

    completions = [
        Completion(habit_id=1, completed_at=datetime(2026, 2, 1, 10, 0, 0)),
        Completion(habit_id=1, completed_at=datetime(2026, 2, 2, 10, 0, 0)),
        Completion(habit_id=1, completed_at=datetime(2026, 2, 3, 10, 0, 0)),
    ]

    assert longest_streak_for_habit(habit, completions) == 3


def test_daily_streak_with_gap():
    habit = Habit(id=1, name="H", task="T", periodicity=Periodicity.DAILY, created_at=datetime.now())

    completions = [
        Completion(habit_id=1, completed_at=datetime(2026, 2, 1, 10, 0, 0)),
        Completion(habit_id=1, completed_at=datetime(2026, 2, 2, 10, 0, 0)),
        # gap on Feb 3
        Completion(habit_id=1, completed_at=datetime(2026, 2, 4, 10, 0, 0)),
    ]

    assert longest_streak_for_habit(habit, completions) == 2


def test_weekly_streak_simple():
    habit = Habit(id=1, name="H", task="T", periodicity=Periodicity.WEEKLY, created_at=datetime.now())

    # ISO week continuity: 2026-02-02 and 2026-02-09 are consecutive weeks
    completions = [
        Completion(habit_id=1, completed_at=datetime(2026, 2, 2, 10, 0, 0)),
        Completion(habit_id=1, completed_at=datetime(2026, 2, 9, 10, 0, 0)),
        Completion(habit_id=1, completed_at=datetime(2026, 2, 16, 10, 0, 0)),
    ]

    assert longest_streak_for_habit(habit, completions) == 3
