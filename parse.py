#!/usr/bin/env python

import os, sys, traceback, re
from BeautifulSoup import BeautifulSoup

filename = ""
 
def parse_page(contents):
    try:
        soup = BeautifulSoup(contents)
	    #get div with id=game_title
        game_title_div = soup.find("div", { "id" : "game_title" }).find("h1")
        game_show = game_title_div.contents[0].split("-")[0]
        game_date = game_title_div.contents[0].split("-")[1]
        #print game_show, game_date
	    #get Show# and Date

        #get div with id=jeopardy_round, table with class=round
        jeopardy_round_table = soup.find("div", { "id" : "jeopardy_round" }).find("table", { "class" : "round" })
        parse_round(jeopardy_round_table, "Jeopardy Round", game_show, game_date)

        #get div with id=double_jeopardy_round, table with class=round
        double_jeopardy_round_table = soup.find("div", { "id" : "double_jeopardy_round" }).find("table", { "class" : "round" })
        parse_round(double_jeopardy_round_table, "Double Jeopardy Round", game_show, game_date)

    except:
         #print "exception in: "+filename
         traceback.print_exc()

def parse_round(round_table, round_name, game_show, game_date):
    jeopardy_round_table_category_row = round_table.find("tr")
    jeopardy_round_table_clue_rows = jeopardy_round_table_category_row.findNextSiblings()

        
    categories = []
    for category_cell in jeopardy_round_table_category_row.findAll("td", { "class" : "category_name" }):
        categories.append(category_cell.contents[0])

    clue_rows = []
    for clue_row in jeopardy_round_table_clue_rows:
        clue_single_row = []
        for clue_cell in clue_row.findAll("td", { "class" : "clue" }):
            try:
                clueTokens = clue_cell.find("td", { "class" : "clue_text" }).contents
                clue = ""
                if(clueTokens[0].string != "("):
                    clue = clueTokens[0].string
                else:
                    add = False
                    for clueToken in clueTokens:
                        strToken = clueToken.string
                        if(add):
                            clue += strToken
                        if(strToken.startswith(")")):
                            clue += strToken[3:]
                            add = True

                reward = clue_cell.find("td", { "class" : "clue_value" }).contents[0]
                answerTokens = BeautifulSoup(clue_cell.find("div")['onmouseover']).find("em").contents
                answer = ""
                for answerToken in answerTokens:
                    answer += answerToken.string

                answerTables = BeautifulSoup(clue_cell.find("div")['onmouseover']).findAll("table")
                strPlayers = ""
                tripleStumper = False
                for answerTable in answerTables:
                    wrongAnswers = answerTable.findAll("td", { "class" : "wrong"})
                    if(wrongAnswers):
                        for wrongAnswer in wrongAnswers:
                            token = wrongAnswer.contents[0]
                            if(token == "Triple Stumper"):
                                tripleStumper = True
                            else:
                                strPlayers+=token + "(wrong), "

                    rightAnswers = answerTable.findAll("td", { "class" : "right"})
                    if(rightAnswers):
                        for rightAnswer in rightAnswers:
                            token = rightAnswer.contents[0]
                            strPlayers+=token + "(right), "

                strPlayers = strPlayers[:-2]

                if(strPlayers == ""):
                    strPlayers = "none"

                if(tripleStumper):
                    strPlayers += "\t"+"true"
                else:
                     strPlayers += "\t"+"false"

                single_clue = clue+"\t"+reward+"\t"+str(answer)+"\t"+strPlayers
                clue_single_row.append(single_clue)
            except:
                #print "exception in: "+filename
                clue_single_row.append(None)
        clue_rows.append(clue_single_row)


    clues = []
    for clue_row in clue_rows:
        i = 0
        for clue_entry in clue_row:
            if clue_entry is not None:
                clues.append(game_show+"\t"+game_date+"\t"+round_name+"\t"+categories[i]+"\t"+clue_entry)
            i = i+1

    print "\n".join(clues)
    return clues
            
        



def parse_game_title(game_title):
    print game_title


path="pages/" 
dirList=os.listdir(path)
for fname in dirList:
    f = open(path+fname, 'r')
    filename = f.name
    #f = open("pages/showgame.php?game_id=3274", 'r')
    fcontents = f.read()
    parse_page(fcontents)
    #break



