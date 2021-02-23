from flask import Flask, render_template, url_for, flash, redirect, request
import recommend
import pandas as pd
import random

app = Flask(__name__)


def getRecipeInfo(name):
    df = pd.read_excel("Dataset/nutritional_info.xlsx")
    df.set_index("name", inplace=True)
    print(name)
    return df.loc[name]


@app.route('/')
def users():
    #users = [{"name": "Aedan", "id": 1}, {"name": "Lucy", "id": 2}]
    return render_template("details.html")


@app.route('/details/')
def details():
    return render_template("details.html")


@app.route('/recommendations/')
def recommendations():
    return render_template('recommendations.html')


@app.route('/recipe/')
def recipe():
    return render_template('recipe.html')


@app.route("/", methods=['GET', 'POST'])
def choices():
    if request.method == 'POST':
        preptime = request.form['time'].strip()
        categories = request.form['categories'].strip()
        ingredients = request.form['ingredients'].strip()
        data = {'time': preptime, 'categories': categories, 'ingredients': ingredients}
        suggestions = recommend.runreccomend(data)

        return render_template("recommendations.html", suggestions=suggestions, choices=data)
    return render_template('details.html')


@app.route("/recommendations", methods=['GET', 'POST'])
def getrecipe():
    if request.method == 'POST':
        name = request.form['name']
        info = getRecipeInfo(name)

        numbers = random.sample(range(1, 100), 4)
        numbers = list(map(str, numbers))

        return render_template("recipe.html", recipe=info, numbers=numbers)
    return render_template('recommendations.html')


if __name__ == '__main__':
    currentUser = ""
    app.run()
