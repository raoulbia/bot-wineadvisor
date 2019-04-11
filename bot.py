#!/usr/bin/env python3
# https://github.com/Ahirice/sato/
# https://cai.tools.sap/blog/python-cryptobot/

from flask import Flask, request, jsonify, render_template
import json, requests
from itertools import compress

app = Flask(__name__)
port = '5000'

@app.route('/apero', methods=['POST'])
def apero():
    # return render_template('index.html') # use methods = GET

    data = json.loads(request.get_data().decode())

    wine_body = data["conversation"]["memory"]["wine_body"]["raw"]
    wine_sweetness = data["conversation"]["memory"]["wine_sweetness"]["raw"]
    wine_effervescence = data["conversation"]["memory"]["wine_effervescence"]["raw"]

    # wine_color = data["conversation"]["memory"]["wine_color"]["raw"]
    # meal_cheese = data["conversation"]["memory"]["meal_cheese"]["raw"]

    dry_sherry = all([wine_body in ('medium', 'full'), wine_sweetness == 'dry'])

    champagne = all([wine_body in ('medium', 'light'),
                     wine_sweetness in ('sweet', 'medium dry'),
                     wine_effervescence in ('sparkling')])

    prosecco = all([wine_body in ('light'),
                   wine_sweetness in ('dry'),
                   wine_effervescence in ('sparkling')])

    sauvignon = all([wine_body in ('medium', 'light'),
                     wine_sweetness in ('sweet', 'medium dry'),
                     wine_effervescence in ('not sparkling', 'non-sparkling')])


    wines = ['Dry Sherry', 'Champagne', 'Prosecco', 'Sauvignon Blanc']
    filter = [dry_sherry, champagne, prosecco, sauvignon]
    print(filter)
    answer = list(compress(wines, filter))[0]
    return respond(answer)


@app.route('/cheese', methods=['POST'])
def cheese():
    # return render_template('index.html') # use methods = GET

    data = json.loads(request.get_data().decode())

    wine_color = data["conversation"]["memory"]["wine_color"]["raw"]
    meal_type_cheese = data["conversation"]["memory"]["meal_type_cheese"]["raw"]

    rose = all([wine_color == 'red'])
    chablis = all(['variety' in meal_type_cheese, wine_color == 'white'])
    sauvignon = all(['mild' in meal_type_cheese, wine_color == 'white'])


    wines = ['Rose', 'Chablis', 'Sauvignon Blanc']
    filter = [rose, chablis, sauvignon]
    answer = list(compress(wines, filter))[0]
    return respond(answer)


@app.route('/meat', methods=['POST'])
def meat():
    # return render_template('index.html') # use methods = GET

    data = json.loads(request.get_data().decode())

    meat = data["conversation"]["memory"]["meat"]["raw"]

    burgundy = all([meat in ('raost beef', 'steak', 'game', 'lamb')])
    pinot = all([meat in ('pork', 'veal', 'chicken', 'turkey')])
    chianti = all(['italian' in meat])
    chardonnay = all([meat in ('shellfish', 'fish')])

    wines = ['Red Burgundy', 'Pinot NOir', 'Chiant', 'Chardonnay']
    filter = [burgundy, pinot, chianti, chardonnay]
    answer = list(compress(wines, filter))[0]
    return respond(answer)


@app.route('/dessert', methods=['POST'])
def dessert():
    # return render_template('index.html') # use methods = GET

    data = json.loads(request.get_data().decode())

    dessert = data["conversation"]["memory"]["dessert"]["raw"]

    port = all([dessert in ('fruit')])
    burgundy = all([dessert in ('chocolate', 'ice cream')])

    wines = ['Port Wine', 'Red Burgundy']
    filter = [port, burgundy]
    answer = list(compress(wines, filter))[0]
    return respond(answer)


def respond(answer):
    return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      # 'content': 'Roger that',
      'content': 'I recommend %s.' % (answer)
    }],
    conversation={
      'memory': { 'key': 'value' }
    }
)

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data().decode()))
  return jsonify(status=200)

# app.run(port=port)
app.run(debug=True, host = '0.0.0.0', port = port)
