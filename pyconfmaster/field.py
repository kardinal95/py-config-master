from pyconfmaster.exceptions import ValidationError, MultipleValidationError


class Field:
    def __init__(
        self,
        type=str,
        value=None,
        validators=list(),
        required=True,
        default=None,
    ):
        self.type = type
        self.validators = validators
        self.required = required
        self.default = default
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if type(value) is not self.type and self.required:
            raise TypeError(
                f"Incorrect type. Expected {self.type.__name__}"
                + f", got {type(value).__name__}"
            )
        try:
            self._value = value
            self.validate()
        except ValidationError as e:
            self._value = None
            raise e

    def validate(self):
        if self.value is None:
            if self.required:
                raise ValidationError(
                    type(self).__name__, "Field is required but got None"
                )
            else:
                return
        errors = list()
        for item in self.validators:
            try:
                item.validate(self.value)
            except ValidationError as e:
                errors.append(e)
        if len(errors) > 1:
            raise MultipleValidationError(errors)
        if len(errors) == 1:
            raise errors[0]
