-- Question 1, query 1

    SELECT mvp.player_name, mvp.height
    FROM mvp;

-- Question 1, query 2

    SELECT player_name, height, total_point
    FROM best_player
    ORDER BY total_point DESC
    LIMIT 50;
