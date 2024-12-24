from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

    def scroll_down(self):
        """
        Simulates pressing the "Page Down" key multiple times to ensure all content is loaded.
        """
        for _ in range(5):  # Adjust the range depending on the length of the content
            self.driver.find_element(By.ID, "profileContainer").send_keys(Keys.PAGE_DOWN)
            time.sleep(1)  # Allow time for lazy-loaded content


    def crawl_page(self):

        profile_links = self.driver.find_elements(By.CLASS_NAME, 'profile-title')

        for link in profile_links:
            print("Profile Status".center(50, "-"))
            link.click()  # Click the link to open the modal/popup

            elements = self.driver.find_elements(By.CLASS_NAME, "profile-heading-content")
            print(f"Found {len(elements)} elements with class 'profile-heading-content'")

            # WebDriverWait(self.driver, 20).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.profile-heading-title h1.profile-title'))
            # )

            # Wait briefly to ensure the modal closes before clicking the next profile
            # time.sleep(5)

            # Scroll down the modal/pop-up to ensure all elements are loaded
            self.scroll_down()

            # Extract data from the modal/popup
            self.extract_profile_data()

            # Close the modal/popup after extracting the data
            close_button = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.details-close .icon-close"))
            )

            close_button.click()

            # Wait briefly to ensure the modal closes before clicking the next profile
            # time.sleep(1)

    def extract_profile_data(self):
        """
        Extracts and prints the data from an open profile modal/popup.
        """
        try:
            # Full Name
            profile_title = self.driver.find_element(By.CLASS_NAME, 'profile-title').text.strip()
            print("Profile Title:", profile_title)

            # Credentials/Titles
            profile_suffix = self.driver.find_element(By.CLASS_NAME, "profile-suffix-heading").text.strip()
            print("Profile Suffix:", profile_suffix)

            # Profile Photo URL
            profile_photo_element = self.driver.find_element(By.CLASS_NAME, "profile-photo")
            profile_photo_url = profile_photo_element.get_attribute("src") if profile_photo_element else "No Photo URL"
            print("Profile Photo URL:", profile_photo_url)

            # Psychology Today Profile URL
            profile_url = self.driver.current_url
            print("Profile URL:", profile_url)

            # License Number and Jurisdiction
            license_info_element = self.driver.find_element(By.CLASS_NAME, "primary-details")
            license_info = license_info_element.text.strip() if license_info_element else "No License Info"
            print("License Info:", license_info)

            # Verification Status
            try:
                verification_status_element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "verified-badge"))
                )
                verification_status = verification_status_element.text.strip()
            except:
                verification_status = "Not Verified"
            print("Verification Status:", verification_status)

            # Office Locations (All)
            try:
                office_locations = []
                address_elements = self.driver.find_elements(By.CLASS_NAME, "address-line")
                for elem in address_elements:
                    office_locations.append(elem.text.strip())
            except:
                office_locations = ["No Address Found"]
            print("Office Locations:", office_locations)
            
            # Scroll again if necessary to ensure all content is captured
            # self.scroll_down()

            # Virtual Session Availability
            try:
                availability_element = self.driver.find_element(By.CLASS_NAME, "at-a-glance_row--appointments-all")
                availability = availability_element.text.strip()
            except:
                availability = "No Availability Info"
            print("Virtual Session Availability:", availability)

            # Service Areas
            try:
                service_areas = []
                service_area_elements = self.driver.find_elements(By.CLASS_NAME, "nearby-areas .area-level")
                for elem in service_area_elements:
                    service_areas.append(elem.text.strip())
            except:
                service_areas = ["No Service Areas Found"]
            print("Service Areas:", service_areas)

            # Postal Codes Served
            try:
                postal_codes = []
                postal_code_elements = self.driver.find_elements(By.CSS_SELECTOR, ".nearby-areas .area-title")
                for elem in postal_code_elements:
                    postal_codes.append(elem.text.strip())
            except:
                postal_codes = ["No Postal Codes Found"]
            print("Postal Codes:", postal_codes)

            # Session Fees/Pricing
            try:
                fees_element = self.driver.find_element(By.CLASS_NAME, "fees")
                fees = fees_element.text.strip()
            except:
                fees = "No Session Fees Found"
            print("Session Fees:", fees)

            # Insurance Details
            try:
                insurance_element = self.driver.find_element(By.CLASS_NAME, "insurance")
                insurance_details = insurance_element.text.strip()
            except:
                insurance_details = "No Insurance Info"
            print("Insurance Details:", insurance_details)

            # Payment Methods
            try:
                payment_element = self.driver.find_element(By.CSS_SELECTOR, "[data-x='payment-methods']")
                payment_methods = payment_element.text.strip()
            except:
                payment_methods = "No Payment Methods Found"
            print("Payment Methods:", payment_methods)

            # Types of Sessions Offered
            try:
                types_of_sessions = []
                session_elements = self.driver.find_elements(By.CSS_SELECTOR, ".client-focus-description")
                for elem in session_elements:
                    types_of_sessions.append(elem.text.strip())
            except:
                types_of_sessions = ["No Types of Sessions Found"]
            print("Types of Sessions Offered:", types_of_sessions)

            # Specialties
            try:
                attribute_elements = self.driver.find_elements(By.CSS_SELECTOR, ".attribute_base")
                all_attributes = [elem.text.strip() for elem in attribute_elements]
            except:
                all_attributes = []
            print("Extracted Attributes:", all_attributes)

            # print("Specialties:", specialties)

            # Treatment Approaches/Modalities
            try:
                treatment_approaches = []
                approach_elements = self.driver.find_elements(By.CSS_SELECTOR, ".treatment-approach-attributes-section .attribute_base")
                for elem in approach_elements:
                    treatment_approaches.append(elem.text.strip())
            except:
                treatment_approaches = ["No Treatment Approaches Found"]
            print("Treatment Approaches:", treatment_approaches)

            # Client Focus (Ages, Groups)
            try:
                client_focus = []
                client_focus_elements = self.driver.find_elements(By.CLASS_NAME, "client-focus-description")
                for elem in client_focus_elements:
                    client_focus.append(elem.text.strip())
            except:
                client_focus = ["No Client Focus Found"]
            print("Client Focus:", client_focus)

            # Languages Offered
            try:
                languages = []
                language_elements = self.driver.find_elements(By.CLASS_NAME, "languages-offered")
                for elem in language_elements:
                    languages.append(elem.text.strip())
            except:
                languages = ["No Languages Found"]
            print("Languages Offered:", languages)

            # Qualifications and Educational Background
            try:
                qualifications_element = self.driver.find_element(By.CLASS_NAME, "qualifications")
                qualifications = qualifications_element.text.strip()
            except:
                qualifications = "No Qualifications Found"
            print("Qualifications:", qualifications)

            # Main Profile Description
            try:
                paragraph_element = self.driver.find_element(By.CLASS_NAME, "paragraph")
                paragraph_text = paragraph_element.text.strip()
            except:
                paragraph_text = "No Paragraph Found"
            print("Main Profile Description:", paragraph_text)

            # Specialized Sections/Boxes
            try:
                specialized_sections = []
                specialized_section_elements = self.driver.find_elements(By.CLASS_NAME, "specialized-section")
                for elem in specialized_section_elements:
                    specialized_sections.append(elem.text.strip())
            except:
                specialized_sections = ["No Specialized Sections Found"]
            print("Specialized Sections:", specialized_sections)

        except Exception as e:
            print("Error during data extraction:", e)


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