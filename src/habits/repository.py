from datetime import datetime
from typing import Optional

from habits.db import get_conn
from habits.models import Habit, Completion, Periodicity


def _dt_to_str(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def _str_to_dt(s: str) -> datetime:
    return datetime.fromisoformat(s)


class HabitRepository:

    def create_habit(self, name: str, task: str, periodicity: Periodicity) -> Habit:
        now = datetime.now()
        conn = get_conn()
        with conn:
            cur = conn.execute(
                "INSERT INTO habits(name, task, periodicity, created_at) VALUES (?, ?, ?, ?)",
                (name, task, periodicity.value, _dt_to_str(now)),
            )
            habit_id = int(cur.lastrowid)
        conn.close()

        return Habit(
            id=habit_id,
            name=name,
            task=task,
            periodicity=periodicity,
            created_at=now,
        )

    def create_habit_if_missing(self, name: str, task: str, periodicity: Periodicity) -> bool:
        existing = self.get_habit_by_name(name)
        if existing is not None:
            return False
        self.create_habit(name, task, periodicity)
        return True

    def delete_habit(self, name: str) -> bool:
        conn = get_conn()
        with conn:
            cur = conn.execute("DELETE FROM habits WHERE name = ?", (name,))
            deleted = cur.rowcount > 0
        conn.close()
        return deleted

    def list_habits(self) -> list:
        conn = get_conn()
        cur = conn.execute(
            "SELECT id, name, task, periodicity, created_at FROM habits ORDER BY id"
        )
        rows = cur.fetchall()
        conn.close()

        habits = []
        for row in rows:
            hid, name, task, per, created_at = row
            habits.append(
                Habit(
                    id=int(hid),
                    name=name,
                    task=task,
                    periodicity=Periodicity(per),
                    created_at=_str_to_dt(created_at),
                )
            )
        return habits

    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        conn = get_conn()
        cur = conn.execute(
            "SELECT id, name, task, periodicity, created_at FROM habits WHERE name = ?",
            (name,),
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        hid, name, task, per, created_at = row
        return Habit(
            id=int(hid),
            name=name,
            task=task,
            periodicity=Periodicity(per),
            created_at=_str_to_dt(created_at),
        )

    def add_completion(self, habit_name: str, when: Optional[datetime] = None):
        habit = self.get_habit_by_name(habit_name)
        if habit is None:
            raise ValueError("Habit not found")

        when = when or datetime.now()

        conn = get_conn()
        with conn:
            conn.execute(
                "INSERT INTO completions(habit_id, completed_at) VALUES (?, ?)",
                (habit.id, _dt_to_str(when)),
            )
        conn.close()

    def list_completions(self, habit_name: str):
        habit = self.get_habit_by_name(habit_name)
        if habit is None:
            raise ValueError("Habit not found")

        conn = get_conn()
        cur = conn.execute(
            "SELECT habit_id, completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at",
            (habit.id,),
        )
        rows = cur.fetchall()
        conn.close()

        completions = []
        for hid, completed_at in rows:
            completions.append(
                Completion(
                    habit_id=int(hid),
                    completed_at=_str_to_dt(completed_at),
                )
            )
        return completions

    def list_all_completions(self):
        conn = get_conn()
        cur = conn.execute(
            "SELECT habit_id, completed_at FROM completions ORDER BY completed_at"
        )
        rows = cur.fetchall()
        conn.close()

        completions = []
        for hid, completed_at in rows:
            completions.append(
                Completion(
                    habit_id=int(hid),
                    completed_at=_str_to_dt(completed_at),
                )
            )
        return completions
