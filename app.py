from flask import Flask, render_template, request
import mysql.connector

    
app = Flask(__name__)

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_biodata")

@app.route('/')
def home():
    return render_template('Biodata Form.html')

@app.route('/save-biodata', methods=['POST'])
def save_biodata():
    data = request.form
    database = connect_to_database()
    cursor = database.cursor()
    sql = """INSERT INTO students
    (first_name, last_name, dob, gender, state, nationality,email,phone,address,matric,level,faculty,
    department)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    values = (
        data["first"],data["last"],data["dob"],data["gender"],data.get("state") or None, data.get("nation") or None, data["email"],
        data["phone"],data.get("address") or None, data["matric"], data["level"],
        data["faculty"], data["dept"])

    cursor.execute(sql, values)
    database.commit()
    cursor.close()
    database.close()
    return "Biodata saved successfully!"

if __name__ == "__main__":
    app.run(debug=True)