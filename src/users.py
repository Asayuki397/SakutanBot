from database import *
from datetime import datetime, timedelta, timezone

timezone_offset = +9.0
tzinfo = timezone(timedelta(hours=timezone_offset))

def checkUser(_id,_guild_id):
    if searchDB("db","id",f"id={_id} AND guild_id={_guild_id}") == None:
        return False
    else :
        return True

def getMoney(_id):
    return searchDB("db","money","id={_id}".format(_id=_id))

def addMoney(_id,_amount):
    addDB("db","money",_amount,"id={_id}".format(_id=_id))

def getLvl(_id):
    return searchDB("db","lvl","id={_id}".format(_id=_id))

def getExp(_id):
    return searchDB("db","exp","id={_id}".format(_id=_id))

def getName(_id):
    return searchDB("db","name","id={_id}".format(_id=_id))

def getLoss(_id):
    return searchDB("db","loss","id={_id}".format(_id=_id))

def getRank(_id,_guild_id):
    return selRank(_id, _guild_id)

def getUser(_id):
    return getName(_id),_id,getLvl(_id),getExp(_id),getLoss(_id),getRank(_id)

def modifyLoss(_id,_amount):
    updateDB("db","loss",_amount,"id={_id}".format(_amount=_amount,_id=_id))

def addLoss(_id,_amount):
    addDB("db","loss",_amount,"id={_id}".format(_amount=_amount,_id=_id))

def modifyExp(_id,_amount):
    curExp = getExp(_id)
    lvl = getLvl(_id)
    expToUP = lvl*lvl + 6*lvl - curExp
    levelup = 0
    _amount += curExp
    while _amount >= expToUP:
        levelup += 1
        _amount -= expToUP
        expToUP = (lvl+levelup)*(lvl+levelup) + 6*(lvl+levelup)
        updateDB("db","exp",0,"id={_id}".format(_id=_id))
    addDB("db","lvl",levelup,"id={_id}".format(_id=_id))
    updateDB("db","exp",_amount,"id={_id}".format(_id=_id))

def checkDaily(_id):
    t = datetime.now(tzinfo)
    result = int(t.strftime("%Y%m%d"))
    lastDaily = searchDB("db","dailybonus","id={_id}".format(_id=_id))
    if lastDaily == None:
        return False, result
    else:
        lastDaily = int(lastDaily)
    if result == lastDaily:
        return True, lastDaily
    else:
        return False, result
    

