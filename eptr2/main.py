import os
import pandas as pd
import json
import requests

from eptr2.mapping import (
    get_total_path,
    get_method,
    get_required_parameters,
    get_param_label,
)


class EPTR2:
    def __init__(self, **kwargs) -> None:
        ## kwargs are
        ### map_param_labels: bool
        ### secure: bool
        ### query_parameters: dict
        ### just_call_phrase: bool
        pass

    def call(self, key: str, call_body: dict | None, **kwargs):
        call_path = get_total_path(key)
        call_method = get_method(key)
        required_body_params = get_required_parameters(key)

        if call_body is not None:
            if not all([x in call_body.keys() for x in required_body_params]):
                raise Exception("Some required parameters are missing in call body.")

            if kwargs.get("map_param_labels", True):
                call_body = {get_param_label(k): v for k, v in call_body.items()}
        elif len(required_body_params) > 0:
            raise Exception("Required parameters are missing in call body.")

        res = transparency_call(
            call_path=call_path, call_method=call_method, call_body=call_body, **kwargs
        )

        return res

    def mcp(self, start_date, end_date, **kwargs):
        return self.call(
            key="mcp",
            call_body={"start_date": start_date, "end_date": end_date, **kwargs},
        )


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

    if call_body is not None and call_method == "GET":
        raise Exception("GET method does not allow body parameters.")

    res = requests.request(
        method=call_method,
        url=call_phrase,
        json=call_body,
        verify=kwargs.get(
            "secure", False
        ),  ## With Openssl 3.0 it is possible to get errors like "certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)"
        **kwargs,
    )

    if res.status_code not in [200, 201]:
        raise Exception(
            "Request failed with status code: " + str(res.status_code) + "\n" + res.text
        )

    return res
