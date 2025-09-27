-- Question 1, query 1
    SELECT mvp.player_name, mvp.height
    FROM mvp;

-- Question 1, query 2
    WITH best_50 AS (
        SELECT player_name, height, total_point
        FROM best_player
    )
    SELECT *
    FROM best_50
    ORDER BY total_point DESC
    LIMIT 50;
