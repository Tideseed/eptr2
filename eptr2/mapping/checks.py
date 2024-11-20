from eptr2.mapping.path import get_path_map
from eptr2.mapping.parameters import get_required_parameters


def check_path_parameter_parity():

    path_keys = get_path_map(just_call_keys=True)
    param_keys = get_required_parameters(
        key="", return_mapping=True, mapping_only_keys=True
    )

    missing_param_keys = [x for x in path_keys if x not in param_keys]
    missing_path_keys = [x for x in param_keys if x not in path_keys]
    if len(missing_param_keys) > 0:
        print("Missing parameters for paths:")
        print(missing_param_keys)
    if len(missing_path_keys) > 0:
        print("Missing paths for parameters:")
        print(missing_path_keys)

    if len(missing_param_keys) == 0 and len(missing_path_keys) == 0:
        print("Path and parameter parity check passed.")
        return True

    return missing_param_keys, missing_path_keys


if __name__ == "__main__":
    check_path_parameter_parity()
