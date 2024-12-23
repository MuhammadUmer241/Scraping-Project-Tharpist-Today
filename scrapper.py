from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import time


'''
- Install all requirements
- Run the script

'''

class Scrapper:
    def __init__(self,url = "https://www.psychologytoday.com/us/therapists?search=ontario"):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def crawl_page(self):
        """
            Crawls through profile links on a webpage, extracts relevant information from each profile,
            and prints the extracted data.
            It only scrape the data from visible one page you need to add functionality to switch profile in order
            to scrape more

            This method performs the following steps:
            1. Finds all profile links by their class name (`profile-title`).
            2. For each profile link:
                - Clicks the link to navigate to the profile page.
                - Extracts and prints the URL of the profile.
                - Extracts and prints the profile title, suffix, and address by parsing the inner HTML of the profile's content section.
                - Extracts and prints the paragraph text from a specific section.
                - Extracts and prints the phone number from the `tel:` link (if available).
                - Closes the profile page after extraction.

            The method uses Selenium for web scraping and BeautifulSoup to parse HTML content.

            Attributes:
                self.driver: A Selenium WebDriver instance used to interact with the web page.

            Returns:
                None. Prints the extracted data to the console.

            Example:
                crawler = scrapper()
                crawler.crawl()
            """

        profile_links = self.driver.find_elements(By.CLASS_NAME, 'profile-title')

        for link in profile_links:
            print("Profile Status".center(50, "-"))
            link.click()  # Click the link to open the modal/popup

            elements = self.driver.find_elements(By.CLASS_NAME, "profile-heading-content")
            print(f"Found {len(elements)} elements with class 'profile-heading-content'")

            # WebDriverWait(self.driver, 20).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-container .profile-heading-content'))
            # )


            # Extract data from the modal/popup
            self.extract_profile_data()

            # Close the modal/popup after extracting the data
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.details-nav.details-close .icon-close'))
            )
            close_button.click()

            # Wait briefly to ensure the modal closes before clicking the next profile
            # time.sleep(2)

    def extract_profile_data(self):
        """
        Extracts and prints the data from an open profile modal/popup.
        """
        try:
            # Extract main content from the modal
            div_element = self.driver.find_element(By.CLASS_NAME, "profile-heading-content")
            inner_html = div_element.get_attribute("innerHTML")
            soup = BeautifulSoup(inner_html, 'html.parser')

            # Extract the desired text
            profile_title = soup.find("h1", class_="profile-title").get_text(strip=True)
            profile_suffix = soup.find("h2", class_="profile-suffix-heading").get_text(strip=True)
            address = soup.find("span", class_="address-region").get_text(strip=True)

            print("Profile Title:", profile_title)
            print("Profile Suffix:", profile_suffix)
            print("Address:", address)
        except Exception as e:
            print("Error extracting profile heading data:", e)

        try:
            # Extract paragraph text
            span_element = self.driver.find_element(By.CLASS_NAME, 'paragraph')
            inner_html = span_element.get_attribute("innerHTML")
            paragraph_text = BeautifulSoup(inner_html, 'html.parser').get_text(strip=True)
            print("Paragraph:", paragraph_text)
        except Exception:
            print("No paragraph found.")

        try:
            # Extract phone number
            phone_element = self.driver.find_element(By.CLASS_NAME, 'lets-connect-phone-number')
            phone_href = phone_element.get_attribute("href")
            phone_number = re.search(r'\+?\(?\d{3}\)?\s?-?\d{3}-\d{4}', phone_href)
            print("Extracted Phone Number:", phone_number.group() if phone_number else "No phone number found.")
        except Exception:
            print("No phone number found.")


    def go_to_next_page(self):
        """
        Clicks on the 'Next' button to go to the next page.
        Returns True if the next page exists, otherwise False.
        """
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.pagination-controls-end .chevron-right'))
            )
            next_button.click()
            time.sleep(3)  # Allow time for the next page to load
            return True
        except Exception:
            print("No more pages found.")
            return False

    def crawl(self):
        """
        Crawls all pages and extracts data from each profile.
        """
        while True:
            print("Scraping current page...")
            self.crawl_page()

            # Go to the next page, break if no more pages
            if not self.go_to_next_page():
                break

        self.driver.quit()


if __name__ == "__main__":
    obj = Scrapper()
    obj.crawl()