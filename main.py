from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

TMDB_API_KEY = "REDACTED"
TMDB_API_READER = "REDACTEDY"
TMDB_API_ENDPOINT = "https://api.themoviedb.org/3"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

tmdb_headers = {
    "accept": "application/json",
    "Authorization": "Bearer REDACTED",
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'REDACTED'
Bootstrap5(app)

# CREATE DB

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///favourite-movies.db"
db.init_app(app)

# CREATE TABLE

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(250),unique=True,nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250),nullable=False)
    rating : Mapped[float] = mapped_column(Float,nullable=True)
    ranking: Mapped[int] = mapped_column(Integer,nullable=True)
    review: Mapped[str] = mapped_column(String(250),nullable=True)
    img_url: Mapped[str] = mapped_column(String(250),nullable=False)


with app.app_context():
    db.create_all()

    # new_movie = Movie(
    #     title="Avatar The Way of Water",
    #     year=2022,
    #     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #     rating=7.3,
    #     ranking=9,
    #     review="I liked the water.",
    #     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    # )
    # db.session.add(new_movie)
    # db.session.commit()

## Create forms

class UpdateMovieForm(FlaskForm):
    rating= StringField("Your Rating Out of 10 eg 7.5")
    review= StringField("Your Review")
    submit = SubmitField('Update')

class AddMovieForm(FlaskForm):
    title = StringField("Movie title")
    submit = SubmitField("Add Movie")

## for tmdb connections

## Create page routes

@app.route("/")
def home():
    result = list(db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars())
    for movie in result:
        print(result.index(movie) +1)
        movie.ranking = result.index(movie) +1
        db.session.commit()
    return render_template("index.html", movies=result)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = UpdateMovieForm()
    movie_to_update_id = request.args.get('id')
    movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_to_update_id)).scalar()
    print(movie_to_update)
    if form.validate_on_submit():
        movie_to_update.rating = request.form["rating"]
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=movie_to_update)

@app.route("/delete", methods=["GET","POST"])
def delete():
    if request.method == "GET":
        movie_id = request.args.get('id')
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect(url_for('home'))

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "GET":
        form = AddMovieForm()
        return render_template('add.html', form=form)
    if request.method == "POST":
        query = request.form["title"]
        url = f"https://api.themoviedb.org/3/search/movie?query={query}"
        response = requests.get(url, headers=tmdb_headers)
        data = response.json()
        # search_results = []
        # for result in data["results"]:
        #     search_results.append(f"{result['title']} - {result['release_date']}")
        return render_template('select.html', results = data["results"])

@app.route(rule="/select", methods=["GET","POST"])
def select():
    if request.method == "GET":
        selected_movie_id = request.args.get('id')
        url = f"https://api.themoviedb.org/3/movie/{selected_movie_id}"
        response = requests.get(url, headers=tmdb_headers).json()
        # print(response['title'])
        # # print(response['img_url'])
        # print(response['release_date'].split('-')[0])
        # print(response['overview'])
        new_movie = Movie(
            title=response['title'],
            year=response['release_date'].split('-')[0],
            description=response['overview'],
            img_url=f"{MOVIE_DB_IMAGE_URL}{response['poster_path']}",
        )
        print(new_movie)
        db.session.add(new_movie)
        db.session.commit()
        print(new_movie.id)
        # movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == new_movie.id)).scalar()
        # form = UpdateMovieForm()
        # return render_template("edit.html", form=form, movie=movie_to_update)
        return redirect(url_for("edit",id=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
