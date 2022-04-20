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


def get_movies_by_years(after: int, before: int) -> list:
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, release_year
					FROM netflix
					WHERE release_year BETWEEN {after} and {before}
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


def get_movies_by_rating(*ratings: tuple) -> list:
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, rating, description
					FROM netflix
					WHERE rating IN {ratings}
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
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, description
					FROM netflix
					WHERE listed_in LIKE '%{genre}%'
					ORDER BY release_year DESC
					'''
	cursor.execute(sqlite_query)
	movies = cursor.fetchmany(10)

	result = []
	for movie in movies:
		keys = ('title', 'description')
		result.append(dict(zip(keys, movie)))

	return result


def get_movies_by_actors(act_1: str, act_2: str) -> list:
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

	actors_list = []
	for actors in cast:
		actors_list.extend(actors[0].split(', '))

	actors_set = set()
	for actor in actors_list:
		if actors_list.count(actor) > 2 and actor.lower() not in {act_1.lower(), act_2.lower()}:
			actors_set.add(actor)

	return list(actors_set)


def get_movies_json(movie_type: str, year: int, genre: str) -> list:
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

	# Допилить отсюда
	result = []
	for movie in movies:
		result.append(json.dumps(movie))

	# print(*result, sep='\n')
	print(result)


# get_movies_json('TV Show', 2002, 'roman')
