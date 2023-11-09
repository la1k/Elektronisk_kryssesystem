# coding=utf-8
import os
import sys
import tkinter as tk
from rfid import wait_for_rfid
from util import get_user_from_nfc_or_username, nfc_reg, update_usage, write_transaction, data_in, make_unblocked, get_transactions


#
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
    

class BackendHandler:

    def wait_for_user(self):
        os.system('killall matchbox-keyboard')



        return self.getUser(nfc=wait_for_rfid())
        
    def getUser(self, nfc):
        os.system('xrandr --display :0 -o inverted')
        os.system('xset -display :0 dpms force on')
        if get_user_from_nfc_or_username(nfc=nfc) == -1:
            os.system('DISPLAY=:0 matchbox-keyboard &')
            gui.user_create(nfc)
        elif len(get_user_from_nfc_or_username(nfc=nfc)) == 1:
            
            return get_user_from_nfc_or_username(nfc=nfc)
        else:
            return -1

    def create_user(self, username, nfc):
        ret = get_user_from_nfc_or_username(username=username)
        print(ret)
        if ret == -1:
            os.system('killall matchbox-keyboard')
            showMessage('Brukeren er ikke registrert i UFS snakk med hybelsjef!', type='error')
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif ret == -3:
            os.system('killall matchbox-keyboard')
            os.system('xset -display :0 dpms force off')
            os.execl(sys.executable, sys.executable, *sys.argv)
            
        elif len(ret) == 1:
            nfc_reg(username=username, nfc=nfc)
            os.system('killall matchbox-keyboard')
            showMessage('Brukeren er registrert på kortet :)')
            os.system('xset -display :0 dpms force off')
            os.execl(sys.executable, sys.executable, *sys.argv)

        else:
            os.system('killall matchbox-keyboard')
            os.system('xset -display :0 dpms force off')
            os.execl(sys.executable, sys.executable, *sys.argv)

    def transaction(self, username, sum):

        user = get_user_from_nfc_or_username(username=username)
        
        balance = float(user[0][4])
        if balance > 0 and user[0][7]:
            make_unblocked(username)

        if user[0][3] or balance > 0 or user[0][7]==False:
            spending = user[0][5]
            if spending == None:
                spending = 0
            update_usage(nfc=user[0][6],sum=sum)
            write_transaction(user, sum)
            showMessage('Du brukte %d og har brukt %d siden forgie avregning' % (sum, spending + sum), timeout=4000)
            os.system('xset -display :0 dpms force off')
            os.execl(sys.executable, sys.executable, *sys.argv)
            
        else:
            data_in()
            user = get_user_from_nfc_or_username(username=username)
            if user[0][3] or balance > 0 or user[0][7] == False:
                spending = user[0][5]
                if spending == None:
                    spending = 0
                update_usage(nfc=user[0][6],sum=sum)
                write_transaction(user, sum)
                showMessage(f'Du brukte {sum} og har brukt {spending+sum} siden forgie avregning', timeout=4000)

                os.system('xset -display :0 dpms force off')
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                showMessage('Du må sette inn mer penger på UFS og snakke med hybelsjef', type='error', timeout=4000)

                os.system('xset -display :0 dpms force off')
                os.execl(sys.executable, sys.executable, *sys.argv)



