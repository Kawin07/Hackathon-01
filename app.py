from flask import Flask, render_template, request, redirect, url_for, json
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
firebase_config = json.loads(os.getenv("FIREBASE_CONFIG"))  # Load from Render environment variable
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()  # Firestore instance

# Dropdown options
domains = [
    "Smart Cities", "Environment", "Disaster Management", "Energy", "Waste Management", "Healthcare", 
    "Agriculture", "Security", "Education", "Cybersecurity", "Accessibility", "Workplace Safety", 
    "Blockchain", "Infrastructure", "Sustainability", "Smart Homes", "Smart Transportation", "Governance", 
    "Media & Communication", "Transportation", "Retail", "E-Commerce", "Human Resources", "Occupational Safety", 
    "Logistics", "Safety", "LegalTech", "Power Electronics", "Renewable Energy", "Power Systems", "Industrial Automation", 
    "Electric Vehicles", "IoT & Agriculture", "Security & Power", "IoT & Automation", "Industrial IoT"
]

themes = [
    "Urban Mobility", "Water Management", "Emergency Response", "Renewable Energy", "Clean & Green Technology", 
    "Assistive Technology", "Precision Farming", "Public Safety", "EdTech", "Digital Security", "Smart Irrigation", 
    "Inclusive Technology", "Smart Infrastructure", "Digital Governance", "Wellness & AI", "Smart Roads", 
    "AgriTech", "Early Warning Systems", "Air Pollution Control", "E-Mobility", "Zero Hunger", "IoT", "Fire Safety", 
    "Road Safety", "Noise Control", "Biodiversity Conservation", "Misinformation Control", "Telemedicine", 
    "Smart Shopping", "Augmented Reality", "Supply Chain Optimization", "Climate Resilience", "Workplace Safety", 
    "Smart Mobility", "Secure Elections", "Personal Wellness"
]

categories = ["Hardware + Software", "Software", "Hardware"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year_section = request.form['year_section']
        email = request.form['email']
        message = request.form['message']
        date_submitted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Store data in Firestore
        contact_ref = db.collection("contact_submissions")
        contact_ref.add({
            "Date": date_submitted,
            "Name": name,
            "Department": department,
            "Year & Section": year_section,
            "Email": email,
            "Message": message
        })

        return redirect(url_for('success'))  

    return render_template('contactus.html')

@app.route('/guidelines')
def guidelines():
    try:
        with open('static/guidelines.txt', 'r', encoding='utf-8') as file:
            guidelines_content = file.read()
    except Exception:
        guidelines_content = "Sorry, we couldn't load the guidelines at this time."
    
    return render_template('guidelines.html', content=guidelines_content)

@app.route('/hackathon')
def hackathon():
    try:
        with open('static/Book1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            problems = data.get("Sheet1", [])
    except Exception as e:
        problems = []
        print(f'Error loading JSON: {e}')

    domains = list(set(problem.get("Domain", "N/A") for problem in problems))
    themes = list(set(problem.get("Theme", "N/A") for problem in problems if "Theme" in problem))
    categories = list(set(problem.get("Category", "N/A") for problem in problems))

    return render_template(
        'hackathon.html',
        problems=problems,  
        domains=domains,
        themes=themes,
        categories=categories
    )

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
