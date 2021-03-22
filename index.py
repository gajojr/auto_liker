from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time

i = 0
while i < 20:
	i += 1
	PATH = "C:\Program Files (x86)\chromedriver.exe"
	driver = webdriver.Chrome(PATH)

	# page to get random email address
	driver.get("https://mail.tm/en/")

	# field where email is stored
	random_mail = driver.find_element_by_id("address")

	# check against all variants
	while(random_mail.get_property("value") == "..."):
		# wait .5s because it takes time
		time.sleep(0.25)
		random_mail = driver.find_element_by_id("address")

    # store mail for later 
	access_info = {
	  "mail": random_mail.get_property("value")
	}

	# enter the second page because that's were the work is
	driver.execute_script('''window.open("https://www.evropskidnevnik.rs/multimedija-kategorija/page/2/","_blank").focus();''')
	temp_mail_page = driver.window_handles[0]
	voting_page = driver.window_handles[2]
	driver.switch_to.window(voting_page)

	works = driver.find_elements_by_class_name("student-single-item-data")
	# we need last(6th) work 
	goal_work = works[5]
	like_btn = goal_work.find_element_by_class_name("vote-btn")
	like_btn.click()

	form = driver.find_element_by_class_name("confirm-registration-data")
	link = form.find_element_by_tag_name("a")
	link.click()

	register_link = WebDriverWait(driver, 5).until(
	        	EC.presence_of_element_located((By.CSS_SELECTOR, "p>a"))
	    	)
	register_link.click()

	username_input = driver.find_element_by_id("user_login")
	username_input.clear()
	username_input.send_keys(access_info["mail"])

	email_input = driver.find_element_by_id("user_email")
	email_input.clear()
	email_input.send_keys(access_info["mail"])

	submit_form_button = driver.find_element_by_id("wp-submit")
	submit_form_button.click()

	driver.switch_to.window(temp_mail_page)

	temp = None
	while temp is None:
		try:
			link_for_like = WebDriverWait(driver, 3).until(
	        	EC.presence_of_element_located((By.CSS_SELECTOR, "li>a"))
	    	)
			link_for_like.click()
			temp = True
		except:
			time.sleep(3)
			driver.refresh()

	go_back_voting_page = WebDriverWait(driver, 20).until(
	        EC.presence_of_element_located((By.CSS_SELECTOR, "span>a"))
	    )
	go_back_voting_page.click()

	# open document
	document = WebDriverWait(driver, 20).until(
	        EC.presence_of_element_located((By.CLASS_NAME, "whitespace-pre-line"))
	    )

	# write document to local file
	with open("file.txt", "w", encoding="utf-8") as file1:
		file1.write(document.text)
		file1.close()

	with open("file.txt", "r", encoding="utf-8") as f:
	    lines = f.read().splitlines()
	    last_line = lines[-1]
	    driver.execute_script('window.open("{last_line}","_blank").focus();'.format(last_line=last_line))

	driver.switch_to.window(driver.window_handles[-1])

	driver.execute_script("document.getElementById('pass1').dataset.pw = '';")
	driver.find_element_by_id("pass1").send_keys(access_info["mail"])

	reset_button = driver.find_element_by_id("wp-submit")
	reset_button.click()

	log_in_link = driver.find_element_by_css_selector("p>a")
	log_in_link.click()


	new_user_login = driver.find_element_by_id("user_login")
	new_user_login.clear()
	new_user_login.send_keys(access_info["mail"])

	new_user_password = driver.find_element_by_id("user_pass")
	new_user_password.clear()
	new_user_password.send_keys(access_info["mail"])

	# might not work when internet connection is slow
	form_final = driver.find_element_by_id("loginform")
	form_final.submit()

	driver.execute_script('''window.open("https://www.evropskidnevnik.rs/multimedija-kategorija/page/2/","_blank").focus();''')
	driver.switch_to.window(driver.window_handles[-1])

	works = driver.find_elements_by_class_name("student-single-item-data")
	# we need last(6th) work 
	goal_work = works[5]
	like_btn = goal_work.find_element_by_class_name("vote-btn")
	like_btn.click()

	# wait for like notification
	time.sleep(3)
	driver.delete_all_cookies() 
	driver.execute_script('window.localStorage.clear();')
	driver.execute_script('window.sessionStorage.clear();')

	driver.quit()