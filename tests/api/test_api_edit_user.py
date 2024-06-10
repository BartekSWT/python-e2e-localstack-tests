from api.data.user_details import UserDetails
from api.data.edit import EditUserDto
from api.get_user import GetUser

import pytest
from api.post_sign_up import SignUp
from api.post_sign_in import SignIn
from api.edit_user import EditUser
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
def edit_user_api():
    return EditUser()

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

@pytest.fixture(scope="module")
def new_user_data():
    return EditUserDto(
        email="newemail@example.com",
        firstName="NewFirstName",
        lastName="NewLastName",
        roles=["ROLE_ADMIN"]
    )

@pytest.fixture(scope="module")
def get_user_api():
    return GetUser()

def test_edit_user_success(edit_user_api, get_user_api, user_token, user_credentials, new_user_data):
    try:
        # Perform the edit operation
        edit_response = edit_user_api.api_call(user_credentials.username, new_user_data, user_token)
        assert edit_response.status_code == 200, "Expected status code 200 after edit"

        # Fetch the updated user details to verify changes
        get_response = get_user_api.api_call(user_credentials.username, user_token)
        updated_user_detail = get_response.to_dict() if isinstance(get_response, UserDetails) else get_response

        # Assert the updated details
        assert updated_user_detail["email"] == new_user_data.email, "Email update mismatch"
        assert updated_user_detail["firstName"] == new_user_data.firstName, "First name update mismatch"
        assert updated_user_detail["lastName"] == new_user_data.lastName, "Last name update mismatch"
        assert updated_user_detail["roles"] == new_user_data.roles, "Roles update mismatch"
    except AssertionError as e:
        print(f"Assertion Error: {e}")
        print(f"Response: {updated_user_detail}")
        raise

def test_edit_user_invalid_username(edit_user_api, user_token, new_user_data):
    try:
        invalid_username = "nonexistent_user"
        response = edit_user_api.api_call(invalid_username, new_user_data, user_token)
        # This line should ideally never be reached if the API behaves correctly
        assert response.status_code == 404, "Expected status code 404 for nonexistent user"
    except Exception as exc:
        assert "404" in str(exc), "Expected a 404 status code for invalid username"
        assert "The user doesn't exist" in str(exc), "Expected error message for invalid username"

def test_edit_user_invalid_token(edit_user_api, user_credentials, new_user_data):
    try:
        invalid_token = "some_invalid_token"
        response = edit_user_api.api_call(user_credentials.username, new_user_data, invalid_token)
        # This line should ideally never be reached if the API behaves correctly
        assert response.status_code == 403, "Expected status code 403 for invalid token"
    except Exception as exc:
        assert "403" in str(exc), "Expected a 403 status code for invalid token"
        assert "Expired or invalid JWT token" in str(exc), "Expected error message for invalid token"
