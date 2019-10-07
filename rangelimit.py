from abc import ABC, abstractmethod

def validate_limits(limit1, limit2):

    min_limit = None
    max_limit = None
    
    if limit1.limit_type == "min" and limit2.limit_type == "max":
        min_limit, max_limit = limit1, limit2
    elif limit1.limit_type == "max" and limit2.limit_type == "min":
        min_limit, max_limit = limit2, limit1
    else:
        return False

    min_val, max_val = min_limit.limit_value, max_limit.limit_value

    def is_valid_type(number_value):
        return isinstance(number_value, int) or isinstance(number_value, float) or number_value == None

    if not (is_valid_type(min_val) and is_valid_type(min_val)):
        return False

    if min_val == None or max_val == None:
        return True
    if min_val < max_val:
        return True
    if min_val == max_val:
        return min_limit.allow_equal and max_limit.allow_equal
    return False

class RangeLimitBase(ABC):
    @abstractmethod
    def __init__(self, limit_type, limit_value=None, allow_equal=True):
        pass
    @abstractmethod
    def evaluate(self, value):
        pass

class RangeLimit:
    def __init__(self, limit_type, limit_value=None, allow_equal=True):
        if not limit_type in ["min", "max"]:
            raise ValueError("Only 'min', 'max' are accepted limit types")
        if not (isinstance(limit_value, int) or (isinstance(limit_value, float)) or limit_value == None):
            raise TypeError("Only int, float or None are accepted as limit value")
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














