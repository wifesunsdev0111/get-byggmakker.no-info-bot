from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import requests
import quickstart
import re
from translate import Translator
import get_latitude_and_longitude



# Create a Translator object and translate the string
translator = Translator(to_lang="en")
driver = webdriver.Chrome()    
driver.maximize_window()
driver.get("https://www.byggmakker.no/kategori/trelast/terrassebord")


try:
    cookey_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"kc-acceptAndHide\"]"))).click()
except:
    pass

urls = []
while True:

    try:
       
        try:
            normal_urls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[class=\"product-card  ab_omni_kampaign\"]")))
            for url_tag in normal_urls:
                url = url_tag.get_attribute("href")
                urls.append(url)
        except:
            normal_urls = []
        print(f'normal urls = ', len(normal_urls))
        
        try:
            regular_urls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[class=\"product-card  ab_omni_regular\"]")))
            for url_tag in regular_urls:
                url = url_tag.get_attribute("href")
                urls.append(url)
        except:
            regular_urls = []
        print(f'reguar urls = ', len(regular_urls))
        
        next_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"pagination__next\"]")))
        driver.execute_script("arguments[0].scrollIntoView(false); window.scrollBy(0, 0);", next_page)
        sleep(5)
        print(f'Select products url count = ', len(urls), len(normal_urls), len(regular_urls))
        next_page.click()
        sleep(5)
    except:
        driver.quit()
        break

