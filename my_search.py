import urllib.request 
from selenium import webdriver
import sys
import time

REVERSE_URL = "http://images.google.com/searchbyimage?site=search&image_url="

# Find twitter urls and extract usernames

# Compare similarity of two images

def _parse_images(browser):
	prev_elems = 0
	post_elems = browser.find_elements_by_tag_name("img")

	while len(post_elems) > prev_elems:
		prev_elems = len(post_elems)
		browser.execute_script(
			"window.scrollTo(0, document.body.scrollHeight);"
		)
		time.sleep(0.5)
		post_elems = browser.find_elements_by_tag_name("img")

	images = [elem.get_attribute('src') for elem in post_elems]
	images = list(set(images))
	images.sort()

	return images

if __name__ == '__main__':
	images = ["http://www.discoverlife.org/nh/tx/Cnidaria/images/Chrysaora_quinquecirrha,I_JP13_1.240.jpg"]
	parser = webdriver.Firefox()

	for img in images:
		parser.get(REVERSE_URL + img)
		page = parser.page_source
		file_ = open('page.html','w')
		file_.write(page)
		file_.close()

	parser.close()