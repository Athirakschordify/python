from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

app = Flask(__name__)
CORS(app)

# Initialize an empty array to store fetched URLs
fetched_urls = []

@app.route('/scrape-linkedin', methods=['POST'])
def fetch_data():
    global fetched_urls  # Declare the fetched_urls array as global

    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required.'}), 400

    try:
        # Store the URL in the fetched_urls array
        fetched_urls.append(url)

        # Install the appropriate version of chromedriver if necessary
        chromedriver_autoinstaller.install()

        # Define the function to solve CAPTCHA manually
        def solve_captcha_manually():
            input("Please solve the CAPTCHA manually and press Enter when done.")

        # Use chromedriver for Selenium
        driver = webdriver.Chrome()

        # Navigate to the login page
        driver.get('https://www.linkedin.com/login')

        # Wait for the username and password fields to be visible
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'username')))
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))

        # Enter login credentials
        username_field.send_keys('ksathira5111997@gmail.com')
        password_field.send_keys('Athiraks@7560' + Keys.RETURN)  # Send Enter key to submit

        # Wait for the login process to complete and handle CAPTCHA if necessary
        try:
            WebDriverWait(driver, 10).until(EC.url_contains('linkedin.com/feed/'))
        except:
            solve_captcha_manually()  # Handle CAPTCHA manually if necessary

        names_list = []
        location_list = []

        for target_url in fetched_urls:
            driver.get(target_url)
            target_page_html = driver.page_source
            soup = BeautifulSoup(target_page_html, 'html.parser')
            app_aware_links = soup.find_all(class_='app-aware-link')
            href_list = []

            for link in app_aware_links:
                href = link.get('href')
                href_list.append(href)

            linkedin_urls = [url for url in href_list if 'https://www.linkedin.com/in/' in url]
            unique_linkedin_urls = list(set(linkedin_urls))

        for href in unique_linkedin_urls:
                driver.get(href)
                href_soup = BeautifulSoup(driver.page_source, 'html.parser')
                target_elements = href_soup.find_all(class_='text-heading-xlarge inline t-24 v-align-middle break-words')
                locations = href_soup.find_all(class_='oDgchkLYcwoOvtFsmaxlfGEbqngEfknEHHciheqKw mt2')
                for target_element in target_elements:
                    content = target_element.get_text(strip=True)
                    names_list.append(content)
                    # Append empty string if location is not found
                    location_tag = href_soup.find(class_='text-body-small inline t-black--light break-words')
                    location = location_tag.get_text(strip=True) if location_tag else ''
                    location_list.append(location)   

        # Create a DataFrame from the lists
        data = {
            'Name': names_list,
            'Location': location_list
        }

        df = pd.DataFrame(data)

        # Define the file path where you want to save the Excel file
        excel_file_path = 'linkedin_data.xlsx'

        # Save the DataFrame to an Excel file
        df.to_excel(excel_file_path, index=False)

        print(f"Data has been saved to {excel_file_path}")

        return jsonify({'message': 'LinkedIn data fetched successfully.'}), 200     

    except Exception as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
