#! /usr/bin/python
# coding: utf-8
import sys
import os
import cgi
import base64
import urllib

fs = cgi.FieldStorage()

LOGO_PATH = './logo.png'

tmpl = """<!DOCTYPE html>
<head>
    <meta charset="utf-8"/>
    <title>html5-ize twitter icon</title>
</head>
<body>
    <h1>HTML5-ize</h1>
    <p>
        公開ユーザのユーザ名を入力するとアイコンをHTML5ロゴっぽくするよ！
    </p>
    <form method="get" action="%s">
        <p>ユーザ: <input type="text" name="screen_name" value="%s"/></p>
        <p><input type="submit" value="生成"/></p>
    </form>
    <div>
        %s
    </div>
    <br/>
    <div>
        <p><a href="http://www.w3.org/html/logo/">http://www.w3.org/html/logo/</a></p>
        <p><a href="http://twitter.com/brainfs">brainfs</a></p>
    </div>
</body>
</html>
"""
tag = ''

screen_name = fs.getvalue('screen_name', '').strip()

if screen_name != '':
    # fetch user iamge via api    
    # see: http://tweetimag.es/
    url = 'http://img.tweetimag.es/i/%s_b' % screen_name
    pid = str(os.getpid())
    try:
        ico = urllib.urlopen(url).read()
        fout = open(pid, 'wb')
        fout.write(ico)
        fout.close()
        # process image
        os.system('convert %s %s.png' % (pid, pid)) # transparentize
        os.system('mv %s.png %s' % (pid, pid))
        os.system('convert %s -matte -virtual-pixel transparent -distort Perspective "0,0 18,19 0,73 21,53 73,0 54,19 73,73 51,53" %s' % (pid, pid))
        os.system('convert %s %s -composite %s' % (LOGO_PATH, pid, pid))
        #os.system('convert -resize 73x73! %s %s' % (pid, pid))

        # encode icon image as base64
        enc = open(pid, 'rb').read().encode('base64')
        
        tag = '<img src="data:image/png;base64,%s"/>' % ico.encode('base64')
        tag += ' → '
        tag += '<img src="data:image/png;base64,%s"/>' % enc
    except Exception, e:
        sys.stderr.write(str(e))
    finally:
        if os.path.exists(pid):
            os.remove(pid)
        

print 'Content-Type: text/html; charset=utf-8'
print ''
print tmpl % (os.environ['SCRIPT_NAME'], screen_name, tag)

