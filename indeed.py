from common import *
import webdriver_manager.chrome
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from pynput.keyboard import Key, Controller
import re

SOURCE = 'TEST'
# SOURCE = 'indeed'

NUM_PAGES = 2


def main():
    # Clean up old entries from running script
    c.execute(f"DELETE FROM positions WHERE source='{SOURCE}'")

    # Initialize Driver
    url = 'https://www.indeed.com/jobs?q=software%20engineer'
    driver = webdriver.Chrome(webdriver_manager.chrome.ChromeDriverManager().install())
    driver.get(url)
    keyboard = Controller()

    keyboard.press(Key.esc)
    keyboard.release(Key.esc)

    num_pages_to_search = NUM_PAGES
    num_pages_searched = 0
    num_jobs_searched = 0

    # extract the job data in "num_pages_to_search" pages
    while num_pages_searched < num_pages_to_search:
        # Each job
        jobs_on_page = driver.find_elements(By.CLASS_NAME, 'cardOutline')

        for job_card in jobs_on_page:
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            sleep(0.5)

            job_card.click()
            sleep(3)


if __name__ == "__main__":
    main()
