SELECT m.title
FROM movies m
JOIN ratings r ON m.id = r.movie_id
WHERE m.id IN (
    SELECT movie_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = 'Chadwick Boseman'
    )
)
ORDER BY r.rating DESC
LIMIT 5;
