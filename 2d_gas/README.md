# Pygame 2D Gas Simulation

![Gas simulation in the box](./videos/2dgas.gif)

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [TODO](#todo)

## Description

This Python Pygame project is a simulation of a two-dimensional gas system. It includes the implementation of a physics engine for particle movements, collisions, and the ability to draw walls that particles can interact with. The simulation provides a visual representation of gas particles bouncing off each other and reacting to the presence of walls.

## Features

- Real-time simulation of a two-dimensional gas system.
- Physics engine for accurate particle movements and collisions.
- Interactive wall drawing for customizing the simulation environment.
- Adjustable parameters for controlling particle behavior.
- Some real-time statistics about observed system.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/slava-qw/game.git
   ```

2. Navigate to the project directory:

   ```bash
   cd game/2d_gas
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulation script to start the 2D gas simulation:

```bash
python main.py
```

Adjust the simulation parameters and draw walls interactively to observe the gas particles' behavior.

## Controls

- **Left Click**: Start drawing walls in the simulation.
- **R**: Restart the simulation.
- **Esc**: Exit the simulation.

## TODO
- Add chunk optimisation, like [here](https://youtu.be/5Ka3tbbT-9E?si=wzKH-vOJXShq-b5e) or [here](https://youtu.be/eED4bSkYCB8?si=zXZ9QaoGsh-I-fKV).
- Add more features related to the walls.
- Add different types of particles and its interactions.
