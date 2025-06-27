import bcrypt


def hash_password(plain_password: str) -> str:
    
    plain_password = bytes(plain_password, "utf-8")

    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(plain_password, salt)

    return hashed_pwd.decode("utf-8")



def compare_password(plain: str, hashed: str) -> bool:

    plain = bytes(plain, "utf-8")
    hashed = bytes(hashed, "utf-8")

    return bcrypt.checkpw(plain, hashed)