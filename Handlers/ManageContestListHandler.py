from Handlers.BaseHandler import BaseHandler

class ManageContestListHandler(BaseHandler) :

    def get(self, *args, **kwargs):

        self.get_current_user()

        if len(self.current_user) == 0 :
            self.write('please log in first !!')
            return

        self.render('managecontestlist.html')
