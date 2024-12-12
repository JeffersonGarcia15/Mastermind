---
id: changelog
title: Changelog
sidebar_label: Changelog
---

# Changelog

This file documents the changes made to the Mastermind Game Documentation.

## [Unreleased]

- **Added:**
  - User authentication.
- **Improved:**
  - Clarity of integration tests on the Mastermind Game Docs.
  - Changed `GET` method for `start_game` to be a `POST`.
    - The `difficulty` is also sent via the `body` rather than as a param.
  - Added API versioning.
  - Upgraded to `v2` which comes with some changes.
    - `data` in each response can now be an object if a single item is being send.
    - When an error occurs `data` can be null.
- **Fixed:**
  - Broken link to `/architecture-design/architecture-design`.
  - Broken link to `/architecture-design/mastermind-design`.
  - Broken link to `/architecture-design/future-improvements`.

## [Older Versions]

- [Running tests on an isolated docker container with its own test database](/docs/changelog/2024-12-10.md)
- [Adding docker and database](/docs/changelog/2024-12-9.md)
- [Initial release](/docs/changelog/2024-12-8.md)
