def Fantasy_Point_Table_Call():
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
    sys.stdout = open(project_directory + '/Output/Fantasy_Point_Table.txt', 'wt')

    #CONNECTING TO DATABASE
    mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database='cricinfo',
    )
    mycursor = mydb.cursor()

    #CALCULATE FANTASY POINTS FOR ODI
    def odi_match(match_url):
        data=requests.get(match_url)
        response=Selector(data)
        data_dict=response.xpath('//*[@id="__NEXT_DATA__" ]/text()').extract_first()
        data_json = json.loads(data_dict)
        players_details=data_json['props']['appPageProps']['data']['content']['matchPlayers']['teamPlayers']
        match_data=data_json['props']['appPageProps']['data']['content']['innings']
        innings_details=data_json['props']['appPageProps']['data']['content']['innings']
        team1=players_details[0]['team']['objectId']
        team2=players_details[1]['team']['objectId']
        fantasy_dict={}
        matches={}
        name_dict={}
        bat_innings={}
        bowl_innings={}
        player_dict={}
        bowling_dict={}
        batting_dict={}
        feilding_dict={}
        team_dict={}
        opponent_dict={}
        innings_dict={}
        catch_player={}
        
        for pla in players_details:
            players=pla['players']
            for play in players:
                player_id=play['player']['objectId']
                name=play['player']['longName']
                player_dict[player_id]=name
            
                if(len(play['player']['longName']) != 0):
                    name_dict[player_id]=play['player']['longName']
                elif(len(play['player']['name']) != 0):
                    name_dict[player_id]=play['player']['name']
                elif(len(play['player']['indexName']) != 0):
                    name_dict[player_id]=play['player']['indexName']
                elif(len(play['player']['battingName']) != 0):
                    name_dict[player_id]=play['player']['battingName']
                elif(len(play['player']['fieldingName']) != 0):
                    name_dict[player_id]=play['player']['fieldingName']
                else:
                    name_dict[player_id]=""

                if pla['team']['objectId'] == team1:
                    team_dict[player_id]=team1
                    opponent_dict[player_id]=team2
                else:
                    team_dict[player_id]=team2
                    opponent_dict[player_id]=team1
                if pla['team']['objectId'] == innings_details[0]['team']['objectId']:
                    innings_dict[player_id]=1
                else:
                    innings_dict[player_id]=2
                fantasy_dict[player_id]=4
                matches[player_id]=1
                bowling_dict[player_id]=0
                batting_dict[player_id]=0
                feilding_dict[player_id]=0
                bowl_innings[player_id]=0
                bat_innings[player_id]=0
                catch_player[player_id]=0
        
        #GET PLAYER ID
        def get_key(dismissal_bowler,player_dict):
            find_id=''
            for key, value in player_dict.items():
                if dismissal_bowler.lower() in value.lower()  :
                        find_id=key
                        return find_id
            
            if len(find_id) == 0:
                dismissal_bowler1=dismissal_bowler.split(' ')
                
                for db in dismissal_bowler1:
                    for key, value in player_dict.items():
                    
                            if db.lower() in value.lower() :
                                find_id=key
                                return find_id
        
        #GET ODI FIELDING FANTASY POINTS
        def odi_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out):
            feilding_points=(catch*8)+(st*12)+(run_out*12)+(sh_run_out*6)
            return feilding_points
        
        #GET ODI BATTING FANTASY POINTS
        def odi_batsman_fantasypoint(Player_id,runs,boundary,six,playingRole,strikerate,balls):
            if boundary == None:
                boundary=0

            if six == None:
                six=0

            hundered=0
            fifty=0
            duck=0
            str_rate=0
            if playingRole !='bowler' and  balls > 20:
                if strikerate > 140:
                    str_rate=6
                elif 120.01 <= strikerate <= 140:
                    str_rate=4
                elif 100 <= strikerate <= 120:
                    str_rate=2
                elif 40 <= strikerate <= 50:
                    str_rate=-2
                elif 30 <= strikerate <= 39.99:
                    str_rate=-4
                elif  strikerate < 30:
                    str_rate=-6

            try:
                if runs >= 100 :
                    hundered=1
                elif runs >=50:
                    fifty=1
            except:
                pass

            if run == 0:
                if playingRole =='bowler':
                    duck=0 
                else:
                    duck=1

            point=(run*1)+(boundary*1)+(six*2)+(fifty*4)+(hundered*8)+(duck*(-3))+(str_rate*1)
            return point
        
        #GET ODI BOWLING FANTASY POINTS
        def odi_bowler_fantasypoint(bowler_id,LBW_Bowled,Wicket,maidens,economy,balls):
            four_w=0
            five_w=0
            ec=0

            if Wicket >=5:
                five_w=1
            elif Wicket >=4:
                four_w=1

            if balls >= 30:
                if economy < 2.5:
                    ec=6
                elif 2.5 <=economy <=3.49:
                    ec=4
                elif 3.5 <=economy <=4.5:
                    ec=2
                elif 7<=economy <=8:
                    ec=-2
                elif 8.01 <=economy <=9:
                    ec=-4
                elif economy >9:
                    ec=-6

            bowling_points=(Wicket*25)+(LBW_Bowled*8)+(four_w*4)+(five_w*8)+(maidens*4)+(ec*1)
            return bowling_points

        for runs_data in match_data:
            batsmans=runs_data['inningBatsmen']
            bowlers=runs_data['inningBowlers']
            
            #UPDATE BATTING POINTS & FIELDING POINTS
            for bastsman in batsmans:
                batted_type=bastsman['battedType']
                if batted_type == 'DNB' or batted_type == 'sub' or batted_type =='absent':
                    pass
                else:
                    Player_id=bastsman['player']['objectId']
                    playingRole=bastsman['player']['playingRoles']
                    run=bastsman['runs']
                    boundary=bastsman['fours']
                    six=bastsman['sixes']
                    bat_innings[Player_id]=bat_innings[Player_id]+1
                    strikerate=bastsman['strikerate']
                    balls=bastsman['balls']
                    batting_point=odi_batsman_fantasypoint(Player_id,run,boundary,six,playingRole,strikerate,balls)
                    batting_dict[Player_id]=  batting_dict[Player_id]+batting_point
                    Di_type=bastsman['dismissalType']
                    fielders=bastsman['dismissalFielders']
                    
                    if bastsman['isOut'] == True and Di_type == 1 :
                        try:
                            fielders=fielders[0]
                            fielder_id=fielders['player']['objectId']
                            try:
                                catch_player[fielder_id]=catch_player[fielder_id]+1
                            except:
                                matches[fielder_id]=0
                                bowl_innings[fielder_id]=0
                                bat_innings[fielder_id]=0
                                catch_player[fielder_id]=1
                            catch=1
                            st=0
                            run_out=0
                            sh_run_out=0
                            feilding_points=odi_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out)
                            try:
                                feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                            except:
                                matches[fielder_id]=0
                                bowl_innings[fielder_id]=0
                                bat_innings[fielder_id]=0
                                feilding_dict[fielder_id]=feilding_points
                        except:
                            pass
                    elif bastsman['isOut'] == True and Di_type == 4:
                        try:
                            if len(fielders)>1:
                                sh_run_out=1
                                run_out=0
                                catch=0
                                st=0
                                for fielder in fielders:
                                    fielder_id=fielder['player']['objectId']
                                    feilding_points=odi_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out)
                                    try:
                                        feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                                    except:
                                        matches[fielder_id]=0
                                        bowl_innings[fielder_id]=0
                                        bat_innings[fielder_id]=0
                                        feilding_dict[fielder_id]=feilding_points
                            elif len(fielders) == 1:
                                sh_run_out=0
                                run_out=1
                                catch=0
                                st=0
                                fielder=fielders[0]
                                fielder_id=fielder['player']['objectId']
                                feilding_points=odi_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out)
                                try:
                                    feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                                except:
                                    matches[fielder_id]=0
                                    bowl_innings[fielder_id]=0
                                    bat_innings[fielder_id]=0
                                    feilding_dict[fielder_id]=feilding_points
                        except:
                            pass
                    elif bastsman['isOut'] == True and Di_type == 5:
                        sh_run_out=0
                        run_out=0
                        catch=0
                        st=1
                        if(fielders is not None):
                            fielder=fielders[0]
                            try:
                                fielder_id=fielder['player']['objectId']
                                feilding_points=odi_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out)
                                feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                            except:
                                matches[fielder_id]=0
                                bowl_innings[fielder_id]=0
                                bat_innings[fielder_id]=0
                                feilding_dict[fielder_id]=feilding_points
                                pass
            
            #UPDATE BOWLING POINTS
            for bowler in bowlers:
                bowler_id=bowler['player']['objectId']
                bowler_name=bowler['player']['name']
                bowl_innings[bowler_id]=bowl_innings[bowler_id]+1
                LBW_Bowled=0
                Wicket=bowler['wickets']
                disssimal_batsmans=bowler['inningWickets']
                maidens=bowler['maidens']
                economy=bowler['economy']
                balls=bowler['balls']
                bowling_points=odi_bowler_fantasypoint(bowler_id,LBW_Bowled,Wicket,maidens,economy,balls)
                bowling_dict[bowler_id]=bowling_dict[bowler_id]+bowling_points
        
        #UPDATE FIELDING POINTS
        for key,value in catch_player.items():
            if value >= 3:
                feilding_dict[key]=feilding_dict[key]+4

        b1=list(bowling_dict.keys())
        f1=list(feilding_dict.keys())
        bo1=list(batting_dict.keys())
        list_of_players=set(b1+f1+bo1)
        
        #UPDATE TOTAL FANTASY POINTS
        for player in list_of_players :    
            try:
                fantasy_dict[player]=bowling_dict[player]+batting_dict[player]+feilding_dict[player]+fantasy_dict[player]
            except:
                try:
                    bowling_pts=bowling_dict[player]
                except:
                    bowling_pts=0
                try:
                    batting_pts=bowling_dict[player]
                except:
                    batting_pts=0
                try:
                    feilding_pts=bowling_dict[player]
                except:
                    feilding_pts=0
                fantasy_dict[player]=bowling_pts+batting_pts+feilding_pts
        
        #DREAM TEAM, CAPTAIN, VICE CAPTAIN SELECTION 
        dream_point=dict(sorted(fantasy_dict.items(), key = lambda x: x[1], reverse = True))
        caps=list(dream_point.keys())[:2]
        dream_team=list(dream_point.keys())[:11]
        captain=caps[0]
        vice_captain=caps[1]
        dream_team_display={}
        
        for player_id in dream_point:
            captain_points=0
            vice_captain_points=0
            in_dream_team=0
            if player_id == captain:
                captain_points=1
            if player_id == vice_captain:
                vice_captain_points=1
            if player_id in dream_team:
                in_dream_team=1
            dream_team_display[player_id]={'points':dream_point[player_id],'captain':captain_points,'vice_captain':vice_captain_points,'In_dream_team':in_dream_team,'Matches':matches[player_id],'Bat_innings':bat_innings[player_id],'Bowl_innings':bowl_innings[player_id]}
        
        return  [dream_team_display,batting_dict,bowling_dict,feilding_dict,team_dict,opponent_dict,innings_dict,name_dict]

    #CALCULATE FANTASY POINTS FOR T20
    def t20(match_url):   
        data=requests.get(match_url)
        response=Selector(data)
        data_dict=response.xpath('//*[@id="__NEXT_DATA__" ]/text()').extract_first()
        data_json = json.loads(data_dict)
        players_details=data_json['props']['appPageProps']['data']['content']['matchPlayers']['teamPlayers']
        match_data=data_json['props']['appPageProps']['data']['content']['innings']
        innings_details=data_json['props']['appPageProps']['data']['content']['innings']
        team1=players_details[0]['team']['objectId']
        team2=players_details[1]['team']['objectId']
        fantasy_dict={}
        matches={}
        bat_innings={}
        bowl_innings={}
        player_dict={}
        bowling_dict={}
        batting_dict={}
        feilding_dict={}
        name_dict={}
        team_dict={}
        opponent_dict={}
        innings_dict={}
        catch_player={}

        for pla in players_details:
            players=pla['players']
            for play in players:
                player_id=play['player']['objectId']
                name=play['player']['longName']
                player_dict[player_id]=name

                if(len(play['player']['longName']) != 0):
                    name_dict[player_id]=play['player']['longName']
                elif(len(play['player']['name']) != 0):
                    name_dict[player_id]=play['player']['name']
                elif(len(play['player']['indexName']) != 0):
                    name_dict[player_id]=play['player']['indexName']
                elif(len(play['player']['battingName']) != 0):
                    name_dict[player_id]=play['player']['battingName']
                elif(len(play['player']['fieldingName']) != 0):
                    name_dict[player_id]=play['player']['fieldingName']
                else:
                    name_dict[player_id]=""

                if pla['team']['objectId'] == team1:
                    team_dict[player_id]=team1
                    opponent_dict[player_id]=team2
                else:
                    team_dict[player_id]=team2
                    opponent_dict[player_id]=team1
                if pla['team']['objectId'] == innings_details[0]['team']['objectId']:
                    innings_dict[player_id]=1
                else:
                    innings_dict[player_id]=2
                fantasy_dict[player_id]=4
                matches[player_id]=1
                bowling_dict[player_id]=0
                batting_dict[player_id]=0
                feilding_dict[player_id]=0
                bowl_innings[player_id]=0
                bat_innings[player_id]=0
                catch_player[player_id]=0

        #GET PLAYER ID
        def get_key(dismissal_bowler,player_dict):
            for key, value in player_dict.items():
                    if dismissal_bowler.lower() in value.lower():
                        return key

        #GET T20 FIELDING FANTASY POINTS
        def t20i_batsman_fantasypoint(Player_id,runs,boundary,six,playingRole,strikerate,balls):
            if boundary == None:
                boundary=0

            if six == None:
                six=0

            hundered=0
            fifty=0
            thirty=0
            duck=0
            str_rate=0
            try:
                if playingRole !='bowler' and  balls >= 10:
                    if strikerate > 170:
                        str_rate=6
                    elif 150.01 <= strikerate <= 170:
                        str_rate=4
                    elif 130 <= strikerate <= 150:
                        str_rate=2
                    elif 60 <= strikerate <= 70:
                        str_rate=-2
                    elif 50 <= strikerate <= 59.99:
                        str_rate=-4
                    elif  strikerate < 50:
                        str_rate=-6
            except:
                pass
            try:
                if runs >= 100 :
                    hundered=1
                elif runs >=50:
                    fifty=1
                elif runs >=30:
                    thirty=1
            except:
                pass

            if run == 0:
                if playingRole =='bowler':
                    duck=0 
                else:
                    duck=1

            point=(run*1)+(boundary*1)+(six*2)+(thirty*4)+(fifty*8)+(hundered*16)+(duck*(-2))+(str_rate*1)        
            return point

        #GET T20 BOWLING FANTASY POINTS
        def t20i_bowler_fantasypoint(bowler_id,LBW_Bowled,Wicket,maidens,economy,balls):
            three_w=0
            four_w=0
            five_w=0
            ec=0
            if Wicket >=5:
                five_w=1
            elif Wicket >=4:
                four_w=1
            elif Wicket >=3:
                three_w=1

            if balls >= 12:
                if economy < 5:
                    ec=6
                elif 5 <=economy <=5.99:
                    ec=4
                elif 6 <=economy <=7:
                    ec=2
                elif 10 <=economy <=11:
                    ec=-2
                elif 11.01 <=economy <=12:
                    ec=-4
                elif economy >12:
                    ec=-6

            bowling_points=(Wicket*25)+(LBW_Bowled*8)+(three_w*4)+(four_w*8)+(five_w*16)+(maidens*12)+(ec*1)        
            return bowling_points

        #GET T20 FIELDING FANTASY POINTS
        def t20i_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out):
            feilding_points=(catch*8)+(st*12)+(run_out*12)+(sh_run_out*6)
            return feilding_points


        for runs_data in match_data:
            batsmans=runs_data['inningBatsmen']
            bowlers=runs_data['inningBowlers']

            #UPDATE BATTING POINTS & FIELDING POINTS
            for bastsman in batsmans:
                batted_type=bastsman['battedType']
                if batted_type == 'DNB' or batted_type == 'sub' or  batted_type =='absent':
                    pass
                else:
                    Player_id=bastsman['player']['objectId']
                    playingRole=bastsman['player']['playingRoles']
                    run=bastsman['runs']
                    boundary=bastsman['fours']
                    six=bastsman['sixes']
                    bat_innings[Player_id]=bat_innings[Player_id]+1
                    strikerate=bastsman['strikerate']
                    balls=bastsman['balls']
                    batting_point=t20i_batsman_fantasypoint(Player_id,run,boundary,six,playingRole,strikerate,balls)
                    batting_dict[Player_id]= batting_dict[Player_id]+batting_point
                    Di_type=bastsman['dismissalType']
                    fielders=bastsman['dismissalFielders']

                    if bastsman['isOut'] == True and Di_type == 1 :
                        try:
                            fielders=fielders[0]
                            fielder_id=fielders['player']['objectId']
                            fielder_name=fielders['player']['name']
                            try:
                                catch_player[fielder_id]=catch_player[fielder_id]+1
                            except:
                                matches[fielder_id]=0
                                bowl_innings[fielder_id]=0
                                bat_innings[fielder_id]=0
                                catch_player[fielder_id]=1

                            catch=1
                            st=0
                            run_out=0
                            sh_run_out=0
                            feilding_points=t20i_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out)
                            try:
                                feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                            except:
                                matches[fielder_id]=0
                                bowl_innings[fielder_id]=0
                                bat_innings[fielder_id]=0
                                feilding_dict[fielder_id]=feilding_points
                        except:
                            pass

                    elif bastsman['isOut'] == True and Di_type == 5:
                        sh_run_out=0
                        run_out=0
                        catch=0
                        st=1
                        if(fielders is not None):
                            fielder=fielders[0]
                            fielder_id=fielder['player']['objectId']
                            feilding_points=t20i_fielder_fantasypoint (fielder_id,catch,st,run_out,sh_run_out)
                            try:
                                feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                            except:
                                matches[fielder_id]=0
                                bowl_innings[fielder_id]=0
                                bat_innings[fielder_id]=0
                                feilding_dict[fielder_id]=feilding_points

                    elif bastsman['isOut'] == True and Di_type == 4:
                        try:
                            if len(fielders)>1:
                                sh_run_out=1
                                run_out=0
                                catch=0
                                st=0

                                for fielder in fielders:
                                    fielder_id=fielder['player']['objectId']
                                    feilding_points=t20i_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out)
                                    try:
                                        feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                                    except:
                                        matches[fielder_id]=0
                                        bowl_innings[fielder_id]=0
                                        bat_innings[fielder_id]=0
                                        feilding_dict[fielder_id]=feilding_points
                            elif len(fielders) == 1:
                                sh_run_out=0
                                run_out=1
                                catch=0
                                st=0
                                fielder=fielders[0]
                                fielder_id=fielder['player']['objectId']
                                feilding_points=t20i_fielder_fantasypoint(fielder_id,catch,st,run_out,sh_run_out)
                                try:
                                    feilding_dict[fielder_id]=feilding_dict[fielder_id]+feilding_points
                                except:
                                    matches[fielder_id]=0
                                    bowl_innings[fielder_id]=0
                                    bat_innings[fielder_id]=0
                                    feilding_dict[fielder_id]=feilding_points
                        except:
                            pass

            #UPDATE BOWLING POINTS                      
            for bowler in bowlers:
                bowler_id=bowler['player']['objectId']
                bowler_name=bowler['player']['name']
                bowl_innings[bowler_id]=bowl_innings[bowler_id]+1
                LBW_Bowled=0
                Wicket=bowler['wickets']
                disssimal_batsmans=bowler['inningWickets']
                for disssimal_batsman in disssimal_batsmans:
                    dismiss_type=disssimal_batsman['dismissalType']
                    if dismiss_type == 2 or dismiss_type ==3:
                        LBW_Bowled=LBW_Bowled+1
                maidens=bowler['maidens']
                economy=bowler['economy']
                balls=bowler['balls']
                bowling_points=t20i_bowler_fantasypoint(bowler_id,LBW_Bowled,Wicket,maidens,economy,balls)
                bowling_dict[bowler_id]=bowling_dict[bowler_id]+bowling_points

        #UPDATE FIELDING POINTS
        for key,value in catch_player.items():
            if value >= 3:
                feilding_dict[key]= feilding_dict[key]+4
        
        b1=list(bowling_dict.keys())
        f1=list(feilding_dict.keys())
        bo1=list(batting_dict.keys())
        list_of_players=set(b1+f1+bo1)

        #UPDATE TOTAL FANTASY POINTS
        for player in list_of_players :
            try:
                fantasy_dict[player]=bowling_dict[player]+batting_dict[player]+feilding_dict[player]+fantasy_dict[player]
            except:
                try:
                    bowling_pts=bowling_dict[player]
                except:
                    bowling_pts=0
                try:
                    batting_pts=bowling_dict[player]
                except:
                    batting_pts=0
                try:
                    feilding_pts=bowling_dict[player]
                except:
                    feilding_pts=0
                fantasy_dict[player]=bowling_pts+batting_pts+feilding_pts

        #DREAM TEAM, CAPTAIN, VICE CAPTAIN SELECTION
        dream_point=dict(sorted(fantasy_dict.items(), key = lambda x: x[1], reverse = True))
        caps=list(dream_point.keys())[:2]
        dream_team=list(dream_point.keys())[:11]
        captain=caps[0]
        vice_captain=caps[1]
        dream_team_display={}

        for player_id in dream_point:
            captain_points=0
            vice_captain_points=0
            in_dream_team=0
            if player_id == captain:
                captain_points=1
            if player_id == vice_captain:
                vice_captain_points=1
            if player_id in dream_team:
                in_dream_team=1

            dream_team_display[player_id]={'points':dream_point[player_id],'captain':captain_points,'vice_captain':vice_captain_points,'In_dream_team':in_dream_team,'Matches':matches[player_id],'Bat_innings':bat_innings[player_id],'Bowl_innings':bowl_innings[player_id]}

        return  [dream_team_display,batting_dict,bowling_dict,feilding_dict,team_dict,opponent_dict,innings_dict,name_dict]

    #INSERT FANTASY POINTS IN DATABASE
    def updation_fantasy_point(data,match_type):

        [data_all,data_bat,data_bowl,data_field,data_team,data_opponent,data_innings,data_name]=data
        
        
        try:
            #QUERY FOR INSERTING FANTASY POINTS
            insert_data="""Insert into  fantasy_point_table (Match_Player_ID,Player_ID,Player_Name,Match_ID,Team_ID,Opponent_Team_ID,Ground_ID,Match_Date,Innings_Order,Match_Type,Matches,Total_Fantasy,Batting_Fantasy,Bowling_Fantasy,Fielding_Fantasy,In_Dream_Team,Captain,Vice_Captain,Bat_Innings,Bowl_Innings,Status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            #QUERY FOR UPDATING STATUS OF THE PLAYER IN ALL MATCH OF SAME FORMAT TO 'NOT UPDATED' TO IDENTIFY DURING PLAYER TABLE UPDATE
            update_status="""UPDATE fantasy_point_table SET Status = 'NOT UPDATED' where player_id =%s and match_type =%s"""

            #INSERT AND UPDATE FOR CATEGORY AND SUBCATEGORY IN DATABASE
            for d in data_all:
                if(d not in data_team):
                    continue
                try:
                    #INSERT DATA IN DATABASE
                    match_playerid=str(match_id)+'_'+str(d)
                    value=(match_playerid,d,data_name[d],match_id,data_team[d],data_opponent[d],ground_id,match_date,data_innings[d],match_type,data_all[d]['Matches'],data_all[d]['points'],data_bat[d],data_bowl[d],data_field[d],data_all[d]['In_dream_team'],data_all[d]['captain'],data_all[d]['vice_captain'],data_all[d]['Bat_innings'],data_all[d]['Bowl_innings'],'NOT UPDATED')
                    mycursor.execute(insert_data,value)
                    
                    #UPDATE STATUS OF THE PLAYER IN ALL MATCH OF SAME CATEGORY TO 'NOT UPDATED' TO IDENTIFY DURING PLAYER TABLE UPDATE
                    update_value=(d,match_type)
                    mycursor.execute(update_status,update_value)
                    mydb.commit()
                    
                    #UPDATE STATUS OF THE PLAYER IN ALL MATCH OF SUB CATEGORY IF THEY EXSIST TO 'NOT UPDATED' TO IDENTIFY DURING PLAYER TABLE UPDATE
                    if match_type == 2:
                        s_value=(d,5)
                    elif match_type == 3:
                        s_value=(d,6)
                    elif match_type == 9:
                        s_value=(d,12)
                    elif match_type == 10:
                        s_value=(d,17)
                    if match_type==2 or match_type==3 or match_type==9 or match_type==10 :
                        mycursor.execute(update_status,s_value)
                        mydb.commit()

                except mysql.connector.IntegrityError as err:
                    pass
                    print("Error: {}".format(err))         
            return 'Success'
        except Exception as e:
            print(e)
            return 'Failed'

    #QUERY FOR FETCHING UNUPDATED MATCHES FROM MATCH ID TABLE
    search="""select * from match_table where Match_Updation='NOT UPDATED'"""

    #QUERY FOR UPDATING STATUS OF THE MATCH IN MATCH ID TABLE
    update_status_in_match_id="""update match_table set Match_Updation=%s where Match_ID =%s"""

    #FETCHING UNUPDATED MATCHES FROM MATCH ID TABLE AND INSERTING IN FANTASY POINT TABLE
    mycursor.execute(search)
    for row in mycursor.fetchall():
        match_id = row[0]
        match_type = row[1]
        match_date = row[2]
        ground_id = row[3]
        match_url = row[5]
        updation_status = 'Failed'
        try:
            if match_type == 2 or match_type == 5: # Mens ODI or Mens List A
                datas1=odi_match(match_url)
                updation_status=updation_fantasy_point(datas1,match_type)
            elif match_type == 3 or match_type ==6: # Mens T20I or Mens T20
                datas1=t20(match_url)
                updation_status=updation_fantasy_point(datas1,match_type)
            elif match_type == 9 or match_type == 12: # Womens ODI or Womens List A
                datas1=odi_match(match_url)
                updation_status=updation_fantasy_point(datas1,match_type) 
            elif match_type == 10 or match_type ==17: # Womens T20I or Womens T20
                datas1=t20(match_url)
                updation_status=updation_fantasy_point(datas1,match_type)
        except Exception as e:
            print("Error: ",e)
            updation_status='Failed' 

        #UPDATE MATCH ID TABLE WITH UPDATION STATUS
        if updation_status == 'Success':
            mycursor.execute(update_status_in_match_id,('COMPLETED',match_id))
            mydb.commit()
            print('Sucessfully Updated : '+str(match_id))
            
        elif updation_status == 'Failed':
            print('Failed to Update : '+str(match_id))
        
    #FINAL COMMIT TO DATABASE       
    mydb.commit()

    #CLOSING DATABASE CONNECTION
    mydb.close()

    #CLOSING OUTPUT FILE
    sys.stdout.close()
    sys.stdout = sys.__stdout__