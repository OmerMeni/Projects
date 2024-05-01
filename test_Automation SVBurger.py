from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import time
import pytest


@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    driver.get('https://svburger1.co.il/#/')
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.close()


"""
Sanity automation test for SVBurger
"""


def test_sanity(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    reserve = driver.find_element(By.XPATH, '//button[text() = " Reserve "]')
    driver.execute_script("arguments[0].scrollIntoView(true);", reserve)
    time.sleep(1)
    reserve.click()
    driver.find_element(By.XPATH, '//button[text() = "Send"]').click()
    assert driver.find_element(By.XPATH, '//h3[text() = " Your order has been successfully received "]').is_displayed()
    time.sleep(2)


"""
Suite 1 : Sign - in

Functionalities :

    - 1.1 > Sign in with Walla mail
    - 1.2 > Using the Reset password button
    - 1.3 > Resetting password for a registered email account
    - 1.4 > Return to the Sign - In page from the Reset password page
    - 1.5 > Return to the Sign Up page from the Reset password page

Error handling : 

    - 1.6 > Signing in without inserting any registered email
    - 1.7 > Signing in without inserting any password
"""


def test_signin_walla(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@walla.co.il")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Moshikomanyak")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    assert driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').is_displayed()
    time.sleep(2)


def test_click_forgotpassword(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//a[@id = "forgotId"]').click()
    assert driver.find_element(By.XPATH, '//button[text() = "Reset Password"]').is_displayed()
    time.sleep(2)


def test_resetpass(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//a[@id = "forgotId"]').click()
    driver.find_element(By.XPATH, '//input[@id = "inputForgotPassword"]').send_keys(
        "omer18@gmail.com")  # Note that it will only work on the first run you will need to enter a different registered email to run this again.
    driver.find_element(By.XPATH, '//button[text() = "Reset Password"]').click()
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        alert_message = alert.text
        time.sleep(2)
        alert.accept()
        assert alert_message == 'Check your inbox for further instructions'  # ---> If entered an already registered email
    except:
        alert = driver.switch_to.alert
        alert_message = alert.text
        time.sleep(2)
        alert.accept()
        assert alert_message == 'Failed to reset password'  # ---> If entered the same email already twice and clicked 'reset password' or entered an unregistered email
        print("You either already entered the same email twice or entered an unregistered email")
    time.sleep(2)


def test_return_to_signin(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//a[@id = "forgotId"]').click()
    driver.find_element(By.XPATH, '//a[text() = "Sign In"]').click()
    assert driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').is_displayed()
    time.sleep(2)


def test_return_to_signup(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//a[@id = "forgotId"]').click()
    driver.find_element(By.XPATH, '//a[text() = "Sign Up"]').click()
    assert driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').is_displayed()
    time.sleep(2)


def test_no_email_signin(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    alert = driver.switch_to.alert
    alert_message = alert.text
    time.sleep(2)
    alert.accept()
    assert alert_message == "Failed to log in"
    time.sleep(2)


def test_no_password_signin(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    alert = driver.switch_to.alert
    alert_message = alert.text
    time.sleep(2)
    alert.accept()
    assert alert_message == "Failed to log in"
    time.sleep(2)


"""
Suite 2 : Sign - up

Functionalities :

    - 2.1 > Sign Up without entering the first name since according to the SRS it is not required to enter first name
    - 2.2 > Sign Up without entering the last name since according to the SRS it is not required to enter last name
    - 2.3 > Sign Up without entering the full name since according to the SRS it is not required to enter first name + last name
    - 2.4 > Sign up with walla account
    - 2.5 > Sign up with 9 characters in the password field

Error handling : 

    - 2.6 > Signing up with different password and confirm password
    - 2.7 > Signing up with inserting hebrew characters in the first name field
"""


def test_signup_no_fname(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href = "#/SignUp"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your first name"]')
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your last name"]').send_keys("Moshiko")
    driver.find_element(By.XPATH, '//input[@type= "email"]').send_keys("snfiopgdsogn@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Create Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//input[@placeholder = "Confirm Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    alert = driver.switch_to.alert
    time.sleep(2)
    alert.accept()
    current_url = driver.current_url
    assert current_url == 'https://svburger1.co.il/#/'
    time.sleep(2)


def test_signup_no_sname(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href = "#/SignUp"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your first name"]').send_keys("Omeriko")
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your last name"]')
    driver.find_element(By.XPATH, '//input[@type= "email"]').send_keys("snfiopgdsogn@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Create Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//input[@placeholder = "Confirm Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    alert = driver.switch_to.alert
    time.sleep(2)
    alert.accept()
    current_url = driver.current_url
    assert current_url == 'https://svburger1.co.il/#/'
    time.sleep(2)


def test_signup_no_fullname(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href = "#/SignUp"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your first name"]')
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your last name"]')
    driver.find_element(By.XPATH, '//input[@type= "email"]').send_keys("snfiopgdsogn@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Create Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//input[@placeholder = "Confirm Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    alert = driver.switch_to.alert
    time.sleep(2)
    alert.accept()
    current_url = driver.current_url
    assert current_url == 'https://svburger1.co.il/#/'
    time.sleep(2)


def test_signup_walla(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href = "#/SignUp"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your first name"]').send_keys('Lionel')
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your last name"]').send_keys("Messsi")
    driver.find_element(By.XPATH, '//input[@type= "email"]').send_keys("lionelmessi10@walla.co.il")
    driver.find_element(By.XPATH, '//input[@placeholder = "Create Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//input[@placeholder = "Confirm Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    assert driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').is_displayed()
    time.sleep(2)


def test_signup_9_char_pass(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href = "#/SignUp"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your first name"]').send_keys('Lionel')
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your last name"]').send_keys("Messsi")
    driver.find_element(By.XPATH, '//input[@type= "email"]').send_keys("daubyobfuabyfabfy@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Create Password"]').send_keys("Moshik12!")
    driver.find_element(By.XPATH, '//input[@placeholder = "Confirm Password"]').send_keys("Moshik12!")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    assert driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').is_displayed()
    time.sleep(2)


def test_signup_password_cpassword(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href = "#/SignUp"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your first name"]').send_keys("Lionel")
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your last name"]').send_keys("Messsi")
    driver.find_element(By.XPATH, '//input[@type= "email"]').send_keys("ndklansdlkas@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Create Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//input[@placeholder = "Confirm Password"]').send_keys("Moshik1")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    alert = driver.switch_to.alert
    alert_message = alert.text
    time.sleep(2)
    alert.accept()
    assert alert_message == "password and confirm error"
    time.sleep(2)


def test_signup_fname_hebrew(setup):
    driver = setup
    driver.find_element(By.XPATH, '//a[@href = "#/SignUp"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your first name"]').send_keys("עומריקו")
    driver.find_element(By.XPATH, '//input[@placeholder = "Type your last name"]').send_keys("Meniii")
    driver.find_element(By.XPATH, '//input[@type= "email"]').send_keys("ndklansdlkas@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Create Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//input[@placeholder = "Confirm Password"]').send_keys("Moshik1!")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    alert = driver.switch_to.alert
    alert_message = alert.text
    time.sleep(2)
    alert.accept()
    assert alert_message == "First name must be in English letters only"
    time.sleep(2)


"""
Suite 3 : Order

Functionalities :

    - 3.1 > Select 2 items from SVBurger menu and make an order
    - 3.2 > Unselect an item from SVBurger and reserve button becomes disabled
    - 3.3 > Log out button
    - 3.4 > Changing table number from 1 to 2
    - 3.5 > Changing quantity from 1 to 2

Error handling : 

    - 3.6 > Select 4 meals
    - 3.7 > Changing the quantity from 1 to 3
"""


def test_2_items(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Kids Meal"]').click()
    reserve = driver.find_element(By.XPATH, '//button[text() = " Reserve "]')
    driver.execute_script("arguments[0].scrollIntoView(true);", reserve)
    time.sleep(1)
    reserve.click()
    driver.find_element(By.XPATH, '//button[text() = "Send"]').click()
    assert driver.find_element(By.XPATH, '//h3[text() = " Your order has been successfully received "]').is_displayed()
    time.sleep(2)


def test_disable_reserve(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    reserve = driver.find_element(By.XPATH, '//button[text() = " Reserve "]')
    driver.execute_script("arguments[0].scrollIntoView(true);", reserve)
    time.sleep(1)
    assert not reserve.is_enabled(), 'Button is not disabled'
    time.sleep(2)


def test_logout(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    logout = driver.find_element(By.XPATH, '//button[text() = " Log out "]')
    driver.execute_script("arguments[0].scrollIntoView(true);", logout)
    time.sleep(1)
    logout.click()
    current_url = driver.current_url
    assert current_url == 'https://svburger1.co.il/#/HomePage'
    time.sleep(2)


def test_changetableno(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    reserve = driver.find_element(By.XPATH, '//button[text() = " Reserve "]')
    driver.execute_script("arguments[0].scrollIntoView(true);", reserve)
    time.sleep(1)
    reserve.click()
    spinbox = driver.find_element(By.XPATH, '//div[@class = "col-6"]/input[@type = "number"]')
    time.sleep(1)
    spinbox.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text() = "Send"]').click()
    assert driver.find_element(By.XPATH, '//div/h3[2]').text == "Table No 2"
    time.sleep(2)


def test_change_quantity(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    reserve = driver.find_element(By.XPATH, '//button[text() = " Reserve "]')
    driver.execute_script("arguments[0].scrollIntoView(true);", reserve)
    time.sleep(1)
    reserve.click()
    spinbox = driver.find_element(By.XPATH, '//div[1]/input[@type = "number"]')
    time.sleep(1)
    spinbox.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text() = "Send"]').click()
    # Checks if it also takes the service amount which is 11.8$
    assert driver.find_element(By.XPATH, '//div/h2[1]').text == "Total: 129.8$"
    time.sleep(2)


def test_select_4_meals(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Kids Meal"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Burger"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Vegan"]').click()
    vegan_bg_color = driver.find_element(By.XPATH, '//div[4]/div[@class = "card text-center mb-3"]')
    vegan_bg_color.get_attribute("style")
    assert 'background-color: white' in vegan_bg_color.get_attribute(
        "style"), "Was able to select 4 meals from the menu!"
    time.sleep(2)


def test_change_quantity_1_to_3(setup):
    driver = setup
    driver.find_element(By.XPATH, '//button[text() = "Sign In"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your email"]').send_keys("omer18@gmail.com")
    driver.find_element(By.XPATH, '//input[@placeholder = "Enter your password"]').send_keys("Omermeni18")
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    driver.find_element(By.XPATH, '//h5[text() = "Combo Meal"]').click()
    reserve = driver.find_element(By.XPATH, '//button[text() = " Reserve "]')
    driver.execute_script("arguments[0].scrollIntoView(true);", reserve)
    time.sleep(1)
    reserve.click()
    spinbox = driver.find_element(By.XPATH, '//div[1]/input[@type = "number"]')
    time.sleep(1)
    spinbox.clear()
    spinbox.send_keys(
        "3")  # The arrows in the spinbox cant go higher than 2, however by not using the spinbox arrows and changing manually the value from 1 to 3 you can make an order
    time.sleep(1)
    send_btn = driver.find_element(By.XPATH, '//button[text() = "Send"]')
    driver.execute_script("arguments[0].click();", send_btn)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div/h3[contains(text(), "Your order has been successfully received")]')))
        print("SVBurger Summary message appeared, indicating that the test failed")
    except TimeoutException:
        print("SVBurger Summary message did not appear, indicating that the test passed.")
    assert not driver.find_element(By.XPATH,
                                   '//div/h3[1]').is_displayed(), "Was able to order 3 items of the same meal!"
    time.sleep(2)

