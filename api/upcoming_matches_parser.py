def parse_upcoming_matches(data):
    matches = []

    for match_type in data.get("typeMatches", []):

        for series in match_type.get("seriesMatches", []):

            series_wrapper = series.get("seriesAdWrapper")

            if not series_wrapper:
                continue

            for match in series_wrapper.get("matches", []):

                info = match.get("matchInfo", {})

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
                    "end_date": info.get("endDate"),

                    "state": info.get("state"),
                    "status": info.get("status"),

                    "team1": team1.get("teamName"),
                    "team2": team2.get("teamName"),

                    "venue": venue.get("ground"),
                    "city": venue.get("city"),
                }

                matches.append(match_data)

    return matches