__author__ = 'robertsibanda20@gmail.com'

import pymysql
import random
import os

class Cs:
    retr_db = pymysql.connect('localhost','root','','betting_customers')
    retr_cur = retr_db.cursor()
    betted_games = {}

    games = {}

    def __init__(self,id,stts):
        self.id = id
        self.stts = stts
        print('ID : ', self.id)

        if stts == '0':
            self.Create_new_Customer()

        elif stts == '1':
            self.retrInfo()


    def retrInfo(self):
        os.system('cls')
        print('\nGetting info on : ', self.id)
        print('\n__________________________________\n')
        execode = "select * from bets where customer_id = '{}'".format(self.id)
        Cs.retr_cur.execute(execode)

        rezls = Cs.retr_cur.fetchone()
        if rezls != None:
            customer_data = rezls
            csid  = customer_data[1]
            csname = str(customer_data[3]).upper() + ' ' + str(customer_data[4]).upper()
            csphone = customer_data[-2]
            collcted = customer_data[-1]
            towin = customer_data[-4]

            print('\nCustomer : {} | ID : {} | Phone : {} '.format(csname,csid,csphone))

            print('\nGames : \n')


            Cs.retr_cur.execute("Select * from customer_bets where customer_id = '{0}'".format(self.id))
            rezlts = Cs.retr_cur.fetchone()
            if rezlts!= None:
                for i in rezlts:
                    if(i==self.id):
                        continue
                    print(i.upper())
                    gamecode = i.split('-')
                    Cs.retr_cur.execute("select * from game_results where game_code = '{0}'".format(gamecode[0]))
                    gr = Cs.retr_cur.fetchone()

                    if gr == None:
                        continue

                    if gr[1] == gamecode[1]:
                        continue
                    if gr[1] == 'X':
                        print('All Games Not Done')
                    if gr[1] != gamecode[1]:
                        print('\nTicket Lost !!!!! with {0}  : {1}'.format(gr[0],gr[1].upper()))
                        return





            #print('Bonus = ', 10)
            print('Total Winnings : ',towin, '\n')

            if collcted == 'collected':
                print('collected **************************************')
                return

            collecting = input('Collecting : ')
            if collecting.upper() == 'Y':
                Cs.retr_cur.execute("update bets set collection_status = 'collected' where customer_id= '{0}'".format(self.id))
                Cs.retr_db.commit()
            else:
                return

    def Create_new_Customer(self):
        all_games = {}
        total_winnings = []
        print('Creating new Customer : ', self.id)

        fname  = input('Name          : ')
        name_ = fname.split(' ')
        name = name_[0]
        surn = name_[-1]
        id_num = input('NAT ID        : ')
        cell   = input('Cell No       : ')
        amt    = input('Amount Placed : ')

        execode = "insert into bets values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(self.id,id_num,amt,name,surn,30,'str(all_games)',cell[0:9],'placed')
        Cs.retr_cur.execute(execode)
        Cs.retr_db.commit()

        Cs.retr_cur.execute("insert into customer_bets values('{}','','','','','','')".format(self.id))
        Cs.retr_db.commit()

        games_betted_ = 0
        while games_betted_<7:
            games_betted_ = games_betted_+1
            game = input('\nGame  : ')
            print('\n')
            if game == '//':
                return
            if game == '':
                break

            else:

                game_data = Cs.retr_cur.execute("select * from games where game_code  = '%s'" % game)
                gamedata = Cs.retr_cur.fetchone()

                if len(gamedata)>1:
                    #print(gamedata)
                    game_info = gamedata
                    print('Game : {} | HOME : {}->{} | AWAY : {}->{} | DRAW : {}'.format(game_info[0],game_info[1],game_info[-2].upper(),game_info[2],game_info[-1].upper(),game_info[3]))

                    bets  = input('\nBetts : ')
                    game_name = 'game_{}'.format(games_betted_)
                    current_bet = '{}-{}'.format(game,bets)
                    Cs.retr_cur.execute("update customer_bets set {0}='{1}' where customer_id='{2}'".format(game_name,current_bet,self.id))
                    Cs.retr_db.commit()

                    Cs.retr_cur.execute("select {0} from games where game_code = '{1}'".format(bets.lower(),game))
                    amt_towin = Cs.retr_cur.fetchone()
                    total_winnings.append(amt_towin[0])

                    total_towin = sum(total_winnings) + int(amt)
                    Cs.retr_cur.execute("update bets set amt_towin='{}'".format(total_towin))
                    Cs.retr_db.commit()

                    all_games[game] = bets


                else:
                    print('Game Not Found')
                    games_betted_ = games_betted_ -1

        print('Total To Be Won', total_towin)

def main():
    os.system('cls')
    print('####################ZimBetting#################')

    while 1:

        customer_id = '';
        stts = ''

        id_ = input('Enter ID : ')
        if id_ == '':
            gen_id = random.random()
            customer_id  = str(gen_id)[-6:-1] + 'z'
            stts = '0'

        else:
            stts = '1'
            customer_id = id_

        cs = Cs(customer_id,stts)

main()
