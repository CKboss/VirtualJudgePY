
'''
import .plk data to DB
'''

import os
import pickle

from dao.problemdao import InsertOrUpdateProblem

from Config.FilePathConfig import ZOJ_PKL_FILE

def ImportProblem(dir) :
    files = os.listdir(dir)
    for f in files :
        if f.endswith(".pkl") :
            path = dir+f
            print('Import problem : ',path)
            try :
                problemdata = pickle.load(open(path,'rb'))
                InsertOrUpdateProblem(problemdata)
            except EOFError:
                print('EOFError ... ')
            except :
                print('other error')

if __name__=='__main__' :
    ImportProblem(ZOJ_PKL_FILE)
