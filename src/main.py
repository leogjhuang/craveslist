import asyncio
import base64
import json
import pandas as pd
import pyaudio
import websockets

from config import key
from flask import Flask, escape, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


app = Flask(__name__)
section = pd.read_csv('../data/aisle.csv')
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=3200)
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


def find_ingredient(ingredient, data):
    for index in data.index:
        if ingredient == (data['Ingredients'][index]):
            if (section['Stock'][index]) == 1:
                return data['Location'][index]
            else:
                return "Not in stock"
    return "Not in stock"


def get_ingredients(search_terms):
    # Initializes Chrome Driver
    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    chrome_options = webdriver.chrome.options.Options()

    # Hides browser window
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.maximize_window()

    # Loads webpage and searches for search_Term
    browser.get("https://www.yummly.com/recipes")
    print("Opening webpage...")
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "searchbox-input")))
    print("Entering search terms...")
    searchBar = browser.find_element(By.ID, "searchbox-input")
    searchBar.send_keys(search_terms)
    searchBar.send_keys(Keys.ENTER)
    print("Searching for results...")

    # Waits until results appear then select the first one
    WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='recipe-card-img-wrapper']")))
    firstItem = browser.find_element(By.XPATH, "//div[@class='recipe-card-img-wrapper']") \
        .find_element(By.TAG_NAME, "a")
    browser.execute_script("arguments[0].click();", firstItem)
    print("Retrieving results...")

    # Waits until ingredients load then collects all of the ingredients
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ingredient']")))
    ingredients = browser.find_elements(By.XPATH, "//span[@class='ingredient']")
    ingredients_list = []
    print("Getting ingredients...")
    for k in range(len(ingredients)):
        ingredients_list.append(ingredients[k].text)

    # Get name of food, time needed to make food, calories of food
    food_name = browser.find_element(By.TAG_NAME, "h1").text
    time = " ".join([k.text for k in browser.find_element(
        By.XPATH, "//div[@class='recipe-summary-item unit h2-text']").find_elements(By.TAG_NAME, "span")])
    nutrition = " ".join([k.text for k in browser.find_element(
        By.XPATH, "//div[@class='recipe-summary-item nutrition h2-text']").find_elements(By.TAG_NAME, "span")])
    print("Ingredients obtained!")

    # Generates dictionary to return
    info = {'name': food_name, 'time': time, 'nutrition': nutrition, 'ingredients': ingredients_list}

    # Closes browser
    browser.quit()

    return info


def get_price(ingredients_to_input):
    # Initializes Chrome Driver
    service1 = webdriver.chrome.service.Service(ChromeDriverManager().install())
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    browser = webdriver.Chrome(service=service1, options=chrome_options)

    browser.get("https://www.loblaws.ca/")
    print("Getting prices...")

    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "search-input__input")))
    price_list = []

    for ingredient in ingredients_to_input:
        search_item = ingredient

        # Enters ingredients
        searchBox = browser.find_element(By.CLASS_NAME, "search-input__input")
        searchBox.send_keys(Keys.COMMAND + "a")
        searchBox.send_keys(Keys.DELETE)
        searchBox.send_keys(search_item)
        searchBox.send_keys(Keys.ENTER)

        # Extracts price
        print("Getting price for", ingredient)
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//span[@class='price selling-price-list__item__price "
                       "selling-price-list__item__price--now-price']")))
        price = browser.find_element(
            By.XPATH, "//span[@class='price selling-price-list__item__price "
                      "selling-price-list__item__price--now-price']").text
        price_list.append(price)

    return price_list

    for index in data.index:
        if ingredient == (data['Ingredients'][index]):
            if (section['Stock'][index]) == 1:
                return data['Location'][index]
            else:
                return "Not in stock"
    return "Not in stock"


@app.route("/", methods=['GET', 'POST'])
def index():
    async def send_receive(trigger):
        print(f'Connecting websocket to url ${URL}')
        async with websockets.connect(
                URL,
                extra_headers=(("Authorization", key),),
                ping_interval=5,
                ping_timeout=20
        ) as _ws:
            await asyncio.sleep(0.1)
            print("Receiving Session Begins ...")
            session_begins = await _ws.recv()
            print(session_begins)
            print("Sending messages ...")

            async def send():
                first_run = True
                while True:
                    try:
                        if task.done():
                            return True
                        data = base64.b64encode(stream.read(1024)).decode("utf-8")
                        json_data = json.dumps({"audio_data": str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"
                    await asyncio.sleep(0.01)

            async def receive():
                while True:
                    try:
                        result_str = await _ws.recv()
                        text = json.loads(result_str)['text']
                        print(text)
                        if trigger in text:
                            index = text.find(trigger)
                            substring = text[:index - 1]
                            return substring
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"

        task = asyncio.create_task(receive())
        _, substring = await asyncio.gather(send(), task)
        return substring

    if request.method == 'GET':
        print("get ingredients pressed")
        if 'get_ingredients' in request.args:
            item = str(escape(request.args.get("item", "")))
            if not item:
                return render_template("index.html", warning="Please enter a search term.")
        else:
            return render_template("index.html")
    else:
        print("voice input pressed")
        item = asyncio.run(send_receive("ingredients"))
    food_info = get_ingredients(item)
    ingredients = food_info['ingredients']
    price_info = get_price(ingredients)
    aisle_info = [find_ingredient(k, section) for k in ingredients]
    for i, k in enumerate(food_info['ingredients']):
        print(str(i+1)+":", k, "-", price_info[i]+" -", find_ingredient(k, section))

    return (
        render_template(
            "index.html",
            result=[[ingredients[i], price_info[i], aisle_info[i]] for i in range(len(price_info))],
            name="Ingredients for: " + food_info['name'],
            time="Approximate preparation time: " + food_info['time'],
            nutrition="Estimated Calories: " + food_info['nutrition'],
            scroll="info"
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
