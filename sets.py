from abc import ABC, abstractmethod
from rangelimit import RangeLimit, validate_limits

class BaseSet(ABC):
    @abstractmethod
    def is_member(self, value):
        pass

    def get_intersection(self, set):
        return IntersectionSet(self, set)

    def get_union_with(self, set):
        return UnionSet(self,set)

    def get_difference_from(self, set):
        return DifferenceSet(self,set)

    def get_complement(self):
        return ComplementSet(self)

class IntersectionSet(BaseSet):
    def __init__(self,set1,set2):
        self.set1 = set1
        self.set2 = set2

    def is_member(self, value):
        return self.set1.is_member(value) and self.set2.is_member(value)

class UnionSet(BaseSet):
    def __init__(self,set1,set2):
        self.set1 = set1
        self.set2 = set2

    def is_member(self, value):
        return self.set1.is_member(value) or self.set2.is_member(value)

class DifferenceSet(BaseSet):
    def __init__(self,set1,set2):
        self.set1 = set1
        self.set2 = set2

    def is_member(self, value):
        return self.set1.is_member(value) and not self.set2.is_member(value)

class ComplementSet(BaseSet):
    def __init__(self,set):
        self.set = set

    def is_member(self, value):
        not self.set.is_member(value)

class EmptySet(BaseSet):
    def is_member(self,value):
        return False

class IntSet(BaseSet):
    def __init__(self,min_val,max_val):
        

        if min_val >= max_val:
            raise ValueError("Min value is greater/equal to max value")



        if not (isinstance(min_val, int) or min_val == None):
            raise ValueError("Min value should be either int or None")
        if not (isinstance(max_val, int) or max_val == None):
            raise ValueError("Max value should be either int or None")
        self.min_val = min_val
        self.max_val = max_val
    
    def is_member(self, value):
        if not (isinstance(value,int) or isinstance(value,float)):
            return False
        if not (float(value)).is_integer():
            return False
        if self.min_val == None and self.max_val == None:
            return True
        if self.min_val == None and not self.max_val == None:
            return True


        return value >= self.min_val and value <= self.max_val


r1 = IntSet(1,4)
r2 = IntSet(4,8)
















