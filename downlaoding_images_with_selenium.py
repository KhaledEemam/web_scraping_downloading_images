from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# searching for the input from user and downloading images
def search(search_for, no_of_images):
    url = "https://www.google.com/imghp"
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)
    search_engine = browser.find_element(By.NAME, "q")
    search_engine.send_keys(str(search_for))
    search_button = browser.find_element(By.XPATH, "//span[@class='z1asCe MZy1Rb']")
    search_button.click()
    image = browser.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[5]/a[1]/div[1]/img')
    image.click()

    scroll_down_time = time.time()
    # Scrolling all the way down to hit the show more results button or for 5 seconds
    while True :
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        if time.time() - scroll_down_time > 5:
            break
        try:
            element = browser.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
            element.click()
            break
        except:
            "Page isn't fully loaded yet."
            continue

    # Scrolling up and getting the total number of the available images
    browser.execute_script("window.scrollTo(0, 0);")
    page_html = browser.page_source
    pageSoup = BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})
    len_containers = len(containers)
    print("Number of available images = ", len_containers)
    if len_containers < no_of_images:
        no_of_images = len_containers
        print("{} images will be downloaded since these are the only available images.".format(str(len_containers)))

    # defining function to download image
    def download_image(url, folder, image_num):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder, "{}.jpg".format(str(image_num))), "wb") as file:
                file.write(response.content)

    # making directory to save images
    folder_name = os.path.join(os.getcwd(), search_for)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    images_downloaded_successfully = 0
    # browsing images & downloading it
    for i in range(1, no_of_images + 1):
        if i % 25 == 0:
            continue
        else:
            image = browser.find_element(By.XPATH, "//*[@id='islrg']/div[1]/div[{}]/a[1]/div[1]/img".format(i))
            image.click()
            start_time = time.time()
            image_url = image.get_attribute("src")

            while True:
                clicked_image = browser.find_element(By.XPATH,"//*[@id='Sva75c']/div/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img")
                clicked_image_url = clicked_image.get_attribute("src")
                if image_url != clicked_image_url:
                    break
                else:
                    current_time = time.time()
                    if (current_time - start_time) > 5:
                        print("Timeout! Will download a lower resolution image and move onto the next one")
                        break

            try:
                download_image(clicked_image_url, folder_name, images_downloaded_successfully)
                images_downloaded_successfully += 1
            except:
                print("Couldn't download an image, continuing downloading the next one")

    print("{} images are downloaded successfully".format(images_downloaded_successfully))
    browser.close()

# getting input from user
search_for = input("Please enter a keyword to the images you need to download. E.g 'Car', 'Cat' .... etc\n")
no_of_images = input("How many images to download ? Please enter a valid number E.g '11','50','65' .... etc\n")

# Handling user's input violations
try :
    no_of_images = int(no_of_images)
except :
    print("You entered an unvalid word structure, kindly stick to the instructions.")


if no_of_images > 0 :
    search(search_for, no_of_images)
else :
    print("You entered an unvalid number, kindly stick to the instructions.")