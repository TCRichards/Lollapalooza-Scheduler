# Lollapalooza-Scheduler

A festival schedule generator and interactive web app for the Lollapalooza board game! This project generates realistic festival lineups with constraint-based scheduling and provides an intuitive Dash web interface for exploring the generated schedules.

## About the Board Game

This app is the digital heart of a physical board game I've been developing and playtesting. Players navigate a generated festival schedule, making strategic decisions about which artists to see while managing limited time and energy. The schedule generator ensures balanced lineups with proper artist sizing and genre distribution - just like a real festival!

## Key Features

- **Smart Schedule Generation**: Creates realistic festival lineups with proper constraints (no artist conflicts, balanced stage usage, appropriate artist sizing) using a constraint satisfaction algorithms (it's not really that hard of a problem, but it was fun to implement!)
- **Interactive Web Interface**: Browse the generated schedule with color-coded artist information, genre icons, and responsive design.  Click on an artist to start playing a random song from their YouTube channel.  This is a core mechanic of the board game, where players get extra points if they can identify an artist's songs by ear.

## Code Structure

The project is split into two main modules:

- **`scheduling/`**: Core game logic and schedule generation
  - Artist definitions with size/genre classifications
  - Constraint-based scheduling algorithms
  - Festival parameters and validation rules
  - A somewhat representative dataset of artists and their genres.  I'd love to expand this over time!
  
- **`app/`**: Web interface and visualization
  - Dash web app with interactive schedule tables
  - Data serialization for web display
  - YouTube integration and visual styling

## Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management:

```bash
# Install dependencies
poetry install

# Run the web app
poetry run python -m lolla.app.app

# Or activate the virtual environment
poetry shell
python -m lolla.app.app
```

## Usage

Launch the app and click "Generate New Schedule" to create a fresh festival lineup. Each artist is displayed with their genre icon, name, size tier, and genre classification. Navigate through different time slots to see the full festival experience!

