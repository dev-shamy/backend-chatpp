from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email=data.email,
            name=data.name,
            hashed_password=hash_password(data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        jwt_token = create_access_token(user_id=str(user.id), email=user.email)

        return {
            "message": "User created successfully",
            "access_token": jwt_token,
            "email": user.email,
            "user_id": user.id
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error during signup: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not exist with this email",
            )

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        jwt_token = create_access_token(user_id=str(user.id), email=user.email)

        return {
            "email": user.email,
            "access_token": jwt_token,
            "user_id": user.id
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Error during login:", str(e))
        raise HTTPException(
            status_code=500, detail=f"Unexpected error during login: {str(e)}"
        )
