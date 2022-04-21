from flask import Flask, render_template, request, jsonify
from utils import *

app = Flask(__name__)


@app.route('/')
def index():
	"""Главная страница"""
	return render_template('index.html')


@app.route('/movie/')
def by_title():
	"""Поиск по названию"""
	title = request.args.get('title')
	movie = get_movie_by_title(title)
	return render_template('by_title.html', movie=movie, title=title)


@app.route('/movie/year-to-year/')
def between_years():
	"""Поиск в диапазоне лет выпуска"""
	years = request.args.get('from_y'), request.args.get('to_y')
	year_1, year_2 = years 
	
	# if not isinstance(year_1, int) or not isinstance(year_2, int):
	# 	print('type')
	# 	raise TypeError
	# elif year_1 > year_2:
	# 	raise ValueError
		
	try:
		year_1, year_2 = int(year_1), int(year_2)
		movies = get_movies_by_years(year_1, year_2)
		return render_template('between_years.html', movies=movies, years=years)
	except TypeError:
		error = 'Нужно ввести целые числа'
		return render_template('between_years.html', error=error)
	except ValueError:
		error = 'Неверный диапазон'
		return render_template('between_years.html', error=error)
	



@app.route('/rating/')
def by_rating():
	"""Фильтр по возрастным ограничениям"""
	group = request.args.get('group')
	movies = get_movies_by_rating(group)
	return render_template('by_rating.html', movies=movies, group=group)


@app.route('/genre/')
def by_genre():
	"""Поиск по жанру"""
	genre = request.args.get('genre')
	movies = get_movies_by_genre(genre)
	return render_template('by_genre.html', movies=movies, genre=genre)


@app.route('/actors/')
def by_actors():
	actors = request.args.get('act_1'), request.args.get('act_2')
	actors_list = get_movies_by_actors(actors)

	return render_template('by_actors.html', actors=actors, actors_list=actors_list)


@app.route('/movie_json/')
def movie_json():
	type_ = request.args.get('type')
	year = request.args.get('year')
	genre = request.args.get('genre')

	try:
		year = int(year)
		movies = get_movies_json(type_, year, genre)
		return render_template('movie_json.html', movies=movies, type=type_, year=year, genre=genre)
	except ValueError:
		error = 'Неверно введен год'
		return render_template('movie_json.html', error=error)


if __name__ == '__main__':
	app.run(debug=True)
