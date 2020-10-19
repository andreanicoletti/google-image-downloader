import scraping_functions
from tqdm import tqdm
import os


class GoogleImagesDownloader:
    def __init__(self, driver_path, image_quality=95):
        self.driver = scraping_functions.create_chrome_driver(driver_path)
        self.quality = image_quality

    def download_images(self, query, folder, max_images):
        print('Fetching urls:')
        urls = scraping_functions.search_urls(self.driver, query, max_images)
        print('{} urls found, downloading images:'.format(len(urls)))
        for index, url in tqdm(enumerate(urls)):
            path = os.path.join(folder, query + str(index) + '.jpg')
            scraping_functions.save_image(url, path, self.quality)
