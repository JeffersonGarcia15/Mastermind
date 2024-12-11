---
title: Start Game Endpoint
---

# Start Game

**Endpoint:** `/start/{difficulty}`

**Method:** `GET`

## Parameters

| Name       | Type   | Description                         | Required |
| ---------- | ------ | ----------------------------------- | -------- |
| difficulty | string | Difficulty level (`medium`, `hard`) | Yes      |

## Request Example

```http
GET /start/medium HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{}
```

## Example cURL Request

```bash
curl -X GET http://127.0.0.1:5000/api/game/start/medium
```

## Response Example

### Success Response

**Condition:** Starting a game with difficulty `medium` when `Random.org` API is available.

```json
{
  "data": [
    {
      "game_id": "f758e8f8-5d4e-48f2-9b1d-fafdd1ba4cd3",
      "length": 4,
      "is_sequence_locally_generated": false
    }
  ],
  "error": null
}
```

**Condition:** Starting a game with difficulty `hard` when `Random.org` API is not available.

```json
{
  "data": [
    {
      "game_id": "b5d5899b-5c54-4a44-b5be-0a62fb9450",
      "length": 6,
      "is_sequence_locally_generated": true
    }
  ],
  "error": null
}
```

## Description

Initializes a new game session with the specified difficulty level (`medium` or `hard`). Depending on the availability of the `Random.org` API, the game sequence is either fetched from the API or generated locally to ensure reliability. The response includes a unique `game_id`, the sequence `length`, and a flag indicating if the sequence was generated locally.

## Errors

The Start Game endpoint handles errors to maintain reliability:

| **Error Code** | **Description**                                                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **500**        | **Internal Server Error** – Occurs if the Random.org API fails. In this case, the game sequence is generated locally to allow the user to start the game without interruption. |
| **400**        | **Bad Request** – Returned if the `difficulty` parameter is missing or invalid.                                                                                                |
| **429**        | **Too Many Requests** – Returned if the rate limit is exceeded.                                                                                                                |

[← Back to API Overview](/docs/api-design/index.md)
