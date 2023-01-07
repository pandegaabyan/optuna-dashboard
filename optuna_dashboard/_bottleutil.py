import base64
import functools
import json
import logging
import traceback
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import TypeVar
from typing import Union

from bottle import BaseResponse
from bottle import response


BottleViewReturn = Union[str, bytes, Dict[str, Any], BaseResponse]
BottleView = TypeVar("BottleView", bound=Callable[..., BottleViewReturn])
logger = logging.getLogger(__name__)


def json_api_view(view: BottleView) -> BottleView:
    @functools.wraps(view)
    def decorated(*args: list[Any], **kwargs: dict[str, Any]) -> BottleViewReturn:
        try:
            response.content_type = "application/json"
            response_body = view(*args, **kwargs)
            return response_body
        except Exception as e:
            response.status = 500
            response.content_type = "application/json"
            stacktrace = "\n".join(traceback.format_tb(e.__traceback__))
            logger.error(f"Exception: {e}\n{stacktrace}")
            return json.dumps({"reason": "internal server error"})

    return cast(BottleView, decorated)


def parse_data_uri(data_uri: str) -> tuple[str, bytes]:
    prefix, a = data_uri.split(":", 1)
    if prefix != "data":
        raise ValueError("data url must start with 'data:' prefix")
    mediatype_with_suffix, base64_data = a.split(",", 1)
    mediatype = mediatype_with_suffix.split(";", 1)[0]
    data = base64.standard_b64decode(base64_data)
    return mediatype, data
