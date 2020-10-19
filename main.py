from google_images_downloader import GoogleImagesDownloader
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download images from Google')
    parser.add_argument('--query', type=str, help='title of the images to be downloaded')
    parser.add_argument('--imagecount', type=int, help='the number of images to be downloaded')
    parser.add_argument('--driverpath', type=str, help='path of the chrome driver executable')
    parser.add_argument('--folder', type=str, help='path of the folder in which save the images')
    args = parser.parse_args()
    GoogleImagesDownloader(args.driverpath).download_images(args.query, args.folder, args.imagecount)
