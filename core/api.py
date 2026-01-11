from ninja_extra import NinjaExtraAPI
from apps.phone_info.controllers import PhoneInfoController

api = NinjaExtraAPI()

api.register_controllers(
    PhoneInfoController,
)
