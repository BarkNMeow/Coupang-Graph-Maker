from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import os

from time import sleep
from random import random

def sleep_random(time: float):
    sleep((0.5 + random()) * time)

search_queue = [('102102 여성용 빅사이즈 데일리 루즈핏 라운드넥 니트, FREE(66~110), 베이지', [])]
# The name of the product to search

header_available = os.path.exists('output.csv')

# Write csv file
output = open('output.csv', 'a')
 
# Write header if it is first time
if not header_available:
    output.write('category_num,product_id,user_num,num_photo,rating,date,num_helpful\n')

# Detect duplicates & convert id and product category to integer
user_dict = {}
category_dict = {}

# Prevent from visiting same product twice
product_id_set = set()
review_id_set = set()

# If exists, reproduce the review
if os.path.exists('category_code.csv'):
    with open('category_code.csv', 'r') as f:
        for line in f:
            code, categ = line.split(',')
            category_dict[categ] = int(code)

if os.path.exists('user_code.csv'):
    with open('user_code.csv', 'r') as f:
        for line in f:
            code, user = line.split(',')
            user_dict[int(user)] = int(code)

if os.path.exists('product_set'):
    with open('product_set', 'r') as f:
        for line in f:
            product_id_set.add(int(line))

if os.path.exists('review_set'):
    with open('review_set', 'r') as f:
        for line in f:
            product_id_set.add(int(line))

# Save dict and set state for reproducing
categ_code = open('category_code.csv', 'a')
user_code = open('user_code.csv', 'a')
product_set_file = open('product_set', 'a')
review_set_file = open('review_set', 'a')

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
    print('Search:', search_keyword)
    search_input = driver.find_element(By.XPATH, '//*[@id="headerSearchKeyword"]')
    search_input.click()
    sleep_random(1)
    search_input.send_keys(search_keyword + '\n')

    # Move to product page that is in the first of the list, which was not visited
    sleep_random(1)
    product_li_list = driver.find_elements(By.CSS_SELECTOR, 'li.search-product:not(.search-product__ad-badge)')

    # Skip if no search result
    if len(product_li_list) == 0:
        continue
    
    # sleep(1000)
    for product_li in product_li_list:
        product_id = int(product_li.get_property('id'))

        if product_id not in product_id_set:
            product_id_set.add(product_id)
            product_set_file.write(f'{product_id}\n')
            product_anchor = product_li.find_element(By.TAG_NAME, 'a')
            driver.get(product_anchor.get_attribute('href'))
            break

    sleep(1.5)
    # Check response code
    try:
        # Should be found
        driver.find_element(By.CSS_SELECTOR, '#container')
    except Exception:
        # Start a new session
        search_queue.insert(0, [search_keyword, others])
        driver.quit()
        driver = webdriver.Chrome(options=options)
        continue

    # Check if the product is still selling (category data exists)
    try:
        driver.find_element(By.CSS_SELECTOR, '.prod-not-find-known__buy__info')
        # If found -> product doesn't exist
        continue
    
    except Exception:
        # Should not be found
        pass

    # Get category
    while True:
        try:
            sleep(1.5)
            category = driver.find_element(By.CSS_SELECTOR, '#breadcrumb li:last-of-type').text

            if category != '쿠팡 홈':
                break
        except Exception:
            pass
    
    # If it is a new category, add to category_dict
    if category_dict.get(category) == None:
        code = len(category_dict.keys())
        category_dict[category] = code
        categ_code.write(f'{code},{category}\n')
    category_num = category_dict[category]

    # We found the product, so append the queued comment
    if len(others) > 0:
        others = list(map(str, others))
        output.write(str(category_num) + ',' + str(product_id) + ',' + ','.join(others) + '\n')

    # Scroll to bottom of the page to load comments
    for i in range(2):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        sleep_random(1)

    # Click on comments button
    try:
        review_btn = driver.find_element(By.XPATH, '//*[@id="btfTab"]/ul[1]/li[2]')
        review_btn.click()
    except Exception:
        driver.execute_script('arguments[0].click();', review_btn)
    sleep_random(2)

    # Get list of comments
    reviews = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list.js_reviewArticleReviewList')
    for review in reviews:
        review_id = int(review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__help').get_attribute('data-review-id'))

        if review_id in review_id_set:
            continue

        review_id_set.add(review_id)
        review_set_file.write(f'{review_id}\n')

        user_id = int(review.find_element(By.CSS_SELECTOR, '.js_reviewUserProfileImage').get_attribute('data-member-id'))

        if user_dict.get(user_id) == None:
            code = len(user_dict.keys())
            user_dict[user_id] = code
            user_code.write(f'{code},{user_id}\n')
        user_num = user_dict[user_id]

        num_photo = int(len(review.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__attachment__list')))
        rating = int(review.find_element(By.CSS_SELECTOR, '.js_reviewArticleRatingValue').get_attribute('data-rating'))
        date = review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__info__product-info__reg-date').text
        num_helpful = int(review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__help.js_reviewArticleHelpfulContainer').get_attribute('data-count'))
        
        output.write(f'{category_num},{product_id},{user_num},{num_photo},{rating},{date},{num_helpful}\n')

        # Go into profile and find next item to get
        try:
            # Try traditional method first
            profile_img = review.find_element(By.CSS_SELECTOR, '.sdp-review__article__list__info__user__name.js_reviewUserProfileImage')
            profile_img.click()
        except Exception:
            # On fail, use javascript
            driver.execute_script('arguments[0].click();', profile_img)
        
        popup = False
        # Explicitly wating for page to load
        for i in range(10):
            try:
                close_btn = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.sdp-review__profile__article__close-btn.js_modalClose'))
                )
                popup = True
                break
            except Exception:
                pass
                
        # If if doesn't popup, skip
        if not popup:
            continue

        sleep(2)
        # Get reviews in the profile
        add_cnt = 0
        profile_reviews = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__profile__article__list__reviews')
        for p_review in profile_reviews:
            # print(p_review.text)
            p_review_id = int(p_review.find_element(By.CSS_SELECTOR, '.sdp-review__profile__article__list__reviews__help').get_attribute('data-review-id'))

            if p_review_id in review_id_set:
                continue

            review_id_set.add(p_review_id)
            review_set_file.write(f'{p_review_id}\n')
            
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

    sleep_random(4)
    if len(user_dict.keys()) > 3000 or len(category_dict.keys()) > 3000:
        break

output.close()
categ_code.close()
product_set_file.close()
review_set_file.close()