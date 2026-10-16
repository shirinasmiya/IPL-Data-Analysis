import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load IPL dataset
df = pd.read_csv("IPL-Data-Analysis/matches.csv")

# Explore the data
print("\nFIRST FIVE ROWS")
print(df.head())

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATASET INFORMATION")
df.info()

print("\nMISSING VALUES")
print(df.isnull().sum())



# STEP 2: DATA CLEANING

print("\n--- DATA CLEANING ---")

# Keep the original data unchanged
clean_df = df.copy()

# 1. Check and remove duplicate rows
duplicate_count = clean_df.duplicated().sum()
clean_df = clean_df.drop_duplicates().copy()

print("Duplicate rows removed:", duplicate_count)

# 2. Fill missing city values
clean_df["city"] = clean_df["city"].fillna("Unknown")

# 3. Convert date column into datetime format
clean_df["date"] = pd.to_datetime(
    clean_df["date"],
    dayfirst=True,
    errors="coerce"
)

# 4. Remove umpire3 because all its values are missing
if clean_df["umpire3"].isna().all():
    clean_df = clean_df.drop(columns=["umpire3"])

# 5. Create a separate dataset for matches with a winner
results_df = clean_df.dropna(subset=["winner"]).copy()

# 6. Display cleaning summary
print("Rows before cleaning:", len(df))
print("Rows after cleaning:", len(clean_df))
print("Matches with a recorded winner:", len(results_df))

print("\nMissing values after cleaning:")
print(clean_df.isnull().sum())

# 7. Save cleaned data
clean_df.to_csv("IPL-Data-Analysis/cleaned_matches.csv", index=False)

print("\nCleaned dataset saved successfully!")



# STEP 3: TEAM PERFORMANCE ANALYSIS

wins = results_df["winner"].value_counts()

print("\n--- MATCHES WON BY EACH TEAM ---")
print(wins)

print("\nTeam with the most wins:", wins.idxmax())
print("Total wins:", wins.max())

# Create bar chart
plt.figure(figsize=(12, 6))

wins.plot(kind="bar")

plt.title("Total IPL Matches Won by Each Team")
plt.xlabel("Team")
plt.ylabel("Number of Matches Won")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("IPL-Data-Analysis/team_wins.png")
plt.show()


# QUESTION 2: DOES WINNING THE TOSS HELP WIN THE MATCH?

toss_df = results_df.dropna(
    subset=["toss_winner", "winner"]
).copy()

toss_wins_match = (
    toss_df["toss_winner"] == toss_df["winner"]
)

toss_percentage = toss_wins_match.mean() * 100

print("\n--- TOSS ANALYSIS ---")
print("Total matches analyzed:", len(toss_df))
print(
    f"Toss winner also won the match: "
    f"{toss_wins_match.sum()} matches"
)
print(
    f"Percentage: {toss_percentage:.2f}%"
)

# Create a pie chart
labels = ["Toss winner won", "Toss winner lost"]
counts = [
    toss_wins_match.sum(),
    (~toss_wins_match).sum()
]

plt.figure(figsize=(7, 7))
plt.pie(
    counts,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Does Winning the Toss Help Win the Match?")
plt.tight_layout()
plt.savefig("IPL-Data-Analysis/toss_analysis.png")
plt.show()



# QUESTION 3: TOP 10 IPL VENUES

venue_counts = clean_df["venue"].value_counts().head(10)

print("\n--- TOP 10 IPL VENUES ---")
print(venue_counts)

# Create horizontal bar chart
plt.figure(figsize=(10, 6))

venue_counts.sort_values().plot(kind="barh")

plt.title("Top 10 IPL Venues by Matches Hosted")
plt.xlabel("Number of Matches")
plt.ylabel("Stadium / Venue")
plt.tight_layout()

plt.savefig("IPL-Data-Analysis/top_venues.png")
plt.show()



# QUESTION 4: MATCHES BY YEAR

year_counts = (
    clean_df.dropna(subset=["date"])
    .groupby(clean_df["date"].dt.year)
    .size()
)

print("\n--- IPL MATCHES BY YEAR ---")
print(year_counts)

print("\nYear with most matches:", year_counts.idxmax())
print("Number of matches:", year_counts.max())

# Create line chart
plt.figure(figsize=(10, 5))

year_counts.plot(kind="line", marker="o")

plt.title("Number of IPL Matches by Year")
plt.xlabel("Year")
plt.ylabel("Number of Matches")
plt.grid(True)
plt.tight_layout()

plt.savefig("IPL-Data-Analysis/matches_by_year.png")
plt.show()



# QUESTION 5: TOP PLAYERS BY PLAYER OF THE MATCH AWARDS

player_awards = (
    clean_df["player_of_match"]
    .dropna()
    .value_counts()
)

print("\n--- TOP 10 PLAYERS BY AWARDS ---")
print(player_awards.head(10))

print("\nPlayer with most awards:", player_awards.idxmax())
print("Total awards:", player_awards.max())

# Create chart
plt.figure(figsize=(10, 6))

player_awards.head(10).sort_values().plot(kind="barh")

plt.title("Top 10 Players by Player of the Match Awards")
plt.xlabel("Number of Awards")
plt.ylabel("Player")
plt.tight_layout()

plt.savefig("IPL-Data-Analysis/top_players.png")
plt.show()
