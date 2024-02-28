# Physarum / Slime Mold Simulation

<div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
    <div style="width: 49%; margin-bottom: 1%;">
        <img src="./videos/output3.6.gif" style="width: 100%;">
    </div>
    <div style="width: 49%; margin-bottom: 1%;">
        <img src="./videos/output3.7.gif" style="width: 100%;">
    </div>
    <div style="width: 49%;">
        <img src="./videos/output3.8_ with1000agents.gif" style="width: 100%;">
    </div>
    <div style="width: 49%;">
        <img src="./videos/output3.14_random_sampling.gif" style="width: 100%;">
    </div>
</div>

## Overview

This project is a simulation of the behavior of Physarum polycephalum, a type of slime mold, using neural cellular automata.
In this simulation, I aim to replicate some of these intriguing behaviors using neural cellular automaton.

## Table of Contents

- [Project Description](#project-description)
- [Getting Started](#getting-started)
- [Features](#features)
- [How It Works](#how-it-works)
- [Usage](#usage)

## Project Description

Slime molds exhibit fascinating emergent behaviors, and the Physarum model,
in particular, has been a source of inspiration for solving various optimization problems,
such as finding efficient transportation networks. This project explores the application of neural cellular automata to
simulate the movement and decision-making process of Physarum in a grid-based environment by using Pygame tools.

## Getting Started

Follow these steps to set up your environment:

1. Clone the repository:

   ```shell
   git clone https://github.com/slava-qw/game.git
   cd game/physarum
   ```

2. Run the simulation:

   ```shell
   python main.py
   ```

## Features

- **Grid Simulation**: Simulate Physarum behavior on a grid, where cells represent the environment.

- **Rule-Based Decisions**: Implement Physarum's decision-making process based on simple rules.

- **Visualization**: Visualize the growth and optimization process in real-time.

- **Parameter Tuning**: Adjust simulation parameters to observe different behaviors and outcomes.

## How It Works

The simulation is based on the concept of neural cellular automata ([video](https://youtu.be/3H79ZcBuw4M?si=pk_Wjyqfz0l0-onC) explanation). Physarum cells in the grid communicate with their neighboring cells and make decisions on where to move. The main components include:

- **Physarum Agents**: Each agent represents a Physarum cell and occupies a grid cell.

- **Local Sensing**: Agents sense their immediate surroundings to decide the direction of movement or in some ways makes the random decisions.

- **Decision Rules**: Implement rule-based decision-making for agents, allowing them to explore and optimize their path. Each agent tries to achive the best score for him. It can be done him by moving towards the slime trace leaved behind each agent. The trace after some time dissapears

- **Simulation Loop**: The simulation runs for a defined number of iterations, allowing the Physarum to evolve its behavior over time.

## Usage

You can customize and experiment with various aspects of the simulation, including:

- Grid size and shape
- Initial conditions
- Decision rules
- Simulation parameters

The primary simulation script, `main.py`, contains the main loop and visualization components. You can modify this script to tailor the simulation to your needs.