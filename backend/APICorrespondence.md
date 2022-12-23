# zvms-backend 新旧API对应
**返回值"type"字段均为"SUCCESS"**

***

## 用户

### 旧

POST `/user/login`
params 
```javascript
{
    "id": int,
    "password": string,
    "version": string
}
```
return
```javascript
{
    "message": "登入成功",
    "userid": int,
    "username": string,
    "class": int,
    "classname": string,
    "permission": int,
    "token": string
}
```

### 新

POST `/users/login`

params
```javascript
{
    "id": int,
    "pwd": string
}
```
return
```javascript
{
    "message": "登录成功",
    "name": string,
    "clz": int,
    "auth": int,
    "token": string,
    "clzName": string
}
```
***

### 旧

POST `/user/logout`

return
```javascript
{
    "message": "登出成功"
}
```

### 新

POST `/users/logout`

return
```javascript
{
    "message": "登出成功"
}
```

***

### 旧

GET `/users/info`

(这个有什么意义吗)

return 
```javascript
{
    "message": "获取成功"
    "info": //token_data
}
```

POST `/users/getInfo/<int:userId>`

(为什么这玩意没有参数还要POST)

return
```javascript
{
    "message": "获取成功"
    "userName": string,
    "class": int,
    "permission": int
}
```

### 新

GET `/users/<int:id>`

return
```javascript
{
    "message": "获取成功"
    "name": string,
    "clz": int,
    "clzName": string,
    "auth": int,
}
```

***

### 旧

POST `/users/modPwd`

params
```javascript
{
    "oldPwd": string,
    "newPwd": string
}
```

return
```javascript
{
    "message": "修改成功",
}
```

### 新

POST `/users/mod-pwd`

params
```javascript
{
    "old": string,
    "new": string
}
```

return
```javascript
{
    "message": "修改成功"
}
```

***