import os
import re
from datetime import date
from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import IntegrityError, Error as MySQLError

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Validation helpers (mirrors front-end rules so direct POST attacks are caught)
# ---------------------------------------------------------------------------
_NAME_RE   = re.compile(r"^[A-Za-z\u00C0-\u024F][A-Za-z\u00C0-\u024F '\-]{1,49}$")
_EMAIL_RE  = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')
_MATRIC_RE = re.compile(r'^VUG/[A-Z]{2,4}/\d{2}/\d{4,6}$')
_PHONE_RE  = re.compile(r'^[+\d][\d\s\-()]{7,}$')

VALID_GENDERS  = {'Male', 'Female'}
VALID_LEVELS   = {'100', '200', '300', '400', '500'}
VALID_FACULTIES = {
    'Natural and Applied Science', 'Computing', 'Engineering',
    'Social Sciences', 'Law', 'Management Science', 'Medicine',
}
FACULTY_DEPARTMENTS = {
    'Natural and Applied Science': {'Microbiology'},
    'Computing':                   {'Software Engineering', 'Computer Science'},
    'Engineering':                 {'Computer Engineering'},
    'Social Sciences':             {'Education Management', 'Mass Communication'},
    'Law':                         {'Law'},
    'Management Science':          {'Accounting'},
    'Medicine':                    {'Nursing'},
}
VALID_STATES = {
    'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue',
    'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
    'FCT (Abuja)', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina',
    'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo',
    'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara',
}
VALID_NATIONS = {
    'Nigerian', 'Beninese', 'Cameroonian', 'Chadian', 'Ghanaian', 'Ivorian',
    'Kenyan', 'Senegalese', 'South African', 'Togolese', 'Other',
}


def _validate(data):
    """Return a list of human-readable error strings, or [] if data is valid."""
    errors = []

    first = (data.get('first') or '').strip()
    last  = (data.get('last')  or '').strip()
    for value, label in ((first, 'First name'), (last, 'Last name')):
        if not value:
            errors.append(f'{label} is required.')
        elif not _NAME_RE.match(value):
            errors.append(f'{label} contains invalid characters.')

    dob = (data.get('dob') or '').strip()
    if not dob:
        errors.append('Date of birth is required.')
    else:
        try:
            born = date.fromisoformat(dob)
            today = date.today()
            if born >= today:
                errors.append('Date of birth must be in the past.')
            else:
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                if not (15 <= age <= 60):
                    errors.append('Age must be between 15 and 60.')
        except ValueError:
            errors.append('Enter a valid date of birth.')

    gender = (data.get('gender') or '').strip()
    if gender not in VALID_GENDERS:
        errors.append('Please select a valid gender.')

    email = (data.get('email') or '').strip().lower()
    if not email:
        errors.append('Email is required.')
    elif not _EMAIL_RE.match(email) or len(email) > 254:
        errors.append('Enter a valid email address.')

    phone = (data.get('phone') or '').strip()
    if not phone:
        errors.append('Phone number is required.')
    else:
        digits = re.sub(r'\D', '', phone)
        if not _PHONE_RE.match(phone) or not (10 <= len(digits) <= 15):
            errors.append('Enter a valid phone number.')

    matric = (data.get('matric') or '').strip().upper()
    if not matric:
        errors.append('Matric number is required.')
    elif not _MATRIC_RE.match(matric):
        errors.append('Matric number must be in the format VUG/SEN/24/12276.')

    level = (data.get('level') or '').strip()
    if level not in VALID_LEVELS:
        errors.append('Please select a valid level.')

    faculty = (data.get('faculty') or '').strip()
    if faculty not in VALID_FACULTIES:
        errors.append('Please select a valid faculty.')

    dept = (data.get('dept') or '').strip()
    if not dept:
        errors.append('Department is required.')
    elif faculty in FACULTY_DEPARTMENTS and dept not in FACULTY_DEPARTMENTS[faculty]:
        errors.append('Department does not belong to the selected faculty.')
    elif faculty not in FACULTY_DEPARTMENTS and dept:
        errors.append('Please select a valid faculty before choosing a department.')

    state = (data.get('state') or '').strip()
    if state and state not in VALID_STATES:
        errors.append('Please select a valid state.')

    nation = (data.get('nation') or '').strip()
    if nation and nation not in VALID_NATIONS:
        errors.append('Please select a valid nationality.')

    address = (data.get('address') or '').strip()
    if len(address) > 300:
        errors.append('Address must be 300 characters or fewer.')

    return errors


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
def _connect():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'student_biodata'),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('Biodata Form.html')


@app.route('/save-biodata', methods=['POST'])
def save_biodata():
    data = request.form

    errors = _validate(data)
    if errors:
        return render_template('Biodata Form.html', errors=errors, form=data), 422

    first  = data['first'].strip()
    last   = data['last'].strip()
    dob    = data['dob'].strip()
    gender = data['gender'].strip()
    state  = data.get('state', '').strip() or None
    nation = data.get('nation', '').strip() or None
    email  = data['email'].strip().lower()
    phone  = re.sub(r'[\s\-()]', '', data['phone'].strip())
    address = data.get('address', '').strip() or None
    matric = data['matric'].strip().upper()
    level  = data['level'].strip()
    faculty = data['faculty'].strip()
    dept   = data['dept'].strip()

    sql = """
        INSERT INTO students
            (first_name, last_name, dob, gender, state, nationality,
             email, phone, address, matric, level, faculty, department)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (first, last, dob, gender, state, nation,
              email, phone, address, matric, level, faculty, dept)

    database = None
    cursor   = None
    try:
        database = _connect()
        cursor   = database.cursor()
        cursor.execute(sql, values)
        database.commit()
    except IntegrityError as exc:
        app.logger.warning('Integrity error: %s', exc)
        msg = exc.msg if hasattr(exc, 'msg') else str(exc)
        if 'email' in msg.lower():
            conflict = 'That email address is already registered.'
        elif 'matric' in msg.lower():
            conflict = 'That matric number is already registered.'
        else:
            conflict = 'A duplicate record was detected. Please check your details.'
        return render_template(
            'Biodata Form.html',
            errors=[conflict],
            form=data,
        ), 409
    except MySQLError as exc:
        app.logger.error('Database error: %s', exc)
        return render_template(
            'Biodata Form.html',
            errors=['A database error occurred. Please try again later.'],
            form=data,
        ), 500
    finally:
        if cursor:
            cursor.close()
        if database:
            database.close()

    return render_template('success.html', name=first)


if __name__ == '__main__':
    app.run(debug=False)