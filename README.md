# nubankapi
Python non-official Nubank API implementation

This project aims to provide a minimal API to access the Nubank services through a transparent and intuitive set of methods. This project was done on my free time, and DOES NOT have any official support from Nubank nor is endorsed by them. This code is provided as is, I can't give you any guarantee that Nubank won't change the API calls in the future or you block your access accidentaly by overloading their API.

Also I do not take any responsability for bad usages of this code for phishing or malware implementation.

I tested almost all functionality myself, I will provide some documentation in the future as time allows. If you are from Nubank and wanna provide any support, I'll be glad to but a big THANK YOU here :)

### Usage

For now, just clone/download this repository and put the whole thing in some place that Python would recognize (or adjust your PYTHONPATH). The code currently is minimal, so it should be easy to understand, but here are some examples:

```python
from nubankapi import NubankAPI

nuba = NubankAPI()
nuba.login("<your-cpf>", "<your-password>") # you should call this before any other method!
print nuba.bills_summary()
```

The code above will bring your last statements in a dictionary. You can examine the output of the methods and grab whatever information you need from it.

That's all, feel free to open an issue if you need!
