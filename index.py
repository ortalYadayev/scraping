from article import Article
from flight import Flight
import json
from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.common.by import By
from collections import namedtuple
import time

articleFilename="data/articles.json"
flightFilename="data/flights.json"

def findElementByClassNameAndText(className):
    try:
        element = driver.find_element(By.CLASS_NAME, className).text

        return element
    except:
        print('error')

def findElementsByClassName(className, attribute=None, text=False):
    try:
        result = []
        elements = driver.find_elements(By.CLASS_NAME, className)

        for element in elements:
            attributeAndText = {}
            if attribute is not None:
                url = element.get_attribute(attribute)
                attributeAndText['url'] = url
            if text:
                content = element.text
                attributeAndText['text'] = content

            result.append(attributeAndText)

        return result
    except:
        print('error')

def writeToFile(fileName, data):
    dataJSON = data.toJson()

    jsonFile = open(fileName, "a")
    jsonFile.write(dataJSON + "\n")
    jsonFile.close()

def readFromFile(fileName, className):
    result = []

    for line in open(fileName, 'r'):
        dataObj = json.loads(line, object_hook=lambda d: namedtuple(className, d.keys())(*d.values()))
        result.append(dataObj)

    return result

def searchArticles(data, value):
    result = []

    for item in data:
        flag = False
        containsInHeader = lambda : item.header and item.header.lower().__contains__(value.lower())

        for p in item.paragraphs:
            containsInP = lambda : p.text and p.text.lower().__contains__(value.lower())
            if(containsInP()):
                flag = True
                break

        for list in item.lists:
            containsInList = lambda : list.text and list.text.lower().__contains__(value.lower())
            if(containsInList()):
                flag = True
                break

        containsInSubtitle = False

        for subtitle in item.subtitles:
            if (subtitle.text and subtitle.text.lower().__contains__(value.lower())):
                flag = True
                break

        if((flag or containsInHeader()) == True):
            result.append(item.urlSite)

    return result

def searchFlights(data, value):
    result = []

    for item in data:
        containsInAirline = lambda : (item.airline and item.airline.lower().__contains__(value.lower()))
        containsInFlight = lambda : (item.flightId and item.flightId.lower().__contains__(value.lower()))
        containsInLand = lambda : (item.landFrom and item.landFrom.lower().__contains__(value.lower()))
        terminalInTerminal = lambda : (item.terminal and item.terminal.lower().__contains__(value.lower()))
        containsInScheduledTime = lambda : (item.scheduledTime and item.scheduledTime.lower().__contains__(value.lower()))
        containsInUpdatedTime = lambda : (item.updatedTime and item.updatedTime.lower().__contains__(value.lower()))
        containsInStatus = lambda : (item.status and item.status.lower().__contains__(value.lower()))

        if((containsInAirline()  or containsInFlight() or containsInLand() or terminalInTerminal or containsInScheduledTime() or containsInUpdatedTime() or containsInStatus()) == True):
            result.append(item)

    return result

switch_caseForArticles = {
    "Article": searchArticles,
    "Flight": searchFlights
}

def search(fileName, className):
    data = readFromFile(fileName, className)

    valueForSearch = input("Search: \n")

    result = switch_caseForArticles.get(className)(data, valueForSearch)
    return result

if __name__ == '__main__':
    config = dotenv_values(".env")
    PATH = str(config["PATH_DRIVER"]) + "/chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.bbc.com/")

#     information for articles
    href_links_bbc = []
    links = driver.find_elements(By.CLASS_NAME, "block-link__overlay-link")

    for link in links:
        l = link.get_attribute("href")
        if l not in href_links_bbc:
            href_links_bbc.append(l)

    for link in href_links_bbc:
        driver.get(link)

        header = findElementByClassNameAndText("ssrcss-15xko80-StyledHeading")
        paragraphs = findElementsByClassName("ssrcss-1q0x1qg-Paragraph", None, True)
        lists = findElementsByClassName("ssrcss-k17ofw-InlineLink", None, True)
        h2 = findElementsByClassName("ssrcss-y2fd7s-StyledHeading", None, True)

        article = Article(link, header, paragraphs, lists, h2)
        writeToFile(articleFilename, article)

#     information for flights
    driver.get("https://www.iaa.gov.il/airports/ben-gurion/flight-board")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    table = driver.find_element(By.CLASS_NAME, "table")

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")

        flightArr = []
        for col in cols:
            div = col.find_element(By.TAG_NAME, "div")
            flightArr.append(div.text)

        flight = Flight()

        switch_caseForFlights = {
            0: flight.set_airline,
            1: flight.set_flightId,
            2: flight.set_landFrom,
            3: flight.set_terminal,
            4: flight.set_scheduledTime,
            5: flight.set_updatedTime,
            6: flight.set_status,
            7: flight.set_trigger
        }

        i = 0
        if(len(flightArr) > 0):
            for i in range(8):
                switch_caseForFlights.get(i)(flightArr[i])

            writeToFile(flightFilename, flight)

    driver.quit()

    print("The articles found: ")
    print(search(articleFilename, "Article"))
    print("The flights found: ")
    print(search(flightFilename, "Flight"))

