# API Documentation — CampusFind REST API

## Base URL
```
http://localhost:8000
```

## Interactive Docs
| UI | URL |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI JSON | http://localhost:8000/openapi.json |

---

## Endpoints Summary

### Users `/api/users`

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| POST | `/api/users/register` | Register new student account | 201, 400, 409 |
| POST | `/api/users/verify/{user_id}` | Verify email address | 200, 404 |
| POST | `/api/users/login` | Login with email and password | 200, 401 |
| GET | `/api/users/` | Get all users | 200 |
| GET | `/api/users/{user_id}` | Get user by ID | 200, 404 |
| PUT | `/api/users/{user_id}` | Update profile | 200, 404 |
| DELETE | `/api/users/{user_id}` | Deactivate account | 200, 404 |

### Reports `/api/reports`

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| POST | `/api/reports/` | Submit lost or found report | 201, 400 |
| GET | `/api/reports/` | Get all reports | 200 |
| GET | `/api/reports/open/lost` | Get all open lost reports | 200 |
| GET | `/api/reports/open/found` | Get all open found reports | 200 |
| GET | `/api/reports/user/{user_id}` | Get reports by user | 200 |
| GET | `/api/reports/{report_id}` | Get report by ID | 200, 404 |
| PUT | `/api/reports/{report_id}` | Update report | 200, 400, 403, 404 |
| DELETE | `/api/reports/{report_id}` | Delete report | 200, 400, 403, 404 |

### Matches `/api/matches`

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| POST | `/api/matches/` | Create AI match record | 201, 400, 404 |
| GET | `/api/matches/` | Get all matches | 200 |
| GET | `/api/matches/pending` | Get pending matches for admin | 200 |
| GET | `/api/matches/{match_id}` | Get match by ID | 200, 404 |
| POST | `/api/matches/{match_id}/confirm` | Admin confirms match | 200, 400, 404 |
| POST | `/api/matches/{match_id}/dismiss` | Admin dismisses match | 200, 400, 404 |

---

## Example Requests

### Register a user
```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Iminathi Didiza","email":"iminathi@university.ac.za","password":"Password123!"}'
```

### Submit a lost report
```bash
curl -X POST http://localhost:8000/api/reports/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your-user-id",
    "report_type": "LOST",
    "item_name": "Black Nike Backpack",
    "category": "ACCESSORIES",
    "description": "Black Nike backpack with broken zip on left pocket and UCT keyring attached",
    "location": "Library Second Floor",
    "date_lost_or_found": "2026-03-10"
  }'
```

### Confirm a match (admin)
```bash
curl -X POST http://localhost:8000/api/matches/{match_id}/confirm \
  -H "Content-Type: application/json" \
  -d '{"admin_id": "admin-user-id"}'
```
