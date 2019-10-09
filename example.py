

from sets import *
from rangelimit import RangeLimit
'''
set1 = IntegerSet(-1,2)


r1 = IntegerSet(1,4)
r2 = IterableSet([-1,1,3,4])
r3 = DifferenceSet(r1,r2)

def check_membership(value):
    print("value: {},\tresult: {}".format(value,r3.is_member(value)))

check_membership(-1)
check_membership(0)
check_membership(1)
check_membership(2)
check_membership(3)
check_membership(4)
check_membership(5)
check_membership(6)
'''
class Bob:
    def __init__(self):
        self.val = 1
    def __add__(self, other):
        if isinstance(other, Bob):
            return self.val + other.val
        return self.val + other

bob1 = Bob()
bob2 = Bob()
bob3 = Bob()
print(bob1 + bob2 + 2)

'''
def bob(asd):
    print(asd.bo)
    asd.bo()
gi = 2
def bo():
    print("bo")
gi.bo = bo
bob(gi)
print(type(bob))'''
