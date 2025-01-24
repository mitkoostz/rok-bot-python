# Rise of Kingdoms BOT
Development started on 24th January 2025

## Overview
`rok-bot-python` is a bot designed to automate certain actions in the game "Rise of Kingdoms" using the BlueStacks emulator. The bot can search for barbarians, increase or decrease their level, and initiate attacks.

## Features
- Connects to BlueStacks emulator
- Searches for barbarians on the map
- Adjusts barbarian levels
- Initiates attacks on barbarians
- Handles marching and combat states

## Requirements
- Python 3.x
- BlueStacks emulator
- Required Python libraries:
  - `pytesseract`
  - `Pillow`

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/mitkoostz/rok-bot-python.git
    cd rok-bot-python
    ```

2. Install the required libraries:
    ```sh
    pip install pytesseract pillow
    ```

3. Ensure that Tesseract-OCR is installed on your system. You can download it from [here](https://github.com/tesseract-ocr/tesseract).

## Usage
1. Start the BlueStacks emulator and ensure the game "Rise of Kingdoms" is running.
2. Run the bot:
    ```sh
    python main.py
    ```

## File Structure
- `main.py`: The main entry point of the bot.
- `BarbarianBot.py`: Contains the `BarbarianBot` class with methods to handle barbarian-related actions.
- `Coordinates.py`: Contains the coordinates used for clicking buttons in the game.
- `GameBot.py`: Contains the `GameBot` class for general bot actions.
- `BlueStacksAppChecker.py`: Contains methods to check if BlueStacks is running.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
