# FastAPI Stepik App

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-311/)

A FastAPI-based web application using PostgreSQL as its database, designed for easy deployment in a development environment.

## Table of Contents
- [FastAPI Stepik App](#fastapi-stepik-app)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [First Start](#first-start)
  - [Quick Start](#quick-start)
  - [Quick Finish](#quick-finish)
  - [Logging](#logging)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **FastAPI**: High-performance web framework for building APIs with Python 3.6+
- **PostgreSQL**: Robust, open-source relational database
- **SQLAlchemy and Asyncpg**: For asynchronous database operations
- **Jinja2**: Fast, expressive, extensible templating engine
- **Loguru**: Library for simplified and structured logging
- **Alembic**: Lightweight database migration tool for SQLAlchemy

## First Start

```bash
git clone <repository-url>
cd <repository-directory>
poetry install
make up
make migrate
make run
```

## Quick Start

```bash
make run
```

The application will be available at
- http://127.0.0.1:8001

## Quick Finish

in separate terminal:
```bash
make stop
make clean_docker
```


API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://127.0.0.1:8001/docs
- Redoc: http://127.0.0.1:8001/redoc

## Logging

This project uses **Loguru** for structured logging, which is visualized directly in the console output. You can monitor logs in real-time while running the application or while interacting with the Docker containers.

## Configuration

The application uses environment variables for configuration. Copy the .env.example file to .env and adjust the values as needed:
cp .env.example .env
Key configuration options include:
- DATABASE_URL: PostgreSQL connection string
- DEBUG: Set to True for development mode

## Contributing

Feel free to submit issues or pull requests to improve the application.

## License

This project is licensed under the MIT License.
