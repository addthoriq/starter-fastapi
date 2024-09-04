from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from ...models.tokenModel import Token
from ...controllers.auth_controller import *
from app.models import userModel

router = APIRouter()

@router.post('/login')
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer",
            }
        )
    access_token_expires = timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
    data = {
        "sub": user.username
    },
    expires_delta = access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
    )

user_deps = Annotated[dict, Depends(get_current_user)]
@router.get('/me', response_model=userModel.User)
def read_user_me(user: user_deps):
    return user

@router.put('/change-password')
def modify_password(
        user: userModel.UserChangePassword,
        userlogin: userModel.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return change_password(db, user.old_password, user.new_password, userlogin)