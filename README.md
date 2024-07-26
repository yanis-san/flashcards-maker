# Flashcards Maker

Flashcards Maker is an application that generates flashcards of words in Japanese, Chinese, and Korean. It uses images and audio files to create educational videos.

## Features

- Generates flashcards with text in Japanese, Chinese, Korean, French, and Arabic.
- Creates audio files for each word.
- Generates videos from the flashcards and audio files.

## Prerequisites

- `pipenv` for dependency management

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yanis-san/flashcards-maker.git
    cd flashcards-maker
    ```

2. Create a virtual environment and install dependencies using `pipenv`:

    ```bash
    pipenv install
    ```

3. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

## Usage

1. Place your images in the `flashcards/` folder.

2. Ensure that the JSON files containing the word data are in the same directory as the main script.

3. Run the main script to generate the flashcards, audio files, and videos:

    ```bash
    python __main__.py
    ```

## Project Structure

- `flashcards/`: Folder containing the flashcard images.
- `fonts/`: Folder containing the fonts used for text on the flashcards.
- `templates/`: Folder containing the templates for each language's flashcards.
- `db.json`: Local database using TinyDB.
- `flashcards_maker.py`: Main script to generate the flashcards, audio files, and videos.
- `video_maker.py`: Script to generate videos from the flashcards and audio files.
