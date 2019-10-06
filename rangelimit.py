from abc import ABC, abstractmethod

limit_types = ["min", "max"]

def validate_limits(limit1, limit2):
        if not (isinstance(limit1, RangeLimitBase) and isinstance(limit2, RangeLimitBase)):
            raise TypeError("Min and max should be both be instances of RangeLimit")
        if limit1.limit_type == limit2.limit_type:
            raise ValueError("Both limits are {}".format(limit1.limit_type))
        if limit1.limit_type == "min" and limit2.limit_type == "max":
            pass

class RangeLimitBase(ABC):
    @abstractmethod
    def __init__(self, limit_type, limit_value=None, allow_equal=True):
        pass
    @abstractmethod
    def evaluate(self, value):
        pass

class RangeLimit:
    def __init__(self, limit_type, limit_value=None, allow_equal=True):
        if not limit_type in limit_types:
            raise ValueError("Only 'min', 'max' are accepted limit types")
        if not (isinstance(limit_value, int) or (isinstance(limit_value, float)) or limit_value == None):
            raise ValueError("Only int, float or None are accepted as {} value".format(limit_type))
        self.limit_type = limit_type
        self.limit_value = limit_value
        self.allow_equal = allow_equal
    
    def evaluate(self, value):
        if self.limit_value == None:
            return True
        if self.allow_equal and value == self.limit_value:
            return True
        if self.limit_type == "min":
            return value > self.limit_value
        else:
            return value < self.limit_value














