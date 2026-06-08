
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="International Cricket Performance Analyser",
    page_icon="🏏",
    layout="wide"
)

BASE = "/kaggle/input/notebooks/vidhi0405/cricket-performance-analyser"

@st.cache_data
def load_data():
    batting  = pd.read_csv("batting_stats.csv")
    bowling  = pd.read_csv("bowling_stats.csv")
    team     = pd.read_csv("team_stats.csv")
    matches  = pd.read_csv("matches.csv")
    matches["date"] = pd.to_datetime(matches["date"])
    return batting, bowling, team, matches

batting, bowling, team_stats, matches = load_data()

TOP_TEAMS = ["India", "Australia", "England", "Pakistan", "South Africa",
             "New Zealand", "West Indies", "Sri Lanka", "Bangladesh", "Zimbabwe"]

COLORS = {"Test": "#185FA5", "ODI": "#1D9E75", "T20": "#D85A30"}

# Header
st.title("🏏 International Cricket Performance Analyser")
st.markdown("Analysing **3.7 million deliveries** across 6,667 international matches - Tests, ODIs and T20Is.")
st.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "🏏 Batting", "🏐 Bowling", "🌍 Teams", "🔍 Player Search"]
)

# ─── OVERVIEW ───────────────────────────────────────────────
if page == "🏠 Overview":
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Deliveries", "3,767,802")
    col2.metric("Total Matches", "6,664")
    col3.metric("Unique Batters", str(batting["batter"].nunique()))
    col4.metric("Unique Bowlers", str(bowling["bowler"].nunique()))

    st.markdown("---")
    st.subheader("Matches by Format")
    fmt_counts = matches.groupby("format")["match_id"].nunique()
    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.bar(fmt_counts.index, fmt_counts.values,
                  color=[COLORS[f] for f in fmt_counts.index], edgecolor="none")
    for bar, val in zip(bars, fmt_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f"{val:,}", ha="center", fontsize=11, fontweight="bold")
    ax.set_ylabel("Number of Matches")
    ax.set_title("Matches per Format")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Matches played over time")
    yearly = matches.groupby(["year", "format"])["match_id"].nunique().reset_index()
    fig, ax = plt.subplots(figsize=(12, 4))
    for fmt, color in COLORS.items():
        data = yearly[yearly["format"] == fmt]
        ax.plot(data["year"], data["match_id"], label=fmt, color=color, linewidth=2)
    ax.set_xlabel("Year")
    ax.set_ylabel("Matches Played")
    ax.set_title("International Cricket Matches per Year")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

# ─── BATTING ────────────────────────────────────────────────
elif page == "🏏 Batting":
    st.subheader("Batting Performance")
    fmt = st.selectbox("Select Format", ["Test", "ODI", "T20"])
    metric = st.selectbox("Sort by", ["runs", "strike_rate", "avg_per_innings", "perf_index"])
    top_n = st.slider("Show top N players", 5, 20, 10)

    data = batting[batting["format"] == fmt].sort_values(metric, ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(data["batter"], data[metric], color=COLORS[fmt], edgecolor="none")
    ax.set_title(f"Top {top_n} Batters by {metric} - {fmt}", fontsize=13, fontweight="bold")
    ax.set_xlabel(metric.replace("_", " ").title())
    ax.invert_yaxis()
    for bar, val in zip(bars, data[metric]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"{val:,.1f}", va="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Raw Data")
    st.dataframe(data[["batter", "innings", "runs", "strike_rate", "avg_per_innings", "fours", "sixes", "perf_index"]].reset_index(drop=True))

# ─── BOWLING ────────────────────────────────────────────────
elif page == "🏐 Bowling":
    st.subheader("Bowling Performance")
    fmt = st.selectbox("Select Format", ["Test", "ODI", "T20"])
    metric = st.selectbox("Sort by", ["wickets", "economy", "avg", "perf_index"])
    top_n = st.slider("Show top N players", 5, 20, 10)

    ascending = metric in ["economy", "avg"]
    data = bowling[bowling["format"] == fmt].sort_values(metric, ascending=ascending).head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(data["bowler"], data[metric], color=COLORS[fmt], edgecolor="none")
    ax.set_title(f"Top {top_n} Bowlers by {metric} — {fmt}", fontsize=13, fontweight="bold")
    ax.set_xlabel(metric.replace("_", " ").title())
    ax.invert_yaxis()
    for bar, val in zip(bars, data[metric]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"{val:,.1f}", va="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Raw Data")
    st.dataframe(data[["bowler", "innings", "wickets", "overs", "economy", "avg", "sr", "perf_index"]].reset_index(drop=True))

# ─── TEAMS ──────────────────────────────────────────────────
elif page == "🌍 Teams":
    st.subheader("Team Performance")
    fmt = st.selectbox("Select Format", ["Test", "ODI", "T20"])

    data = team_stats[
        (team_stats["format"] == fmt) &
        (team_stats["team"].isin(TOP_TEAMS))
    ].sort_values("avg_runs", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.barh(data["team"], data["avg_runs"], color=COLORS[fmt], edgecolor="none")
        ax.set_title(f"Avg Runs per Innings - {fmt}", fontweight="bold")
        ax.invert_yaxis()
        for bar, val in zip(bars, data["avg_runs"]):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    f"{val:.0f}", va="center", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.barh(data["team"], data["avg_wickets"], color="#7F77DD", edgecolor="none")
        ax.set_title(f"Avg Wickets Lost per Innings - {fmt}", fontweight="bold")
        ax.invert_yaxis()
        for bar, val in zip(bars, data["avg_wickets"]):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    f"{val:.1f}", va="center", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("Team Stats Table")
    st.dataframe(data[["team", "matches_played", "avg_runs", "avg_wickets"]].reset_index(drop=True))

# ─── PLAYER SEARCH ──────────────────────────────────────────
elif page == "🔍 Player Search":
    st.subheader("Search any Player")

    # Get all unique player names from dataset
    all_batters = sorted(batting["batter"].unique().tolist())
    all_bowlers = sorted(bowling["bowler"].unique().tolist())
    all_players = sorted(set(all_batters + all_bowlers))

    selected = st.selectbox(
        "Select a player",
        options=[""] + all_players,
        format_func=lambda x: "Type to search..." if x == "" else x
    )

    if selected:
        bat_result  = batting[batting["batter"] == selected]
        bowl_result = bowling[bowling["bowler"] == selected]

        if not bat_result.empty:
            st.markdown(f"### 🏏 Batting stats for: {selected}")
            st.dataframe(bat_result[["batter", "format", "innings", "runs", "strike_rate",
                                      "avg_per_innings", "fours", "sixes", "perf_index"]].reset_index(drop=True))

            fig, ax = plt.subplots(figsize=(8, 3))
            for _, row in bat_result.iterrows():
                ax.bar(row["format"], row["runs"],
                       color=COLORS.get(row["format"], "#888"), edgecolor="none")
            ax.set_title(f"{selected} - Runs by Format")
            ax.set_ylabel("Total Runs")
            plt.tight_layout()
            st.pyplot(fig)

        if not bowl_result.empty:
            st.markdown(f"### 🏐 Bowling stats for: {selected}")
            st.dataframe(bowl_result[["bowler", "format", "innings", "wickets", "overs",
                                       "economy", "avg", "perf_index"]].reset_index(drop=True))

        if bat_result.empty and bowl_result.empty:
            st.warning("No stats found for this player.")

st.markdown("---")
st.markdown("**Built by Vidhi Prajapati** - Data Analytics Portfolio Project | Data: Cricsheet.org | 3.7M deliveries across 6,664 matches")
