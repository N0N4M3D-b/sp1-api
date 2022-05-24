# SW Project 1 Database API Usage

> Global Response
>> 400 : invaild request argument

## User API
> /users

### Description
#### POST
APP 유저 계정 추가
> 1. Request
>> {"app_id": str, "app_pw": str, "app_email": str}
> 2. Response
>> 201 : insert user success  
>> 401 : already exist id  

#### DELETE
APP 유저 계정 삭제
> 1. Request
>> {"app_id": str, "app_pw": str}
> 2. Response
>> 200 : delete user success  
>> 401 : delete user fail

#### PUT
APP 유저 계정 정보 변경
> 1. Request
>> {"app_id": str, "app_pw": str, "app_email": str}
> 2. Response
>> 200 : modify user info success  
>> 400 : modify user info fail

## Login API
> /login

### Description
#### POST
APP 유저 로그인 체크
> 1. Request
>> {"app_id": str, "app_pw": str}
> 2. Response
>> 200 : auth success  
>> 404 : auth fail

## OTT Group API
> /otts/group

### Description
#### POST
그룹 생성  
만약 이미 동일한 OTT 서비스의 ott id를 사용하는 그룹이 존재하면 그 그룹의 멤버로 그룹 가입
> 1. Request
>> {"app_id": str, "ott_id": str, "ott_pw": str, "ott": str}
> 2. Response
>> 200 : joined in group  
>> 400 : invalid ott service  
>> 401 : already joined in group  

#### DELETE
그룹 탈퇴  
만약 그룹 어드민이 탈퇴하는 경우 해당 그룹 삭제
> 1. Request
>> {"app_id": str, "idx": int}
> 2. Response
>> 200 : exit group successfully  
>> 404 : invalid index

## OTT Group Info API
> /otts/info/<int:idx>

### Description
#### GET
그룹이 사용하는 OTT 계정 정보 가져오기 
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
그룹이 사용하는 OTT 계정 정보 수정
> 1. Request
>> {"ott_pw": str, "payment_type": int, "payment_next": int, "membership_type": int, "membership_cost": int}  
>> {"ott_pw": str, "payment_type": int, "payment_detail": str, "payment_next": int, "membership_type": int, "membership_cost": int}

payment_detail이 NULL일 경우 포함하지 않고 요청

> 2. Response
>> 200 : update account info success  
>> 404 : invalid index
