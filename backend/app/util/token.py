from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

# JWT 配置
SECRET_KEY = "your_secret_key"  # 替换为你的密钥
ALGORITHM = "HS256"  # 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token 有效时间

# HTTP Bearer 认证
security = HTTPBearer()


# Token 生成方法
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 从 Token 中获取用户 ID
def get_user_id_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print(token)
    try:
        # 解码 Token
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # 添加这个打印语句
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user ID not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
