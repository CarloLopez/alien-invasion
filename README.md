# Alien Invasion

## Project Overview
"Alien Invasion" is an arcade-style game developed in Python. Players take control of a rocket ship positioned at the bottom center of the screen, using arrow keys to navigate and the spacebar to fire bullets. The primary objective is to obliterate a fleet of aliens moving across and down the screen. With each level, the game introduces a faster fleet of aliens, increasing the challenge. The game ends if an alien collides with the player's ship or reaches the bottom of the screen, with players having a life limit.

## Installation
Ensure you have Python installed on your system. Additionally, the game requires Pygame. Install Pygame using the following command in your terminal:

```bash
py -m pip install -U pygame --user
```
## How to Play
- **Starting the Game**: Execute `alien_invasion.py` to begin.
- **Controls**:
  - **Move**: Use the left and right arrow keys.
  - **Shoot**: Press the spacebar.

## Features
- **Difficulty Levels**: Select from Normal or Hardmode.
- **Interactive Gameplay**: Aliens shoot back at the player randomly.
- **Player Power-ups**: Gain random power-ups during the game.
- **Audio and Visual Experience**: Includes background music and sound effects for an immersive experience.
- **Persistent High Score**: High scores are saved using a .json file.

### Additional Features
These features have been added to expand upon the original project from "Python Crash Course" by Eric Matthes:
- Difficulty settings for varied gameplay experiences.
- Aliens with the ability to shoot at the player.
- Collectible power-ups for the player.
- Enhanced audio and visual elements.
- A system to save high scores persistently.
