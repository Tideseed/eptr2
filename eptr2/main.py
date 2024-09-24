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
from datetime import datetime, timedelta


class EPTR2:
    def __init__(
        self,
        username: str = None,
        password: str = None,
        tgt_d: dict | None = None,
        **kwargs,
    ) -> None:
        ## kwargs are
        ### map_param_labels: bool
        ### secure: bool
        ### query_parameters: dict
        ### just_call_phrase: bool
        self.ssl_verify = kwargs.get("ssl_verify", True)
        self.check_postprocess(postprocess=kwargs.get("postprocess", True))
        self.get_raw_response = kwargs.get("get_raw_response", False)
        self.username = username
        self.password = password
        self.is_test = kwargs.get("is_test", False)
        self.skip_credentials = kwargs.get("skip_credentials", False)
        root_phrase_test = "-prp" if self.is_test else ""
        root_phrase_default = f"https://seffaflik{root_phrase_test}.epias.com.tr"
        self.root_phrase = kwargs.get("root_phrase", root_phrase_default)
        self.skip_login_warning = kwargs.get("skip_login_warning", False)

        if tgt_d is not None:
            self.import_tgt_info(tgt_d)
        else:
            self.tgt = None
            self.tgt_exp = 0
            self.tgt_exp_0 = 0

        self.check_renew_tgt()

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

    def import_tgt_info(self, tgt_d):
        self.tgt = tgt_d["tgt"]
        self.tgt_exp = tgt_d["tgt_exp"]
        self.tgt_exp_0 = tgt_d["tgt_exp_0"]

    def check_renew_tgt(self):
        if self.tgt is None or self.tgt_exp_0 < datetime.now().timestamp():
            self.get_tgt()

    def get_tgt(self, **kwargs):
        if self.username is None or self.password is None:
            if self.skip_credentials:
                if not self.skip_login_warning:
                    print(
                        "Warning: You chose to skip the credentials and your calls may fail due to authentication requirements. Username and password will be required in the EPIAS Transparency API after August 26 (check EPIAS Transparency website for the latest and detailed information). This warning is shown once per session. If you want to disable it set 'skip_login_warning' parameter to True when calling EPTR2 class."
                    )
                    self.skip_login_warning = True

                self.tgt = None
                self.tgt_exp = 0
                self.tgt_exp_0 = 0
                return None
            else:
                raise Exception(
                    "Username and password must be provided for tgt renewal."
                )

        test_suffix = "-prp" if self.is_test else ""
        login_url = f"""https://giris{test_suffix}.epias.com.tr/cas/v1/tickets"""
        login_url += f"?username={self.username}&password={self.password}"

        http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED" if self.ssl_verify else "CERT_NONE"
        )

        res = http.request(
            method="POST",
            url=login_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            **kwargs.get("request_kwargs", {}),
        )
        if res.status not in [200, 201]:
            raise Exception(
                "Request failed with status code: "
                + str(res.status)
                + "\n"
                + res.data.decode("utf-8")
            )

        res_data = json.loads(res.data.decode("utf-8"))
        self.tgt = res_data["tgt"]
        try:
            tgt_start_time = datetime.fromisoformat(res_data["created"])
        except:
            tgt_start_time = datetime.now()

        ## Hard timeout
        self.tgt_exp = (tgt_start_time + timedelta(hours=6)).timestamp()

        ## Soft timeout
        self.tgt_exp_0 = min(
            self.tgt_exp,
            (tgt_start_time + timedelta(hours=1, minutes=45)).timestamp(),
        )

    def export_tgt_info(self):
        return {
            "tgt": self.tgt,
            "tgt_exp": self.tgt_exp,
            "tgt_exp_0": self.tgt_exp_0,
        }

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
        self.check_renew_tgt()

        call_path = get_total_path(key)
        call_method = get_call_method(key)
        required_body_params = get_required_parameters(key)
        call_body_raw = kwargs.pop("call_body", kwargs)

        ## Parameter change
        if key in ["bpm-orders", "bpm-orders-w-avg"]:
            if "date_time" in call_body_raw.keys():
                raise Exception(
                    f"date_time parameter is not supported for {key}. Use 'date' instead."
                )
                # warn(
                #     f"date_time parameter name is deprecated for {key}. Use 'date' instead. Support will be removed starting from version 0.3.0.",
                #     DeprecationWarning,
                #     stacklevel=2,
                # )

                # call_body_raw["date"] = call_body_raw.pop("date_time")

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
            is_test=self.is_test,
            tgt=self.tgt,
            **kwargs,
        )

        ## Set soft timeout for tgt renewal
        self.tgt_exp_0 = min(
            self.tgt_exp,
            datetime.now().timestamp() + 60 * 90,
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
    is_test: bool = False,
    tgt: str = None,
    **kwargs,
):
    ## kwargs are
    ### secure: bool
    ### query_parameters: dict
    ### just_call_phrase: bool

    root_phrase_test = "-prp" if is_test else ""
    root_phrase_default = f"https://seffaflik{root_phrase_test}.epias.com.tr"
    root_phrase = kwargs.get("root_phrase", root_phrase_default)

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

    header_d = {"Content-Type": "application/json"}
    if tgt is not None:
        header_d["TGT"] = tgt

    res = http.request(
        method=call_method,
        url=urljoin(call_phrase, ""),
        body=json.dumps(call_body),
        headers=header_d,
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
