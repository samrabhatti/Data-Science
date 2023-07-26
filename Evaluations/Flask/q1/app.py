from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/square', methods=['POST'])
def square_number():
    data = request.form['number']
    try:
        number = int(data)
        result = number ** 2
        return render_template('index.html', result=result, number_input=data)
    except ValueError:
        error_message = 'Invalid input. Please provide a valid number.'
        return render_template('index.html', error=error_message)

if __name__ == "__main__":
    app.run(debug=True)