from dataclasses import dataclass, field

@dataclass(frozen=True)
class Attribution:
    requested_credits: tuple[str, ...] = ()
    evidenced_contributions: tuple[dict, ...] = ()
    limitations: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        return {
            "requested_credits": list(self.requested_credits),
            "evidenced_contributions": list(self.evidenced_contributions),
            "limitations": list(self.limitations),
        }

def separate_credits(requested_credits=(), evidenced_contributions=()) -> Attribution:
    return Attribution(tuple(requested_credits), tuple(evidenced_contributions))
