from re import I
from bs4 import BeautifulSoup
import requests
import csv
from fake_useragent import UserAgent


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
ua=UserAgent()
hdr = {'User-Agent': ua.random,
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

csv_header = ["Company", "Website", "Rating", "Reviews", "Min Project Size", "Hourly Rate", "Employee Size", "Location"]

objects_list = [[]]

url1 = "https://clutch.co/directory/"
url = "https://clutch.co/"

url_suffix = ''

#print("Pick a category\n")
#category_choice = int(input("1. Development\n 2. Design & Production\n 3. Marketing\n 4. Advertising\n 5. Business Services\n 6. IT Services\n"))

print("Pick the option you want to scrape:")
#if category_choice == 1:
choice = int(input(" 1. Mobile App development \n 2. Software Development \n 3. Web Development \n 4. AR/VR \n 5. Artificial Intelligence \n 6. Blockchain\n"))
if choice == 1:
    url_suffix = 'mobile-application-developers'
elif choice == 2:
    url_suffix = 'developers'
elif choice == 3:
    url_suffix = 'web-developers'
elif choice == 4:
    url_suffix = 'virtual-reality'
elif choice == 5:
    url_suffix = 'artificial-intelligence'
elif choice == 6:
    url_suffix = 'blockchain'
else:
    print("Invalid choice selected!!!")                        

num_of_pages = int(input("How many pages do you want to scrape? >=1 \n   "))

if choice == 1:
    final_url = url1+url_suffix
elif choice == 2 or choice == 3:
    final_url = url+url_suffix
elif choice == 4 or choice == 5 or choice == 6:
    final_url = url+'developers/'+url_suffix     
else:
    print("Invalid choice!!!")      

#print(final_url)

req = requests.get(final_url, headers=hdr)

#print(req.status_code)

soup = BeautifulSoup(req.text, "lxml")

list_of_objects = soup.find("ul", {"class": "directory-list shortlist"})
 
for item in list_of_objects.find_all('li', {"class": "provider provider-row sponsor"}):
    row = []
    company = item.find('h3', {"class": "company_info"}).text
    website = item.find('a', {"class": "website-link__item"})['href']
    rating = item.find('span', {"class": "rating sg-rating__number"}).text
    reviews = item.find('a', {"class": "reviews-link sg-rating__reviews"}).text
    min_project_size = item.find('div', {"class": "list-item block_tag custom_popover"}).text
    hourly_rate = item.find_all('div', {"class": "list-item custom_popover"})[0].text
    employee_size = item.find_all('div', {"class": "list-item custom_popover"})[1].text
    location = item.find_all('div', {"class": "list-item custom_popover"})[2].text
    row.extend((company, website, rating, reviews, min_project_size, hourly_rate, employee_size, location))

    objects_list.append(row)

if num_of_pages > 1:
    i = 1
    while i < num_of_pages:
        next_page_url = final_url+"?page="+str(i)
        req = requests.get(final_url, headers=hdr)
        soup = BeautifulSoup(req.text, "lxml")
        list_of_objects = soup.find("ul", {"class": "directory-list shortlist"})

        for item in list_of_objects.find_all('li', {"class": "provider provider-row sponsor"}):
            row = []
            company = item.find('h3', {"class": "company_info"}).text
            website = item.find('a', {"class": "website-link__item"})['href']
            rating = item.find('span', {"class": "rating sg-rating__number"}).text
            reviews = item.find('a', {"class": "reviews-link sg-rating__reviews"}).text
            min_project_size = item.find('div', {"class": "list-item block_tag custom_popover"}).text
            hourly_rate = item.find_all('div', {"class": "list-item custom_popover"})[0].text
            employee_size = item.find_all('div', {"class": "list-item custom_popover"})[1].text
            location = item.find_all('div', {"class": "list-item custom_popover"})[2].text
            row.extend((company, website, rating, reviews, min_project_size, hourly_rate, employee_size, location))

            objects_list.append(row)

with open('clutch.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(objects_list)

