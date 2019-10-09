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
    
    def __lt__(self,other):
        if self.val == None:
            return False
        if other.val == None:
            return True
        if self.val == other.val:
            if self.is_lower:
                if (self.allow_equal and other.is_lower and not other.allow_equal):
                    return True
                return False
            else:
                if other.is_lower:
                    if self.allow_equal and other.allow_equal:
                        return False
                    return True
                else:
                    if not self.allow_equal and other.allow_equal:
                        return True
                    return False
        return self.val < other.val
    def __le__(self, other):
        return self < other or self == other
    def __eq__(self, other):
        return (self.val == other.val and 
            self.allow_equal == other.allow_equal)
    def __ne__(self, other):
        return not self == other
    def __ge__(self, other):
        return self > other or self == other
    def __gt__(self, other):
        return not self <= other






class Range:
    def __init__(self,low_edge,up_edge,is_int_range=False):
        if is_int_or_float(low_edge) or low_edge == None:
            low_edge = RangeEdge(val=low_edge)
        if is_int_or_float(up_edge) or up_edge == None:
            up_edge = RangeEdge(val=up_edge)
        low_edge.is_lower = True
        up_edge.is_lower = False

        if (not low_edge.val == None and 
            not up_edge.val == None and
            low_edge.val > up_edge.val):
            raise ValueError("Lower edge of range can't be less than upper edge")

        self.low_edge = low_edge
        self.up_edge = up_edge
        self.is_int_range = is_int_range

    def __repr__(self):
        return "Range({},{},{})".format(
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
        if not is_int_or_float(item):
            return False
        if self.is_int_range and not float(item).is_integer():
            return False
        return self.low_edge.evaluate(item) and self.up_edge.evaluate(item)
    
    def is_overlapping(self, other):
        '''
        if self.low_edge.val == None:
            if self.up_edge.val == None:
                return True
            if other.low_edge.val == None:
                return True
            if self.up_edge.val < other.low_edge.val:
                return True
            if self.up_edge.val == other.low_edge.val:
                return self.up_edge.allow_equal and other.low_edge.allow_equal
        elif self.up_edge.val == None:
            if other.up_edge.val == None:
                return True
            if self.low_edge.val < other.up_edge.val:
                return True
            if self.low_edge.val == other.up_edge.val:
                return self.low_edge.allow_equal and other.up_edge.allow_equal
        raise "Code should never get here self: {}, other: {}".format(str(self), str(other))
    '''

    def is_mergeable(self,other):
        if not self.is_int_range == other.is_int_range:
            return False
        if self.is_int_range:
            if (self.low_edge.val == other.up_edge.val + 1 or
                self.up_edge.val + 1 == other.low_edge.val):
                return True
        else:
            if (self.low_edge.val == other.up_edge.val and
                (self.low_edge.allow_equal or other.up_edge.allow_equal)):
                return True
            elif (self.up_edge.val == other.low_edge.val and
                (self.up_edge.allow_equal or other.low_edge.allow_equal)):
                return True
        return self.is_overlapping(other)

    def merge(self, other):
        if not self.is_int_range == other.is_int_range:
            raise ValueError("Can't merge float range with int range")
        if not self.is_mergeable(other):
            raise ValueError("Not ranges aren't mergeable")
        lower = (self.low_edge 
            if self.low_edge >= other.low_edge 
            else other.low_edge)
        upper = (self.up_edge 
            if self.up_edge >= other.up_edge 
            else other.up_edge)
        return Range(lower,upper,self.is_int_range)

    def __add__(self,other):
        self.merge(other)

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
        pass
    for allow_equal_1 in range(0,2):
        for is_lower_1 in range(0,2):
            for allow_equal_2 in range(0,2):
                for is_lower_2 in range(0,2):
                    r1 = RangeEdge(val=3, allow_equal=allow_equal_1, is_lower=is_lower_1)
                    r2 = RangeEdge(val=i, allow_equal=allow_equal_2, is_lower=is_lower_2)
                    print("{} < {}: {}".format(str(r1),str(r2),r1 < r2))

check_range_less_than()


