from pyconfmaster.exceptions import ValidationError
from typing import List


class BaseValidator:
    def __init__(self, types: List[type]):
        self.types = types

    def validate(self, value):
        if type(value) not in self.types:
            raise ValidationError(
                source=type(self).__name__,
                message=f"Not a supported type: {type(value).__name__}",
            )
