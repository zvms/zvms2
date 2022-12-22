
import typing

 

NoticeNewResponse = TypedDict('NoticeNewResponse',
            {
                
            }
        )
        
def postNoticeNew(content: str,
announcer: str) -> NoticeNewResponse : '''
## POST notice/new
# 新建一条公告

'''


NoticeQueryResponse = TypedDict('NoticeQueryResponse',
            {
                "list": typing.Sequence[structs.Notice]
            }
        )
        
def getNoticeQuery() -> NoticeQueryResponse : '''
## GET notice/query
# 查询活跃公告

''' 


 

NoticeModifyByNtcIdResponse = TypedDict('NoticeModifyByNtcIdResponse',
            {
                
            }
        )
        
def postNoticeModifyByNtcId(id: int,
content: str,
announcer: str,
time: str,
status: int) -> NoticeModifyByNtcIdResponse : '''
## POST notice/modify/<ntcId>
# 修改指定公告

'''
