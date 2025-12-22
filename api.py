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


@app.route('/habits/<int:habit_id>/increment', methods=['POST'])
def increment_habit(habit_id):
    increment(habit_id)
    return jsonify(success=True)


@app.route('/habits/<int:habit_id>/decrement', methods=['POST'])
def decrement_habit(habit_id):
    decrement(habit_id)
    return jsonify(success=True)


@app.route('/test/<int:number>', methods=['POST'])
def test(number):
    print(f'Hello {number}')
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
