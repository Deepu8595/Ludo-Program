from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Function to simulate dice roll
def roll_dice():
    return random.randint(1, 6)

# Ludo game logic
def ludo_game(players):
    result = []
    for i in range(1, players + 1):
        player_result = {
            "team": f"Team {i}",
            "team_color": ['red', 'green', 'blue', 'yellow'][i-1]  # Assigning different colors for each team
        }

        dice_1 = roll_dice()
        player_result["dice_1"] = dice_1

        if dice_1 == 6:
            player_result["token_status"] = "Your token is open now!"
            dice_2 = roll_dice()
            player_result["dice_2"] = dice_2
            if dice_2 == 6:
                dice_3 = roll_dice()
                player_result["dice_3"] = dice_3
                if dice_3 == 6:
                    player_result["token_action"] = "Turn is canceled!"
                else:
                    player_result["token_action"] = f"Token moves {dice_3} steps!"
            else:
                player_result["token_action"] = f"Token moves {dice_2} steps!"
        else:
            player_result["token_status"] = "Token failed to open."
            player_result["token_action"] = "No movement."

        result.append(player_result)
    return result

# Flask routes
@app.route('/')
def index():
    return render_template('ludo.html')

@app.route('/play', methods=['POST'])
def play():
    try:
        players = int(request.form['players'])
        if 1 <= players <= 4:
            result = ludo_game(players)
            return render_template('ludo.html', result=result)
        else:
            return render_template('ludo.html', error="Please enter a number of players between 1 and 4.")
    except ValueError:
        return render_template('ludo.html', error="Invalid input. Please enter a valid number of players.")

if __name__ == '__main__':
    app.run(debug=True)