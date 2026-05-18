"""
exceptions.py — Custom Service Layer Exceptions
================================================
All business logic errors are raised as typed exceptions.
The API layer catches these and returns appropriate HTTP responses.
This keeps business rules out of the API layer.
"""


class UserNotFoundException(Exception):
    def __init__(self, user_id: str):
        super().__init__(f"User '{user_id}' not found.")
        self.user_id = user_id


class EmailAlreadyRegisteredException(Exception):
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' is already registered.")
        self.email = email


class InvalidEmailDomainException(Exception):
    def __init__(self, email: str):
        super().__init__(
            f"Email '{email}' is not a valid university email address."
        )
        self.email = email


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Invalid email or password.")


class AccountNotVerifiedException(Exception):
    def __init__(self):
        super().__init__("Account not verified. Please check your email.")


class ReportNotFoundException(Exception):
    def __init__(self, report_id: str):
        super().__init__(f"Report '{report_id}' not found.")
        self.report_id = report_id


class ReportNotEditableException(Exception):
    def __init__(self, report_id: str, status: str):
        super().__init__(
            f"Report '{report_id}' cannot be edited in status '{status}'."
        )


class ReportValidationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MatchNotFoundException(Exception):
    def __init__(self, match_id: str):
        super().__init__(f"Match record '{match_id}' not found.")
        self.match_id = match_id


class MatchAlreadyResolvedException(Exception):
    def __init__(self, match_id: str):
        super().__init__(f"Match '{match_id}' has already been confirmed or dismissed.")


class UnauthorisedActionException(Exception):
    def __init__(self, message: str = "You are not authorised to perform this action."):
        super().__init__(message)