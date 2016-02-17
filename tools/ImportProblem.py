
'''
import .plk data to DB
'''

import os
import pickle

from dao.problemdao import InsertOrUpdateProblem

def ImportProblem(dir) :
    files = os.listdir(dir)
    for f in files :
        if f.endswith(".pkl") :
            path = dir+os.sep+f
            print('Import problem : ',path)
            try :
                problemdata = pickle.load(open(path,'rb'))
                InsertOrUpdateProblem(problemdata)
            except EOFError:
                print('EOFError ... ')
            except :
                print('other error')

if __name__=='__main__' :
    ImportProblem('/home/ckboss/Desktop/Development/testData/POJ')
