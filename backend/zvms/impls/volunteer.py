
import typing


VolunteerListResponse = TypedDict('VolunteerListResponse',
            {
                
            }
        )
        
def getVolunteerList() -> VolunteerListResponse : '''
## GET volunteer/list
# 义工活动总表

''' 



VolunteerFetchByVolIdResponse = TypedDict('VolunteerFetchByVolIdResponse',
            {
                "name": str,
"date": str,
"time": str,
"stuMax": int,
"stuNow": int,
"description": str,
"status": int,
"inside": int,
"outside": int,
"large": int
            }
        )
        
def getVolunteerFetchByVolId() -> VolunteerFetchByVolIdResponse : '''
## GET volunteer/fetch/<volId>
# 查询单次义工详细信息

''' 


 

VolunteerSignupByVolIdResponse = TypedDict('VolunteerSignupByVolIdResponse',
            {
                
            }
        )
        
def postVolunteerSignupByVolId(stulist: typing.Sequence[int]) -> VolunteerSignupByVolIdResponse : '''
## POST volunteer/signup/<volId>
# 报名义工活动

'''

 

VolunteerCreateResponse = TypedDict('VolunteerCreateResponse',
            {
                
            }
        )
        
def postVolunteerCreate(name: str,
date: str,
time: str,
stuMax: int,
description: str,
status: int,
inside: int,
outside: int,
large: int) -> VolunteerCreateResponse : '''
## POST volunteer/create
# 创建义工活动

'''


VolunteerSignerListByVolIdResponse = TypedDict('VolunteerSignerListByVolIdResponse',
            {
                
            }
        )
        
def getVolunteerSignerListByVolId() -> VolunteerSignerListByVolIdResponse : '''
## GET volunteer/signerList/<volId>
# 获取义工活动报名列表

''' 


 

VolunteerThoughtByVolIdResponse = TypedDict('VolunteerThoughtByVolIdResponse',
            {
                
            }
        )
        
def postVolunteerThoughtByVolId() -> VolunteerThoughtByVolIdResponse : '''
## POST volunteer/thought/<volId>
# 义工活动感想提交

'''


VolunteerRandomThoughtResponse = TypedDict('VolunteerRandomThoughtResponse',
            {
                
            }
        )
        
def getVolunteerRandomThought(username: str,
userId: int,
content: str) -> VolunteerRandomThoughtResponse : '''
## GET volunteer/randomThought
# 随机获取一条感想

''' 


 

VolunteerAuditByVolIdResponse = TypedDict('VolunteerAuditByVolIdResponse',
            {
                
            }
        )
        
def postVolunteerAuditByVolId(thought: typing.Sequence[structs.VolunteerRecord]) -> VolunteerAuditByVolIdResponse : '''
## POST volunteer/audit/<volId>
# 感想审核

'''


VolunteerUnauditedResponse = TypedDict('VolunteerUnauditedResponse',
            {
                
            }
        )
        
def getVolunteerUnaudited() -> VolunteerUnauditedResponse : '''
## GET volunteer/unaudited
# 获取未审核感想

''' 


 

VolunteerHolidayResponse = TypedDict('VolunteerHolidayResponse',
            {
                
            }
        )
        
def postVolunteerHoliday(name: str,
date: str,
time: str,
stuId: typing.Sequence[int],
description: str,
inside: int,
outside: int,
large: int) -> VolunteerHolidayResponse : '''
## POST volunteer/holiday
# 假期义工统一修改

'''
