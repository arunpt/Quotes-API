from bs4 import BeautifulSoup 
import requests
import random


class GoodReads:
    def __init__(self):
        pass

    @staticmethod
    def extract(url):
        results = []
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        for quote in soup.find_all("div", class_= "quote"):
            squote = {}
            squote['text']= quote.find("div", {"class": "quoteText"}).text.replace('\n','').strip()
            squote['author'] = quote.find("span", {"class": "authorOrTitle"}).text.replace('\n','').strip()  
            leftAlignedImage = quote.find("a", {"class": "leftAlignedImage"})
            image = leftAlignedImage.img['src'] if leftAlignedImage else None
            squote['image'] = image
            if image:
                squote["image"] = image.replace("p2", "p8") 
            quoteFooter = quote.find("div", {"class": "quoteFooter"})
            squote['tags'] = [tag.text.strip() for tag in quoteFooter.find_all("a") if tag and "likes" not in tag.text]
            results.append(squote)
        return results

    @property
    def random(self):
        ran_pageNo = random.randint(1, 99)
        baseUrl = f"https://www.goodreads.com/quotes?format=html&mobile_xhr=1&page={ran_pageNo}"
        results = GoodReads.extract(baseUrl) 
        return results[random.randint(0, len(results))]
        
        
    @staticmethod
    def search_all(search_query, pages=1):
        res = []
        for page in range(1, pages + 1):
            baseUrl = f"https://www.goodreads.com/quotes/search?commit=Search&page={page}&q={search_query.replace(' ', '+')}&utf8=%E2%9C%93"
            results = GoodReads.extract(baseUrl)
            res.extend(results)   
        return res
