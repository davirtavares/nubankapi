# nubankapi
Nubank non-official API implementation in Python

This project aims to provide a minimal API to access the Nubank services through a transparent and intuitive set of methods. This project was done on my free time, and DOES NOT have any official support from Nubank nor is endorsed by them. This code is provided as is, I can't give you any guarantee that Nubank won't change the API calls in the future or you block your access accidentaly by overloading their API.

All those methods were hacked from the webapp, after some hours debugging and monitoring a lot of javascript I found how their authentication system works. It begins by calling a webservice called "discovery", which provides the initial API calls (like "login"). After this initial step, login should be called, which returns the list of valid API calls. Not sure why they did that way tho, maybe to balance the calls between their clusters. After finding that out, the remaining part was easy, just implemented some decorators (that cake care of validation and decoding the response data) and implementing each of the API methods.

Some of the API methods seemed too specific to their webapp, so I left those out of my implementation, but don't worry, they normally only have meaning for the webapp.

I tested almost all functionality myself, I will provide some documentation in the future as time allows. If you are from Nubank and wanna provide any support, I'll be glad to but a big THANK YOU here :)

### Installation and Usage

The only requirement is that you should install Python requests (http://python-requests.org), and Python, of course.

For now, just clone/download this repository and put the whole thing in some place that Python would recognize (or adjust your PYTHONPATH). The code currently is minimal, so it should be easy to understand, but here are some examples:

```python
from nubankapi import NubankAPI

nuba = NubankAPI()
nuba.login("<your-cpf>", "<your-password>") # you should call this before any other method!
print nuba.bills_summary()
```

The code above will bring your last statements in a dictionary. You can examine the output of the methods and grab whatever information you need from it.

That's all, feel free to open an issue if you need!
