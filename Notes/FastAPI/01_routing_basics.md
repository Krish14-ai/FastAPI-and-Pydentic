# FastAPI — Routing Basics

## 1. What is Routing?

**Routing** is the process of mapping an HTTP request to a Python function.

```python
@app.get("/students")
def get_students():
    return {"message": "All students"}
```

When the client sends:

```text
GET /students
```

FastAPI calls:

```text
get_students()
```

### Basic idea

```text
HTTP Request
     ↓
  Route Match
     ↓
Python Function
     ↓
  Response
```

---

# 2. FastAPI App Setup

First, create a FastAPI application.

```python
from fastapi import FastAPI

app = FastAPI()
```

Create a basic route:

```python
@app.get("/")
def home():
    return {"message": "Hello World"}
```

Run the application with Uvicorn:

```bash
uvicorn main:app --reload
```

Where:

```text
main → Python file (main.py)
app  → FastAPI application object
```

The API will usually be available at:

```text
http://127.0.0.1:8000
```

---

# 3. HTTP Methods

HTTP methods tell the server **what action the client wants to perform**.

| Method | Purpose               |
| ------ | --------------------- |
| GET    | Retrieve data         |
| POST   | Create data           |
| PUT    | Replace/update data   |
| PATCH  | Partially update data |
| DELETE | Delete data           |

Example:

```python
@app.get("/students")
def get_students():
    ...

@app.post("/students")
def create_student():
    ...

@app.put("/students/{student_id}")
def update_student(student_id: int):
    ...

@app.patch("/students/{student_id}")
def update_student_partially(student_id: int):
    ...

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    ...
```

### Easy way to remember

```text
GET     → Read
POST    → Create
PUT     → Replace
PATCH   → Partial update
DELETE  → Delete
```

---

# 4. Basic Routes

A route is usually defined using:

```python
@app.get("/path")
def function():
    ...
```

Example:

```python
@app.get("/")
def home():
    return {"message": "Home"}

@app.get("/students")
def students():
    return {"message": "Students"}

@app.get("/about")
def about():
    return {"message": "About"}
```

The path is the URL part after the domain.

```text
/          → Home
/students  → Students
/about     → About
```

The function connected to the route is called the **route handler**.

---

# 5. Path Parameters

A **path parameter** is a variable value inside the URL path.

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}
```

Request:

```text
GET /students/10
```

FastAPI extracts:

```text
student_id = 10
```

### Type annotation

```python
student_id: int
```

tells FastAPI that the value should be an integer.

```text
/students/10      ✅
/students/25      ✅
/students/hello   ❌
```

### Multiple path parameters

```python
@app.get("/students/{student_id}/subjects/{subject_id}")
def get_subject(student_id: int, subject_id: int):
    return {
        "student_id": student_id,
        "subject_id": subject_id
    }
```

Request:

```text
GET /students/5/subjects/20
```

---

# 6. Query Parameters

**Query parameters** are values added to the URL after `?`.

Example:

```text
/students?age=20
```

FastAPI:

```python
@app.get("/students")
def get_students(age: int):
    return {"age": age}
```

Request:

```text
GET /students?age=20
```

FastAPI gets:

```text
age = 20
```

### Multiple query parameters

Use `&` between parameters.

```text
/students?age=20&gender=male
```

```python
@app.get("/students")
def get_students(age: int, gender: str):
    return {
        "age": age,
        "gender": gender
    }
```

### Default value

```python
@app.get("/students")
def get_students(limit: int = 10):
    return {"limit": limit}
```

If the client sends:

```text
/students
```

then:

```text
limit = 10
```

If the client sends:

```text
/students?limit=50
```

then:

```text
limit = 50
```

---

# 7. Path Parameter vs Query Parameter

This distinction is important.

## Path Parameter

```text
/students/10
```

Usually identifies **which resource** you want.

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    ...
```

Meaning:

> Get student `10`.

---

## Query Parameter

```text
/students?age=20
```

Usually provides a **filter or option**.

```python
@app.get("/students")
def get_students(age: int):
    ...
```

Meaning:

> Get students whose age is `20`.

### Quick rule

```text
PATH
/students/10
        ↑
   Which resource?

QUERY
/students?age=20
          ↑
   Filter / option
```

---

# 8. Request Body — Brief Introduction

The **request body** is data sent by the client to the server.

It is commonly used with `POST`, `PUT`, and `PATCH`.

Example JSON:

```json
{
    "name": "Krish",
    "age": 21
}
```

FastAPI commonly uses **Pydantic models** for request bodies.

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
```

Then:

```python
@app.post("/students")
def create_student(student: Student):
    return student
```

The detailed topic is covered in:

```text
02_pydantic.md
```

---

# 9. Request → Response Flow

A FastAPI request follows this general flow:

```text
Client
  ↓
HTTP Request
  ↓
FastAPI
  ↓
Route Matching
  ↓
Read Parameters
  ↓
Run Python Function
  ↓
Create Response
  ↓
Client
```

Example:

```text
GET /students/10
```

```text
      GET /students/10
             ↓
       Route Matching
             ↓
     student_id = 10
             ↓
      get_student(10)
             ↓
    {"student_id": 10}
             ↓
          Response
```

---

# 10. Small Example

Here is a small API combining the concepts:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Student API"}


@app.get("/students")
def get_students():
    return {
        "students": ["Krish", "Rahul", "Arun"]
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {
        "student_id": student_id
    }


@app.get("/search")
def search_students(
    name: str,
    limit: int = 10
):
    return {
        "name": name,
        "limit": limit
    }
```

### Example requests

Get all students:

```text
GET /students
```

Get one student:

```text
GET /students/10
```

Search students:

```text
GET /search?name=Krish&limit=5
```

---

# Quick Revision

```text
ROUTING
→ Maps a request to a Python function

HTTP METHOD
→ Defines the action

GET
→ Read

POST
→ Create

PUT
→ Replace

PATCH
→ Partial update

DELETE
→ Delete

PATH PARAMETER
→ /students/{student_id}

QUERY PARAMETER
→ /students?age=20

REQUEST BODY
→ Data sent to the server

RESPONSE
→ Data returned by the server
```

## Mental Model

```text
HTTP Method + Path
        ↓
      Route
        ↓
 Python Function
        ↓
    Response
```

> **Path = What resource?**
> **Query = Filter / option?**
> **Method = What action?**
> **Body = What data?**
