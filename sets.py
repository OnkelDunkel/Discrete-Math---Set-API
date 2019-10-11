from abc import ABC, abstractmethod

def is_int_or_float(item):
    return isinstance(item, float) or isinstance(item, int)

class RangeEdge:
    def __init__(self, val=None, allow_equal=True, is_lower=False):
        self.val = val
        self.allow_equal = allow_equal
        self.is_lower = is_lower
    
    def __repr__(self):
        return "RangeEdge(val={},allow_equal={},is_lower={})".format(
            repr(self.val),
            repr(self.allow_equal),
            repr(self.is_lower)
            )

    def __str__(self):
        if self.is_lower:
            if self.allow_equal:
                return "[{}".format(self.val)
            else:
                return "{}[".format(self.val)
        else:
            if self.allow_equal:
                return "{}]".format(self.val)
            else:
                return "]{}".format(self.val)
    
    def evaluate(self, item):
        if is_int_or_float(item):
            if self.val == None:
                return True
            if self.allow_equal and item == self.val:
                return True
            if self.is_lower:
                return self.val < item
            else:
                return self.val > item
        else:
            return False
    
    def __lt__(self,other): # self < other
        if self.val == None: # None is superior
            return False # None can never be smaller than other.val
        elif is_int_or_float(other):
            '''
            ]2 < 1: F   |   2] < 1: F   |   [2 < 1: F   |   2[ < 1: F
          **]2 < 2: T** |   2] < 2: F   |   [2 < 2: F   |   2[ < 2: F
            ]2 < 3: T   |   2] < 3: T   |   [2 < 3: T   |   2[ < 3: T
            '''
            if self.val == other and not self.allow_equal and not self.is_lower:
                return True # see above under ** **
            return self.val < other
        elif not isinstance(other, RangeEdge):
            return False # Not a comparable type
        elif other.val == None:
            return True # None is superior and self.val is not None
        elif self.val == other.val:
            if self.is_lower:
                '''
                [2 < ]2: F   |   [2 < 2]: F   |   [2 < [2: F   |   [2 < 2[: T
                2[ < ]2: F   |   2[ < 2]: F   |   2[ < [2: F   |   2[ < 2[: F
                '''
                if (self.allow_equal and other.is_lower and not other.allow_equal):
                    return True
                return False
            else:
                '''
                ]2 < [2: T   |   ]2 < 2[: T   |   2] < [2: F   |   2] < 2[: T
                -------------------------------------------------------------
                ]2 < ]2: F   |   ]2 < 2]: T   |   2] < ]2: F   |   2] < 2]: F
                '''
                if other.is_lower:
                    if self.allow_equal and other.allow_equal:
                        return False
                    return True
                else:
                    if not self.allow_equal and other.allow_equal:
                        return True
                    return False
        '''
        ]2 < ]1: F   |   ]2 < 1]: F   |   2] < [1: F   |   2] < 1[: F
        [2 < ]1: F   |   [2 < 1]: F   |   2[ < [1: F   |   2[ < 1[: F
        ]2 < ]3: T   |   ]2 < 3]: T   |   2] < [3: T   |   2] < 3[: T
        [2 < ]3: T   |   [2 < 3]: T   |   2[ < [3: T   |   2[ < 3[: T
        '''
        return self.val < other.val
        
    def __le__(self, other): # self <= other
        return self < other or self == other

    def __eq__(self, other): # self == other
        if is_int_or_float(other):
            if not self.allow_equal:
                return False
            return self.val == other
        if not isinstance(other, RangeEdge):
            return False
        return (self.val == other.val and 
            self.allow_equal == other.allow_equal)

    def __ne__(self, other): # self != other
        return not self == other

    def __ge__(self, other): # self >= other
        return not self < other

    def __gt__(self, other): # self > other
        return not self <= other

