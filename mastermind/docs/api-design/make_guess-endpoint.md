---
title: Make Guess Endpoint
---

# Make Guess

**Endpoint:** `/guess`

**Method:** `POST`

## Parameters

| Name    | Type        | Description                                         | Required |
| ------- | ----------- | --------------------------------------------------- | -------- |
| game_id | UUID string | The ID sent by the backend at the start of the game | Yes      |
| guess   | string      | The guess you think will lead to the right answer   | Yes      |

## Request Example

```http
POST /guess
Host: 127.0.0.1:5000
Content-Type: application/json

{
    "game_id": "f758e8f8-5d4e-48f2-9b1d-fafdd1ba4cd3",
    "guess": "0123"
}
```

## Example cURL Request

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"game_id":"f758e8f8-5d4e-48f2-9b1d-fafdd1ba4cd3","guess":"1234"}' \
  http://127.0.0.1:5000/api/game/guess

```

## Response Example

### Success Response: <i>The following responses are shown assuming the game being played is of medium difficulty.</i>

**Condition:** Making a guess with all correct numbers and positions.

```json
{
  "data": [
    {
      "attempts_left": 9,
      "correct_numbers_only": 4,
      "correct_positions": 0,
      "status": "win",
      "solution": "0123"
    }
  ],
  "error": null
}
```

**Condition:** Making a guess with half correct numbers in their positions and half correct numbers only.

```json
{
  "data": [
    {
      "attempts_left": 9,
      "correct_numbers_only": 2,
      "correct_positions": 2,
      "status": "ongoing"
    }
  ],
  "error": null
}
```

**Condition:** Making a guess with some correct numbers in their positions and some correct numbers only. <i>Note: While the length of the solution is 4, since only 2/4 numbers in the guess are present in the solution we only receive feedback for 2 out of those 4 numbers.</i>

```json
{
  "data": [
    {
      "attempts_left": 9,
      "correct_numbers_only": 1,
      "correct_positions": 1,
      "status": "ongoing"
    }
  ],
  "error": null
}
```

**Condition:** Making a guess where all the numbers are wrong.

```json
{
  "data": [
    {
      "attempts_left": 9,
      "correct_numbers_only": 0,
      "correct_positions": 0,
      "status": "ongoing"
    }
  ],
  "error": null
}
```

**Condition:** Not winning the game after 10 attempts.

```json
{
  "data": [
    {
      "attempts_left": 0,
      "correct_numbers_only": 1,
      "correct_positions": 2,
      "status": "lose",
      "solution": "5671"
    }
  ],
  "error": null
}
```

## Description

Makes a `guess`, given a `game_id`, with length 4 or 6 (`medium` or `hard`) depending on the difficulty.

## Errors

The Make Guess endpoint handles errors to maintain reliability:

| **Error Code** | **Description**                                                     | **Detailed Error Description**                                                              |
| -------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **400**        | Invalid request format.                                             | The request payload is malformed or missing required fields.                                |
| **400**        | This game has already ended.                                        | Attempts to make a guess in a game session that has already concluded.                      |
| **400**        | Guess must be a 4 or 6-digit string.                                | The guess provided does not match the required length based on the game's difficulty level. |
| **404**        | Game ID not found.                                                  | The provided `game_id` does not correspond to any active game session.                      |
| **500**        | Internal Server Error – An unexpected error occurred on the server. | An unforeseen error occurred, possibly related to database operations or internal logic.    |

### Response Example

```json
{
  "data": [],
  "error": "Game ID not found."
}
```

[← Back to API Overview](/docs/api-design/index.md)
