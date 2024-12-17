import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Function to check Zul'jin realm status using Selenium and BeautifulSoup
def check_zuljin_status():
    url = "https://worldofwarcraft.blizzard.com/en-us/game/status/us"
    print("Checking Zul'jin realm status...\n")

    # Setup headless Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Setup ChromeDriver
    service = Service("chromedriver")  # Replace with the path to your chromedriver if needed
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        while True:
            # Load the page and wait for JavaScript to render
            driver.get(url)
            time.sleep(0.1)  # Allow time for JavaScript execution
            
            # Parse page content with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Search for Zul'jin row
            rows = soup.find_all("div", class_="SortTable-row")
            for row in rows:
                columns = row.find_all("div", class_="SortTable-col SortTable-data align-center")
                if len(columns) > 1 and "Zul'jin" in columns[1].get_text():
                    # Check for the red X icon in the first column
                    if row.find("span", class_="Icon--closeCircleRed"):
                        print("Zul'jin Realm Status: Down (Red X detected)")
                    else:
                        print("Zul'jin Realm Status: Up (No Red X detected)")
                        print("\nZul'jin is UP! Go log in!\n")
                        #make a noise
                        import winsound
                        frequency = 2500
                        duration = 3000
                        winsound.Beep(frequency, duration)

                        driver.quit()
                        return
            
            print("Zul'jin is still down. Checking again in 1 seconds...")
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    check_zuljin_status()
