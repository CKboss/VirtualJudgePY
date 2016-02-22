import time
import datetime
import os
import pickle

from Config.FilePathConfig import PendingContestFile,RunningContestFile,EndedContestFile
from tools.dbtools import getUpdateSQL
from tools.dbcore import conn

class ContestScanner():

    PendingContestFile = PendingContestFile
    RunningContestFile = RunningContestFile
    EndedContestFile = EndedContestFile

    def mainloop(self):

        while True :

            self.PendingScanner()
            self.RunningScanner()

            time.sleep(20)

    def PendingScanner(self):

        files = os.listdir(self.PendingContestFile)

        for file in files:

            filepath = self.PendingContestFile+'/'+file

            if file.endswith('.pkl'):

                cdata = self.PklToData(self.PendingContestFile+file)

                begintime = datetime.datetime.strptime(cdata['begintime'],'%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()

                dt = begintime - now

                if dt.total_seconds() < 0 :

                    os.remove(filepath)

                    cdata['cstatus'] = 1
                    file = open(self.RunningContestFile+file,'wb')
                    pickle.dump(cdata,file)

                    # upd database
                    cid = cdata['cid']
                    self.UpdateDatabaseContestStatus(cid,1)

                else :
                    continue



    def RunningScanner(self):

        files = os.listdir(self.RunningContestFile)

        for file in files :

            filepath = self.RunningContestFile+file

            if file.endswith('.pkl') :
                cdata = self.PklToData(self.RunningContestFile+file)

                endtime = datetime.datetime.strptime(cdata['endtime'],'%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()

                dt = endtime - now

                if dt.total_seconds() < 0 :

                    os.remove(filepath)

                    cdata['cstatus'] = 2
                    file = open(self.EndedContestFile+file,'wb')
                    pickle.dump(cdata,file)

                    # upd database
                    cid = cdata['cid']
                    self.UpdateDatabaseContestStatus(cid,2)

                else :
                    continue


    def PklToData(self,file):

        file = open(file,'rb')
        data = pickle.load(file)
        print(data)
        return data

    def UpdateDatabaseContestStatus(self,cid,cstauts):

        data = dict()
        data['cstatus'] = cstauts

        sql = getUpdateSQL('contest',data,' cid = {} '.format(cid))

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()


def main():
    CS = ContestScanner()
    CS.mainloop()

if __name__=='__main__':
    main()
