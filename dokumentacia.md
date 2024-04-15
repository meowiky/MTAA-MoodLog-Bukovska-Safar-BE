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

## Add tag to diary entry `/api/entries/<id>/add_tag/`

Method: Post  
Written By: Viky

Curl call:

```bash
curl --location 'http://localhost:8000/api/entries/2/add_tag/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "tagname": "TagName2"
}'
```

Response 201 Created:
```json
{
    "diaryentry": 2,
    "tag": 2
}
```
Response 404 Not found:
```json
{
    "message": "Tag not found"
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Remove tag from diary entry `/api/entries/<entryid>/remove_tag/<tagid>/`

Method: Delete  
Written By: Viky

Curl call:
```bash
curl --location --request DELETE 'http://localhost:8000/api/entries/1/remove_tag/1/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json'
```

Response 204 No content:
```json
{
    "message": "Tag removed from entry"
}
```

response 404 Not found:
```json
{
    "message": "Tag not found"
}
```

Response 404 Not found:
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

## Send Friend request `/api/friend_requests/send/id/`

Method: Post  
Written By: Robert and Viky

Curl call:
```bash
curl --location --request POST 'http://localhost:8000/api/friend_requests/send/5/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json'
```

Response 201 Created:
```json
{
    "id": 5,
    "status": "PEN",
    "sender": 1,
    "user1": 1,
    "user2": 8
}
```

Response 400 Bad request:
```json
{
    "error": "Friend request already sent or connection exists."
}
```

Response 404 Not found:
```json
{
    "detail": "No User matches the given query."
}
```

response 400 Bad request:
```json
{
    "error": "You cannot send a friend request to yourself."
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Accept friend request `/api/friend_requests/accept/id/`

Method: Patch  
Written By: Robert and Viky


Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/friend_requests/accept/1/' \
--header 'Authorization: Token 014190002278d1985544999725adec3f9d3d4517' \
--header 'Content-Type: application/json'
```

Response 200 OK:
```json
{
    "status": "ACC"
}
```

Response 404 Not found:
```json
{
    "detail": "No Friendship matches the given query."
}
```

Response 403 forbidden:
```json
{
    "error": "You do not have permission to accept this friend request"
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Decline Friend request `/api/friend_requests/decline/id/`

Method: Patch  
Written By: Robert and Viky

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/friend_requests/decline/1/' \
--header 'Authorization: Token 014190002278d1985544999725adec3f9d3d4517' \
--header 'Content-Type: application/json'
```

Response 200 Ok:
```json
{
    "status": "DEC"
}
```

Response 404 not found:
```json
{
    "detail": "No Friendship matches the given query."
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Get all friends `/api/friends/`

Method: Get  
Written By: Robert and Viky

Curl call:
```bash
curl --location 'http://localhost:8000/api/friends/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json'
```

Response 200 ok:
```json
[
    {
        "name": "Test User2",
        "email": "tes2@example.com"
    },
    {
        "name": "Test User4",
        "email": "test4@example.com"
    },
    {
        "name": "Test User5",
        "email": "test5@example.com"
    }
]
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Change User name `/api/change_name/`

Method: Patch  
Written By: Viky

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/change_name/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "name": "New Name user1"
}'
```

Response 200 OK:
```json
{
    "message": "Name updated successfully."
}
```

Response 400 bad request:
```json
{
    "error": "Invalid request, name is required."
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Change User email `/api/change_email/`

Method: Patch  
Written By: Viky

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/change_email/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "blab@example.com"
}'
```

Response 200 OK:
```json
{
    "message": "Email updated successfully."
}
```

Response 400 Bad request:
```json
{
    "error": "This email is already in use."
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
    "error": "This email is already in use."
}
```

Response 400 bad request:
```json
{
    "error": "Invalid request, email is required."
}
```

## Change Password `/api/change_password/`

Method: Patch  
Written By: Viky

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/change_password/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json' \
--data '{
    "old_password": "newpassword123",
    "new_password": "newpassword1234"
}'
```

Response 200 ok:
```json
{
    "message": "Password updated successfully."
}
```

Response 400 bad request:
```json
{
    "error": "New password cannot be the same as the old password."
}
```

Response 400 bad request:
```json
{
    "error": "Old password is incorrect."
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Get all User tags `/api/tags/`

Method: Get
Written by: Viky

Curl Call:
```bash
curl --location 'http://localhost:8000/api/tags/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: application/json'
```

Response 200 ok:
```json
[
    {
        "id": 1,
        "tagname": "TagName"
    },
    {
        "id": 2,
        "tagname": "TagName2"
    }
]
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Get weekly emotion stats `/api/stats/emotions/weekly/`

Method: Get
Written by: Viky

Curl Call:
```bash
curl --location 'http://localhost:8000/api/stats/emotions/weekly/' \
--header 'Authorization: Token ca5a2dc59738f73dd3eacbe1a3142d6f514a2b39' \
--header 'Content-Type: application/json'
```

Response 200 ok:
```json
{
    "emotion_stats": [
        {
            "emotion": "A",
            "count": 1
        },
        {
            "emotion": "H",
            "count": 1
        },
        {
            "emotion": "N",
            "count": 1
        },
        {
            "emotion": "S",
            "count": 1
        },
        {
            "emotion": "VH",
            "count": 1
        }
    ],
    "number_of_days_with_entry": 5,
    "number_of_days": 7
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Get monthly emotion stats `/api/stats/emotions/monthly/`

Method: Get
Written by: Viky

Curl Call:
```bash
curl --location 'http://localhost:8000/api/stats/emotions/monthly/' \
--header 'Authorization: Token ca5a2dc59738f73dd3eacbe1a3142d6f514a2b39' \
--header 'Content-Type: application/json'
```

Response 200 ok:
```json
{
    "emotion_stats": [
        {
            "emotion": "A",
            "count": 2
        },
        {
            "emotion": "H",
            "count": 1
        },
        {
            "emotion": "N",
            "count": 1
        },
        {
            "emotion": "S",
            "count": 3
        },
        {
            "emotion": "VH",
            "count": 2
        }
    ],
    "number_of_days_with_entry": 9,
    "number_of_days": 30
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```


## Get yearly emotion stats `/api/stats/emotions/yearly/`

Method: Get
Written by: Viky

Curl Call:
```bash
curl --location 'http://localhost:8000/api/stats/emotions/yearly/' \
--header 'Authorization: Token ca5a2dc59738f73dd3eacbe1a3142d6f514a2b39' \
--header 'Content-Type: application/json'
```

Response 200 ok:
```json
{
    "emotion_stats": [
        {
            "emotion": "A",
            "count": 2
        },
        {
            "emotion": "H",
            "count": 1
        },
        {
            "emotion": "N",
            "count": 1
        },
        {
            "emotion": "S",
            "count": 3
        },
        {
            "emotion": "VH",
            "count": 2
        }
    ],
    "number_of_days_with_entry": 9,
    "number_of_days": 366
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Get all diary entries ordered `/api/entries/ordered/`

Method: Get
Written by: Viky

Curl Call:
```bash
curl --location 'http://localhost:8000/api/entries/ordered/' \
--header 'Authorization: Token ca5a2dc59738f73dd3eacbe1a3142d6f514a2b39' \
--header 'Content-Type: application/json'
```

Response 200 ok:
```json
[
    {
        "id": 17,
        "date": "2024-04-14T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "S",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 16,
        "date": "2024-04-13T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "A",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 15,
        "date": "2024-04-12T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "N",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 14,
        "date": "2024-04-11T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "H",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 13,
        "date": "2024-04-10T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "VH",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 21,
        "date": "2024-04-05T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "VH",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 20,
        "date": "2024-04-04T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "A",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 19,
        "date": "2024-04-03T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "S",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 18,
        "date": "2024-04-01T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "S",
        "location": "My Location",
        "user": 9
    }
]
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Add photo to entry `/api/entries/id/add_photo/`

Method: Post  
Written by: Viky

not working properly :((

Curl call:
```bash
curl --location 'http://localhost:8000/api/entries/1/add_photo/' \
--header 'Authorization: Token a05ae5b929658e5da58ff8de46abfdf714bee1d1' \
--header 'Content-Type: multipart/form-data' \
--form 'photo=@"/C:/Users/vikyb/Pictures/gosig-ratta.jpg"'
```

## Send a Message `/api/send_message/<id>/`

Method: Patch  
Written By: Robert

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/send_message/2/' \
--header 'Authorization: Token fa9b8410308e45b2ed0ba0f13aebcd495792cbf8' \
--header 'Content-Type: application/json'
```

Response 201 Created:
```json
{
  "id": 11,
  "text": "toto je sprava ktoru ti posielam",
  "sent_at": "2024-04-15T16:54:21.816618Z",
  "read_at": null,
  "sender": 1,
  "receiver": 2
}
```

Response 400 Bad Request
```json
{
  "text": [
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

## Get All Messages With a User `/api/get_messages/<id>/`

Method: Patch  
Written By: Robert

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/get_messages/2/' \
--header 'Authorization: Token fa9b8410308e45b2ed0ba0f13aebcd495792cbf8' \
--header 'Content-Type: application/json'
```

Response 200 Ok:
```json
[
  {
    "text": "cavko cavko",
    "sent_at": "2024-04-13T13:11:34.971819Z",
    "read_at": "2024-04-13T13:42:49.723997Z",
    "sender": 1,
    "receiver": 5
  },
  {
    "text": "ahoj",
    "sent_at": "2024-04-13T13:15:11.121171Z",
    "read_at": "2024-04-13T13:40:17.399384Z",
    "sender": 5,
    "receiver": 1
  },
  {
    "text": "ako?",
    "sent_at": "2024-04-13T13:41:42.194771Z",
    "read_at": "2024-04-13T13:42:49.723997Z",
    "sender": 1,
    "receiver": 5
  }
]
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Delete a Message `/api/delete_message/<id>/`

Method: Patch  
Written By: Robert

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/delete_message/11/' \
--header 'Authorization: Token fa9b8410308e45b2ed0ba0f13aebcd495792cbf8' \
--header 'Content-Type: application/json'
```

Response 204 Not Found:
```json
{
  "message": "Message deleted"
}
```

Response 404 Not Found
```json
{
  "message": "Message not found"
}
```

Response 401 Unauthorized:
```json
{
  "error": "You are not authorized to delete this message"
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Change Notifications `/api/change_notifications/`

Method: Patch  
Written By: Robert

Curl call:
```bash
curl --location --request PATCH 'http://localhost:8000/api/change_notifications/' \
--header 'Authorization: Token fa9b8410308e45b2ed0ba0f13aebcd495792cbf8' \
--header 'Content-Type: application/json'
```

Response 200 OK:
```json
{
  "notification": false
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Search with keyword `/api/entries/search/?keyword=jahoda`

Method: Get  
Written by: Viky

Curl call:
```bash
curl --location 'http://localhost:8000/api/entries/search/?keyword=jahoda' \
--header 'Authorization: Token ca5a2dc59738f73dd3eacbe1a3142d6f514a2b39' \
--header 'Content-Type: application/json'
```

Response 200 OK:
```json
[
    {
        "id": 16,
        "date": "2024-04-13T14:58:27.600700Z",
        "title": "mnam jahoda",
        "text": "Today was an amazing day...",
        "emotion": "A",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 20,
        "date": "2024-04-04T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "jahoda je super",
        "emotion": "A",
        "location": "My Location",
        "user": 9
    }
]
```

Response 400 bad request:
```json
{
    "message": "Keyword parameter is missing."
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Get all diary entries with tag `/api/entries/tagged/malina/`

Method: Get
Written by: Viky

Curl call:
```bash
curl --location 'http://localhost:8000/api/entries/tagged/malina/' \
--header 'Authorization: Token ca5a2dc59738f73dd3eacbe1a3142d6f514a2b39' \
--header 'Content-Type: application/json'
```

Response 200 ok:
```json
[
    {
        "id": 13,
        "date": "2024-04-10T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "VH",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 14,
        "date": "2024-04-11T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "H",
        "location": "My Location",
        "user": 9
    },
    {
        "id": 15,
        "date": "2024-04-12T14:58:27.600700Z",
        "title": "My Diary Entry",
        "text": "Today was an amazing day...",
        "emotion": "N",
        "location": "My Location",
        "user": 9
    }
]
```

Response 404 not found:
```json
{
    "detail": "No Tag matches the given query."
}
```

Response 401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```