product_driver = webdriver.Chrome()    
product_driver.maximize_window()
for index, url in enumerate(urls):
    try:
        product_driver.get(url)
        print(f'Select products url count = ', len(urls), index)
        if index == 0:
            try:
                cookey_button = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"kc-acceptAndHide\"]"))).click()
            except:
                pass

        product_page_info = WebDriverWait(product_driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"product-page__info-section\"]")))

        product_name = product_page_info.find_element(By.CSS_SELECTOR, "h1[class=\"product-heading__product-name \"]").text
        print(f'Product name = ', product_name)

        try:
            product_price = product_page_info.find_element(By.CSS_SELECTOR, "div[class=\"price-view__sale-price-container__internal\"]").text
        except:
            product_price = ""
            pass
        print(f'product_price = ', product_price)
        
        try:
            product_advantage = product_page_info.find_element(By.CSS_SELECTOR, "div[class=\"product-advantages\"]").text
        except:
            product_advantage = ""
            pass
        print(f'product_advantage = ', product_advantage)

        try:
            product_imgs_body = WebDriverWait(product_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"product-images-and-videos__thumbnails\"]")))
            product_imags = product_imgs_body.find_elements(By.TAG_NAME, "img")
            print(f'img length = ', len(product_imags))
            img_urls_first = []
            for img in product_imags:
                img_url = img.get_attribute("src")
                img_urls_first.append(img_url)
            
            img_urls = ",".join(img_urls_first)
        except:
            pass
        print(f'img_urls = ', img_urls)

        product_info_tab = WebDriverWait(product_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"product-info__wrapper--tabs-container\"]")))
        product_driver.execute_script("arguments[0].scrollIntoView(false); window.scrollBy(0, 0);", product_info_tab)

        WebDriverWait(product_info_tab, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"tab-heading tab-heading__description tab-heading--active\"]"))).click()

        try:
            prodcut_description_body = WebDriverWait(product_info_tab, 10).until(EC.presence_of_element_located(((By.CSS_SELECTOR, "div[class=\"product-info__main-content\"]"))))
        except:
            prodcut_description_body = WebDriverWait(product_info_tab, 10).until(EC.presence_of_element_located(((By.CSS_SELECTOR, "div[class=\"product-info__main-content hidden\"]"))))
            pass

        product_code_body_main = product_info_tab.find_element(By.CSS_SELECTOR, "ul[class=\"article-numbers reset-style\"]")

        product_code_body = product_code_body_main.find_elements(By.XPATH, "./*")
        print(f'product_code_body lenght = ', len(product_code_body))

        try:
            article_number_all = product_code_body[0].text
            article_number_exact = article_number_all.split()
            article_number = article_number_exact[1].strip()
        except:
            article_number = ""
            pass
        print(f'article number = ', article_number)

        try:
            ena_number_all = product_code_body[1].text
            ena_number_exact = ena_number_all.split(":")
            ena_number = ena_number_exact[1].strip() 
        except:
            ena_number = ""
        print(f'ena number = ', ena_number)

        try:
            product_description = prodcut_description_body.find_element(By.CSS_SELECTOR, "div[class=\"product-description\"]").text
        except:
            product_description = ""
        print(f'product description = ', product_description)

        WebDriverWait(product_info_tab, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"tab-heading tab-heading__specifications\"]"))).click()

        product_attribute_body = product_info_tab.find_element(By.CSS_SELECTOR, "div[class=\"product-attributes__content\"]")

        product_attribute_contents = product_attribute_body.find_elements(By.XPATH, "./*")

        

        try:
            wood_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Treslag')]")
            wood_spices = wood_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            wood_spices = ""
            pass
        print(f"wood spices = ", wood_spices)

        try:
            modification_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Modifiseringsmetode')]")
            modification_method =  modification_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            modification_method = ""
            pass

        print(f'modification method = ', modification_method)

        try:
            with_bark_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Med bark')]")
            with_bark =  with_bark_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            with_bark = ""
            pass

        print(f' with_bark = ',  with_bark)


        try:
            dt_elem = product_driver.find_elements(By.TAG_NAME, "dt")
            for dt in dt_elem:
                if "Tykkelse (Millimetre)" == dt.text:
                    thickness_millimeters =  dt.find_element(By.XPATH, "./following-sibling::*[1]").text
                if "Bredde (Millimetre)" == dt.text:
                    widht_millimeters =  dt.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            thickness_millimeters = ""
            widht_millimeters = ""
            pass

        print(f'thickness_millimeters = ', thickness_millimeters)
        print(f'widht_millimeters = ', widht_millimeters)

        try:
            surface_treatment_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Overflatebearbeiding')]")
            surface_treatment =  surface_treatment_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            surface_treatment = ""
            pass

        print(f'surface_treatment = ', surface_treatment)

        try:
            number_of_processed_page_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Antall bearbeidede sider')]")
            number_of_processed_page =  number_of_processed_page_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            number_of_processed_page = ""
            pass

        print(f' number_of_processed_page = ',  number_of_processed_page)

        try:
            environment_certification_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Miljøsertifisering')]")
            environment_certification =  environment_certification_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            environment_certification = ""
            pass

        print(f'environment_certification = ', environment_certification)


        try:
            durability_class_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Holdbarhetsklasse')]")
            durability_class =  durability_class_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            durability_class = ""
            pass

        print(f'urability_class = ', durability_class)



        try:
            nwpc_wood_protection_class_according_to_en_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'NWPC Trebeskyttelsesklasse ihenhold til EN 351-1 og EN 335-1')]")
            nwpc_wood_protection_class_according_to_en =  nwpc_wood_protection_class_according_to_en_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            nwpc_wood_protection_class_according_to_en = ""
            pass

        print(f'nwpc_wood_protection_class_according_to_en = ', nwpc_wood_protection_class_according_to_en)



        try:
            use_class_according_to_en_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'Bruksklasse i henhold til EN 351-1')]")
            use_class_according_to_en =   use_class_according_to_en_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            use_class_according_to_en = ""
            pass

        print(f'use_class_according_to_en = ', use_class_according_to_en)



        try:
            ce_mark_element = product_attribute_contents[0].find_element(By.XPATH, "//*[contains(text(), 'CE-merket')]")
            ce_mark =  ce_mark_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            ce_mark = ""
            pass

        print(f'ce_mark = ', ce_mark)


        try:
            net_content_element = product_attribute_contents[1].find_element(By.XPATH, "//*[contains(text(), 'Netto innhold')]")
            net_content =   net_content_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            net_content = ""
            pass

        print(f'net_content = ', net_content)

        try:
            height_element = product_attribute_contents[1].find_element(By.XPATH, "//*[contains(text(), 'Høyde')]")
            height =  height_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            height = ""
            pass

        print(f'height = ', height)

        try:
            length_element = product_attribute_contents[1].find_element(By.XPATH, "//*[contains(text(), 'Lengde')]")
            length =  length_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            length = ""
            pass

        print(f'length = ', length)

        try:
            width_element = product_attribute_contents[1].find_element(By.XPATH, "//*[contains(text(), 'Bredde')]")
            width =  width_element.find_element(By.XPATH, "./following-sibling::*[1]").text
        except:
            width = ""
            pass

        print(f'width = ', width)
        sleep(1)    
        
        quickstart.main()
        columnCount = quickstart.getColumnCount()

        
        print(f'columnCount = ',columnCount)


        results = []
        results.append(str(columnCount + 1))
        results.append(product_name)
        results.append(product_price)
        results.append(product_advantage)
        results.append(img_urls)
        results.append(article_number)
        results.append(ena_number)
        results.append(product_description)
        results.append(wood_spices)
        results.append(modification_method)
        results.append(with_bark)
        results.append(thickness_millimeters)
        results.append(widht_millimeters)
        results.append(surface_treatment)
        results.append(number_of_processed_page)
        results.append(environment_certification)
        results.append(durability_class)
        results.append(nwpc_wood_protection_class_according_to_en)
        results.append(use_class_according_to_en)
        results.append(ce_mark)
        results.append(net_content)
        results.append(height)
        results.append(length)
        results.append(width)
        

        quickstart.main()
        RANGE_DATA = f'www_byggmakker_no!A{columnCount + 2}:X'
        quickstart.insert_data(RANGE_DATA, results)

                
        
    except:
        continue

    
   





    

                            
        
    


        
        
    
