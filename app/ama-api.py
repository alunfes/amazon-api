import os
import urllib
import re
import time
import requests
import pandas as pd
import lxml
from dotenv import find_dotenv, load_dotenv
from bottlenose import Amazon
from bs4 import BeautifulSoup
from retry import retry
import csv


class AmazonAccess():
    def __init__(self):
        print("started")

    def getAmaAPI(self):
        AMAZON_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
        AMAZON_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        # AWS_ASSOCIATE_TAG = os.environ.get('AWS_ASSOCIATE_TAG')

        while True:
            try:
                amazon = Amazon(AMAZON_ACCESS_KEY, AMAZON_SECRET_ACCESS_KEY, '', Region='JP')
                response = amazon.ItemSearch(
                    SearchIndex='Books',
                    BrowseNode=3550442051,
                    ResponseGroup='Large'
                )
                soup = BeautifulSoup(response, "lxml")
                print("データの取得に成功しました")
                return (soup.findAll("item"))
            except:  # 503エラーが出たら再取得する
                print("再取得しています....")
                time.sleep(3)

    def getAma(self):
        url = "https://www.amazon.co.jp/gp/bestsellers/digital-text/2293143051/"
        htmltext = requests.get(url, timeout=30, verify=False).text
        soup = BeautifulSoup(htmltext, "lxml")

        for el in soup.find_all("div", class_="zg_itemRow"):
            rank = el.find("span", class_="zg_rankNumber").string.strip()
            name = el.find_all("div", class_="p13n-sc-truncate")[0].string.strip()
            price = el.find("span", class_="p13n-sc-price").string.strip()
            print("{} {} {}".format(rank, price, name))

    def getAllCategories(self):
        url = "https://www.amazon.co.jp/gp/site-directory?ref=nav_shopall_btn"
        htmltext = requests.get(url, timeout=30, verify=False).text
        soup = BeautifulSoup(htmltext)

        all_categories =[]
        for el in soup.find_all("div", class_="popover-grouping"):
            category_name = el.find("h2", class_="popover-category-name").string
            sub_category_name = el.find_all(class_="nav_a")
            for ell in sub_category_name:
                all_categories.append([category_name, sub_category_name, "https://www.amazon.co.jp"+ell.get("href"), ell.string])


            #d = pd.DataFrame(all_categories, "category,sub,data")
            #d.to_csv("all_categories1.csv")

            header = ["category", "sub", "url", "data"]
            with open('all_categories.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
                writer.writerow(header)
                writer.writerows(all_categories)


ama = AmazonAccess()
ama.getAllCategories()