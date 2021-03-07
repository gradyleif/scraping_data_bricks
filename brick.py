from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

driver_path = '/home/grady/Downloads/chromedriver'
delay = 1
def wait_ready_page(driver, delay):
	while True:
		val = driver.execute_script("return document.readyState")
		if val == 'complete':
			break
		time.sleep(delay)

def get_tokopedia_url(driver, link_list, count, max_size):
	product_div = driver.find_element_by_xpath("//div[@data-testid='lstCL2ProductList']")
	products = product_div.find_elements_by_xpath("//a[@data-testid='lnkProductContainer']")
	for product in products:
		href = product.get_attribute("href")
		link_list.append(href)
		count+=1
		if count >= max_size:
			break

def get_list_of_link(url, starting_page, get_urls, max_size = 100):
	link_list = []
	page = starting_page
	error_count = 0
	while True:
		try:
			count = len(link_list)
			if count >= max_size:
				break
			print(count)

			driver = webdriver.Chrome(driver_path)
			driver.get(url+str(page))
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			wait_ready_page(driver,delay)

			get_urls(driver, link_list, count, max_size)
			
			driver.quit()
			page+=1
			error_count = 0
		except Exception as e:
			print(starting_page, e)
			error_count += 1
			if error_count > 5:
				break
			time.sleep(5)
	return link_list

def get_tokopedia_information(url):
	error_count = 0
	while True:
		try:
			data = {}

			driver = webdriver.Chrome(driver_path)
			driver.get(url)
			wait_ready_page(driver,delay)

			# get name of product
			name = driver.find_element_by_xpath("//h1[@data-testid='lblPDPDetailProductName']")
			data['name_of_product'] = name.text

			# get description
			description = driver.find_element_by_xpath("//div[@data-testid='lblPDPDescriptionProduk']")
			data['description'] = description.text

			# get image
			img_div = driver.find_element_by_xpath("//div[@data-testid='PDPImageMain']")
			img = img_div.find_element_by_tag_name("img")
			data['image_link'] = img.get_attribute("src")

			# get price
			price = driver.find_element_by_xpath("//div[@data-testid='lblPDPDetailProductPrice']")
			data['price'] = price.text
			# get rating
			try:
				rating = driver.find_element_by_xpath("//div[@data-testid='lblPDPDetailProductRatingNumber']")
				data['rating'] = rating.text
			except:
				data['rating'] = '-'

			driver.quit()
			print(data)
			return data
		except Exception as e:
			print(url, e)
			error_count += 1
			if error_count > 5:
				break
			time.sleep(5)
	return url

links = get_list_of_link("https://www.tokopedia.com/p/handphone-tablet/handphone?page=", 1, get_tokopedia_url, 100)

products = []
failed_urls = []

for link in links:
	data = get_tokopedia_information(url)
	if isinstance(data,str):
		failed_urls.append(result)
	else:
		product.append(result)
print(product)
print(failed_urls)