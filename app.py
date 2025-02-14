from flask import Flask, render_template, request, redirect, url_for, json
from flask_mail import Mail, Message
import os
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Flask-Mail Configuration (Update with real credentials)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

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
    file_path = 'static/contact_submissions.xlsx'

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year_section = request.form['year_section']
        email = request.form['email']
        message = request.form['message']
        date_submitted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if file exists and is valid
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
            except Exception:
                print("Error reading the Excel file. Creating a new one.")
                df = pd.DataFrame(columns=['Date', 'Name', 'Department', 'Year & Section', 'Email', 'Message'])
        else:
            df = pd.DataFrame(columns=['Date', 'Name', 'Department', 'Year & Section', 'Email', 'Message'])

        # Append new data
        new_entry = pd.DataFrame([[date_submitted, name, department, year_section, email, message]], 
                                 columns=['Date', 'Name', 'Department', 'Year & Section', 'Email', 'Message'])
        df = pd.concat([df, new_entry], ignore_index=True)

        # Save back to Excel with error handling
        try:
            df.to_excel(file_path, index=False, engine='openpyxl')
        except Exception as e:
            print(f"Error saving the Excel file: {e}")

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
