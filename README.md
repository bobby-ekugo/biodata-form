# Student Biodata Form

Group 3 · VUA-SEN 305 Web Assignment

A Flask + MySQL web form that collects, validates, and stores student biodata.

---

## Project structure

```
biodata-form/
├── app.py                        # Flask application and server-side validation
├── README.md
├── .gitignore
├── static/
│   ├── script.js                 # Client-side validation and form behaviour
│   └── style.css                 # Styles (including error/status styles)
└── templates/
    ├── Biodata Form.html         # Main form
    └── success.html              # Confirmation page shown after a successful save
```

---

## Prerequisites

- Python 3.8+
- MySQL / MariaDB running locally (for example, XAMPP with the **MySQL** module started)

---

## Installation

```bash
python -m pip install Flask mysql-connector-python
```

Using `python -m pip` makes sure the packages are installed into the same Python that runs the app. This matters if you have more than one Python installed.

---

## Database setup

Run the following SQL in your local MySQL client (phpMyAdmin's **SQL** tab or the MySQL shell) **before** starting the app:

```sql
CREATE DATABASE IF NOT EXISTS student_biodata
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE student_biodata;

CREATE TABLE IF NOT EXISTS students (
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

> **Already have the table from an earlier version?** Add the unique email constraint with:
> ```sql
> ALTER TABLE students ADD UNIQUE (email);
> ```

Each team member needs to run this on their own machine, because the database is local and is not stored in the Git repository.

---

## Configuration

By default the app connects to XAMPP's MySQL: user `root`, no password, host `localhost`, database `student_biodata`. No changes are needed for a default XAMPP setup.

To use different settings, set these environment variables before starting the app:

| Variable | Default |
|---|---|
| `DB_HOST` | `localhost` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | *(empty)* |
| `DB_NAME` | `student_biodata` |

PowerShell: `$env:DB_PASSWORD="yourpassword"`
Command Prompt: `set DB_PASSWORD=yourpassword`
macOS / Linux: `export DB_PASSWORD=yourpassword`

The variables last only for that terminal session. Never commit a real password to the repository.

---

## Running the app

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**. Keep the terminal open while using the form.

> **Note:** `debug=False` is set in `app.py`. Change it to `True` only during local development. Never use debug mode on a production server, because it exposes an interactive traceback shell in the browser.

---

## How it works

1. The browser loads the form at `/`.
2. `script.js` validates every field client-side on blur, input, and change, and blocks submission if any field is invalid.
3. On a valid form, `form.submit()` sends a standard POST to `/save-biodata`.
4. `app.py` re-validates all fields server-side, so direct POST requests that bypass the browser are also checked.
5. On success the record is inserted and `success.html` is shown.
6. On failure (validation error, duplicate matric number or email, or database error) the form is shown again with a list of error messages and the values the student already entered.

> **Known behaviour:** refreshing the success page re-sends the form, which then fails with an "already registered" message. Use the **Submit another** link instead.

---

## Validation rules

| Field | Rules |
|---|---|
| First / Last name | Required · 2–50 letters, spaces, hyphens, apostrophes |
| Date of birth | Required · must be in the past · age 15–60 |
| Gender | Required · Male or Female |
| State of origin | Optional · must be one of the listed states |
| Nationality | Optional · must be one of the listed nationalities |
| Email | Required · standard email format · max 254 characters · must be unique · stored in lowercase |
| Phone | Required · 10–15 digits · leading `+` allowed · spaces, hyphens and brackets are removed before saving |
| Address | Optional · max 300 characters |
| Matric number | Required · format `VUG/XXX/YY/NNNNN` (e.g. `VUG/SEN/24/12276`) · must be unique · stored in uppercase |
| Level | Required · 100 / 200 / 300 / 400 / 500 |
| Faculty | Required · must match a known faculty |
| Department | Required · must belong to the selected faculty |

### Faculties and departments

| Faculty | Departments |
|---|---|
| Natural and Applied Science | Microbiology |
| Computing | Software Engineering, Computer Science |
| Engineering | Computer Engineering |
| Social Sciences | Education Management, Mass Communication |
| Law | Law |
| Management Science | Accounting |
| Medicine | Nursing |

This mapping exists in two places and must be kept in sync: `FACULTY_DEPARTMENTS` in `static/script.js` and in `app.py`. The department names must also match the options in `templates/Biodata Form.html`.

---

## Error handling

| Scenario | Behaviour |
|---|---|
| Client-side invalid field | Inline error shown beneath the field; submit blocked |
| Server-side validation failure | Form shown again with a red error list (HTTP 422) |
| Duplicate matric number or email | Form shown again with an "already registered" message (HTTP 409) |
| Database error | Form shown again with a generic error message (HTTP 500); full error logged server-side |
| Connection cleanup | `cursor` and `database` are closed in a `finally` block regardless of success or failure |

---

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Packages were installed into a different Python. Run `python -m pip install Flask mysql-connector-python`. |
| Cannot connect to MySQL (error 2003) | MySQL is not running. Start it in the XAMPP Control Panel. |
| `Unknown database 'student_biodata'` | The database setup SQL has not been run. |
| `Access denied for user 'root'` | Your MySQL root password is not empty. Set `DB_PASSWORD`. |
| Page will not load at `http://127.0.0.1:5000` | The Flask app is not running, or the address is missing the `:5000` port. |
| Department list is empty after choosing a faculty | The department option is missing from the HTML, or the names do not match the mapping. |

---

## Contributing

The `main` branch is protected, so changes cannot be pushed to it directly.

1. Create a branch: `git switch -c your-branch-name`
2. Commit your changes and push the branch.
3. Open a pull request into `main` on GitHub and merge it once approved.