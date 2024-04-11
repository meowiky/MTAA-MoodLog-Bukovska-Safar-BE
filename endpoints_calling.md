```
curl --location 'http://localhost:8000/api/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "securepassword123"
}'
```

```
curl --location 'http://localhost:8000/api/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@example.com",
    "password": "securepassword123"
}
'
```

```
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
'
```

```
curl --location 'http://localhost:8000/api/tags/create/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "tagname": "TagName"
}
'
```

```
curl --location 'http://localhost:8000/api/entries/1/add_tag/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "tagname": "TagName"
}'
```

```
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

```
curl --location --request PATCH 'http://localhost:8000/api/entries/1/modify/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "title": "Updated Title for PATCH"
}'
```