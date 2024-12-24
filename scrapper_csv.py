import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import time


class Scrapper:
    def __init__(self, url="https://www.psychologytoday.com/us/therapists?search=ontario"):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # Create and open the CSV file
        self.file_name = "Ontario_Therapists.csv"  # Dynamically set based on region if needed
        self.csv_file = open(self.file_name, mode="w", newline="", encoding="utf-8")
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=["Profile Title", "Profile Suffix", "Address", "Paragraph", "Phone Number"])
        self.csv_writer.writeheader()  # Write the header row

    def crawl_page(self):
        """
        Crawls through profile links on a webpage, extracts relevant information from each profile,
        and saves the extracted data into a CSV file.
        """
        profile_links = self.driver.find_elements(By.CLASS_NAME, 'profile-title')

        for link in profile_links:
            try:
                print("Profile Status".center(50, "-"))
                link.click()  # Click the link to open the modal/popup

                # Wait for the profile modal/popup to appear
                # WebDriverWait(self.driver, 20).until(
                #     EC.visibility_of_element_located((By.CLASS_NAME, "profile-heading-content"))
                # )

                # Extract data from the modal/popup
                profile_data = self.extract_profile_data()

                # Write the data to the CSV file
                if profile_data:
                    self.csv_writer.writerow(profile_data)

                # Close the modal/popup after extracting the data
                close_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.details-nav.details-close .icon-close'))
                )
                close_button.click()

                # Wait briefly to ensure the modal closes before clicking the next profile
                # time.sleep(2)
            except Exception as e:
                print(f"Error processing profile: {e}")

    def extract_profile_data(self):
        """
        Extracts and returns the data from an open profile modal/popup.
        """
        profile_data = {
            "Profile Title": "",
            "Profile Suffix": "",
            "Address": "",
            "Paragraph": "",
            "Phone Number": ""
        }

        try:
            # Extract main content from the modal
            div_element = self.driver.find_element(By.CLASS_NAME, "profile-heading-content")
            inner_html = div_element.get_attribute("innerHTML")
            soup = BeautifulSoup(inner_html, 'html.parser')

            # Extract the desired text
            profile_data["Profile Title"] = soup.find("h1", class_="profile-title").get_text(strip=True)
            profile_data["Profile Suffix"] = soup.find("h2", class_="profile-suffix-heading").get_text(strip=True)
            profile_data["Address"] = soup.find("span", class_="address-region").get_text(strip=True)
        except Exception as e:
            print("Error extracting profile heading data:", e)

        try:
            # Extract paragraph text
            span_element = self.driver.find_element(By.CLASS_NAME, 'paragraph')
            inner_html = span_element.get_attribute("innerHTML")
            profile_data["Paragraph"] = BeautifulSoup(inner_html, 'html.parser').get_text(strip=True)
        except Exception:
            print("No paragraph found.")

        try:
            # Extract phone number
            phone_element = self.driver.find_element(By.CLASS_NAME, 'lets-connect-phone-number')
            phone_href = phone_element.get_attribute("href")
            phone_number = re.search(r'\+?\(?\d{3}\)?\s?-?\d{3}-\d{4}', phone_href)
            profile_data["Phone Number"] = phone_number.group() if phone_number else "No phone number found."
        except Exception:
            print("No phone number found.")
        print(profile_data)
        return profile_data

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
        Crawls all pages, extracts data from each profile, and saves it into a CSV file.
        """
        try:
            while True:
                print("Scraping current page...")
                self.crawl_page()

                # Go to the next page, break if no more pages
                if not self.go_to_next_page():
                    break
        finally:
            # Ensure the driver and CSV file are properly closed
            self.driver.quit()
            self.csv_file.close()
            print(f"Scraping complete. Data saved to {self.file_name}")


if __name__ == "__main__":
    obj = Scrapper()
    obj.crawl()
