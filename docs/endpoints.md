# General

## Deployment
The API can be found here: https://scrum-gang-job-applications.herokuapp.com/

## Headers
- `Content-Type`: `application/json`
- `Authorization`: `Bearer <auth_token>`

# Applications
## View
### `GET` to `/applications/user`
Returns applications by `USER ID`
#### Sample Response
```
[
    {
        "application_id": 71,
        "comment": "",
        "company": "345",
        "date": "2019-03-21 11:58:47.526299",
        "date_posted": "",
        "deadline": "",
        "is_inhouse_posting": false,
        "position": "345",
        "resume": "",
        "status": "asdasdasd",
        "url": "345",
        "user_id": "potato"
    }
]
```
### `GET` to `/applications/user/<application_type>`
Returns applications by `USER ID` and `APPLICATION TYPE` ("internal" or "external")
#### Sample Response
Same as the previous, just queried differently!

### `GET` to `/applications/job/<job_id>`
Returns applications by `JOB ID`
#### Sample Response
Same as the previous, just queried differently!

### `GET` to `/applications/<application_id>`
Returns applications by `APPLICATION ID`
#### Sample Response
Same as the previous, just queried differently!

## Update
### `PUT` to `/update/status`
#### Body
- `id`: Job application ID
- `new_status`: New status of the job application
#### Sample Response
```
[
    {
        "comment": "",
        "date": "2019-03-21 13:06:54.830240",
        "id": 73,
        "is_inhouse_posting": true,
        "resume": "asd",
        "status": "Got the job boii",
        "user_id": "potato"
    }
]
```

### `PUT` to `/update/comment`
#### Body
- `id`: Job application ID
- `new_comment`: New comment of the job application
#### Sample Response
```
[
    {
        "comment": "hyped to solve solutions.",
        "date": "2019-03-22 03:46:39.338004",
        "id": 2,
        "is_inhouse_posting": false,
        "resume": "",
        "status": "Applied",
        "user_id": "5c945a7f063dbc00179b0815"
    }
]
```
## Withdraw
## `DELETE` to `/withdraw`:
### Body
- `id`: Job application ID
### Sample Response
```
{
    "status": "success"
}
```
# Inhouse Applications
## Apply
### `POST` to `/apply/internal/`:
#### Body
- `job_id`: ID of the job the user is applying to
- `resume`: Handy tool for applying to jobs
- `comment`: Comment associated with your application
#### Sample Response
This returns all applications, regardless of internal or external.
```
[
    {
        "comment": "",
        "date": "2019-03-21 13:06:54.830240",
        "id": 73,
        "is_inhouse_posting": true,
        "resume": "asd",
        "status": "Applied",
        "user_id": "potato"
    }
]
```

# External Applications
## Apply
### `POST` to `/apply/external`
#### Body
- `url`: URL of the external posting
- `position`: Job position of the external posting
- `comment`: Comment related to the tracked application
- `company`: Company where job takes place
- `resume`: Handy tool for applying to jobs
- `date_posted`: When the application was posted
- `deadline`: Deadline to apply for the job

#### Sample Response
```
[
    {
        "comment": "",
        "date": "2019-03-21 23:10:15.739623",
        "id": 36,
        "is_inhouse_posting": false,
        "resume": "",
        "status": "Applied",
        "user_id": "5c944a1c063dbc00179b0813"
    }
]
```

# Interview Questions
## Create
### `POST` to `/interview/question`:
#### Body
- `application_id`: ID of the application to which the question maps to
- `question`: Interview question
- `title`: Title for the question
#### Sample Response
```
[
    {
        "application_id": 71,
        "id": 17,
        "question": "asdasd",
        "title": "asdasd"
    }
]
```
## Update
### `PUT` to `/update/question`:
#### Body
- `id`: Question ID
- `new_question`: New question for that interview
#### Sample Response
```
{
    "application_id": 71,
    "id": 17,
    "question": "bobbobobo",
    "title": "asdasd"
}
```
## View
### `GET` to `/interview/question/<application_id>`
#### Sample Response
```
[
    {
        "application_id": 71,
        "id": 17,
        "question": "bobbobobo",
        "title": "asdasd"
    }
]
```
