from datetime import datetime, timedelta
from typing import List, Set, Tuple

from habits.models import Habit, Completion, Periodicity


def habits_by_periodicity(habits: List[Habit], periodicity: Periodicity) -> List[Habit]:
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def _day_key(dt: datetime) -> Tuple[int, int, int]:
    return (dt.year, dt.month, dt.day)


def _week_key(dt: datetime) -> Tuple[int, int]:
    iso = dt.isocalendar()
    return (iso[0], iso[1])


def _period_keys(completions: List[Completion], periodicity: Periodicity):
    key_fn = _day_key if periodicity == Periodicity.DAILY else _week_key
    keys = list(map(lambda c: key_fn(c.completed_at), completions))
    return sorted(set(keys))


def longest_streak_from_keys(keys, periodicity: Periodicity) -> int:
    if not keys:
        return 0

    key_set: Set = set(keys)
    longest = 1

    for k in keys:
        if periodicity == Periodicity.DAILY:
            dt = datetime(k[0], k[1], k[2])
            prev = _day_key(dt - timedelta(days=1))
        else:
            dt = datetime.fromisocalendar(k[0], k[1], 1)
            prev = _week_key(dt - timedelta(days=7))

        if prev in key_set:
            continue

        length = 1
        current = k

        while True:
            if periodicity == Periodicity.DAILY:
                dt = datetime(current[0], current[1], current[2]) + timedelta(days=1)
                next_key = _day_key(dt)
            else:
                dt = datetime.fromisocalendar(current[0], current[1], 1) + timedelta(days=7)
                next_key = _week_key(dt)

            if next_key in key_set:
                length += 1
                current = next_key
            else:
                break

        longest = max(longest, length)

    return longest


def longest_streak_for_habit(habit: Habit, completions: List[Completion]) -> int:
    keys = _period_keys(completions, habit.periodicity)
    return longest_streak_from_keys(keys, habit.periodicity)


def longest_streak_overall(habits: List[Habit], completions: List[Completion]) -> int:
    streaks = list(
        map(
            lambda h: longest_streak_for_habit(
                h,
                list(filter(lambda c: c.habit_id == h.id, completions)),
            ),
            habits,
        )
    )
    return max(streaks) if streaks else 0
