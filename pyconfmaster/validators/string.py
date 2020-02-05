import re
import socket
from pyconfmaster.validators.base import BaseValidator
from pyconfmaster.exceptions import ValidationError


class HostValidator(BaseValidator):
    def __init__(self):
        super(HostValidator, self).__init__([str])

    @staticmethod
    def is_valid_hostname(hostname):
        if hostname[-1] == ".":
            # strip exactly one dot from the right, if present
            hostname = hostname[:-1]
        if len(hostname) > 253:
            return False

        labels = hostname.split(".")

        # the TLD must be not all-numeric
        if re.match(r"[0-9]+$", labels[-1]):
            return False

        allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(label) for label in labels)

    @staticmethod
    def is_valid_ipv4_address(address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count(".") == 3
        except socket.error:  # not a valid address
            return False

        return True

    def validate(self, value):
        super(HostValidator, self).validate(value)
        if not HostValidator.is_valid_hostname(
            value
        ) and not HostValidator.is_valid_ipv4_address(value):
            raise ValidationError(type(self).__name__, "Not valid ip/hostname")
