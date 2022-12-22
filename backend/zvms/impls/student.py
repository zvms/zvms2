
import typing


StudentVolbookByStuIdResponse = TypedDict('StudentVolbookByStuIdResponse',
            {
                "rec": typing.Sequence[structs.VolunteerRecord]
            }
        )
        
def getStudentVolbookByStuId() -> StudentVolbookByStuIdResponse : '''
## GET student/volbook/<stuId>
# 查询某个学生的义工本

''' 

