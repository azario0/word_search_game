# Cosmic Word Search Game

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)
![Made with Pygame](https://img.shields.io/badge/Made%20with-Pygame-1f425f.svg)

A visually appealing, space-themed word search game built with Python and the Pygame library. Find all the hidden words related to space exploration in a dynamically generated grid!

## ✨ Features

*   **Dynamically Generated Grid**: Every game is a new challenge, as the grid and word placements are randomized on startup.
*   **Creative "Cosmic Neon" Theme**: A dark, space-themed UI with bright, neon-style text and highlights.
*   **Intuitive Mouse Controls**: Simply click and drag from the first letter to the last letter of a word to select it.
*   **Clear Visual Feedback**: Your current selection is highlighted in blue, and correctly found words are permanently marked in green.
*   **Dynamic Word List**: The list of words to find is displayed on the side, with found words being struck through in real-time.
*   **Win Condition**: A "You Win!" screen appears once all the words have been discovered.

## 🛠️ Requirements

*   Python 3.6+
*   Pygame library

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/azario0/word_search_game.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd word_search_game
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install pygame
    ```

## 🎮 How to Play

1.  **Run the game from your terminal:**
    ```bash
    python word_search_game.py
    ```

2.  **Find words:**
    *   Look for the words listed in the "WORDS TO FIND" panel on the right.
    *   Words can be hidden horizontally, vertically, or diagonally, in any direction (including backwards).
    *   When you find a word, click and hold the left mouse button on the first letter and drag your cursor to the last letter.
    *   Release the mouse button. If the word is correct, it will be highlighted on the grid and struck through in the list.

3.  **Win the game:**
    *   Find all the words in the list to complete the game!

## 🔧 Customization

It's easy to customize the game with your own words and theme!

### Changing the Word List

Open `word_search_game.py` and modify the `WORDS_TO_FIND` list near the top of the file:

```python
# Word List (Theme: Space Exploration)
WORDS_TO_FIND = [
    "YOUR", "CUSTOM", "WORDS", "GO", "HERE"
]
```

### Changing the Theme

All colors and fonts are defined as constants at the top of `word_search_game.py`. Feel free to change these values to create your own unique theme.

```python
# Colors (Creative Theme: "Cosmic Neon")
COLOR_BACKGROUND = (5, 10, 20)      # Deep space blue
COLOR_GRID_LINES = (40, 60, 80)     # Faint nebula lines
COLOR_LETTER = (200, 220, 255)      # Bright star white
# ... and so on
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

_Created by azario0_
