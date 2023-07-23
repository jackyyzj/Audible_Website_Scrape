from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
# options.add_argument('--headless')
# options.add_argument('window-size=1920x1080')

web = "https://www.audible.com/search?sort=review-rank&ref=a_search_c1_sort_5&pf_rd_p=073d8370-97e5-4b7b-be04" \
	  "-aa06cf22d7dd&pf_rd_r=N9YP47GFTW3G613864AR&pageLoadId=9uXkDnMiaK0g2Bbw&creativeId=792c6ece-15a9-4a32-b4ea" \
	  "-d95a6bbc6141#"
driver = webdriver.Chrome(options=options)
driver.get(web)
driver.maximize_window()

book_title = []
book_author = []
book_length = []

pagination = driver.find_element(By.XPATH, '//ul[contains(@class,"pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)

current_page = 1

while current_page <= last_page:

	products = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "productListItem")]')))

	for product in products:
		book_title.append(product.find_element(By.CSS_SELECTOR, "li h3 a").text)
		book_author.append(product.find_element(By.CLASS_NAME, "authorLabel").text)
		book_length.append(product.find_element(By.CLASS_NAME, "runtimeLabel").text)

	current_page += 1

	try:
		next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
		next_page.click()

	except:
		pass

driver.close()

df_books = pd.DataFrame({"title": book_title, "author": book_author, "length": book_length})
df_books.to_csv("books.csv", index=False)
