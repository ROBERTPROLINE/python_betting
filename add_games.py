__author__ = 'robertsibanda20@gmail.com'

import pymysql
import os
import random

dbconn = pymysql.connect('localhost','root','','betting_customers')
dbcur  = dbconn.cursor()

def main():

    hometeam  = input('Home Team  : ')
    homemoney = input('Home money : ')
    awayteam  = input('Away Team  : ')
    awaymoney = input('Away money : ')
    drawmoney = input('Draw money : ')
    game_code = input('Game Code  :')

    dbcur.execute("insert into games values('{0}','{1}','{2}','{3}','{4}','{5}')".format(game_code,homemoney,awaymoney,drawmoney,hometeam,awayteam))
    dbconn.commit()

    dbcur.execute("insert into game_results values('{0}','X','X')".format(game_code))
    dbconn.commit()

    print('Game Added**************')

try:
    while 1:
        main()
except Exception as ex:
    print('Error : ',ex)
