from enum import Enum


class TransactionStatus(Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    CANCELED = "CANCELED"

class TransactionsFilter(Enum):
    ALL = "all"
    MARKET = "market"
    RESOURCE = "resource"
    SERVICE = "service"