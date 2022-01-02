import requests
import lxml
from bs4 import BeautifulSoup
from price_alert import PriceAlert

# item to watch
amazon_item_url = "https://www.amazon.com/gp/product/B009PVKVSG/ref=as_li_tf_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B009PVKVSG&SubscriptionId=&linkCode=as2&tag=bestprodtag300-20"

# grab my headers from http://myhttpheader.com/
headers = {
    'Accept-Language' : "en-US,en;q=0.9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

# send request
response = requests.get(url=amazon_item_url, headers=headers)
# store response
amazon_item_page = response.text

# lxml parser needed for amazon
soup = BeautifulSoup(amazon_item_page, "lxml")
# grab item title
item_title = soup.find(name="div", id="title_feature_div").getText()
# grab price
price_field = soup.find(name="span", class_="a-offscreen").getText()
# strip the $ and treat price as float for compares
current_price = float(price_field.split('$')[1])

# if price < 300.00 send email (300 is a test value)
if current_price < 300.0:
    item_tracked = PriceAlert(item_title, current_price, amazon_item_url)
    item_tracked.send_alert()
