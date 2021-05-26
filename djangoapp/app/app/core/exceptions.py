from rest_framework.exceptions import APIException

class UniqueEmail(APIException):
    status_code = 406
    default_detail = 'This email already exists'
    default_code = 'unique_email'