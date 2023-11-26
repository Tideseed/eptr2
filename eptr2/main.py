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
)

from eptr2.processing import preprocess_parameter


class EPTR2:
    def __init__(self, **kwargs) -> None:
        ## kwargs are
        ### map_param_labels: bool
        ### secure: bool
        ### query_parameters: dict
        ### just_call_phrase: bool
        pass

    ## Ref: https://stackoverflow.com/a/62303969/3608936
    def __getattr__(self, __name: str) -> Any:
        def method(*args, **kwargs):
            key = re.sub("_", "-", __name)
            if key not in get_path_map(just_call_keys=True):
                raise Exception(
                    "This call is not yet defined. Call 'get_available_calls' method to see the available calls."
                )
            required_body_params = get_required_parameters(key)
            call_body = {
                k: preprocess_parameter(k, v)
                for k, v in kwargs.items()
                if k in required_body_params
            }
            for body_key in required_body_params:
                kwargs.pop(body_key, None)
            return getattr(self, "call")(key=key, call_body=call_body, **kwargs)

        return method

    def get_available_calls(self):
        return get_path_map(just_call_keys=True)

    def call(self, key: str, call_body: dict | None, **kwargs):
        call_path = get_total_path(key)
        call_method = get_call_method(key)
        required_body_params = get_required_parameters(key)

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
            call_path=call_path, call_method=call_method, call_body=call_body, **kwargs
        )

        return res


def transparency_call(
    call_path: dict,
    call_method: str,
    call_body: dict | None = None,
    root_phrase: str = "https://seffaflik-prp.epias.com.tr",
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

    if kwargs.get("just_call_phrase", False):
        return call_phrase

    if call_body is not None and call_body != {} and call_method == "GET":
        raise Exception("GET method does not allow body parameters.")

    res = requests.request(
        method=call_method,
        url=urljoin(call_phrase, ""),
        json=call_body,
        verify=kwargs.get(
            "verify_with_local_ssl", False
        ),  ## With Openssl 3.0 it is possible to get errors like "certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)"
        **kwargs,
    )

    if res.status_code not in [200, 201]:
        raise Exception(
            "Request failed with status code: " + str(res.status_code) + "\n" + res.text
        )

    return res
