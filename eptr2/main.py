import os
from typing import Any
import pandas as pd
import json
import requests
import re
from urllib.parse import urljoin

from eptr2.mapping import (
    get_total_path,
    get_call_method,
    get_required_parameters,
    get_param_label,
    get_path_map,
    get_optional_parameters,
)

from eptr2.processing import preprocess_parameter, postprocess_items_to_df
from eptr2.mapping import get_postprocess_function


class EPTR2:
    def __init__(self, **kwargs) -> None:
        ## kwargs are
        ### map_param_labels: bool
        ### secure: bool
        ### query_parameters: dict
        ### just_call_phrase: bool
        self.ssl_verify = kwargs.get("ssl_verify", False)
        self.postprocess = kwargs.get("postprocess", True)

    ## Ref: https://stackoverflow.com/a/62303969/3608936
    def __getattr__(self, __name: str) -> Any:
        def method(*args, **kwargs):
            key = re.sub("_", "-", __name)
            if key not in get_path_map(just_call_keys=True):
                raise Exception(
                    "This call is not yet defined. Call 'get_available_calls' method to see the available calls."
                )
            required_body_params = get_required_parameters(key)
            return getattr(self, "call")(key=key, **kwargs)

        return method

    def get_available_calls(self):
        return get_path_map(just_call_keys=True)

    def call(self, key: str, **kwargs):
        call_path = get_total_path(key)
        call_method = get_call_method(key)
        required_body_params = get_required_parameters(key)
        optional_body_params = get_optional_parameters(key)
        all_params = required_body_params + optional_body_params

        call_body = {
            k: preprocess_parameter(k, v)
            for k, v in kwargs.pop(
                "call_body", kwargs
            ).items()  ## If there is a call_body parameter in kwargsi, use it, else use kwargs
            if k in all_params
        }

        for body_key in required_body_params:
            if body_key not in call_body.keys():
                call_body[body_key] = preprocess_parameter(body_key, None)
            kwargs.pop(body_key, None)

        if call_body is not None:
            if not all([x in call_body.keys() for x in required_body_params]):
                raise Exception("Some required parameters are missing in call body.")

            if kwargs.get("map_param_labels", True):
                call_body = {
                    get_param_label(k)["label"]: v for k, v in call_body.items()
                }
        elif len(required_body_params) > 0:
            raise Exception("Required parameters are missing in call body.")

        res = transparency_call(
            call_path=call_path,
            call_method=call_method,
            call_body=call_body,
            ssl_verify=self.ssl_verify,
            **kwargs,
        )

        if kwargs.get("postprocess", self.postprocess):
            df = get_postprocess_function(key)(res)
            return df

        return res


def transparency_call(
    call_path: dict,
    call_method: str,
    call_body: dict | None = None,
    root_phrase: str = "https://seffaflik.epias.com.tr",
    **kwargs,
):
    ## kwargs are
    ### secure: bool
    ### query_parameters: dict
    ### just_call_phrase: bool

    call_phrase = os.path.join(root_phrase, call_path)

    ## If there are query parameters (not body parameters), append
    q_params = kwargs.get("query_parameters", {})

    if len(q_params.keys()) > 0:
        call_phrase += "?" + "&".join(
            [str(k) + "=" + str(v) for k, v in q_params.items()]
        )

    if kwargs.pop("just_call_phrase", False):
        return call_phrase

    if call_body is not None and call_body != {} and call_method == "GET":
        raise Exception("GET method does not allow body parameters.")

    ssl_verify = kwargs.pop("ssl_verify", False)

    res = requests.request(
        method=call_method,
        url=urljoin(call_phrase, ""),
        json=call_body,
        verify=ssl_verify,
        **kwargs.get("request_kwargs", {}),
    )

    if res.status_code not in [200, 201]:
        raise Exception(
            "Request failed with status code: " + str(res.status_code) + "\n" + res.text
        )

    return res
