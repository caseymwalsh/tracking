from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
from sqlite3 import Error

def db_connect_read(db):
	conn = None
	results = {}
	try:
		conn = sqlite3.connect(db)
	except Error as e:
		print(e)

	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	for row in c.execute('select trackingnumber, id, note from tracking where active = 1'):
		results[row[0]] = [row[1],row[2]]
	conn.close()
	return results


def db_update(db, id, status, location):
	conn = None
	try:
		conn = sqlite3.connect(db)
	except Error as e:
		print(e)

	c = conn.cursor()
	c.execute('update tracking set status = ? where id = ?', (status, id))
	c.execute('update tracking set location = ? where id = ?', (location, id))
	if 'Delivered' in status:
			if input('Delivered. Remove?: y/n ') == 'y':
					c.execute('update tracking set active = 0 where id = ?', (id,))
	conn.commit()
	conn.close()

def get_status(trknb, id, note):
	URL = "https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=" + trknb
	driver.get(URL)
	
	try:
		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "delivery_status")))
		status_parent = driver.find_element(By.CLASS_NAME, "delivery_status")
		status = status_parent.find_element(By.TAG_NAME, "strong").text
		location_parent = driver.find_element(By.CLASS_NAME, "status_feed")
		location = location_parent.find_elements(By.TAG_NAME, "p")[1].text
		
		print(trknb, status, location.rjust(100-len(status)), note)
		db_update('tracking.db', id, status, location)
	except TimeoutException:
		print(trknb, 'Request timed out')
	except:
		print(trknb, 'Something broke')


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

print('Driver open')

data = db_connect_read('tracking.db')
for key,value in data.items():
		get_status(key, value[0], value[1])

driver.quit()
print('Driver closed')