class GUIhandler:

    #Will move into a datbase, to simplyfy changeing prices
    total_sum=0
    total_timer=1
    price_nordals=30
    price_Austman=40
    price_Drink=50
    times_flag=False
    times_2er=1
    
    
    def __init__(self, backend):
        self.backend = backend
        
    def main_window(self, user):
        self.bg_c_btn = '#E0F5FF'
        self.bg_c = '#C6DBFF'
        self.root = tk.Tk()
        self.root.title('ARK krysseliste')
        self.root.wm_attributes('-fullscreen', 'True')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(45000, self.on_closing)
        self.starcount = 0
        self.root.configure(bg=self.bg_c)
        
        
        #images:
        nordals = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/Nordahls.png')
        austmann = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/Austmann.png')
        drink = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/Drink.png')

        N1 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N1.png')
        N2 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N2.png')
        N3 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N3.png')
        N4 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N4.png')
        N5 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N5.png')
        N6 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N6.png')
        N7 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N7.png')
        N8 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N8.png')
        N9 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N9.png')
        N0 = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/N0.png')
        NM = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/Nmin.png')
        NT = tk.PhotoImage(file='/home/la1k/Elektronisk_kryssesystem/img/NX.png')
        
        #greeting
        self.vel = tk.Label(self.root, text="Velkommen til RADIOLÅFTE!", font=('Arial', 22), bg=self.bg_c)
        self.vel.grid(row=0, column=0, columnspan=5)
        self.label1 = tk.Label(self.root, text=f'{user[0][2]}', font=('Arial', 18), bg=self.bg_c)
        self.label1.grid(column=4, row=2)
        self.label3 = tk.Label(self.root, text=f'UFS:{user[0][4]}', font=('Arial', 18), bg=self.bg_c)
        self.label3.grid(column=4, row=3)
       

        #main buttonframe
        self.buttonframe = tk.Frame(self.root)
        self.btn1 = tk.Button(self.buttonframe, image=nordals, font=('Arial', 18), command=lambda: self.update_window(price=self.price_nordals, mult=2), bg=self.bg_c_btn)
        self.btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.btn4 = tk.Button(self.buttonframe, image=austmann, font=('Arial', 18), command=lambda: self.update_window(price=self.price_Austman, mult=2), bg=self.bg_c_btn)
        self.btn4.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.btn7 = tk.Button(self.buttonframe, image=drink, font=('Arial', 18), command=lambda: self.update_window(price=self.price_Drink, mult=2), bg=self.bg_c_btn)
        self.btn7.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.buttonframe.grid(column=0, row=2, rowspan=8)
        

       #Totals

        self.label2 = tk.Label(self.root, text=f'Egendefinert:', font=('Arial', 18), bg=self.bg_c)
        self.label2.grid(column=1, columnspan=3, row=2, rowspan=1)
        self.subtotal = tk.Entry(self.root, font=('Arial', 18))
        self.subtotal.grid(column=1, columnspan=3, row=3, rowspan=1)
        #self.subtotal.focus_force()  #Need to grab nfc devs first
        self.subUpdate = tk.Button(text='Legg til', command=lambda: self.update_window(), height=3, width=8, bg=self.bg_c_btn )
        self.subUpdate.grid(column=1, row=5, rowspan=1)
        self.label2 = tk.Label(self.root, text=f'Total:', font=('Arial', 18), bg=self.bg_c)
        self.label2.grid(column=1,columnspan=3, row=6, rowspan=1)
        self.total = tk.Entry(self.root, font=('Arial', 18), takefocus=0)
        self.total.grid(column=1,columnspan=3, row=7, rowspan=1)

        #Buy and reset Button
        self.buy = tk.Button(text='Nullstill', command=lambda: self.update_window(reset=True), height=3, width=8, bg=self.bg_c_btn)
        self.buy.grid(column=1, row=8, rowspan=1)
        self.buy = tk.Button(text='Kryss', command=lambda: self.update_window(buy=True, username=user[0][1]), height=3, width=8, bg=self.bg_c_btn)
        self.buy.grid(column=3, row=8, rowspan=1)

        #numpad
        self.buttonframe1 = tk.Frame(self.root)
        self.btn1 = tk.Button(self.buttonframe1, image=N1, font=('Arial', 18), command=lambda: self.numpad('1'), bg=self.bg_c_btn)
        self.btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.btn2 = tk.Button(self.buttonframe1, image=N2, text='+5', font=('Arial', 18), command=lambda: self.numpad('2'), bg=self.bg_c_btn)
        self.btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.btn3 = tk.Button(self.buttonframe1, image=N3, text='+10', font=('Arial', 18), command=lambda: self.numpad('3'), bg=self.bg_c_btn)
        self.btn3.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.btn4 = tk.Button(self.buttonframe1, image=N4, font=('Arial', 18), command=lambda: self.numpad('4'), bg=self.bg_c_btn)
        self.btn4.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.btn5 = tk.Button(self.buttonframe1, image=N5, text='+5', font=('Arial', 18), command=lambda: self.numpad('5'), bg=self.bg_c_btn)
        self.btn5.grid(row=1, column=1, sticky=tk.W+tk.E)
        self.btn6 = tk.Button(self.buttonframe1, image=N6, text='+10', font=('Arial', 18), command=lambda: self.numpad('6'), bg=self.bg_c_btn)
        self.btn6.grid(row=1, column=2, sticky=tk.W+tk.E)
        self.btn7 = tk.Button(self.buttonframe1, image=N7, font=('Arial', 18), command=lambda: self.numpad('7'), bg=self.bg_c_btn)
        self.btn7.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.btn8 = tk.Button(self.buttonframe1, image=N8, text='+5', font=('Arial', 18), command=lambda: self.numpad('8'), bg=self.bg_c_btn)
        self.btn8.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.btn9 = tk.Button(self.buttonframe1, image=N9, text='+10', font=('Arial', 18), command=lambda: self.numpad('9'), bg=self.bg_c_btn)
        self.btn9.grid(row=2, column=2, sticky=tk.W+tk.E)
        self.btn9 = tk.Button(self.buttonframe1, image=N0, text='+10', font=('Arial', 18), command=lambda: self.numpad('0'), bg=self.bg_c_btn)
        self.btn9.grid(row=3, column=1, sticky=tk.W+tk.E)
        self.btnm = tk.Button(self.buttonframe1, image=NM, text='+10', font=('Arial', 18), command=lambda: self.numpad('-'), bg=self.bg_c_btn)
        self.btnm.grid(row=3, column=0, sticky=tk.W+tk.E)
        self.btnx = tk.Button(self.buttonframe1, image=NT, text='+10', font=('Arial', 18), command=lambda: self.numpad('*'), bg=self.bg_c_btn)
        self.btnx.grid(row=3, column=2, sticky=tk.W+tk.E)
        self.buttonframe1.grid(column=4, row=5, rowspan=4)

        #last transactions
        self.header_last = tk.Label(self.root, text=f'Siste 14 kryssinger', font=('Arial', 12), bg=self.bg_c)
        self.header_last.grid(column=5, row=1)
        self.usage = tk.Label(self.root, text=f'Totalt forbruk: {user[0][5]},-', font=('Arial', 12), bg=self.bg_c)
        self.usage.grid(column=5, row=0)
        self.transactionframe = tk.Frame(self.root)
        posr = 0
        for i in get_transactions(number=14, username=user[0][1]):
            tk.Label(self.transactionframe, text=f'{i[3].hour}:{i[3].minute}       {i[1]},-', font=('Arial', 12), bg=self.bg_c).grid(column=0, row=posr)
            posr += 1
        self.transactionframe.grid(column=5, row=2, rowspan=8)
        self.root.mainloop()

    def numpad(self, car = ''):

        self.subtotal.insert(tk.END, string= f'{car}')

    def update_window(self, price=0, mult=1, reset=False, buy=False, username=""):
        subtotal = 0
        
        if reset:
            self.total_sum = 0
            self.total.delete(0, tk.END)
            self.subtotal.delete(0, tk.END)
            self.total.insert(tk.INSERT, string= f'{self.total_sum}')
            return

        if self.starcount > 1:
            self.total_sum = 0
            self.total.delete(0, tk.END)
            self.subtotal.delete(0, tk.END)
            self.total.insert(tk.INSERT, string= f'{self.total_sum}')
            self.starcount = 0
            return
        try:
            if len(self.subtotal.get()) == 0:
                subtotal = 0
            elif self.subtotal.get()[-1] == '*':
                self.starcount +=1
                subtotal = eval(self.subtotal.get()[:-1])
            else: 
                subtotal = eval(self.subtotal.get())
        except ValueError:
            print('value error', self.subtotal.get())
        if mult == 2:
            if subtotal == 0:
                subtotal = 1
            self.total_sum += price * subtotal
        else:
            self.total_sum += price + subtotal
        if buy:

            try:
                if len(self.total.get()) == 0:
                    self.total_sum = 0
                else: 
                    self.total_sum = int(self.total.get())
            except ValueError:
                print('value error', self.subtotal.get())
            
            self.root.destroy()
            self.backend.transaction(username=username, sum= self.total_sum + subtotal)
            
        self.total.delete(0, tk.END)
        self.subtotal.delete(0, tk.END)
        self.total.insert(tk.INSERT, string= f'{self.total_sum}')

    def user_create(self, nfc):
        user_C = tk.Tk()
        user_C.title("Lag bruker")
        user_C.after(45000, self.on_closing)

        user_C.lift()

        label1 = tk.Label(user_C, text='Det er ingen brukere på dette kortet \n venligst skriv ufs brukernavn under:')
        label1.pack()

        entry1 = tk.Entry(user_C)
        entry1.focus()
        entry1.pack()

        button = tk.Button(user_C, text='Lag Bruker', command=lambda: self.backend.create_user(entry1.get(), nfc))
        button.pack()

        user_C.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        user_C.mainloop()

    def on_closing(self):
        os.system('xset -display :0 dpms force off')
        os.execl(sys.executable, sys.executable, *sys.argv)




#The backend needs to be global :/

backend = BackendHandler()
#The gui must also be global

gui = GUIhandler(backend)

#Waiting for a card scan
user = backend.wait_for_user()


gui.main_window(user)
