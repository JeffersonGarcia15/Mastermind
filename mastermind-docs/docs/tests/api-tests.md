---
id: api-tests
title: Integration Tests for Mastermind API
sidebar_label: Integration Tests
---

# Integration Tests for Mastermind API

Integration tests verify that different components of the Mastermind API work together as expected. This section details the integration test cases, their descriptions, endpoints, inputs, and expected outputs.

## **1. Test Cases Examples**

| **Test Case ID** | **Description**                                       | **Endpoint**             | **Method** | **Input**                                                              | **Expected Output**                                                                            |
| ---------------- | ----------------------------------------------------- | ------------------------ | ---------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| IT1              | Start game successfully (Medium Difficulty)           | `/api/game/start/medium` | `GET`      | None                                                                   | `200 OK`, unique `game_id`, and a valid game state initialized                                 |
| IT2              | Guess correctly and win the game (Medium)             | `/api/game/guess`        | `POST`     | `{ "game_id": "valid_id", "guess": "1234" }`                           | `200 OK`, `status: "win"`, all `correct_positions` match                                       |
| IT3              | Guess incorrectly and lose after 10 attempts (Medium) | `/api/game/guess`        | `POST`     | `{ "game_id": "valid_id", "guess": "5678" }` repeated 10 times         | `200 OK`, `status: "lose"`, `attempts_left: 0`                                                 |
| IT4              | Invalid game ID                                       | `/api/game/guess`        | `POST`     | `{ "game_id": "invalid_id", "guess": "1234" }`                         | `400 Bad Request` with descriptive error message                                               |
| IT5              | Invalid input format (non-numeric guess)              | `/api/game/guess`        | `POST`     | `{ "game_id": "valid_id", "guess": "abcd" }`                           | `400 Bad Request` with descriptive error message                                               |
| IT6              | Start game successfully (Hard Difficulty)             | `/api/game/start/hard`   | `GET`      | None                                                                   | `200 OK`, unique `game_id`, and a valid game state initialized                                 |
| IT7              | Guess correctly and win the game (Hard)               | `/api/game/guess`        | `POST`     | `{ "game_id": "valid_id", "guess": "012345" }`                         | `200 OK`, `status: "win"`, all `correct_positions` match                                       |
| IT8              | Guess incorrectly and lose after 10 attempts (Hard)   | `/api/game/guess`        | `POST`     | `{ "game_id": "valid_id", "guess": "567801" }`                         | `200 OK`, `status: "lose"`, `attempts_left: 0`                                                 |
| IT9              | Make a guess after winning the game                   | `/api/game/guess`        | `POST`     | `{ "game_id": "win_game_id", "guess": "1234" }`                        | `400 Bad Request` with descriptive error message                                               |
| IT10             | Make a guess after losing the game                    | `/api/game/guess`        | `POST`     | `{ "game_id": "lose_game_id", "guess": "5678" }`                       | `400 Bad Request` with descriptive error message                                               |
| IT11             | Start game with API failure triggering fallback       | `/api/game/start/medium` | `GET`      | None (API fails)                                                       | `200 OK`, unique `game_id`, fallback sequence generated, `is_sequence_locally_generated: true` |
| IT12             | Start game with hard difficulty and fallback          | `/api/game/start/hard`   | `GET`      | None (API fails)                                                       | `200 OK`, unique `game_id`, fallback sequence generated, `is_sequence_locally_generated: true` |
| IT13             | Guess correctly and win the game with fallback        | `/api/game/guess`        | `POST`     | `{ "game_id": "fallback_win_id", "guess": "0123" }`                    | `200 OK`, `status: "win"`, solution revealed, `is_sequence_locally_generated: true`            |
| IT14             | Guess incorrectly and lose with fallback              | `/api/game/guess`        | `POST`     | `{ "game_id": "fallback_lose_id", "guess": "5678" }` repeated 10 times | `200 OK`, `status: "lose"`, solution revealed, `attempts_left: 0`                              |
