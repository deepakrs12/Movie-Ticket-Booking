"""
 **** Console based Movie Ticket Reservation ****
Assumption : Currently supports only one theater seat reservation for a single
             movie show with specified date & time by Admin
Project modules : Admin, User, Booking, Payment
"""
import sys
import sqlite3
from Admin import Admin
from User import User

connection = sqlite3.connect('db_movie.db')
query = connection.cursor()

class Movie:
    def __init__(self):
        self.choices = {
            "1": self.admin,
            "2": self.user,
            "3": self.exit
        }

    def main_menu(self):
        print("""
                 *************************
                       WELCOME TO 
                    " BOOK MY SHOW "
                        1. ADMIN
                        2. USER   
                        3. EXIT
                 *************************
        """)

    def run(self):
        while True:
            self.main_menu()
            choice = input("Enter an option : ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{} is not a valid choice".format(choice))

    def admin(self):
        password = input("Enter ADMIN password : ")
        try:
            log = query.execute("select password from tbl_adminlogin where user_name = 'admin' ")
            passwordlist = log.fetchone()
            for i in passwordlist:
                passcode = i
            if (passcode == password):
                Admin().run(connection, query)
            else:
                print("Sorry Wrong password!")
        except Exception as ex:
            print("Oops something went wrong", ex)

    def user(self):
        User().run(connection,query)

    def exit(self):
        print("Thank you for using our service!!!")
        sys.exit(0)


if __name__ == '__main__':
    Movie().run()

connection.close()



