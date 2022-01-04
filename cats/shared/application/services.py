from typing import Any, Dict, List, Type


def validator(rules: Dict[Type, Any]) -> List:
    failures = []
    for rule, value in rules.items():
        try:
            if value is not None:
                rule(value)
        except Exception as ex:
            failures.append(ex)
    return failures
