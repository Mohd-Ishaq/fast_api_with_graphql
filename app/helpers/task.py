from app.models import Task
from fastapi import Depends,HTTPException,status



def get_all_task_of_user(user_id:int,db):
    if not id:
        raise HTTPException(detail="invalid id provided",status_code=status.HTTP_400_BAD_REQUEST)
    task=db.query(Task).filter(Task.user_id==user_id).all()
    return task

def get_task_by_id(id:int,db):
    if not id:
        raise HTTPException(detail="invalid id provided",status_code=status.HTTP_400_BAD_REQUEST)
    task=db.query(Task).filter(Task.id==id).first()
    print(task)
    if task is None:  # Check if the task was found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id:{id} does not exist."
        )
    return task


def add_user_task(title:str,description:str,user_id:int,db):
    try:
        added_task=Task(title=title, description=description,user_id=user_id)
        db.add(added_task)
        db.add(added_task)
        db.commit()
        db.refresh(added_task)
    except Exception as e:
        raise HTTPException(detail="something went wrong"+str(e),status_code=status.HTTP_400_BAD_REQUEST)
    return added_task




def update_task_by_user(id:int,title:str,description:str,db):
    try:
        task=db.query(Task).filter(Task.id==id)
        updated_task=task.first()
        if not updated_task:
            return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"task does not exist with id:{id}"
            )
        to_update={}
        if title is not None:
            to_update[Task.title] = title
        if description is not None:
            to_update[Task.description] = description
        task.update(to_update,synchronize_session=False)
        db.commit()
        db.refresh(updated_task)
    except Exception as e:
        raise HTTPException(detail=str(e),status_code=status.HTTP_400_BAD_REQUEST)
    return "updated_successfully"



def delete_task_user(id:int,db):
    task=db.query(Task).filter(Task.id==id)
    to_delete=task.first()
    if not to_delete:
        return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"task does not exist with id:{id}"
        )
    db.delete(to_delete)
    db.commit()
    return "Deleted Successfully"