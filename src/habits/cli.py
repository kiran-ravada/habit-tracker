import argparse

from habits.db import init_db
from habits.models import Periodicity
from habits.repository import HabitRepository
from habits.analytics import habits_by_periodicity


def main():
    init_db()
    repo = HabitRepository()

    parser = argparse.ArgumentParser(prog="habits")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a habit")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--task", required=True)
    p_add.add_argument("--period", choices=["daily", "weekly"], required=True)

    p_list = sub.add_parser("list", help="List habits")
    p_list.add_argument("--period", choices=["daily", "weekly"], required=False)

    p_check = sub.add_parser("check", help="Check off a habit")
    p_check.add_argument("--name", required=True)

    p_delete = sub.add_parser("delete", help="Delete a habit")
    p_delete.add_argument("--name", required=True)

    p_history = sub.add_parser("history", help="Show completion history for a habit")
    p_history.add_argument("--name", required=True)

    sub.add_parser("seed", help="Create 5 predefined habits")
    sub.add_parser("seed-data", help="Insert 4 weeks of example completion data")

    p_analyze = sub.add_parser("analyze", help="Analyze habits and streaks")
    p_analyze.add_argument("--all", action="store_true")
    p_analyze.add_argument("--period", choices=["daily", "weekly"])
    p_analyze.add_argument("--longest", action="store_true")
    p_analyze.add_argument("--habit")

    args = parser.parse_args()

    if args.cmd == "add":
        repo.create_habit(args.name, args.task, Periodicity(args.period))
        print("Habit added.")

    elif args.cmd == "list":
        habits = repo.list_habits()
        if args.period:
            habits = habits_by_periodicity(habits, Periodicity(args.period))
        for h in habits:
            print(f"{h.name} ({h.periodicity.value}) - {h.task}")

    elif args.cmd == "check":
        repo.add_completion(args.name)
        print("Habit checked off.")

    elif args.cmd == "delete":
        deleted = repo.delete_habit(args.name)
        print("Deleted." if deleted else "Habit not found.")

    elif args.cmd == "history":
        items = repo.list_completions(args.name)
        if not items:
            print("(no completions yet)")
        for c in items:
            print(c.completed_at.isoformat(timespec="seconds"))
    elif args.cmd == "seed":
        predefined = [
            ("Workout", "20 min exercise", Periodicity.DAILY),
            ("Drink water", "Drink 2 liters of water", Periodicity.DAILY),
            ("Read", "Read 10 pages", Periodicity.DAILY),
            ("Clean house", "Clean apartment", Periodicity.WEEKLY),
            ("Call family", "Call family members", Periodicity.WEEKLY),
        ]

        created_count = 0
        for name, task, period in predefined:
            if repo.create_habit_if_missing(name, task, period):
                created_count += 1

        print(f"✅ Seed complete. Created {created_count} new habits.")
    elif args.cmd == "seed-data":
        from datetime import datetime, timedelta

        # last 28 days (including today)
        today = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        days = [today - timedelta(days=i) for i in range(0, 28)]

        # DAILY habits: create realistic completion patterns
        # Workout: 5 days/week (skip some days)
        for d in days:
            if d.weekday() in [0, 1, 2, 3, 4]:  # Mon-Fri
                repo.add_completion("Workout", d)

        # Drink water: almost every day, skip 3 random-ish days
        skip = {3, 11, 19}
        for i, d in enumerate(days):
            if i not in skip:
                repo.add_completion("Drink water", d)

        # Read: 4 days/week
        for d in days:
            if d.weekday() in [0, 2, 4, 6]:  # Mon, Wed, Fri, Sun
                repo.add_completion("Read", d)

        # WEEKLY habits: 1 completion per week (some missed weeks to show struggles)
        weeks = [today - timedelta(days=7*i) for i in range(0, 4)]

        # Clean house: done 3 out of 4 weeks
        repo.add_completion("Clean house", weeks[0])
        repo.add_completion("Clean house", weeks[1])
        repo.add_completion("Clean house", weeks[3])

        # Call family: done all 4 weeks
        for w in weeks:
            repo.add_completion("Call family", w)

        print("✅ Seed-data complete. Inserted example completions for 4 weeks.")

    elif args.cmd == "analyze":
        from habits.analytics import (
            habits_by_periodicity,
            longest_streak_overall,
            longest_streak_for_habit,
        )

        habits = repo.list_habits()
        completions = repo.list_all_completions()

        if args.all:
            for h in habits:
                print(f"- {h.name} ({h.periodicity.value})")

        elif args.period:
            filtered = habits_by_periodicity(habits, Periodicity(args.period))
            for h in filtered:
                print(f"- {h.name} ({h.periodicity.value})")

        elif args.longest:
            print(longest_streak_overall(habits, completions))

        elif args.habit:
            h = repo.get_habit_by_name(args.habit)
            if h is None:
                print("Habit not found.")
            else:
                cs = list(filter(lambda c: c.habit_id == h.id, completions))
                print(longest_streak_for_habit(h, cs))

        else:
            print('Choose one: --all OR --period daily|weekly OR --longest OR --habit "Name"')


if __name__ == "__main__":
    main()
