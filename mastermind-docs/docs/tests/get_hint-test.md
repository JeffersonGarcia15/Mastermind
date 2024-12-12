---
id: get-hint-unit-tests
title: Unit Tests for get_hint Function
sidebar_label: Unit Tests
---

# Unit Tests for `get_hint` Function

Unit tests are essential for verifying the correctness of individual components within your application. This section details the unit test cases for the **`get_hint`** function, outlining their descriptions, inputs, and expected outputs.

## **1. Test Cases**

| **Test Case ID** | **Description**                               | **Input**                        | **Expected Output**                                      |
| ---------------- | --------------------------------------------- | -------------------------------- | -------------------------------------------------------- |
| **UT1**          | All digits correct and in correct position    | `secret: "1234", guess: "1234"`  | `[4, 0]`                                                 |
| **UT2**          | Some digits correct and in correct position   | `secret: "1234", guess: "1243"`  | `[2, 2]`                                                 |
| **UT3**          | No digits correct                             | `secret: "1234", guess: "5678"`  | `[0, 0]`                                                 |
| **UT4**          | Duplicate digits with all matching digits     | `secret: "1122", guess: "2211"`  | `[0, 4]`                                                 |
| **UT5**          | Some digits correct with duplicates in secret | `secret: "1123", guess: "0111"`  | `[1, 1]`                                                 |
| **UT6**          | All digits correct but shuffled               | `secret: "1234", guess: "4321"`  | `[0, 4]`                                                 |
| **UT7**          | Partial overlap with duplicates in guess      | `secret: "1212", guess: "1221"`  | `[2, 2]`                                                 |
| **UT8**          | Identical secret and guess with duplicates    | `secret: "1111", guess: "1111"`  | `[4, 0]`                                                 |
| **UT9**          | Guess has extra digits not in secret          | `secret: "1234", guess: "12345"` | `[4, 0]` _(Assuming only first 4 digits are considered)_ |
| **UT10**         | Secret has extra digits not in guess          | `secret: "12345", guess: "1234"` | `[4, 0]` _(Assuming only first 4 digits are considered)_ |
