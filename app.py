from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
driver_path = r"C:\Users\KAMESH\OneDrive\Desktop\DATA SCIENCE\ASSIGNMENT ANSWERS\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
url='https://www.youtube.com/@PW-Foundation/videos'
driver.get(url)
SCROLL_PAUSE_TIME=3
last_height=driver.execute_script("return document.documentElement.scrolllHeight")
while True:
    driver.execute_script("window.scrollTo(0,arguments[0]);",last_height)
    time.sleep(SCROLL_PAUSE_TIME)
    new_height=driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height=new_height
titles=driver.find_elements(By.ID,"video-title")
views=driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[1]')
images=driver.find_elements(By.CSS_SELECTOR, 'img.yt-core-image.yt-core-image--fill-parent-height.yt-core-image--fill-parent-width.yt-core-image--content-mode-scale-aspect-fill.yt-core-image--loaded')
url=driver.find_elements(By.XPATH,'//*[@id="thumbnail"]')
time=driver.find_elements(By.XPATH, '//*[@id="metadata-line"]/span[2]')
data=[]
for i,j,k,m,n in zip(titles[:5],views[:5],images[1:6],url[3:8],time[:5]):
    data.append([i.text,j.text,k.get_attribute('src'),m.get_attribute('href'),n.text])
df=pd.DataFrame(data,columns=['title','views','thumbnail','URL','TIME'])
df.to_csv("youtube_ideos_details.csv")
driver.quit()


print(df.head())

from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def upload():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('youtube_ideos_details.csv')
    
    # Convert the DataFrame to an HTML table
    html_table = df.to_html(classes='table table-striped', index=False)
    
    # HTML template to embed the table
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Videos Details</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h2 class="mt-4">YouTube Videos Details</h2>
            {html_table}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0")