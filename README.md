# Translation Bot 2

![Translation Bot](https://img.shields.io/badge/Translation-Bot-blue)

**Translation Bot 2** is a sophisticated and user-friendly bot designed to provide efficient translation services using various APIs, including DeepL. It supports multiple languages, offering a seamless experience for users who need translations in different languages. The bot is easily deployable using Docker and Docker Compose, making it accessible for a wide range of users.

Bot is available in telegram for usage https://t.me/GK_translation_2_bot

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
  - [Available Commands](#available-commands)
- [Configuration](#configuration)
- [Supported Languages](#supported-languages)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multi-Language Translation**: Supports a variety of languages, enabling users to translate text and documents effortlessly.
- **Docker-Based Deployment**: Quick and straightforward setup with Docker and Docker Compose.
- **High-Quality Translations**: Utilizes the DeepL API for accurate and contextually appropriate translations.
- **User Interaction History**: Tracks and manages translation history, allowing users to review past translations.
- **Error Handling & Robust Logging**: Ensures smooth operation and easy troubleshooting.
- **Deployed on Yandex Cloud**: The bot is currently running on Yandex Cloud (Ubuntu Virtual Machine using public IPv4 http://51.250.35.2/)

## Installation

### Prerequisites

Ensure the following software is installed on your system:

- **Docker**: Containerization platform for packaging and running applications.
- **Docker Compose**: Tool for defining and running multi-container Docker applications.

### Steps

1. **Clone the Repository**:

    Clone the project repository to your local machine:

    ```sh
    git clone https://github.com/Warmetallic/translation-bot-2.git
    cd translation-bot-2
    ```

2. **Configure Environment Variables**:

    Copy the `.env.template` file to `.env` and fill in the required environment variables:

    ```sh
    cp .env.template .env
    nano .env
    ```

3. **Build and Launch the Containers**:

    Build the Docker images and start the containers:

    ```sh
    docker-compose up -d --build
    ```

## Usage

Once the bot is up and running, it can be accessed through specified commands. The bot responds to various commands, providing functionalities such as translating text, retrieving translation history, and managing user data.

### Available Commands

- **/translate**: Starts a translation session. The bot prompts the user to choose a target language and input text for translation.

  **Example**:
  ```
  User: /translate
  Bot: Please choose a language to translate to:
  ```

- **/history**: Displays the user's translation history, including original and translated texts along with timestamps.

  **Example**:
  ```
  User: /history
  Bot: 
  1. Original Text: Hello
     Translated Text: Bonjour
     Date: 2024-07-31
  ```

- **/history_dates**: Allows the user to select a date and view translation history for that specific date.

  **Example**:
  ```
  User: /history_dates
  Bot: Please choose a date to view the translation history:
  ```

- **/delete_history**: Deletes the user's entire translation history.

  **Example**:
  ```
  User: /delete_history
  Bot: Deleted 5 records from your Translation History.
  ```

- **/translate_file**: Facilitates the translation of documents. The user uploads a document, selects a target language, and receives the translated document.

  **Example**:
  ```
  User: /translate_file
  Bot: Please choose a language to translate the document to:
  ```

## Configuration

The bot's settings are managed via the `.env` file. Key environment variables include:

- `BOT_KEY`: Authentication key for the bot.
- `API_KEY`: API key for the translation service.

Ensure these variables are correctly set for the bot to function properly.

## Supported Languages

Translation Bot 2 supports the following languages:

- 🇷🇺 **Russian** (RU)
- 🇬🇧 **English** (EN)
- 🇪🇸 **Spanish** (ES)
- 🇫🇷 **French** (FR)
- 🇩🇪 **German** (DE)
- 🇨🇳 **Chinese** (ZH)

Users can select these languages for both text and document translations, making the bot versatile for global use.

## Contributing

We welcome contributions from the community! To contribute, follow these steps:

1. **Fork the Repository**:

    Create a fork of the repository to work on your changes.

2. **Create a New Branch**:

    Create a new branch for your feature or bug fix:

    ```sh
    git checkout -b feature-branch
    ```

3. **Implement Your Changes**:

    Make the necessary changes or additions to the codebase.

4. **Commit and Push**:

    Commit your changes and push them to your forked repository:

    ```sh
    git commit -m 'Add new feature'
    git push origin feature-branch
    ```

5. **Open a Pull Request**:

    Open a pull request in the original repository to merge your changes.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file. This license allows for open-source collaboration and redistribution, making it ideal for community-driven projects.

---

This version of the README provides a comprehensive overview of the bot's features, usage, and configuration, along with detailed command descriptions and examples. The inclusion of flags and a well-organized layout enhances readability and appeal.
