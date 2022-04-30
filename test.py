import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

executor = ThreadPoolExecutor(10)


def scraper(url):
    print('a')
    options = Options()
    driver = webdriver.Chrome("./chromedriver")
    driver.get(url)


loop = asyncio.get_event_loop()
for url in ["https://google.de"] * 2:
    loop.run_in_executor(executor, scraper, url)

loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))