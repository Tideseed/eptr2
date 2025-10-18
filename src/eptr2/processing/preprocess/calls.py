def process_special_calls(call_key, param_d):

    if call_key in ["bpm-orders", "bpm-orders-w-avg"]:
        if "date_time" in param_d.keys():
            raise Exception(
                f"date_time parameter is not supported for {call_key}. Use 'date' instead."
            )

    if call_key in [
        "ng-vgp-contract-price-summary-period",
        "ng-vgp-ggf-period",
        "ng-vgp-matched-quantity-period",
        "ng-vgp-open-positions-period",
        "ng-vgp-transaction-history-period",
        "ng-vgp-transaction-volumes-period",
    ]:
        param_d["is_txn_period"] = False
    elif call_key in [
        "ng-vgp-contract-price-summary-se",
        "ng-vgp-ggf-se",
        "ng-vgp-matched-quantity-se",
        "ng-vgp-open-positions-se",
        "ng-vgp-transaction-history-se",
        "ng-vgp-transaction-volumes-se",
    ]:
        param_d["is_txn_period"] = True

    return param_d
