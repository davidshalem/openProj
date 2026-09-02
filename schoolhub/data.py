"""Sample in-memory data for SchoolHub.

In a real system these records would usually be stored in a database.
Changes made through the website live only until the Flask process restarts.
"""


# DEMO 2 – Add another dictionary to this list and refresh /students.
students = [
    {"id": 1, "name": "נועם כהן", "class_name": "י״ב1", "average": 94.0},
    {"id": 2, "name": "מאיה לוי", "class_name": "י״ב1", "average": 88.0},
    {"id": 3, "name": "איתי מזרחי", "class_name": "י״ב2", "average": 91.0},
    {"id": 4, "name": "שירה אברהם", "class_name": "י״א3", "average": 84.0},
    {"id": 5, "name": "יובל פרץ", "class_name": "י״ב2", "average": 97.0},
]


grades = {
    1: {"מתמטיקה": 92, "אנגלית": 94, "מדעי המחשב": 96},
    2: {"מתמטיקה": 86, "אנגלית": 90, "מדעי המחשב": 88},
    3: {"מתמטיקה": 89, "אנגלית": 90, "מדעי המחשב": 94},
    4: {"מתמטיקה": 82, "אנגלית": 87, "מדעי המחשב": 83},
    5: {"מתמטיקה": 98, "אנגלית": 94, "מדעי המחשב": 99},
}


teachers = [
    {"id": 1, "name": "דנה ישראלי", "subject": "מדעי המחשב"},
    {"id": 2, "name": "אורי רז", "subject": "מתמטיקה"},
    {"id": 3, "name": "יעל שלו", "subject": "אנגלית"},
    {"id": 4, "name": "רון ברק", "subject": "פיזיקה"},
]


classes = ["י״א3", "י״ב1", "י״ב2"]


open_tasks = [
    "בדיקת מבחני מתמטיקה",
    "פרסום מערכת שעות",
    "עדכון ציוני פרויקט",
]
