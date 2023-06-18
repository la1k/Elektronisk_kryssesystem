import psycopg2
import os
import requests
import json

dbconn = psycopg2.connect(database="kryss",
                        host="localhost",
                        user="krysser",
                        password=os.environ['dbpass'],
                        port="5432")


    
def get_transactions(number = 100, username = None):
    cursor = dbconn.cursor()
    if username == None:
        cursor.execute("""SELECT "ID", "sum", "slug", "time" FROM "public"."transaction_names" ORDER BY "ID" DESC LIMIT %s""", [number])
    else:
        cursor.execute("""SELECT "ID", "sum", "slug", "time" FROM "public"."transaction_names" WHERE "slug" = %s ORDER BY "ID" DESC LIMIT %s""", [username, number])
    transactions = cursor.fetchall()
    
    cursor.close()
    
    return transactions
    
 
def data_in():
    conn = requests.Session()
    
    conn.get(url="https://ufs.samfundet.no/", auth=('mortekho', os.environ['ufspass']))
    
    data = conn.get(url='https://ufs.samfundet.no/ark/api/accounts/', auth=('mortekho', os.environ['ufspass'])).json()
    cursor = dbconn.cursor()
    
    for i in data:
        cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET slug=%s, callsign=%s, ignore_limit=%s, balance=%s", (data[i]["id"], data[i]["slug"], data[i]["short_name"], data[i]["ignore_block_limit"], data[i]["balance"], data[i]["slug"], data[i]["short_name"], data[i]["ignore_block_limit"], data[i]["balance"]))
    dbconn.commit()

    cursor.close()   
    
    return 1

def make_unblocked(username=None):
    
    cursor = dbconn.cursor()
    if username==None:
        cursor.execute(f"""UPDATE "public"."users" SET is_blocked = false WHERE "balance" >= 0""")
    else:
        cursor.execute(f"""UPDATE "public"."users" SET is_blocked = false WHERE "slug" = '{username}'""")
    dbconn.commit()
    cursor.close()
    
def make_blocked():
    cursor = dbconn.cursor()
    for i in find_low_bal():
        if i[1] == True:
            cursor.execute(f"""UPDATE "public"."users" SET is_blocked = false WHERE id = {i[0]}""")
        else:
            cursor.execute(f"""UPDATE "public"."users" SET is_blocked = true WHERE id = {i[0]}""")
    dbconn.commit()
    cursor.close()

def find_low_bal():
    cursor = dbconn.cursor()
    
    cursor.execute("""SELECT "id", "ignore_limit", "balance" FROM "public"."users" WHERE "balance" < 0""")
    low_balance = cursor.fetchall()
    
    cursor.close()
    
    return low_balance
            

def get_user_from_nfc_or_username(nfc=-1, username=""):
    cursor = dbconn.cursor()
    if nfc == -1 and username != "":
        cursor.execute("""SELECT "id","slug","callsign","ignore_limit","balance","usage","nfc", "is_blocked" FROM "public"."users" WHERE "slug" = %s """, [username])
    elif nfc != -1 and username == "":
        cursor.execute("""SELECT "id","slug","callsign","ignore_limit","balance","usage","nfc", "is_blocked" FROM "public"."users" WHERE "nfc" = '%s' """, [int(nfc)])
    else:
        cursor.close() 
        return -3
    ret = cursor.fetchall()
    cursor.close() 
    if len(ret) == 1:
        return ret
    elif len(ret) == 0:
        return -1
    else:
        return -2

def update_usage(nfc, sum):
    cursor = dbconn.cursor()
    preUsage = get_user_from_nfc_or_username(nfc=nfc)[0][5]
    if preUsage == None:
        preUsage = 0
    cursor.execute(f"""UPDATE "public"."users" SET usage = {sum+preUsage} WHERE nfc = '{nfc}'""")
    dbconn.commit()
    cursor.close()
    
    cursor.close()

    
def write_transaction(user, sum):
    if sum == 0:
        return 1
    cursor = dbconn.cursor()
    cursor.execute("""INSERT INTO transactions ("sum", "user") VALUES (%s, %s)""", (sum, user[0][0]))
    dbconn.commit()
    cursor.close()
    return 1

def nfc_reg(username, nfc):
    cursor = dbconn.cursor()
    cursor.execute(f"""UPDATE "public"."users" SET nfc = {nfc} WHERE slug = '{username}'""")
    dbconn.commit()
    cursor.close()
