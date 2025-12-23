"""Flask REST API"""

from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv

from database import create_habit, get_habits

app = Flask(__name__)

DEFAULT_EMAIL = "example@gmail.com"
DEFAULT_PASSWORD = "example"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/habits', methods=['GET'])
def habits():
    if request.method == 'GET':
        return render_template('habits.html')

    return 'Error 405: Method not allowed'


@app.route("/goodHabits/<email>", methods=["GET"])
def get_good_habits(email):
    """Gets a list of good habits for the account associated with the email."""
    try:
        return [habit for habit in get_habits(email) if habit["habit_type"] == "good"]
    except ValueError as e:
        return {"error": e}


@app.route("/badHabits/<email>", methods=["GET"])
def get_bad_habits(email):
    """Gets a list of bad habits for the account associated with the email."""
    try:
        return [habit for habit in get_habits(email) if habit["habit_type"] == "bad"]
    except ValueError as e:
        return {"error": e}


@app.route("/addHabit", methods=["POST"])
def add_habit():
    """Adds new habit to database, defaults to good habit."""
    data = request.get_json()
    habit_name = data['habit_name']
    # email = data["email"]
    habit_type = request.args.get("habit_type", "good")

    new_habit = create_habit(habit_name, habit_type, DEFAULT_EMAIL)

    return jsonify(new_habit)


@app.route('/test/<int:number>', methods=['POST'])
def test(number):
    print(f'Hello {number}')
    return jsonify(success=True)


if __name__ == "__main__":

    load_dotenv()

    app.run(port=8000, debug=True)
