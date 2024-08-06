from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db, init_app
from models import Thought, ProcessedThought, FailedThought
from gpt_connect import filter_user_input  # Import the filter function
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Needed for session management

init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw_thought = request.form['thought']
        filtered_response = filter_user_input(raw_thought)  # Use the imported function

        challenging_thought = filtered_response.get('challenging_thought', '')

        if filtered_response.get('status', 'fail') == 'pass':
            # Save the passed thought to the database
            new_processed_thought = ProcessedThought(
                original_text=raw_thought,
                pass_fail=filtered_response.get('status', 'fail'),
                emotions=filtered_response.get('emotions', []),  # Pass list directly
                sentiment_basic=filtered_response.get('sentiment_basic', 'neutral'),
                sentiment_score=int(filtered_response.get('sentiment_score', 0)),
                tldr=filtered_response.get('TLDR', ''),
                time_stamp=filtered_response['time_stamp'],
                keywords=filtered_response.get('keywords', [])  # Pass list directly
            )
            db.session.add(new_processed_thought)
        else:
            # Save the failed thought to the database
            new_failed_thought = FailedThought(
                original_text=raw_thought,
                pass_fail=filtered_response.get('status', 'fail'),
                emotions=filtered_response.get('emotions', []),  # Pass list directly
                sentiment_basic=filtered_response.get('sentiment_basic', 'neutral'),
                sentiment_score=int(filtered_response.get('sentiment_score', 0)),
                tldr=filtered_response.get('TLDR', ''),
                time_stamp=filtered_response['time_stamp'],
                keywords=filtered_response.get('keywords', [])  # Pass list directly
            )
            db.session.add(new_failed_thought)

        db.session.commit()

        # Pass challenging thought to the thank_you route
        session['challenging_thought'] = challenging_thought
        return redirect(url_for('thank_you'))
    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    challenging_thought = session.get('challenging_thought', '')
    return render_template('thankyou.html', challenging_thought=challenging_thought)

if __name__ == '__main__':
    app.run(debug=True)
