import requests
import lxml.html as html 
import datetime
import os
import re
import csv

HOME_URL = "https://www.descubre.vc"
XPATH_LINK_TO_ARTICLE = '//a[@class="block hover:bg-gray-50"]/@href'
XPATH_TITLE = '//h2[@class="text-lg sm:text-xl text-gray-900 font-extrabold tracking-tightwhitespace-pre-line"]/text()'
XPATH_BODY = '//div[@class=" text-gray-700 markdown"]/ul/li/text()'

def parse_notice(link, today, csv_writer):
    try:
        
        response = requests.get(HOME_URL+link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace('\n', '')
                title = sanitize_filename(title)  # Sanitize the title

                body = parsed.xpath(XPATH_BODY)
                csv_writer.writerow([title] + body)
                
                
            except IndexError:
                return

        else:
            raise ValueError(f'Error: {response.status_code}')    
    except ValueError as ve:
        print(ve)
            
            
def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return re.sub(r'[\/:*?"<>|]', '', filename)


def parse_home(page_number, csv_writer): #Get links
    url = f"{HOME_URL}?page={page_number}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            
            
            for link in links_to_notice:
                parse_notice(link, today, csv_writer)   
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    
    num_pages = 60  # Number of pages to scrape
    
    if os.path.exists("Scraped News"): #Checks if the folder exists
        pass
    else:
        print(f"Creating directory: Scraped News") #Creates teh folder
        os.mkdir("Scraped News")
    
    file_path = os.path.join("Scraped News", "scraped_data.csv")
    
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Title', 'Body'])  # Write headers

        for page_number in range(num_pages + 1):
            parse_home(page_number, csv_writer)


if __name__ == '__main__':
    run()
    