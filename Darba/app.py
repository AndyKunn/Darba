from flask import Flask, render_template, request, redirect, url_for
from peewee import *
import pandas as pd
import matplotlib.pyplot as plt
import os

db = SqliteDatabase("database.db")

class Film(Model):
    title = CharField()
    year = IntegerField()
    genre = CharField()
    rating = FloatField()

    class Meta:
        database = db

db.connect()
db.create_tables([Film], safe=True)
db.close()

app = Flask(__name__)

@app.route('/')
def index():
    db.connect()
    films = Film.select()
    db.close()
    return render_template("index.html", films=films)

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if file:
        df = pd.read_csv(file)
        db.connect()
        for _, row in df.iterrows():
            Film.create(title=row['Title'], year=row['Year'], genre=row['Genre'], rating=row['Rating'])
        db.close()
    return redirect(url_for('index'))

@app.route('/chart')
def chart():
    db.connect()
    genres = []
    ratings = {}

    for film in Film.select():
        if film.genre in ratings:
            ratings[film.genre].append(film.rating)
        else:
            ratings[film.genre] = [film.rating]

    db.close()

    avg_ratings = {genre: sum(vals) / len(vals) for genre, vals in ratings.items()}

    plt.figure(figsize=(8, 5))
    plt.bar(avg_ratings.keys(), avg_ratings.values())
    plt.xlabel("Žanrs")
    plt.ylabel("Vidējais vērtējums")
    plt.title("Filmu vērtējums pēc žanra")
    plt.xticks(rotation=45)
    plt.savefig("static/chart.png")
    plt.close()

    return render_template("chart.html")

if __name__ == "__main__":
    app.run(debug=True)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        try:
        
            df = pd.read_csv(filename, delimiter=',') 

            return df.to_html() 

        except pd.errors.ParserError as e:
            return f"Kļūda, lasot failu: {e}"

if __name__ == '__main__':
    app.run(debug=True)
