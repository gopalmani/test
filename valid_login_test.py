import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# we would be keeping these in a config/secret file ideally, keeping in test file for simplicity
appUrl = "https://www.saucedemo.com/"
valid_user = "standard_user"
locked_user = "locked_out_user"
invalid_user = "problem_user"
performace_test_user = "performance_glitch_user"
sign_in_password = "secret_sauce"


# Declaring a driver for test file, we can utilise Chrome, Edge, Firefox etc. Fixture is used for repetetive usage
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Helper function for login
def login(driver, username, password):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys(username)
    
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    ).send_keys(password)
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    ).click()


# Helper function for logout
def logout(driver):
    # Wait for the sidebar button to be clickable
    sidebar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "bm-burger-button"))
    )
    sidebar_button.click()
    
    # Click on the logout link
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    logout_link.click()

def test_successful_login_and_logout(driver):
    try:
        # Navigate to the website
        driver.get(appUrl)

        # Login as standard_user
        login(driver, valid_user, sign_in_password)
        # Locate the element by class name
        element = driver.find_element(By.CLASS_NAME,"app_logo")

        # Retrieve the text from the element
        text = element.text

        # Assert the text
        assert text == "Swag Labs", f"Expected 'Swag Labs' but got '{text}'"

        time.sleep(5)

        # Logout
        logout(driver)

        # Login as performance_glitch_user

        driver.get(appUrl)  # Navigate to the website again for a fresh login
        login(driver, performace_test_user, sign_in_password)

        # Locate the element by class name
        element = driver.find_element(By.CLASS_NAME, "app_logo")

        # Retrieve the text from the element
        text = element.text

        # Assert the text
        assert text == "Swag Labs", f"Expected 'Swag Labs' but got '{text}'"

        # Logout
        logout(driver)

    except Exception as e:
        print("Test failed: ", str(e))
        raise

# Helper function to verify default sort order
def verify_default_sort_order(driver):
    # Login if not already logged in
    driver.get(appUrl)
    login(driver, valid_user, sign_in_password)

    # Ensure items are displayed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    )

    # Retrieve item names in default order
    items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    item_names = [item.text for item in items]

    # Verify the items are sorted from A to Z
    assert item_names == sorted(item_names)

    # Logout
    logout(driver)

# Helper function to verify user can change sort order
def verify_user_sort_order(driver):
    # Login if not already logged in
    driver.get(appUrl)
    login(driver, valid_user, sign_in_password)

    # Ensure items are displayed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    # Sort items by price high to low
    driver.find_element(By.CLASS_NAME, "product_sort_container").click()
    driver.find_element(By.XPATH, "//option[text()='Price (high to low)']").click()

    # Wait for the sort to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    # Retrieve item prices in high to low order
    items = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices = [float(item.text.replace("$", "")) for item in items]

    # Verify the items are sorted by price high to low
    assert prices == sorted(prices, reverse=True)

    # Logout
    logout(driver)

# Test to verify default sort order
def test_verify_default_sort_order(driver):
    verify_default_sort_order(driver)

# Test to verify user can change sort order
def test_verify_user_sort_order(driver):
    verify_user_sort_order(driver)


