from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup


'''
- Install all requirements
- Run the script

'''

class scrapper:
    def __init__(self,url = "https://www.psychologytoday.com/us/therapists?search=ontario"):
        self.driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
    def crawl(self):
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
        # Iterate over the found links and print them

        for link in profile_links:
            print("Profile Status".center(50,"-"))
            link.click()
            link_url = link.get_attribute("href")

            # Print the extracted link
            print("Extracted Link:", link_url)
            print("Name:",link.text)
            div_element = self.driver.find_element(By.CLASS_NAME, "profile-heading-content")

            # Extract inner HTML
            inner_html = div_element.get_attribute("innerHTML")
            soup = BeautifulSoup(inner_html, 'html.parser')

            # Extract the desired text
            profile_title = soup.find("h1", class_="profile-title").get_text(strip=True)  # Extract h1 text
            profile_suffix = soup.find("h2", class_="profile-suffix-heading").get_text(strip=True)  # Extract h2 text
            address = soup.find("span", class_="address-region").get_text(strip=True)  # Extract address

            # Print the extracted text
            print("Profile Title:", profile_title)
            print("Profile Suffix:", profile_suffix)
            print("Address:", address)
            span_element = self.driver.find_element(By.CLASS_NAME, 'paragraph')

            # Get the inner HTML of the <span> element
            inner_html = span_element.get_attribute("innerHTML")

            # Parse the inner HTML with BeautifulSoup
            soup = BeautifulSoup(inner_html, 'html.parser')

            # Extract the text content from the <span> element
            paragraph_text = soup.get_text(strip=True)

            # Print the extracted paragraph text
            print("Paragraph:", paragraph_text)
            phone_element = self.driver.find_element(By.CLASS_NAME, 'lets-connect-phone-number')

            # Get the 'href' attribute which contains the phone number in the 'tel:' format
            phone_href = phone_element.get_attribute("href")

            # Extract the phone number from the href string (remove 'tel:' part)
            phone_number = re.search(r'\+?\(?\d{3}\)?\s?-?\d{3}-\d{4}', phone_href)

            # If a phone number is found, print it
            if phone_number:
                print("Extracted Phone Number:", phone_number.group())
            else:
                print("No phone number found.")



            # Print the extracted text
            wait = WebDriverWait(self.driver, 10)
            #close the button
            close_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.details-nav.details-close .icon-close')))

            close_button.click()






obj = scrapper()
obj.crawl()

