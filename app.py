from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# =========================
# Database Connection
# =========================
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=AI_Interview;'
        'Trusted_Connection=yes;'
    )

# =========================
# Home Page
# =========================
@app.route('/')
def home():
    return render_template('index.html')

# =========================
# Register
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Users (Name, Email, Password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# =========================
# Login
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Users WHERE Email=? AND Password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')

# =========================
# Dashboard
# =========================
@app.route('/dashboard')
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM InterviewHistory")
    total_interviews = cursor.fetchone()[0]

    cursor.execute("SELECT ISNULL(MAX(Score),0) FROM InterviewHistory")
    highest_score = cursor.fetchone()[0]

    cursor.execute("SELECT ISNULL(AVG(Score),0) FROM InterviewHistory")
    average_score = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total_interviews=total_interviews,
        highest_score=highest_score,
        average_score=round(float(average_score), 2)
    )

# =========================
# Questions
# =========================
@app.route('/questions/<category>', methods=['GET', 'POST'])
def questions(category):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':

        answers = request.form.getlist('answers')

        for answer in answers:

            cursor.execute(
                "INSERT INTO Answers (UserAnswer) VALUES (?)",
                (answer,)
            )

        score = min(len(answers) * 2, 10)

        cursor.execute(
            "INSERT INTO InterviewHistory (Category, Score) VALUES (?, ?)",
            (category, score)
        )

        conn.commit()
        conn.close()

        if score >= 8:
            feedback = """
Excellent Performance!
Strong communication skills.
Good confidence level.
Ready for interviews.
"""

        elif score >= 5:
            feedback = """
Good Performance!
Practice technical concepts more.
Improve confidence while answering.
"""

        else:
            feedback = """
Needs Improvement!
Practice common interview questions.
Improve communication skills.
"""

        return render_template(
            'result.html',
            score=score,
            feedback=feedback
        )

    cursor.execute(
        "SELECT QuestionText FROM Questions WHERE Category=?",
        (category,)
    )

    questions = cursor.fetchall()

    conn.close()

    return render_template(
        'questions.html',
        questions=questions
    )

# =========================
# Result
# =========================
@app.route('/result')
def result():
    return render_template('result.html')

# =========================
# Interview History
# =========================
@app.route('/history')
def history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT Category,
               Score,
               InterviewDate
        FROM InterviewHistory
        ORDER BY InterviewDate DESC
        """
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        'history.html',
        records=records
    )

# =========================
# Logout
# =========================
@app.route('/logout')
def logout():
    return redirect('/login')

# =========================
# Run Application
# =========================
if __name__ == '__main__':
    app.run(debug=True)
