def Bat_vs_Bowl_Call():

    import pandas as pd
    import numpy as np
    import mysql.connector
    
    #CONNECTING TO DATABASE
    mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database='cricinfo',
    )
    my_cursor = mydb.cursor()

    # Read the CSV file
    df = pd.read_csv("./Docs/Bat_vs_Bowl.csv", header=None)

    report = pd.DataFrame(
        columns = ['Player ID','Player Name','Matches','Batted Matches','Average Batting_Fantasy', 'Average Value_Fantasy' ,'Average Player_Rank','Average In_Dream_Team','Average Captain','Average Vice_Captain']
    )

    def get_match_id(player_id, match_type, innings, ground):
        query = f"""SELECT Player_Name, Match_ID FROM fantasy_point_table WHERE Player_ID = {player_id}"""
        if(match_type != 0):
            query += f""" AND Match_Type = {match_type}"""
        if(innings == 1 or innings == 2):
            query += f""" AND Innings_Order = {innings}"""
        if(ground != 0):
            query += f""" AND Ground_ID = {ground}"""
        query += ";"

        my_cursor.execute(query)
        results = my_cursor.fetchall()

        match_ids = [result[1] for result in results]
        return match_ids
    
    #Iterate every row in the dataframe except first one
    for index, row in df.iterrows():
        # Extracting batsman_id
        batsman_url = row.iloc[0]
        batsman_id = int(batsman_url.split('-')[-1])
        
        bowlers_id = []

        no_of_bowlers = int(row.iloc[1])

        for i in range(no_of_bowlers):
            bowler_url = row.iloc[2 + i]
            bowler_id = int(bowler_url.split('-')[-1])
            bowlers_id.append(bowler_id)
        
        # Extracting match details
        match_type = int(row.iloc[2 + no_of_bowlers])
        innings = int(row.iloc[3 + no_of_bowlers])
        ground = int(row.iloc[4 + no_of_bowlers])

        #Batsman Name
        name_query = f"""SELECT Player_Name from fantasy_point_table WHERE Player_ID = {batsman_id}"""
        my_cursor.execute(name_query)
        name = my_cursor.fetchall()
        if(len(name)!=0):
            name=name[0][0]
            All_match_ids = []

            All_match_ids.append(get_match_id(batsman_id, match_type, innings, ground))
            for bowler_id in bowlers_id:
                All_match_ids.append(get_match_id(bowler_id, match_type, innings, ground))

            # Find the common match_ids
            common_match_ids = list(set(All_match_ids[0]).intersection(*All_match_ids))

            if(len(common_match_ids)!=0):
                #Collect the data
                data_query = f"""SELECT SUM(Bat_Innings), AVG(Batting_Fantasy), AVG(Value_Fantasy), AVG(Player_Rank), AVG(In_Dream_Team), AVG(Captain), AVG(Vice_Captain) FROM fantasy_point_table WHERE Player_ID = {batsman_id} AND Bat_Innings = 1 AND Match_ID IN ({','.join(map(str, common_match_ids))});"""
                my_cursor.execute(data_query)
                data = my_cursor.fetchall()[0]
                print(data)

                # report.loc[i] = [batsman_id,name,len(common_match_ids),int(str(data[0][0])),str(data[0][1]),str(data[0][2]),str(data[0][3]),str(data[0][4]),str(data[0][5]),str(data[0][6])]
                # report.loc[i] = [batsman_id,name,len(common_match_ids),data[0],data[1],str(data[2]),str(data[3]),str(data[4]),str(data[5]),str(data[6])]
                #DECIMAL TO FLOAT
                report.loc[i] = [batsman_id,name,len(common_match_ids),int(str(data[0])),float(str(data[1])),float(str(data[2])),float(str(data[3])),float(str(data[4])),float(str(data[5])),float(str(data[6]))]
            else:
                report.loc[i] = [batsman_id,name,0,0,0,0,0,0,0,0]
        else:
            name="Batsman Not Found"
            report.loc[i] = [batsman_id,name,'','','','','','','','']

    pd.set_option('display.max_colwidth', 500)

    #WRITING IN OUTPUT FILE
    excel_writer = pd.ExcelWriter('./Docs/Bat_vs_Bowl_Output.xlsx', engine='xlsxwriter')
    report.to_excel(excel_writer, index=False, sheet_name='BAT_VS_BOWL')
    excel_writer.close()

    # Don't forget to close your cursor and connection when done
    my_cursor.close()
    mydb.close()

            



    

