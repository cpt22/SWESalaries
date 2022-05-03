from common import *
import webdriver_manager.chrome
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from pynput.keyboard import Key, Controller
from selenium.webdriver.support import expected_conditions as EC
import re

SOURCE = 'TEST'
# SOURCE = 'indeed'

NUM_PAGES = 1
SEARCH_TIMEOUT = 4


def main():
    # Clean up old entries from running script
    c.execute(f"DELETE FROM positions WHERE source='{SOURCE}'")

    # Initialize Driver
    url = 'https://www.indeed.com/jobs?q=software%20engineer'
    driver = webdriver.Chrome(webdriver_manager.chrome.ChromeDriverManager().install())
    driver.get(url)
    keyboard = Controller()
    driver.implicitly_wait(SEARCH_TIMEOUT)

    keyboard.press(Key.esc)
    keyboard.release(Key.esc)

    num_pages_to_search = NUM_PAGES
    num_pages_searched = 0
    num_jobs_searched = 0

    # extract the job data in "num_pages_to_search" pages
    while True:
        # Each job
        jobs_on_page = driver.find_elements(By.CLASS_NAME, 'tapItem')

        for job_card in jobs_on_page:
            job_card.click()
            sleep(1.5)
            # keyboard.press(Key.esc)
            # keyboard.release(Key.esc)
            # keyboard.press(Key.esc)
            # keyboard.release(Key.esc)
            # sleep(0.25)
            try:
                process(driver, job_card)
                num_jobs_searched += 1
            except Exception as ex:
                print(f'There was an error: {str(ex)}')
            finally:
                driver.switch_to.parent_frame()

        num_pages_searched += 1

        if num_pages_searched >= num_pages_to_search:
            break
        else:
            driver.find_element(By.CSS_SELECTOR, '[aria-label=Next]').click()
            sleep(5)


def process(driver, job_card):
    salary = process_salary(driver, job_card)
    driver.switch_to.frame("vjs-container-iframe")
    element = driver.find_element(By.ID, 'viewJobSSRRoot')
    job_description = element.find_element(By.ID, 'jobDescriptionText').text.lower()
    rating_section = element.find_element(By.CLASS_NAME, 'jobsearch-InlineCompanyRating')
    techs = extract_technologies(job_description)
    title = element.find_element(By.CLASS_NAME, 'jobsearch-JobInfoHeader-title').text.split('\n')[0]
    print(salary)


def process_company_name(section):
    return ''


def process_salary(driver, section):
    salary_text = ''
    driver.implicitly_wait(0)
    try:
        salary_text = section.find_element(By.CLASS_NAME, 'salary-snippet-container').text
    except NoSuchElementException:
        try:
            salary_text = section.find_element(By.CLASS_NAME, 'estimated-salary').text
        except NoSuchElementException:
            return None
    finally:
        driver.implicitly_wait(SEARCH_TIMEOUT)
        salary = None
        sals = re.findall(r'\$?\d{1,3}.?\d?K|\$?\d{0,3},?\d{0,3},?\d{2,3}(?:.\d{1,2})?', salary_text)
        if len(sals) < 1:
            return salary
        if re.match(r'\$?[\d.,]*K', sals[0]):
            components = list(map(lambda x: float(re.sub(r'[^\d.]', "", x)) * 1000, sals))
        else:
            components = list(map(lambda x: float(re.sub("[^\d.]", "", x)), sals))

        if 'year' in salary_text:
            salary = sum(components) / len(components)
        elif 'month' in salary_text:
            salary = 12 * (sum(components) / len(components))
        elif 'day' in salary_text:
            salary = 52 * 5 * (sum(components) / len(components))
        elif 'hour' in salary_text:
            salary = 52 * 40 * (sum(components) / len(components))

        return salary


if __name__ == "__main__":
    main()
