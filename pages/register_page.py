from typing import Type, TypeVar
from selenium import webdriver
from components.alert import AlertComponent
from pages.abstract_base_page import AbstractBasePage
from selenium.webdriver.common.by import By

T = TypeVar('T', bound='AbstractBasePage')


class RegisterPage(AbstractBasePage):
    firstname_input = (By.NAME, "firstName")
    lastname_input = (By.NAME, "lastName")
    username_input = (By.NAME, "username")
    password_input = (By.NAME, "password")
    email_input = (By.NAME, "email")
    register_button = (By.CSS_SELECTOR, "button.btn.btn-primary")

    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def attempt_register(self, firstname: str, lastname: str, username: str, password: str, email: str,
                         expected_page: Type[T]) -> T:
        self.driver.find_element(*self.firstname_input).send_keys(firstname)
        self.driver.find_element(*self.lastname_input).send_keys(lastname)
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.register_button).click()
        return self.new_instance_of(expected_page)

    def get_alert(self):
        return AlertComponent(self.driver)
