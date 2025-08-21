# SudokuVerse

A modern web-based Sudoku game built with Flask and Docker, featuring user authentication, statistics tracking, and 
an interactive gameplay experience.

***Developed as a 12th grade computer science project.***

## Table of Contents

* [Features](#features)
* [Game Features](#game-features)
  * [Sudoku Solver](#sudoku-solver)
  * [User Interface](#user-interface)
  * [Statistics](#statistics)
* [Tech Stack](#tech-stack)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Configuration](#configuration)

## Features

- **Interactive Sudoku Gameplay**: Clean, responsive grid interface with intuitive controls
- **User Authentication**: Secure login and signup system
- **Statistics Tracking**: Monitor your progress and performance over time
- **Multiple Game Modes**: Various difficulty levels and gameplay options

## Game Features

### Sudoku Solver

- Advanced algorithm for puzzle generation and solving
- Configurable difficulty levels
- Automatic puzzle validation

### User Interface

* Clean, modern design with custom styling
* Interactive grid with hover effects and visual feedback
* Timer functionality for tracking solve times
* Hint system and error checking

### Statistics

* Track completion times
* Monitor accuracy and progress
* Historical performance data

## Tech Stack

- **Backend**: Python with Flask framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Configured for production use
- **Containerization**: Docker and Docker Compose
- **Font**: Metropolis (self-hosted)

## Getting Started

### Prerequisites

- Docker Desktop: 4.43
- MySQL: 8.0
- Docker: 28.3

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sudokuverse
   ```

2. **Configure the application**

   - Windows:
     ```commandline
     copy instance/config.toml.sample instance/config.toml
     copy .env.sample .env
     ```

   - Linux:
     ```bash
     cp instance/config.toml.sample instance/config.toml
     cp .env.sample .env
     ```
  
   - Open these files and update them according to your settings.

3. **Run with Docker**
   ```
   docker compose up -d
   ```
   
4. **Access the application**

   Open your browser and navigate to http://localhost:5000

## Configuration

The application uses configuration files located in the instance/ directory:

- `config.toml`: Main application configuration
- `error_messages.toml`: Custom error messages
