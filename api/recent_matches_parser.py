def parse_recent_matches(data):
    matches = []

    for match_type in data.get("typeMatches", []):

        for series in match_type.get("seriesMatches", []):

            series_wrapper = series.get("seriesAdWrapper")

            if not series_wrapper:
                continue

            for match in series_wrapper.get("matches", []):

                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                team1 = info.get("team1", {})
                team2 = info.get("team2", {})
                venue = info.get("venueInfo", {})

                match_data = {
                    "match_id": info.get("matchId"),
                    "series_id": info.get("seriesId"),
                    "series_name": info.get("seriesName"),
                    "match_description": info.get("matchDesc"),
                    "format": info.get("matchFormat"),
                    "start_date": info.get("startDate"),
                    "state": info.get("state"),
                    "status": info.get("status"),

                    "team1": team1.get("teamName"),
                    "team2": team2.get("teamName"),

                    "venue": venue.get("ground"),
                    "city": venue.get("city"),

                    "team1_score": None,
                    "team1_wickets": None,
                    "team1_overs": None,

                    "team2_score": None,
                    "team2_wickets": None,
                    "team2_overs": None,
                }

                # Team 1 score
                team1_innings = (
                    score.get("team1Score", {})
                    .get("inngs1", {})
                )

                if team1_innings:
                    match_data["team1_score"] = team1_innings.get("runs")
                    match_data["team1_wickets"] = team1_innings.get("wickets")
                    match_data["team1_overs"] = team1_innings.get("overs")

                # Team 2 score
                team2_innings = (
                    score.get("team2Score", {})
                    .get("inngs1", {})
                )

                if team2_innings:
                    match_data["team2_score"] = team2_innings.get("runs")
                    match_data["team2_wickets"] = team2_innings.get("wickets")
                    match_data["team2_overs"] = team2_innings.get("overs")

                matches.append(match_data)

    return matches