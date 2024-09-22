from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas import UserSchema,UserOut,UserUpdateSchema
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.models import User
from app.utils import get_password_hash
from app.oauth2 import get_current_user
router = APIRouter(prefix="/users")

@router.post("/",response_model=UserOut)
def create_post(
    request: UserSchema, db: Session = Depends(get_db)
):
    try:
        request.password=get_password_hash(request.password)
        create_user = User(**request.dict())
        db.add(create_user)
        db.commit()
        db.refresh(create_user)
    except Exception as e:
        raise HTTPException(detail="something went wrong"+str(e),status_code=status.HTTP_400_BAD_REQUEST)
    return create_user


@router.get("/all")
def get_all_users(db:Session=Depends(get_db)):
    users=db.query(User).all()
    return users


@router.get("/user/{id}", response_model=UserOut)
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exists",
        )
    return user



@router.put("/update/{id}",response_model=UserOut)
def update_user_email(id:int,request:UserUpdateSchema,db:Session=Depends(get_db)):
    update = db.query(User).filter(User.id == id)
    user_update = update.first()
    if not user_update:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"this id:{id} does not exist"
        )
   
    if request.password:
        request.password=get_password_hash(request.password)
        ## can be replace with below code
        ##{key:val for key,val in request.dict().items() if val}
    update.update({key:val for key,val in request.dict().items() if val}, synchronize_session=False)
    db.commit()
    db.refresh(user_update)
    return user_update



@router.delete("/user/delete/{id}")
def delete_user(
    id: int, db: Session = Depends(get_db)
):
    delete = db.query(User).filter(User.id == id)
    delete_user = delete.first()
    if not delete_user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"this id:{id} does not exist"
        )
    delete.delete()
    db.commit()
    return {"message":"deleted successfully"}