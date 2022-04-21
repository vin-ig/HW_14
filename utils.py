import sqlite3
import json


def get_movie_by_title(name: str) -> dict:
	"""Возвращает новейший фильм по названию"""
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, country, release_year, listed_in, description
					FROM netflix
					WHERE title LIKE '%{name}%'
					ORDER BY release_year DESC
					'''
	cursor.execute(sqlite_query)

	values = cursor.fetchone()
	keys = ('title', 'country', 'release_year', 'genre', 'description')

	return dict(zip(keys, values))


def get_movies_by_years(from_y: int, to_y: int) -> list:
	"""Возвращает фильмы в диапазоне лет выпуска"""
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, release_year
					FROM netflix
					WHERE release_year BETWEEN {from_y} and {to_y}
					ORDER BY release_year
					LIMIT 100
					'''
	cursor.execute(sqlite_query)
	movies = cursor.fetchall()

	result = []
	for movie in movies:
		keys = ('title', 'release_year')
		result.append(dict(zip(keys, movie)))

	return result


def get_movies_by_rating(group: str) -> list:
	"""Возвращает фильмы по возрастным ограничениям"""
	if group == 'children':
		rating = 'G', 'G'
	elif group == 'family':
		rating = 'G', 'PG', 'PG-13'
	elif group == 'adult':
		rating = 'R', 'NC-17'

	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()
	sqlite_query = f'''
					SELECT title, rating, description
					FROM netflix
					WHERE rating IN {rating}
					LIMIT 100
					'''
	cursor.execute(sqlite_query)
	movies = cursor.fetchall()

	result = []
	for movie in movies:
		keys = ('title', 'rating', 'description')
		result.append(dict(zip(keys, movie)))

	return result


def get_movies_by_genre(genre: str) -> list:
	"""Возвращает фильмы по жанру"""
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, listed_in, description
					FROM netflix
					WHERE listed_in LIKE '%{genre}%'
					ORDER BY release_year DESC
					'''
	cursor.execute(sqlite_query)
	movies = cursor.fetchmany(10)

	result = []
	for movie in movies:
		keys = ('title', 'genre', 'description')
		result.append(dict(zip(keys, movie)))

	return result


def get_movies_by_actors(actors: tuple) -> list:
	"""Возвращает актеров, сыгравших с указанными более 2 раз"""
	act_1, act_2 = actors
	
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT "cast"
					FROM netflix
					WHERE "cast" LIKE '%{act_1}%'
					AND "cast" LIKE '%{act_2}%'
					'''
	cursor.execute(sqlite_query)
	cast = cursor.fetchall()

	# Создаем список всех актеров, сыгравших с указанными
	actors_list = []
	for actors in cast:
		actors_list.extend(actors[0].split(', '))

	# Выводим актеров, удовлетворяющих условию
	actors_set = set()
	for actor in actors_list:
		if actors_list.count(actor) > 2 and actor.lower() not in {act_1.lower(), act_2.lower()}:
			actors_set.add(actor)

	return list(actors_set)


def get_movies_json(movie_type: str, year: int, genre: str) -> str:
	"""Возвращает json с фильмами по типу, году выпуска, жанру"""
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, description
					FROM netflix
					WHERE type = '{movie_type}'
					AND release_year = {year}
					AND listed_in LIKE '%{genre}%'
					'''
	cursor.execute(sqlite_query)
	movies = cursor.fetchall()

	result = []
	for movie in movies:
		keys = ('title', 'description')
		result.append(dict(zip(keys, movie)))

	result = json.dumps(result, indent=2)

	return result
