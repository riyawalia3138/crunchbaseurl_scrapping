import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import urllib.parse
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
import faker

fake = faker.Faker()

df = pd.read_csv('sample.csv')
URLs = df['page'].tolist()
options = Options()                                                         
proxy_ip_port = '190.61.88.147:8080'                                                                                                                                           
proxy = Proxy()                                                                                                                        
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)
path = 'C:/Users/ASUS/Desktop/web/beautiful_soup/chromedriver.exe'

final_list = []

for link in URLs:
    
    # Generate fake user details
    fake_user = {
        'name': fake.name(),
        'email': fake.email(),
        'username': fake.user_name(),
        'password': fake.password(),
    }
    
    print('Fake User:', fake_user)
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(link)
    time.sleep(6)
    html_source = driver.page_source

    soup = BeautifulSoup(html_source, "html.parser")
    div = soup.find('div', {'class': 'main-content'})
    with open('field_formatter.txt', 'w', encoding='utf-8') as file:
        file.write(str(div))

    Company = soup.find('h1', {'class': 'profile-name'}).text
    print('Company_name----->', Company)
    Crunchbase = link
    print('Company_link--------->', Crunchbase)

    dic_1 = {
        'Company Name': Company,
        'Company Url': Crunchbase
    }
    print(dic_1)

    links_with_text = [(a.get('href'), a.text) for a in div.find_all('a')]
    if not links_with_text:
        print(f"No FOUNDER found")
        pass
    specific_keyword = 'person'
    filtered_links_with_text = [(href, text) for href, text in links_with_text if href is not None and specific_keyword in href]
    f_list = []
    count = 1
    for href, text in filtered_links_with_text:
        fulldic = {}
        ndic= {}
        fulldic[f'founder{count}'] = text
        ndic[f'founder{count}'] = text
        base_url = 'https://www.crunchbase.com'
        full_url = urllib.parse.urljoin(base_url, href)
        fulldic[f'link'] = full_url
        f_list.append(fulldic)
        count += 1

    count = 1
    dic_2 = {}
    driver.quit()
    time.sleep(5)
    for n_link in f_list:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(n_link["link"])
        time.sleep(5)
        html_source = driver.page_source

        soup = BeautifulSoup(html_source, "html.parser")
        div = soup.find('a', {'title': 'View on LinkedIn'})
        if not div:
            print(f"No link found")
            ndic[f'founder{count}'] = text
            del n_link['link']
            n_link[f'linkedin{count}'] = ("No Links Available")
            dic_2.update(ndic)
            dic_2.update(n_link)
            count += 1
            time.sleep(5)
            driver.quit()
            continue
        href = div.get('href')
        del n_link['link']
        n_link[f'linkedin{count}'] = href
        dic_2.update(n_link)
        count += 1
        driver.quit()
        time.sleep(5)

    print(dic_2)
    final = (dic_1 | dic_2)
    final_list.append(final)
    df = pd.DataFrame(final_list)
    print(df)
    df.to_csv(r'finall7000_8000.csv', sep=',', encoding='utf-8-sig', index=False)