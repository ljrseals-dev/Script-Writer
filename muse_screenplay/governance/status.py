from enum import Enum

class GovernanceStatus(str, Enum):
    VERIFIED = "Verified"
    INFERRED = "Inferred"
    DISPUTED = "Disputed"
    UNKNOWN = "Unknown"
    INCOMPLETE = "Incomplete"
