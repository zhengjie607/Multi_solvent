import uuid
import datetime
u=uuid.uuid1()
print(u)
print(u.time)
w=str(u).replace('-','')
print(w)
print(len(w))