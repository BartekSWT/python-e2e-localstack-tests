from typing import Type, TypeVar
from selenium import webdriver
from components.alert import AlertComponent
from pages.abstract_base_page import AbstractBasePage
from selenium.webdriver.common.by import By

T = TypeVar('T', bound='AbstractBasePage')


class EmailPage(AbstractBasePage):
    subject_input = (By.NAME, "subject")
    message_input = (By.NAME, "message")
    send_button = (By.CSS_SELECTOR, "button.btn.btn-primary")
    error_alert = (By.CSS_SELECTOR, ".alert.alert-danger")
    success_alert = (By.CSS_SELECTOR, ".alert.alert-success")

    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def attempt_send_email(self, subject: str, message: str, expected_page: Type[T]) -> T:
        self.driver.find_element(*self.subject_input).send_keys(subject)
        self.driver.find_element(*self.message_input).send_keys(message)
        self.driver.find_element(*self.send_button).click()
        return self.new_instance_of(expected_page)

    def get_alert(self):
        return AlertComponent(self.driver)
