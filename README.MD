<h1> A Python Web (Corpus) Scraper </h1>

> As with anything else, I (very naturally) take no responsiblity for what the average internet denizen decides to do with the code or the (daft) antics that ensue. 

**By continuing, you have tacitly agreed to the above.**

A web-scraper written in Python: makes use of Scrapy, BeautifulSoup, PySelenium and a litany of other libraries. Scrapes web-pages, selects the plain text from parsed content and returns output according a set of rules.

This can be considered version **1.0a**. It was still functional last I checked, with the caveat time has broken some of its functionality. 

TwitterScraper:
  > Currently points to and makes use of an outdated version of the Twitter API.
  > Need to be updated to the latest + changes made to align with the new rate-limiting rules.
  > Possibly some other quirks and foibles I've forgotten to mention.
  
  
TumblrScraper:
  > Should work for the most part.
  > Note 1: there are some particular cases (such as the case of private pages potentially) that haven't been handled in the code
  > Note 2: Tumblr recently updated their architeecture to automatically block content they consider NSFW--whether that breaks the
            scraper or not, I do not know. The code currently does not handle this case (easy enough to add though).

NOTE: You _must_ make use of the ChromeDriver executable if you plan to automate using PySelenium. You can get started here: https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver
