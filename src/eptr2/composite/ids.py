from eptr2 import EPTR2
from eptr2.composite.periodic_orgs import get_generation_org_and_uevcb_wrapper
import os


def get_all_important_ids(
    the_date: str, export_to_excel: bool = False, main_dir: str = "data", **kwargs
) -> list[int]:
    """Get all relevant ID lists for a given date/period.

    Args:
        the_date (str): The date for which to retrieve relevant UEVCB IDs in 'YYYY-MM-DD' format.
    Returns:
        list[int]: A list of relevant UEVCB IDs.
    """
    verbose = kwargs.get("verbose", False)
    eptr = kwargs.get("eptr", None)
    if eptr is None:
        eptr = EPTR2()

    d = {}

    max_lives = kwargs.get("max_lives", 3)
    retry_kwargs = {
        "retry_attempts": max_lives,
        "retry_backoff": kwargs.get("retry_backoff", 0),
        "retry_backoff_max": kwargs.get("retry_backoff_max", 0),
        "retry_jitter": kwargs.get("retry_jitter", 0.0),
    }

    if verbose:
        print(f"Fetching all important IDs for date: {the_date}")

    if verbose:
        print("Fetching day ahead market participants organization list")
    d["dam_clearing_org_list"] = eptr.call(
        "dam-clearing-org-list",
        period=the_date,
        request_kwargs={"timeout": kwargs.get("timeout", 10)},
        **retry_kwargs,
    )

    if verbose:
        print("Fetching balancing responsible parties list")

    d["imb_org_list"] = eptr.call(
        "imb-org-list",
        start_date=the_date,
        end_date=the_date,
        request_kwargs={"timeout": kwargs.get("timeout", 10)},
        **retry_kwargs,
    )

    if verbose:
        print("Fetching generation organization and UEVCB data")

    d["gen_org_uevcb"] = get_generation_org_and_uevcb_wrapper(
        period=the_date, eptr=eptr, **retry_kwargs
    )

    if verbose:
        print("Fetching power plant list")

    d["pp_list"] = eptr.call(
        "pp-list", request_kwargs={"timeout": kwargs.get("timeout", 10)}, **retry_kwargs
    )

    if verbose:
        print("Fetching UEVM power plant list")

    d["uevm_pp_list"] = eptr.call("uevm-pp-list", **retry_kwargs)

    if export_to_excel:
        import pandas as pd

        os.makedirs(main_dir, exist_ok=True)

        with pd.ExcelWriter(
            os.path.join(main_dir, f"all_important_ids_{the_date}.xlsx")
        ) as writer:
            for key, df in d.items():
                df.to_excel(writer, sheet_name=key, index=False)

    return d
