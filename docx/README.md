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

## OTT Group API
> /otts/group

### Description
#### POST
> 1. Request
>> {"app_id": str, "ott_id": str, "ott_pw": str, "ott": str}
> 2. Response
>> 200 : joined in group  
>> 400 : invalid ott service  
>> 401 : already joined in group  

#### DELETE
> 1. Request
>> {"app_id": str, "idx": int}
> 2. Response
>> 200 : exit group successfully  
>> 404 : invalid index

## OTT User Info API
> /otts/info/<int:idx>

### Description
#### GET
> 1. Request
>> None
> 2. Response
>> 200 : get info success
```json
{
    "idx": int,
    "ott": str,
    "account": {
        "id": str,
        "pw": str,
        "payment": {
            "type": int,
            "detail": str,
            "next": datetime
        },
        "membership": {
            "type": int,
            "cost": int
        }
    },
    "updatetime": datetime,
    "members": [[app_id(str), isAdmin(int(0||1))], [app_id, isAdmin], ...]
}
```
>> 404 : invalid index

#### PUT
> 1. Request
>> {"ott_pw": str, "payment_type": int, "payment_next": int, "membership_type": int, "membership_cost": int}  
>> {"ott_pw": str, "payment_type": int, "payment_detail": str, "payment_next": int, "membership_type": int, "membership_cost": int}

payment_detail이 NULL일 경우 포함하지 않고 요청

> 2. Response
>> 200 : update account info success  
>> 404 : invalid index
