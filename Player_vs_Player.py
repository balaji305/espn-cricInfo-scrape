def Player_vs_Player_Call():

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
    df = pd.read_excel("./Docs/Player_vs_Player.xlsx", header=None)

    report = pd.DataFrame(
        columns = ['Player1 ID','Player1 Name','Player2 ID','Player2 Name','Matches','Bat_Innings','Bowl_Innings','Avg Batting_Fantasy', 'Avg Bowling_Fantasy', 'Avg Value_Fantasy' ,'Avg Player_Rank','Avg In_Dream_Team','Avg Captain','Avg Vice_Captain']
    )

    #SUPERSET CATEGORY
    supersetCategory = [5,6,12,17]

    #FUNCTION TO GET SUPERSET CATEGORY
    def get_Superset_Category(match_format):
        if(match_format==5):
            return 2
        elif(match_format==6):
            return 3
        elif(match_format==12):
            return 9
        else:
            return 10

    def get_match_id(player_id, match_type, innings, ground, is_player1):
        query = f"""SELECT Player_Name, Match_ID, Team_ID FROM fantasy_point_table WHERE Player_ID = {player_id}"""
        if(match_type != 0):
            query += f""" AND Match_Type = {match_type}"""
        if(innings == 1 or innings == 2):
            if(is_player1):
                query += f""" AND Innings_Order = {innings}"""
        if(ground != 0):
            query += f""" AND Ground_ID = {ground}"""
        query += ";"
        my_cursor.execute(query)
        results = my_cursor.fetchall()

        match_ids = [result[1] for result in results]
        team_ids = [result[2] for result in results]

        return match_ids, team_ids
    
    def get_player_vs_player_data(player1_id, player2_id, match_type, innings, ground):

        #PLAYER NAMES
        name_query = """SELECT Player_Name from fantasy_point_table WHERE Player_ID = %s"""
        
        my_cursor.execute(name_query, (player1_id,))
        player1_name = my_cursor.fetchall()[0][0]

        my_cursor.execute(name_query, (player2_id,))
        player2_name = my_cursor.fetchall()[0][0]
        
        if(player1_name != None and player2_name != None):
            All_match_ids = []
            All_team_ids = []
            player1_match_team_map = {}
            player2_match_team_map = {}

            player1_ids, player1_teams = get_match_id(player1_id, match_type, innings, ground, True)
            player2_ids, player2_teams = get_match_id(player2_id, match_type, innings, ground, False)
            All_match_ids.append(player1_ids)
            All_match_ids.append(player2_ids)
            All_team_ids.append(player1_teams)
            All_team_ids.append(player2_teams)            

            common_match_ids = list(set(All_match_ids[0]).intersection(*All_match_ids))

            for i in range(len(player1_ids)):
                player1_match_team_map[player1_ids[i]] = player1_teams[i]

            for i in range(len(player2_ids)):
                player2_match_team_map[player2_ids[i]] = player2_teams[i]

            new_All_match_ids = []
            for match_id in common_match_ids:
                if match_id in player1_match_team_map and match_id in player2_match_team_map:
                    if player1_match_team_map[match_id] != player2_match_team_map[match_id]:
                        new_All_match_ids.append(match_id)
                else:
                    print("error")

            common_match_ids = new_All_match_ids
            print(player1_name + " vs " + player2_name + " : " + str(common_match_ids))

            if(len(common_match_ids)!=0):
                if(match_type in supersetCategory):
                    match_types = [match_type]
                    match_types.append(get_Superset_Category(match_type))
                    data_query = f"""SELECT SUM(Bat_Innings), SUM(Bowl_Innings), SUM(Batting_Fantasy), SUM(Bowling_Fantasy), SUM(Value_Fantasy), AVG(Player_Rank), AVG(In_Dream_Team), AVG(Captain), AVG(Vice_Captain) FROM fantasy_point_table WHERE Player_ID = {player1_id} AND Match_ID IN ({','.join(map(str, common_match_ids))}) AND Match_Type IN ({','.join(map(str, match_types))});"""
                else:                                                                                                                                                                                                                                                                                                                 
                    data_query = f"""SELECT SUM(Bat_Innings), SUM(Bowl_Innings), SUM(Batting_Fantasy), SUM(Bowling_Fantasy), SUM(Value_Fantasy), AVG(Player_Rank), AVG(In_Dream_Team), AVG(Captain), AVG(Vice_Captain) FROM fantasy_point_table WHERE Player_ID = {player1_id} AND Match_ID IN ({','.join(map(str, common_match_ids))});"""
                my_cursor.execute(data_query)
                data = my_cursor.fetchall()[0]
                newdata = [0,0,0,0,0,0,0,0,0]
                
                #HANDLE NONE CASE
                for i in range(len(data)):
                    if(data[i]!=None):
                        newdata[i]=data[i]

                data = newdata
                #DECIMAL TO FLOAT
                return [player1_id,player1_name,player2_id,player2_name,len(common_match_ids),int(str(data[0])),int(str(data[1])), 0 if int(str(data[0]))==0 else float(str(data[2]))/int(str(data[0])), float(str(data[3]))/len(common_match_ids), 0 if int(str(data[0]))==0 else float(str(data[4]))/int(str(data[0])), float(str(data[5])), float(str(data[6])), float(str(data[7])), float(str(data[8]))]
            else:
                return [player1_id,player1_name,player2_id,player2_name,0,0,0,0,0,0,0,0,0,0]
        else:
            if(player1_name == None):
                player1_name="Player1 Not Found"
            if(player2_name == None):
                player2_name="Player2 Not Found"
            return [player1_id,player1_name,player2_id,player2_name,'','','','','','','','','','']
    #Iterate every row in the dataframe except first one
    for index, row in df.iterrows():
        #PLAYER1 DETAILS
        player1_url = row.iloc[0]
        player1_id = int(player1_url.split('-')[-1])
        
        #PLAYER2 DETAILS
        player2_url = row.iloc[1]
        player2_id = int(player2_url.split('-')[-1])
        
        #MATCH TYPE
        match_type = int(row.iloc[2])

        #INNINGS
        innings = int(row.iloc[3])

        #GROUND
        ground = int(row.iloc[4])

        #GET DATA
        data = get_player_vs_player_data(player1_id, player2_id, match_type, innings, ground)
        report.loc[index] = data


    pd.set_option('display.max_colwidth', 500)

    #WRITING IN OUTPUT FILE
    excel_writer = pd.ExcelWriter('./Docs/Player_vs_Player_Output.xlsx', engine='xlsxwriter')
    report.to_excel(excel_writer, index=False, sheet_name='PLAYER_VS_PLAYER')
    excel_writer.close()

    # Don't forget to close your cursor and connection when done
    my_cursor.close()
    mydb.close()

    