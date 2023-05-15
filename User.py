import sqlite3
import re
import random
from datetime import datetime
import traceback

connection = sqlite3.connect('db_movie.db')
query = connection.cursor()

s1 = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10']
s2 = ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10']
s3 = ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','I1','I2','I3','I4','I5','I6','I7','I8','I9','I10']

count1 = count2 = count3 = tots1 = tots2 = tots3 = 0
usr_seat = []
usrseat = ""
flag = True

class User:
    def __init__(self):
        self.choices = {
            "1": self.view_movie,
            "2": self.cancel_book,
            "3": self.exit
        }

    def display(self):
        print("\t                ) () ) * () ( ) () ")
        print("\t         ( ( /( () /( () /( () ` ( /() )\ ) () /( () /( () ( ")
        print("\t     ( )\ )\()) )\()) )\()) )\))( )\()) (()/( )\()) )\()) )\))(  ")
        print("\t  )((_) ((_)\ ((_)\ ((_)\ ((_)()\ ((_)\ /(_)) ((_)\ ((_)\ ((_)()\ ) ")
        print("\t ((_)_ ((_)  ((_) _ ((_)  (_()((_) __ ((_)  (_)) _((_)  ((_) _(()) \_)() ")
        print("\t | _ ) / _ \ / _ \ | |/ / |  \/  | \ \ / / / __| | || | / _ \ \ \((_)/ / '")
        print("\t | _ \ |(_) ||(_)| | '<   | |\/| |  \ V /  \__ \ | __ | |(_)|  \ \/\/ / ")
        print("\t |___/ \___/ \___/ |_|\_\ |_|  |_|   |_|   |___/ |_||_| \___/   \_/\_/ ")

    def user_menu(self):
        self.display()
        print("""
                 ***** THE PINNACLE THEATER *****
                 ********************************
                        1. SHOW NEW MOVIE 
                        2. CANCEL BOOKING
                        3. EXIT 
                 ********************************
        """)

    # switching through option
    def run(self,connection,query):
        global flag
        while flag:
            self.user_menu()
            choice = input("Enter an option : ")
            action = self.choices.get(choice)
            if action:
                action(connection,query)
            else:
                print("{} is not a valid choice".format(choice))

    # display currently shown movie details in theater
    def view_movie(self,connection,query):
        try:
            query.execute("select mov_name,mov_duration,mov_show_time,mov_show_date from tbl_movie")
            for row in query.fetchall():
                r = 1
            print("\n************************** MOVIE DETAILS ***************************")
            print("   Movie\t\t|\tDuration\t|\tShow Time\t|\tShow Date")
            print(" ------------------------------------------------------------------")
            print(" ","\t\t|  ".join(row))
            selid = query.execute("select mov_id from tbl_movie")
            for row1 in selid.fetchall():
                r1 = 1
            for i in row1:
                mid = i
        except Exception as ex:
            print("Oops something went wrong",ex)
        #  Continue to book the available movie , proceed with login or register
        while True:
            ch = input("\nDo you want to book this movie (Y/N) : ")
            if ch in ('Y', 'y'):
                ch1 = input("\n\t| 1. Login    |\n\t| 2. Register |\n\t| 3. Go back  |\nEnter your choice to proceed : ")
                if ch1 == '1':
                    self.login(mid,connection,query)
                elif ch1 == '2':
                    self.register(mid,connection,query)
                elif ch1 == '3':
                    self.run(connection,query)
            elif ch in ('N', 'n'):
                self.run(connection,query)

    # display available seat details for that particular theater
    def display_seats(self,usid,mid,connection,query):
        usid = usid
        mid = mid
        print("""
                 -------------- Seat Category ----------------
                    | (A - C) Row No (1-3) NORMAL Rs.150   |
                    | (D - F) Row No (4-6) GOLD Rs.250     |
                    | (G - I) Row No (7-9) PLATINUM Rs.300 |
                """)
        selc = query.execute("select * from tbl_seats")
        for row in selc.fetchall():
            print(row, end=" ")
            print(end="\n")
        self.reserve(usid,mid,connection,query)

    # processing seat booking and total cost for booked seats
    def reserve(self,usid,mid,connection,query):
        usid = usid
        mid = mid
        global count1, count2, count3, tots1, tots2, tots3, usr_seat, usrseat
        isbk = set()
        rowno = input("Enter row number : ")
        res = input("Enter seats value to reserve : ")
        rr = []
        for e in res.split(","):
            rr.append(e)
        #  checking if seats already booked by any user
        ins_seat = query.execute("select seats from tbl_user_seats")
        for row in ins_seat:
            isbk = row
        try:
            for r in rr:
                if r not in isbk:
                    # updating seat data based on user input on validation
                    resv = query.execute("select s1,s2,s3,s4,s5,s6,s7,s8,s9,s10 from tbl_seats where sid = :m1",(rowno,))
                    for row in resv.fetchall():
                        if r in row:
                            query.execute("""update tbl_seats set s1 = case when s1 = :p1 then '* ' else s1 end , s2 = case when s2 = :p1 then '* ' else s2 end,
                                           s3 = case when s3 = :p1 then '* ' else s3 end, s4 = case when s4 = :p1 then '* ' else s4 end,
                                           s5 = case when s5 = :p1 then '* ' else s5 end, s6 = case when s6 = :p1 then '* ' else s6 end,
                                           s7 = case when s7 = :p1 then '* ' else s7 end, s8 = case when s8 = :p1 then '* ' else s8 end,
                                           s9 = case when s9 = :p1 then '* ' else s9 end, s10 = case when s10 = :p1 then '* ' else s10 end
                                           where sid = :p2 """,(r,rowno,))
                            query.execute("insert into tbl_user_seats values (:k2)", (r,))
                            connection.commit()
                        else:
                            print("Selected seat is not available in row : ", rowno)
                            self.reserve(usid,mid,connection,query)
                else:
                    print("seat already booked !!!")
                    self.reserve(usid,mid,connection,query)
                if r in s1:
                    count1 += 1
                    tots1 = 150 * count1
                elif r in s2:
                    count2 += 1
                    tots2 = 250 * count2
                elif r in s3:
                    count3 += 1
                    tots3 = 300 * count3
                usr_seat.append(r)
        except Exception as ex:
            print(ex)
        # option to book more seats if required
        while True:
            ch = input("Do you want to book more seats (Y/N) : ")
            if ch in ('Y', 'y'):
                self.reserve(usid,mid,connection,query)
            elif ch in ('N', 'n'):
                total = tots1 + tots2 + tots3
                usrseat = ",".join(usr_seat)
                tdydate = datetime.now().strftime('%Y-%m-%d %H:%M')
                bid = str(random.randint(0000, 9999))
                bookId = "BOOK" + bid
                try:
                    book = query.execute("insert into tbl_booking(book_id,b_username, b_date_time, b_mov_date, b_seats, b_tot_price) values (:b1, (select u_name from tbl_user where u_id = :v1),:v2,(select mov_show_date from tbl_movie where mov_id = :v3),:v4,:v5)",(bookId,usid,tdydate,mid,usrseat,total,))
                    connection.commit()
                    if book:
                        print("Movie booking successfull")
                        # displaying user booking infromation
                        bklist = []
                        bsel = query.execute("select * from tbl_booking")
                        for brow in bsel:
                            bs = 1
                        for k in brow:
                            bklist.append(k)
                        print("\t**************************************************")
                        print("\t  Booking ID : ", bklist[0])
                        print("\t  Booking Date & Time : ", bklist[2])
                        print("\t  Booked Movie Date : ", bklist[3])
                        print("\t  Booked seats : ", bklist[4])
                        print("\t  Total Price : ", bklist[5])
                        print("\t**************************************************")
                        bknid = query.execute("select book_id from tbl_booking where book_id =:b", (bookId,))
                        for bk in bknid.fetchall():
                            for j in bk:
                                bkid = j
                        self.payment(usid, bkid, connection, query)
                    else:
                        print("Error booking")
                except Exception as ex:
                    print("Oops something went wrong", ex)

    # display user name and proceed to booking seats
    def booking(self, usid, mid, connection,query):
        usid = usid
        mid = mid
        try:
            usr = query.execute("select u_name from tbl_user where u_id = :p1",(usid,))
            print("\n\t\t\t\t\t\t***** WELCOME ",''.join(usr.fetchone())," *****")
            self.display_seats(usid,mid, connection,query)
        except Exception as ex:
            print("Oops something went wrong", ex)

    # authentication for already registered user to book a movie
    def login(self,mid,connection,query):
        userid = 0
        mid = mid
        usrid = []
        username = input("Enter your username : ")
        passwd = input("Enter your password : ")
        try:
            log = query.execute("select u_id, u_name, u_passwd from tbl_user where u_name = :p1 and u_passwd = :p2", (username, passwd,))
            for row in log:
                usrid.append(row[0])
                for i in usrid:
                    userid = i
                if row:
                    print("\n\t----- Successfully logged in -----")
                    self.booking(userid, mid, connection,query)
            else:
                print("Wrong username or password")
                self.login(mid,connection,query)
        except Exception as ex:
            print("Oops something went wrong",ex)

    # new user registration for booking a movie with regx validation
    def register(self,mid,connection,query):
        mid = mid
        username = input("Enter your username : ")
        while not re.match(r'^[A-Za-z]*$', username):
            print("Error ! Make sure you only use letters for your username")
            username = input("Enter your username : ")
        email = input("Enter your email address (xyz@mail.com) : ")
        while not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            print("Error ! Enter valid email address")
            email = input("Enter your email address : ")
        mob = input("Enter your mobile number (+91) : ")
        while not re.match(r'^([+][9][1]|[9][1]|[0]){0,1}([7-9]{1})([0-9]{9})$', mob):
            print("Error ! Enter valid mobile number (+91)")
            mob = input("Enter your mobile number (+91) : ")
        password = input("Enter the password : ")
        while not re.match(r'^[A-Za-z0-9@#$%^&+=]{6,}$', password):
            print("Error ! Password must cointain atleast 6 characters, one uppercase & one digit")
            password = input("Enter the password : ")
        re_password = input("Re-enter the password : ")
        try:
            while re_password != password:
                print("Password does not match")
                password = input("Enter the password : ")
                re_password = input("Re-enter the password : ")
            if password == re_password:
                uid = str(random.randint(0000, 9999))
                usrId = "USER" + uid
                query.execute("Insert into tbl_user (u_id,u_name,u_email,u_passwd,u_mobile) values(:ui,:un, :ue, :p, :um)", {'ui':usrId, 'un': username, 'ue': email, 'p': password, 'um': mob})
                print("\n\t----- Successfully registered -----")
                connection.commit()
        except Exception as ex:
            print("Oops something went wrong",ex)
        # option to proceed to login for booking
        while True:
            ch = input("\nDo you want to Login (Y/N) : ")
            if ch in ('Y', 'y'):
                self.login(mid,connection,query)
            elif ch in ('N', 'n'):
                self.run(connection,query)

    # process user payment details
    def payment(self,usid,bkid,connection,query):
        bkid = bkid
        print("""
                ******************************
                      PAYMENT GATEWAY
                ------------------------------
                    1. CREDIT/DEBIT CARD
                    2. NET BANKING
                ******************************
        """)
        while True:
            ch = int(input("Enter the choice : "))
            if ch == 1:
                crnumber = input("Enter Credit/Debit card number (XXXX-XXXX-XXXX-XXXX) : ")
                while not re.match(r'^[0-9 \-]+$',crnumber):
                    print("Please enter valid credit card number")
                    crnumber = input("Enter Credit/Debit card number (XXXX-XXXX-XXXX-XXXX) : ")
                cr = len(str(crnumber).replace("-",""))
                if cr == 16:
                    cvvno = int(input("Enter CVV no : "))
                    cv = len(str(cvvno))
                    if cv == 3:
                        cpin = int(input("Enter Pin number : "))
                        cp = len(str(cpin))
                        if cp == 4:
                            pid = str(random.randint(0000, 9999))
                            payId = "PAY" + pid
                            try:
                                pay = query.execute("insert into tbl_payment(p_id,p_usr_id,p_tot_cost,p_credit,p_cvv,p_pin) values (:c1, (select u_id from tbl_user where u_id =:u1),(select b_tot_price from tbl_booking where book_id =:u2),:u3,:u4,:u5)",(payId,usid,bkid,crnumber,cvvno,cpin,))
                                connection.commit()
                                if pay:
                                    print("Payment made successfully")
                                    print("**Please provide QR code sent to your email at BOX OFFICE")
                                else:
                                    print("Error payment")
                            except Exception as ex:
                                print("Oops something went wrong", ex)
                self.run(connection, query)
            elif ch == 2:
                print("\t**Future Implemntation, Under Maintainence")

    # cancel booking
    def cancel_book(self,connection,query):
        rlist = []
        ruser = input("Enter your username : ")
        rpass = input("Enter your password : ")
        try:
            auth = query.execute("select u_name, u_passwd from tbl_user where u_name = :p1 and u_passwd = :p2",(ruser,rpass,))
            for row in auth.fetchall():
                rusername = row[0]
                if row:
                    print("\t\t\t******** BOOKING HISTORY **********")
                    print("---------------------------------------------------------------------------------")
                    print(" BOOKING ID |  BOOKING DATETIME  |   MOVIE DATE   | SEATS BOOKED | TOTAL AMOUNT")
                    print("---------------------------------------------------------------------------------")
                    disp_usrb = query.execute("select book_id,b_date_time,b_mov_date,b_seats,b_tot_price from tbl_booking where b_username = :l1",(rusername,))
                    for rl in disp_usrb:
                        print(" "+rl[0]+"\t|\t"+rl[1]+"\t|\t"+rl[2]+"\t|\t"+rl[3]+"\t|\t"+str(rl[4]))
                    bk_id = input("\nEnter the Booking ID : ")
                    bk_date = input("Enter the Booking date in (YYYY-MM-DD) format : ")
                    while not re.match(r'^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$',bk_date):
                        print("Please enter valid date and time")
                        bk_date = input("Enter the Booking date in (YYYY-MM-DD) format : ")
                    bookdate = datetime.strptime(bk_date,'%Y-%m-%d')
                    book_date = bookdate.date()
                    tddate = datetime.now().strftime('%Y-%m-%d')
                    ch = input("Confirm cancellation (Y/N) : ")
                    if ch == 'Y' or ch == 'y':
                        if book_date.__eq__(tddate):
                            bank_accno = input("Enter bank account number to refund the amount : ")
                            while not re.match(r'^[0-9]{10}$', bank_accno):
                                print("Please enter valid account number")
                                bank_accno = input("Enter bank account number to refund the amount : ")
                            b1 = query.execute("select book_id,b_seats from tbl_booking where book_id = :a1 and b_username = :a2",(bk_id,rusername,))
                            b11 = b1.fetchone()
                            for i in b11:
                                rlist.append(i[1])
                                idur = i[0]
                            query.execute("""create trigger if not exists aft_delete after delete on tbl_booking
                                             begin 
                                                insert into tbl_delete_booking(book_id, b_usrname, b_date_time, b_mov_date, b_seats, b_tot_price) values (old.book_id,old.b_username,old.b_date_time,old.b_mov_date,old.b_seats,old.b_tot_price);
                                             end;""")
                            urid = str(random.randint(0000, 9999))
                            urefId = "USER" + urid
                            ins_r = query.execute("insert into tbl_refund(r_id,r_date,r_bnk_accno,r_amount) values (:o1,:o2,:o3,(select b_tot_price from tbl_booking where book_id = :o4))",(urefId,bk_date,bank_accno,idur,))
                            if ins_r:
                                print("Booking cancelled successfully")
                                query.execute("delete from tbl_booking where book_id = :h1", (bk_id,))
                                connection.commit()
                                self.run(connection, query)
                        else:
                            print("Sorry cannot cancel the booking")
                            print("The cancel option is available only for the date on which booking is done")
                            print("Please send email to 'support.bookmyshow@gmail.com' for further details")
                            self.run(connection,query)
                    elif ch == 'N' or ch == 'n':
                        self.run(connection,query)
            else:
                print("Wrong username or password")
                self.cancel_book(connection, query)
        except Exception :
            print("Oops something went wrong",traceback.format_exc())


    # exit from the system
    def exit(self,connection,query):
        print("Thank you for using our service!!!")
        exit(0)

connection.close()