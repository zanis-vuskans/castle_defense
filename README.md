# Castle Defense

A small incremental defense game built with Python and [pygame](https://www.pygame.org/). Enemies march down the screen toward your castle wall. Shoot them, earn points, and spend those points on upgrades that let you hold out longer.

Built as a first solo project for [boot.dev](https://www.boot.dev/).

## How it works

- **Click to shoot.** Click anywhere on the screen to fire a shot from the player at that point.
- **Earn points.** Every hit gives 1 point, and every kill gives a 10-point bonus.
- **Spend points on upgrades** (buttons bellow player):
  - **Click Damage**: your shots hit harder.
  - **Tower Damage**: automatic towers hit harder.
  - **Tower Fire Rate**: automatic towers shoot faster.
  - **Buy Tower**: add another tower that fires at enemies on its own (limited to a maximum number).
- **Costs scale up.** Each upgrade gets more expensive the more you buy it 
- **Difficulty ramps with kills.** Enemies get more health, spawn faster, and more can be on screen at once as your kill count grows.
- **Protect the wall.** Enemies damage the wall when they reach it. If it breaks, you get a game over screen with to total kills you got
- **Progress is saved** to a local `save.json` file, so you can pick up where you left off.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/) (recommended), or `pip`
- pygame 2.6.1 (installed automatically with the steps below)

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/zanis-vuskans/castle_defense.git
cd castle_defense
```

### 2. Install dependencies and run

**With uv (recommended):**

```bash
uv sync
uv run main.py
```

**With pip:**

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install pygame==2.6.1
python main.py
```


## Resetting your progress

Enemies destroy the wall or delete the `save.json` file in the project folder and start the game again.
