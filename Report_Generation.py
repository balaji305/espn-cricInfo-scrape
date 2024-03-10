def Report_Generation_Call():
    #IMPORTS
    import requests
    import json
    import pandas as pd
    import mysql.connector


    #CONNECTING TO DATABASE
    mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database='cricinfo',
    )
    my_cursor = mydb.cursor()
    
    #READ INPUT FILE
    input_data = pd.read_excel("./Docs/Report Input.xlsx",sheet_name='Sheet1',header=0)
    # player_url = list(input_data['Player URL'])
    player_id = list(input_data['Player ID'])
    innings_order = list(input_data['Innings Order'])
    ground_id = list(input_data['Ground ID'])
    opponent_id = list(input_data['Opponent ID'])
    match_format = list(input_data['Match Format'])
    normal = list(input_data['Normal'])
    ground = list(input_data['Ground'])
    h2h = list(input_data['H2H'])
    form = list(input_data['Form'])
    international = list(input_data['International'])
    days = list(input_data['Days'])

    #REPORTS DATAFRAME
    report_1 = pd.DataFrame(
        columns = ['Player ID','Player Name','Innings Order','Matches','Average Player Rank','Value Points','In_Dream_Team','Captain','Vice_Captain','PPG','DT PERCENT','CAP PERCENT','VCAP PERCENT','EXPECTED PTS','CAP CHANCE']
    )
    report_2 = pd.DataFrame(
        columns = ['Player ID','Player Name','Innings Order','Matches','Average Player Rank','Value Points','In_Dream_Team','Captain','Vice_Captain','PPG','DT PERCENT','CAP PERCENT','VCAP PERCENT','EXPECTED PTS','CAP CHANCE']
    )
    report_3 = pd.DataFrame(
        columns = ['Player ID','Player Name','Innings Order','Matches','Average Player Rank','Value Points','In_Dream_Team','Captain','Vice_Captain','PPG','DT PERCENT','CAP PERCENT','VCAP PERCENT','EXPECTED PTS','CAP CHANCE']
    )
    report_4 = pd.DataFrame(
        columns = ['Player ID','Player Name','Innings Order','Matches','Average Player Rank','Value Points','In_Dream_Team','Captain','Vice_Captain','PPG','DT PERCENT','CAP PERCENT','VCAP PERCENT','EXPECTED PTS','CAP CHANCE']
    )
    report_5 = pd.DataFrame(
        columns = ['Player ID','Player Name','Innings Order','Matches','Average Player Rank','Value Points','In_Dream_Team','Captain','Vice_Captain','PPG','DT PERCENT','CAP PERCENT','VCAP PERCENT','EXPECTED PTS','CAP CHANCE']
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

    for i in range(len(player_id)):
        # player_id.append(player_url[i].split('-')[-1])
        player_id[i] = int(player_id[i])
        innings_order[i] = int(innings_order[i])
        ground_id[i] = int(ground_id[i])
        opponent_id[i] = int(opponent_id[i])
        match_format[i] = int(match_format[i])

        #QUERY FOR CHECKING IN PLAYER TABLE
        query = """select * from player_table where Player_ID = %s and Match_Type = %s"""
        value = (player_id[i],match_format[i])
        my_cursor.execute(query,value)
        result = my_cursor.fetchall()
        name = 'Player Not Found'

        if(len(result) == 0):
            query_t = """select Player_Name from player_table where Player_ID = %s"""
            value_t = (player_id[i],)
            my_cursor.execute(query_t,value_t)
            result_t = my_cursor.fetchall()
            if(len(result_t) > 0):
                name = result_t[0][0]

        report_1.loc[i] = [player_id[i],name,innings_order[i],'','','','','','','','','','','','']
        report_2.loc[i] = [player_id[i],name,innings_order[i],'','','','','','','','','','','','']
        report_3.loc[i] = [player_id[i],name,innings_order[i],'','','','','','','','','','','','']
        report_4.loc[i] = [player_id[i],name,innings_order[i],'','','','','','','','','','','','']
        report_5.loc[i] = [player_id[i],name,innings_order[i],'','','','','','','','','','','','']

        if(international[i]==1 and match_format[i] in supersetCategory):
            if(innings_order[i] == 3):
                query5 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                where Player_ID = %s and Match_Type = %s and Ground_ID = %s and Opponent_Team_ID = %s"""
                value5 = (player_id[i],get_Superset_Category(match_format[i]),ground_id[i],opponent_id[i])
            else:
                query5 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                where Player_ID = %s and Match_Type = %s and Innings_Order = %s and Ground_ID = %s and Opponent_Team_ID = %s"""
                value5 = (player_id[i],get_Superset_Category(match_format[i]),innings_order[i],ground_id[i],opponent_id[i])
            
            my_cursor.execute(query5,value5)
            result5 = my_cursor.fetchall()
            if(result5[0][0] == None):
                report_5.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
            else:
                rank_avg = int(str(result5[0][1]))/int(str(result5[0][0]))
                ppg = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][2]))/int(str(result5[0][0]))
                dt_percent = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][3]))/int(str(result5[0][0]))
                cap_percent = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][4]))/int(str(result5[0][0]))
                vcap_percent = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][5]))/int(str(result5[0][0]))
                expected_pts = ppg*dt_percent + ppg*cap_percent + ppg*vcap_percent*0.5
                cap_chance = cap_percent + vcap_percent
                report_5.loc[i] = [player_id[i],result[0][2],innings_order[i],int(str(result5[0][0])),rank_avg,int(str(result5[0][2])),int(str(result5[0][3])),int(str(result5[0][4])),int(str(result5[0][5])),ppg,dt_percent,cap_percent,vcap_percent,expected_pts,cap_chance]
   

        if(len(result) > 0):
            #QUERY FOR REPORT 1
            if(normal[i]==1 and match_format[i] in supersetCategory):
                if(innings_order[i] == 3):
                    query1 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type in (%s, %s)"""
                    value1 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]))
                else:
                    query1 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type in (%s, %s) and Innings_Order = %s"""
                    value1 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]),innings_order[i])
            else:
                if(innings_order[i] == 3):
                    query1 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s"""
                    value1 = (player_id[i],match_format[i])
                else:
                    query1 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s and Innings_Order = %s"""
                    value1 = (player_id[i],match_format[i],innings_order[i])

            my_cursor.execute(query1,value1)
            result1 = my_cursor.fetchall()
            if(result1[0][0] == None):
                report_1.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
            else:
                rank_avg = int(str(result1[0][1]))/int(str(result1[0][0]))
                ppg = 0 if int(str(result1[0][2])) == 0 else int(str(result1[0][2]))/int(str(result1[0][0]))
                dt_percent = 0 if int(str(result1[0][2])) == 0 else int(str(result1[0][3]))/int(str(result1[0][0]))
                cap_percent = 0 if int(str(result1[0][2])) == 0 else int(str(result1[0][4]))/int(str(result1[0][0]))
                vcap_percent = 0 if int(str(result1[0][2])) == 0 else int(str(result1[0][5]))/int(str(result1[0][0]))
                expected_pts = ppg*dt_percent + ppg*cap_percent + ppg*vcap_percent*0.5
                cap_chance = cap_percent + vcap_percent
                report_1.loc[i] = [player_id[i],result[0][2],innings_order[i],int(str(result1[0][0])),rank_avg,int(str(result1[0][2])),int(str(result1[0][3])),int(str(result1[0][4])),int(str(result1[0][5])),ppg,dt_percent,cap_percent,vcap_percent,expected_pts,cap_chance]
            
            #QUERY FOR REPORT 2
            if(ground[i]==1 and match_format[i] in supersetCategory):
                if(innings_order[i] == 3):
                    query2 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type in (%s, %s) and Ground_ID = %s"""
                    value2 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]),ground_id[i])
                else:
                    query2 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type in (%s, %s) and Innings_Order = %s and Ground_ID = %s"""
                    value2 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]),innings_order[i],ground_id[i])
            else:
                if(innings_order[i] == 3):
                    query2 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s and Ground_ID = %s"""
                    value2 = (player_id[i],match_format[i],ground_id[i])
                else:
                    query2 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s and Innings_Order = %s and Ground_ID = %s"""
                    value2 = (player_id[i],match_format[i],innings_order[i],ground_id[i])
            my_cursor.execute(query2,value2)
            result2 = my_cursor.fetchall()
            if(result2[0][0] == None):
                report_2.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
            else:
                rank_avg = int(str(result2[0][1]))/int(str(result2[0][0]))
                ppg = 0 if int(str(result2[0][2])) == 0 else int(str(result2[0][2]))/int(str(result2[0][0]))
                dt_percent = 0 if int(str(result2[0][2])) == 0 else int(str(result2[0][3]))/int(str(result2[0][0]))
                cap_percent = 0 if int(str(result2[0][2])) == 0 else int(str(result2[0][4]))/int(str(result2[0][0]))
                vcap_percent = 0 if int(str(result2[0][2])) == 0 else int(str(result2[0][5]))/int(str(result2[0][0]))
                expected_pts = ppg*dt_percent + ppg*cap_percent + ppg*vcap_percent*0.5
                cap_chance = cap_percent + vcap_percent
                report_2.loc[i] = [player_id[i],result[0][2],innings_order[i],int(str(result2[0][0])),rank_avg,int(str(result2[0][2])),int(str(result2[0][3])),int(str(result2[0][4])),int(str(result2[0][5])),ppg,dt_percent,cap_percent,vcap_percent,expected_pts,cap_chance]
                
            #QUERY FOR REPORT 3
            if(h2h[i]==1 and match_format[i] in supersetCategory):
                if(innings_order[i] == 3):
                    query3 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type in (%s, %s) and Opponent_Team_ID = %s"""
                    value3 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]),opponent_id[i])
                else:
                    query3 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type in (%s, %s) and Innings_Order = %s and Opponent_Team_ID = %s"""
                    value3 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]),innings_order[i],opponent_id[i])
            else:
                if(innings_order[i] == 3):
                    query3 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s and Opponent_Team_ID = %s"""
                    value3 = (player_id[i],match_format[i],opponent_id[i])
                else:
                    query3 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s and Innings_Order = %s and Opponent_Team_ID = %s"""
                    value3 = (player_id[i],match_format[i],innings_order[i],opponent_id[i])
            my_cursor.execute(query3,value3)
            result3 = my_cursor.fetchall()
            if(result3[0][0] == None):
                report_3.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
            else:
                rank_avg = int(str(result3[0][1]))/int(str(result3[0][0]))
                ppg = 0 if int(str(result3[0][2])) == 0 else int(str(result3[0][2]))/int(str(result3[0][0]))
                dt_percent = 0 if int(str(result3[0][2])) == 0 else int(str(result3[0][3]))/int(str(result3[0][0]))
                cap_percent = 0 if int(str(result3[0][2])) == 0 else int(str(result3[0][4]))/int(str(result3[0][0]))
                vcap_percent = 0 if int(str(result3[0][2])) == 0 else int(str(result3[0][5]))/int(str(result3[0][0]))
                expected_pts = ppg*dt_percent + ppg*cap_percent + ppg*vcap_percent*0.5
                cap_chance = cap_percent + vcap_percent
                report_3.loc[i] = [player_id[i],result[0][2],innings_order[i],int(str(result3[0][0])),rank_avg,int(str(result3[0][2])),int(str(result3[0][3])),int(str(result3[0][4])),int(str(result3[0][5])),ppg,dt_percent,cap_percent,vcap_percent,expected_pts,cap_chance]
                
            #QUERY FOR REPORT 4
            if(form[i]==0):
                report_4.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
            else:
                if(match_format[i] in supersetCategory):
                    if(innings_order[i] == 3):
                        query4 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                        where Player_ID = %s and Match_Type in (%s, %s) and Ground_ID = %s and Opponent_Team_ID = %s and Match_Date > DATE_SUB(NOW(), INTERVAL %s DAY)"""
                        value4 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]),ground_id[i],opponent_id[i],days[i])
                    else:
                        query4 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                        where Player_ID = %s and Match_Type in (%s, %s) and Innings_Order = %s and Ground_ID = %s and Opponent_Team_ID = %s and Match_Date > DATE_SUB(NOW(), INTERVAL %s DAY)"""
                        value4 = (player_id[i],match_format[i],get_Superset_Category(match_format[i]),innings_order[i],ground_id[i],opponent_id[i],days[i])
                else:
                    if(innings_order[i] == 3):
                        query4 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                        where Player_ID = %s and Match_Type = %s and Ground_ID = %s and Opponent_Team_ID = %s and Match_Date > DATE_SUB(NOW(), INTERVAL %s DAY)"""
                        value4 = (player_id[i],match_format[i],ground_id[i],opponent_id[i],days[i])
                    else:
                        query4 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                        where Player_ID = %s and Match_Type = %s and Innings_Order = %s and Ground_ID = %s and Opponent_Team_ID = %s and Match_Date > DATE_SUB(NOW(), INTERVAL %s DAY)"""
                        value4 = (player_id[i],match_format[i],innings_order[i],ground_id[i],opponent_id[i],days[i])

                my_cursor.execute(query4,value4)
                result4 = my_cursor.fetchall()
                if(result4[0][0] == None):
                    report_4.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
                else:
                    rank_avg = int(str(result4[0][1]))/int(str(result4[0][0]))
                    ppg = 0 if int(str(result4[0][2])) == 0 else int(str(result4[0][2]))/int(str(result4[0][0]))
                    dt_percent = 0 if int(str(result4[0][2])) == 0 else int(str(result4[0][3]))/int(str(result4[0][0]))
                    cap_percent = 0 if int(str(result4[0][2])) == 0 else int(str(result4[0][4]))/int(str(result4[0][0]))
                    vcap_percent = 0 if int(str(result4[0][2])) == 0 else int(str(result4[0][5]))/int(str(result4[0][0]))
                    expected_pts = ppg*dt_percent + ppg*cap_percent + ppg*vcap_percent*0.5
                    cap_chance = cap_percent + vcap_percent
                    report_4.loc[i] = [player_id[i],result[0][2],innings_order[i],int(str(result4[0][0])),rank_avg,int(str(result4[0][2])),int(str(result4[0][3])),int(str(result4[0][4])),int(str(result4[0][5])),ppg,dt_percent,cap_percent,vcap_percent,expected_pts,cap_chance]
                
            #QUERY FOR REPORT 5
            if(international[i]==1 and match_format[i] in supersetCategory):
                if(innings_order[i] == 3):
                    query5 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s and Ground_ID = %s and Opponent_Team_ID = %s"""
                    value5 = (player_id[i],get_Superset_Category(match_format[i]),ground_id[i],opponent_id[i])
                else:
                    query5 = """select sum(Matches),sum(Player_Rank),sum(Value_Fantasy),sum(In_Dream_Team),sum(Captain),sum(Vice_Captain) from fantasy_point_table 
                    where Player_ID = %s and Match_Type = %s and Innings_Order = %s and Ground_ID = %s and Opponent_Team_ID = %s"""
                    value5 = (player_id[i],get_Superset_Category(match_format[i]),innings_order[i],ground_id[i],opponent_id[i])
                
                my_cursor.execute(query5,value5)
                result5 = my_cursor.fetchall()
                if(result5[0][0] == None):
                    report_5.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
                else:
                    rank_avg = int(str(result5[0][1]))/int(str(result5[0][0]))
                    ppg = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][2]))/int(str(result5[0][0]))
                    dt_percent = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][3]))/int(str(result5[0][0]))
                    cap_percent = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][4]))/int(str(result5[0][0]))
                    vcap_percent = 0 if int(str(result5[0][2])) == 0 else int(str(result5[0][5]))/int(str(result5[0][0]))
                    expected_pts = ppg*dt_percent + ppg*cap_percent + ppg*vcap_percent*0.5
                    cap_chance = cap_percent + vcap_percent
                    report_5.loc[i] = [player_id[i],result[0][2],innings_order[i],int(str(result5[0][0])),rank_avg,int(str(result5[0][2])),int(str(result5[0][3])),int(str(result5[0][4])),int(str(result5[0][5])),ppg,dt_percent,cap_percent,vcap_percent,expected_pts,cap_chance]

            else:
                report_5.loc[i] = [player_id[i],result[0][2],innings_order[i],'','','','','','','','','','','','']
            

    pd.set_option('display.max_colwidth', 500)

    #WRITING IN OUTPUT FILE
    excel_writer = pd.ExcelWriter('./Docs/Report Output.xlsx', engine='xlsxwriter')
    report_1.to_excel(excel_writer, index=False, sheet_name='NORMAL')
    report_2.to_excel(excel_writer, index=False, sheet_name='GROUND')
    report_3.to_excel(excel_writer, index=False, sheet_name='H2H')
    report_4.to_excel(excel_writer, index=False, sheet_name='FORM')
    report_5.to_excel(excel_writer, index=False, sheet_name='INTERNATIONAL')
    excel_writer.close()

    #CLOSING DATABASE CONNECTION
    mydb.close()