import time
import pytest
import os
import requests
from api.get_emails import GetMessages
from pages.email_page import EmailPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from dotenv import load_dotenv
from faker import Faker

from tests.conftest import setup_test_user

load_dotenv()


@pytest.fixture(scope="module")
def new_user():
    return setup_test_user()


@pytest.fixture
def home_page(chrome_browser, new_user):
    chrome_browser.get(os.getenv("FRONTEND_URL"))
    login_page = LoginPage(chrome_browser)
    return login_page.attempt_login(new_user.username, new_user.password, HomePage)


@pytest.fixture(scope="module")
def get_emails_api():
    return GetMessages()


def test_sending_mail(home_page: HomePage, get_emails_api: GetMessages, new_user):
    fake = Faker()
    message = fake.text(max_nb_chars=50)
    subject = fake.text(max_nb_chars=10)
    email_page = home_page.click_email_on(new_user)
    email_page.attempt_send_email(subject, message, EmailPage).get_alert().verify_alert_success(
        "Email was scheduled to be send")
    time.sleep(5)  # gives time for mail to process through queue
    response = get_emails_api.api_call()
    try:
        response.raise_for_status()
        assert response.status_code == 200, "Expected status code 200"
        assert response.json()["items"] is not None, "Token should not be None"
        assert assert_email_is_sent(response.json()["items"], subject, message) == True
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")


def assert_email_is_sent(items, subject, message):
    assertion = False
    for item in items:
        if item["Content"]["Headers"]["Subject"][0] == subject and item["Content"]["Body"] == message:
            assertion = True
            break
    return assertion


'''def test_failed_login(login_page: LoginPage):
    login_page.attempt_login("wrong", "wrong", LoginPage).get_alert().verify_alert_danger(
        "Invalid username/password supplied"
    )'''
