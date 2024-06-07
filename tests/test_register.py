import time
import pytest
import os
import requests
from api.post_sign_in import SignIn
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from dotenv import load_dotenv
from generators import user_generator
from api.data.register import User

load_dotenv()


@pytest.fixture
def register_page(chrome_browser):
    chrome_browser.get(os.getenv("FRONTEND_URL"))
    login_page = LoginPage(chrome_browser)
    return login_page.go_to_register(RegisterPage)


@pytest.fixture(scope="module")
def sign_in_api():
    return SignIn()


def test_successful_register(register_page: RegisterPage, sign_in_api: SignIn):
    user = user_generator.get_random_user()
    register_page.attempt_register(user.firstName, user.lastName, user.username, user.password, user.email, LoginPage
                                   ).get_alert().verify_alert_success("Registration successful")
    assert_user_via_api(user, sign_in_api)


def assert_user_via_api(user: User, sign_in_api: SignIn):
    time.sleep(1)  # gives server time to process
    response = sign_in_api.api_call(user.username, user.password)
    try:
        response.raise_for_status()
        assert response.status_code == 200, "Expected status code 200"
        assert response.json()['token'] is not None, "Token should not be None"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")


'''def test_failed_login(login_page: LoginPage):
    login_page.attempt_login("wrong", "wrong", LoginPage).get_alert().verify_alert_danger(
        "Invalid username/password supplied"
    )'''
