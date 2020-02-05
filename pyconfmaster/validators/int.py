from pyconfmaster.validators.base import BaseValidator
from pyconfmaster.exceptions import ValidationError


class RangeValidator(BaseValidator):
    def __init__(self, min=None, max=None):
        super(RangeValidator, self).__init__([int])
        self.min = min
        self.max = max

    def validate(self, value):
        super(RangeValidator, self).validate(value)
        if self.min is not None and value < self.min:
            raise ValidationError(
                type(self).__name__, f"Out of range: {value}<{self.min}"
            )
        if self.max is not None and value > self.max:
            raise ValidationError(
                type(self).__name__, f"Out of range: {value}>{self.max}"
            )
