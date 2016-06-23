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


def RelUrlToBase64Code(baseurl, text, checkpicture=True, referer='http://www.baidu.com'):
    '''
    将相对url换成base64编码的格式,从而离线访问图片,但是速度缓慢而且会让html代码变的很长
    :param basurl:
    :param text:
    :return:
    '''

    text = str(text)
    L = re.split(r' |\n', text)
    ret = ''

    picture_end = ['png', 'jpg', 'gif', 'bmp', 'svg', 'pcx']

    isimg = 0
    for l in L:

        #距离<img 5个以内就下载图片
        if l is not None:
            ok = re.match(r'.*<img.*', l)
            if ok is not None:
                isimg = 10
            else: isimg -= 1

        if len(l) > 5 and l[:5] == 'src="' and isimg >= 0:


            m = re.match(r'src="(.*)"', l)
            #parturl = baseurl + '/' + m.group(1)
            parturl = GetRealUrl(baseurl,m.group(1))

            print('down load img: ',parturl)

            if m.group(1)[0:7] == 'http://' or m.group(1)[0:8] == 'https://':
                parturl = m.group(1)
            url = m.group(1)

            ispicture = False

            for end in picture_end:
                if url.endswith(end):
                    ispicture = True
                    break

            if checkpicture == False:
                ispicture = True

            if ispicture == True:
                basedata = PictureToBase64(Url=parturl, referer=referer)
                if basedata is not None:
                    l = l[:m.start(1)] + basedata + l[m.end(1):]
            elif ispicture == False:
                if url[0] == '/':
                    l = l[:m.start(1)] + GetRealUrl(baseurl , url) + l[m.end(1):]

        lastword = str(l).lower()
        ret = ret + ' ' + l

    return ret

def test1():
    text = '''/></div>
<p>　　N轮状病毒的产生规律是在一个N轮状基中删去若干条边，使得各原子之间有唯一的信息通道，例如共有16个不<br
False -63
/>
同的3轮状病毒，如下图所示</p>
<div><img'''
    text='''<div><img'''
    ok = re.match(r'.*<img.*',text)
    print(ok)


def main():
    '''
    lastword = '<img'
    isimg = re.match(r'.*<img.*',lastword)
    print(isimg)
    '''

    f = open('/tmp/t1.html', 'r')
    baseurl = 'http://www.lydsy.com/JudgeOnline'
    # baseurl = 'http://acm.hdu.edu.cn/'
    ret = RelUrlToBase64Code(baseurl, f.read())
    fout = open('/tmp/t2.html', 'w')
    fout.write(ret)
    fout.close()


def GetRealUrl(nowurl,pattern):
    #直接是绝对路径
    if len(pattern)>=8 and (pattern[0:7] == 'http://' or pattern[0:8] == 'https://'):
        return pattern
    #处理nowurl,获得nowurl所在的目录
    urls = str(nowurl).split('/')
    if nowurl[-1] != '/': urls[-1] = ''
    #位于根目录下
    if pattern[0] == '/':
        urls = urls[0:3]
        url = '/'.join(urls)+pattern
    #直接放在原url的目录下面
    else :
        url = '/'.join(urls)+pattern
    #处理./和../
    temp = [ x for x in str(url).split('/') if x != '.']

    urls = list()
    for x in temp :
        if x == '..': urls = urls[:-1]
        else : urls.append(x)
    url = '/'.join(urls)
    return url

def test2():
    baseurl = 'http://www.lydsy.com/JudgeOnline/problem.php?id=1668'
    url = GetRealUrl(baseurl,'htt:///./././oj/img/1.png')
    print(url)

if __name__ == '__main__':
    test2()
