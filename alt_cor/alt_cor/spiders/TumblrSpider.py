#############################################
# Author: Zeeshan Shahid                    #
# Last edited: 19-09-2016                   #
############################################

import sys, time, re, uuid, random
from scrapy.selector import Selector
from scrapy.spiders import Spider
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Constants//Depth levels to crawl
GROUNDFLOOR = 2
BASEMENT = 30 # Must be greater than 3!
PLACES = 30 # Must be greater than 2!
HOME = "thewritershandbook" #the user-name for the base_url

class TumblrSpider(Spider):
        name = "tumblrcrawl"
        allowed_domains = ["www.tumblr.com"]
        start_urls = ["http://copygirlofficial.tumblr.com/"] # some related tumblr url

        def __init__(self):
                chromeOptions = webdriver.ChromeOptions()
                prefs = {"profile.managed_default_content_settings.images":2}
                chromeOptions.add_experimental_option("prefs", prefs)
                self.driver = webdriver.Chrome('D:\GitHub\chromedriver.exe', chrome_options = chromeOptions)

                self.driver.implicitly_wait(30)
                self.base_url = "http://writing-questions-answered.tumblr.com/" #"https://thewritershandbook.tumblr.com/" #"https://www.tumblr.com/explore/trending"
                self.verificationErrors = []
                self.accept_next_alert = True

        def parse(self, response):
            try:
                past = []
                random_url = self.base_url

                outname = "output__tumblr__text.txt" # + str(uuid.uuid4().hex) + ".txt"
                for buildings in range(1, (PLACES+1)):
                    self.driver.get(random_url)

                    #Note to self: https://www.tumblr.com/blog_auth/anonymous is a variation on the case below,
                    #handle it later.

                    if("login_required" in self.driver.current_url): # or "anonymous" in self.driver.current_url): #<-- This way?
                        try:
                            random_url = random.choice(past)
                        except IndexError:
                            random_url = self.base_url # go home and try again
                    else:
                        pass

                    floors = GROUNDFLOOR
                    collect, yuarells = "", []
                    whale_killer = False
                    while ((floors < (BASEMENT+1)) and (not whale_killer)):
                        try:
                            site = Selector(text=self.driver.page_source)
                            content = site.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "post-content", " " ))]//text() | //*[(@id = "150547630873")]//p//text() | //blockquote//p//text() | //p//text() | //*[(@id = "stat-articles")]//section//p//text() | //*[contains(concat( " ", @class, " " ), concat( " ", "post_content_inner", " " ))]//text() | //p//text() | //li//text() | //h2//text() | //*[contains(concat( " ", @class, " " ), concat( " ", "odd", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "source", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "quote", " " ))]//p//*[contains(concat( " ", @class, " " ), concat( " ", "q", " " ))]//text() | //*[contains(concat( " ", @class, " " ), concat( " ", "asker-question", " " ))]//text() | //*[contains(concat( " ", @class, " " ), concat( " ", "q", " " ))]//text() | //*[contains(concat( " ", @class, " " ), concat( " ", "post_info", " " ))]//text()').extract()

                            # perhaps add error handling for 'Anonymous asks' -- for the time being doing it above
                            # before navigating to urls by detecing any white-space
                            collect = site.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "tumblr_blog", " " ))]//text() | //*[contains(concat( " ", @class, " " ), concat( " ", "asker", " " ))]//text()').extract()

                            print "floor_" + str(floors) + "\t" + str(collect) # DEBUG

                            # Here! This is (was?) where the bias's getting introduced
                            collect = list(set(collect)) #remove repeats
                            if(collect):
                                for i in range(0, len(collect)):
                                    if (not " " in collect[i]):
                                        collect[i] = collect[i].rstrip("\r\n\t")
                                    else:
                                        continue

                                for yuar in collect:
                                    try:
                                        if yuar != None:
                                            yuarells.append(yuar.encode("utf-8"))
                                            yuarells = filter (None, yuarells)
                                    except:
                                        continue
                            else:
                                yuarells.append(HOME) #exit dead-end by going home--and trying again

                            random.shuffle(yuarells)
                            content = [x.rstrip() for x in content]
                            with open(outname, "a") as result:
                                for item in content:
                                    just_text = BeautifulSoup(item, "lxml").get_text().rstrip().encode('utf-8')
                                    result.write(just_text + "\r\n")

                            if(random_url.endswith("/")):
                                next_page = random_url + "page/" + str(floors)
                            else:
                                next_page = random_url + "/page/" + str(floors)
                            self.driver.get(next_page)
                            floors += 1 # into the void

                        except NoSuchElementException:
                            whale_killer = True # exit while
                            continue

                    print yuarells # DEBUG
                    if(yuarells):
                        temp = "http://" + random.choice(yuarells) + ".tumblr.com"
                        while(temp == random_url):
                            print "Loopy hell!" #DEBUG
                            temp = "http://" + random.choice(yuarells) + ".tumblr.com"
                            if(all(urls in past for urls in yuarells)):
                                temp = self.base_url
                                break
                    else:
                        try:
                            random.shuffle(past)
                            temp = random.choice(past)
                        except IndexError:
                            temp = self.base_url # go home and try again
                    past.append(temp)
                    random_url = temp
                    print random_url #DEBUG
                print past #DEBUG
                self.driver.close()

            except:
                    print "Error", sys.exc_info()[0]
                    raise #do nothing for now



""" ### Miscellaneous and Other ###
    # Go down a Twitter dash until you get to the end:
    while True:
        elemsCount = self.driver.execute_script("return document.querySelectorAll('.stream-items > li.stream-item').length")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.25)

        try:
            WebDriverWait(self.driver, 30).until(
                lambda x: x.find_element_by_xpath("//*[contains(@class,'stream-items')]/li[contains(@class,'stream-item')]["+str(elemsCount+1)+"]"))
        except:
            break

    site = Selector(text=self.driver.page_source)
    content = site.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "tweet-text", " " ))]//text()').extract()
    content = [x.rstrip() for x in content]

    outname = "output_" + str(uuid.uuid4().hex) + ".txt"
    with open(outname, "wb") as result:
        for item in content:
            just_text = BeautifulSoup(item, "lxml").get_text().rstrip().encode('utf-8')
            result.write(just_text) #+ "\r\n")
"""
