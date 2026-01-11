from ninja_extra import api_controller, http_post
from ninja.errors import HttpError
from apps.phone_info.services.phone_range import detect_operator_and_region, validate_ru_phone_or_raise


@api_controller("/phone-info", tags=["Phone Info"])
class PhoneInfoController:
    @http_post("/")
    def get_phone_info(self, phone_number: str):
        validate_ru_phone_or_raise(phone_number)
        details = detect_operator_and_region(phone_number)
        if details is None:
            raise HttpError(404, "Phone number not found")

        return details
