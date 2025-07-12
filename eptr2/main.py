from typing import Any
import urllib3
import re
import os
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
    get_derived_calls,
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
        credentials_file_path: str | None = None,
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

        ### Credentials and Login
        self.username = username
        self.password = password
        self.is_test = kwargs.get("is_test", False)  ## Currently not used
        self.credentials_file_path = credentials_file_path
        # self.credentials_file_path = kwargs.get("credentials_file_path", None)
        self.login(custom_root_phrase=kwargs.get("root_phrase", None))

        if tgt_d is not None:
            self.import_tgt_info(tgt_d)
        else:
            self.tgt = None
            self.tgt_exp = 0
            self.tgt_exp_0 = 0

        self.check_renew_tgt()

        ## Path map keys and custom aliases
        self.path_map_keys = get_path_map(just_call_keys=True)
        self.custom_aliases = kwargs.get("custom_aliases", {})

    def login(self, custom_root_phrase: str | None = None):
        if self.username is None or self.password is None:
            if self.credentials_file_path is not None:
                with open(self.credentials_file_path, "r") as f:
                    credentials_d = json.load(f)
                    self.username = credentials_d["EPTR_USERNAME"]
                    self.password = credentials_d["EPTR_PASSWORD"]
            else:
                self.username = os.environ.get("EPTR_USERNAME", None)
                self.password = os.environ.get("EPTR_PASSWORD", None)

        if self.username is None or self.password is None:
            raise Exception(
                "Username and password must be provided for login. If you do not have the necessary credentials, you can get them from EPIAS Transparency Platform website."
            )

        if not custom_root_phrase:
            root_phrase_test = "-prp" if self.is_test else ""
            root_phrase_default = f"https://seffaflik{root_phrase_test}.epias.com.tr"
            self.root_phrase = root_phrase_default

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
            raise Exception("Username and password must be provided for tgt renewal.")

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
        self.tgt_exp = (tgt_start_time + timedelta(hours=1, minutes=45)).timestamp()

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

    def get_number_of_calls(self):
        """
        List the number of calls in the package. It also lists the number of derived calls and API calls (excluding derived calls).
        """

        d = {
            "all_calls": self.path_map_keys,
            "derived_calls": get_derived_calls(),
        }
        d["n_total_calls"] = len(d["all_calls"])
        d["n_derived_calls"] = len(d["derived_calls"])
        d["n_api_calls"] = len(d["all_calls"]) - len(d["derived_calls"])

        return d

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


def set_eptr_credentials_to_env(cred_path: str = "creds/eptr_credentials.json"):
    """Set EPTR credentials to environment variables from a JSON file."""

    if not os.path.exists(cred_path):
        raise FileNotFoundError(
            f"Credentials file not found at {cred_path}. Please provide a valid path or put your eptr_credentials.json file there."
        )

    try:
        with open(cred_path, "r") as f:
            cred_d: dict = json.load(f)

        os.environ["EPTR_USERNAME"] = cred_d["EPTR_USERNAME"]
        os.environ["EPTR_PASSWORD"] = cred_d["EPTR_PASSWORD"]
        if "tgt_d" in cred_d.keys():
            os.environ["tgt_d"] = json.dumps(cred_d["tgt_d"])
    except Exception as e:
        raise ValueError(
            f"Error while reading the credentials file from path {cred_path}. Please check the file format and content. Error: {e}"
        ) from e


def eptr_w_tgt_wrapper(
    cred_path: str = "creds/eptr_credentials.json", **kwargs
) -> EPTR2:
    """This function is a wrapper for the EPTR2 class to handle TGT (Ticket Granting Ticket) management and credentials loading. This way TGT is automatically renewed when it expires, and credentials are loaded from a file or environment variables."""

    ### Initially you can define EPTR_USERNAME and EPTR_PASSWORD in the keyword arguments (strictly optional) and even tgt_d optional parameter. It is not a conventional use of this function.
    username = kwargs.get("EPTR_USERNAME", None)
    password = kwargs.get("EPTR_PASSWORD", None)
    tgt_d = None

    ### If username and password are not defined in the keyword arguments, try to get them from the environment variables.
    if username is not None:
        os.environ["EPTR_USERNAME"] = username
    else:
        username = os.getenv("EPTR_USERNAME", None)
    if password is not None:
        os.environ["EPTR_PASSWORD"] = password
    else:
        password = os.getenv("EPTR_PASSWORD", None)

    ### Check for EPTR_USERNAME and EPTR_PASSWORD in the environment variables. If they are not set, try to get them from the credentials file.
    if any([k is None for k in [username, password]]):
        set_eptr_credentials_to_env(cred_path)
        username = os.getenv("EPTR_USERNAME", None)
        password = os.getenv("EPTR_PASSWORD", None)
        tgt_d = os.getenv("tgt_d", None)
        if tgt_d is not None:
            tgt_d = json.loads(tgt_d)
    else:
        tgt_d = kwargs.get("tgt_d", None)
        if tgt_d is not None:
            os.environ["tgt_d"] = json.dumps(tgt_d)

        if tgt_d is None:
            tgt_d = os.getenv("tgt_d", None)
            if tgt_d is not None:
                tgt_d = json.loads(tgt_d)

    ### Check for EPTR_USERNAME and EPTR_PASSWORD in the environment variables. If they are not set, raise an error. (Sanity check)

    if any([k is None for k in [username, password]]):
        raise ValueError(
            "EPTR_USERNAME and/or EPTR_PASSWORD is not set in the environment variables. They are also not acquired from the credentials file."
        )

    eptr = EPTR2(
        username=username,
        password=password,
        tgt_d=tgt_d,
    )

    if kwargs.get("skip_tgt_update", False):
        return eptr

    ### Export the tgt information and check with the existing one. If they are different, update the environment variables and the credentials file.
    tgt_d2 = eptr.export_tgt_info()

    if tgt_d != tgt_d2:
        os.environ["tgt_d"] = json.dumps(tgt_d2)

        if all([x in os.environ.keys() for x in ["EPTR_USERNAME", "EPTR_PASSWORD"]]):
            with open(cred_path, "w") as f:
                json.dump(
                    {
                        "EPTR_USERNAME": os.getenv("EPTR_USERNAME", None),
                        "EPTR_PASSWORD": os.getenv("EPTR_PASSWORD", None),
                        "tgt_d": tgt_d2,
                    },
                    f,
                )
        else:
            print(
                "EPTR_USERNAME and/or EPTR_PASSWORD are not set in the environment variables. Credentials file is not updated."
            )

    return eptr


def generate_eptr2_credentials_file(
    username: str = "YOUR_USERNAME",
    password: str = "YOUR_PASSWORD",
    cred_path: str = "creds/eptr_credentials.json",
    overwrite: bool = False,
):
    """Generate a credentials file for EPTR2 class. It creates a JSON file with EPTR_USERNAME and EPTR_PASSWORD."""

    if not overwrite and os.path.exists(cred_path):
        print(
            f"Credentials file already exists at {cred_path}. Use overwrite=True to overwrite."
        )
        return

    if not os.path.exists(os.path.dirname(cred_path)):
        os.makedirs(os.path.dirname(cred_path))

    cred_d = {
        "EPTR_USERNAME": username,
        "EPTR_PASSWORD": password,
    }

    with open(cred_path, "w") as f:
        json.dump(cred_d, f)

    print(f"Credentials file created at {cred_path}.")
