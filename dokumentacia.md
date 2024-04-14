# Endpoints

## Register `/api/register/`
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

## Login `/api/login/`
Method: Post  
Written By: Viky  

Curl call:
```bash
curl --location 'http://localhost:8000/api/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "newemail@example.com",
    "password": "newpassword123"
}
```

Example body:
```json
{
    "email": "newemail@example.com",
    "password": "newpassword123"
}
```

Response 200 OK:
```json
{
    "token": "a05ae5b929658e5da58ff8de46abfdf714bee1d1"
}
```

Response 400 Bad request:
```json
{
    "non_field_errors": [
        "Incorrect email or password"
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

## Create Diary Entry `/api/entries/create/`

Method: Post  
Written by: Viky

Curl call:
```bash
curl --location 'http://localhost:8000/api/entries/create/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--data '{
    "date": "2024-04-09T20:37:35Z",
    "title": "My Diary Entry",
    "text": "Today was an amazing day...",
    "emotion": "H",
    "location": "My Location"
}
```

Example Body:
```json
{
    "date": "2024-04-09T20:37:35Z",
    "title": "My Diary Entry",
    "text": "Today was an amazing day...",
    "emotion": "H",
    "location": "My Location"
}
```
Location is not required

Response 201 Created:
```json
{
    "id": 4,
    "date": "2024-04-14T16:26:51.532901Z",
    "title": "My Diary Entry",
    "text": "Today was an amazing day...",
    "emotion": "H",
    "location": "My Location",
    "user": 1
}
```

Response 400 bad request:
```json
{
    "emotion": [
        "This field is required."
    ]
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Modify Diary Entry `/api/entries/<id>/modify/`

Method: Put, Patch  
Written By: Viky  

Curl call Patch:
```bash
curl --location --request PATCH 'http://localhost:8000/api/entries/1/modify/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "title": "Updated Title for PATCH"
}'
```

Curl call Put:
```bash
curl --location --request PUT 'http://localhost:8000/api/entries/1/modify/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "title": "Updated Title",
    "text": "Updated text of the diary entry.",
    "emotion": "H",
    "location": "Updated Location"
}'
```

Response 200 OK:
```json
{
    "id": 4,
    "date": "2024-04-14T16:26:51.532901Z",
    "title": "Updated Title",
    "text": "Updated text of the diary entry.",
    "emotion": "H",
    "location": "My Location",
    "user": 1
}
```

Response 404 Not Found:
```json
{
    "message": "DiaryEntry not found"
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

Response 400 Bad Request (Put):
```json
{
    "emotion": [
        "This field is required."
    ]
}
```

## Delete Diary Entry `/api/entries/<id>/delete/`

Method: Delete
Written By: Viky

Curl call:
```bash
curl --location --request DELETE 'http://localhost:8000/api/entries/4/delete/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json'
```

Response 204 No context:
```json

```

Response 404 Not Found:
```json
{
    "message": "DiaryEntry not found"
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Create Tag `/api/tags/create/`

Method: Post
Written By: Viky

Curl call:
```bash
curl --location 'http://localhost:8000/api/tags/create/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "tagname": "TagName2"
}
'
```

Response 201 Created:
```json
{
    "id": 3,
    "tagname": "TagName2"
}
```

Response 400 Bad request:
```json
{
    "tagname": [
        "This field is required."
    ]
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

Response 400 Bad request:
```json
{
    "error": "duplicate key value violates unique constraint \"moodlogapp_tag_user_id_tagname_618d0a9a_uniq\"\nDETAIL:  Key (user_id, tagname)=(1, TagName2) already exists.\n"
}
```






