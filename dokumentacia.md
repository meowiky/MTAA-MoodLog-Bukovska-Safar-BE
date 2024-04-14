# Endpoints

### Register `/api/register/`
Method: POST  
Written by: Viky

Curl call:
```bash
curl --location 'http://localhost:8000/api/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "securepassword123"
}'
```

Example body:
```json
{
    "email": "test@example.com",
    "name": "Test User",
    "password": "securepassword123"
}
```

Response 201 Created:
```json
{
    "id": 6,
    "email": "test@example.com",
    "name": "Test User"
}
```

Reponse 400 Bad request:
```json
{
    "email": [
        "user with this email already exists."
    ]
}
```

Response 400 Bad request:
```json
{
    "password": [
        "This field is required."
    ]
}
```