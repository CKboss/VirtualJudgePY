
def argCheck(arg,kind='string'):

    if kind=='number' :

        if isinstance(arg,int) or isinstance(arg,float) :
            return True
        else :
            return False

    elif kind=='string' :
        if isinstance(arg,str) :
            return arg.isalnum()
        else :
            return False
    else :
        return False
