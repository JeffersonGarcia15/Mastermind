---
title: API Design
---

# Mastermind Game API

## Overview

The Mastermind Game API enables developers to integrate the classic Mastermind game into their applications. It provides the following endpoints:

- **Start Game:** `GET /game/start/{difficulty}` – Initialize a new game with a specified difficulty(medium or hard).
- **Make a Guess:** `POST /game/guess` – Submit a guess for the current game.

## Authentication

No authentication is required to use the Mastermind Game API at this time. All endpoints are publicly accessible.

## Base URL

- **Development:** `http://127.0.0.1:5000/api`

## Rate Limiting

To ensure fair usage and prevent abuse, the Mastermind Game API enforces the following rate limits:

| Endpoint              | Limit                 |
| --------------------- | --------------------- |
| **Start Game**        | 5 requests per minute |
| **Overall API Usage** | 200 requests per day  |
| **Overall API Usage** | 50 requests per hour  |

### Rationale

- **Start Game Limit:** Prevents excessive game creation which could strain the backend and database.
- **Overall Limits:** Ensures balanced usage across all endpoints, maintaining performance and reliability.

## Error Codes

The API uses standard HTTP status codes to indicate the success or failure of requests.

| Code    | Description                                                          |
| ------- | -------------------------------------------------------------------- |
| **400** | Bad Request – The request was invalid or cannot be otherwise served. |
| **404** | Not Found – The requested resource could not be found.               |
| **429** | Too Many Requests – Rate limit exceeded.                             |
| **500** | Internal Server Error – An error occurred on the server.             |

## Endpoints

- [Start Game](/docs/api-design/start_game-endpoint) – Initialize a new game with a specified difficulty.
- [Make a Guess](/docs/api-design/make_guess-endpoint) – Submit a guess for the current game.
