from api.data.user_details import UserDetails

import pytest
from api.post_sign_up import SignUp
from api.post_sign_in import SignIn
from api.get_users import GetUsers
from api.delete_user import DeleteUser
from generators.user_generator import get_random_user

@pytest.fixture(scope="module")
def user_credentials():
    return get_random_user()

@pytest.fixture(scope="module")
def sign_up_api():
    return SignUp()

@pytest.fixture(scope="module")
def sign_in_api():
    return SignIn()

@pytest.fixture(scope="module")
def get_users_api():
    return GetUsers()

@pytest.fixture(scope="module")
def delete_user_api():
    return DeleteUser()

@pytest.fixture(scope="module")
def user_token(sign_up_api, sign_in_api, user_credentials, delete_user_api):
    # Sign up the user
    sign_up_response = sign_up_api.api_call(user_credentials)
    if sign_up_response.status_code != 201:
        raise Exception("Signup failed")

    # Sign in the user
    sign_in_response = sign_in_api.api_call(user_credentials.username, user_credentials.password)
    sign_in_response.raise_for_status()
    if sign_in_response.status_code != 200:
        raise Exception("Signin failed")
    token = sign_in_response.json().get('token')
    if not token:
        raise Exception("Token should not be None")

    yield token  # Yield the token for use in tests

    # Delete the user after the test is done
    delete_user_api.api_call(user_credentials.username, token)

def test_get_all_users_success(get_users_api, user_token):
    users_details = get_users_api.api_call(user_token)
    
    # Convert UserDetails instances to dictionaries if necessary
    users_details = [user.to_dict() if isinstance(user, UserDetails) else user for user in users_details]

    for user in users_details:
        assert set(user.keys()) == {"id", "username", "email", "roles", "firstName", "lastName"}, "User data keys mismatch"
        assert all(isinstance(user[key], str) for key in ["username", "email", "firstName", "lastName"]), "User data types mismatch"
        assert isinstance(user["roles"], list), "Roles should be a list"
        assert all(isinstance(role, str) for role in user["roles"]), "Role types mismatch"

def test_get_all_users_invalid_token(get_users_api):
    invalid_token = "some_invalid_token"
    with pytest.raises(Exception) as excinfo:
        get_users_api.api_call(invalid_token)
    assert "403" in str(excinfo.value), "Expected a 403 status code for invalid token"
    assert "Expired or invalid JWT token" in str(excinfo.value), "Expected error message for invalid token"
