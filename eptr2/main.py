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
    alias_to_path,
    get_alias_map,
)
from warnings import warn
from eptr2.processing.preprocess import preprocess_parameter, process_special_calls
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
        self.path_map_keys = get_path_map(just_call_keys=True)
        self.custom_aliases = kwargs.get("custom_aliases", {})

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
            key = alias_to_path(alias=key, custom_aliases=self.custom_aliases)
            if key not in self.path_map_keys:
                raise Exception(
                    "This call is not yet defined. Call 'get_available_calls' method to see the available calls."
                )
            else:
                warn("This method is deprecated. Use 'call' method instead.")
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
        """
        Exports TGT information to a dictionary. Contents are TGT itself, expiration timestamp (tgt_exp) and soft expiration (tgt_exp_0 i.e. expiration if not used) timestamp.
        """
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

    def get_available_calls(self, include_aliases: bool = False):
        """
        Gets all the available calls of eptr2 package. As a reminder, number of calls at eptr2 package might be lower than the actual calls. If include_aliases is set to True, it also includes the aliases.
        """

        if include_aliases:

            return {
                "keys": self.path_map_keys,
                "default_aliases": get_alias_map(),
                "custom_aliases": self.custom_aliases,
            }

        return self.path_map_keys

    def get_aliases(self, include_custom_aliases: bool = False):
        """
        Gets only the aliases. If include_custom_aliases is set to True, it also includes the user defined aliases (custom_aliases).
        """

        alias_d = get_alias_map()
        if include_custom_aliases:
            alias_d.update(self.custom_aliases)

        return alias_d

    def call(self, key: str, **kwargs):
        """
        Main call function for the API. This function is used to process parameters and make calls to EPIAS Transparency API.
        """

        self.check_renew_tgt()
        raw_key = key
        key = alias_to_path(alias=key, custom_aliases=self.custom_aliases)

        if key not in self.path_map_keys:
            if raw_key == key:
                raise Exception(
                    f"This call {raw_key} is not yet defined in calls or aliases. Call 'get_available_calls' method to see the available calls."
                )
            else:
                raise Exception(
                    f"This alias {raw_key} forwarded to key {key} is not yet defined in calls. Call 'get_available_calls' method to see the available calls."
                )

        call_path = get_total_path(key)
        call_method = get_call_method(key)
        required_body_params = get_required_parameters(key)
        call_body_raw = kwargs.pop("call_body", kwargs)

        ### There are some calls requiring special handling, they have a special function to process them
        call_body_raw = process_special_calls(key, call_body_raw)

        ## Parameter change
        # if key in ["bpm-orders", "bpm-orders-w-avg"]:
        #     if "date_time" in call_body_raw.keys():
        #         raise Exception(
        #             f"date_time parameter is not supported for {key}. Use 'date' instead."
        #         )

        # if key in ["ng-vgp-contract-price-summary-period"]:
        #     call_body_raw["is_txn_period"] = False
        # elif key in ["ng-vgp-contract-price-summary-se"]:
        #     call_body_raw["is_txn_period"] = True

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
    """
    Core function to perform the calls and return results. This function is used by the EPTR2 class to make calls to EPIAS Transparency API.
    """

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

    full_url = urljoin(call_phrase, "")
    res = http.request(
        method=call_method,
        url=full_url,
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
