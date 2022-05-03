import webdriver_manager.chrome
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from pynput.keyboard import Key, Controller
from common import *

SOURCE = 'TEST'
# SOURCE = 'linkedin'


# WHEN SELENIUM IS RUNNING, DON'T CLICK AROUND OTHER TABS, THIS WILL BREAK PROGRAM
def main():
    # Clean up old entries from running script
    c.execute(f"DELETE FROM positions WHERE source='{SOURCE}'")

    # Initialize Driver
    url = 'https://www.linkedin.com/jobs/search/?keywords=software%20engineer'
    driver = webdriver.Chrome(webdriver_manager.chrome.ChromeDriverManager().install())
    driver.get(url)
    keyboard = Controller()

    load_more_jobs = 0
    num_jobs_to_search = 25
    num_jobs_searched_so_far = 0
    load_more_jobs_text = 'infinite-scroller__show-more-button infinite-scroller__show-more-button--visible'

    #
    while num_jobs_searched_so_far < num_jobs_to_search:
        # Each job
        job_list = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')
        for i in range(num_jobs_searched_so_far, len(job_list)):
            job_list[i].click()
            sleep(3)  # CHANGE THIS TO MAKE IT CLICK ON NEXT PAGE FASTER. CAREFUL IF THE PAGE DOESN'T LOAD THOUGH
            num_jobs_searched_so_far += 1

            # Try to load more jobs
            try:
                driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[2]/button').click()  # Load More Jobs
                sleep(2)
            # If not possible, then get the current job
            except ElementNotInteractableException:
                try:
                    # Get salary stuff
                    num_jobs_searched_so_far += 1
                    company = driver.find_element(By.CLASS_NAME, 'topcard__org-name-link').text
                    company = company if company else None
                    job_position = driver.find_element(By.CLASS_NAME, 'top-card-layout__title').text
                    location = driver.find_element(By.XPATH,
                                                   '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[2]').text  # [8:-1] gets location
                    salary = process_linkedin_salary(driver)
                    job_description = driver.find_element(By.CLASS_NAME,
                                                          'show-more-less-html__markup').text  # Job Description
                    techs = extract_technologies(job_description)
                    print(
                        "Company: " + str(company) + ". Job Position: " + job_position + ". Location: " + location + ". Salary: " + str(
                            salary))
                    save_data({'company': company, 'salary': salary, 'position': job_position, 'technologies': techs,
                               'location': location}, source=SOURCE)
                except NoSuchElementException as ex:
                    print(f'There was an error: {str(ex)}')
        # Load more jobs by pressing space
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        sleep(2)
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        sleep(2)

    print("Finished searching")


# Helper function to extract programming languages from the job description text
def extract_languages(job_description):
    return


# Used to get the name of Job company without star ratings
def process_company(driver, company):
    try:
        if driver.find_element(By.CLASS_NAME, 'css-1m5m32b') is not None:
            return company[0:-4]
    except NoSuchElementException:
        return company


# Function specific to LinkedIn, don't try to use for glassdoor
# $123,000.00/yr - $180,000.00/yr ==> Becomes avg
def process_linkedin_salary(driver):
    try:
        salary = driver.find_element(By.XPATH,
                                     '/html/body/div[1]/div/section/div[2]/div[1]/section[1]/div/div/div').text
        output = re.findall(r'\d+', salary)

        # Sometimes it falsly reads salaries. If there are no numbers, throw error
        if len(output) <= 3:
            raise NoSuchElementException('No Salary')
        # output is now [123, 000, 00, 180, 000, 00] from example

        # Output is sometimes 4 elements long, ex: $123,000/yr - 180,000/yr  --> No decimal places
        # Check if output has decimal places or not
        if len(output) == 6:
            # combine first two elements for min pay, combine 4th and 5th elements for max pay
            min_pay = int(output[0] + output[1])
            max_pay = int(output[3] + output[4])
            return int((min_pay + max_pay) / 2)
        # Or not -> output is [123, 000, 180, 000]
        min_pay = int(output[0] + output[1])
        max_pay = int(output[2] + output[3])
        return int((min_pay + max_pay) / 2)
    except NoSuchElementException:
        return None


if __name__ == "__main__":
    # Run my main program
    main()

#%%
