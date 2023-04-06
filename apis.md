# 镇海中学义工管理系统API文档
## 1.zvms.views.user
### **...**

#### 1.1 check
[GET] /user/check  
**检查登录状态**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```

#### 1.2 login
[POST] /user/login  
**登录**  
参数: 
```json
{
    "id": "number",
    "pwd": "string"
}
```
响应:  
```json
{
    "token": "string"
}
```

#### 1.3 logout
[POST] /user/logout  
**登出**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```

#### 1.4 searchUsers
[GET] /user/search  
**搜索用户**  
参数: 
```json
{
    "name": "string",
    "cls": "number",
    "auth": "number"
}
```
响应:  
```json
"any"
```

#### 1.5 getUserInfo
[GET] /user/<int:id>  
**获取一个用户的详细详细信息**  
参数: 
```json
"any"
```
响应:  
```json
{
    "name": "string",
    "cls": "number",
    "auth": "number",
    "clsName": "string"
}
```

#### 1.6 getStudentStat
[GET] /user/<int:id>/time  
**获取一个用户(学生)的义工分**  
参数: 
```json
"any"
```
响应:  
```json
{
    "inside": "number",
    "outside": "number",
    "large": "number"
}
```

#### 1.7 modifyPassword
[POST] /user/mod-pwd  
**修改自己的密码**  
参数: 
```json
{
    "old": "string",
    "neo": "string"
}
```
响应:  
```json
"any"
```

#### 1.8 createUser
[POST] /user/create  
**创建用户**  
参数: 
```json
{
    "users": [
        {
            "id": "number",
            "name": "string",
            "cls": "number",
            "auth": "number"
        }
    ]
}
```
响应:  
```json
"any"
```

#### 1.9 modifyUser
[POST] /user/<int:id>/modify  
**修改用户信息**  
参数: 
```json
{
    "name": "string",
    "cls": "number",
    "auth": "number"
}
```
响应:  
```json
"any"
```

#### 1.10 deleteUser
[POST] /user/<int:id>/delete  
**删除用户**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```


---

## 2.zvms.views.report
### **...**

#### 2.1 report
[POST] /report  
**发送反馈**  
参数: 
```json
{
    "report": "string"
}
```
响应:  
```json
"any"
```


---

## 3.zvms.views.notice
### **...**

#### 3.1 searchNotices
[GET] /notice/search  
**搜索通知**  
参数: 
```json
{
    "sender": "number",
    "user": "number",
    "cls": "number",
    "school": "number"
}
```
响应:  
```json
[
    {
        "id": "number",
        "title": "string",
        "content": "string",
        "sender": "number",
        "deadtime": "string",
        "senderName": "string"
    }
]
```

#### 3.2 sendUserNotice
[POST] /notice/send/user  
**发送用户通知**  
参数: 
```json
{
    "targets": [
        "number"
    ],
    "title": "string",
    "content": "string",
    "deadtime": "string"
}
```
响应:  
```json
"any"
```

#### 3.3 sendClassNotice
[POST] /notice/send/class  
**发送班级通知**  
参数: 
```json
{
    "targets": [
        "number"
    ],
    "title": "string",
    "content": "string",
    "deadtime": "string"
}
```
响应:  
```json
"any"
```

#### 3.4 sendSchoolNotice
[POST] /notice/send/school  
**发送学校通知**  
参数: 
```json
{
    "title": "string",
    "content": "string",
    "deadtime": "string"
}
```
响应:  
```json
"any"
```

#### 3.5 deleteNotice
[POST] /notice/<int:id>/delete  
**删除一个通知**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```

#### 3.6 modifyNotice
[POST] /notice/<int:id>/modify  
**修改一个通知**  
参数: 
```json
{
    "title": "string",
    "content": "string",
    "deadtime": "string"
}
```
响应:  
```json
"any"
```


---

## 4.zvms.views.signup
### **...**

#### 4.1 listSignup
[GET] /signup/list/<int:cls>  
**列出一个班级的报名**  
参数: 
```json
"any"
```
响应:  
```json
[
    {
        "volId": "number",
        "volName": "string",
        "stuId": "number",
        "stuName": "string"
    }
]
```

#### 4.2 auditSignup
[POST] /signup/<int:volId>/<int:stuId>/audit  
**审核一个报名**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```

#### 4.3 signup
[POST] /signup/<int:volId>  
**报名一个义工**  
参数: 
```json
{
    "students": [
        "number"
    ]
}
```
响应:  
```json
"any"
```

#### 4.4 rollback
[POST] /signup/<int:volId>/<int:stuId>/rollback  
**撤回一个报名**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```


---

## 5.zvms.views.volunteer
### **...**

#### 5.1 searchVolunteers
[GET] /volunteer/search  
**搜索义工**  
参数: 
```json
{
    "holder": "number",
    "student": "number",
    "cls": "number",
    "name": "string",
    "status": "VolStatus",
    "signable": "boolean"
}
```
响应:  
```json
[
    {
        "id": "number",
        "name": "string",
        "time": "string",
        "status": "number",
        "signable": "boolean",
        "joiners": [
            {
                "id": "number",
                "name": "string"
            }
        ],
        "holder": "number",
        "holderName": "string"
    }
]
```

#### 5.2 getVolunteerInfo
[GET] /volunteer/<int:id>  
**获取一个义工的详细信息**  
参数: 
```json
"any"
```
响应:  
```json
{
    "name": "string",
    "description": "string",
    "time": "string",
    "status": "VolStatus",
    "type": "VolType",
    "reward": "number",
    "signable": "boolean",
    "joiners": [
        {
            "id": "number",
            "name": "string"
        }
    ],
    "holder": "number",
    "holderName": "string"
}
```

