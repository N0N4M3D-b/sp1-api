# SW Project 1 Database API Usage

> Global Response
>> 400 : invaild request argument

## User API
> /users

### Description
#### POST
> 1. Request
>> {"app_id": str, "app_pw": str, "app_email": str}
> 2. Response
>> 201 : insert user success  
>> 401 : already exist id  

#### DELETE
> 1. Request
>> {"app_id": str, "app_pw": str}
> 2. Response
>> 200 : delete user success  
>> 401 : delete user fail

#### PUT
> 1. Request
>> {"app_id": str, "app_pw": str, "app_email": str}
> 2. Response
>> 200 : modify user info success  
>> 400 : modify user info fail

## Login API
> /login

### Description
#### POST
> 1. Request
>> {"app_id": str, "app_pw": str}
> 2. Response
>> 200 : auth success  
>> 404 : auth fail
