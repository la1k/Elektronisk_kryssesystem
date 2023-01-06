import  tkinter as tk
from rfid import wait_for_rfid
import mysql.connector, os, sys
from dbkey import passwd


def showMessage(message, type='info', timeout=2500):
      from tkinter import messagebox as msgb
      root = tk.Tk()
      root.withdraw()
      try:
          root.after(timeout, root.destroy)
          if type == 'info':
              msgb.showinfo('Info', message, master=root)
          elif type == 'warning':
              msgb.showwarning('Warning', message, master=root)
          elif type == 'error':
              msgb.showerror('Error', message, master=root)
      except:
          pass
    
def signal_handler(signum, frame):
    print('timed out...')
    os.execl(sys.executable, sys.executable, *sys.argv)

class BackendHandler:

    mydb = mysql.connector.connect(
        host="localhost",
        user="morten",
        password="CumRocket!",
        database="krysseliste"
    )
    

    def wait_for_user(self):

        

        return self.getUser(wait_for_rfid())
        


    def getUser(self, nfc=-1, username=""):
    
        if username=="" and nfc > 0:
            mycursor = self.mydb.cursor()
            user = f"SELECT username, balance, can_spend FROM users WHERE rfid = '{nfc}'"
            mycursor.execute(user)
            res = mycursor.fetchall()
            if res == []:
                return gui.user_create(nfc=nfc)
                    
                
            if len(res) > 1:
                raise Exception ('Multiple users found, shit :/')
            return res[0]


        elif nfc==-1 and username != "":
            mycursor = self.mydb.cursor()
            user = f"SELECT username, balance, can_spend FROM users WHERE username = '{username}'" 
            mycursor.execute(user)
            res = mycursor.fetchall()
            if len(res) == 0:
                raise Exception ('No user found')
            if len(res) > 1:
                raise Exception ('Multiple users found, shit :/')
            return res[0]
        else:
            raise Exception ('Function requiers one input!')

    def create_user(self, username, nfc):

            mycursor = self.mydb.cursor()
            userT = f"SELECT username, balance, can_spend FROM users WHERE username = '{username}'"
            mycursor.execute(userT)
            res = mycursor.fetchall()
            if res == []:
                showMessage(type='error', message="Bruker finnes ikke snakk med hybelsjef", timeout=5000)
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                print(nfc, " ", res[0][0])
                user = f"UPDATE users SET rfid = '{int(nfc)}' WHERE username = '{res[0][0]}'"
                mycursor.execute(user)
                self.mydb.commit()
                os.execl(sys.executable, sys.executable, *sys.argv)

    def transaction(self, username, sum):

        user = self.getUser(username=username)

        balance = float(user[1])

        if user[2] or balance >= 0:
            mycursor = self.mydb.cursor()
            user = f"UPDATE users SET balance = '{balance-sum}' WHERE username = '{user[0]}'"
            mycursor.execute(user)
            self.mydb.commit()
            showMessage(f'Du brukte {sum} og har nå igjen {balance-sum} kronasj', timeout=4000)
            print(f'boughtn {balance-sum} and {user[0]}')
            os.execl(sys.executable, sys.executable, *sys.argv)
            
        else:
            showMessage('Du må sette inn mer penger på UFS og snakke med hybelsjef', type='error', timeout=4000)
            os.execl(sys.executable, sys.executable, *sys.argv)

backend = BackendHandler()

