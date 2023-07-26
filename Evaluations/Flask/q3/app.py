from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table', methods=['POST'])
def table():
    data = request.form['number']
    try:
        number = int(data)
        table = []
        for i in range(1, 11):
            table.append(number*i)
        
        return render_template('index.html', tables=table, input=number)

    except KeyError:
        error_message = 'Invalid input. Please provide a valid number.'
        return render_template('index.html', error=error_message)

if __name__ == "__main__":
    app.run(debug=True)