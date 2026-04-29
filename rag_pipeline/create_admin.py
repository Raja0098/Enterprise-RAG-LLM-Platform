from config.db import SessionLocal
from api.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

username = "raja"
password = "raja"

# check if exists
existing = db.query(User).filter(User.username == username).first()

if existing:
    print("⚠️ Admin already exists")
else:
    admin = User(
        username=username,
        password=pwd_context.hash(password),
        is_admin=True
    )

    db.add(admin)
    db.commit()

    print("✅ Admin created: username=raja password=raja")