
from tkinter.filedialog import Open

import pandas as pd
import matplotlib.pyplot as plt

# Load the baseball datasets
batting = pd.read_csv("Batting.csv")
people = pd.read_csv("People.csv")
teams = pd.read_csv("Teams.csv")

# Explore the batting dataset
print("Dataset shape:")
print(batting.shape)

print("\nColumn names:")
print(batting.columns.tolist())

print("\nDataset information:")
batting.info()

# Find the top 10 players by total home runs
top_home_run_hitters = (
    batting.groupby("playerID")["HR"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 players by home runs:")
print(top_home_run_hitters)

# Step 11: Visualise the top 10 home-run hitters
plt.figure(figsize=(10, 6))

top_home_run_hitters.sort_values().plot(kind="barh")

plt.title("Top 10 Players by Career Home Runs")
plt.xlabel("Total Home Runs")
plt.ylabel("Player ID")

plt.tight_layout()
plt.savefig("charts/top_home_run_hitters.png", dpi=300, bbox_inches="tight")
plt.show()


# Step 12: Match player IDs with their real names
top_home_run_df = top_home_run_hitters.rename("HR").reset_index()

top_home_run_df = top_home_run_df.merge(
    people[["playerID", "nameFirst", "nameLast"]],
    on="playerID",
    how="left"
)

top_home_run_df["playerName"] = (
    top_home_run_df["nameFirst"].fillna("")
    + " "
    + top_home_run_df["nameLast"].fillna("")
)

print("\nTop 10 home-run hitters with real names:")
print(top_home_run_df[["playerName", "HR"]])

# Step 13: Create a bar chart using real player names
named_hitters = top_home_run_df.sort_values("HR")

plt.figure(figsize=(10, 6))

plt.barh(named_hitters["playerName"], named_hitters["HR"])

plt.title("Top 10 Players by Career Home Runs")
plt.xlabel("Total Home Runs")
plt.ylabel("Player Name")

plt.tight_layout()
plt.show()

# Step 14: Analyse home runs over time
home_runs_by_year = batting.groupby("yearID")["HR"].sum()

print("\nTotal home runs by year:")
print(home_runs_by_year.tail(10))

# Create a line graph
plt.figure(figsize=(12, 6))

plt.plot(home_runs_by_year.index, home_runs_by_year.values)

plt.title("Total Home Runs by Year")
plt.xlabel("Year")
plt.ylabel("Total Home Runs")

plt.tight_layout()
plt.savefig("charts/chart_3.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 15: Analyse hits over time
hits_by_year = batting.groupby("yearID")["H"].sum()

print("\nTotal hits by year:")
print(hits_by_year.tail(10))

# Create a line graph
plt.figure(figsize=(12, 6))

plt.plot(hits_by_year.index, hits_by_year.values)

plt.title("Total Hits by Year")
plt.xlabel("Year")
plt.ylabel("Total Hits")

plt.tight_layout()
plt.savefig("charts/chart_4.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 16: Find the top 10 team seasons by home runs
top_teams = teams.nlargest(10, "HR").copy()

top_teams["team_season"] = (
    top_teams["name"] + " (" + top_teams["yearID"].astype(str) + ")"
)

print("\nTop 10 team seasons by home runs:")
print(top_teams[["team_season", "HR"]])

# Create a horizontal bar chart
top_teams = top_teams.sort_values("HR")

plt.figure(figsize=(12, 7))

plt.barh(top_teams["team_season"], top_teams["HR"])

plt.title("Top 10 Team Seasons by Home Runs")
plt.xlabel("Total Home Runs")
plt.ylabel("Team and Year")

plt.tight_layout()
plt.savefig("charts/chart_5.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 17: Find players with the highest career batting averages

# Calculate each player's total hits and at-bats
player_stats = batting.groupby("playerID")[["H", "AB"]].sum()

# Remove players with zero at-bats
player_stats = player_stats[player_stats["AB"] > 0]

# Calculate batting average
player_stats["BA"] = player_stats["H"] / player_stats["AB"]

# Keep players with at least 500 at-bats
qualified_players = player_stats[player_stats["AB"] >= 500]

# Find the top 10 batting averages
top_batting_averages = qualified_players.sort_values(
    "BA", ascending=False
).head(10)

# Match player IDs with real names
top_batting_averages = top_batting_averages.reset_index()

top_batting_averages = top_batting_averages.merge(
    people[["playerID", "nameFirst", "nameLast"]],
    on="playerID",
    how="left"
)

top_batting_averages["playerName"] = (
    top_batting_averages["nameFirst"].fillna("")
    + " "
    + top_batting_averages["nameLast"].fillna("")
)

print("\nTop 10 Batting Averages:")
print(
    top_batting_averages[
        ["playerName", "H", "AB", "BA"]
    ].to_string(index=False)
)

# Create a bar chart
top_batting_averages = top_batting_averages.sort_values("BA")

plt.figure(figsize=(10, 6))
plt.barh(
    top_batting_averages["playerName"],
    top_batting_averages["BA"]
)

plt.title("Top 10 Career Batting Averages")
plt.xlabel("Batting Average")
plt.ylabel("Player Name")
plt.tight_layout()
plt.savefig("charts/chart_6.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 18: Analyse strikeouts over time

strikeouts_by_year = batting.groupby("yearID")["SO"].sum()

print("\nTotal Strikeouts by Year:")
print(strikeouts_by_year.tail(10))

# Create a line graph
plt.figure(figsize=(12, 6))

plt.plot(
    strikeouts_by_year.index,
    strikeouts_by_year.values
)

plt.title("Total Strikeouts by Year")
plt.xlabel("Year")
plt.ylabel("Total Strikeouts")
plt.tight_layout()
plt.savefig("charts/chart_7.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 19: Find the top 10 players by career hits

career_hits = (
    batting.groupby("playerID")["H"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Convert the results into a DataFrame
career_hits_df = career_hits.rename("Hits").reset_index()

# Match player IDs with real names
career_hits_df = career_hits_df.merge(
    people[["playerID", "nameFirst", "nameLast"]],
    on="playerID",
    how="left"
)

career_hits_df["playerName"] = (
    career_hits_df["nameFirst"].fillna("")
    + " "
    + career_hits_df["nameLast"].fillna("")
)

print("\nTop 10 Players by Career Hits:")
print(
    career_hits_df[["playerName", "Hits"]]
    .to_string(index=False)
)

# Create a horizontal bar chart
career_hits_df = career_hits_df.sort_values("Hits")

plt.figure(figsize=(10, 6))

plt.barh(
    career_hits_df["playerName"],
    career_hits_df["Hits"]
)

plt.title("Top 10 Players by Career Hits")
plt.xlabel("Total Career Hits")
plt.ylabel("Player Name")
plt.tight_layout()
plt.savefig("charts/chart_8.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 20: Compare home runs and hits for the top 10 players

# Calculate each player's career home runs and hits
player_comparison = batting.groupby("playerID")[["HR", "H"]].sum()

# Find the top 10 players by home runs
player_comparison = player_comparison.sort_values(
    "HR", ascending=False
).head(10)

# Match player IDs with real names
player_comparison = player_comparison.reset_index()

player_comparison = player_comparison.merge(
    people[["playerID", "nameFirst", "nameLast"]],
    on="playerID",
    how="left"
)

player_comparison["playerName"] = (
    player_comparison["nameFirst"].fillna("")
    + " "
    + player_comparison["nameLast"].fillna("")
)

print("\nHome Runs vs. Hits:")
print(
    player_comparison[
        ["playerName", "HR", "H"]
    ].to_string(index=False)
)

# Create a comparison chart
chart_data = player_comparison.sort_values("HR")

plt.figure(figsize=(12, 7))

plt.barh(
    chart_data["playerName"],
    chart_data["H"],
    label="Hits"
)

plt.barh(
    chart_data["playerName"],
    chart_data["HR"],
    label="Home Runs"
)

plt.title("Career Hits vs. Home Runs")
plt.xlabel("Total Career Count")
plt.ylabel("Player Name")
plt.legend()
plt.tight_layout()
plt.savefig("charts/chart_9.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 21: Count the number of players recorded each year

players_by_year = batting.groupby("yearID")["playerID"].nunique()

print("\nNumber of Players Recorded in Each Year:")
print(players_by_year.tail(10))

# Create a line graph
plt.figure(figsize=(12, 6))

plt.plot(
    players_by_year.index,
    players_by_year.values
)

plt.title("Number of Players Recorded by Year")
plt.xlabel("Year")
plt.ylabel("Number of Players")
plt.tight_layout()
plt.savefig("charts/chart_10.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 22: Count the number of teams recorded each year

teams_by_year = teams.groupby("yearID")["teamID"].nunique()

print("\nNumber of Teams Recorded Each Year:")
print(teams_by_year.tail(10))

# Create a line graph
plt.figure(figsize=(12, 6))

plt.plot(
    teams_by_year.index,
    teams_by_year.values
)

plt.title("Number of Teams Recorded by Year")
plt.xlabel("Year")
plt.ylabel("Number of Teams")
plt.tight_layout()
plt.savefig("charts/chart_11.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 23: Find the top 10 players by career runs

career_runs = (
    batting.groupby("playerID")["R"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Convert results into a DataFrame
career_runs_df = career_runs.rename("Runs").reset_index()

# Match player IDs with real names
career_runs_df = career_runs_df.merge(
    people[["playerID", "nameFirst", "nameLast"]],
    on="playerID",
    how="left"
)

career_runs_df["playerName"] = (
    career_runs_df["nameFirst"].fillna("")
    + " "
    + career_runs_df["nameLast"].fillna("")
)

print("\nTop 10 Players by Career Runs:")
print(
    career_runs_df[["playerName", "Runs"]]
    .to_string(index=False)
)

# Create a horizontal bar chart
career_runs_df = career_runs_df.sort_values("Runs")

plt.figure(figsize=(10, 6))

plt.barh(
    career_runs_df["playerName"],
    career_runs_df["Runs"]
)

plt.title("Top 10 Players by Career Runs")
plt.xlabel("Total Career Runs")
plt.ylabel("Player Name")
plt.tight_layout()
plt.savefig("charts/chart_12.png", dpi=300, bbox_inches="tight")
plt.show()


# Step 24: Find the top 10 players by career RBI

career_rbi = (
    batting.groupby("playerID")["RBI"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Convert results into a DataFrame
career_rbi_df = career_rbi.rename("RBI").reset_index()

# Match player IDs with real names
career_rbi_df = career_rbi_df.merge(
    people[["playerID", "nameFirst", "nameLast"]],
    on="playerID",
    how="left"
)

career_rbi_df["playerName"] = (
    career_rbi_df["nameFirst"].fillna("")
    + " "
    + career_rbi_df["nameLast"].fillna("")
)

print("\nTop 10 Players by Career RBI:")
print(
    career_rbi_df[["playerName", "RBI"]]
    .to_string(index=False)
)

# Create a horizontal bar chart
career_rbi_df = career_rbi_df.sort_values("RBI")

plt.figure(figsize=(10, 6))

plt.barh(
    career_rbi_df["playerName"],
    career_rbi_df["RBI"]
)

plt.title("Top 10 Players by Career RBI")
plt.xlabel("Total Career RBI")
plt.ylabel("Player Name")
plt.tight_layout()
plt.savefig("charts/chart_13.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 25: Analyse home runs by decade

# Create a decade column
batting_by_decade = batting.copy()

batting_by_decade["decade"] = (
    batting_by_decade["yearID"] // 10
) * 10

# Calculate total home runs for each decade
home_runs_by_decade = (
    batting_by_decade.groupby("decade")["HR"].sum()
)

print("\nTotal Home Runs by Decade:")
print(home_runs_by_decade)

# Create a bar chart
plt.figure(figsize=(12, 6))

plt.bar(
    home_runs_by_decade.index.astype(str),
    home_runs_by_decade.values
)

plt.title("Total Home Runs by Decade")
plt.xlabel("Decade")
plt.ylabel("Total Home Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/chart_14.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 26: Calculate average yearly home runs by decade

average_home_runs_by_decade = (
    home_runs_by_year.groupby((home_runs_by_year.index // 10) * 10).mean()
)

print("\nAverage Yearly Home Runs by Decade:")
print(average_home_runs_by_decade.round(2))

# Create a bar chart
plt.figure(figsize=(12, 6))

plt.bar(
    average_home_runs_by_decade.index.astype(str),
    average_home_runs_by_decade.values
)

plt.title("Average Yearly Home Runs by Decade")
plt.xlabel("Decade")
plt.ylabel("Average Home Runs per Year")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/chart_15.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 27: Find the top 10 years by total home runs

top_home_run_years = (
    batting.groupby("yearID")["HR"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Years by Total Home Runs:")
print(top_home_run_years)

# Sort chronologically for a clearer chart
chart_years = top_home_run_years.sort_index()

# Create a bar chart
plt.figure(figsize=(12, 6))

plt.bar(
    chart_years.index.astype(str),
    chart_years.values
)

plt.title("Top 10 Years by Total Home Runs")
plt.xlabel("Year")
plt.ylabel("Total Home Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/chart_16.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 28: Find the top 10 years by total hits

top_hit_years = (
    batting.groupby("yearID")["H"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Years by Total Hits:")
print(top_hit_years)

# Sort chronologically for a clearer chart
chart_hit_years = top_hit_years.sort_index()

# Create a bar chart
plt.figure(figsize=(12, 6))

plt.bar(
    chart_hit_years.index.astype(str),
    chart_hit_years.values
)

plt.title("Top 10 Years by Total Hits")
plt.xlabel("Year")
plt.ylabel("Total Hits")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/chart_17.png", dpi=300, bbox_inches="tight")
plt.show()

# Step 29: Find the top 10 years by total strikeouts

top_strikeout_years = (
    batting.groupby("yearID")["SO"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Years by Total Strikeouts:")
print(top_strikeout_years)

# Sort chronologically for the chart
chart_strikeout_years = top_strikeout_years.sort_index()

# Create a bar chart
plt.figure(figsize=(12, 6))

plt.bar(
    chart_strikeout_years.index.astype(str),
    chart_strikeout_years.values
)

plt.title("Top 10 Years by Total Strikeouts")
plt.xlabel("Year")
plt.ylabel("Total Strikeouts")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/chart_18.png", dpi=300, bbox_inches="tight")
plt.show()


# Step 30: Final Baseball Analysis Summary

# Find the player with the most career home runs
career_home_runs = batting.groupby("playerID")["HR"].sum()
top_hr_player_id = career_home_runs.idxmax()
top_hr_player_total = career_home_runs.max()

# Find the player with the most career hits
career_hits = batting.groupby("playerID")["H"].sum()
top_hits_player_id = career_hits.idxmax()
top_hits_player_total = career_hits.max()

# Look up the players' real names
top_hr_player = people.loc[
    people["playerID"] == top_hr_player_id
].iloc[0]

top_hits_player = people.loc[
    people["playerID"] == top_hits_player_id
].iloc[0]

top_hr_player_name = (
    str(top_hr_player["nameFirst"]) + " " +
    str(top_hr_player["nameLast"])
)

top_hits_player_name = (
    str(top_hits_player["nameFirst"]) + " " +
    str(top_hits_player["nameLast"])
)

# Find the year with the most total home runs
yearly_home_runs = batting.groupby("yearID")["HR"].sum()
top_hr_year = yearly_home_runs.idxmax()
top_hr_year_total = yearly_home_runs.max()

# Find the year with the most total hits
yearly_hits = batting.groupby("yearID")["H"].sum()
top_hits_year = yearly_hits.idxmax()
top_hits_year_total = yearly_hits.max()

# Display the final summary
print("\n" + "=" * 50)
print("          BASEBALL ANALYSIS SUMMARY")
print("=" * 50)

print(f"\nTop career home-run hitter: {top_hr_player_name}")
print(f"Career home runs: {top_hr_player_total:,}")

print(f"\nTop career hits leader: {top_hits_player_name}")
print(f"Career hits: {top_hits_player_total:,}")

print(f"\nYear with the most home runs: {top_hr_year}")
print(f"Total home runs that year: {top_hr_year_total:,}")

print(f"\nYear with the most hits: {top_hits_year}")
print(f"Total hits that year: {top_hits_year_total:,}")

print("\nAnalysis complete!")
print("=" * 50)

