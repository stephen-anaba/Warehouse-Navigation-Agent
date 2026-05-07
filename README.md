# Logistics Robot Decision Agent

A mini AI system for a warehouse robot that navigates from a Start location to a Goal location using multiple AI techniques combined into one decision-making pipeline.

## Project Overview

This project simulates a logistics robot operating in a warehouse environment. Rather than simply finding the shortest path, the robot evaluates candidate routes by considering travel conditions, congestion, restricted areas, time of day, and uncertainty — then selects the **best** route based on all of these factors.

## AI Components

| Component | Description |
|---|---|
| **Search** | BFS or A* generates 2–3 candidate routes on a grid/map |
| **Machine Learning** | A Decision Tree predicts `delay_level` for each candidate route |
| **Logical Reasoning** | 4–6 decision rules accept, reject, or deprioritize routes |
| **Probability / Uncertainty** | Weighted scoring or conditional probability adjusts final preference |

## Project Structure

project/
├── main.py          # Entry point — runs the full pipeline
├── search.py        # Search component (BFS / A*)
├── ml.py            # ML component (model training + delay prediction)
├── reasoning.py     # Rules, scoring, and final route selection
└── data/
└── robot_delay_data.csv

## Dataset

**File:** `data/robot_delay_data.csv`

| Column | Values |
|---|---|
| `time_of_day` | morning, afternoon, evening, night |
| `zone_type` | normal, high_traffic, restricted |
| `congestion_level` | low, medium, high |
| `distance` | short, medium, long |
| `delay_level` | low, medium, high *(prediction target)* |

## How to Run

```bash
python main.py
```

## Expected Output
- Route A: short distance, predicted delay = high → rejected
- Route B: medium distance, predicted delay = low → accepted
- Route C: passes restricted zone → rejected

## Team Roles

| Role | Responsibility |
|---|---|
| **Thomas – Search Engineer** | Grid/map setup, BFS or A*, candidate path generation |
| **Quan – Data / ML Engineer** | Dataset loading, model training, delay prediction |
| **Stephen – Reasoning Engineer** | Decision rules, probability scoring, final route selection |

LinkedIn: 
