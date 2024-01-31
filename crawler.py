import requests
from bs4 import BeautifulSoup

urls = ["https://firstmfg.com/collections/full-mens-catalogue"]
visited_urls = []

# until all pages have been visited
count = 0
while len(urls) != 0:
    # get the page to visit from the list
    current_url = urls.pop() 
    
    # crawling logic
    response = requests.get(current_url)
    # print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    link_elements = soup.select("a[href]")
    for link_element in link_elements:
        url = link_element['href']
        if "/collections/" in url:
  
            print('URL: ', url)
            if url not in visited_urls and url not in urls:
                    urls.append(url)
    if count == 10:
         break
print(urls)
        
#           <a href="/collections/mens-jackets/products/chaos-mens-leather-motorcycle-jacket" class="js-product-details-link">
    
#     <h3>Chaos - Men's Leather Motorcycle Jacket</h3>
#   </a>