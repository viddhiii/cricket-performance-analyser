# 🏏 International Cricket Performance Analyser

An interactive data analytics dashboard analysing **3.7 million deliveries** 
across 6,664 international cricket matches - Tests, ODIs and T20Is.

## 🔴 Live Demo
👉 https://viddhiii-cricket-performance-analyser-app-gvihkz.streamlit.app

## 📊 What it does
- Analyses batting and bowling performance across all international teams
- Compares players across 3 formats - Test, ODI and T20
- Custom **Performance Index** built from scratch to rank players
- Interactive team comparison for top 10 cricket nations
- Player search - find stats for any international cricketer

## 🛠️ Tech Stack
- Python, Pandas, Matplotlib, Streamlit
- Data: Cricsheet.org (ball-by-ball match data)
- 3.7M deliveries | 6,664 matches | 1,155 batters | 824 bowlers

## 📁 Project Structure
- `app.py` - Streamlit dashboard
- `batting_stats.csv` - Processed batting statistics
- `bowling_stats.csv` - Processed bowling statistics
- `team_stats.csv` - Team performance by format
- `matches.csv` - Match level data

## 🔍 Pages
- **Overview** - Dataset summary and matches over time
- **Batting** - Top batters by runs, strike rate, average
- **Bowling** - Top bowlers by wickets, economy, average
- **Teams** - Country comparison across formats
- **Player Search** - Search any international cricketer

## ⚠️ Note
Data sourced from Cricsheet.org covering international matches up to 
early 2025. Women's cricket analysis coming in next version.

## 👩‍💻 Built by
Vidhi Prajapati - Data Analytics Portfolio Project
