SELECT name FROM people WHERE id IN (SELECT DISTINCT person_id FROM directors, ratings WHERE ratings.rating >= 9.0 AND ratings.movie_id = directors.movie_id);
