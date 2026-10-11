# web-portal-template

## Description
A secured api/frontend for the AQL platform. 

---

## To run

### Start services
```bash
docker compose up --build
```

### View frontend
[localhost](https://localhost)

### Health check
```bash
curl -ikL localhost/health
```

### Call API
```bash
curl -ikL localhost/api/data
```

### Run playwrite tests
```bash
docker compose --profile test up
```

### Stop services
```bash
docker compose down
```

### Cleanup docker
```bash
docker volume prune && docker system prune
```
---

## Services

### Caddy
Reverse proxy with additional rate limit plugin. Manages self-signed ssl certificates.

### FastAPI
A python based api only gateway protected by docker secrets file. Being python based, can use `subprocess` function to make external calls to AQL platform applications.

### Frontend
A React simple page that displays api data.

### Node
A nodejs express BFF (backend for frontend) gateway protected by docker secrets file.

### Playwrite
Tests browser and api.

---

## Creating docker secrets
```bash
openssl rand -hex 32
```

---

## System Flow

```text
                         ┌──────────────┐
                         │    Caddy     │
                         └──────┬───────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
              Django Portal          Active Application
                    │                       │
                    │                       │
                    ▼                      BFF
             Service Manager               │
                    │                     FastAPI
                    │                       │
                    ▼                    subprocess
              Host Agent
                    │
                    ▼
                  Docker
             ┌──────┼──────┐
             ▼      ▼      ▼
            A       B      C
           OFF     ON     OFF
```