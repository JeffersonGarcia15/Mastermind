# Mastermind Game App

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Game Rules](#game-rules)
- [Backend Architecture](#backend-architecture)
- [Endpoints & Documentation](#endpoints--documentation)
- [Testing](#testing)
- [Leaderboard & Scoring](#leaderboard--scoring)
- [UI & Frontend](#ui--frontend)
- [Local Setup](#local-setup)

---

## Overview

Welcome to the **Mastermind Game App**, an implementation of the classic Mastermind guessing game. The primary focus of this project is the **backend** logic, which includes authentication, playing a game, a history of a user's game and their game details as well as leaderboards with redis, and a rich set of API endpoints. We’ve also included a simple UI as a reference front end, showcasing how to interact with the backend from a browser-based interface.

This repository demonstrates clean code organization, testing, CI/CD with GitHub Actions, containerization with Docker, caching and leaderboards with Redis, persistent storage with PostgreSQL as well as good GitHub Pull Request practices with a `pull_request_template.md`.

---

Here is a walkthrough for how to play in the website and a couple of rules!

Complete walkthrough here with all the features: https://www.youtube.com/watch?v=9HUrlxFSY-w

## Features

- **User Authentication:**  
  Register, log in, and log out users. Sessions are maintained via sessions.

- **Game Logic:**  
  Start new games, make guesses (digits 0–7), and receive hints. The game can be played in medium (4 digits) or hard (6 digits) mode.

- **Scoring & Leaderboards:**  
  Track user scores and number of games played as well as the attempts it took to complete a game. Leaderboards show users with the most number of points and users with the most completed games.

- **Game History & Details:**  
  View a list of previously played games and inspect the details of each game, including attempts, hints, final solution, and final result.

- **Caching & Performance:**  
  Redis integration for caching leaderboard results for efficient retrieval.

- **Custom Algorithm:**
  Custom algorithm, inspired by the [Bulls and Cows](https://leetcode.com/problems/bulls-and-cows/description/) algorithm, modified to meet the project's need.

- **Containerization:**
  Created containers for dev and test app.

- **Tests:**
  Implemented both unit and integration tests for the core requirements of the game such as starting a game and making a guess. Tests use their own backend and test app and are run in their `docker-compose-test.yml`

- **UI:**  
  A minimal front-end client (React-based) demonstrating how to sign in, start a game, make guesses, view history, and see leaderboards and ability to play the last "ongoing" match you had before logging in(handle through local storage). Very little styling at the moment but enough to be able to see all implemented features.

---

## Game Rules

1. **Sequence Generation:**  
   At the start of each game, the server chooses a random sequence of 4 or 6 digits (0–7), depending on the difficulty.
   If the `Random.org` API is down, rather than not allowing the user to play the game we generate a sequence locally.
   At the same time we are storing a `fallback_used` boolean in the db which will serve for monitoring purposes.
   If the number of times the `fallback_used` is True, meaning that the Random.org API failed and we generated the sequence locally is quite high, we might consider replacing the third party API.

2. **Making Guesses:**  
   Players guess a combination of digits. After each guess, out of a total of 10, the server returns hints:

   - **correct_numbers_only:** Correct digit in the correct position.
   - **correct_positions:** Correct digit in the wrong position.
   - **attempts_left:** The number of attempts you have left before losing the game
   - **status:** Either `ongoing`, `win` or `lose`.

3. **Attempts & Winning:**  
   The player has up to 10 attempts to guess the correct sequence. If they guess it before running out of attempts, they win. Otherwise, they lose.

4. **Scoring:**  
   Score is based on the number of attempts left. So if you win in your last attempt you get a point only. Hard mode grants additional points, 5 to be precised.

---

## Backend Architecture

- **Stack:**  
  Python, Flask, SQLAlchemy, Alembic for migrations, Docker, Redis and PostgreSQL as the database.

- **Authentication:**  
  Session auth for secure endpoints. Logged-in users can access their history, start new games, and see their own scores.

- **Docker & Docker Compose:**  
  The entire backend can be run in Docker containers. Below are the services for the `mastermind_dev` and `mastermind_test` containers.

  - **db:** Runs PostgreSQL
  - **redis:** For caching leaderboards
  - **app:** The Flask backend

  - **db:** Runs PostgreSQL
  - **redis:** For caching leaderboards
  - **app:** The Flask backend

- **Migrations:**  
  Uses Flask-Migrate and Alembic to handle database schema changes.

- **Seeders:**
  Uses a flask command to generate users and games with random number of attempts. This is helpful to see the leaderboard in action.
  For now, we generate as many games as the `user_id` which depends on the index.
  We generate 15 users where user 1 has 1 game, user 2 has 2 games and so on.

---

## Endpoints & Documentation

A full list of the primary game endpoints, so not all endpoints have been documented or tested because of the time constraints, and their parameters is documented in our Docusaurus-based documentation:

- **API Docs:** [Docusaurus Docs Link](https://mastermind-ten.vercel.app/docs/overview)

Endpoints include:

- **Auth:** `/api/v2/auth/login`, `/api/v2/auth/signup`, `/api/v2/auth/logout`
- **Game:** `/api/v2/game/start`, `/api/v2/game/guess`, `/api/v2/game/force_lose`
- **History:** `/api/v2/history/all_games`, `/api/v2/history/game_details/{game_id}`
- **Leaderboards:** `/api/v2/leaderboard/score`, `/api/v2/leaderboard/games`, `/api/v2/leaderboard/score/refresh` for debugging redis if needed, `/api/v2/leaderboard/games/refresh` for debugging redis if needed.

Each endpoint description, payload, and response examples are in the linked external docs.

---

## Testing

- **Unit & Integration Tests:**  
  Written using `pytest` and `request_mock`. Covers backend game logic, endpoints, and authentication.

- **CI/CD with GitHub Actions:**  
  Linting (Flake8), formatting checks (Black) run on every push or PR. Because of the time constraints tests running on GitHub Actions was not able to get done.

- **Test Environment:**  
  Dockerized test environment ensures consistent results. Migrations run before tests, and test databases are isolated.

**Run tests locally:**

```bash
docker-compose -f docker-compose-test.yml -p mastermind_test up -d --build
# Wait for services
docker-compose -f docker-compose-test.yml -p mastermind_test exec test_app flask db upgrade
docker-compose -f docker-compose-test.yml -p mastermind_test exec test_app pytest tests/ -s
```

## Leaderboard & Scoring

**Extra Points for Hard Mode:**  
Hard difficulty sequences are longer and can yield bonus points.

**Leaderboards:**

- **By Score:** Top users by total score.
- **By Games:** Users who have completed the most games.

**Caching with Redis:**  
Leaderboard data is cached for fast retrieval. Updated periodically, every 60 seconds for demonstration purposes so that we see the redis cache getting in sync with the db as the project is presented.

---

## UI & Frontend

**UI Stack:**  
React-based front end (optional). Minimal pages for login, signup, starting a game, making guesses, viewing history, and leaderboards.

**Running UI Locally:**

```bash
cd frontend
npm install
npm start
```

Access at http://localhost:5173/

**Integration with Backend:**
The frontend fetches from http://localhost:5000/api/v2 as the base url. Adjust api.js BASE_URL if needed, in case your port 5000 is taken already.

## Local Setup

### Prerequisites

- [Python & Flask](https://gist.github.com/dineshviswanath/af72af0ae2031cd9949f)
- Docker & Docker Compose installed.
- [Node.js & npm for the frontend](https://nodejs.org/en/download/package-manager)

After setting up Docker, if you want the desktop version please download it from here https://www.docker.com/products/docker-desktop/

If by this point you are tired of reading, you can watch this video where I setup the app from scratch while having the prerequisites installed so that the walkthrough wasn't too long.

Part1: https://youtu.be/m74H-jvU5PM

Part2: https://youtu.be/9HUrlxFSY-w

### Backend Setup

**Clone the Repository:**

```bash
git clone https://github.com/JeffersonGarcia15/Mastermind.git
cd Mastermind
cd app
virtualenv .
source bin/activate
pip install -r requirements.txt
```

**Create a `.env` and a `.env.test` with environment variables:**

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
SQLALCHEMY_DATABASE_URI=postgresql://your_user:your_password@name_of_db_service_on_docker_compose:5432/your_db
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_super_secret_key
SESSION_TYPE=filesystem
```

Please add your own values for those keys, those are just examples.

**Build and Start Containers:**

Open two terminals, both located in the `app` folder.

```bash
docker-compose -p mastermind_dev up --build
```

If everything went well you should see messages like these ones

```bash
mastermind_app    |  * Serving Flask app 'app'
mastermind_app    |  * Debug mode: off
mastermind_app    | INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
mastermind_app    |  * Running on all addresses (0.0.0.0)
mastermind_app    |  * Running on http://127.0.0.1:5000
mastermind_app    |  * Running on http://172.23.0.4:5000
```

If a migrations folder or a versions > some_name.py file is not present then run

```bash
docker-compose -p mastermind_dev exec app flask db init
docker-compose -p mastermind_dev exec app flask create-db
docker-compose -p mastermind_dev exec app flask db migrate -m 'Initial message'
docker-compose -p mastermind_dev exec app flask db upgrade
```

If a migrations folder with a versions file exists then you can run the following command if your db does not have the migrations.

```bash
docker-compose -p mastermind_dev exec app flask create-db
docker-compose -p mastermind_dev exec app flask db upgrade
```

To check that everything went well with your db you can do the following:

```bash
docker-compose -p mastermind_dev up --build
docker-compose -p mastermind_dev exec db psql -U your_user_from_env -d your_db_from_env
```

then try the following command:

This commands lets you see all the tables

```bash
\dt
```

to exit run

```bash
\q
```

if you see the users, games, attempts and match_records table then you are good to go!

To run the seed command do:

```bash
docker-compose -p mastermind_dev exec app flask seed
```

You can check that there is data in the db now by running

```bash
docker-compose -p mastermind_dev exec db psql -U your_user_from_env -d your_db_from_env
SELECT * FROM games;
```

and you should see data there!

Now that the app has a migrations folder you can run the tests from the other docker-compose!

```bash
docker-compose -f docker-compose-test.yml -p mastermind_test up -d --build
docker-compose -f docker-compose-test.yml -p mastermind_test exec test_app pytest tests/ -s
```

If you want to check the endpoints only please use a tool like Postman. Below I have attached a public link to all the endpoints currently in my postman collection.

https://www.postman.com/navigation-astronomer-35854228/mastermind/collection/srkh99c/mastermind?action=share&creator=15583774

### Frontend Setup

**Create a `.env` and a `.env.test` with environment variables:**

```env
VITE_DEMO_NAME=user15
VITE_DEMO_PASSWORD=password
```

**Navigate to frontend folder:**
Assuming that you are in the root Mastermind folder

```bash
cd UI
npm install
```

**Run Frontend Server:**

```bash
npm run dev
```

### Documentation Setup (optional)

**Navigate to docs folder:**
Assuming that you are in the root Mastermind folder

```bash
cd mastermind-docs
npm install
```

**Run docusaurus app:**

```bash
npm start
```
