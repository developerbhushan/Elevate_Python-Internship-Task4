# Elevate_Python-Internship-Task4
Task 4 : Build a REST API with Flask


## Description
Simple Flask API demonstrating CRUD operations for user data. Stores users in-memory (list of dicts).

## Endpoints
- `GET /users` — list all users
- `GET /users/<id>` — get user by id
- `POST /users` — create user (`{ "name": "...", "email": "..." }`)
- `PUT /users/<id>` — update user (partial ok)
- `DELETE /users/<id>` — delete user

## Run
1. (Optional) Create virtual env and activate
2. Install:
```bash
pip install flask