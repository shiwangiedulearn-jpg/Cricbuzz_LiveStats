from sqlalchemy import text
from database.database import engine


query = """
SELECT
    m.format,
    b.player_name,
    b.runs AS highest_score
FROM batting b
JOIN matches m
    ON b.match_id = m.match_id
WHERE m.format IN ('Test', 'ODI', 'T20I')
  AND b.runs = (
      SELECT MAX(b2.runs)
      FROM batting b2
      JOIN matches m2
          ON b2.match_id = m2.match_id
      WHERE m2.format = m.format
  )
ORDER BY
    CASE m.format
        WHEN 'Test' THEN 1
        WHEN 'ODI' THEN 2
        WHEN 'T20I' THEN 3
    END;
"""


with engine.connect() as connection:
    result = connection.execute(text(query))

    print("\nHighest Individual Score by Format")
    print("-" * 60)

    for row in result:
        print(row)