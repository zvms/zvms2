# 镇海中学义工管理系统API文档

## 1.zvms.views.user

### **...**

#### 1.1 login

[POST] /user/login  
**登录**  

参数:
```json
{
    "id": "int",
    "pwd": "string"
}
```
返回:
```json
{
    "id": "int",
    "token": "string"
}
```

#### 1.2 logout

[POST] /user/logout  
**登出**  

参数:
```json
"any"
```
返回:
```json
"any"
```

#### 1.3 search-users

[GET] /user/search  
**搜索用户**  

参数:
```json
{
    "name": "string",
    "cls": "int",
    "auth": "int"
}
```
返回:
```json
{
    "id": "int",
    "name": "string"
}
```

#### 1.4 get-user-info

[GET] /user/<int:id>  
**获取用户详细信息**  

参数:
```json
"any"
```
返回:
```json
{
    "name": "string",
    "auth": "int",
    "cls": "int",
    "clsName": "string"
}
```

#### 1.5 get-student-scores

[GET] /user/<int:id>/scores  
**获取一个学生的义工分**  

参数:
```json
"any"
```
返回:
```json
{
    "inside": "int",
    "outside": "int",
    "large": "int"
}
```

#### 1.6 modify-password

[POST] /user/<int:id>/mod-pwd  
**修改某人的密码**  

参数:
```json
{
    "oldPwd": "string",
    "newPwd": "string"
}
```
返回:
```json
"any"
```
## 2.zvms.views.class

### **...**

#### 2.1 list-classes

[GET] /class/list  
**列出所有班级**  

参数:
```json
"any"
```
返回:
```json
[
    {
        "id": "int",
        "name": "string"
    }
]
```

#### 2.2 get-class-info

[GET] /class/<int:id>  
**获取班级详细信息**  

参数:
```json
"any"
```
返回:
```json
{
    "name": "string",
    "students": [
        {
            "auth": "int",
            "id": "int",
            "name": "string"
        }
    ],
    "teachers": [
        {
            "auth": "int",
            "id": "int",
            "name": "string"
        }
    ]
}
```
## 3.zvms.views.issue

### **...**

#### 3.1 send-issue

[POST] /issue/send  
**发送反馈**  

参数:
```json
{
    "content": "string"
}
```
返回:
```json
"any"
```

#### 3.2 fetch-issues

[GET] /issue/fetch  
**获取反馈**  

参数:
```json
"any"
```
返回:
```json
[
    {
        "content": "string",
        "reporter": "int",
        "reporterName": "string",
        "time": "string"
    }
]
```
## 4.zvms.views.notice

### **...**

#### 4.1 search-notices

[GET] /notice/search  
**搜索通知**  

参数:
```json
{
    "sender": "int",
    "receiver": "int",
    "cls": "int",
    "school": "any"
}
```
返回:
```json
[
    {
        "id": "int",
        "title": "string",
        "content": "string",
        "sender": "int",
        "senderName": "string",
        "sendtime": "string",
        "deadtime": "string"
    }
]
```

#### 4.2 send-user-notice

[POST] /notice/send/user  
**发送用户通知**  

参数:
```json
{
    "title": "string",
    "content": "string",
    "time": "datetime",
    "targets": [
        "int"
    ]
}
```
返回:
```json
"any"
```

#### 4.3 send-class-notice

[POST] /notice/send/class  
**...**  

参数:
```json
{
    "title": "string",
    "content": "string",
    "deadtime": "datetime",
    "targets": [
        "int"
    ]
}
```
返回:
```json
"any"
```

#### 4.4 send-school-notice

[POST] /notice/send/school  
**...**  

参数:
```json
{
    "title": "string",
    "content": "string",
    "deadtime": "datetime",
    "anonymous": "boolean"
}
```
返回:
```json
"any"
```

#### 4.5 get-main-menu-notice

[GET] /notice/mainmenu  
**...**  

参数:
```json
"any"
```
返回:
```json
{
    "title": "string",
    "content": "string"
}
```
## 5.zvms.views.system

### **...**

#### 5.1 restart-ttyd

[POST] /system/ttyd/restart  
**...**  

参数:
```json
"any"
```
返回:
```json
"any"
```

#### 5.2 restart-backend

[POST] /system/restart  
**...**  

参数:
```json
"any"
```
返回:
```json
"any"
```
