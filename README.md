# Translation Bot 2

![Translation Bot](https://img.shields.io/badge/Translation-Bot-blue)

Translation Bot 2 is a powerful and efficient translation bot that leverages various APIs to provide seamless translation services. This bot is designed to be easily deployable using Docker and Docker Compose.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Supports multiple languages
- Easy to deploy with Docker
- Integrates with DeepL API for high-quality translations
- Maintains user history and translation states

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

    ```sh
    git clone https://github.com/Warmetallic/translation-bot-2.git
    cd translation-bot-2
    ```

2. Copy the `.env.template` to `.env` and fill in the required environment variables:

    ```sh
    cp .env.template .env
    nano .env
    ```

3. Build and run the Docker containers:

    ```sh
    docker-compose up -d --build
    ```

## Usage

Once the containers are up and running, the bot will be active and ready to use. You can interact with the bot through the specified endpoints and commands.

## Configuration

The bot can be configured using environment variables specified in the `.env` file. Here are the key variables:

- `BOT_KEY`: The key for the bot.
- `API_KEY`: The API key for the translation service.

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.