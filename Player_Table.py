def Player_Table_Call():
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
    sys.stdout = open(project_directory + '/Output/Player_Table.txt', 'wt')

    #CONNECTING TO DATABASE
    mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database='cricinfo',
    )
    mycursor = mydb.cursor()

    #QUERY FOR FETCHING DATA FROM DATABASE
    fetch_Player= """SELECT Player_ID,Match_Type,Match_Player_ID FROM fantasy_point_table where Status='NOT UPDATED'"""

    #QUERY FOR INSERTING DATA INTO DATABASE
    Insert_player="""Insert into player_table (Match_Type_Player_ID,Player_ID,Match_Type,Matches,Total_Fantasy,Batting_Fantasy,Bowling_Fantasy,Fielding_Fantasy,In_Dream_Team,Captain,Vice_Captain,Bat_Innings,Bowl_Innings) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    #QUERY FOR UPDATING DATA INTO DATABASE
    Update_data="""UPDATE player_table SET Matches = %s,Total_Fantasy = %s, Batting_Fantasy = %s,Bowling_Fantasy = %s,Fielding_Fantasy = %s, In_Dream_Team = %s, Captain = %s,Vice_Captain = %s,Bat_innings = %s,Bowl_innings = %s WHERE Match_Type_Player_ID =%s """

    #QUERY FOR SELECTING DATA FROM DATABASE
    select_data="""SELECT * PLAYER_TABLE WHERE MATCH_TYPE_PLAYER_ID = %s"""

    #QUERY FOR SELECTING PLAYER FROM DATABASE
    select_player = """SELECT * FROM fantasy_point_table WHERE Match_Player_ID = %s"""

    #QUERY FOR UPDATING STATUS INTO DATABASE
    update_status="""UPDATE fantasy_point_table SET Status = 'Completed' where Match_Player_ID = %s"""

    #INSERTING DATA INTO DATABASE
    mycursor.execute(fetch_Player)
    for row in mycursor.fetchall():
        player_id=row[0]
        match_type=row[1]
        match_player_id=row[2]
        match_type_player=str(player_id)+'_'+str(match_type)
                    
        select_data_value=(str(player_id)+'_'+str(match_type))
        mycursor.execute(select_data,(select_data_value,))
        record=mycursor.fetchall()
        if len(record)==0:
            #create new row in player_table as we are fetching all values from fantasy_point_table
            mycursor.execute(select_player,(match_player_id,))
            record=mycursor.fetchall()
            row=list(record[-1])
            if match_type==2 or match_type==3 or match_type==9 or match_type==10:
                insert_value=(match_type_player,player_id,match_type,1,int(row[11]),int(row[12]),int(row[13]),int(row[14]),int(row[15]),int(row[16]),int(row[17]),int(row[18]),int(row[19]))
                mycursor.execute(Insert_player,(insert_value,))
                mycursor.execute(update_status,(match_player_id,))
                print("Sucessfully Inserted : ",player_id," ",match_type," ",match_type_player)

                if match_type ==2:
                    match_type1=5
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    insert_value=(match_type_player1,player_id,match_type1,1,int(row[11]),int(row[12]),int(row[13]),int(row[14]),int(row[15]),int(row[16]),int(row[17]),int(row[18]),int(row[19]))
                elif match_type ==3:
                    match_type1=6
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    insert_value=(match_type_player1,player_id,match_type1,1,int(row[11]),int(row[12]),int(row[13]),int(row[14]),int(row[15]),int(row[16]),int(row[17]),int(row[18]),int(row[19]))
                elif match_type ==9:
                    match_type1=12
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    insert_value=(match_type_player1,player_id,match_type1,1,int(row[11]),int(row[12]),int(row[13]),int(row[14]),int(row[15]),int(row[16]),int(row[17]),int(row[18]),int(row[19]))
                elif match_type ==10:
                    match_type1=17
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    insert_value=(match_type_player1,player_id,match_type1,1,int(row[11]),int(row[12]),int(row[13]),int(row[14]),int(row[15]),int(row[16]),int(row[17]),int(row[18]),int(row[19]))

                mycursor.execute(Insert_player,(insert_value,))
                mycursor.execute(update_status,(match_player_id,))
                mydb.commit()
                print("Sucessfully Inserted : ",player_id," ",match_type1," ",match_type_player1)
            else:
                insert_value=(match_type_player,player_id,match_type,1,int(row[11]),int(row[12]),int(row[13]),int(row[14]),int(row[15]),int(row[16]),int(row[17]),int(row[18]),int(row[19]))
                mycursor.execute(Insert_player,(insert_value,))
                mycursor.execute(update_status,(match_player_id,))
                mydb.commit()
                print("Sucessfully Inserted : ",player_id," ",match_type," ",match_type_player)

        else:          
            #update existing row in player_table as we are fetching all values from fantasy_point_table
            mycursor.execute(select_player,(match_player_id,))
            record=mycursor.fetchall()
            row=list(record[-1])
            Update_data="""UPDATE player_table SET Matches = %s,Total_Fantasy = %s, Batting_Fantasy = %s,Bowling_Fantasy = %s,Fielding_Fantasy = %s, In_Dream_Team = %s, Captain = %s,Vice_Captain = %s,Bat_innings = %s,Bowl_innings = %s WHERE Match_Type_Player_ID =%s """

            if match_type==2 or match_type==3 or match_type==9 or match_type==10:
                update_value=(int(record[4])+1,int(record[5])+int(row[11]),int(record[6])+int(row[12]),int(record[7])+int(row[13]),int(record[8])+int(row[14]),int(record[9])+int(row[15]),int(record[10])+int(row[16]),int(record[11])+int(row[17]),int(record[12])+int(row[18]),int(record[13])+int(row[19]),match_type_player)
                mycursor.execute(Update_data,update_value)
                mycursor.execute(update_status,(match_player_id,))
                mydb.commit()
                print("Sucessfully Updated : ",player_id," ",match_type," ",match_type_player)

                if match_type ==2:
                    match_type1=5
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    update_value=(int(record[4])+1,int(record[5])+int(row[11]),int(record[6])+int(row[12]),int(record[7])+int(row[13]),int(record[8])+int(row[14]),int(record[9])+int(row[15]),int(record[10])+int(row[16]),int(record[11])+int(row[17]),int(record[12])+int(row[18]),int(record[13])+int(row[19]),match_type_player1)
                elif match_type ==3:
                    match_type1=6
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    update_value=(int(record[4])+1,int(record[5])+int(row[11]),int(record[6])+int(row[12]),int(record[7])+int(row[13]),int(record[8])+int(row[14]),int(record[9])+int(row[15]),int(record[10])+int(row[16]),int(record[11])+int(row[17]),int(record[12])+int(row[18]),int(record[13])+int(row[19]),match_type_player1)
                elif match_type ==9:
                    match_type1=12
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    update_value=(int(record[4])+1,int(record[5])+int(row[11]),int(record[6])+int(row[12]),int(record[7])+int(row[13]),int(record[8])+int(row[14]),int(record[9])+int(row[15]),int(record[10])+int(row[16]),int(record[11])+int(row[17]),int(record[12])+int(row[18]),int(record[13])+int(row[19]),match_type_player1)
                elif match_type ==10:
                    match_type1=17
                    match_type_player1=str(player_id)+'_'+str(match_type1)
                    update_value=(int(record[4])+1,int(record[5])+int(row[11]),int(record[6])+int(row[12]),int(record[7])+int(row[13]),int(record[8])+int(row[14]),int(record[9])+int(row[15]),int(record[10])+int(row[16]),int(record[11])+int(row[17]),int(record[12])+int(row[18]),int(record[13])+int(row[19]),match_type_player1)

                mycursor.execute(Update_data,update_value)
                mycursor.execute(update_status,(match_player_id,))
                mydb.commit()


    #QUERY FOR UPDATING NAME INTO DATABASE
    update_name="""UPDATE player_table SET player_table.Player_Name = (SELECT Player_Name from fantasy_point_table WHERE player_table.Player_ID = fantasy_point_table.Player_ID LIMIT 1)"""
    mycursor.execute(update_name,())
    mydb.commit()

    #CLOSING DATABASE CONNECTION
    mydb.close()

    #CLOSING OUTPUT FILE
    sys.stdout.close()
    sys.stdout = sys.__stdout__