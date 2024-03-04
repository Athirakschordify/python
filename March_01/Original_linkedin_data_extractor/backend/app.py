from flask import Flask, jsonify, request, send_file, make_response  # Import send_file and make_response
from flask_cors import CORS
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

@app.route('/scrape-linkedin', methods=['POST'])
def fetch_data():
    data = request.json
    url = data.get('url')
    page_number = data.get('pageNumber')

    if not url or not page_number:
        return jsonify({'error': 'URL and pageNumber parameters are required.'}), 400

    try:
        chromedriver_autoinstaller.install()

        def solve_captcha_manually():
            input("Please solve the CAPTCHA manually and press Enter when done.")

        driver = webdriver.Chrome()
        driver.get('https://www.linkedin.com/login')
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'username')))
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
        username_field.send_keys('ksathira5111997@gmail.com')
        password_field.send_keys('Athiraks@7560' + Keys.RETURN)
        try:
            WebDriverWait(driver, 10).until(EC.url_contains('linkedin.com/feed/'))
        except:
            solve_captcha_manually()

        updated_urls = []

        for page_num in range(1, int(page_number) + 1):
            parsed_url = urlparse(url)
            query_parameters = parse_qs(parsed_url.query)
            query_parameters['page'] = [str(page_num)]
            query_parameters['sid'] = ['663']
            updated_query_string = urlencode(query_parameters, doseq=True)
            updated_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query_string, parsed_url.fragment))
            updated_urls.append(updated_url)
        
        linkedin_profiles = []
        names_list = []
        location_list = []

        for url in updated_urls:
            driver.get(url)
            target_page_html = driver.page_source
            soup = BeautifulSoup(target_page_html, 'html.parser')
            app_aware_links = soup.find_all(class_='app-aware-link')
            href_list = []

            for link in app_aware_links:
                href = link.get('href')
                href_list.append(href)

            linkedin_urls = [url for url in href_list if 'https://www.linkedin.com/in/' in url]
            unique_linkedin_urls = list(set(linkedin_urls))
            linkedin_profiles.extend(unique_linkedin_urls)

        for href in linkedin_profiles:
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

        # Return the file for download
        return send_file(excel_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
