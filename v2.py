from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
import re
import time
import requests
import json

driver = webdriver.Chrome()
driver.get("https://www.ghanayello.com/")
total_companies = 46590


company_names = []
company_descriptions = []
company_addresses = []
contact_numbers = []
company_products = []
company_websites = []
establishment_years = []
employees = []
vat_registration = []
registration_code = []
company_manager = []
company_employees = []
company_categories = []
company_tags = []


companies = []
counter = 0
for i in range(1, total_companies+1):
    print(counter, "/", total_companies)
    url = f"https://www.ghanayello.com/company/{i}"
    try:
        response = requests.head(url)
        # print(response.status_code)

        if response.status_code == 301:
            # If the response status code is 200 (OK), proceed with scraping
            driver.get(url)
            
            try:
                name = driver.find_element(By.TAG_NAME, "h1")
                company_names.append(name.text)
            except TimeoutException:
                company_names.append("unkwown company")

            try:
                address = driver.find_element(By.CSS_SELECTOR, "div.text.location")
                company_addresses.append(address.text)
            except NoSuchElementException:
                company_addresses.append("unkwown company")

            try:
                description = driver.find_element(By.CSS_SELECTOR, "div.text.desc")
                company_descriptions.append(description.text)
            except TimeoutException:
                company_descriptions.append("unkwown company")

            phone_number_pattern = re.compile(r'\b(?:\+\d{1,3}\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
            details = driver.find_elements(By.CSS_SELECTOR, "div.text")
            phone_numbers = []
            for detail in details:
                text = detail.text
                
                matches = phone_number_pattern.findall(text)
                
                if matches:
                    phone_numbers.extend(matches)

            if not phone_numbers:
                contact_numbers.append("None")
            else:
                contact_numbers.append(phone_numbers)

            try:
                website = driver.find_element(By.CSS_SELECTOR, "div.text.weblinks")
                company_websites.append(website.text)
                # print(website.text)
            except NoSuchElementException:
                company_websites.append("unkwown website")
            
            info_divs = driver.find_elements(By.CLASS_NAME, "info")

            for div in info_divs:
                managers = []
                # Extract the text from the div
                div_text = div.text
                
                # Check if the div contains the text "Company manager"
                if "Company manager" in div_text:
                    # Split the text by the span's text ("Company manager") and get the second part
                    manager_name = div_text.split("Company manager")[1].strip()
                    
                    # Print or use the extracted manager name
                    managers.append(manager_name)
                    break
            if len(managers) < 1:
                company_manager.append(["unkown manager"])
            else:
                company_manager.append(managers)
            

            for div in info_divs:
                years = []
                # Extract the text from the div
                div_text = div.text
                
                # Check if the div contains the text "Company manager"
                if "Establishment year" in div_text:
                    # Split the text by the span's text ("Company manager") and get the second part
                    year = div_text.split("Establishment year")[1].strip()
                    
                    # Print or use the extracted manager name
                    years.append(year)
                    break
            if len(years) < 1:
                establishment_years.append(["unkown year"])
            else:
                establishment_years.append(years)
            # print(years)


            for div in info_divs:
                codes = []
                # Extract the text from the div
                div_text = div.text
                
                # Check if the div contains the text "Company manager"
                if "Registration code" in div_text:
                    # Split the text by the span's text ("Company manager") and get the second part
                    code = div_text.split("Registration code")[1].strip()
                    
                    # Print or use the extracted manager name
                    codes.append(code)
                    break
            if len(codes) < 1:
                registration_code.append(["unknown code"])
            else:
                registration_code.append(codes)
            # print(codes)



            for div in info_divs:
                vats = []
                # Extract the text from the div
                div_text = div.text
                
                # Check if the div contains the text "Company manager"
                if "VAT registration" in div_text:
                    # Split the text by the span's text ("Company manager") and get the second part
                    vat = div_text.split("VAT registration")[1].strip()
                    
                    # Print or use the extracted manager name
                    vats.append(vat)
                    break
            if len(codes) < 1:
                vat_registration.append(["unknown VAT"])
            else:
                vat_registration.append(vat)
            # print(vats)


            try:
                products = driver.find_elements(By.CSS_SELECTOR, 'div.product:not(.employee)')
                listed_products = [product.text for product in products]
                company_products.append(listed_products)
                # print(listed_products)
            except Exception as e:
                company_products.append("None")
            

            try:
                employees = driver.find_elements(By.CSS_SELECTOR, 'div.product.employee')
                listed_employees = [employee.text for employee in employees]
                company_employees.append(listed_employees)
                # print(listed_employees)
            except Exception as e:
                company_employees.append("None")
            


            try:
                categories = driver.find_elements(By.CSS_SELECTOR, 'div.categories')
                listed_categories = [category.text for category in categories]
                company_categories.append(listed_categories)
                # print(listed_categories)
            except Exception as e:
                company_categories.append("None")

            

            try:
                tags = driver.find_elements(By.CSS_SELECTOR, 'div.tags2')
                listed_tags = [tag.text for tag in tags]
                company_tags.append(listed_tags)
                # print(listed_tags)
            except Exception as e:
                company_tags.append("None")

            counter += 1
        else:
            print("url is not correct")
    except Exception as e:
        # Handle other exceptions if necessary
        print("An error occurred:", e)

if len(company_names) == len(company_descriptions) == len(company_addresses) == len(contact_numbers) == len(company_products) == len(company_websites) == len(establishment_years) == len(vat_registration) == len(registration_code) == len(company_manager) == len(company_employees) == len(company_categories) == len(company_tags):
    for i in range(len(company_names)):
        company_info = {
            "name": company_names[i],
            "description": company_descriptions[i],
            "address": company_addresses[i],
            "contacts": contact_numbers[i],
            "products": company_products[i],
            "website": company_websites[i],
            "establishment_year": establishment_years[i],
            "vat_registration": vat_registration[i],
            "registration_code": registration_code[i],
            "company_manager": company_manager[i],
            "company_employees": company_employees[i],
            "company_tags": company_tags[i],
            "listed_categories": company_categories[i]
        }
        companies.append(company_info)
        
else:
    print("Error: Lengths of company names, addresses, contact numbers and descriptions are not consistent.")

# print(companies)
with open(f'data.json', 'w') as json_file:
    json.dump(companies, json_file, indent=4)   
    
        
    