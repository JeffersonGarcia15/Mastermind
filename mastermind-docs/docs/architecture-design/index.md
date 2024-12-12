---
id: architecture-design
title: Architecture and Design Details
sidebar_label: Architecture and Design Details
---

# Architecture and Design Details

The Mastermind application follows a **Monolithic Architecture** at the moment. In the future, it might be transitioned to a **Microservice Architecture** to enhance scalability and maintainability.

## **Components:**

- **Game Service:**
  - Manages game logic, including game creation, guessing, user creation, and user authentication.
- **Database:**
  - Utilizes PostgreSQL for data persistence, ensuring data integrity and reliability.

## **Technology Stack:**

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Testing:** pytest, requests-mock

## **1. Data Flow**

**Description:**  
The Data Flow section outlines how data moves through the Mastermind application, from user interactions to data processing and storage. Understanding this flow is essential for maintaining system integrity and optimizing performance.

### **Data Sources:**

- **User Inputs:**
  - Users interact with the API by sending HTTP requests to endpoints such as `/api/game/start/medium` or `/api/game/guess`.
  - Inputs include parameters like `game_id`, `guess`, and user credentials (when authentication is implemented).

### **Processing:**

1. **Game Service:**

   - **Game Creation:**

     - Upon receiving a request to start a new game, the Game Service generates a unique `game_id` and initializes the game state.
     - If authentication is implemented, it associates the game with a specific user.

   - **Guess Handling:**

     - Processes user guesses by comparing them against the secret solution stored in the database.
     - Utilizes the `get_hint` function to determine the number of bulls and cows.
     - Updates game state and records the attempt.

   - **User Management:**
     - Manages user creation and authentication (planned feature).
     - Stores user credentials securely in the database.

## **Data Storage**

### **PostgreSQL Database**

The Mastermind application utilizes **PostgreSQL** for data persistence, ensuring data integrity and reliability. The database schema comprises the following primary tables:

- **Game Records:**
  - **Table:** `games`
  - **Description:** Stores details of each game, including `game_id`, `user_id`, `difficulty`, `created_at`, `solution`, and `fallback_used`.
  - **Indexes:**
    - `game_user_id_index` on `user_id` to optimize queries filtering by user.
- **User Data:**
  - **Table:** `users`
  - **Description:** Stores user information such as `id`, `username`, and `password`.
- **Attempt Records:**
  - **Table:** `attempts`
  - **Description:** Records each guess made in a game, including `id`, `game_id`, `guess`, `hints`, and `time`.
  - **Indexes:**
    - `attempt_game_id_index` on `game_id` to optimize queries related to specific games.
- **Match Records:**
  - **Table:** `match_records`
  - **Description:** Stores the outcome of each game, including `id`, `game_id`, `result`, `score`, and `time_taken`.
  - **Indexes:**
    - `match_record_score_index` on `score` to optimize high-score retrievals.

### **Database Schema Diagram**

Below is a visual representation of the PostgreSQL database schema for the Mastermind application:

![Database Schema Diagram](/img/dbdiagram.png)
[Database Schema](https://dbdiagram.io/d/Mastermind-Game-6759f3bc46c15ed47916c59b)

### **Response:**

- After processing, the Game Service sends a response back to the user:

  - **Success Responses:**

    - Contain relevant data such as `game_id`, current game state, and results of guesses.

  - **Error Responses:**
    - Provide descriptive error messages and appropriate HTTP status codes based on the nature of the error.

---

## **2. Scalability and Performance Considerations**

**Description:**  
Scalability and performance are critical for ensuring that the Mastermind application can handle increasing loads and deliver responses promptly. This section outlines the strategies employed to achieve scalability and maintain high performance.

### **Current Architecture:**

- **Monolithic Architecture:**
  - All components of the application (Game Service, User Management, etc.) are bundled into a single deployable unit.
  - Simplifies development and deployment but can become a bottleneck as the application grows.

### **Scalability Strategies:**

1. **Containerization with Docker:**

   - **Benefit:**

     - Enables consistent deployment across different environments.
     - Simplifies scaling by allowing multiple containers to run instances of the application.

   - **Implementation:**
     - Uses Docker Compose to manage services, making it easy to scale services horizontally by increasing the number of container instances.

2. **Database Optimization:**

   - **Indexes:**

     - Implements database indexes on fields like `game_id`, `score` and `user_id` to speed up query execution.

   - **Connection Pooling:**
     - Manages database connections efficiently to handle multiple simultaneous requests without overwhelming the database server.

3. **Potential Transition to Microservices:**

   - **Future Plans:**

     - Splitting the monolithic Game Service into smaller, independent microservices (e.g., Game Service, User Service).
     - Facilitates independent scaling of services based on demand.

   - **Benefits:**
     - Enhances fault isolation, as issues in one service do not directly impact others.
     - Improves maintainability by allowing teams to work on different services concurrently.

### **Performance Enhancements:**

1. **Efficient Code Practices:**
   - Writing optimized algorithms, especially within core functionalities like the `get_hint` function, to ensure rapid execution. Luckily, the current implementation of it, inspired by the leetcode question [Bulls and Cows](https://leetcode.com/problems/bulls-and-cows/description/), is already optimal at Time: O(n) and Space: O(1).
2. **Caching Mechanisms:**

   - **Planned Implementation:**

     - Introducing caching (e.g., using Redis) to store frequently accessed data and reduce database load.

   - **Benefit:**
     - Decreases response times for repeated requests, enhancing user experience.

---

## **3. Security Measures**

**Description:**  
Security is essential to protect user data and ensure the integrity of the Mastermind application. This section outlines the security practices integrated into the architecture, both currently implemented and planned for future development.

### **Current Security Measures:**

1. **Password Storage:**
   - **Hashing:**
     - User passwords are hashed using a secure algorithm (e.g., bcrypt) before being stored in the database.
     - Ensures that plaintext passwords are never stored, mitigating risks in case of database breaches.
2. **Input Validation:**

   - **Sanitization:**

     - All user inputs are validated and sanitized to prevent injection attacks (e.g., SQL injection, Cross-Site Scripting).

   - **Flask-WTF or Similar Libraries:**
     - Utilizes libraries to handle form data validation and secure input handling.

3. **Database Security:**

   - **Secure Connections:**

     - Ensures that connections to the PostgreSQL database use secure credentials.

   - **Role-Based Access Control:**
     - Assigns appropriate database roles and permissions, adding an admin panel for example, to restrict access based on the principle of least privilege.
