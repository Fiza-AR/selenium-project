from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options (disable headless for debugging)
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Uncomment for headless mode

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the demo login page
    driver.get("https://the-internet.herokuapp.com/login")

    # Wait for the username field
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    username.send_keys("tomsmith")  # Demo username

    # Wait for the password field
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password.send_keys("SuperSecretPassword!")  # Demo password

    # Click the login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
    )
    login_button.click()

    # Wait for login confirmation
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flash.success"))
    )

    print("Login successful:", success_message.text)

except Exception as e:
    print(f"Error: {e}")

finally:
    time.sleep(3)  # Keep the browser open for debugging
    driver.quit()
