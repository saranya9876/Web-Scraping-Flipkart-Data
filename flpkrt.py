import requests
from bs4 import BeautifulSoup
import pandas as pd

product_name = []
price = []
description = []
reviews = []

for i in range(2, 15):
    try:
        r = requests.get(f"https://www.flipkart.com/search?q=mobile+phones+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        box = soup.find("div", class_="DOjaWF gdgoEp")

        np_element = soup.find('a', class_="cn++Ap")
        if np_element:
            np = np_element.get("href")
            cnp = "https://www.flipkart.com/" + np

            url = cnp
            rn = requests.get(url)
            rn.raise_for_status()
            soup = BeautifulSoup(rn.text, "lxml")

            names = box.find_all("div", class_="KzDlHZ") if box else []
            prices = box.find_all("div", class_="Nx9bqj _4b5DiR") if box else []
            desc = box.find_all("ul", class_="G4BRas") if box else []
            review = box.find_all("div", class_="XQDdHH") if box else []

            # Ensure all required elements are present before appending
            for item_name, item_price, item_desc, item_review in zip(names, prices, desc, review):
                product_name.append(item_name.text)
                price.append(item_price.text)
                description.append(item_desc.text)
                reviews.append(item_review.text)
        else:
            print(f"No pagination link found on page {i}")
    except Exception as e:
        print(f"An error occurred on page {i}: {e}")

# Check if all lists have the same length
if len(product_name) == len(price) == len(description) == len(reviews):
    df = pd.DataFrame({
        "Product Name": product_name,
        "Price": price,
        "Description": description,
        "Reviews": reviews
    })
    print(df)
else:
    print("Data lists are not of the same length.")
    print(f"Product Names: {len(product_name)}, Prices: {len(price)}, Descriptions: {len(description)}, Reviews: {len(reviews)}")


if  df.to_csv('flipkart_mobile_phones.csv', index=False):
    print("Data has been written to flipkart_mobile_phones.csv")
else:
    print("Data lists are not of the same length.")
    print(f"Product Names: {len(product_name)}, Prices: {len(price)}, Descriptions: {len(description)}, Reviews: {len(reviews)}")
