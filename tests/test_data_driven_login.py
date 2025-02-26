import csv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Load test data from CSV file
def load_test_data():
    data = []
    csv_file_path = "C:/Users/HP/OneDrive/Documents/selenium-project/data/test_data.csv"
    try:
        with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                data.append((row[0].strip(), row[1].strip(), row[2].strip()))  # Remove extra spaces
    except FileNotFoundError:
        pytest.fail(f"❌ CSV file not found at {csv_file_path}. Check your path!")
    return data

@pytest.mark.parametrize("username,password,expected_message", load_test_data())
def test_login(username, password, expected_message):
    print(f"\n🟢 Testing with Username: {username}, Password: {password}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        driver.get("https://practicetestautomation.com/practice-test-login")
        wait = WebDriverWait(driver, 10)

        # ✅ Wait for username field and enter credentials
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(username)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        driver.find_element(By.ID, "submit").click()

        # ✅ Handle SUCCESS case
        if expected_message == "Login Successful":
            try:
                success_message_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                success_message = success_message_element.text.strip()
                print(f"✅ SUCCESS! Expected: '{expected_message}', Found: '{success_message}'")
                assert success_message == "Logged In Successfully", f"❌ Expected 'Logged In Successfully', but got '{success_message}'"
            except Exception as e:
                driver.save_screenshot("failed_success_case.png")
                pytest.fail(f"❌ Expected success message not found. Error: {str(e)}")

        # ✅ Handle ERROR case
        else:
            try:
                error_message_element = wait.until(EC.presence_of_element_located((By.ID, "error")))
                error_message = error_message_element.text.strip()
                print(f"❌ FAILURE! Expected: '{expected_message}', Found: '{error_message}'")
                assert error_message == expected_message, f"❌ Expected '{expected_message}', but got '{error_message}'"
            except Exception as e:
                driver.save_screenshot("failed_error_case.png")
                pytest.fail(f"❌ Expected error message element not found. Error: {str(e)}")

    finally:
        driver.quit()
