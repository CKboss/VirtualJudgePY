
def getInserSQL(table,data) :
    part1 = ''
    part2 = ''

    for key in data :
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

if __name__=='__main__' :
    pass
    '''
    data = dict(
        arg1='a1',
        arg2='a2',
        arg4=911,
        arg3='a3',
    )
    sql = getInserSQL('table2',data)
    print(sql)
    '''
