import json
from datetime import date, timedelta

DATA_FILE = "study_data.json"


def load_sessions():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_sessions(sessions):
    with open(DATA_FILE, "w") as file:
        json.dump(sessions, file, indent=4)

def add_session(sessions):
    subject = input("Subject: ").strip()

    while True:
        try:
            duration = int(input("Duration (minutes): "))

            if duration <= 0:
                print("Duration must be greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    session = {
        "subject": subject,
        "duration": duration,
        "date": date.today().isoformat()
    }

    sessions.append(session)
    save_sessions(sessions)

    print("Session saved!")


def view_sessions(sessions):
    if not sessions:
        print("No study sessions found.")
        return

    print("\n===== Study Sessions =====")

    for i, session in enumerate(sessions, start=1):
        session_date = session.get("date", "Unknown date")
        print(f"{i}. {session['subject']} - {format_time(session['duration'])} - {session_date}")
        print(f"{i}. {session['subject']} - {format_time(session['duration'])} - {date}")


def delete_session(sessions):
    if not sessions:
        print("No study sessions found.")
        return

    view_sessions(sessions)

    try:
        choice = int(input("\nEnter the session number to delete: "))

        if choice < 1 or choice > len(sessions):
            print("Invalid session number.")
            return

        deleted = sessions.pop(choice - 1)
        save_sessions(sessions)

        print(f"Deleted: {deleted['subject']} - {format_time(deleted['duration'])}")

    except ValueError:
        print("Please enter a valid number.")


def edit_session(sessions):
    if not sessions:
        print("No study sessions found.")
        return

    view_sessions(sessions)

    try:
        choice = int(input("\nEnter the session number to edit: "))

        if choice < 1 or choice > len(sessions):
            print("Invalid session number.")
            return

        session = sessions[choice - 1]

        new_subject = input(
            f"New subject (press Enter to keep '{session['subject']}'): "
        ).strip()

        new_duration = input(
            f"New duration (press Enter to keep {session['duration']} minutes): "
        ).strip()

        if new_subject:
            session["subject"] = new_subject

        if new_duration:
            duration = int(new_duration)

            if duration <= 0:
                print("Duration must be greater than 0.")
                return

            session["duration"] = duration

        save_sessions(sessions)

        print("Session updated!")

    except ValueError:
        print("Please enter a valid number.")


def format_time(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours > 0:
        return f"{hours}h {remaining_minutes}m"
    else:
        return f"{remaining_minutes}m"


def show_weekly_statistics(sessions):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    weekly_total = 0
    subject_totals = {}

    for session in sessions:
        session_date = session.get("date")

        if session_date:
            session_date = date.fromisoformat(session_date)

            if start_of_week <= session_date <= today:
                duration = session["duration"]
                subject = session["subject"]

                weekly_total += duration
                subject_totals[subject] = subject_totals.get(subject, 0) + duration

    print("\n===== This Week =====")
    print(f"Total study time: {format_time(weekly_total)}")

    if subject_totals:
        print("\nTime by subject:")

        for subject, duration in subject_totals.items():
            print(f"{subject}: {format_time(duration)}")
    else:
        print("No sessions recorded this week.")


def show_statistics(sessions):
    if not sessions:
        print("No study sessions found.")
        return

    total_time = sum(session["duration"] for session in sessions)

    subject_totals = {}

    for session in sessions:
        subject = session["subject"]
        duration = session["duration"]

        if subject in subject_totals:
            subject_totals[subject] += duration
        else:
            subject_totals[subject] = duration

    print("\n===== Statistics =====")
    print(f"Total study time: {format_time(total_time)}")

    print("\nTime by subject:")

    for subject, duration in subject_totals.items():
        print(f"{subject}: {format_time(duration)}")


def main():
    sessions = load_sessions()

    while True:
        print("\n===== StudyTrack =====")
        print("1. Add study session")
        print("2. View sessions")
        print("3. View statistics")
        print("4. Weekly statistics")
        print("5. Edit a session")
        print("6. Delete a session")
        print("7. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            show_statistics(sessions)
        elif choice == "4":
            show_weekly_statistics(sessions)
        elif choice == "5":
            edit_session(sessions)
        elif choice == "6":
            delete_session(sessions)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1-7.")


if __name__ == "__main__":
    main()