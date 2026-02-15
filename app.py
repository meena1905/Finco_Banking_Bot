from flask import Flask, request, render_template_string, redirect
from predict import generate_llm_reply, score_priority, vectorizer, model
from database import init_db, save_complaint, get_pending_complaints, add_employee_reply

# Initialize SQLite database
init_db()

app = Flask(__name__)

# ---------------- LOGIN PAGE ----------------
login_template = """
<!DOCTYPE html>
<html>
<head>
    <title>FinCo Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background:#f4f7fb; }
        .login-box { max-width:420px; margin:auto; margin-top:120px; }
    </style>
</head>

<body>

<div class="card shadow p-4 login-box">
    <h3 class="text-center text-primary">FinCo Banking Login</h3>

    <form method="POST">

        <div class="mb-3">
            <label>Email</label>
            <input type="text" name="email" class="form-control" required>
        </div>

        <div class="mb-3">
            <label>Password</label>
            <input type="password" name="password" class="form-control" required>
        </div>

        <div class="mb-3">
            <label>Login As</label>
            <select name="role" class="form-control">
                <option value="customer">Customer</option>
                <option value="employee">Employee</option>
            </select>
        </div>

        <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>
</div>

</body>
</html>
"""

# ---------------- CUSTOMER PAGE ----------------
customer_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FinCo Banking Assistant</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
        body { background-color: #f4f7fb; }
        .navbar { background-color: #0d6efd; }
        .navbar-brand { color: white !important; font-weight: bold; }
        .chat-card { background: #eef6ff; border-left: 5px solid #0d6efd; }
        .high { color: red; font-weight: bold; }
        .medium { color: orange; font-weight: bold; }
        .low { color: green; font-weight: bold; }
    </style>
</head>

<body>

<nav class="navbar">
  <div class="container-fluid">
    <span class="navbar-brand">FinCo AI Banking Assistant</span>
  </div>
</nav>

<div class="container mt-4">

    <div class="card shadow p-4">
        <h3 class="text-primary">Submit Your Banking Complaint</h3>

        <form method="POST">
            <div class="mb-3">
                <label>Your Name</label>
                <input type="text" name="name" class="form-control" required>
            </div>

            <div class="mb-3">
                <label>Complaint</label>
                <textarea name="complaint" class="form-control" rows="4" required></textarea>
            </div>

            <button type="submit" class="btn btn-primary">Submit Complaint</button>
        </form>
    </div>

    {% if reply %}
    <div class="card chat-card shadow p-4 mt-4">
        <h4 class="text-primary">AI Banking Response</h4>
        <p><strong>Ticket ID:</strong> {{ ticket_id }}</p>
        <p><strong>Category:</strong> {{ category }}</p>
        <p><strong>Priority:</strong> <span class="{{ priority|lower }}">{{ priority }}</span></p>
        <hr>
        <p>{{ reply }}</p>
    </div>
    {% endif %}

</div>
</body>
</html>
"""

# ---------------- EMPLOYEE PAGE ----------------
employee_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<div class="container mt-4">
    <h2>Employee Complaint Dashboard</h2>

    {% for c in complaints %}
    <div class="card p-3 mb-3">
        <p><strong>Ticket ID:</strong> {{ c['ticket_id'] }}</p>
        <p><strong>Name:</strong> {{ c['name'] }}</p>
        <p><strong>Complaint:</strong> {{ c['complaint'] }}</p>
        <p><strong>Priority:</strong> {{ c['priority'] }}</p>
        <p><strong>Status:</strong> {{ c['status'] }}</p>

        <form method="POST" action="/reply/{{ c['ticket_id'] }}">
            <textarea name="employee_reply" class="form-control mb-2" placeholder="Write solution..."></textarea>
            <button class="btn btn-success">Send Reply & Resolve</button>
        </form>
    </div>
    {% endfor %}
</div>

</body>
</html>
"""

# ---------------- ML PREDICTION ----------------
def model_predict(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# ---------------- ROUTES ----------------

@app.route("/")
def root():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]

        if role == "customer":
            return redirect("/customer")

        elif role == "employee":
            return redirect("/employee")

    return render_template_string(login_template)

@app.route("/customer", methods=["GET", "POST"])
def customer():
    reply = ticket_id = category = priority = None

    if request.method == "POST":
        name = request.form["name"]
        complaint = request.form["complaint"]

        category = model_predict(complaint)
        priority = score_priority(complaint)
        reply, ticket_id = generate_llm_reply(complaint, category, priority, name)

        save_complaint(name, complaint, category, priority, ticket_id, reply)

    return render_template_string(customer_template,
                                  reply=reply,
                                  ticket_id=ticket_id,
                                  category=category,
                                  priority=priority)

@app.route("/employee")
def employee():
    complaints = get_pending_complaints()
    return render_template_string(employee_template, complaints=complaints)

@app.route("/reply/<ticket_id>", methods=["POST"])
def reply(ticket_id):
    employee_reply = request.form["employee_reply"]
    if employee_reply.strip():
        add_employee_reply(ticket_id, employee_reply)
    return redirect("/employee")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)