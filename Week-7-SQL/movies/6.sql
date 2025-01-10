SELECT AVG(rating) FROM ratings JOIN movies ON movie_id = movies.id AND movies.year = 2012;
