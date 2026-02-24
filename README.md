# Habit Tracking Application
Course: Object-Oriented and Functional Programming with Python (DLBDSOOFPP01)

---

## 1. Project Overview

This project implements a backend habit tracking application using Python.

The system applies:

- Object-Oriented Programming (OOP) for domain modeling  
- Functional Programming principles for analytics  
- SQLite for data persistence  
- Command-Line Interface (CLI) using argparse  
- Unit testing using pytest  

The application allows users to:

- Create daily and weekly habits  
- Delete habits  
- Check off habit completions  
- View completion history  
- Analyze streaks  
- Seed predefined habits  
- Insert 4 weeks of example tracking data  

---

## 2. Architecture

The application follows a layered architecture:

CLI → Repository → SQLite Database  
        ↓  
     Analytics Module  

### Components

- `cli.py` – Handles command-line interaction  
- `repository.py` – Database operations (CRUD)  
- `db.py` – Database initialization and connection  
- `models.py` – Domain models (Habit, Completion)  
- `analytics.py` – Functional streak calculations  

---

## 3. Database Schema

### Table: habits
- id (INTEGER PRIMARY KEY)  
- name (TEXT, UNIQUE)  
- task (TEXT)  
- periodicity (daily | weekly)  
- created_at (TEXT)  

### Table: completions
- id (INTEGER PRIMARY KEY)  
- habit_id (FOREIGN KEY)  
- completed_at (TEXT)  

---

## 4. Installation & Setup

Navigate to project directory:

```bash
cd ~/Desktop/habit-tracker
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

Set Python path:

```bash
export PYTHONPATH=src
```

---

## 5. Usage – Complete Workflow

### Basic Commands

Create a habit:

```bash
python -m habits.cli add --name "Workout" --task "20 min exercise" --period daily
```

List habits:

```bash
python -m habits.cli list
```

Check off a habit:

```bash
python -m habits.cli check --name "Workout"
```

View completion history:

```bash
python -m habits.cli history --name "Workout"
```

Delete a habit:

```bash
python -m habits.cli delete --name "Workout"
```

---

### Project Requirements Setup

Seed predefined habits (5 habits):

```bash
python -m habits.cli seed
```

Insert 4 weeks of example tracking data:

```bash
python -m habits.cli seed-data
```

---

### Analytics

List all habits:

```bash
python -m habits.cli analyze --all
```

List habits by periodicity:

```bash
python -m habits.cli analyze --period daily
```

Show longest streak overall:

```bash
python -m habits.cli analyze --longest
```

Show longest streak for a specific habit:

```bash
python -m habits.cli analyze --habit "Workout"
```

---

## 6. Streak Logic

- Daily habits are evaluated per calendar day.  
- Weekly habits are evaluated per ISO calendar week.  
- A streak represents consecutive completed periods.  
- Missing one period breaks the streak.  

---

## 7. Testing

Run tests:

```bash
pytest -q
```

All tests validate streak calculations for daily and weekly habits.

---

## 8. Technologies Used

- Python 3.9+  
- SQLite  
- argparse  
- pytest  

---

## 9. Author

Kiran Ravada  
IU Internationale Hochschule
