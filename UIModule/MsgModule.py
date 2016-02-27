import tornado.web


def renderMSG(msg, waittime=1000):
    function = '''
        <script type = "text/javascript">
            function myfunction() {
                location.href = document.referrer;
            }
            setTimeout(myfunction,''' + str(waittime) + ''');</script>'''
    html = '''
        <div class="flash flash-with-icon"><span class="octicon octicon-alert"></span>
          <h2>''' + str(msg) + '''</h2></div>'''

    return html + function
