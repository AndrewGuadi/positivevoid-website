from flask import Flask, render_template, request, redirect, url_for
from extensions import db, init_app
from models import Thought

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_app(app)

# Function to parse input
def parse_input(input_text):
    parsed_text = input_text.lower()  # Example of parsing: make text lowercase
    return parsed_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw_thought = request.form['thought']
        parsed_thought = parse_input(raw_thought)
        new_thought = Thought(content=parsed_thought)
        db.session.add(new_thought)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)

