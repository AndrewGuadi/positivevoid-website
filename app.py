from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db, init_app
from models import Thought, ProcessedThought, FailedThought, BadIP
from gpt_connect import filter_user_input  # Import the filter function
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Needed for session management

init_app(app)

def get_user_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def sanitize_input(input_text):
    # Remove any HTML tags and limit length
    sanitized_text = re.sub(r'<.*?>', '', input_text)
    return sanitized_text[:500]  # Limit to 500 characters

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    user_ip = get_user_ip()  # Get the user's IP address
    invalidate_ip = BadIP.query.filter_by(ip=user_ip).first()
    if invalidate_ip:
        # Set a session flag to display the warning popup
        session['warning'] = True
    else:
        session.pop('warning', None)  # Remove the warning flag if not invalidated

    if request.method == 'POST':
        raw_thought = request.form['thought']
        sanitized_thought = sanitize_input(raw_thought)
        filtered_response = filter_user_input(sanitized_thought)  # Use the imported function

        challenging_thought = filtered_response.get('challenging_thought', '')

        if filtered_response.get('status', 'fail') == 'pass':
            # Save the passed thought to the database
            new_processed_thought = ProcessedThought(
                original_text=sanitized_thought,
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
                original_text=sanitized_thought,
                pass_fail=filtered_response.get('status', 'fail'),
                emotions=filtered_response.get('emotions', []),  # Pass list directly
                sentiment_basic=filtered_response.get('sentiment_basic', 'neutral'),
                sentiment_score=int(filtered_response.get('sentiment_score', 0)),
                tldr=filtered_response.get('TLDR', ''),
                time_stamp=filtered_response['time_stamp'],
                keywords=filtered_response.get('keywords', [])  # Pass list directly
            )
            db.session.add(new_failed_thought)

            # Log the bad IP address if it doesn't already exist
            bad_ip = BadIP.query.filter_by(ip=user_ip).first()
            if not bad_ip:
                bad_ip = BadIP(ip=user_ip)
                db.session.add(bad_ip)
            else:
                bad_ip.time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            db.session.commit()
        except Exception as e:
            print(f"There was an issue uploading data to DB. {e}")
            db.session.rollback()

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
