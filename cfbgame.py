from urllib.request import urlopen, Request
import time, json,html, datetime

'''
borrowed some code from /r/cfb's IRC bot, thank you
https://github.com/diagonalfish/FootballBotX2
'''


#Constants
MODE_ACTIVE = 0
MODE_INACTIVE = 1
GAME_STATUS_PRE = 0
GAME_STATUS_IN = 1
GAME_STATUS_POST = 2

type = "80" # 80 = FBS
# Other leagues go here

def get_game(team):
    now = datetime.now()
    req = Request("http://espn.go.com/college-football/scoreboard/_/group/" +
                  type + "/year/"+now.year+"/seasontype/2/?t=" + str(time.time()))
    req.headers["User-Agent"] = "windows 10 bot"
    # Load data
    scoreData = urlopen(req).read().decode("utf-8")
    scoreData = scoreData[scoreData.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
    scoreData = json.loads(scoreData[:scoreData.find('};')+1])
    #print(scoreData)
    #f = open('espnout.txt','w')
    #f.write(json.dumps(scoreData))
    #f.close()

    games = []
    for event in scoreData['events']:
        game = dict()

        game["date"] = event['date']
        status = event['status']['type']['state']
        if status == "pre":
            game['status'] = GAME_STATUS_PRE
            game['time'] = event['status']['type']['shortDetail']
        elif status == "in":
            game['status'] = GAME_STATUS_IN
            game['time'] = event['status']['type']['shortDetail']
        else:
            game['status'] = GAME_STATUS_POST
            game['time'] = "FINAL"
        team1 = html.unescape(event['competitions'][0]['competitors'][0]['team']['location'])
        tid1 = event['competitions'][0]['competitors'][0]['id']
        score1 = int(event['competitions'][0]['competitors'][0]['score'])
        team1abv = event['competitions'][0]['competitors'][0]['team']['abbreviation']
        team2 = html.unescape(event['competitions'][0]['competitors'][1]['team']['location'])
        tid2 = event['competitions'][0]['competitors'][1]['id']
        score2 = int(event['competitions'][0]['competitors'][1]['score'])
        team2abv = event['competitions'][0]['competitors'][1]['team']['abbreviation']
        
        rank1 = event['competitions'][0]['competitors'][0]['curatedRank']
        rank2 = event['competitions'][0]['competitors'][1]['curatedRank']
        
        # Hawaii workaround
        if team1 == "Hawai'i":
            team1 = "Hawaii"
        if team2 == "Hawai'i":
            team2 = "Hawaii"
            
        homestatus = event['competitions'][0]['competitors'][0]['homeAway']
        
        if homestatus == 'home':
            game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'], game['homerank'], game['awayrank']=\
                team1, tid1, team1abv, score1, team2, tid2, team2abv, score2, rank1, rank2
        else:
            game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'], game['homerank'], game['awayrank'] = \
                team2, tid2, team2abv, score2, team1, tid1, team1abv, score1, rank2, rank1
            
        #print (game)
        games.append(game)
    for game in games:
        if game['hometeam'].lower() == team.lower() or game['homeabv'].lower() == team.lower() or game['awayteam'].lower() == team.lower() or game['awayabv'].lower() == team.lower():
            awayr = "("+str(game['awayrank']['current'])+") " if game['awayrank']['current'] <= 25 else ""
            homer = "("+str(game['homerank']['current'])+") " if game['homerank']['current'] <= 25 else ""
            return "%s**%s %s** @ %s**%s %s** - %s" % (awayr,game['awayabv'], game['awayscore'], homer,game['homeabv'], game['homescore'], game['time'])
    return "game not found"