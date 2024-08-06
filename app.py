from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thought = request.form['thought']
        # Here you would add your logic to filter and save the thought
        return redirect(url_for('thank_you'))
    return render_template('index.html')  # Render the main page

@app.route('/thank_you')
def thank_you():
    # Render the thank you page after a thought is submitted
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
