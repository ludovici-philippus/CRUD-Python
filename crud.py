import sqlite3, os, time, winsound

class Manager:
    def __init__(self):
        self.name = ""
        self.phone = ""
        self.address = ""

    def add(self):
        running = True
        while running:
            os.system("cls")
            print("---------- ADD A NEW CONTACT ----------")
            print("PRESS (SHIFT+Q) TO CANCEL")
            print()

            temp_name = input("Name: ")
            if len(temp_name) != 0 and temp_name != "Q".upper():
                db = sqlite3.connect("connection")
                cursor = db.cursor()
                cursor.execute("SELECT Name FROM contacts")
                results = cursor.fetchall()
                for i in results:
                    if temp_name in i:
                        print("THIS CONTACT ALREADY EXISTS")
                        time.sleep(3)
                        self.add()
                self.name = temp_name
                temp_name = ""
                self.phone = input("Phone: ")
                time.sleep(0.20)
                self.address = input("Address: ")
                cursor.execute("""INSERT INTO contacts
                                (Name, Phone, Address)VALUES(?, ?, ?)""", 
                                (self.name, self.phone, self.address))
                db.commit()
                add_more = input("DO YOU WANT TO ADD ANOTHER CONTACT? (Y/N): ").capitalize()
                if add_more == "Y":
                    continue
                else:
                    db.close()
                    running = False
                    print("QUITTING THE MENU")
                    time.sleep(2)
                    self.menu()
            elif temp_name == "Q".upper():
                print("QUITTING THE MENU")
                time.sleep(2)
                self.menu()
            else:
                winsound.Beep(3000, 100)
                print("PLEASE FILL ALL FIELDS")
                time.sleep(2)
                self.add()
    
    def update(self):
        print()
        print("---------- UPDATE CONTACT ----------")
        print()
        name = input("PLEASE, ENTER THE CLIENT'S NAME TO UPDATE: ")
        confirm = input(f"ARE YOU SURE YOU WANT TO UPDATE {name} (Y/N): ").capitalize()
        if confirm == "Y":
            db = sqlite3.connect("connection")
            cursor = db.cursor()
            want_name = input("DO YOU WANT TO UPDATE THE NAME? (Y/N): ").capitalize()
            if want_name == "Y":
                new_name = input("ENTER THE NEW NAME: ")
                cursor.execute("""UPDATE contacts SET Name = ? WHERE Name = ?""", 
                                (new_name, name))
            
            want_phone = input("DO YOU WANT TO UPDATE THE PHONE? (Y/N): ").capitalize()
            if want_phone == "Y":
                new_phone = input("ENTER THE NEW PHONE: ")
                cursor.execute("UPDATE contacts SET Phone = ? WHERE Name = ?", 
                                (new_phone, name))
            
            want_address = input("DO YOU WANT TO UPDATE THE ADDRESS? (Y/N): ").capitalize()
            if want_address == "Y":
                new_address = input("ENTER THE NEW ADDRESS: ")
                cursor.execute("UPDATE contacts SET Address = ? WHERE Name = ?", 
                                (new_address, name))

            db.commit()
            print("CONTACT SUCCESSFULLY UPDATED")
            time.sleep(2)
            self.menu()
        else:
            winsound.Beep(2000, 50)
            print("UPDATE CANCELLED")
            time.sleep(2)
            self.menu()

    def remove(self):
        print()
        print("---------- REMOVE CONTACT ----------")
        print()
        name = input("PLEASE, ENTER THE CLIENT'S NAME TO DELETE: ")
        confirm = input(f"ARE YOU SURE YOU WANT TO DELETE {name} (Y/N): ").capitalize()
        if confirm == "Y":
            db = sqlite3.connect("connection")
            cursor = db.cursor()
            cursor.execute("DELETE FROM contacts WHERE Name = ?", (name,))
            db.commit()
            print("REGISTRATION SUCCESSFULLY REMOVED")
            time.sleep(3)
            self.menu()
        
        else:
            print("---------- QUITTING THE MENU ----------")
            time.sleep(3)
            self.menu()

    def get_list(self):
        count = 0
        count_2 = 0
        db = sqlite3.connect("connection")
        cursor = db.cursor()
        os.system("cls")
        print("---------- CONTACTS ----------")
        time.sleep(0.5)
        cursor.execute("SELECT Name, Phone, Address FROM contacts")
        results = cursor.fetchall()
        for row in results:
            time.sleep(0.5)
            count += 1
            count_2 += 1
            print(f"{count_2} - {row}")
            if count == 5:
                input("PRESS ANY KEY TO CONTINUE")
                count = 0
                print()
        print()
        print("END OF RESULTS")
        print()
        print("PRESS ANY KEY TO CONTINUE")
        option = input("PRESS (U) TO UPDATE, (D) TO DELETE OR (M) TO MENU: ").capitalize()
        if option == "U":
            self.update()
        elif option == "D":
            self.remove()
        elif option == "M":
            self.menu()

    def terminate(self):
        confirm = input("ARE YOU SURE YOU WANT TO QUIT? (Y/N): ").capitalize()
        if confirm == "Y":
            print("---------- SEE YOU LATER ----------")
            for i in range(5, 0, -1):
                time.sleep(0.5)
                winsound.Beep(1000*i, 100)
                print("."*i)
            exit()
        else:
            self.menu()

    def menu(self):
        os.system("cls")
        winsound.Beep(2000, 50)
        print("-=-=-=-=-=- MENU -=-=-=-=-=-")
        time.sleep(0.05)
        print()
        print("1 :) Add")
        time.sleep(0.05)
        print("2 :) Remove")
        time.sleep(0.05)
        print("3 :) Update")
        time.sleep(0.05)
        print("4 :) List")
        time.sleep(0.05)
        print("5 :) Terminate")
        print()

        opcao = input("Select an action: ")
        if opcao == "1":
            self.add()

        elif opcao == "2":
            self.remove()

        elif opcao == "3":
            self.update()

        elif opcao == "4":
            self.get_list()

        elif opcao == "5":
            self.terminate()

        else:
            winsound.Beep(2500, 100)
            print("INVALID OPTION! SELECT AN OPTION BETWEEN 1 AND 5")
            time.sleep(2)

    def main(self):
        if os.path.isfile("connection"):
            db = sqlite3.connect("connection")
            time.sleep(3)
            winsound.Beep(2000, 50)
            print()
            
            print("SUCCESSFULLY CONNECTED!")
            time.sleep(3)
            self.menu()
        else:
            print("FAILED CONNECTION. THIS CONNECTION DOES NOT EXIST.")
            print()
            time.sleep(3)
            winsound.Beep(2000, 50)

            print("Creating new connection file...")
            time.sleep(3)
            db = sqlite3.connect("connection")

            cursor = db.cursor()
            cursor.execute("""CREATE TABLE contacts
                            (Name TEXT, Phone TEXT, Address TEXT)""")

            winsound.Beep(2000, 50)
            print()

            print("CONNECTION SUCCESSFULLY CREATED")
            print("SUCCESSFULLY CONNECTED!")
            time.sleep(3)
            self.menu()


        self.menu()


contacts_manager = Manager()
contacts_manager.main()