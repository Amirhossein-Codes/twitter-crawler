from time import sleep
from bs4 import BeautifulSoup
from tkinter import messagebox
from secretInformation import MySecrets
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DELAY_FOR_TIMEOUT = 45
LOGIN_USERNAME_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
LOGIN_PASSWORD_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'

# =======================================================GET FOLLOWINGS======================================================


def search_for_followings(user_id):
    service = Service("chromedriver.exe")
    option = webdriver.ChromeOptions()
    # option.add_argument('--disable-dev-sh-usage')
    # option.add_argument('--disable-gpu')
    # option.add_argument('--headless')
    # option.add_argument('--no-sandbox')
    # option.add_argument("--user-data-dir=C:\\Users\\pm22i\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Chrome(service=service, options=option)

    # Loging in to account part
    driver.get('https://twitter.com/login')

    try:
        username_input = WebDriverWait(driver, DELAY_FOR_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, LOGIN_USERNAME_XPATH)))
        username_input.send_keys(MySecrets.USERNAME)
        driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]').click()
    except TimeoutException:
        messagebox.showerror('Slow connection!', "Twitter online content can't be loaded. Please try again")
        driver.quit()
        return []

    try:
        password_input = WebDriverWait(driver, DELAY_FOR_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, LOGIN_PASSWORD_XPATH)))
        password_input.send_keys(MySecrets.PASSWORD)
        driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
    except TimeoutException:
        messagebox.showerror('Slow connection!', "Twitter online content can't be loaded. Please try again")
        driver.quit()
        return []

    sleep(5)

    # Getting followings part

    driver.get('https://twitter.com/'+user_id+'/following')

    try:
        WebDriverWait(driver, DELAY_FOR_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section')))
    except TimeoutException:
        messagebox.showerror('Slow connection!', "Twitter online content can't be loaded. Please try again")
        driver.quit()
        return []

    # scroll part : scrolls until all javascript things (followings) loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    followings_list = []
    while True:
        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, "lxml")
        followings_block_tag = soup.find(name='section', class_='css-1dbjc4n')
        tags = followings_block_tag.find_all(name='span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')
        # Twitter id validition
        for tag in tags:
            if '@' in tag.text and len(tag.text) <= 15 and not ('.' in tag.text) and not (':' in tag.text):
                followings_list.append(tag.text.strip())
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # end of scroll part
    driver.quit()

    return [*set(followings_list)]

# =======================================================GET TWEETS======================================================

def get_tweets(user_id, amount):
    service = Service("chromedriver.exe")

    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=option)

    # Loging in to account
    driver.get('https://twitter.com/login')
    try:
        username_input = WebDriverWait(driver, DELAY_FOR_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, LOGIN_USERNAME_XPATH)))
        username_input.send_keys(MySecrets.USERNAME)
        driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]').click()
    except TimeoutException:
        messagebox.showerror('Slow connection!', "Twitter online content can't be loaded. Please try again")
        driver.quit()
        return [],[]

    try:
        password_input = WebDriverWait(driver, DELAY_FOR_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, LOGIN_PASSWORD_XPATH)))
        password_input.send_keys(MySecrets.PASSWORD)
        driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
    except TimeoutException:
        messagebox.showerror('Slow connection!', "Twitter online content can't be loaded. Please try again")
        driver.quit()
        return [],[]

    sleep(5)

    driver.get('https://twitter.com/'+user_id)

    # wait for tweets section block to be loaded
    try:
        WebDriverWait(driver, DELAY_FOR_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section')))

    except TimeoutException:
        messagebox.showerror('Slow connection!', "Twitter online content can't be loaded. Please try again")
        driver.quit()
        return [],[]

    sleep(10)

    tweets = []
    images_list = []
    string_of_tweets = []
    scroll_counter = 250
    while len(tweets) <= amount:
        sleep(0.2)
        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, "lxml")
        section_tweets = soup.find(name="section", class_="css-1dbjc4n")
        
        tweet_box = section_tweets.find_all(name="div", attrs={"data-testid":"tweetText"})
        for tweet in tweet_box:
            if tweets.count(tweet) != 0:
                tweets.remove(tweet)
        tweets.extend(tweet_box)
        images_parts = soup.find_all(name='div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu')
        driver.execute_script(f'window.scrollTo(0, {scroll_counter})')
        scroll_counter += 250
    for image_part in images_parts:
        images = image_part.find_all('img')
        for image in images:
            if not 'emoji' in image['src']:
                images_list.append(image['src'])
    for tweet in enumerate(tweets,start=1):
        string_of_tweets.append((f"----------------------------------------({tweet[0]})----------------------------------------\n\n"+tweet[1].text + "\n\n"))


    driver.quit()
    return string_of_tweets[:amount], [*set(images_list)]
