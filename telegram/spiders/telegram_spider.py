import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html
import time


class TelegramSpider(scrapy.Spider):
    name = "telegram"
    detail_url = "https://www.flashscores.co.uk/match/%s/#match-summary"
    history = []
    user_name = []

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")
        fp = open("res.json", "a")
        fp.close()


    def start_requests(self):
        self.driver.get('https://web.telegram.org/#/im?p=u777000_12086136118423149707')

        raw_input("prompt") 

        source = self.driver.page_source.encode("utf8")
        tree = html.fromstring(source)
        open("res.html", "wb").write(source)

        index = 0
        while(1):
            for idx in range(0, 10):
                flag = 0
                try:
                    scroll = self.driver.find_element_by_xpath('//div[@class="im_history_message_wrap"]//a[contains(@class, "im_message_author")]')
                    scroll.click()
                    # scroll.send_keys(Keys.NULL)
                    # self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll)

                    close = self.driver.find_element_by_xpath('//div[@class="modal_close_wrap"]')
                    close.click()
                    time.sleep(2)
                    flag = 1
                except Exception as e: 
                    print(e)

                try:
                    if flag == 0:
                        close = self.driver.find_element_by_xpath('//div[@class="modal_close_wrap"]')
                        close.click()
                        time.sleep(2)
                except:
                    pass

            try:
                self.driver.find_element_by_xpath('//a[@class="btn btn-md btn-md-primary im_edit_cancel_link"]').click()
            except:
                pass

            try:
                
                users = tree.xpath('//div[@class="im_history_message_wrap"]//a[contains(@class, "im_message_author")]')
                elements = self.driver.find_elements_by_xpath('//div[@class="im_history_message_wrap"]//a[contains(@class, "im_message_author")]')
            except Exception as e:
                print "error: ??????????????"
                print(e)
            

            for idx in range(0, 500):
                if idx >= len(users):
                    break
                name = self.validate(users[idx].xpath("./text()"))
                print "existed name: ",  name
                if name != "" and name not in self.history:
                    try:
                        self.history.append(name)
                        elements[idx].click()
                        time.sleep(1)
                        print "new name: ", name
                        source = self.driver.page_source.encode("utf8")
                        tp_tree = html.fromstring(source)
                        username = self.validate(tp_tree.xpath("//div[@class='md_modal_section_param_value']//span/text()"))
                        if username != "":
                            self.user_name.append(username)
                            print "#" * 20
                            print username

                        self.driver.find_element_by_xpath('//div[@class="modal_close_wrap"]').click()
                    except Exception as e: 
                        print(e)

                    try:
                        self.driver.find_element_by_xpath('//div[@class="modal_close_wrap"]').click()
                    except:
                        pass

            time.sleep(1)

    def validate(self, xpath_obj):
        try:
            xpath_obj = [tp.strip() for tp in xpath_obj if tp.strip()!=""]
            return xpath_obj[0].strip()
        except:
            return ""

