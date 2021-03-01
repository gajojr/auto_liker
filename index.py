from selenium import webdriver
import pyperclip
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# page to get random email address
driver.get("https://temp-mail.org/sr/")

# field where email is stored
random_mail = driver.find_element_by_id("mail")
# while email is in process of making these are the values of input:
variants = ["Учитавање", "Учитавање.", "Учитавање..", "Учитавање..."]

# check against all variants
while(random_mail.get_property("value") in variants):
	# wait .5s because it takes time
	time.sleep(0.5)
	random_mail = driver.find_element_by_id("mail")

# print to check if it's successful
print("Nova vrednost", random_mail.get_property("value"))
access_info = {
  "mail": random_mail.get_property("value")
}

# copy the text to clipboard
# pyperclip.copy(random_mail.get_property("value"))
# check if it copied
# copied_text = pyperclip.paste()
# print(copied_text)

# enter the second page because that's were the work is
driver.execute_script('''window.open("https://www.evropskidnevnik.rs/multimedija-kategorija/page/2/","_blank").focus();''')
print(len(driver.window_handles))
driver.switch_to_window(driver.window_handles[2])

print("naslov:", driver.title)
works = driver.find_elements_by_class_name("student-single-item-data")
# we need last(6th) work 
goal_work = works[5]
project_name = goal_work.find_element_by_class_name("total-votes").text
print("Broj lajkova:", project_name)

# driver.quit()