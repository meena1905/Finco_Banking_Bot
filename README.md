# FinCo Banking Bot 🤖💰

[Live Demo](https://finco-banking-bot.onrender.com)

---

## 🚀 Project Overview
A brief description of the project:
- AI-powered web application for handling banking complaints.
- Customers can submit complaints, which are automatically categorized, prioritized, and replied to using AI.
- Employees can track and resolve complaints through a dashboard.

---

## 💡 Features
- Complaint Classification (Account, Credit Card, Loan, etc.)
- Priority Detection (High, Medium, Low)
- AI-generated Responses using OpenAI LLM
- Ticketing System with unique IDs
- Employee Dashboard to view & resolve complaints
- Database storage with SQLite
- Responsive UI using Flask + Bootstrap
- Deployment-ready on Render

---

## 🛠️ Tech Stack
- Backend: Python, Flask  
- Machine Learning: TF-IDF + Logistic Regression  
- AI: OpenAI API  
- Database: SQLite  
- Frontend: HTML, CSS, Bootstrap  
- Deployment: Render + Gunicorn  

---

## 📂 Project Structure

finco-banking-bot/
├── app.py                 
├── database.py           
├── predict.py             
├── requirements.txt      
├── Procfile               
├── README.md                      
└── models/               
    └── tfidf_model.pkl 
    
## 🖥️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/meena1905/finco-banking-bot.git
cd finco-banking-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Flask app
python app.py

# 4. Open in your browser
# http://127.0.0.1:5000/
```
## 📌 Notes

- OpenAI API: The AI reply system requires an OpenAI API key. Make sure to set it in `predict.py` before running the app.  
- SQLite Database: All complaints, ticket IDs, priorities, and employee replies are stored in `complaints.db`.  
- Bootstrap: The frontend uses Bootstrap for responsive and clean UI design.  
- ML Model: Complaint classification uses TF-IDF + Logistic Regression (trained model saved in `models/`).  
- Jupyter Users: You can run the Flask app directly in Jupyter using `!python app.py` in a notebook cell.  
- Deployment: The app is deployment-ready using Render + Gunicorn (`Procfile` included).

## 🤝 Connect with Me

- [LinkedIn](https://linkedin.com/in/s-meenakshi-b2356b288)  

