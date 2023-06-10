import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(
    DATABASE_URL,
    sslmode='require',
    sslrootcert='BaltimoreCyberTrustRoot.crt.pem'
)

cur = conn.cursor()
conn.autocommit = True
conn.commit()

cur.execute("CREATE TABLE IF NOT EXISTS db (name VARCHAR(255),id BIGINT, guild_id BIGINT, lvl INT DEFAULT 1, exp INT DEFAULT 0, money BIGINT DEFAULT 50000, loss BIGINT DEFAULT 0, dailybonus INT DEFAULT 0)")
cur.execute("CREATE TABLE IF NOT EXISTS stocks (name VARCHAR(255), id BIGINT, guild_id BIGINT, AKKN BIGINT DEFAULT 0, AKKNavg BIGINT DEFAULT 0, SHRN BIGINT DEFAULT 0, SHRNavg BIGINT DEFAULT 0, STND BIGINT DEFAULT 0, STNDavg BIGINT DEFAULT 0, UMSI BIGINT DEFAULT 0, UMSIavg BIGINT DEFAULT 0)")
cur.execute("CREATE TABLE IF NOT EXISTS guilds (name VARCHAR(255), id BIGINT, on_member_join BOOLEAN DEFAULT TRUE, on_guild_join BOOLEAN DEFAULT TRUE, on_member_remove BOOLEAN DEFAULT TRUE)")

def delbr(value):
    tup = value[0]
    string = tup[0]
    return string

def insertDB(table,column,data : tuple):
    sql = f" INSERT INTO {table}({column}) VALUES %s ;"
    try:
        cur.execute(sql, (data,))
        conn.commit()
    except Exception as e :
        print(" insert DB  ",e)

def updateDB(table,column,value,condition):
    sql = f" UPDATE {table} SET {column}=%s WHERE {condition} ;"
    try :
        cur.execute(sql, (value,))
        conn.commit()
    except Exception as e :
        print(" update DB err",e)

def addDB(table,column,value,condition):
    sql = f" UPDATE {table} SET {column}={column}+%s WHERE {condition} ; "
    try :
        cur.execute(sql, (value,))
        conn.commit()
    except Exception as e :
        print(" update DB err",e)

def readDB(table,column):
    sql = f" SELECT {column} from {table}"
    try:
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return None
        else:
            return delbr(result)
    except Exception as e :
        result = (" read DB err",e)

    return result

def deleteDB(table,condition):
    sql = f" delete from {table} where {condition} ; "
    try :
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print( "delete DB err", e)

def searchDB(table,selectcolumn,condition):
    sql = f" SELECT {selectcolumn} FROM {table} WHERE {condition}"
    try :
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            return None
        else:
            return delbr(result)
    except Exception as e:
        print("searchDB err",e)
        return False

def signup(_name,_id,_guild_id):
    sql = f" INSERT INTO db (name,id,guild_id) VALUES (%s,%s,%s) ;"
    sql2 = f" INSERT INTO stocks (name,id,guild_id) VALUES (%s,%s,%s)"
    try:
        cur.execute(sql, (_name,_id,_guild_id))
        cur.execute(sql2, (_name,_id,_guild_id))
        conn.commit()
    except Exception as e :
        print(" insert DB  ",e)

def DeleteAccount(_id):
    deleteDB("db",f"id={_id}")
    deleteDB("stocks",f"id={_id}")

def selRank(_id,_guild_id):
    sql = f" SELECT rank FROM (SELECT RANK() OVER(ORDER BY lvl DESC) AS rank,* FROM db) AS db WHERE id = %s AND guild_id = %s;"
    try:
        cur.execute(sql, (_id,_guild_id))
        return delbr(cur.fetchall())
    except Exception as e :
        print("rank  ",e)

def fetchAllRanks(_guild_id):
    sql = f" SELECT name,lvl,rank FROM (SELECT RANK() OVER(ORDER BY lvl DESC) AS rank,* FROM db WHERE guild_id = %s) AS db ;"
    try:
        cur.execute(sql, (_guild_id,))
        return cur.fetchall()
    except Exception as e :
        print("fetchAllRanks  ",e)

'''
def insertDB(table,column,data):
    sql = f" INSERT INTO {table}({column}) VALUES ({data}) ;"
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e :
        print(" insert DB  ",e)
        
def updateDB(table,column,value,condition):
    sql = f" UPDATE {table} SET {column}={value} WHERE {condition} ;"
    try :
        cur.execute(sql)
        conn.commit()
    except Exception as e :
        print(" update DB err",e)

def addDB(table,column,value,condition):
    sql = f" UPDATE {table} SET {column}={column}+{value} WHERE {condition} ; "
    try :
        cur.execute(sql)
        conn.commit()
    except Exception as e :
        print(" update DB err",e)

def readDB(table,column):
    sql = f" SELECT {column} from {table}"
    try:
        cur.execute(sql)
        result = cur.fetchall
        if result == None or False or []:
            return None
        else:
            return delbr(result)
    except Exception as e :
        result = (" read DB err",e)
    
    return result

def deleteDB(table,condition):
    sql = f" delete from {table} where {condition} ; "
    try :
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print( "delete DB err", e)

def searchDB(table,selectcolumn,condition):
    sql = f" SELECT {selectcolumn} FROM {table} WHERE {condition}"
    try :
        cur.execute(sql)
        result = cur.fetchall()
        if result == []:
            return None
        else:
            return delbr(result)
    except Exception as e:
        print("searchDB err",e)
        return False


def signup(_name,_id):
    sql = f" INSERT INTO db VALUES ('{_name}',{_id},1,1,10000,0) ;"
    sql2 = f" INSERT INTO stocks (name,id) VALUES ('{_name}',{_id})"
    try:
        cur.execute(sql)
        cur.execute(sql2)
        conn.commit()
    except Exception as e :
        print(" insert DB  ",e)

def DeleteAccount(_id):
    deleteDB("db","id={_id}".format(_id=_id))
    deleteDB("stocks","id={_id}".format(_id=_id))

def selRank(_id):
    sql = f" SELECT rank FROM (SELECT RANK() OVER(ORDER BY lvl DESC) AS rank,* FROM db) AS db WHERE id = {_id};"
    try:
        cur.execute(sql)
        return delbr(cur.fetchall())
    except Exception as e :
        print("rank  ",e)

def fetchAllRanks():
    sql = " SELECT name,lvl,rank FROM (SELECT RANK() OVER(ORDER BY lvl DESC) AS rank,* FROM db) AS db ;"
    try:
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e :
        print("fetchAllRanks  ",e)

'''
