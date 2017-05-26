import requests

DISCOVERY_URI = "https://prod-s0-webapp-proxy.nubank.com.br/api/discovery"

REQUEST_HEADERS = {
  "Content-Type": "application/json",
  "X-Correlation-Id": "WEB-APP.jO4x1",
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  "Origin": "https://conta.nubank.com.br",
  "Referer": "https://conta.nubank.com.br/",
}

class NubankAPI(object):
    _autologin = True
    _linsk = None
    _signin_info = None

    def login(self, login, password, autologin=True):
        payload = {
            "login": login,
            "password": password,
            "grant_type": "password",
            "client_id": "other.conta",
            "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO",
        }

        self._discovery()
        self._signin_info = requests.post(self._links["login"], json=payload, headers=REQUEST_HEADERS).json()
        self._links.update(map(lambda l: (l[0], l[1]["href"]), self._signin_info["_links"].items()))

    def customer(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        customer = requests.get(self._links["customer"], headers=headers)

        return customer.json()

    def revoke_all(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        requests.post(self._links["account"], headers=headers)

    def account(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        account = requests.get(self._links["account"], headers=headers)

        return account.json()

    def purchases(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        purchases = requests.get(self._links["purchases"], headers=headers)

        return purchases.json()

    def user_change_password(self):
        pass #TODO

    def events_page(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        events_page = requests.get(self._links["events_page"], headers=headers)

        return events_page.json()

    def revoke_token(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        requests.post(self._links["revoke_token"], headers=headers)

    def userinfo(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        userinfo = requests.get(self._links["userinfo"], headers=headers)

        return userinfo.json()

    def change_password(self, password):
        payload = {
            "password": password,
        }

        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        response = requests.post(self._links["change_password"], json=payload, headers=headers).json()

    def events(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        events = requests.get(self._links["events"], headers=headers)

        return events.json()

    def bills_summary(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        bills_summary = requests.get(self._links["bills_summary"], headers=headers)

        return bills_summary.json()

    def _discovery(self):
        self._links = requests.get(DISCOVERY_URI, headers=REQUEST_HEADERS).json()
