from sets import *
from rangelimit import RangeLimit

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

