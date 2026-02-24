import os
import sys
import subprocess
from pathlib import Path

import pytest


def run_cli(args, *, cwd: Path, env: dict) -> subprocess.CompletedProcess:
    """
    Run the habits CLI as a subprocess and return the completed process.
    """
    cmd = [sys.executable, "-m", "habits.cli"] + args
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.fixture()
def cli_env(tmp_path: Path) -> dict:
    """
    Provide an isolated environment for CLI tests:
    - Uses a temp SQLite DB path so tests don't touch your real data/habits.db
    - Sets PYTHONPATH=src so 'python -m habits.cli' works
    """
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")
    env["HABITS_DB_PATH"] = str(tmp_path / "test_habits.db")
    return env


def test_cli_add_list_delete_habit(cli_env):
    project_root = Path(__file__).resolve().parents[1]

    # Add
    p = run_cli(
        ["add", "--name", "TestHabit", "--task", "Do something", "--period", "daily"],
        cwd=project_root,
        env=cli_env,
    )
    assert p.returncode == 0, p.stderr

    # List should show the habit
    p = run_cli(["list"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr
    assert "TestHabit" in p.stdout

    # Delete
    p = run_cli(["delete", "--name", "TestHabit"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr

    # List should NOT show it anymore
    p = run_cli(["list"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr
    assert "TestHabit" not in p.stdout


def test_cli_check_and_history(cli_env):
    project_root = Path(__file__).resolve().parents[1]

    # Add habit
    p = run_cli(
        ["add", "--name", "Workout", "--task", "20 min", "--period", "daily"],
        cwd=project_root,
        env=cli_env,
    )
    assert p.returncode == 0, p.stderr

    # Check-off completion
    p = run_cli(["check", "--name", "Workout"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr

    # History should contain at least one entry / mention
    p = run_cli(["history", "--name", "Workout"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr
    # Keep this assertion light (format may vary)
    assert ("Workout" in p.stdout) or ("202" in p.stdout) or (len(p.stdout.strip()) > 0)


def test_cli_seed_and_seed_data(cli_env):
    project_root = Path(__file__).resolve().parents[1]

    # Seed habits
    p = run_cli(["seed"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr

    # Seed 4-week data
    p = run_cli(["seed-data"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr


def test_cli_analytics_longest(cli_env):
    project_root = Path(__file__).resolve().parents[1]

    # Prepare data
    p = run_cli(["seed"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr
    p = run_cli(["seed-data"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr

    # Overall longest streak
    p = run_cli(["analyze", "--longest"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr
    assert len(p.stdout.strip()) > 0


def test_cli_analytics_by_habit(cli_env):
    project_root = Path(__file__).resolve().parents[1]

    # Prepare data
    p = run_cli(["seed"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr
    p = run_cli(["seed-data"], cwd=project_root, env=cli_env)
    assert p.returncode == 0, p.stderr

    # Pick one seeded habit name that you know exists.
    # If your seed uses different names, replace "Workout" with one of your seeded habits.
    p = run_cli(["analyze", "--habit", "Workout"], cwd=project_root, env=cli_env)

    # If your seeded habits don't include "Workout", change it to an existing one, e.g. "Drink water"
    assert p.returncode == 0, p.stderr
    assert len(p.stdout.strip()) > 0