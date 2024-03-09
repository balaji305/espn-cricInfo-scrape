def Match_Table_Call():
    #IMPORTS
    import requests
    import json
    import pandas as pd
    from scrapy import Selector
    import mysql.connector
    import sys
    import os

    #OUTPUT FILE
    project_directory = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = open(project_directory + '/Output/Match_Table.txt', 'wt')

    #CONNECTING TO DATABASE
    mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database='cricinfo',
    )
    mycursor = mydb.cursor()

    #QUERY FOR INSERTING DATA INTO DATABASE
    match_updation="""insert into match_table (Match_ID,Match_Type,Match_Date,Ground_ID,Match_Updation,Match_URL) values (%s,%s,%s,%s,%s,%s)"""

    #READING MATCH URL FROM EXCEL FILE
    match_list=list(pd.read_excel('./Docs/Match Input.xlsx')['Match Url'])

    #INSERTING DATA INTO DATABASE
    for i in match_list:
        try:
            data=requests.get(i)
            response=Selector(data)
            m_data=response.xpath('//*[@id="__NEXT_DATA__"]/text()').extract_first()
            match_data=json.loads(m_data)['props']['appPageProps']['data']['match']
            match_id=match_data['objectId']
            date=match_data['startDate']
            match_date=date[0:10]
            ground_id=match_data['ground']['objectId']
            match_type=match_data['internationalClassId']
            if match_type is None:
                match_type=match_data['generalClassId']
            if match_type == 13:
                match_type = 6
            updation='NOT UPDATED'
            value=(match_id,match_type,match_date,ground_id,updation,i)
            mycursor.execute(match_updation,value)
            mydb.commit()
            print("Sucessfully Updated : {}".format(match_id))  
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))  

    #CLOSING DATABASE CONNECTION
    mydb.close()

    #CLOSING OUTPUT FILE
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    
