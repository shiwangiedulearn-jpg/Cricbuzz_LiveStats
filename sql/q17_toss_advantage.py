from sqlalchemy import text
from database.database import engine

print("\nQ17 cannot be calculated from the current dataset.")
print("Reason: toss winner and toss decision are not stored in the matches table.")
print("Required fields:")
print("- toss_winner")
print("- toss_decision (bat/bowl)")