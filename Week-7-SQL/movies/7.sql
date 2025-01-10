SELECT title, rating FROM movies, ratings WHERE id = ratings.movie_id AND year = 2010 ORDER BY ratings.rating DESC, title ASC;
