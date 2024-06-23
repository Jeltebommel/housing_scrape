import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set Chrome options
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)
driver.get("https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/con-precio-hasta_1500,precio-desde_500,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas/")

# Wait manually to pass the CAPTCHA
input("Press Enter after passing CAPTCHA...")

# Save cookies
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
driver.quit()