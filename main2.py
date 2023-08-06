from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.service import Service as ChromeService
from amazoncaptcha import AmazonCaptcha


def get_product_title_from_asin(asin):

    URL = 'https://www.amazon.com/dp/' + asin
    chrome_options = Options()
    service = ChromeService(executable_path="path/to/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)
    driver.implicitly_wait(50)

    #amazon captcha
    image = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
    image_link = image.get_attribute('src')
    captcha = AmazonCaptcha.fromlink(image_link)
    solution = captcha.solve(keep_logs=True)
    print(solution)
    TFF = driver.find_element(By.XPATH, '//*[@id="captchacharacters"]')
    TFF.send_keys(solution)

    button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')
    button.click()
    #//*[@id="captchacharacters"]
    #/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button


    title_element = driver.find_element(By.ID, 'productTitle')
    title = title_element.text.strip()
    photo_element = driver.find_element(By.ID, 'landingImage')
    photo_url = photo_element.get_attribute('src')
    price_element = driver.find_element(By.CSS_SELECTOR, '.a-price[data-a-size=b], .a-price[data-a-size=xl]')
    price = price_element.text.strip()
    Brand_element = driver.find_element(By.XPATH, '//*[@id="bylineInfo"]')
    brand_text = Brand_element.text.strip()
    if 'Brand:' in brand_text:
        index_brand = brand_text.index("Brand:")
        brand=brand_text[index_brand + 1:]
    else:
        start_index = brand_text.find('the') + len('the') + 1
        end_index = brand_text.find('Store') - 1
        brand = brand_text[start_index:end_index].strip()
    try:
        table_element = driver.find_element(By.ID, 'productDetails_detailBullets_sections1')
    except:
        try:
            table_element = driver.find_element(By.ID, 'productDetails_db_sections')
        except:
            return None
    rows = table_element.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        if "Best Sellers Rank" in row.text:
            best_seller_rank_element = row.find_element(By.TAG_NAME, 'td')
            BSR = best_seller_rank_element.text.strip()

    Star5_element=driver.find_element(By.XPATH,'//*[@id="histogramTable"]/tbody/tr[1]/td[3]')
    Star5=Star5_element.text.strip()
    Star4_element=driver.find_element(By.XPATH,'//*[@id="histogramTable"]/tbody/tr[2]/td[3]/span[2]')
    Star4=Star4_element.text.strip()
    Star3_element=driver.find_element(By.XPATH,'//*[@id="histogramTable"]/tbody/tr[3]/td[3]/span[2]')
    Star3=Star3_element.text.strip()
    Star2_element=driver.find_element(By.XPATH,'//*[@id="histogramTable"]/tbody/tr[4]/td[3]/span[2]')
    Star2=Star2_element.text.strip()
    Star1_element=driver.find_element(By.XPATH,'//*[@id="histogramTable"]/tbody/tr[5]/td[3]/span[2]')
    Star1=Star1_element.text.strip()
    product_info = {
        'title': title,
        'photo_url': photo_url,
        'price': price,
        'Brand': brand,
        'BSR': BSR,
        'Star5':Star5,
        'Star4':Star4,
        'Star3': Star3,
        'Star2':Star2,
        'Star1':Star1
    }
    for key, value in product_info.items():
        print(f"{key}: {value}")

asin = 'B093B59MGM'
get_product_title_from_asin(asin)