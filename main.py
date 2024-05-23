from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep
from random import random

def sleep_random(time: float):
    sleep((0.5 + random()) * time)

# The name of the product to search
search_queue = [('신라면', [])]

# Write csv file
output = open('output.csv', 'w')
 
# Write header
output.write('category_num,user_num,num_photo,rating,date,num_helpful')

# Detect duplicates & convert id and product category to integer
user_dict = {}
category_dict = {}

# Prevent from visiting same product twice
product_id_set = set()
review_id_set = set()

# Start selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options) 

while True:
    driver.get('https://www.coupang.com')
    sleep_random(2)

    # Terminate if no keyword
    if len(search_queue) == 0:
        break

    # Search the keyword in the front of the queue
    search_keyword, others = search_queue.pop(0)
    search_input = driver.find_element(By.XPATH, '//*[@id="headerSearchKeyword"]')
    search_input.click()
    sleep_random(0.5)
    search_input.send_keys(search_keyword + '\n')

    # Move to product page that is in the first of the list, which was not visited
    sleep_random(1)
    product_li_list = driver.find_elements(By.CSS_SELECTOR, 'li.search-product:not(.search-product__ad-badge)')
    for product_li in product_li_list:
        product_id = int(product_li.get_attribute('id'))

        if product_id not in product_id_set:
            product_id_set.add(product_id)
            product_anchor = product_li.find_element(By.TAG_NAME, 'a')
            driver.get(product_anchor.get_attribute('href'))
            break

    # Get category
    while True:
        try:
            category = driver.find_element(By.XPATH, '//*[@id="breadcrumb"]/li[6]/a').text
            sleep(0.5)
            break
        except Exception:
            pass
    
    # If it is a new category, add to category_dict
    if category_dict.get(category) == None:
        category_dict[category] = len(category_dict.keys())
    category_num = category_dict[category]

    if len(others) > 0:
        others = list(map(str, others))
        output.write(str(category_num) + ',' + ','.join(others) + '\n')

    # Scroll to bottom of the page to load comments
    for i in range(2):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        sleep_random(1)

    # Click on comments button
    driver.find_element(By.XPATH, '//*[@id="btfTab"]/ul[1]/li[2]').click()
    sleep_random(2)

    # Get list of comments
    reviews = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list.js_reviewArticleReviewList')
    for review in reviews:
        review_id = int(review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__help').get_attribute('data-review-id'))

        if review_id in review_id_set:
            continue

        review_id_set.add(review_id)

        user_id = int(review.find_element(By.CSS_SELECTOR, '.js_reviewUserProfileImage').get_attribute('data-member-id'))

        if user_dict.get(user_id) == None:
            user_dict[user_id] = len(user_dict.keys())
        user_num = user_dict[user_id]

        num_photo = int(len(review.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__attachment__list')))
        rating = int(review.find_element(By.CSS_SELECTOR, '.js_reviewArticleRatingValue').get_attribute('data-rating'))
        date = review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__info__product-info__reg-date').text
        num_helpful = int(review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__help.js_reviewArticleHelpfulContainer').get_attribute('data-count'))
        
        output.write(f'{category_num},{user_num},{num_photo},{rating},{date},{num_helpful}\n')

        # Find next item to get
        review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__info__user__name.js_reviewUserProfileImage').click()
        
        # Explicitly wating for page to load
        while True:
            try:
                close_btn = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.sdp-review__profile__article__close-btn.js_modalClose'))
                )
                print('wait')
                break
            except Exception:
                pass
        sleep(2)
        # Get reviews in the profile
        add_cnt = 0
        profile_reviews = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__profile__article__list__reviews')
        for p_review in profile_reviews:
            # print(p_review.text)
            p_review_id = int(p_review.find_element(By.CSS_SELECTOR, '.sdp-review__profile__article__list__reviews__help').get_attribute('data-review-id'))

            if p_review_id in review_id_set:
                continue
            
            p_name = p_review.find_element(By.CSS_SELECTOR, '.sdp-review__profile__article__list__reviews__product__name').text
           
            p_num_photo = int(len(p_review.find_elements(By.CSS_SELECTOR,'.sdp-review__profile__article__list__reviews__attachment__list')))
            p_rating = int(p_review.find_element(By.CSS_SELECTOR, '.sdp-review__profile__article__list__reviews__star__orange.js_reviewProfileModalReviewRating').get_attribute('data-rating'))
            p_num_helpful = int(p_review.find_element(By.CSS_SELECTOR, '.js_reviewProfileModalHelpfulContainer').get_attribute('data-count'))
            p_date = p_review.find_element(By.CSS_SELECTOR, '.sdp-review__profile__article__list__reviews__star__date').text

            search_queue.append((p_name, [user_num, p_num_photo, p_rating, p_date, p_num_helpful]))
            add_cnt += 1

            if add_cnt == 3:
                break       

        sleep_random(1)
        driver.execute_script("arguments[0].click();", close_btn)
        sleep_random(1)

    if len(user_dict.keys()) > 10:
        break

output.close()