from selenium import webdriver
from PIL import Image
import requests
import io
from tqdm import tqdm


# returns a new instance of Chrome Driver
# if the driver executable path is not given, it is assumed it's in the $PATH
def create_chrome_driver(path='chromedriver'):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    return webdriver.Chrome(path, options=chrome_options)


# search the google images urls
# the number of urls fetched goes up to max_images but could be less if there are no more images available
def search_urls(driver, query, max_images):
    def scroll_to_end(d: webdriver):
        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # load page
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    driver.get(search_url.format(q=query))

    pbar = tqdm(total=max_images)
    image_urls = set()
    count = 0
    thumbnails_start = 0
    while count < max_images:
        # load more thumbnails in page
        more_results_btn = driver.find_element_by_css_selector(".mye4qd")
        if more_results_btn:
            driver.execute_script("document.querySelector('.mye4qd').click();")
        scroll_to_end(driver)

        # get all available thumbnails
        thumbnails = driver.find_elements_by_css_selector("img.Q4LuWd")
        thumbnails_len = len(thumbnails)
        if thumbnails_len == thumbnails_start:
            print('No more images available - urls found: ' + str(count))
            break

        for thumbnail in thumbnails[thumbnails_start:thumbnails_len]:
            # try to click a thumbnail to open the image panel
            try:
                thumbnail.click()
            except Exception:
                continue

            # inside the image panel find the source
            images = driver.find_elements_by_css_selector('img.n3VNCb')
            for image in images:
                if len(image_urls) >= max_images:
                    return image_urls
                elif image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    pbar.update()

        # move the result startpoint further down
        thumbnails_start = thumbnails_len

    pbar.close()
    return image_urls


# download and save the image to storage with the desired quality
def save_image(url, file_path, quality):
    try:
        response = requests.get(url)
        content = response.content
    except (requests.ConnectionError, requests.Timeout) as e:
        print('Internet not available - exception: {}'.format(e))
        return

    try:
        image_file = io.BytesIO(content)
        image = Image.open(image_file).convert('RGB')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=quality)
    except OSError as e:
        print('Cannot save image to storage - exception: {}'.format(e))
