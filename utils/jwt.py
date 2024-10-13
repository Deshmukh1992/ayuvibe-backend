from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Secret key and algorithm
SECRET_KEY = '22b22897-2f07-4df2-9cc2-66c40c591d99'  # Should be stored in environment variable in production
ALGORITHM = "HS256"

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# print(hash_password("admin123"))


# print(verify_password("admin123", "$2b$12$BTNz8sKJ/yiEdIDEuyeaC.HfTwGbipHaNfewYJCOGevzuB1yKbQg."))