
def getInserSQL(table,data) :
    part1 = ''
    part2 = ''

    for key in data :

        if data[key] is None :
            continue

        if len(part1)!=0 :
            part1+=','
            part2+=','
        part1+=key
        if isinstance(data[key],str) :
            part2+='"'+data[key]+'"'
        else :
            part2+=str(data[key])

    sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table,part1,part2)

    return sql

def getUpdateSQL(table,data,clause) :

    part1 = ''

    for key in data :

        if data[key] is None :
            continue

        if len(part1)!=0 :
            part1+=' , '

        if(isinstance(data[key],str)) :
            part1 = part1 + key + ' = "' + str(data[key]) + '"'
        else :
            part1 = part1 +  key + ' = ' + str(data[key])

    sql = 'UPDATE {} SET {} WHERE ( {} )'.format(table,part1,clause)

    return sql

def getPageLimitSQL(tablename,whereclause,ordclause,n,m) :

    sql = 'SELECT * FROM {} WHERE ( {} ) ORDER BY {} LIMIT {} , {}'\
        .format(tablename,whereclause,ordclause,n,m)
    return sql

def LAST_INSERT_ID():
    return 'SELECT LAST_INSERT_ID()'

if __name__=='__main__' :
    data = dict(
        arg1='a1',
        arg2='a2',
        arg4=911,
        arg3='a3',
    )
    sql = getPageLimitSQL('table2','1 is none',"id=87",10,30)
    print(sql)
