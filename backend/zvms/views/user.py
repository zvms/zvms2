
import typing

 

UserLoginResponse = TypedDict('UserLoginResponse',
            {
                "username": str,
"classId": int,
"permission": str,
"token": str
            }
        )
        
def postUserLogin(userid: int,
password: str,
version: str) -> UserLoginResponse : '''
## POST user/login
# 登陆

'''


UserLogoutResponse = TypedDict('UserLogoutResponse',
            {
                
            }
        )
        
def getUserLogout() -> UserLogoutResponse : '''
## GET user/logout
# 登出

''' 



UserInfoResponse = TypedDict('UserInfoResponse',
            {
                "username": str,
"classId": int,
"permission": str
            }
        )
        
def getUserInfo() -> UserInfoResponse : '''
## GET user/info
# 查看当前登陆账号的信息

''' 



UserGetInfoByUserIdResponse = TypedDict('UserGetInfoByUserIdResponse',
            {
                "username": str,
"classId": int,
"permission": str
            }
        )
        
def getUserGetInfoByUserId() -> UserGetInfoByUserIdResponse : '''
## GET user/getInfo/<userId>
# 查看账号信息

''' 


 

UserModPwdResponse = TypedDict('UserModPwdResponse',
            {
                
            }
        )
        
def postUserModPwd(oldPwd: str,
newPwd: str) -> UserModPwdResponse : '''
## POST user/modPwd
# 修改帐号密码

'''
