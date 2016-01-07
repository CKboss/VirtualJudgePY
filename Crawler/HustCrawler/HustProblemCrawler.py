import requests
import json

from dao.problemdao import InsertProblem

class HUSTProblemCralwer:

    prob_url = 'http://acm.hust.edu.cn/vjudge/dwr/fetchDescriptions.action'
    pid_url = 'http://acm.hust.edu.cn/vjudge/problem/listProblem.action'

    d_id = {
        'draw':'5',
        'columns[0][data]':'0',
        'columns[0][name]':'',
        'columns[0][searchable]':'false',
        'columns[0][orderable]':'false',
        'columns[0][search][value]':'',
        'columns[0][search][regex]':'false',
        'order[0][column]':'3',
        'order[0][dir]':'desc',
        'start':'0',
        'length':'20',
        'search[value]':'',
        'search[regex]':'false',
        'OJId':'HDU',
        'probNum':'3006',
        'title':'',
        'source':'',
    }


    d_prob = dict(
        pid=16373,
    )

    def getP(self):
        r = requests.post(self.prob_url,self.d_prob)
        return r.text

    def getPid(self):
        r = requests.post(self.pid_url,self.d_id)
        return r.text

    def InsertIntoDB(self,voj,vid):

        self.d_id['OJId']=voj
        self.d_id['probNum']=vid
        J1 = json.loads(self.getPid())

        print(J1)
        print('-'*60)

        pid = J1['data'][0][5]
        self.d_prob['pid']=pid
        J2 = json.loads(self.getP())

        #print(J2)
        pdata = dict()
        pdata['description']=J2[0]['description']
        pdata['input']=J2[0]['input']
        pdata['output']=J2[0]['output']
        pdata['sampleInput']=J2[0]['sampleInput']
        pdata['sampleOutput']=J2[0]['sampleOutput']
        pdata['author']=J2[0]['author']
        pdata['hint']=J2[0]['hint']
        pdata['source']=J1['data'][0][4]
        pdata['title']=J1['data'][0][2]
        pdata['voj']=voj
        pdata['vid']=vid

        #print(pdata)
        sql = InsertProblem(**pdata)
        #f = open('/tmp/test.sql','w')
        #f.write(sql)



def main():
    hpc = HUSTProblemCralwer()
    hpc.InsertIntoDB('hdu','5101')

if __name__=='__main__':
    main()
