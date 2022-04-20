from flask import Flask, render_template
from utils import *

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/movie/<title>/')
def by_title(title):
	movie = get_movie_by_title(title)
	return render_template('by_title.html', movie=movie)


@app.route('/movie/year/to/year/')
def between_years(year_1, year_2):
	movies = get_movies_by_years(year_1, year_2)
	return render_template('between_years.html', movies=movies)


@app.route('/rating/<group>/')
def by_rating(group):
	if group == 'children':
		rating = 'G'
	elif group == 'family':
		rating = 'G', 'PG', 'PG-13'
	elif group == 'adult':
		rating = 'R', 'NC-17'
	else:
		pass

	movies = get_movies_by_rating(rating)
	return render_template('by_rating.html', movies=movies)


@app.route('/genre/<genre>/')
def by_genre(genre):
	movies = get_movies_by_genre(genre)
	return render_template('between_years.html', movies=movies)


if __name__ == '__main__':
	app.run(debug=True)
