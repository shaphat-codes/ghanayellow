from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import re
import time
import requests
import json

driver = webdriver.Chrome()
driver.get("https://www.ghanayello.com/browse-business-directory")
driver.implicitly_wait(1)
list_of_business_by_category = driver.find_elements(By.XPATH, "//ul")
list_of_business_by_category = list_of_business_by_category[2] if list_of_business_by_category else None
businesses = list_of_business_by_category.find_elements(By.TAG_NAME, "li")
list_of_business_names = [item.text for item in businesses]
# print(list_of_business_names)

formatted_category_names = []

for item in list_of_business_names:
    string_without_count = re.findall(r'[A-Za-z\s]+', item)
    category_name = ' '.join(string_without_count)
    category_name = category_name.lower()
    category_name = re.sub(r"\s+", "_", category_name)
    formatted_category_names.append(category_name)

failed_categories = []
companies = []

for category in formatted_category_names[26:]:
    if category == "cleaning_equipment_services":
        category = "cleaning_equipmentservices"
    elif category == "laundry_dry_cleaning":
        category = "dry_cleaning"
    elif category == "b_b":
        category= "B2B"
    elif category == "washing_machines_repairs":
        category_name = "washing-machines-repairs"
    else:
        # response = requests.get(f"https://www.ghanayello.com/category/{category}")
        # if response.status_code == 404:
        #     failed_categories.append(category)

        driver.get(f"https://www.ghanayello.com/category/{category}")
        try:
            # Find all name_heading elements with increased timeout
            name_heading = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "h4")))
        except TimeoutException:
            print("TimeoutException: Timed out waiting for elements.")        
        
        try:

            pages = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.pages_container")))
            page_numbers = []
        except TimeoutException:
            page_numbers = [1,2]
        if len(page_numbers) > 2:

            for page in pages:
                page_numbers.append(page.text)
            all_pages = page_numbers[0].split("\n")
            total_pages = all_pages[4]
            print("total", total_pages)
        else:
            total_pages = 1
        
    for i in range(1, int(total_pages) + 1):
        company_names = []
        company_descriptions = []
        company_addresses = []
        contact_numbers = []
        company_products = []

        driver.get(f"https://www.ghanayello.com/category/{category}/{i}")
        
        # Find all name_heading elements without waiting for visibility
        name_heading = driver.find_elements(By.TAG_NAME, "h4")

        for name in name_heading:
            try:
                company_names.append(name.text)
            except Exception as e:
                company_names.append("Unknown company")

        company_address = driver.find_elements(By.CLASS_NAME, "address")

        for address in company_address:
            try:

                company_addresses.append(address.text)
            except Exception as e:
                company_addresses.append("Uknown address")

        company_description = driver.find_elements(By.CLASS_NAME, "details")
        for description in company_description:
            try:
                if description.text:

                    company_descriptions.append(description.text)
                else:
                    company_descriptions.append("No description available")
            except Exception as e:
                company_descriptions.append("unknown description")

        # Fetch href values without waiting for visibility
        try:

            href_values = [name.find_element(By.TAG_NAME, "a").get_attribute("href") for name in name_heading]
        except Exception as e:
            href_values = []
        # Visit each href and collect phone numbers and products
        if len(href_values) > 0:

            for href_value in href_values:
                try:

                    driver.get(href_value)
                    
                    # Fetch phone numbers without waiting for visibility
                    try:
                        details = driver.find_elements(By.CSS_SELECTOR, "div.text.phone")
                        phone_numbers = [detail.text for detail in details]
                        contact_numbers.append(phone_numbers)
                    except Exception as e:
                        contact_numbers.append("None")
                    
                    # Fetch products without waiting for visibility
                    try:
                        products = driver.find_elements(By.CSS_SELECTOR, 'div.product:not(.employee)')
                        listed_products = [product.text for product in products]
                        company_products.append(listed_products)
                    except Exception as e:
                        company_products.append("None")
                except Exception as e:
                    contact_numbers.append("none")
                    company_products.append("none")
        else:
            contact_numbers.append("none")
            company_products.append("none")


        max_length = max(len(company_names), len(company_descriptions), len(company_addresses), len(contact_numbers), len(company_products))
        company_names += ["Unknown company"] * (max_length - len(company_names))
        company_descriptions += ["No description available"] * (max_length - len(company_descriptions))
        company_addresses += ["Unknown address"] * (max_length - len(company_addresses))
        contact_numbers += ["None"] * (max_length - len(contact_numbers))
        company_products += ["None"] * (max_length - len(company_products))

        if len(company_names) == len(company_addresses) == len(company_descriptions) == len(contact_numbers):
            for i in range(len(company_names)):
                company_info = {
                    "category": category,
                    "name": company_names[i],
                    "description": company_descriptions[i],
                    "address": company_addresses[i],
                    "contacts": contact_numbers[i],
                    "products": company_products[i]
                }
                companies.append(company_info)
        else:
            print("Error: Lengths of company names, addresses, contact numbers and descriptions are not consistent.")
        # driver.switch_to.window(driver.window_handles[1])  
        print("names", len(company_names))
        print("descriptions", len(company_descriptions))
        print("addresses", len(company_addresses))
        print("contact numbers", len(contact_numbers))
        print("products", len(company_products))
        # print(companies)
        
    with open(f'{category}.json', 'w') as json_file:
        json.dump(companies, json_file, indent=4)   
    print(companies)

