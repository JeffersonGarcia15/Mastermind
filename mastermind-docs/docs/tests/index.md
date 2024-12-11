---
id: testing
title: Testing Overview
sidebar_label: Testing
---

# Testing Overview

Ensuring the reliability and correctness of the **Mastermind** application is essential. This document outlines the testing strategy, test cases, environment setup, and necessary CLI commands to effectively run and maintain the test suite.

**<i>Disclaimer: The testing docs are part of the `public` docs mainly to have all the docs in one place. Ideally, this should have been part of the internal docs.</i>**

## **Test Environment Setup**

To ensure that tests run consistently across different environments, follow the steps below to set up the testing environment using Docker Compose:

### **Prerequisites**

- **Docker & Docker Compose:** Ensure that both Docker and Docker Compose are installed on your machine.

### **Setup Steps**

1. **Create a `.env.test` File:**

   - Duplicate the `.env.example` file and rename it to `.env.test`.
   - Update the environment variables as needed for the testing environment.

   ```bash
   cp .env.example .env.test
   ```

2. ## **Start the Test Environment:**

   ```bash
   docker-compose -f docker-compose-test.yml up -d
   ```

3. ## **Initialize the Database:**

   ```bash
   docker-compose -f docker-compose-test.yml exec test_app flask db init
   docker-compose -f docker-compose-test.yml exec test_app flask create-db
   docker-compose -f docker-compose-test.yml exec test_app flask create-indexes
   ```

4. ## **Apply Database Migrations:**

   ```bash
   docker-compose -f docker-compose-test.yml exec test_app flask db migrate -m "Initial migration"
   docker-compose -f docker-compose-test.yml exec test_app flask db upgrade
   ```

5. ## **Run the Tests:**
   ```bash
   docker-compose -f docker-compose-test.yml exec test_app pytest tests -s
   ```
