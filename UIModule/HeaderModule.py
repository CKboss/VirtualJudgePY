import tornado.web

class TitleModule(tornado.web.UIModule) :

    def render(self):

        html1 = '''
        <div id="title" class="span">
            <a href="/" class="filter-item selected text-center">
                <h1>The VirtualJudgePY</h1>
            </a>
        </div>

        <table class="flex-table">
            <tr>
                <td>
                    <a href="/problemlist">
                        <button class="btn btn-outline" type="button">Problem</button>
                    </a>
                </td>
                <td>
                    <a href="/status">
                        <button class="btn btn-outline" type="button">Status</button>
                    </a>
                </td>
                <td>
                    <a href="/contestlist">
                        <button class="btn btn-outline" type="button">Contest</button>
                    </a>
                </td>
            </tr>
        </table>
        '''

        return html1