class Range:
    def __init__(self, low_edge, up_edge, is_int_range=False):
        if is_int_or_float(low_edge) or low_edge == None:
            low_edge = RangeEdge(val=low_edge)
        if is_int_or_float(up_edge) or up_edge == None:
            up_edge = RangeEdge(val=up_edge)
        low_edge.is_lower = True
        up_edge.is_lower = False

        if is_int_range:
            if not low_edge.allow_equal:
                if not low_edge.val == None:
                    low_edge.val += 1 # (X)[ -> [(X+1)
                low_edge.allow_equal = True
            if not up_edge.allow_equal:
                if not up_edge.val == None:
                    up_edge.val -= 1 # ](X) -> (X-1)]
                up_edge.allow_equal = True

        if (not low_edge.val == None and 
            not up_edge.val == None and
            low_edge.val > up_edge.val):
            raise ValueError("Lower edge of range can't be less than upper edge")

        self.low_edge = low_edge
        self.up_edge = up_edge
        self.is_int_range = is_int_range

    def __repr__(self):
        return "Range(low_edge={},up_edge={},is_int_range={})".format(
            repr(self.low_edge),
            repr(self.up_edge),
            repr(self.is_int_range))
    
    def __str__(self):
        return "{} {} {}".format(
            str(self.low_edge),
            "int" if self.is_int_range else "float",
            str(self.up_edge),
        )

    def __contains__(self,item):
        if isinstance(item, RangeEdge):
            return item <= self.up_edge and item >= self.low_edge
        if isinstance(item, Range):
            return item.low_edge in self and item.up_edge in self
        elif not is_int_or_float(item):
            return False
        elif self.is_int_range and not float(item).is_integer():
            return False
        return self.low_edge.evaluate(item) and self.up_edge.evaluate(item)
    
    def overlaps(self, other):
        if (self.low_edge <= other.low_edge and
            self.up_edge >= other.low_edge):
            return True
        elif (self.low_edge <= other.up_edge and
            self.up_edge >= other.up_edge):
            return True
        return False

    def touches(self,other):
        if self.is_int_range:
            try:
                if self.up_edge.val == other.low_edge.val - 1:
                    return True # [* self 2] & [3 other *]
            except (TypeError, SyntaxError):
                pass
            try:
                if self.low_edge.val == other.up_edge.val + 1:
                    return True # [* other 2] & [3 self *]
            except (TypeError, SyntaxError):
                pass
        else:
            if (self.up_edge.val == other.low_edge.val and 
                self.up_edge.val != None and
                self.up_edge.allow_equal != other.low_edge.allow_equal
                ):
                return True # [* self 2] & 2[ other *] ||  [* self ]2 & [2 other *]
            if (self.low_edge.val == other.up_edge.val and 
                self.low_edge.val != None and
                self.low_edge.allow_equal != other.up_edge.allow_equal
                ):
                return True # [* other 2] & 2[ self *] ||  [* other ]2 & [2 self *]

        return self.overlaps(other)

    def merge(self, other):
        if not self.is_int_range == other.is_int_range:
            raise ValueError("Can't merge float range with int range")
        if not self.touches(other):
            raise ValueError("Ranges aren't mergeable")
        lower = (self.low_edge 
            if self.low_edge <= other.low_edge 
            else other.low_edge)
        upper = (self.up_edge 
            if self.up_edge >= other.up_edge 
            else other.up_edge)
        return Range(lower,upper,self.is_int_range)

    def __add__(self,other):
        return self.merge(other)

    def __sub__(self,other):
        pass


class BaseSet(ABC):
    @abstractmethod
    def is_member(self, value):
        pass
    @abstractmethod
    def contains_set(self, value):
        pass
    @abstractmethod
    def get_intersection(self, set_b):
        pass
    @abstractmethod
    def get_union_with(self, set_b):
        pass
    @abstractmethod
    def get_difference_from(self, set_b):
        pass
    @abstractmethod
    def get_complement(self):
        pass


re2 = RangeEdge(val=3,allow_equal=True)
re1 = RangeEdge(val=1,allow_equal=False)
#r = Range(re1,re2, True)

def check_range_less_than():
    for i in range(1,4):
        print("\n\n")
        for is_lower_1 in range(0,2):
            print("")
            for allow_equal_1 in range(0,2):
                for is_lower_2 in range(0,2):
                    for allow_equal_2 in range(0,2):
                        r1 = RangeEdge(val=2, allow_equal=allow_equal_1, is_lower=is_lower_1)
                        r2 = RangeEdge(val=i, allow_equal=allow_equal_2, is_lower=is_lower_2)
                        print("{} < {}: {}".format(str(r1),str(r2),r1 < r2))

#check_range_less_than()

re_l = RangeEdge(6, True,True)
re_u = RangeEdge(10, False)

range1 = Range(
    low_edge=RangeEdge(val=1,allow_equal=True),
    up_edge=RangeEdge(val=2,allow_equal=False),
    is_int_range=False
)
range2 = Range(
    low_edge=RangeEdge(val=2,allow_equal=True),
    up_edge=RangeEdge(val=4,allow_equal=True),
    is_int_range=False
)
print(range1)
print(range2)
print("range1 overlaps range2: " + str(range1.overlaps(range2)))
print("range1 touches range2: " + str(range1.touches(range2)))
print("range2 touches range1: " + str(range2.touches(range1)))

range3 = range1 + range2
print(range3)
print(range1 in range3)
print(range2 in range3)
print(range3 in range1)
print(range3 in range2)

r1 = Range(re_l, re_u, is_int_range=False)
r2 = Range(9.999999, 15, is_int_range=False)
'''
print(r1)
print(r2)
print(r1.is_overlapping(r2))'''