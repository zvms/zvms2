
import typing


ClassListResponse = TypedDict('ClassListResponse',
            {
                
            }
        )
        
def getClassList() -> ClassListResponse : '''
## GET class/list
# 获取班级列表

''' 



ClassStulistByClassIdResponse = TypedDict('ClassStulistByClassIdResponse',
            {
                
            }
        )
        
def getClassStulistByClassId() -> ClassStulistByClassIdResponse : '''
## GET class/stulist/<classId>
# 获取某个班级的学生列表

''' 



ClassVolunteerByClassIdResponse = TypedDict('ClassVolunteerByClassIdResponse',
            {
                
            }
        )
        
def getClassVolunteerByClassId() -> ClassVolunteerByClassIdResponse : '''
## GET class/volunteer/<classId>
# 查询某个班级能参加的义工活动列表

''' 



ClassNoThoughtResponse = TypedDict('ClassNoThoughtResponse',
            {
                
            }
        )
        
def getClassNoThought() -> ClassNoThoughtResponse : '''
## GET class/noThought
# 获取未填写感想的义工

''' 

