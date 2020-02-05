from typing import List


class ValidationError(Exception):
    def __init__(self, source, message):
        msg = f"{source}: {message}"
        super(ValidationError, self).__init__(msg)


class ConfigError(Exception):
    def __init__(self, *args, **kwargs):
        super(ConfigError, self).__init__(args, kwargs)


class MultipleValidationError(Exception):
    def __init__(self, errors: List[ValidationError]):
        msg = f"Multiple validation errors occured:\n"
        for item in errors:
            msg += f"{item}\n"
        super(MultipleValidationError, self).__init__(msg)
