import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.mark.parametrize("username, password, expected_error", [
    ("wronguser", "wrongpassword", "Your username is invalid!"),
    ("admin", "wrongpassword", "Your password is invalid!"),
    ("", "password123", "Your username is invalid!"),
    ("student", "", "Your password is invalid!"),
    ("", "", "Your username is invalid!"),
])
def test_invalid_login(username, password, expected_error):
    # Setup WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # Open the login page
        driver.get("https://practicetestautomation.com/practice-test-login")
        time.sleep(2)  # Allow page to load

        # Locate input fields and login button
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "submit")

        # Enter credentials and submit
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        time.sleep(2)  # Wait for response

        # Verify error message
        error_message = driver.find_element(By.ID, "error").text
        assert expected_error in error_message, f"Expected: {expected_error}, Got: {error_message}"
        print(f"✅ Test Passed for ({username}, {password})")

    except Exception as e:
        print(f"❌ Test encountered an error: {e}")

    finally:
        driver.quit()
