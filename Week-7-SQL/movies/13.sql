SELECT p.name
FROM people p
WHERE p.id IN (
    SELECT s.person_id
    FROM stars s
    WHERE s.movie_id IN (
        SELECT s2.movie_id
        FROM stars s2
        WHERE s2.person_id = (
            SELECT id
            FROM people
            WHERE name = 'Kevin Bacon' AND birth = '1958'
        )
    )
) AND p.id != (
    SELECT id
    FROM people
    WHERE name = 'Kevin Bacon' AND birth = '1958'
);
