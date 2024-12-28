from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import os

'''
- Install all requirements
- Run the script

'''

class Scrapper:
    def __init__(self,url = "https://www.psychologytoday.com/us/therapists?search=ontario"):
        self.license_number= []
        self.fee= []
        self.insurance= []
        self.speciality = []
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.profile_title= []
        self.profle_suffix= []
        self.address = []
        self.availablity= []
        self.bio = []
        self.number = []
        self.image_url = []
        self.expetise= []
        self.cities= []
        self.countries = []
        self.zip = []
        self.neighboor = []
        self.age = []
        self.ethentisy= []
        self.thrapy_Way = []
        self.speak= []
        self.participants = []
        self.unique_index= []
        self.url_profile = []
        self.education= []
        columns = [
            "url",
            "profile_title",
            "profle_suffix",
            "address",
            "availablity",
            "bio",
            "number",
            "license_number",
            "image_url",
            "fee",
            "insurance",
            "expetise",
            "speciality",
            "cities",
            "countries",
            "zip",
            "neighboor",
            "age",
            "participants",
            "ethentisy",
            "thrapy_Way",
            "Education",
        ]

        self.df = pd.DataFrame(columns= columns)




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
            WebDriverWait(self.driver, 10)
            url = link.get_attribute("href")

            link.click()  # Click the link to open the modal/popup
            print("Profile Status".center(50, "-"))
            self.url_profile.append(url)
            print(self.url_profile)


            elements = self.driver.find_elements(By.CLASS_NAME, "profile-heading-content")
            WebDriverWait(self.driver,30)
            print(f"Found {len(elements)} elements with class 'profile-heading-content'")



            # Extract data from the modal/popup
            self.extract_profile_data()

            # Close the modal/popup after extracting the data
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.details-nav.details-close .icon-close'))
            )
            time.sleep(3)
            close_button.click()





    def extract_profile_data(self):
        """
        Extracts and prints the data from an open profile modal/popup.
        """


        try:
            # Extract main content from the modal

            WebDriverWait(self.driver,10)

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
            self.profile_title= profile_title
            self.profle_suffix= profile_suffix
            self.address= address


        except Exception as e:
            print("Error extracting profile heading data:", e)

        try:


            # Wait until the element with the given class name is present
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "at-a-glance_row--appointments-online"))
            )

            # Get the inner HTML of the element
            inner_html = element.get_attribute("innerHTML")

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(inner_html, "html.parser")

            # Extract the text content
            text_content = soup.get_text(strip=True)
            print("Avalabilty Text:", text_content)
            self.availablity = text_content

        except Exception as e:
            print("Error:", e)

        try:

            # Extract paragraph text
            WebDriverWait(self.driver, 10)
            span_element = self.driver.find_element(By.CLASS_NAME, 'paragraph')
            inner_html = span_element.get_attribute("innerHTML")
            paragraph_text = BeautifulSoup(inner_html, 'html.parser').get_text(strip=True)
            print("Paragraph:", paragraph_text)
            self.bio= paragraph_text

        except Exception:
            print("No paragraph found.")

        try:

            # Extract phone number
            WebDriverWait(self.driver, 10)
            phone_element = self.driver.find_element(By.CLASS_NAME, 'lets-connect-phone-number')
            phone_href = phone_element.get_attribute("href")
            phone_number = re.search(r'\+?\(?\d{3}\)?\s?-?\d{3}-\d{4}', phone_href)
            print("Extracted Phone Number:", phone_number.group() if phone_number else "No phone number found.")
            self.number= phone_number.group()

        except Exception:
            print("No phone number found.")

        try:

            # Find the element
            WebDriverWait(self.driver, 10)
            element = self.driver.find_element(By.CLASS_NAME, "primary-details")

            # Get the inner HTML content
            inner_html = element.get_attribute("innerHTML")

            # Parse the inner HTML using BeautifulSoup
            soup = BeautifulSoup(inner_html, "html.parser")

            # Get the text content from the parsed HTML
            text_content = soup.get_text(strip=True)  # `strip=True` removes leading/trailing spaces

            print("Licensed:", text_content)
            self.license_number= text_content

        except Exception as e:
            print("Nothing found:", e)
        try:

            # Wait until the element with class 'profile-photo clickable' is visible
            wait = WebDriverWait(self.driver, 10)
            image_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile-photo.clickable"))
            )

            # Get the image URL from the 'src' attribute
            image_url = image_element.get_attribute("src")
            print("Image URL:", image_url)
            self.image_url= image_url

        except Exception as e:
            print("Error:", e)




        try:

            WebDriverWait(self.driver, 10)

            text_content = self.extract_list_items("fees")
            print("Fees Text:", text_content)
            self.fee= text_content
        except Exception as e:
            print("Error:", e)

        try:

            #using method as class name was unique
            WebDriverWait(self.driver, 10)

            li = self.extract_list_items("insurance")
            print("Insurane Text:", li)
            self.insurance= li

        except Exception as e:
            print("Error:", e)
        try:
            WebDriverWait(self.driver, 10)

            main_div = self.driver.find_element("id", "specialty-attributes-section")

            # Get the outerHTML of the main div
            html = main_div.get_attribute("outerHTML")

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            # Extract "Top Specialties" <li> items
            specialties_group = soup.find('h3', string="Top Specialties").find_next('ul')
            specialties_list = [li.get_text(strip=True) for li in specialties_group.find_all('li')]

            # Extract "Expertise" <li> items
            expertise_group = soup.find('h3', string="Expertise").find_next('ul')
            expertise_list = [li.get_text(strip=True) for li in expertise_group.find_all('li')]

            # Print the results
            print("Top Specialties:", specialties_list)
            print("Expertise:", expertise_list)
            self.speciality= specialties_list
            self.expetise = expertise_list

        except Exception as e:
            print("Error:", e)

        try:
            WebDriverWait(self.driver, 10)
            main_div = self.driver.find_element("class name", "nearby-areas")

            # Get the outerHTML of the main div
            html = main_div.get_attribute("outerHTML")

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            # Extract all area-level sections (Cities, Counties, Zips, Neighborhoods)
            area_sections = soup.find_all('div', class_='area-level')

            # Loop through each section and extract data
            areas_data = {}
            for section in area_sections:
                # Get the title of the section (e.g., Cities, Counties, Zips, Neighborhoods)
                title = section.find('h3', class_='area-title').get_text(strip=True)

                # Find all <a> tags inside the <ul> for each section
                links = [a.get_text(strip=True) for a in section.find_all('a')]

                # Store the links in a dictionary with the section title
                areas_data[title] = links

            # Print the results
            i= 1
            for title, links in areas_data.items():

                print(f"{title}: {links}")
                if i==1:
                    self.cities = links
                if i==2:
                    self.countries= links
                if i==3:
                    self.zip= links
                if i==4:
                    self.neighboor= links
                i+=1

        except:
            print("Error Occured in Nearby Areas ")



        try:


            WebDriverWait(self.driver,10)  # Adjust wait time based on page loading speed

            # Step 4: Get the HTML source of the page
            html = self.driver.page_source

            # Step 5: Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Step 6: Initialize lists to store extracted values
            age_list = set()
            participants_list = set()
            speak_list = set()
            ethnicity_list = set()

            # Step 7: Extract Age section
            age_section = soup.find_all('h3', string="Age")
            for section in age_section:
                items = section.find_next('div').find_all('span', class_='client-focus-description')
                for item in items:
                    age_list.add(item.text.strip())

            # Step 8: Extract Participants section
            participants_section = soup.find_all('h3', string="Participants")
            for section in participants_section:
                items = section.find_next('div').find_all('span', class_='client-focus-description')
                for item in items:
                    participants_list.add(item.text.strip())

            # Step 9: Extract "I also speak" section
            speak_section = soup.find_all('h3', string="I also speak")
            for section in speak_section:
                items = section.find_next('div').find_all('span', class_='client-focus-description')
                for item in items:
                    speak_list.add(item.text.strip())

            # Step 10: Extract Ethnicity section
            ethnicity_section = soup.find_all('h3', string="Ethnicity")
            for section in ethnicity_section:
                items = section.find_next('div').find_all('span', class_='client-focus-description')
                for item in items:
                    ethnicity_list.add(item.text.strip())

            # Step 11: Close the browser after scraping

            # Step 12: Print or use the extracted data

            print("Age:", age_list)
            self.age = list(age_list)

            print("Participants:", participants_list)
            self.participants= list(participants_list)

            print("I also speak:", speak_list)
            self.speak.append([speak_list])
            print("Ethnicity:", ethnicity_list)
            self.ethentisy= list(ethnicity_list)


        except:
            print("No Client")

        try:
            # Step 1: Wait for the page to load and get the HTML source
            WebDriverWait(self.driver,10)  # Adjust wait time based on page loading speed
            html = self.driver.page_source

            # Step 2: Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Step 3: Find the div with the specific id
            treatment_section = soup.find('div', {'id': 'treatment-approach-attributes-section'})

            # Step 4: Find the 'Types of Therapy' section by checking the heading
            therapy_group = treatment_section.find('h3', string="Types of Therapy").find_next('ul',
                                                                                              class_='section-list')

            # Step 5: Extract all li elements and their text
            therapy_list = [li.get_text(strip=True) for li in therapy_group.find_all('li')]

            # Step 6: Print the list of extracted therapies
            print("Therapy Ways:", therapy_list)
            self.thrapy_Way= therapy_list


            #check to save only unique values



        except Exception as e:
            print("Error:", e)
        try:

            # Step 2: Locate the main div and its elements
            qualifications_div = self.driver.find_element(By.CLASS_NAME, "qualifications")
            qualification_elements = qualifications_div.find_elements(By.CLASS_NAME, "qualifications-element")

            # Step 3: Extract the inner HTML of each element
            inner_html_list = [element.get_attribute("innerHTML") for element in qualification_elements]
            education = []

            # Step 4: Process and print the text with Beautiful Soup
            print("Extracted Text from <li> Elements:")
            for idx, inner_html in enumerate(inner_html_list, 1):
                if idx==1:
                    continue
                soup = BeautifulSoup(inner_html, "html.parser")
                extracted_text = soup.get_text(strip=True)  # Get the clean text content
                education.append(extracted_text)
                print(f"LI {idx}: {extracted_text}\n")
            self.education = education


            if self.number not in self.unique_index:
                self.unique_index.append(self.number)
                self.df.loc[len(self.df)] = [self.url_profile, self.profile_title, self.profle_suffix, self.address, self.availablity,
                                             self.bio, self.number, self.license_number, self.image_url, self.fee,
                                             self.insurance, self.expetise, self.speciality, self.cities, self.countries,
                                             self.zip, self.neighboor, self.age, self.participants, self.ethentisy, self.thrapy_Way, self.education]

        except:
            print("No Qualification found ")

    def extract_list_items(self, class_name):
        # Find the insurance section using Selenium
        insurance_section = self.driver.find_element("class name", class_name)

        # Pass the inner HTML of the section to BeautifulSoup
        soup = BeautifulSoup(insurance_section.get_attribute('outerHTML'), 'html.parser')

        # Find all <li> elements within the <ul>
        li_elements = soup.find_all('li')


        # Extract text from each <li>
        items = [li.get_text(strip=True) for li in li_elements]
        return items
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



    def print_attributes(self):
        # Loop through all attributes of the class
        for attr, value in self.__dict__.items():
            # Print attribute name and its value
            print(f"{attr}: {value}")

    def save_to_csv(self):
        for col in self.df.columns:
            if self.df[col].apply(lambda x: isinstance(x, list)).any():
                self.df[col] = self.df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
        self.df.set_index("number", inplace= True)
        self.df = self.df[~self.df.index.duplicated(keep='first')]
        self.df.replace("set()", "Not Presented")
        self.df.reset_index(drop=False, inplace =True)


        output_path = "CSV Data Lake"
        os.makedirs(output_path, exist_ok=True)

        # Generate filename with current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data_{timestamp}.csv"
        # Create the full path for the file
        full_path = os.path.join(output_path, filename)

        # Save the DataFrame as CSV
        self.df.to_csv(full_path, index=False)
        print(f"DataFrame saved at: {full_path}")

    def save_to_json(self):
        output_path = "Json Data Lake"
        os.makedirs(output_path, exist_ok=True)

        # Generate filename with current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data_{timestamp}.json"

        # Create the full path for the file
        full_path = os.path.join(output_path, filename)

        # Save the DataFrame as a JSON file
        self.df.to_json(path_or_buf=full_path, orient="index", indent=4, force_ascii=False)
        print(f"DataFrame saved at: {full_path}")




if __name__ == "__main__":
    obj = Scrapper()
    try:
        obj.crawl()
    except:
        print("Finished")

    obj.df["url"] = obj.url_profile[:len(obj.df)]
    obj.save_to_csv()
    obj.save_to_json()