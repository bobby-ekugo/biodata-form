# Student Biodata Form
Group 3 · VUA-SEN 305 Web Assignment

A Flask + MySQL web form that collects, validates, and stores student biodata.

---

## Project structure

```
biodata-form/
├── app.py                        # Flask application
├── static/
│   ├── script.js                 # Client-side validation
│   └── style.css                 # Styles (including error/status styles)
└── templates/
    ├── Biodata Form.html         # Main form
    └── success.html              # Confirmation page shown after a successful save
```

---

## Prerequisites

- Python 3.8+
- MySQL / MariaDB running locally

---

## Installation

```bash
pip install Flask mysql-connector-python
```

---

## Database setup

Run the following SQL in your local MySQL client (e.g. phpMyAdmin or the MySQL shell) **before** starting the app:

```sql
CREATE DATABASE student_biodata;

USE student_biodata;

CREATE TABLE students (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(100)  NOT NULL,
    last_name   VARCHAR(100)  NOT NULL,
    dob         DATE          NOT NULL,
    gender      VARCHAR(20)   NOT NULL,
    state       VARCHAR(100),
    nationality VARCHAR(100),
    email       VARCHAR(254)  NOT NULL UNIQUE,
    phone       VARCHAR(30)   NOT NULL,
    address     TEXT,
    matric      VARCHAR(50)   NOT NULL UNIQUE,
    level       VARCHAR(10)   NOT NULL,
    faculty     VARCHAR(100)  NOT NULL,
    department  VARCHAR(100)  NOT NULL,
    created_at  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
```

> **Already have the table?** Run this instead to add the unique constraint:
> ```sql
> ALTER TABLE students ADD UNIQUE (email);
> ```

---

## Configuration

Open `app.py` and update the `_connect()` function with your local database credentials:

```python
def _connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',          # ← your MySQL password
        database='student_biodata',
    )
```

---

## Running the app

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**.

> **Note:** `debug=False` is set in `app.py`. Change it to `True` only during local development — never on a production server, as it exposes an interactive traceback shell in the browser.

---

## How it works

1. The browser loads the form at `/`.
2. `script.js` validates every field client-side on blur, input, and change, and blocks submission if any field is invalid.
3. On a valid form, `form.submit()` sends a standard POST to `/save-biodata`.
4. `app.py` re-validates all fields server-side (so direct POST attacks are also caught).
5. On success the record is inserted and the user is redirected to `success.html`.
6. On failure (validation error, duplicate matric, or database error) the form is re-rendered with a list of error messages.

---

## Validation rules

| Field | Rules |
|---|---|
| First / Last name | Required · 2–50 letters, spaces, hyphens, apostrophes |
| Date of birth | Required · must be in the past · age 15–60 |
| Gender | Required · Male or Female |
| Email | Required · standard email format · max 254 chars |
| Phone | Required · 10–15 digits · leading `+` allowed |
| Address | Optional · max 300 characters |
| Matric number | Required · format `VUG/XXX/YY/NNNNN` (e.g. `VUG/SEN/24/12276`) · must be unique |
| Level | Required · 100 / 200 / 300 / 400 / 500 |
| Faculty | Required · must match a known faculty |
| Department | Required · must belong to the selected faculty |

---

## Error handling

| Scenario | Behaviour |
|---|---|
| Client-side invalid field | Inline error shown beneath the field; submit blocked |
| Server-side validation failure | Form re-rendered with a red error list (HTTP 422) |
| Duplicate matric number | Form re-rendered with "already registered" message (HTTP 409) |
| Database error | Form re-rendered with a generic error message (HTTP 500); full error logged server-side |
| Connection always closed | `cursor` and `database` are closed in a `finally` block regardless of success or failure |
## Running the app

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**.

> **Note:** `debug=False` is set in `app.py`. Change it to `True` only during local development — never on a production server, as it exposes an interactive traceback shell in the browser.

---

## How it works

1. The browser loads the form at `/`.
2. `script.js` validates every field client-side on blur, input, and change, and blocks submission if any field is invalid.
3. On a valid form, `form.submit()` sends a standard POST to `/save-biodata`.
4. `app.py` re-validates all fields server-side (so direct POST attacks are also caught).
5. On success the record is inserted and the user is redirected to `success.html`.
6. On failure (validation error, duplicate matric, or database error) the form is re-rendered with a list of error messages.

---

## Validation rules

| Field | Rules |
|---|---|
| First / Last name | Required · 2–50 letters, spaces, hyphens, apostrophes |
| Date of birth | Required · must be in the past · age 15–60 |
| Gender | Required · Male or Female |
| Email | Required · standard email format · max 254 chars |
| Phone | Required · 10–15 digits · leading `+` allowed |
| Address | Optional · max 300 characters |
| Matric number | Required · format `VUG/XXX/YY/NNNNN` (e.g. `VUG/SEN/24/12276`) · must be unique |
| Level | Required · 100 / 200 / 300 / 400 / 500 |
| Faculty | Required · must match a known faculty |
| Department | Required · must belong to the selected faculty |

---

## Error handling

| Scenario | Behaviour |
|---|---|
| Client-side invalid field | Inline error shown beneath the field; submit blocked |
| Server-side validation failure | Form re-rendered with a red error list (HTTP 422) |
| Duplicate matric number | Form re-rendered with "already registered" message (HTTP 409) |
| Database error | Form re-rendered with a generic error message (HTTP 500); full error logged server-side |
| Connection always closed | `cursor` and `database` are closed in a `finally` block regardless of success or failure |