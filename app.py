from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.get("/")
def home():
    """Render the portfolio landing page."""
    return render_template("index.html")

# This sample data is stored in memory and resets whenever the server restarts.
students = [
    {
        "id": 1,
        "name": "Aarav Sharma",
        "age": 20,
        "course": "Computer Science",
        "email": "aarav.sharma@example.com",
    },
    {
        "id": 2,
        "name": "Diya Patel",
        "age": 21,
        "course": "Information Technology",
        "email": "diya.patel@example.com",
    },
    {
        "id": 3,
        "name": "Rohan Mehta",
        "age": 19,
        "course": "Business Administration",
        "email": "rohan.mehta@example.com",
    },
    {
        "id": 4,
        "name": "Ananya Singh",
        "age": 22,
        "course": "Data Science",
        "email": "ananya.singh@example.com",
    },
    {
        "id": 5,
        "name": "Vikram Rao",
        "age": 20,
        "course": "Mechanical Engineering",
        "email": "vikram.rao@example.com",
    },
]

UPDATABLE_FIELDS = {"name", "age", "course", "email"}


def find_student(student_id):
    """Return the student with the requested ID, or None if it is missing."""
    return next((student for student in students if student["id"] == student_id), None)


def validate_student_updates(data):
    """Return an error message when an update payload contains invalid data."""
    unexpected_fields = set(data) - UPDATABLE_FIELDS
    if unexpected_fields:
        fields = ", ".join(sorted(unexpected_fields))
        return f"Invalid field(s): {fields}. Only name, age, course, and email can be updated."

    if not data:
        return "Request JSON must contain at least one field to update."

    if "name" in data and (not isinstance(data["name"], str) or not data["name"].strip()):
        return "name must be a non-empty string."

    if "age" in data and (
        isinstance(data["age"], bool)
        or not isinstance(data["age"], int)
        or not 1 <= data["age"] <= 120
    ):
        return "age must be an integer between 1 and 120."

    if "course" in data and (
        not isinstance(data["course"], str) or not data["course"].strip()
    ):
        return "course must be a non-empty string."

    if "email" in data:
        email = data["email"]
        if not isinstance(email, str) or email.count("@") != 1:
            return "email must be a valid email address."
        local_part, domain = email.split("@")
        if not local_part or not domain or "." not in domain:
            return "email must be a valid email address."

    return None



@app.get("/students")
def get_students():
    """Return all students as a JSON array."""
    return jsonify(students), 200


@app.get("/students/<int:student_id>")
def get_student(student_id):
    """Return one student by ID."""
    student = find_student(student_id)
    if student is None:
        return jsonify({"error": "Student not found."}), 404
    return jsonify(student), 200


@app.put("/students/<int:student_id>")
def update_student(student_id):
    """Partially update an existing student with JSON request data."""
    student = find_student(student_id)
    if student is None:
        return jsonify({"error": "Student not found."}), 404

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must contain valid JSON."}), 400
    if not isinstance(data, dict):
        return jsonify({"error": "Request JSON must be an object."}), 400

    validation_error = validate_student_updates(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    # Only supplied fields are changed; all other student details are preserved.
    for field, value in data.items():
        student[field] = value.strip() if isinstance(value, str) else value

    return jsonify(student), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
