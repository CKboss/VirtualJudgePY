import re

def RelUrlToAbsUrl(baseurl,text):
    '''
    将/开头的相对url换成绝对url
    :param baseurl:
    :param text:
    :return:
    '''

    text = str(text)

    L = re.split(r' ',text)

    ret = ''

    for l in L :

        if len(l) > 5 and l[:5] == 'src="':
            l = l[:5] + baseurl + '/' + l[5:]

        ret = ret + ' '+l

    return ret
