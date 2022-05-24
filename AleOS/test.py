from datetime import datetime, timedelta

time1 = '2022-05-22 21:37:11'
time2 = '2022-05-22 21:38:35'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
class MyDate(object):
    def __init__(self, date):
        self.date, self.time = date.split()[0], date.split()[1]
        self.Y, self.M, self.D = int(self.date.split('-')[0]), int(self.date.split('-')[1]), int(self.date.split('-')[2])
        self.h, self.m, self.s = int(self.time.split(':')[0]), int(self.time.split(':')[1]), int(self.time.split(':')[2])

    def __gt__(self, other):
        if self.Y > other.Y:
            return False
        else:
            if self.M > other.M:
                return False
            else:
                if self.D > other.D:
                    return False
                else:
                    if self.h > other.h:
                        return False
                    else:
                        if self.m > other.m:
                            return False
                        else:
                            if self.s > other.s:
                                return False
                            else: return True

MyDate1 = MyDate(time1)

print(MyDate1 > MyDate(time2))
print(MyDate1.M)
print(MyDate1.D)
print(MyDate1.h)
print(MyDate1.m)
print(MyDate1.s)
