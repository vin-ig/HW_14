import sqlite3


def get_move_by_title(name: str) -> dict:
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


def get_moves_by_years(after: int, before: int) -> list:
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
	moves = cursor.fetchall()

	result = []
	for move in moves:
		keys = ('title', 'release_year')
		result.append(dict(zip(keys, move)))

	return result


def get_moves_by_rating(*ratings: tuple) -> list:
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, rating, description
					FROM netflix
					WHERE rating IN {ratings}
					LIMIT 100
					'''
	cursor.execute(sqlite_query)
	moves = cursor.fetchall()

	result = []
	for move in moves:
		keys = ('title', 'rating', 'description')
		result.append(dict(zip(keys, move)))

	return result


def get_moves_by_genre(genre: str) -> list:
	with sqlite3.connect('netflix.db') as connection:
		cursor = connection.cursor()

	sqlite_query = f'''
					SELECT title, description
					FROM netflix
					WHERE listed_in LIKE '%{genre}%'
					ORDER BY release_year DESC
					'''
	cursor.execute(sqlite_query)
	moves = cursor.fetchmany(10)

	result = []
	for move in moves:
		keys = ('title', 'description')
		result.append(dict(zip(keys, move)))

	return result


def get_moves_by_actors(act_1: str, act_2: str) -> list:
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
