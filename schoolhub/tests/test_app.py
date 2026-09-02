"""Small end-to-end tests for the classroom project."""

import unittest

from app import app
from data import grades, students


class SchoolHubTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.students_snapshot = [student.copy() for student in students]
        self.grades_snapshot = {
            student_id: student_grades.copy()
            for student_id, student_grades in grades.items()
        }

    def tearDown(self):
        students[:] = self.students_snapshot
        grades.clear()
        grades.update(self.grades_snapshot)

    def test_all_pages_load(self):
        for path in ["/", "/students", "/grades"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_student_search(self):
        response = self.client.get("/students?q=נועם")
        self.assertIn("נועם כהן".encode(), response.data)
        self.assertNotIn("מאיה לוי".encode(), response.data)

    def test_add_student(self):
        response = self.client.post(
            "/students",
            data={"name": "רוני ישראלי", "class_name": "י״ב3"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("רוני ישראלי".encode(), response.data)
        self.assertEqual(students[-1]["name"], "רוני ישראלי")

    def test_update_grade_and_average(self):
        response = self.client.post(
            "/grades",
            data={"student_id": "1", "subject": "מתמטיקה", "grade": "100"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(grades[1]["מתמטיקה"], 100)
        self.assertIn("עודכן בהצלחה".encode(), response.data)

    def test_grade_above_100_is_rejected(self):
        original_grade = grades[1]["מתמטיקה"]
        response = self.client.post(
            "/grades",
            data={"student_id": "1", "subject": "מתמטיקה", "grade": "150"},
        )
        self.assertEqual(grades[1]["מתמטיקה"], original_grade)
        self.assertIn("בין 0 ל-100".encode(), response.data)

    def test_negative_grade_is_rejected(self):
        original_grade = grades[1]["מתמטיקה"]
        response = self.client.post(
            "/grades",
            data={"student_id": "1", "subject": "מתמטיקה", "grade": "-1"},
        )
        self.assertEqual(grades[1]["מתמטיקה"], original_grade)
        self.assertIn("בין 0 ל-100".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
