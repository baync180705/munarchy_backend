class MunarchyException(Exception):
    """Base exception class for Munarchy application"""
    pass

class UserAlreadyExistsError(MunarchyException):
    """Raised when attempting to register an existing user"""
    pass

class UserNotFoundError(MunarchyException):
    """Raised when user is not found in database"""
    pass

class PaymentError(MunarchyException):
    """Raised when payment processing fails"""
    def __init__(self, message, transaction_id=None):
        self.message = message
        self.transaction_id = transaction_id
        super().__init__(self.message)

class AllotmentError(MunarchyException):
    """Raised when portfolio allotment fails"""
    pass

class EmailError(MunarchyException):
    """Raised when email sending fails"""
    pass 