def calculate_error_list(
    actual_values: list, forecast_values: list, type: str, return_average=False
):
    if type == "ae":
        error_list = [abs(x - y) for x, y in zip(forecast_values, actual_values)]
    elif type == "bias":
        error_list = [(x - y) for x, y in zip(forecast_values, actual_values)]
    elif type == "pbias":
        error_list = [(x - y) / y for x, y in zip(forecast_values, actual_values)]
    elif type == "ape":
        error_list = [abs((x - y) / y) for x, y in zip(forecast_values, actual_values)]
    elif type == "se":
        error_list = [(x - y) ** 2 for x, y in zip(forecast_values, actual_values)]
    else:
        raise ValueError("type must be one of ae, bias, pbias or ape")

    if return_average:
        return sum(error_list) / len(error_list)

    return error_list


def calculate_wmape(actual_values: list, forecast_values: list):
    if len(actual_values) != len(forecast_values):
        raise ValueError("Actual and forecast values must have the same length")

    wmape = sum(
        calculate_error_list(
            actual_values=actual_values, forecast_values=forecast_values, type="ae"
        )
    ) / sum(actual_values)

    return wmape
