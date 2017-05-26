import requests

DISCOVERY_URI = "https://prod-s0-webapp-proxy.nubank.com.br/api/discovery"

REQUEST_HEADERS = {
  "Content-Type": "application/json",
  "X-Correlation-Id": "WEB-APP.jO4x1",
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  "Origin": "https://conta.nubank.com.br",
  "Referer": "https://conta.nubank.com.br/",
}

class APIError(RuntimeError):
    pass

def json_response(func):
    def wrapper(self, *args, **kwargs):
        response = func(self, *args, **kwargs)

        try:
            response_data = response.json()

        except ValueError:
            raise APIError("Unexpected response content")

        if response_data.has_key("error"):
            raise APIError("API error: %s" % (response_data["error"], ))

        if not response.ok:
            raise APIError("HTTP error: %s (code %d)" % (response.reason, response.status_code))

        return response_data

    return wrapper

def auth_required(func):
    def wrapper(self, *args, **kwargs):
        if self._signin_info is None:
            raise APIError("You need to authenticate first")

        return func(self, *args, **kwargs)

    return wrapper

class NubankAPI(object):
    _autologin = True
    _linsk = None
    _signin_info = None

    def login(self, login, password):
        self._signin_info = self._login(login, password)
        self._links.update(map(lambda l: (l[0], l[1]["href"]), self._signin_info["_links"].items()))

    @auth_required
    @json_response
    def customer(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        customer = requests.get(self._links["customer"], headers=headers)

        return customer

    @auth_required
    @json_response
    def revoke_all(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        response = requests.post(self._links["account"], headers=headers)

        return response

    @auth_required
    @json_response
    def account(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        account = requests.get(self._links["account"], headers=headers)

        return account

    @auth_required
    @json_response
    def purchases(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        purchases = requests.get(self._links["purchases"], headers=headers)

        return purchases

    @auth_required
    @json_response
    def user_change_password(self):
        pass #TODO

    @auth_required
    @json_response
    def events_page(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        events_page = requests.get(self._links["events_page"], headers=headers)

        return events_page

    @auth_required
    @json_response
    def revoke_token(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        response = requests.post(self._links["revoke_token"], headers=headers)

        return response

    @auth_required
    @json_response
    def userinfo(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        userinfo = requests.get(self._links["userinfo"], headers=headers)

        return userinfo

    @auth_required
    @json_response
    def change_password(self, password):
        payload = {
            "password": password,
        }

        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        response = requests.post(self._links["change_password"], json=payload, headers=headers).json()

        return response

    @auth_required
    @json_response
    def events(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        events = requests.get(self._links["events"], headers=headers)

        return events

    @auth_required
    @json_response
    def bills_summary(self):
        headers = {
            "Authorization": "Bearer %s" % (self._signin_info["access_token"], ),
        }

        headers.update(REQUEST_HEADERS)
        bills_summary = requests.get(self._links["bills_summary"], headers=headers)

        return bills_summary

    @json_response
    def _discovery(self):
        return requests.get(DISCOVERY_URI, headers=REQUEST_HEADERS)

    @json_response
    def _login(self, login, password):
        payload = {
            "login": login,
            "password": password,
            "grant_type": "password",
            "client_id": "other.conta",
            "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO",
        }

        self._links = self._discovery()

        return requests.post(self._links["login"], json=payload, headers=REQUEST_HEADERS)
