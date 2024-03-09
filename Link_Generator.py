import requests
from scrapy import Selector
import json
import csv



filename="Match Input"
with open(f"{filename}.csv", "w+", newline='') as f:
    writer = csv.writer(f)
    header = ['Team1','Team2','Status','Match_Type','Scorecard_url']
    writer.writerow(header)

# #COMMENT THIS FOR TESTING
# data=requests.get('https://stats.espncricinfo.com/ci/engine/records/team/series_results.html?class=13;id=2023;type=year')
# response=Selector(data)
# series_table=response.xpath('.//parent::table')
# series_urls=series_table.xpath('.//*[contains(@href,"/series/")]/@href').extract()

#UNCOMMENT THIS FOR TESTING
series_urls=["series/icc-cricket-world-cup-2023-24-1367856/match-schedule-fixtures-and-results"]

for url in series_urls:
    series_url=f'https://www.espncricinfo.com/{url}'
    print(series_url)
    data3=requests.get(series_url)
    response3=Selector(data3)
    matchs=response3.xpath('.//*[contains(@class,"ds-p-4 hover:ds-bg-ui-fill-translucent")]')
    for m in matchs:
        teams=m.xpath('.//*[@class="ds-flex ds-items-center ds-min-w-0 ds-mr-1"]/p/text()').extract()
        status=m.xpath('.//*[@class="ds-text-tight-s ds-font-regular ds-line-clamp-2 ds-text-typo"]/span/text()').extract_first()
        scorecard =m.xpath('.//a/@href').extract_first()
        team1=teams[0]
        team2=teams[-1]
        scorecard_url='https://www.espncricinfo.com'+scorecard
        print(scorecard_url)
        data4=requests.get(scorecard_url)
        response4=Selector(data4)
        m_data=response4.xpath('//*[@id="__NEXT_DATA__"]/text()').extract_first()
        match_data=json.loads(m_data)['props']['appPageProps']['data']['match']
        match_type=match_data['internationalClassId']
        if match_type is None:
            match_type=match_data['generalClassId']
        if(match_type==13):
            match_type=6
        if(match_type==2 or match_type==5 or match_type==3 or match_type==6 or match_type==9 or match_type==12 or match_type==10 or match_type==17):
            if(status is None):
                continue
            elif('walkover' not in status and ('won' in status or 'tied' in status)):
                with open(f"{filename}.csv", "a+", newline='') as f:
                    writer = csv.writer(f)
                    value = [team1,team2,status,match_type,scorecard_url]
                    writer.writerow(value)
            