📘 Revision Optimizer — Backend System

A backend system that helps students decide what to revise next by prioritizing topics using revision history, difficulty, importance, and self-reported confidence.

Instead of reminders or task lists, this system focuses on decision-making:

“Given everything I’ve studied so far, what should I revise now — and why?”

🎯 Problem Statement

Students often:

revise topics randomly

focus too much on easy topics

forget difficult or high-weight topics

lack a clear revision strategy

Most tools track tasks, but do not prioritize learning.



💡 Solution Overview

This project models studying as a data-driven process.

It:

stores topics and revision history

tracks confidence after each revision

computes a priority score for each topic

returns a ranked revision queue with explainable reasons

The system is deterministic, transparent, and extensible.



🧠 Core Concepts
1. Topics

Each topic represents a unit of study and includes:

subject

difficulty (1–5)

importance (1–5)

Topics are user-scoped and isolated per account.

2. Revisions (Event-Based)

Each revision is stored as an event, not a counter:

topic

timestamp

confidence (1–5)

This allows:

historical analysis

flexible scoring

future extensions (analytics, trends)

3. Revision Priority Engine

For each topic, a priority score is computed using:

time since last revision

topic difficulty

topic importance

last recorded confidence

This produces:

a ranked revision queue

a human-readable explanation for each recommendation



🚀 Key Features

🔐 JWT-based authentication (HTTP Bearer)

👤 User-scoped data isolation

📚 Topic management (CRUD)

📝 Revision logging with confidence tracking

📊 Revision queue with explainable priority scores

📘 Syllabus parsing (raw text → structured topics)

⚡ Optimized database queries (no N+1 problem)



🏗️ System Architecture
Client
  ↓
FastAPI (API Layer)
  ↓
Domain Logic (Revision Engine)
  ↓
PostgreSQL (Async SQLAlchemy)


Authentication handled via reusable dependencies

Business logic separated from API handlers

Configuration isolated from application code



📌 API Highlights
Authentication

POST /auth/register

POST /auth/login

GET /me

Topics

POST /topics

GET /topics

POST /topics/bulk

Revisions

POST /revisions

Decision Engine

GET /revision-queue

Syllabus Parsing

POST /syllabus/parse



⚙️ Revision Queue Logic (Simplified)
priority_score =
    (days_since_last_revision × decay_weight)
  + (difficulty × difficulty_weight)
  + (importance × importance_weight)
  − (confidence × confidence_weight)


Higher score → higher revision priority.

Each response includes both:

the score

the reasoning behind it



🛠️ Tech Stack

Backend: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy (async)

Auth: JWT (python-jose)

Validation: Pydantic

Security: bcrypt (passlib)



🧩 Design Decisions

HTTP Bearer over OAuth2
Chosen for simplicity and clarity in a single-client system.

Event-based revisions
Enables richer analysis compared to counters.

Explainable logic over ML
Prioritization is transparent and deterministic.

Optimized queries
Core decision endpoint avoids N+1 queries.

🔮 Future Improvements

Frontend (web or mobile)

Notification system

Adaptive weighting based on exam proximity

Analytics on study patterns

Optional ML-based recommendations




👤 Author

Shivansh Goyal
Computer Science / IT Undergraduate
Focused on backend engineering and system design.
