from typing import Any, List, Tuple, Type


def validator(rules: List[Type], values: List[Any]) -> Tuple[List[Exception], List[object]]:
    """
    Validates the given values using the given rules.

    :param rules: List of types that will be used to validate the values.
    :param values: List of values to validated.
    :return: Tuple of a list of exceptions and a list of valid values.
    """
    fail = []
    success = []
    for rule, value in list(zip(rules, values)):
        try:
            result = rule(value)
            success.append(value if result is None else result)
        except Exception as ex:
            fail.append(ex)
    return fail, success
