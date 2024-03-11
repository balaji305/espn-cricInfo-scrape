import requests
from scrapy import Selector
import csv



filename="Match Input"
with open(f"./Docs/{filename}.csv", "w+", newline='') as f:
    writer = csv.writer(f)
    header = ['Scorecard_url']
    writer.writerow(header)

# #COMMENT THIS FOR TESTING
data=requests.get('https://www.espncricinfo.com/records/year/team-series-results/2024-2024/all-cricket-records-including-minor-cricket-13')
response=Selector(data)
series_table=response.xpath('.//parent::table')
series_urls=series_table.xpath('.//*[contains(@href,"/series/")]/@href').extract()

#UNCOMMENT THIS FOR TESTING
series_urls=["series/england-in-india-2023-24-1389386"]

for url in series_urls:
    series_url=f'https://www.espncricinfo.com/{url}'
    print(series_url)
    data3=requests.get(series_url)
    response3=Selector(data3)
    matchs=response3.xpath('.//*[@class="ds-py-3 ds-px-4"]/a/@href').extract()
    print(matchs)
    for m in matchs:
        scorecard_url='https://www.espncricinfo.com'+m
        print(scorecard_url)
        with open(f"{filename}.csv", "a+", newline='') as f:
            writer = csv.writer(f)
            value = [scorecard_url]
            writer.writerow(value)
    
        
            