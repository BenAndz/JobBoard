import bcrypt 

def hash_password(password: str) -> str: 
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(real_password: str, hashed_password: str) -> bool: 
    return bcrypt.checkpw(real_password.encode('utf-8'), hashed_password.encode('utf-8'))
