def parse_scorecard(data, match_id):
    result = {
        "batting": [],
        "bowling": [],
        "partnerships": [],
        "fall_of_wickets": []
    }

    scorecards = data.get("scorecard", [])

    for innings in scorecards:

        innings_id = innings.get("inningsid")
        batting_team = innings.get("batteamname")

        # -------------------------
        # Batting
        # -------------------------
        for batsman in innings.get("batsman", []):

            result["batting"].append({
                "match_id": match_id,
                "innings_id": innings_id,
                "team": batting_team,
                "player_id": batsman.get("id"),
                "player_name": batsman.get("name"),
                "runs": batsman.get("runs"),
                "balls": batsman.get("balls"),
                "fours": batsman.get("fours"),
                "sixes": batsman.get("sixes"),
                "strike_rate": float(
                    batsman.get("strkrate") or 0
                ),
                "dismissal": batsman.get("outdec")
            })

        # -------------------------
        # Bowling
        # -------------------------
        for bowler in innings.get("bowler", []):

            result["bowling"].append({
                "match_id": match_id,
                "innings_id": innings_id,
                "player_id": bowler.get("id"),
                "player_name": bowler.get("name"),
                "overs": bowler.get("overs"),
                "maidens": bowler.get("maidens"),
                "runs": bowler.get("runs"),
                "wickets": bowler.get("wickets"),
                "economy": float(
                    bowler.get("economy") or 0
                ),
                "balls": bowler.get("balls")
            })

        # -------------------------
        # Partnerships
        # -------------------------
        partnership_data = innings.get(
            "partnership", {}
        ).get("partnership", [])

        for partnership in partnership_data:

            result["partnerships"].append({
                "match_id": match_id,
                "innings_id": innings_id,

                "batsman1_id": partnership.get("bat1id"),
                "batsman1_name": partnership.get("bat1name"),
                "batsman1_runs": partnership.get("bat1runs"),
                "batsman1_balls": partnership.get("bat1balls"),

                "batsman2_id": partnership.get("bat2id"),
                "batsman2_name": partnership.get("bat2name"),
                "batsman2_runs": partnership.get("bat2runs"),
                "batsman2_balls": partnership.get("bat2balls"),

                "total_runs": partnership.get("totalruns"),
                "total_balls": partnership.get("totalballs")
            })

        # -------------------------
        # Fall of wickets
        # -------------------------
        fow_data = innings.get(
            "fow", {}
        ).get("fow", [])

        for fow in fow_data:

            result["fall_of_wickets"].append({
                "match_id": match_id,
                "innings_id": innings_id,
                "player_id": fow.get("batsmanid"),
                "player_name": fow.get("batsmanname"),
                "over": fow.get("overnbr"),
                "team_runs": fow.get("runs"),
                "ball": fow.get("ballnbr")
            })

    return result