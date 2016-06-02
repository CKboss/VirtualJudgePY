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

def RelUrlToBase64Code(baseurl,text,checkpicture=True,referer='http://www.baidu.com'):

    '''
    将相对url换成base64编码的格式,从而离线访问图片,但是速度缓慢而且会让html代码变的很长
    :param basurl:
    :param text:
    :return:
    '''

    text = str(text)
    L = re.split(r' ', text)
    ret = ''

    picture_end = ['png','jpg','gif','bmp','svg','pcx']


    lastword = None

    for l in L:

        isimg = None
        if lastword is not None :
            isimg = re.match(r'.*<img.*',lastword)

        if len(l) > 5 and l[:5] == 'src="' and lastword is not None and isimg is not None:

            m = re.match(r'src="(.*)"',l)
            parturl=baseurl+'/'+m.group(1)

            if m.group(1)[0:7]=='http://' or m.group(1)[0:8]=='https://' :
                parturl = m.group(1)
            url = m.group(1)

            ispicture = False

            for end in picture_end :
                if url.endswith(end) :
                    ispicture = True
                    break

            if checkpicture==False:
                ispicture=True

            if ispicture == True :
                basedata = PictureToBase64(Url=parturl,referer=referer)
                if basedata is not None :
                    l = l[:m.start(1)]+basedata+l[m.end(1):]
            elif ispicture == False :
                if url[0] == '/':
                    l = l[:m.start(1)]+baseurl+'/'+url+l[m.end(1):]

        lastword=str(l).lower()
        ret = ret + ' ' + l

    return ret


if __name__=='__main__':

    lastword = '<img'
    isimg = re.match(r'.*<img.*',lastword)
    print(isimg)

    '''
    f = open('/tmp/t.html','r')
    baseurl = 'http://www.lydsy.com/JudgeOnline/'
    #baseurl = 'http://acm.hdu.edu.cn/'
    ret = RelUrlToBase64Code(baseurl,f.read())
    fout = open('/tmp/t2.html','w')
    fout.write(ret)
    fout.close()
    '''
