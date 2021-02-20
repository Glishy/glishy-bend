error_dict = {
    "required": "This field is required.",
    "does_not_exist": "{} does not exist",
    "min_length": "{0} must be at least {1} characters long.",
    "max_length": "{0} must be at at most {1} characters long.",
    "invalid_phone_no": "Phone number must be numbers of the format +254...",
    "already_exist": "{0} already exist.",
    'invalid_password': 'Password must have at least a number, and a least an uppercase and a lowercase letter.',
    "invalid_name": "{0} cannot have spaces or special characters.",
    "user_not_found": "A user with this email and password was not found."
}

jwt_errors = {
    'token_expired': 'Token expired. Please login to get a new token.',
    'invalid_token': 'Authorization failed due to an Invalid token.',
    'invalid_secret': 'Cannot verify the token provided as the expected issuer does not match.',
    'token_user_not_found': "No user found for token provided"
}
