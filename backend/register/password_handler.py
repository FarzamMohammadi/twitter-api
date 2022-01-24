import bcrypt


# Password validation
def password_check(password):

    special_symbols = ['$', '@', '#', '%', '/']
    val = True

    if len(password) < 6:
        print('length should be at least 6')
        val = False

    if len(password) > 20:
        print('length should be not be greater than 8')
        val = False

    if not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in password):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in password):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in special_symbols for char in password):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val


# Password hashing
def hash_password(password):
    hashed_pass = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))
    return hashed_pass
