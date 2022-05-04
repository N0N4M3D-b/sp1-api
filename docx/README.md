# SW Project 1 Database API Usage

## User API
> /users

### Description
#### POST
1. Request
> {"app_id": str, "app_pw": str, "app_email": str}
2. Response
> 201 : insert user success
> 400 : invalid request argument
> 401 : already exist id