#### 5.3 createVolunteer
[POST] /volunteer/create  
**创建一个义工**  
参数: 
```json
{
    "classes": [
        {
            "id": "number",
            "max": "number"
        }
    ],
    "name": "string",
    "description": "string",
    "time": "string",
    "type": "VolType",
    "reward": "number"
}
```
响应:  
```json
"any"
```

#### 5.4 createAppointedVolunteer
[POST] /volunteer/create/appointed  
**创建一个成员全部指定的义工**  
参数: 
```json
{
    "joiners": [
        "number"
    ],
    "name": "string",
    "description": "string",
    "time": "string",
    "type": "VolType",
    "reward": "number"
}
```
响应:  
```json
"any"
```

#### 5.5 modifyVolunteer
[POST] /volunteer/<int:id>/modify  
**修改义工**  
参数: 
```json
{
    "classes": [
        {
            "id": "number",
            "max": "number"
        }
    ],
    "name": "string",
    "description": "string",
    "time": "string",
    "type": "VolType",
    "reward": "number"
}
```
响应:  
```json
"any"
```

#### 5.6 deleteVolunteer
[POST] /volunteer/<int:id>/delete  
**删除义工**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```

#### 5.7 auditVolunteer
[POST] /volunteer/<int:id>/audit  
**审核义工(班内)**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```


---

## 6.zvms.views.thought
### **...**

#### 6.1 getStudentThoughts
[GET] /thought/student/<int:id>  
**获取某个学生的感想**  
参数: 
```json
"any"
```
响应:  
```json
{
    "accepted": [
        {
            "status": "ThoughtStatus",
            "reason": "string",
            "thought": "string",
            "reward": "number",
            "pics": [
                {
                    "hash": "string",
                    "type": "string"
                }
            ]
        }
    ],
    "unsubmitted": [
        {
            "status": "ThoughtStatus",
            "reason": "string",
            "thought": "string",
            "reward": "number",
            "pics": [
                {
                    "hash": "string",
                    "type": "string"
                }
            ]
        }
    ],
    "draft": [
        {
            "status": "ThoughtStatus",
            "reason": "string",
            "thought": "string",
            "reward": "number",
            "pics": [
                {
                    "hash": "string",
                    "type": "string"
                }
            ]
        }
    ],
    "unaudited": [
        {
            "status": "ThoughtStatus",
            "reason": "string",
            "thought": "string",
            "reward": "number",
            "pics": [
                {
                    "hash": "string",
                    "type": "string"
                }
            ]
        }
    ]
}
```

#### 6.2 searchThoughts
[GET] /thought/search  
**搜索感想**  
参数: 
```json
{
    "cls": "number",
    "status": "ThoughtStatus",
    "student": "number",
    "volunteer": "number"
}
```
响应:  
```json
[
    {
        "volId": "number",
        "stuId": "number",
        "status": "ThoughtStatus",
        "stuName": "string",
        "volName": "string"
    }
]
```

#### 6.3 getThoughtInfo
[GET] /thought/<int:volId>/<int:stuId>  
**获取一个感想的详细信息**  
参数: 
```json
"any"
```
响应:  
```json
{
    "status": "ThoughtStatus",
    "reason": "string",
    "thought": "string",
    "reward": "number",
    "pics": [
        {
            "hash": "string",
            "type": "string"
        }
    ]
}
```

#### 6.4 saveThought
[POST] /thought/<int:volId>/<int:stuId>/save  
**保存感想草稿**  
参数: 
```json
{
    "thought": "string",
    "pictures": [
        {
            "base64": "string",
            "type": "string"
        }
    ]
}
```
响应:  
```json
"any"
```

#### 6.5 submitThought
[POST] /thought/<int:volId>/<int:stuId>/submit  
**提交感想**  
参数: 
```json
{
    "thought": "string",
    "pictures": [
        {
            "base64": "string",
            "type": "string"
        }
    ]
}
```
响应:  
```json
"any"
```

#### 6.6 firstAudit
[POST] /thought/<int:volId>/<int:stuId>/audit/first  
**初审感想(班内)**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```

#### 6.7 finalAudit
[POST] /thought/<int:volId>/<int:stuId>/audit/final  
**终审感想(义管会)**  
参数: 
```json
{
    "reward": "number"
}
```
响应:  
```json
"any"
```

#### 6.8 repulse
[POST] /thought/<int:volId>/<int:stuId>/repulse  
**打回感想**  
参数: 
```json
{
    "reason": "string"
}
```
响应:  
```json
"any"
```


---

## 7.zvms.views.class_
### **...**

#### 7.1 listClasses
[GET] /class/list  
**列出所有班级**  
参数: 
```json
"any"
```
响应:  
```json
[
    {
        "id": "number",
        "name": "string"
    }
]
```

#### 7.2 getClassInfo
[GET] /class/<int:id>  
**获取一个班级的详细信息**  
参数: 
```json
"any"
```
响应:  
```json
{
    "name": "string",
    "students": [
        {
            "auth": "number",
            "id": "number",
            "name": "string"
        }
    ],
    "teachers": [
        {
            "auth": "number",
            "id": "number",
            "name": "string"
        }
    ]
}
```

#### 7.3 deleteClass
[POST] /class/<int:id>/delete  
**删除一个班级**  
参数: 
```json
"any"
```
响应:  
```json
"any"
```

#### 7.4 createClass
[POST] /class/create  
**创建一个班级**  
参数: 
```json
{
    "name": "string"
}
```
响应:  
```json
"any"
```

#### 7.5 modifyClass
[POST] /class/<int:id>/modify  
**修改一个班级的名称**  
参数: 
```json
{
    "name": "string"
}
```
响应:  
```json
"any"
```


---


