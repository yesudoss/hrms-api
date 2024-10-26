#### To Login
```
endpoint: http://127.0.0.1:8000/auth/login
method: post
Body Input (as form)
username: admin@test.com
password: admin
```

#### To get jobs
```
endpoint: http://127.0.0.1:8000/jobs
method: get
Header
Authorization: Bearer JWTTOKEN
```

#### To post job
```
endpoint: http://127.0.0.1:8000/jobs
method: post
Header
Authorization: Bearer JWTTOKEN
Body Input as json
{
  "title": "Software Engineer 2",
  "description": "Develop and maintain applications."
}
```
