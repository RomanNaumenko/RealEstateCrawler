import scrapy
import json
import csv


class DepartmentSpider(scrapy.Spider):
    name = "department"
    start_urls = [
        "https://djursbo.dk/for-boligsoegende/boligsoegning/#ar=&tt=&at=&pr=&wa=&ro=1%253B5&re=null%253B9000&"
        "si=0%253B140&av=false&pe=false&cNo=&dNo=&p=0",
    ]
    headers = {
        'Authority': 'djursbo.dk',
        'Method': 'POST',
        'Path': '/Umbraco/api/TenancySearch/GetSearchResults',
        'Scheme': 'https',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,uk-UA;q=0.8,uk;q=0.7,en-US;q=0.6,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'ASP.NET_SessionId=qg2bxndqdkxwvl5fcppbiq21; CookieConsent={"categoryPreferences":'
                  '[{"cookiePreferences":[{"id":"29d31b2e-0b31-4caa-8113-53e318f436de"},'
                  '{"id":"50e0e825-72d6-47b4-824a-94793930a246"},{"id":"0e36698e-a021-4c19-a2f4-a33c952f2cfd"},'
                  '{"id":"80c60008-d5b7-450a-8f87-bae7345d2729"},{"id":"45cffc2b-b6b3-462a-bf14-c160ad66c7f1"},'
                  '{"id":"697a2159-8635-4379-bf06-cbb08c4eb1a1"}],"id":"5517f432-f173-4d05-b21d-0d4fc41c935a",'
                  '"isSelected":true,"hash":"c6d27436c8d58822e231cb7b0c7c136c"},{"cookiePreferences":'
                  '[{"id":"7b4d6805-d6ca-4ef2-ba88-4c7f873aab67"}],"id":"6f95bec9-4620-4899-bcc6-19c3859113c0",'
                  '"isSelected":false,"hash":"1ab597c7afcafe3a2429e7349e8f227d"},{"cookiePreferences":[],'
                  '"id":"1da611b6-0fa3-44f6-8157-276497d71b16","isSelected":false,'
                  '"hash":"d41d8cd98f00b204e9800998ecf8427e"},{"cookiePreferences":[],'
                  '"id":"cd653bd2-2370-4bec-85b9-058c1c7d5ce4","isSelected":false,'
                  '"hash":"d41d8cd98f00b204e9800998ecf8427e"},{"cookiePreferences":[],'
                  '"id":"710163ab-9b86-417a-81d1-5a42ba462300","isSelected":false,'
                  '"hash":"d41d8cd98f00b204e9800998ecf8427e"}]}',
        'Origin': 'https://djursbo.dk',
        'Pragma': 'no-cache',
        'Referer': 'https://djursbo.dk/for-boligsoegende/boligsoegning/',
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        url = 'https://djursbo.dk/Umbraco/api/TenancySearch/GetSearchResults'
        payload = {}  # Replace this with the actual payload data if necessary(as a dictionary).
        request = scrapy.Request(url, method='POST', headers=self.headers, body=json.dumps(payload),
                                 callback=self.parse_api)

        yield request

    def parse_api(self, response):
        raw_data = response.body
        data = json.loads(raw_data)

        """
        I also implemented the functionality of data storage in csv file.
        With the command 'scrapy crawl department -O departments.json' the data will 
        storage both in csv and json formats. And, of course, one`s functionality will not 
        be changed if other`s will be removed.
        """

        rows = []
        for department in data['Data']['Departments']:

            yield {
                'Title': department['Name'],
                'Address': f"{department['Address']['Street']}, {department['Address']['ZipCode']} {department['Address']['City']}",
                'Rent': f"{department['MinRent']} - {department['MaxRent']}",
                'Size': f"{department['MinSqm']} - {department['MaxSqm']}",
                'Rooms': f"{department['MinRooms']} - {department['MaxRooms']}",
                'Description': department['DepartmentDescription']
            }

            rows.append({
                'Title': department['Name'],
                'Address': f"{department['Address']['Street']} {department['Address']['ZipCode']} {department['Address']['City']}",
                'Rent': f"{department['MinRent']} - {department['MaxRent']}",
                'Size': f"{department['MinSqm']} - {department['MaxSqm']}",
                'Rooms': f"{department['MinRooms']} - {department['MaxRooms']}",
                'Description': department['DepartmentDescription']
            })

        csv_file = 'departments.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Title', 'Address', 'Rent', 'Size', 'Rooms', 'Description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
