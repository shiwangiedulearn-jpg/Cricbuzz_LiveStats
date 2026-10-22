"""
Q1 - Find all players who represent India.

Requirement from project document:
Display full name, playing role, batting style, and bowling style.

IMPORTANT:
The current database does not contain a players table or columns for:
- player country/team
- playing role
- batting style
- bowling style

The Cricbuzz player-stats endpoint was also unavailable during collection because
the RapidAPI monthly quota was exhausted. Therefore this query cannot be
honestly executed against the current database without inventing data.

When player profile data is added later, the intended SQL shape is:

SELECT
    full_name,
    playing_role,
    batting_style,
    bowling_style
FROM players
WHERE country = 'India'
ORDER BY full_name;

Do not create a fake players table just to make this query appear complete.
"""

print("\nQ1 - Players Representing India")
print("-" * 70)
print("Cannot be calculated from the current database.")
print("Required player-profile fields are not stored:")
print("- country/team")
print("- playing role")
print("- batting style")
print("- bowling style")
