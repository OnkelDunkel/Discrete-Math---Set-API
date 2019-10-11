from abc import ABC, abstractmethod
from rangelimit import RangeLimitBase, RangeLimit, validate_limits

class BaseSet(ABC):
    @abstractmethod
    def is_member(self, value):
        pass

    @abstractmethod
    def contains_set(self, value):
        pass

    def get_intersection(self, set_b):
        return IntersectionSet(self, set_b)

    def get_union_with(self, set_b):
        return UnionSet(self,set_b)

    def get_difference_from(self, set_b):
        return DifferenceSet(self,set_b)

    def get_complement(self):
        return ComplementSet(self)

class IntersectionSet(BaseSet):
    def __init__(self,set_a,set_b):
        self.set_a = set_a
        self.set_b = set_b

    def is_member(self, value):
        return self.set_a.is_member(value) and self.set_b.is_member(value)

    def contains_set(self, value):
        pass

class UnionSet(BaseSet):
    def __init__(self,set_a,set_b):
        self.set_a = set_a
        self.set_b = set_b

    def is_member(self, value):
        return self.set_a.is_member(value) or self.set_b.is_member(value)

    def contains_set(self, value):
        pass

class DifferenceSet(BaseSet):
    def __init__(self,set_a,set_b):
        self.set_a = set_a
        self.set_b = set_b

    def is_member(self, value):
        return self.set_a.is_member(value) and not self.set_b.is_member(value)

    def contains_set(self, value):
        pass

class ComplementSet(BaseSet):
    def __init__(self,set_a):
        self.set_a = set_a

    def is_member(self, value):
        return not self.set_a.is_member(value)

    def contains_set(self, value):
        pass

class EmptySet(BaseSet):
    def is_member(self,value):
        return False

    def contains_set(self, value):
        pass

class UniversalSet(BaseSet):
    def is_member(self,value):
        return True

    def contains_set(self, value):
        pass

class RealNumberSet(BaseSet):
    def __init__(self,min_val,max_val):
        self.min_limit = min_val if isinstance(min_val, RangeLimitBase) else RangeLimit("min", limit_value=min_val)
        self.max_limit = max_val if isinstance(max_val, RangeLimitBase) else RangeLimit("max", limit_value=max_val)
        if not validate_limits(self.min_limit, self.max_limit):
            raise "Invalid min or max limit for set"
    
    def is_member(self, value):
        if not (isinstance(value,int) or isinstance(value,float)):
            return False
        return self.min_limit.evaluate(value) and self.max_limit.evaluate(value)

    def contains_set(self, value):
        pass

class IntegerSet(RealNumberSet):
    def is_member(self, value):
        if not (float(value)).is_integer():
            return False
        return super().is_member(value)

    def contains_set(self, value):
        pass

class IterableSet(BaseSet):
    def __init__(self,iterable_col):
        try:
            iter(iterable_col)
        except TypeError:
            raise TypeError("iterable_col should be iterable")
        self.col = iterable_col

    def is_member(self, value):
        return value in self.col

    def contains_set(self, value):
        pass

    def is_subset_of(self,set_b):
        for e in self.col:
            if not set_b.is_member(e):
                return False
        return True

    def __getitem__(self, key):
        return self.col[key]