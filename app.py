from flask import Flask, render_template, request, redirect, url_for, json
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail with your email server settings (use a real SMTP service like Gmail, Mailgun, or SendGrid)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Or use your email provider
app.config['MAIL_PORT'] = 587  # For Gmail
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Replace with your email password (or use an App Password)
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # The email to send from

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
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Prepare the email message
        msg = Message('New Contact Form Submission', recipients=['recipient@example.com'])  # Replace with your recipient's email
        msg.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        
        try:
            # Send the email
            mail.send(msg)
            return redirect(url_for('success'))  # Redirect to success page after sending
        except Exception as e:
            print(f'Error: {e}')
            return 'There was an error sending your message. Please try again later.'

    return render_template('contactus.html')

@app.route('/guidelines')
def guidelines():
    # Read the guidelines.txt and pass its contents to the template
    try:
        with open('static/guidelines.txt', 'r') as file:
            guidelines_content = file.read()
    except Exception as e:
        guidelines_content = "Sorry, we couldn't load the guidelines at this time."
    return render_template('guidelines.html', content=guidelines_content)

@app.route('/hackathon')
def hackathon():
    # Get the page number from request arguments, default is 1
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of problem statements per page
    
    # Read the JSON file
    try:
        with open('static/ps.json', 'r') as file:
            data = json.load(file)
            problems = data.get("Sheet1", [])  # Extracting the list of problem statements
    except Exception as e:
        problems = []
        print(f'Error loading JSON: {e}')
    
    total_problems = len(problems)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_problems = problems[start:end]
    
    # Pass domains, themes, and categories to the template
    return render_template(
        'hackathon.html', 
        problems=paginated_problems, 
        page=page, 
        total_problems=total_problems, 
        per_page=per_page,
        domains=domains,  # Pass domains to the template
        themes=themes,    # Pass themes to the template
        categories=categories  # Pass categories to the template
    )

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/success')
def success():
    return render_template('success.html')  # Render a success page after form submission

if __name__ == '__main__':
    app.run(debug=True)
