class OrderNotFoundError(Exception):
    pass

class InvalidOrderStateError(Exception):
    pass

class PermissionDeniedError(Exception):
    pass

class ApprovalRequiredError(Exception):
    pass