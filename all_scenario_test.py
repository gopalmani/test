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

# Helper function to add random 3 items to cart
def add_random_items_to_cart(driver, num_items=3):
    # Login if not already logged in
    driver.get(appUrl)

    login(driver, valid_user, sign_in_password)
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    for i in range(num_items):
        items[i].find_element(By.CLASS_NAME, "btn_primary").click()

# Helper function to add highest and lowest price items to cart
def add_highest_and_lowest_price_items_to_cart(driver):
    # Login if not already logged in
    driver.get(appUrl)
    login(driver, valid_user, sign_in_password)

    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    items.sort(key=lambda x: float(x.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", "")))
    items[0].find_element(By.CLASS_NAME, "btn_primary").click()  # Add lowest price item
    items[-1].find_element(By.CLASS_NAME, "btn_primary").click()  # Add highest price item

# Test to verify items in cart are retained after logout
def test_verify_items_in_cart_retained(driver):
    try:
        # Login if not already logged in
        driver.get(appUrl)
        login(driver, valid_user, sign_in_password)

        # Add 3 random items to cart
        add_random_items_to_cart(driver, num_items=3)

        # Logout
        logout(driver)

        # Login again
        login(driver, valid_user, sign_in_password)

        # Navigate to cart and verify previously added items are in cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        items_in_cart = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items_in_cart) == 3

        # Logout
        logout(driver)

    except Exception as e:
        print("Test failed: ", str(e))
        raise

# Test to verify user can place order
def test_verify_user_can_place_order(driver):
    try:
        # Login if not already logged in
        driver.get(appUrl)
        login(driver, valid_user, sign_in_password)

        # Add highest and lowest price items to cart
        add_highest_and_lowest_price_items_to_cart(driver)

        # Navigate to checkout information page
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.CLASS_NAME, "checkout_button").click()

        # Verify input field validations on checkout information page
        first_name_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "first-name"))
        )
        first_name_field.send_keys("John")

        last_name_field = driver.find_element(By.ID, "last-name")
        last_name_field.send_keys("Doe")

        zip_code_field = driver.find_element(By.ID, "postal-code")
        zip_code_field.send_keys("12345")

        # Navigate to checkout overview page
        driver.find_element(By.CLASS_NAME, "cart_button").click()

        # Verify total price and place order
        total_price = float(driver.find_element(By.CLASS_NAME, "summary_total_label").text.replace("Total: $", ""))
        assert total_price > 0  # Verify total price is greater than 0

        # Place order
        driver.find_element(By.CLASS_NAME, "btn_action").click()

        # Verify confirmation and navigate to home page
        confirmation_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert confirmation_message.text == "Thank you for your order!"

        # Navigate to home page
        driver.find_element(By.CLASS_NAME, "btn_primary").click()

    except Exception as e:
        print("Test failed: ", str(e))
        raise



