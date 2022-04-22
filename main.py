from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from config import TWITTER_USERNAME, TWITTER_PASSWORD

# Setting up Selenium

PROMISED_DOWN = 150
PROMISED_UP = 10

chrome_driver_path = "C:\Development\chromedriver.exe"


class InternetSpeedTwitterBot:

    def __init__(self):
        global TWITTER_PASSWORD, TWITTER_USERNAME
        self.up = 0
        self.down = 0
        self.user = TWITTER_USERNAME
        self.password = TWITTER_PASSWORD
        self.speedtest_endpoint = "https://www.speedtest.net/"
        self.twitter_endpoint = "https://www.twitter.com/"

        s = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=s)

    def get_internet_speed(self):
        self.driver.get(self.speedtest_endpoint)
        self.driver.maximize_window()
        time.sleep(2)
        speedtest_cookies_accept_button = self.driver.find_element(by=By.ID, value="_evidon-banner-acceptbutton")
        speedtest_cookies_accept_button.click()
        speedtest_start = self.driver.find_element(by=By.CSS_SELECTOR, value="a .start-text")
        speedtest_start.click()
        time.sleep(55)
        self.down = float(self.driver.find_element(by=By.CSS_SELECTOR, value=".download-speed").text)
        self.up = float(self.driver.find_element(by=By.CSS_SELECTOR, value=".upload-speed").text)


    def tweet_at_provider(self):
        self.driver.get(self.twitter_endpoint)
        self.driver.maximize_window()
        time.sleep(3)
        sign_in = self.driver.find_element(by=By.LINK_TEXT, value="Sign in")
        sign_in.click()
        time.sleep(2)
        username_input = self.driver.find_element(by=By.CSS_SELECTOR, value="input")
        username_input.send_keys(TWITTER_USERNAME)
        username_input.send_keys(Keys.ENTER)
        time.sleep(1)
        password_input = self.driver.find_element(by=By.CSS_SELECTOR, value="input[type='password']")
        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)
        tweet = f"Hey @TalkTalk why is my internet speed {self.down} down/{self.up} up when I pay for " \
                f"{PROMISED_DOWN} down/ {PROMISED_UP} up?"
        tweet_input = self.driver.find_element(by=By.CLASS_NAME, value="public-DraftStyleDefault-block")
        tweet_input.send_keys(tweet)
        send_tweet = self.driver.find_element(by=By.CSS_SELECTOR, value="div[data-testid='tweetButtonInline']")
        send_tweet.click()
        self.driver.quit()



bot = InternetSpeedTwitterBot()
bot.get_internet_speed()

if bot.up < PROMISED_UP or bot.down < PROMISED_DOWN:
    print(f"We got DL {bot.down}, UL {bot.up}. \nWe should be getting DL {PROMISED_DOWN}, UL {PROMISED_UP}")
    bot.tweet_at_provider()
