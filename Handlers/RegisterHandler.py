import tornado.web

class RegisterHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):

        username = self.get_argument("username",None)
        password = self.get_argument("password",None)
        repassword = self.get_argument("repassword",None)
        email = self.get_argument("email",None)

        print(username,password,repassword,email)


        if password!=repassword :
            self.render('register.html')
        else :

            pass

    def get(self):
        self.render('register.html')
