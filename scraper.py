import requests
import lxml.html as html 
import datetime
import os

HOME_URL = "https://www.descubre.vc/"
XPATH_LINK_TO_ARTICLE = '//a[@class="block hover:bg-gray-50"]/@href'
XPATH_TITLE = '//h2[@class="text-lg sm:text-xl text-gray-900 font-extrabold tracking-tightwhitespace-pre-line"]/text()'
XPATH_BODY = '//div[@class=" text-gray-700 markdown"]/ul/li/text()'

def parse_notice(link,today):
    try:
        
        response = requests.get('https://www.descubre.vc'+link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace('\n', '')
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')    
    except ValueError as ve:
        print(ve)
            


def parse_home(): #Get links
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notice:
                parse_notice(link, today)   
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
    