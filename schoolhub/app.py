"""A small, classroom-friendly Flask application."""

from flask import Flask, render_template, request

from data import classes, grades, open_tasks, students, teachers


app = Flask(__name__)


def find_student(student_id):
    """Return one student by id, or None when the id does not exist."""
    return next((student for student in students if student["id"] == student_id), None)


def update_average(student_id):
    """Recalculate a student's average after a grade changes."""
    student = find_student(student_id)
    student_grades = grades.get(student_id, {})

    if student and student_grades:
        student["average"] = round(sum(student_grades.values()) / len(student_grades), 1)


@app.route("/")
def dashboard():
    """Prepare dashboard statistics and send them to Jinja."""
    excellent_students_count = sum(
        1 for student in students if student["average"] > 90
    )

    # DEMO 1 – These Python values travel from Flask to Jinja and then to HTML.
    return render_template(
        "dashboard.html",
        students_count=len(students),
        teachers_count=len(teachers),
        classes_count=len(classes),
        open_tasks_count=len(open_tasks),
        excellent_students_count=excellent_students_count,
        open_tasks=open_tasks,
    )


# DEMO 5 – REQUEST → FLASK → DATA → JINJA → HTML
@app.route("/students", methods=["GET", "POST"])
def students_page():
    """Show, search and add students without a database."""
    message = None
    message_type = "success"

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        class_name = request.form.get("class_name", "").strip()

        if not name or not class_name:
            message = "יש למלא שם וכיתה"
            message_type = "error"
        else:
            new_id = max((student["id"] for student in students), default=0) + 1
            students.append(
                {"id": new_id, "name": name, "class_name": class_name, "average": 0.0}
            )
            grades[new_id] = {}
            message = f"התלמיד/ה {name} נוסף/ה בהצלחה"

    search_query = request.args.get("q", "").strip()
    filtered_students = students
    if search_query:
        filtered_students = [
            student
            for student in students
            if search_query.casefold() in student["name"].casefold()
        ]

    return render_template(
        "students.html",
        students=filtered_students,
        search_query=search_query,
        message=message,
        message_type=message_type,
    )


# DEMO 6 – GET displays data; POST sends form data back to Flask.
@app.route("/grades", methods=["GET", "POST"])
def grades_page():
    """Display one student's grades and allow a validated grade update."""
    message = None
    message_type = "success"

    raw_student_id = request.form.get("student_id") or request.args.get("student_id")
    try:
        selected_student_id = int(raw_student_id) if raw_student_id else students[0]["id"]
    except (TypeError, ValueError):
        selected_student_id = students[0]["id"]

    selected_student = find_student(selected_student_id)
    if selected_student is None:
        selected_student = students[0]
        selected_student_id = selected_student["id"]
        message = "התלמיד המבוקש לא נמצא"
        message_type = "error"

    if request.method == "POST":
        subject = request.form.get("subject", "")
        raw_grade = request.form.get("grade", "").strip()
        student_subjects = grades.get(selected_student_id, {})

        try:
            new_grade = int(raw_grade)
        except ValueError:
            message = "יש להזין ציון כמספר שלם"
            message_type = "error"
        else:
            # Validation: never trust input that arrived from the browser.
            if not 0 <= new_grade <= 100:
                message = "הציון חייב להיות בין 0 ל-100"
                message_type = "error"
            elif subject not in student_subjects:
                message = "המקצוע שנבחר אינו קיים"
                message_type = "error"
            else:
                student_subjects[subject] = new_grade
                update_average(selected_student_id)
                message = f"הציון ב{subject} עודכן בהצלחה"

    return render_template(
        "grades.html",
        students=students,
        selected_student=selected_student,
        student_grades=grades.get(selected_student_id, {}),
        message=message,
        message_type=message_type,
    )


if __name__ == "__main__":
    # debug=True is convenient for a live classroom demo: Flask reloads after edits.
    app.run(debug=True)
