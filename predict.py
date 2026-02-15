import re
import joblib
import random
import datetime
import openai
openai.api_key = "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"

HIGH_KEYWORDS = [
    "fraud", "unauthorized", "scam", "money deducted", "charged twice",
    "identity theft", "account hacked", "transaction failed but money deducted",
    "illegal", "stolen", "phishing", "blocked account"
]

MEDIUM_KEYWORDS = [
    "not working", "error", "issue", "delay", "pending",
    "unable", "failed", "complaint", "problem", "technical"
]

LOW_KEYWORDS = [
    "information", "how to", "query", "clarification",
    "details", "process", "request", "guidance"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def score_priority(text):
    text = clean_text(text)

    high_score = sum(1 for word in HIGH_KEYWORDS if word in text)
    medium_score = sum(1 for word in MEDIUM_KEYWORDS if word in text)

    if high_score >= 1:
        return "High"
    elif medium_score >= 1:
        return "Medium"
    else:
        return "Low"

def generate_ticket_id():
    return "BANK" + str(random.randint(100000, 999999))

def generate_llm_reply(text, category, priority, customer_name="Customer"):

    ticket_id = generate_ticket_id()
    date = datetime.datetime.now().strftime("%d-%m-%Y")

    prompt = f"""
You are an AI banking customer support assistant.

Customer Name: {customer_name}
Complaint: {text}
Predicted Category: {category}
Priority Level: {priority}
Ticket ID: {ticket_id}
Date: {date}

Generate a professional, empathetic, personalized banking response.

Include:
- greeting with name
- acknowledgement
- reassurance
- action statement
- ticket reference
- closing line

Keep tone formal like a real bank.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        reply_text = response['choices'][0]['message']['content']
        return reply_text, ticket_id

    except Exception as e:
        # fallback if API fails
        reply = f"""
Dear {customer_name},

We have received your complaint regarding "{text}".

Your issue is categorized under {category} with {priority} priority.
Our banking team is actively reviewing this.

Ticket ID: {ticket_id}

We assure resolution at the earliest.

Regards,
AI Banking Support
"""
        return reply, ticket_id


# load saved model and vectorizer
model = joblib.load("complaint_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# new complaint text
text = "Unauthorized transaction happened and money deducted"

# category prediction
vec = vectorizer.transform([text])
category = model.predict(vec)[0]

# priority prediction
priority = score_priority(text)

customer_name = "Meenakshi"

reply, ticket_id = generate_llm_reply(text, category, priority, customer_name)

print("Predicted Category:", category)
print("Priority Level:", priority)
print("Ticket ID:", ticket_id)

print("\nAI Banking Response:\n")
print(reply)