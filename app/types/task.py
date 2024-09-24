import strawberry
import typing
from app.helpers.task import get_all_task_of_user,add_user_task,update_task_by_user,delete_task_user,get_task_by_id
from app.database import SessionLocal
from typing import Optional


@strawberry.type
class Tasks:
    id:int
    title:str
    description:str
    user_id:int

@strawberry.type
class Query:
    @strawberry.field
    def get_all_user_task(self,info,user_id:int)->typing.List[Tasks]:
        db = SessionLocal()
        tasks=get_all_task_of_user(user_id=user_id,db=db)
        return tasks
    
    @strawberry.field
    def get_task(self,info,id:int)->Tasks:
        db = SessionLocal()
        tasks=get_task_by_id(id=id,db=db)
        return tasks


@strawberry.type
class Mutations:
    @strawberry.field
    def add_task(self,info,title:str,description:str,user_id:int)->str:
        db = SessionLocal()
        task=add_user_task(title=title,description=description,user_id=user_id,db=db)
        if task:
            return "added task successfully"
        else:
            return "something went wrong"
        
    @strawberry.field
    def update_task(self,info,id:int,title: Optional[str] = None, description: Optional[str] = None)->str:
        db=SessionLocal()
        updated=update_task_by_user(id=id,title=title,description=description,db=db)
        return updated
    @strawberry.field
    def delete_task(self,info,id:int)->str:
        db=SessionLocal()
        deleted=delete_task_user(id=id,db=db)
        return deleted