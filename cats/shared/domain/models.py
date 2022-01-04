from dataclasses import dataclass


@dataclass(frozen=True)
class ID:
    value: str

    def __post_init__(self):
        self._invariant_must_have_valid_format()

    def _invariant_must_have_valid_format(self) -> None:
        if not self.value.startswith('AS-') or len(self.value) < 17:
            raise ValueError(f'Invalid ID <{self.value}>, must have AS-XXXX-XXXX-XXXX format.')
