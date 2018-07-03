# TODO: convert the fields to required=True in schemas
__all__ = []

from temp_app.app.schema.telegram.chat import *

__all__ += chat.__all__

from app.schema.telegram.keyboard_button import *

__all__ += keyboard_button.__all__

from app.schema.telegram.message import *

__all__ += message.__all__

from app.schema.telegram.message_entity import *

__all__ += message_entity.__all__

from temp_app.app.schema.telegram.reply_keyboard_markup import *

__all__ += reply_keyboard_markup.__all__

from app.schema.telegram.update import *

__all__ += update.__all__

from temp_app.app.schema.telegram.user import *

__all__ += user.__all__

# ----------- telegram methods ----------- #

from temp_app.app.schema.telegram.send_message import *

__all__ += send_message.__all__
