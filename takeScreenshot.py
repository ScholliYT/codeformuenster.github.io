from selenium import webdriver

# Save a screenshot from spotify.com in current directory.
DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER)
driver.get('https://www.spotify.com')
screenshot = driver.save_screenshot('spotify.png')
driver.quit()