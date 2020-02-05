import os
import json
from pyconfmaster.exceptions import (
    ValidationError,
    ConfigError,
    MultipleValidationError,
)

__version__ = "0.1.0"


class BaseConfig:
    name = None
    subpath = None
    _fields = dict()

    @property
    def fields(self):
        return {
            key: self._fields[key].value
            for key in self._fields.keys()
            if self._fields[key].required
            or self._fields[key].value is not None
        }

    def __init__(self, name=None):
        self.name = name

    def validate(self):
        for field in self._fields.values():
            try:
                field.validate()
            except (ValidationError, MultipleValidationError) as ve:
                raise ValidationError(field, f"Errors on validation: {ve}")

    def load(self):
        path = (
            os.path.join(self.subpath, self.name)
            if self.subpath is not None
            else self.name
        )
        with open(path) as file:
            content = json.load(file)

        for item in self._fields.keys():
            if item in content.keys():
                try:
                    self._fields[item].value = content[item]
                except (ValidationError, MultipleValidationError) as e:
                    raise ValidationError(f"{self.name}:{item}", e)
            else:
                if self._fields[item].required:
                    raise ConfigError(f"Missing required parameter: {item}")

    def restore(self, optional=False):
        for field in self._fields.values():
            if field.value is None:
                if field.required or optional:
                    field.value = field.default

    def save(self):
        path = (
            os.path.join(self.subpath, self.name)
            if self.subpath is not None
            else self.name
        )
        if not os.path.exists(self.subpath):
            os.makedirs(self.subpath)
        with open(path, "w") as file:
            content = self.fields
            file.write(json.dumps(content))
