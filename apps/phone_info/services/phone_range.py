import re
from ninja.errors import HttpError
from apps.phone_info.models import PhoneRange


def detect_operator_and_region(phone: str) -> dict | None:
    """
    Определяет оператора и регион по номеру телефона РФ.

    :param phone: номер в любом формате (+7..., 8..., 7900...)
    :return: dict с оператором и регионом или None
    """

    digits = re.sub(r"\D", "", phone)

    # Приводим к формату 7XXXXXXXXXX
    if digits.startswith("8"):
        digits = "7" + digits[1:]

    if not digits.startswith("7") or len(digits) != 11:
        return None

    def_code = int(digits[1:4])
    local_number = int(digits[4:])

    record = (
        PhoneRange.objects
        .filter(
            def_code=def_code,
            from_number__lte=local_number,
            to_number__gte=local_number,
        )
        .only("operator", "region", "gar_region", "inn")
        .first()
    )

    if not record:
        return None

    return {
        "operator": record.operator,
        "region": record.region,
        "gar_region": record.gar_region,
        "inn": record.inn,
    }

def validate_ru_phone_or_raise(phone: str) -> str:
    """
    Валидирует номер телефона РФ.
    Возвращает нормализованный номер (7XXXXXXXXXX) или кидает HttpError.
    """
    if not phone:
        raise HttpError(400, "Phone number is required")

    digits = re.sub(r"\D", "", phone)

    if digits.startswith("8"):
        digits = "7" + digits[1:]

    if not digits.startswith("7") or len(digits) != 11:
        raise HttpError(
            status_code=400,
            message="Invalid phone number format. Expected +7XXXXXXXXXX or 8XXXXXXXXXX",
        )

    return digits