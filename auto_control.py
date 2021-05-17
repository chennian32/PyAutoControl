class Condition:
    def __init__(self):
        self.state = False
        self.last_state = False
    def o(self):
        return self.state 
    def raising(self):
        return self.state and not self.last_state   
    def falling(self):
        return not self.state and self.last_state
    def out(self,condition):
        self.state = condition
    def keep(self,set,reset):
        if reset:
            self.state = False
        elif set:
            self.state = True
    def reset(self):
        self.state = False
        self.last_state = False
    def loop(self):
        self.last_state = self.state
class Timer(Condition):
    def __init__(self,time_scan = 100):
        super().__init__()
        self.time_scan = time_scan
        self.cur_time = time_scan
    def t(self):
        return self.cur_time
    def run(self,condition):
        value=False
        if condition :
            if self.last_state == 0:
                self.cur_time = self.time_scan
            self.cur_time -= 1
            if self.cur_time <= 0:
                value = True
                self.cur_time = 0
        else:
            self.cur_time = self.time_scan
        self.state = 1 if value else 0
        self.last_state = 1 if condition else 0
class Counter(Condition):
    def __init__(self,count = 100):
        super().__init__()
        self.count = count
        self.cur_index = count
    def t(self):
        return self.cur_index
    def run(self,condition):
        value=False
        if condition :
            if self.last_state == 0:
                self.cur_index = 0
            self.cur_index += 1
            if self.cur_index >= self.count:
                value = True
                self.cur_index = self.count
        else:
            self.cur_time = 0
        self.state = 1 if value else 0
        self.last_state = 1 if condition else 0
class AutoControl:
    def __init__(self,count = -1):
        self.conditions = []
        self.timers = []
        self.cur_index = 0
        self.monitor = 0
        self.count = count
    def is_index(self,idx):
        return self.cur_index == idx
    def get_bool(self,o):
        return o.o() if isinstance(o,Condition) else o
    def shift(self,conditions,timers,reset = False):
        if len(conditions) < self.count:
            raise Exception ("conditions length must greator or equal to count")
        if len(conditions) != len(timers):
            raise Exception ("conditions length must equal to timers length")
        if self.count == -1:
            self.count = len(conditions)
        if reset:
            self.cur_index = 0
            return
        if self.cur_index == self.count:
            self.cur_index = 0
        i = self.cur_index
        b = self.is_index(i)
        c = self.get_bool(conditions[i])
        bitCond = b and c
        isTimer = isinstance(timers[i] , Timer)
        timeOut = False
        if isTimer:
            timers[i].run(bitCond)
            timeOut = timers[i].o()
        else:
            timeOut = timers[i]; 
        cond = bitCond and timeOut
        if cond:
            self.cur_index+=1
            if isTimer:
                timers[i].run(False)
    def step_(self,condition = True,timer = True):
        if self.conditions == None or self.timers == None:
            self.conditions = []
            self.timers = []
        s = len(self.conditions)
        self.conditions.append(condition)
        self.timers.append(timer)
        return s
    def step(self,condition = True,time = 0):
        if time == 0:
            return self.step_(condition);
        t = Timer(time);
        return self.step_(condition,t);
    def time(self,idx):
        if idx < len(self.timers) and idx >= 0:
            t = self.timers[idx]
            isTimer = isinstance(t,Timer)
            if isTimer:
                return t
        return None
    def delay(self,time = 0):
        return self.step(True,time)
    def loop(self,reset=False):
        self.shift(self.conditions,self.timers,reset)
    def debug(self,b,idx):
        if b:
            self.monitor = self.monitor | 1 << idx
        else:
            self.monitor = self.monitor & ~(1 << idx) 
    def keep(self,condition,start,end = -1,reset = False):
        if reset or not isinstance(condition,Condition):
            return False
        if end == -1:
            end = start + 1
        if self.is_index(end):
            condition.out(False)
        elif self.is_index(start):
            condition.out(True)
        return condition.o()
    def keep_multi(self,condition,start,end = [],reset = False):
        if reset or not isinstance(condition,Condition):
            return False
        start_m = False
        end_m = False
        add = len(end) == 0
        for s in start:
            start_m = start_m or self.is_index(s)
            if add:
                end.append(s + 1)
        for e in end:
            end_m = end_m or self.is_index(e)
        if end_m:
            condition.out(False)
        elif start_m:
            condition.out(True)
        return condition.o()        
    def reset(self):
        self.cur_index = 0
        self.monitor = 0
    def monitor_index(self):
        return self.cur_index   
if  __name__ == "__main__":
    a = AutoControl()
    a.delay(2000)
    a.delay(20000)
    a.delay(2000)
    c0 = Condition()
    while True:
        a.loop()
        a.keep(c0,1)
        print(a.monitor_index())