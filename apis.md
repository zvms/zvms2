# 镇海中学义工管理系统文档
## API
### 1. signup
#### 1.4 listSignup `/signup/list/<int:cls>`
列出一个班级的报名  
权限: Any  
请求方法: `GET`  
参数: `cls: number`  
返回值: `structs.SingleSignup[]`  
#### 1.5 auditSignup `/signup/<int:volId>/<int:stuId>/audit`
审核一个报名  
权限: Class | Teacher  
请求方法: `POST`  
参数: `volId: number,
    stuId: number`  
返回值: `any`  
#### 1.6 signup `/signup/<int:volId>`
报名一个义工  
权限: Any  
请求方法: `POST`  
参数: `
    volId: number,
    students: number[]
  `  
返回值: `any`  
#### 1.7 rollback `/signup/<int:volId>/<int:stuId>/rollback`
撤回一个报名  
权限: Any  
请求方法: `POST`  
参数: `volId: number,
    stuId: number`  
返回值: `any`  
### 2. volunteer
#### 2.4 searchVolunteers `/volunteer/search`
搜索义工  
权限: Any  
请求方法: `GET`  
参数: `
    holder?: number,
    student?: number,
    cls?: number,
    name?: string,
    status?: enums.VolStatus
  `  
返回值: `structs.SingleVolunteer[]`  
#### 2.5 getVolunteerInfo `/volunteer/<int:id>`
获取一个义工的详细信息  
权限: Any  
请求方法: `GET`  
参数: `id: number`  
返回值: `any`  
#### 2.6 createVolunteer `/volunteer/create`
创建一个义工  
权限: Any  
请求方法: `POST`  
参数: `
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number,
    classes: structs.ClassVol[]
  `  
返回值: `
    name: string,
    description: string,
    time: string,
    type: number,
    reward: number,
    joiners: structs.SingleUserWithoutAuth[],
    holder: number,
    holderName: string
  `  
#### 2.7 modifyVolunteer `/volunteer/<int:id>/modify`
修改义工  
权限: Any  
请求方法: `POST`  
参数: `
    id: number,
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number,
    classes: structs.ClassVol[]
  `  
返回值: `any`  
#### 2.8 deleteVolunteer `/volunteer/<int:id>/delete`
删除义工  
权限: Any  
请求方法: `POST`  
参数: `id: number`  
返回值: `any`  
#### 2.9 auditVolunteer `/volunteer/<int:id>/audit`
审核义工(班内)  
权限: Class | Teacher  
请求方法: `POST`  
参数: `id: number`  
返回值: `any`  
### 3. notice
#### 3.4 searchNotices `/notice/search`
搜索通知  
权限: Any  
请求方法: `GET`  
参数: `
    sender?: number,
    user?: number,
    cls?: number,
    school?: any
  `  
返回值: `structs.SingleNotice[]`  
#### 3.6 sendUserNotice `/notice/send/user`
发送用户通知  
权限: Manager | Teacher  
请求方法: `POST`  
参数: `
    title: string,
    content: string,
    deadtime: string,
    targets: number[]
  `  
返回值: `any`  
#### 3.7 sendClassNotice `/notice/send/class`
发送班级通知  
权限: Manager | Teacher  
请求方法: `POST`  
参数: `
    title: string,
    content: string,
    deadtime: string,
    targets: number[]
  `  
返回值: `any`  
#### 3.8 sendSchoolNotice `/notice/send/school`
发送学校通知  
权限: Manager | Teacher  
请求方法: `POST`  
参数: `
    title: string,
    content: string,
    deadtime: string
  `  
返回值: `any`  
#### 3.9 deleteNotice `/notice/<int:id>/delete`
删除一个通知  
权限: Manager | Teacher  
请求方法: `POST`  
参数: `id: number`  
返回值: `any`  
#### 3.10 modifyNotice `/notice/<int:id>/modify`
修改一个通知  
权限: Manager | Teacher  
请求方法: `POST`  
参数: `
    id: number,
    title: string,
    content: string,
    deadtime: string
  `  
返回值: `any`  
### 4. report
#### 4.3 report `/report`
发送反馈  
权限: Any  
请求方法: `POST`  
参数: `
    report: string
  `  
返回值: `any`  
### 5. class_
#### 5.4 listClasses `/class/list`
列出所有班级  
权限: Any  
请求方法: `GET`  
参数: `any`  
返回值: `structs.SingleClass[]`  
#### 5.5 getClassInfo `/class/<int:id>`
获取一个班级的详细详细  
权限: Any  
请求方法: `GET`  
参数: `id: number`  
返回值: `
    name: string,
    students: structs.SingleUser[],
    teachers: structs.SingleUser[]
  `  
