"""
users.py — User API Router
============================
RESTful endpoints for User registration, authentication, and management.
All endpoints documented for OpenAPI/Swagger auto-generation.

Base path: /api/users
"""
from fastapi import APIRouter, Depends, HTTPException, status
from api.schemas import (
    RegisterRequest, LoginRequest, UpdateProfileRequest,
    UpdateRoleRequest, UserResponse, MessageResponse, ErrorResponse,
)
from api.dependencies import get_user_service
from services.user_service import UserService
from services.exceptions import (
    EmailAlreadyRegisteredException,
    InvalidEmailDomainException,
    InvalidCredentialsException,
    AccountNotVerifiedException,
    UserNotFoundException,
    UnauthorisedActionException,
)
from src.enums import UserRole

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student account",
    description=(
        "Creates a new CampusFind account using a valid university email address. "
        "BR-01: Email must end with the university domain. "
        "A verification email is sent upon successful registration."
    ),
    responses={
        201: {"description": "User registered successfully"},
        400: {"model": ErrorResponse, "description": "Invalid email domain or weak password"},
        409: {"model": ErrorResponse, "description": "Email already registered"},
    },
)
def register(
    body: RegisterRequest,
    svc: UserService = Depends(get_user_service),
):
    try:
        user = svc.register(body.full_name, body.email, body.password)
        return _to_response(user)
    except InvalidEmailDomainException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EmailAlreadyRegisteredException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/verify/{user_id}",
    response_model=UserResponse,
    summary="Verify user email address",
    description="Activates a user account after email verification link is clicked.",
    responses={
        200: {"description": "Account verified"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
def verify_email(
    user_id: str,
    svc: UserService = Depends(get_user_service),
):
    try:
        user = svc.verify_email(user_id)
        return _to_response(user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/login",
    response_model=UserResponse,
    summary="Login with email and password",
    description=(
        "Authenticates a user. Returns generic error on failure "
        "(never reveals which field is wrong — security best practice)."
    ),
    responses={
        200: {"description": "Login successful"},
        401: {"model": ErrorResponse, "description": "Invalid credentials or unverified account"},
    },
)
def login(
    body: LoginRequest,
    svc: UserService = Depends(get_user_service),
):
    try:
        user = svc.login(body.email, body.password)
        return _to_response(user)
    except (InvalidCredentialsException, AccountNotVerifiedException) as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Get all users (admin only)",
    description="Returns all registered users. Intended for admin use only.",
)
def get_all_users(svc: UserService = Depends(get_user_service)):
    return [_to_response(u) for u in svc.get_all()]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    responses={
        200: {"description": "User found"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
def get_user(user_id: str, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.get_by_id(user_id)
        return _to_response(user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user profile",
    responses={
        200: {"description": "Profile updated"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
def update_profile(
    user_id: str,
    body: UpdateProfileRequest,
    svc: UserService = Depends(get_user_service),
):
    try:
        user = svc.update_profile(user_id, body.full_name)
        return _to_response(user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Deactivate user account",
    responses={
        200: {"description": "Account deactivated"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
def deactivate_user(user_id: str, svc: UserService = Depends(get_user_service)):
    try:
        svc.deactivate(user_id)
        return {"message": f"User '{user_id}' has been deactivated."}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Helper ────────────────────────────────────────────────────────

def _to_response(user) -> dict:
    return {
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role.value,
        "is_verified": user.is_verified,
    }
