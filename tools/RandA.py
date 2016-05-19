import re
from tools.PictureToBase64 import PictureToBase64


def RelUrlToAbsUrl(baseurl, text):
    '''
    将/开头的相对url换成绝对url
    :param baseurl:
    :param text:
    :return:
    '''

    text = str(text)

    L = re.split(r' ', text)

    ret = ''

    for l in L:

        if len(l) > 5 and l[:5] == 'src="':
            if l[5:10] == '../..':
                l = l[:5] + l[10:]
            l = l[:5] + baseurl + '/' + l[5:]
        ret = ret + ' ' + l

    return ret

def RelUrlToBase64Code(baseurl,text):

    '''
    将相对url换成base64编码的格式,从而离线访问图片,但是速度缓慢而且会让html代码变的很长
    :param basurl:
    :param text:
    :return:
    '''

    text = str(text)
    L = re.split(r' ', text)
    ret = ''

    for l in L:

        if len(l) > 5 and l[:5] == 'src="':
            m = re.match(r'src="(.*)"',l)
            parturl=baseurl+'/'+m.group(1)
            basedata = PictureToBase64(Url=parturl)
            if basedata is not None :
                l = l[:m.start(1)]+basedata+l[m.end(1):]

        ret = ret + ' ' + l

    return ret


if __name__=='__main__':
    f = open('/tmp/t1.html','r')
    baseurl = 'http://www.lydsy.com/JudgeOnline/'
    ret = RelUrlToBase64Code(baseurl,f.read())
    fout = open('/tmp/t2.html','w')
    fout.write(ret)
    fout.close()