class GUIhandler:

    total_sum=0
    total_timer=0
    price_nordals=35
    price_Austman=40
    price_Drink=50
        
    def main_window(self, username="", balance=0):
        self.root = tk.Tk()
        self.root.title('ARK krysseliste')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        ico = tk.PhotoImage(file='icon.png')
        self.root.tk.call('wm', 'iconphoto', self.root._w, ico)
        self.root.after(45000, self.on_closing)
        

        #images:

        nordals = tk.PhotoImage(file='img/Nordahls.png')
        austmann = tk.PhotoImage(file='img/Austmann.png')
        drink = tk.PhotoImage(file='img/Drink.png')
        five = tk.PhotoImage(file='img/5.png')
        ten = tk.PhotoImage(file='img/10.png')

        N1 = tk.PhotoImage(file='img/N1.png')
        N2 = tk.PhotoImage(file='img/N2.png')
        N3 = tk.PhotoImage(file='img/N3.png')
        N4 = tk.PhotoImage(file='img/N4.png')
        N5 = tk.PhotoImage(file='img/N5.png')
        N6 = tk.PhotoImage(file='img/N6.png')
        N7 = tk.PhotoImage(file='img/N7.png')
        N8 = tk.PhotoImage(file='img/N8.png')
        N9 = tk.PhotoImage(file='img/N9.png')
        N0 = tk.PhotoImage(file='img/N0.png')



        #greeting

        # self.label = tk.Label(self.root, text='ARK krysseliste:', font=('Arial', 18))
        # self.label.pack(padx=10, pady=10)

        # self.label1 = tk.Label(self.root, text=f'Hei {username} du har {balance} kronasj', font=('Arial', 18))
        # self.label1.pack(padx=10, pady=10)

        #main buttonframe

        self.buttonframe = tk.Frame(self.root)
        self.btn1 = tk.Button(self.buttonframe, image=nordals, font=('Arial', 18), command=lambda: self.update_window(price=self.price_nordals, mult=1))
        self.btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.btn2 = tk.Button(self.buttonframe, image=five, text='+5', font=('Arial', 18), command=lambda: self.update_window(price=self.price_nordals, mult=5))
        self.btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.btn3 = tk.Button(self.buttonframe, image=ten, text='+10', font=('Arial', 18), command=lambda: self.update_window(price=self.price_nordals, mult=10))
        self.btn3.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.btn4 = tk.Button(self.buttonframe, image=austmann, font=('Arial', 18), command=lambda: self.update_window(price=self.price_Austman, mult=1))
        self.btn4.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.btn5 = tk.Button(self.buttonframe, image=five, text='+5', font=('Arial', 18), command=lambda: self.update_window(price=self.price_Austman, mult=5))
        self.btn5.grid(row=1, column=1, sticky=tk.W+tk.E)
        self.btn6 = tk.Button(self.buttonframe, image=ten, text='+10', font=('Arial', 18), command=lambda: self.update_window(price=self.price_Austman, mult=10))
        self.btn6.grid(row=1, column=2, sticky=tk.W+tk.E)
        self.btn7 = tk.Button(self.buttonframe, image=drink, font=('Arial', 18), command=lambda: self.update_window(price=self.price_Drink, mult=1))
        self.btn7.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.btn8 = tk.Button(self.buttonframe, image=five, text='+5', font=('Arial', 18), command=lambda: self.update_window(price=self.price_Drink, mult=5))
        self.btn8.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.btn9 = tk.Button(self.buttonframe, image=ten, text='+10', font=('Arial', 18), command=lambda: self.update_window(price=self.price_Drink, mult=10))
        self.btn9.grid(row=2, column=2, sticky=tk.W+tk.E)
        self.buttonframe.grid(column=0, row=2, rowspan=8)
        

       #Totals

        self.label2 = tk.Label(self.root, text=f'Egendefinert pris:', font=('Arial', 18))
        self.label2.grid(column=1, columnspan=3, row=2, rowspan=1)

        self.subtotal = tk.Entry(self.root, font=('Arial', 18))
        self.subtotal.grid(column=1, columnspan=3, row=3, rowspan=1)

        self.subUpdate = tk.Button(text='Oppdater', command=lambda: self.update_window(), height=3, width=8)
        self.subUpdate.grid(column=1, row=5, rowspan=1)

        self.label2 = tk.Label(self.root, text=f'Total:', font=('Arial', 18))
        self.label2.grid(column=1,columnspan=3, row=6, rowspan=1)

        self.total = tk.Entry(self.root, font=('Arial', 18))
        self.total.grid(column=1,columnspan=3, row=7, rowspan=1)

        #Buy and reset Button
        self.buy = tk.Button(text='Nullstill', command=lambda: self.update_window(reset=True), height=3, width=8)
        self.buy.grid(column=1, row=8, rowspan=1)

        self.buy = tk.Button(text='Kjøp', command=lambda: self.update_window(buy=True, username=username), height=3, width=8)
        self.buy.grid(column=3, row=8, rowspan=1)

        self.buttonframe1 = tk.Frame(self.root)
        self.btn1 = tk.Button(self.buttonframe1, image=N1, font=('Arial', 18), command=lambda: self.numpad(1))
        self.btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.btn2 = tk.Button(self.buttonframe1, image=N2, text='+5', font=('Arial', 18), command=lambda: self.numpad(2))
        self.btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.btn3 = tk.Button(self.buttonframe1, image=N3, text='+10', font=('Arial', 18), command=lambda: self.numpad(3))
        self.btn3.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.btn4 = tk.Button(self.buttonframe1, image=N4, font=('Arial', 18), command=lambda: self.numpad(4))
        self.btn4.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.btn5 = tk.Button(self.buttonframe1, image=N5, text='+5', font=('Arial', 18), command=lambda: self.numpad(5))
        self.btn5.grid(row=1, column=1, sticky=tk.W+tk.E)
        self.btn6 = tk.Button(self.buttonframe1, image=N6, text='+10', font=('Arial', 18), command=lambda: self.numpad(6))
        self.btn6.grid(row=1, column=2, sticky=tk.W+tk.E)
        self.btn7 = tk.Button(self.buttonframe1, image=N7, font=('Arial', 18), command=lambda: self.numpad(7))
        self.btn7.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.btn8 = tk.Button(self.buttonframe1, image=N8, text='+5', font=('Arial', 18), command=lambda: self.numpad(8))
        self.btn8.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.btn9 = tk.Button(self.buttonframe1, image=N9, text='+10', font=('Arial', 18), command=lambda: self.numpad(9))
        self.btn9.grid(row=2, column=2, sticky=tk.W+tk.E)
        self.btn0 = tk.Button(self.buttonframe1, image=N0, text='+10', font=('Arial', 18), command=lambda: self.numpad(0))
        self.btn0.grid(row=3, column=1, sticky=tk.W+tk.E)
        self.buttonframe1.grid(column=4, row=2, rowspan=4)


        self.root.mainloop()


    def numpad(self, number):
        self.subtotal.insert(tk.END, string= f'{number}')


    def update_window(self, price=0, mult=1, reset=False, buy=False, username="", backend = backend):
        subtotal = 0

        if reset:
            self.total_sum = 0
            self.total.delete(0, tk.END)
            self.subtotal.delete(0, tk.END)
            self.total.insert(tk.INSERT, string= f'{self.total_sum}')
            return


        try:
            if len(self.subtotal.get()) == 0:
                subtotal = 0
            else: 
                subtotal = int(self.subtotal.get())
        except ValueError:
            print('value error', self.subtotal.get())

        self.total_sum += price*mult + subtotal
        if buy:

            try:
                if len(self.total.get()) == 0:
                    self.total_sum = 0
                else: 
                    self.total_sum = int(self.total.get())
            except ValueError:
                print('value error', self.subtotal.get())
            
            self.root.destroy()
            backend.transaction(username=username, sum= self.total_sum + subtotal)
            
        self.total.delete(0, tk.END)
        self.subtotal.delete(0, tk.END)
        self.total.insert(tk.INSERT, string= f'{self.total_sum}')

    def user_create(self, nfc):
        user_C = tk.Tk()
        user_C.title("Lag bruker")
        ico = tk.PhotoImage(file='icon.png')
        user_C.tk.call('wm', 'iconphoto', user_C._w, ico)
        user_C.after(45000, self.on_closing)

        user_C.lift()

        label1 = tk.Label(user_C, text='Det er ingen brukere på dette kortet \n venligst skriv ufs brukernavn under:')
        label1.pack()

        entry1 = tk.Entry(user_C)
        entry1.pack()

        button = tk.Button(user_C, text='Lag Bruker', command=lambda: backend.create_user(entry1.get(), nfc))
        button.pack()

        user_C.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        user_C.mainloop()

    def on_closing(self):
        os.execl(sys.executable, sys.executable, *sys.argv)


gui = GUIhandler()

user = backend.wait_for_user()


gui.main_window(username=user[0], balance=user[1])


