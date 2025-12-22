"""Flask REST API"""
from flask import Flask, render_template, request, jsonify
from database import

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/habits', methods=['GET'])
def habits():
    if request.method == 'GET':
        return render_template('habits.html')

    return 'Error 405: Method not allowed'


@app.route('/habits/addGoodHabit/<str:habit_name>', methods=['POST'])
def addGoodHabit(habit_name):
    """adds habit_name to database"""
    print(habit_name)
    return jsonify(success=True)


@app.route('/habits/addBadHabit/<str:habit_name>', methods=['POST'])
def addBadHabit(habit_name):
    """adds habit_name to database"""
    print(habit_name)
    return jsonify(success=True)


@app.route('/test/<int:number>', methods=['POST'])
def test(number):
    print(f'Hello {number}')
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
