import pytest
from api.post_sign_up import SignUp
from dotenv import load_dotenv
import requests
from generators import user_generator

load_dotenv()


@pytest.fixture
def sign_up_api():
    return SignUp()


def test_successful_sign_up(sign_up_api: SignUp):
    user = user_generator.get_random_user()
    response = sign_up_api.api_call(user)
    try:
        response.raise_for_status()
        assert response.status_code == 201, "Expected status code 201"
        assert response.json()['token'] is not None, "Token should not be None"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")
