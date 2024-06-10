from api.data.user_details import UserDetails

import pytest
from api.post_sign_up import SignUp
from api.post_sign_in import SignIn
from api.get_me import GetMe
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
def get_me_api():
    return GetMe()

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

def test_get_me_success(get_me_api, user_token, user_credentials):
    try:
        user_detail = get_me_api.api_call(user_token)
        
        # Convert UserDetails instance to dictionary if necessary
        user_detail = user_detail.to_dict() if isinstance(user_detail, UserDetails) else user_detail

        # Assert that the user details in the response match those provided during signup
        assert user_detail["username"] == user_credentials.username, "Username mismatch"
        assert user_detail["email"] == user_credentials.email, "Email mismatch"
        assert user_detail["firstName"] == user_credentials.firstName, "First name mismatch"
        assert user_detail["lastName"] == user_credentials.lastName, "Last name mismatch"
        assert user_detail["roles"] == user_credentials.roles, "Roles mismatch"
    except AssertionError as e:
        print(f"Assertion Error: {e}")
        print(f"Response: {user_detail}")
        raise

def test_get_me_invalid_token(get_me_api, user_credentials):
    try:
        invalid_token = "some_invalid_token"
        response = get_me_api.api_call(invalid_token)
        # This line should ideally never be reached if the API behaves correctly
        assert response.status_code == 403, "Expected status code 403 for invalid token"
    except Exception as exc:
        assert "403" in str(exc), "Expected a 403 status code for invalid token"
        assert "Expired or invalid JWT token" in str(exc), "Expected error message for invalid token"
