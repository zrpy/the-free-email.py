# the-free-email.py
Email Generator
thefree.email wrapper in python
```py
import TheFree
c=TheFree.Client(token="token",proxy="https://localhost:8080") # Even without token, it will work if you use c.register()
if not c.token:
    print(c.register()) # generate email
email=c.address # get email
print(email)
print(c.get_messages()) # List of received messages
```
