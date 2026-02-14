# Distributed Sliding Window Rate Limiter

A high-performance rate limiting service built with **FastAPI**, **Redis**, and **Docker**. This project implements a **Sliding Window Log** algorithm to manage API traffic and prevent abuse across distributed systems.

## Why This Project?
Traditional "Fixed Window" rate limiters (like counting hits per minute) have a "reset" problem where a user can double their quota by spamming at the end of one window and the start of the next. 

This project uses a **Sliding Window** approach with Redis Sorted Sets to provide a perfectly smooth, fair limit.

## Tech Stack
- **Framework**: FastAPI (Asynchronous Python)
- **State Store**: Redis (Sorted Sets for timestamp tracking)
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3.11

## Getting Started

### Prerequisites
- Docker & Docker Compose installed on your machine.

### Installation & Run
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Anup-001/rate-limiter.git
   cd rate-limiter
   ```

2. **Launch with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   This will automatically pull the Redis image, build your Python app, and link them in a private network.

3. **Access the API**:
   The server will be live at http://localhost:8000.

## API Endpoints

### Sliding Window Rate Limiter
**Endpoint**: `GET /advanced`

**Limit**: 5 requests per 60-second sliding window.

**Logic**:
- `ZREMRANGEBYSCORE`: Removes timestamps older than 60 seconds.
- `ZADD`: Adds the current request timestamp with a unique UUID.
- `ZCARD`: Counts remaining valid requests to check against the limit.

**Success Response (200 OK)**:
```json
{
  "message": "Success",
  "current_count": 3
}
```

**Rate Limited Response (429 Too Many Requests)**:
```json
{
  "detail": "Rate Limit Exceeded (Sliding Window)"
}
```

## Project Structure
```
.
├── main.py              # FastAPI application logic
├── Dockerfile           # Container build instructions
├── docker-compose.yml   # Multi-container orchestration
├── requirements.txt     # Python dependencies
└── .gitignore           # Files excluded from version control
```
