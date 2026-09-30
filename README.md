# Student Details REST API

A beginner-friendly Flask application that displays and updates student details through REST APIs. The application uses JSON request and response data and does not require a database or any additional service.

## Student fields

Each student has:

- `id`: unique student ID
- `name`: student name
- `age`: student age
- `course`: course name
- `email`: student email address

The sample records are stored in a Python list of dictionaries in memory. Any updates are lost when the Flask server restarts.

## Project files

- `app.py`: Flask application, sample data, validation, and API routes
- `requirements.txt`: Flask dependency
- `README.md`: setup and Postman instructions

## Windows Command Prompt setup

Open Command Prompt in this project folder:

```cmd
cd C:\Users\AIML-LAB1-22\Desktop\Portfolio
```

Activate the existing virtual environment:

```cmd
my_venv\Scripts\activate
```

Install Flask from the requirements file:

```cmd
python -m pip install -r requirements.txt
```

Start the application:

```cmd
python app.py
```

The API runs at `http://127.0.0.1:5000`.

## API endpoints

### 1. Get all students

- Method: `GET`
- URL: `http://127.0.0.1:5000/students`
- Headers: none required
- Body: none

Expected response: HTTP `200` and a JSON array containing all five students.

```json
[
	{
		"age": 20,
		"course": "Computer Science",
		"email": "aarav.sharma@example.com",
		"id": 1,
		"name": "Aarav Sharma"
	}
]
```

The actual response includes all sample records.

### 2. Get one student

- Method: `GET`
- URL: `http://127.0.0.1:5000/students/1`
- Headers: none required
- Body: none

Expected response: HTTP `200` with the student whose ID is `1`.

```json
{
	"age": 20,
	"course": "Computer Science",
	"email": "aarav.sharma@example.com",
	"id": 1,
	"name": "Aarav Sharma"
}
```

### 3. Update a student

PUT supports partial updates. Include one or more of `name`, `age`, `course`, and `email`. Fields not included in the request are preserved.

- Method: `PUT`
- URL: `http://127.0.0.1:5000/students/1`
- Required header: `Content-Type: application/json`
- Body type in Postman: `raw` and `JSON`

Example JSON request body:

```json
{
	"name": "Aarav Kumar",
	"age": 21,
	"course": "Artificial Intelligence",
	"email": "aarav.kumar@example.com"
}
```

Expected response: HTTP `200` with the updated student:

```json
{
	"age": 21,
	"course": "Artificial Intelligence",
	"email": "aarav.kumar@example.com",
	"id": 1,
	"name": "Aarav Kumar"
}
```

A partial update can contain only one field. For example, use the same URL and header with this body:

```json
{
	"course": "Cyber Security"
}
```

The response contains the new course and the previous name, age, and email.

### 4. Test a student ID that does not exist

Use either of these requests:

- Method: `GET`
- URL: `http://127.0.0.1:5000/students/999`

or:

- Method: `PUT`
- URL: `http://127.0.0.1:5000/students/999`
- Required header: `Content-Type: application/json`
- Body: `{ "name": "Unknown Student" }`

Expected response for either request: HTTP `404`.

```json
{
	"error": "Student not found."
}
```

### 5. Test invalid request data

Use this PUT request:

- Method: `PUT`
- URL: `http://127.0.0.1:5000/students/1`
- Required header: `Content-Type: application/json`
- Body type in Postman: `raw` and `JSON`

Invalid JSON example:

```text
{"age": }
```

Expected response: HTTP `400`.

```json
{
	"error": "Request body must contain valid JSON."
}
```

Invalid field value example:

```json
{
	"age": -5
}
```

Expected response: HTTP `400`.

```json
{
	"error": "age must be an integer between 1 and 120."
}
```

A PUT request without a JSON content type returns HTTP `400`. An empty JSON object, an unknown field, a blank name/course, or an invalid email also returns HTTP `400`.

## How the implementation works

1. Flask starts the application and keeps five sample student dictionaries in the `students` list.
2. `GET /students` serializes the complete list using `jsonify()`.
3. `GET /students/<int:student_id>` searches the list by ID and returns either the matching dictionary or a JSON `404` error.
4. `PUT /students/<int:student_id>` checks the content type, parses the JSON object, validates each supplied field, and updates only those fields.
5. The updated dictionary is returned with HTTP `200`. Since storage is in memory, restarting the server restores the original sample records.