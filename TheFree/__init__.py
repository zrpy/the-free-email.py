import requests,time

class Client:
    def __init__(self, token=None, proxy=None):
        self.cookies = {}
        self.csrf_token = None
        self.session = requests.Session()
        self.address = None
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}
        if token:
            res = self.session.get("https://thefree.email/ja",cookies={"email": token})
            if res.status_code != 200:
                raise Exception("Couldn't get html")
            self.cookies = {"free_email_session": res.cookies.get_dict()["free_email_session"],"email": token}
            self.csrf_token = res.text.split('<meta name="csrf-token"')[1].split('"')[1]
            mail_data = self.session.post("https://thefree.email/messages",data={"_token": self.csrf_token, "captcha": ""},cookies=self.cookies)
            if mail_data.status_code != 200:
                raise Exception("Couldn't get email")
            self.address = mail_data.json()["mailbox"]

    def register(self):
        if self.cookies:return self.cookies
        res = self.session.get("https://thefree.email/ja")
        if res.status_code != 200:
            raise Exception("Couldn't get html")
        self.cookies = {"free_email_session": res.cookies.get_dict()["free_email_session"]}
        self.csrf_token = res.text.split('<meta name="csrf-token"')[1].split('"')[1]
        res = self.session.post("https://thefree.email/messages",data={"_token": self.csrf_token, "captcha": ""},cookies=self.cookies)
        if res.status_code != 200:
            raise Exception("Couldn't get email")
        self.cookies["email"] = res.cookies.get_dict()["email"]
        self.address = res.json()["mailbox"]
        return {"email": res.json()["mailbox"],"token": self.cookies["email"]}

    def get_messages(self):
        if not self.cookies:
            raise Exception("cookies isn't set.")
        if not self.csrf_token:
            raise Exception("csrf_token isn't set.")
        res = self.session.post("https://thefree.email/messages",data={"_token": self.csrf_token, "captcha": ""},cookies={"email": self.cookies["email"],"free_email_session": self.cookies["free_email_session"]})
        if res.status_code != 200:
            raise Exception("Couldn't get messages")
        return res.json()["messages"]

    @property
    def token(self):
        return self.cookies.get("email")
