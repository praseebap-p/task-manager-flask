from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("tasks.db")

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, status TEXT)")

    if request.method == "POST":
        task = request.form.get("task")
        cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "Pending"))
        conn.commit()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/complete/<int:id>")
def complete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status='Done' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
