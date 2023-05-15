import sqlite3
from datetime import datetime
from datetime import date
import random

connection = sqlite3.connect('db_movie.db')
query = connection.cursor()

seats = [['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10'],
	     ['B1','B2','B3','B4','B5','B6','B7','B8','B9','B10'],
	     ['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10'],
	     ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10'],
	     ['E1','E2','E3','E4','E5','E6','E7','E8','E9','E10'],
	     ['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10'],
	     ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10'],
	     ['H1','H2','H3','H4','H5','H6','H7','H8','H9','H10'],
	     ['I1','I2','I3','I4','I5','I6','I7','I8','I9','I10']]

flag = True
movdate = datetime.strptime("3000-01-01","%Y-%m-%d")

class Admin():
    def __init__(self):
        self.choices = {
            "1": self.add_movie,
            "2": self.view_all_movies,
            "3": self.del_movie,
            "4": self.add_seats,
            "5": self.del_seats,
            "6": self.disp_seat_book,
            "7": self.del_user_seats,
            "8": self.check_user_book,
            "9": self.check_user_pay,
            "10": self.change_password,
            "11": self.cancel_book_reset,
            "12": self.exit
        }

    def admin_menu(self):
        print("""
                 ***** THE PINNACLE THEATER *****
                 ********************************
                    1.  ADD NEW MOVIE
                    2.  VIEW ALL MOVIES
                    3.  DELETE OLD MOVIE
                    4.  ADD SEATS
                    5.  DELETE SEATS
                    6.  VIEW BOOKED SEATS 
                    7.  DELETE USER SEAT BOOKING
                    8.  USER BOOKING HISTORY
                    9.  USER PAYMENT HISTORY
                    10. CHANGE ADMIN PASSWORD
                    11. RESET CANCELED SEATS
                    12. EXIT TO MAIN MENU
                 ********************************
        """)

    # switching through option
    def run(self,connection,query):
        global flag
        while flag:
            self.admin_menu()
            choice = input("Enter an option : ")
            action = self.choices.get(choice)
            if action:
                action(connection,query)
            else:
                print("{} is not a valid choice".format(choice))

    # inserting new movie
    def add_movie(self,connection,query):
        global movdate
        row = []
        query.execute("select mov_show_date from tbl_movie")
        for row in query.fetchall():
            m = 1
        movr = "".join(row)
        if movr:
            movdate = datetime.strptime(movr,"%Y-%m-%d")
        movName = input("Enter the movie name : ")
        movTime = input("Enter the movie duration in HH:MM:TT format : ")
        showTime = input("Enter the show time in HH:MM (AM/PM) format : ")
        showDate = input("Enter the show date in YYYY-MM-DD format : ")
        mdate = datetime.strptime(showDate, "%Y-%m-%d")
        # checking if date entered is less than current date
        while mdate.date() < date.today():
            print("Please enter valid movie show date")
            showDate = input("Enter the show date in YYYY-MM-DD format : ")
            mdate = datetime.strptime(showDate, "%Y-%m-%d")
        else:
            # checking if date entered is greater than already in show, movie date
            if not (mdate.date() > movdate.date()):
                mid = str(random.randint(0000, 9999))
                movId = "MOV" + mid
                try:
                    sql = query.execute("insert into tbl_movie(mov_id,mov_name, mov_duration, mov_show_time, mov_show_date) values(:m1,:p1,:p2,:p3,:p4)",(movId,movName,movTime,showTime,showDate,))
                    if sql:
                        print("Movie added successfully")
                    else:
                        print("Error adding movie")
                    connection.commit()
                except Exception as ex:
                    print("Oops something went wrong!!!",ex)
            else:
                print("\tCannot add for that specified date since there is a movie still shown in theater")

    # display all movies data
    def view_all_movies(self,connection,query):
        print("-------------------------------------------------------------")
        print(" MOV ID  |  MOV NAME | MOV DURATION | SHOW TIME | SHOW DATE")
        print("-------------------------------------------------------------")
        try:
            query.execute("""select * from tbl_movie""")
            for row in query.fetchall():
                print(row)
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # remove particular movie from db based on movie id
    def del_movie(self,connection,query):
        try:
            query.execute("""select mov_id,mov_name from tbl_movie""")
            for row in query.fetchall():
                print(row)
            mid = int(input("Enter movie id to delete : "))
            delmov = query.execute("delete from tbl_movie where mov_id = :p1",(mid,))
            if delmov:
                print("Movie removed successfully")
            else:
                print("Error removing movie")
            connection.commit()
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # add/reset theater seat data
    def add_seats(self,connection,query):
        try:
            query_string = 'INSERT INTO tbl_seats(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            if query.executemany(query_string, seats):
                print("Seats added successfully")
            connection.commit()
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # delete seat data once movie show date ends
    def del_seats(self,connection,query):
        try:
            delseats = query.execute("delete from tbl_seats")
            if delseats:
                print("Seats removed successfully")
            connection.commit()
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # display all booked seats details
    def disp_seat_book(self,connection,query):
        print("\t\t\t  ********** SEATS BOOKED **********")
        try:
            selc = query.execute("select * from tbl_seats ")
            for row in selc.fetchall():
                print(row, end=" ")
                print(end="\n")
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # delete user booked seat data once movie show date ends
    def del_user_seats(self,connection,query):
        try:
            delusrseats = query.execute("delete from tbl_user_seats")
            if delusrseats:
                print("Deleted booked seats successfully")
            connection.commit()
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # display all user booking history
    def check_user_book(self,connection,query):
        print("---------------------------------------------------------------------------")
        print(" BOOK ID  | USER NAME |    BOOK DATETIME    |  SHOW DATE |  SEATS | PRICE")
        print("---------------------------------------------------------------------------")
        try:
            bookdisp = query.execute("select * from tbl_booking")
            for row in bookdisp:
                print(row)
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # display all user payment history
    def check_user_pay(self,connection,query):
        print("------------------------------")
        print(" PAY ID   |  USER ID | PRICE ")
        print("------------------------------")
        try:
            paydisp = query.execute("select p_id,p_usr_id,p_tot_cost from tbl_payment")
            for row in paydisp:
                print(row)
        except Exception as ex:
            print("Oops something went wrong!!!", ex)

    # option for admin to change password
    def change_password(self, connection, query):
        old_pass = input("Enter current ADMIN password: ")
        new_pass = input("Enter new ADMIN password: ")
        new_pass_conf = input("Confirm new ADMIN password: ")
        if (new_pass.__eq__(new_pass_conf)):
            log = query.execute("select password from tbl_adminlogin where user_name = 'admin' ")
            passwordlist = log.fetchone()
            for i in passwordlist:
                passcode = i
            if passcode == old_pass:
                log = query.execute("update tbl_adminlogin set password= :p1 where user_name= 'admin' ",(new_pass,))
                if log:
                    connection.commit()
                    print("ADMIN password has been UPDATED.")
            else:
                print("Entered password is wrong")
        else:
            print("The Passwords dont match")

    def cancel_book_reset(self,connection, query):
        cnclList = []
        print("""
                         -------------- Seat Category ----------------
                            | (A - C) Row No (1-3) |
                            | (D - F) Row No (4-6) |
                            | (G - I) Row No (7-9) |
                        """)
        print("\t\t\t******** BOOKING HISTORY **********")
        print("---------------------------------------------------------------------------------")
        print(" BOOKING ID |  BOOKING DATETIME  |   MOVIE DATE   | SEATS BOOKED | TOTAL AMOUNT")
        print("---------------------------------------------------------------------------------")
        disp_usrb = query.execute("select book_id,b_date_time,b_mov_date,b_seats,b_tot_price from tbl_delete_booking")
        for rl in disp_usrb:
            r = 1
        print(" " + rl[0] + "\t|\t" + rl[1] + "\t|\t" + rl[2] + "\t|\t" + rl[3] + "\t|\t" + str(rl[4]))
        cncl = rl[3]
        cnclList = [x.strip() for x in cncl.split(',')]
        for i in range(0,len(cnclList)):
            seat_no = int(input("Enter seat number : "))
            seat_val = input("Enter seat value to reset : ")
            query.execute("""update tbl_seats set s1 = case when s1 = :p1 then :p1 else s1 end , s2 = case when s2 = :p1 then s2 = :p1 else s2 end,
                                                       s3 = case when s3 = :p1 then s3 = :p1 else s3 end, s4 = case when s4 = :p1 then s4 = :p1 else s4 end,
                                                       s5 = case when s5 = :p1 then s5 = :p1 else s5 end, s6 = case when s6 = :p1 then s6 = :p1 else s6 end,
                                                       s7 = case when s7 = :p1 then s7 = :p1 else s7 end, s8 = case when s8 = :p1 then s8 = :p1 else s8 end,
                                                       s9 = case when s9 = :p1 then s9 = :p1 else s9 end, s10 = case when s10 = :p1 then s10 = :p1 else s10 end
                                                       where sid = :p2 """, (seat_val, seat_no,))
            connection.commit()

    # return back to main menu
    def exit(self,connection,query):
        global flag
        flag = False

connection.close()