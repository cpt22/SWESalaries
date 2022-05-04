from common import *
import webdriver_manager.chrome
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException
from pynput.keyboard import Key, Controller
import re

# SOURCE = 'TEST'
SOURCE = 'glassdoor'

NUM_PAGES = 50
NUM_RECORDS = 800


# WHEN SELENIUM IS RUNNING, DON'T CLICK AROUND OTHER TABS, THIS WILL BREAK PROGRAM
def main():
    # Clean up old entries from running script
    deduplicate(SOURCE)

    # Initialize Driver
    url = 'https://www.glassdoor.com/Job/software-engineer-jobs-SRCH_KO0,17.htm'
    driver = webdriver.Chrome(webdriver_manager.chrome.ChromeDriverManager().install())
    driver.get(url)
    keyboard = Controller()

    keyboard.press(Key.esc)
    keyboard.release(Key.esc)

    num_pages_to_search = NUM_PAGES
    num_jobs_to_search = NUM_RECORDS
    num_pages_searched = 0
    num_jobs_searched = 0

    # extract the job data in "num_pages_to_search" pages
    while num_jobs_searched < num_jobs_to_search:
        # Each job
        jobs_on_page = driver.find_elements(By.CLASS_NAME, 'react-job-listing')
        sleep(2)
        for job_card in jobs_on_page:
            # sleep to load the info
            count = 0
            while count < 100:
                count += 1
                try:
                    job_card.click()
                    break
                except ElementClickInterceptedException:
                    keyboard.press(Key.esc)
                    keyboard.release(Key.esc)
                    sleep(0.1)
                except StaleElementReferenceException:
                    sleep(0.1)
                # keyboard.press(Key.esc)
                # keyboard.release(Key.esc)

            if count >= 100:
                continue

            count = 0
            sleep(1)
            while count < 25:
                try:
                    driver.find_element(By.CLASS_NAME, 'jobDescriptionContent')
                    break
                except Exception:
                    sleep(0.1)
                    count += 1

            # Continue to next card if there was an issue loading one
            if count >= 25:
                continue

            try:
                if process(driver):
                    num_jobs_searched += 1
                print(f"Jobs Searched: {num_jobs_searched}")
            except Exception as ex:
                print(f'There was an error: {str(ex)}')

        sleep(1)
        # keyboard.press(Key.esc)
        # keyboard.release(Key.esc)
        # keyboard.press(Key.esc)
        # keyboard.release(Key.esc)
        #
        # try:
        #     if process(driver):
        #         num_jobs_searched += 1
        #         print(f"Jobs Searched: {num_jobs_searched}")
        # except Exception as ex:
        #     print(f'There was an error: {str(ex)}')

        # num_pages_searched += 1
        # if num_pages_searched == num_pages_to_search:
        #     print("Finished Searching.")

        # go to next page
        driver.find_element(By.CLASS_NAME, 'nextButton').click()
        sleep(5)

    deduplicate(SOURCE)
    print("Finished searching")


def process(driver):
    job_description = driver.find_element(By.CLASS_NAME,
                                          'jobDescriptionContent').text.lower()  # THIS IS JOB DESCRIPTION
    techs = extract_technologies(
        job_description)
    salary = process_salary(driver)
    company = process_company(driver, driver.find_element(By.CLASS_NAME, 'css-xuk5ye').text)
    title = driver.find_element(By.CLASS_NAME, 'css-1j389vi').text
    location = driver.find_element(By.CLASS_NAME, 'css-56kyx5').text
    location = None if location == "" else location
    return save_data({'company': company, 'salary': salary, 'position': title, 'technologies': techs,
                      'location': location}, source=SOURCE)


# Used to get the name of Job company without star ratings
def process_company(driver, company):
    try:
        if driver.find_element(By.CLASS_NAME, 'css-1m5m32b') is not None:
            return company[0:-4]
    except NoSuchElementException:
        return company


# $70,000 /yr (est.) => 70000
# $35 /hr (est.) => 35*52*40
def process_salary(driver):
    try:
        salary = driver.find_element(By.CLASS_NAME, 'css-y2jiyn').text
        new_salary = salary.split(' ', 1)
        if new_salary[1] == '/yr (est.)':
            return float(re.sub(r'[^\d.]', "", new_salary[0][1:]))
        else:
            return str(float(new_salary[0][1:]) * 52 * 40)
    except NoSuchElementException:
        return None


# Run my main program
if __name__ == "__main__":
    main()

# %%
