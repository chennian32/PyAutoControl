# PyAutoControl
## How to use it？
``` python
from auto_control import Condition,AutoControl
#External start automatic program
start = Condition()
#AutoControl class
a = AutoControl()
#first step must wait start condition
first = a.delay(start)
#second step delay 20000 cycle time
second = a.delay(20000)
#end step delay 20000 cycle time
end = a.delay(20000)
#define two conditions
light = Condition()
dark = Conditon()
#enter the loop
while True:
    a.loop()
    a.keep(light,second)
    a.keep(dark,end)
    print(light.o())
    print(dark.o())
```
