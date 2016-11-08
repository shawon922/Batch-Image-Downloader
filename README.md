# Batch-Image-Downloader
### A simple Batch Image Downloader using Python and BeautifulSoup.

## What it does

* Downloads all the images from a given url and saves them
  in the directory of the script.

* Takes input either from the use or from system clipboard

* Constraints :
  1. An url (from where images will be downloaded)
  2. Yes or No (whether user want to download images from sub-pages of the given url)

The program can also use Pyperclip to get the link from your clipboard with a
cmd arg as whether user want to download images from sub-pages of the given url


## Usage

1. If the user has the web page link copied to clipboard :
   usage : python image_downloader.py <y/n>
   If user copies an invalid link execution will terminate and print invalid link
   on the console.

   Best if downloading from webpages!

    ```python
    python image_downloader.py y
    # this will download the images from the sub pages, n will mean to get from
    # root pages only
    ```

2. If the user wants to input the url and the choice :

    ```python
    python image_downloader.py
    # this will download the images from the sub pages, n will mean to get from
    # root pages only
    ```

## Output

A directory will be auto generated and images will be downloaded into the directory. If there are more than 50 images, the program will ask for permission to continue or stop the execution.

> Change record is in log_revision_1.txt
