import requests
import json
import re
import queue
import asyncio
from aiohttp import ClientSession
import mysql.connector
import pymysql
import urllib3
from fake_useragent import UserAgent
urllib3.disable_warnings()


def f(book):
    with requests.get(
        url=f'https://www.douban.com/search?q={book}'
    ) as response:
        print(response.text)


f(book='精进')