valid_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.-_'
valid_categories = ['Electronics', 'Household', 'Sports', 'Fashion', 'Entertainment']
valid_roles = ['User', 'Seller', 'Admin']

def is_valid_string(string):
    for char in string:
        if char not in valid_string:
            return False
    return True

def is_valid_category(category):
    return category in valid_categories

def is_valid_positive_int(integer):
    try:
        integer = int(integer)
        return integer > 0
    except Exception:
        return False

def is_valid_role(role):
    return role in valid_roles