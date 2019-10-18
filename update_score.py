__author__ = 'robertsibanda20@gmail.com'

import pymysql

dbconn = pymysql.connect('localhost','root','','betting_customers')
dbcur  = dbconn.cursor()

def main():
    game_code = input('Game Code : ')

    dbcur.execute("select * from game_results where game_code = '{0}'".format(game_code))
    rezlts = dbcur.fetchone()

    if rezlts != None:
        dbcur.execute("select * from games where game_code = '{0}'".format(game_code))
        print(dbcur.fetchone()[-2:-1])

        final = input('Result(home/away/draw) :')
        dbcur.execute("update game_results set overal='{0}'".format(final))
        score = input('Final Score(home:away) :')
        dbcur.execute("update game_results set score_sheet='{0}'".format(score))
        dbconn.commit()

try:
    while 1:
        main()
except Exception as e:
    print('Error : ',ex)