#### 5.6 deleteClass `/class/<int:id>/delete`
删除一个班级  
权限: System  
请求方法: `POST`  
参数: `id: number`  
返回值: `any`  
#### 5.7 createClass `/class/create`
创建一个班级  
权限: System  
请求方法: `POST`  
参数: `
    name: string
  `  
返回值: `any`  
#### 5.8 modifyClass `/class/<int:id>/modify`
修改一个班级的名称  
权限: System  
请求方法: `POST`  
参数: `
    id: number,
    name: string
  `  
返回值: `any`  
### 6. user
#### 6.4 check `/user/check`
检查登录状态  
权限: Any  
请求方法: `GET`  
参数: `any`  
返回值: `any`  
#### 6.5 login `/user/login`
登录  
权限: None  
请求方法: `POST`  
参数: `
    id: number,
    pwd: string
  `  
返回值: `
    token: string
  `  
#### 6.6 logout `/user/logout`
登出  
权限: Any  
请求方法: `POST`  
参数: `any`  
返回值: `any`  
#### 6.7 searchUsers `/user/search`
搜索用户  
权限: Any  
请求方法: `GET`  
参数: `
    name?: string,
    cls?: number,
    auth?: number
  `  
返回值: `any`  
#### 6.8 getUserInfo `/user/<int:id>`
获取一个用户的详细详细信息  
权限: Any  
请求方法: `GET`  
参数: `id: number`  
返回值: `
    name: string,
    cls: number,
    auth: number,
    clsName: string
  `  
#### 6.9 getVolunteerTime `/user/<int:id>/time`
获取一个用户(学生)的义工分  
权限: Any  
请求方法: `GET`  
参数: `id: number`  
返回值: `
    inside: number,
    outside: number,
    large: number
  `  
#### 6.10 modifyPassword `/user/mod-pwd`
修改自己的密码  
权限: Any  
请求方法: `POST`  
参数: `
    old: string,
    neo: string
  `  
返回值: `any`  
#### 6.11 changeClass `/user/change-class`
修改自己(老师)的班级  
权限: Any  
请求方法: `POST`  
参数: `
    cls: number
  `  
返回值: `any`  
#### 6.12 createUser `/user/create`
创建用户  
权限: System  
请求方法: `POST`  
参数: `
    users: structs.OneUser[]
  `  
返回值: `any`  
#### 6.13 modifyUser `/user/<int:id>/modify`
修改用户信息  
权限: System  
请求方法: `POST`  
参数: `
    id: number,
    name: string,
    cls: number,
    auth: number
  `  
返回值: `any`  
#### 6.14 deleteUser `/user/<int:id>/delete`
删除用户  
权限: System  
请求方法: `POST`  
参数: `id: number`  
返回值: `any`  
### 7. thought
#### 7.7 searchThoughts `/thought/search`
搜索感想  
权限: Any  
请求方法: `GET`  
参数: `
    cls?: number,
    status?: enums.ThoughtStatus,
    student?: number,
    Volunteer?: number
  `  
返回值: `any`  
#### 7.8 getThoughtInfo `/thought/<int:volId>/<int:stuId>`
获取一个感想的详细信息  
权限: Any  
请求方法: `GET`  
参数: `volId: number,
    stuId: number`  
返回值: `any`  
#### 7.12 saveThought `/thought/<int:volId>/<int:stuId>/save`
保存感想草稿  
权限: Any  
请求方法: `POST`  
参数: `
    volId: number,
    stuId: number,
    thought: string,
    pictures: string[]
  `  
返回值: `any`  
#### 7.13 submitThought `/thought/<int:volId>/<int:stuId>/submit`
提交感想  
权限: Any  
请求方法: `POST`  
参数: `
    volId: number,
    stuId: number,
    thought: string,
    pictures: string[]
  `  
返回值: `any`  
#### 7.14 firstAudit `/thought/<int:volId>/<int:stuId>/audit/first`
初审感想(班内)  
权限: Class | Teacher  
请求方法: `POST`  
参数: `volId: number,
    stuId: number`  
返回值: `any`  
#### 7.15 finalAudit `/thought/<int:volId>/<int:stuId>/audit/final`
终审感想(义管会)  
权限: Auditor  
请求方法: `POST`  
参数: `volId: number,
    stuId: number`  
返回值: `any`  
#### 7.16 repulse `/thought/<int:volId>/<int:stuId>/repulse`
打回感想  
权限: Any  
请求方法: `POST`  
参数: `
    volId: number,
    stuId: number,
    reason: string
  `  
返回值: `any`  
