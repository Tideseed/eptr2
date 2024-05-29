from typing import Any
import urllib3
import re
import json
from urllib.parse import urljoin
import copy
from eptr2.mapping import (
    get_total_path,
    get_call_method,
    get_required_parameters,
    get_param_label,
    get_path_map,
    get_optional_parameters,
)
from warnings import warn
from eptr2.processing.preprocess.params import preprocess_parameter


class EPTR2:
    def __init__(self, **kwargs) -> None:
        ## kwargs are
        ### map_param_labels: bool
        ### secure: bool
        ### query_parameters: dict
        ### just_call_phrase: bool
        self.ssl_verify = kwargs.get("ssl_verify", True)
        self.check_postprocess(postprocess=kwargs.get("postprocess", True))
        self.get_raw_response = kwargs.get("get_raw_response", False)
        self.root_phrase = kwargs.get("root_phrase", "https://seffaflik.epias.com.tr")

    ## Ref: https://stackoverflow.com/a/62303969/3608936
    def __getattr__(self, __name: str) -> Any:
        def method(*args, **kwargs):
            key_raw = __name
            key = re.sub("_", "-", key_raw)
            if key not in get_path_map(just_call_keys=True):
                raise Exception(
                    "This call is not yet defined. Call 'get_available_calls' method to see the available calls."
                )
            # required_body_params = get_required_parameters(key)
            return getattr(self, "call")(key=key, **kwargs)

        return method

    def check_postprocess(self, postprocess: bool = True):
        self.postprocess = postprocess
        if self.postprocess:
            try:
                from eptr2.mapping.processing import get_postprocess_function
            except ImportError:
                print(
                    "pandas is not installed. Some functionalities may not work properly. Postprocessing is disabled. To disable postprocessing just set 'postprocess' parameter to False when calling EPTR2 class.",
                )
                self.postprocess = False

    def get_available_calls(self):
        return get_path_map(just_call_keys=True)

    def call(self, key: str, **kwargs):
        call_path = get_total_path(key)
        call_method = get_call_method(key)
        required_body_params = get_required_parameters(key)
        call_body_raw = kwargs.pop("call_body", kwargs)

        ## Parameter change
        if key in ["bpm-orders", "bpm-orders-w-avg"]:
            if "date_time" in call_body_raw.keys():
                warn(
                    f"date_time parameter name is deprecated for {key}. Use 'date' instead. Support will be removed starting from version 0.3.0.",
                    DeprecationWarning,
                    stacklevel=2,
                )

                call_body_raw["date"] = call_body_raw.pop("date_time")

        optional_body_params = get_optional_parameters(key)
        all_params = required_body_params + optional_body_params

        call_body = {
            k: preprocess_parameter(k, v)
            for k, v in call_body_raw.items()  ## If there is a call_body parameter in kwargsi, use it, else use kwargs
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
                cb2 = {}
                for k, v in call_body.items():
                    ## Updated this part to handle multiple labels originating from a single label
                    label = get_param_label(k)["label"]
                    value = v
                    if isinstance(label, list):
                        for l in label:
                            cb2[l] = value
                    else:
                        cb2[label] = value
                call_body = copy.deepcopy(cb2)

        elif len(required_body_params) > 0:
            raise Exception("Required parameters are missing in call body.")

        ## If the call is uevm, change powerPlantId to powerplantId due to only non-standard naming in powerPlantId
        if key == "uevm" and "powerPlantId" in call_body.keys():
            call_body["powerplantId"] = call_body.pop("powerPlantId")

        res = transparency_call(
            call_path=call_path,
            call_method=call_method,
            call_body=call_body,
            root_phrase=self.root_phrase,
            ssl_verify=self.ssl_verify,
            **kwargs,
        )

        if kwargs.get("get_raw_response", self.get_raw_response):
            return res

        res = json.loads(res.data.decode("utf-8"))
        if kwargs.get("postprocess", self.postprocess):
            from eptr2.mapping.processing import get_postprocess_function

            df = get_postprocess_function(key)(res, key=key)
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

    call_phrase = urljoin(root_phrase, call_path)

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

    ssl_verify = kwargs.pop("ssl_verify", True)

    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED" if ssl_verify else "CERT_NONE")
    res = http.request(
        method=call_method,
        url=urljoin(call_phrase, ""),
        body=json.dumps(call_body),
        headers={"Content-Type": "application/json"},
        **kwargs.get("request_kwargs", {}),
    )
    if res.status not in [200, 201]:
        raise Exception(
            "Request failed with status code: "
            + str(res.status)
            + "\n"
            + res.data.decode("utf-8")
        )
    return res
