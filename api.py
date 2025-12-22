"""Flask REST API"""
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/habits', methods=['GET'])
def habits():
    if request.method == 'GET':
        return render_template('habits.html')

    return 'Error 405: Method not allowed'


@app.route('/addGoodHabit', methods=['POST'])
def addGoodHabit():
    """adds habit_name to database"""
    data = request.get_json()
    habit_name = data['habit_name']
    # Save to DB
    return jsonify({
        'habit_name': habit_name
    })


@app.route('/addBadHabit', methods=['POST'])
def addBadHabit():
    """adds habit_name to database"""
    data = request.get_json()
    habit_name = data['habit_name']
    # Save to DB
    return jsonify({
        'habit_name': habit_name
    })


@app.route('/test/<int:number>', methods=['POST'])
def test(number):
    print(f'Hello {number}')
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
