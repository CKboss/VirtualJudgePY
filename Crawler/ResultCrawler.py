import requests
import json

class HUSTResualtCrawler :

    baseurl = 'http://acm.hust.edu.cn/vjudge/problem/fetchStatus.action'

    datastring = ''

    D = {
        'draw':'1',
        'columns[0][data]':'0',
        'columns[0][name]':'',
        'columns[0][searchable]':'true',
        'columns[0][orderable]':'false',
        'columns[0][search][value]':'',
        'columns[0][search][regex]':'false',
        'order[0][column]':'0',
        'order[0][dir]':'desc',
        'start':'0',
        'length':'10',
        'search[value]':'',
        'search[regex]':'false',
        'un':'',
        'OJId':'All',
        'probNum':'',
        'res':'0',
        'orderBy':'run_id',
        'language':'',
    }

    def catch(self):
        r = requests.post(self.baseurl,self.D)
        self.datastring = r.text


    def solve(self):
        J = json.loads(self.datastring)
        L = [ x for x in J['data']]
        return L

    def getResult(self):
        self.catch()
        return self.solve()

def main():
    crawler = HUSTResualtCrawler()
    crawler.catch()
    crawler.solve()


if __name__=='__main__':
    main()

