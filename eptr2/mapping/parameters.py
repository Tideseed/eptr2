def get_param_label(key):
    d = {
        "start_date": {
            "label": "startDate",
        },
        "end_date": {
            "label": "endDate",
        },
        "date_time": {"label": "date"},
        "date": {"label": "date"},
        "period": {"label": "period"},
        "org_id": {"label": "organizationId"},
        "uevcb_id": {"label": "uevcbId"},
        "imb_org_id": {"label": "organizationId"},
        "region": {"label": "region"},
        "region_id": {"label": "regionId"},
        "pp_id": {"label": "powerPlantId"},
        # "pp_id2": {
        #     "label": "powerplantId"
        # },  ## Because all the other calls use powerPlantId and uevm uses powerplantId (lowercase p)
        # UPDATE: Fixed somewhere else
        "year": {"label": "year"},
        "price_type": {"label": "priceType"},
        "order_type": {"label": "orderType"},
        "message_type_id": {"label": "mesajTipId"},
        "intl_direction": {"label": "direction"},
        "province_id": {"label": "provinceId"},
        "uevcb_name": {"label": "uevcbName"},
        "basin_name": {"label": "basinName"},
        "dam_name": {"label": "damName"},
        "idm_contract_id": {"label": "contractId"},
        "se_date": {"label": ["startDate", "endDate"]},  ## Start-end date
        "dist_org_id": {
            "label": "distrubutionOrganization"
        },  ## TYPO is intentional (same as api)
        "province_id": {"label": "provinceId"},
        "profile_group_id": {"label": "profileGroupId"},
        "distribution_id": {"label": "distributionId"},
        "spg_name": {"label": "subscriberProfileGroupName"},
        "mr_org_id": {"label": "meterReadOrgId"},
        "period_start_date": {"label": "periodStartDate"},
        "period_end_date": {"label": "periodEndDate"},
        "version_start_date": {"label": "versionStartDate"},
        "version_end_date": {"label": "versionEndDate"},
        "is_txn_period": {"label": "isTransactionPeriod"},
        "delivery_year": {"label": "deliveryYear"},
        "delivery_period": {"label": "deliveryPeriod"},
        "point_type": {"label": "pointType"},
        "storage_facility_id": {"label": "storageFacilityId"},
        "point_id": {"label": "pointId"},
    }
    return d.get(key, key)


def get_required_parameters(key):
    d = {
        "mcp": ["start_date", "end_date"],
        "interim-mcp": ["start_date", "end_date"],
        "interim-mcp-status": [],
        "date-init": [],
        "smp": ["start_date", "end_date"],
        "smp-dir": ["start_date", "end_date"],
        "bpm-up": ["start_date", "end_date"],
        "bpm-down": ["start_date", "end_date"],
        "dam-volume": ["start_date", "end_date"],
        "pi-offer": ["start_date", "end_date"],
        "pi-bid": ["start_date", "end_date"],
        "dam-bid": ["start_date", "end_date"],
        "dam-offer": ["start_date", "end_date"],
        "supply-demand": ["date_time"],
        "dam-clearing": ["start_date", "end_date"],
        "dam-clearing-org-list": ["period"],
        "dam-block-bid": ["start_date", "end_date"],
        "dam-block-offer": ["start_date", "end_date"],
        "dam-flexible-matching": ["start_date", "end_date"],
        "dam-flexible-bid": ["start_date", "end_date"],
        "dam-flexible-offer": ["start_date", "end_date"],
        "dam-diff": ["start_date", "end_date"],
        "wap": ["start_date", "end_date"],
        "idm-ob-qty": ["start_date", "end_date"],
        "idm-qty": ["start_date", "end_date"],
        "idm-mm-offer": ["start_date", "end_date"],
        "idm-mm-bid": ["start_date", "end_date"],
        "idm-mm-matching": ["start_date", "end_date"],
        "idm-volume": ["start_date", "end_date"],
        "idm-log": ["start_date", "end_date"],
        "bi-long": ["start_date", "end_date"],
        "bi-short": ["start_date", "end_date"],
        "bi-euas": ["start_date", "end_date"],
        "imb-qty": ["start_date", "end_date"],
        "imb-vol": ["start_date", "end_date"],
        "imb-qty-g": ["start_date", "end_date"],
        "imb-org-list": ["start_date", "end_date"],
        "mcp-smp-imb": ["start_date", "end_date"],
        "bpm-orders-w-avg": ["date"],
        "bpm-orders": ["date"],
        "market-participants": [],
        "market-participants-organization-list": [],
        "kgup": ["start_date", "end_date", "region"],
        "kudup": ["start_date", "end_date", "region"],
        "eak": ["start_date", "end_date", "region"],
        "gen-org": ["start_date", "end_date"],
        "gen-uevcb": ["org_id", "start_date"],
        "rt-gen": ["start_date", "end_date"],
        "uevm": ["start_date", "end_date"],
        "ren-uevm": ["start_date", "end_date"],
        "uecm": ["start_date", "end_date"],
        "su-uecm": ["start_date", "end_date"],
        "st-uecm": ["period"],
        "lic-pp-list": ["start_date", "end_date"],
        "load-plan": ["start_date", "end_date"],
        "rt-cons": ["start_date", "end_date"],
        "pp-list": [],
        "uevm-pp-list": [],
        "ren-pp-list": ["period"],
        "ren-rt-gen": ["start_date", "end_date"],
        "ren-ul-gen": ["start_date", "end_date"],
        "ren-ul-cost": ["start_date", "end_date"],
        "ren-unit-cost": ["start_date", "end_date"],
        "ren-income": ["start_date", "end_date"],
        "ren-lic-cost": ["start_date", "end_date"],
        "ren-total-cost": ["start_date", "end_date"],
        "ren-capacity": ["period"],
        "wind-forecast": ["start_date", "end_date"],
        "ren-participant-list": ["year"],
        "zero-balance": ["start_date", "end_date"],
        "iskk": ["start_date", "end_date"],
        "congestion-cost": ["start_date", "end_date", "price_type", "order_type"],
        "eic-x-org-list": ["period"],
        "eic-w-org-list": ["period"],
        "eic-w-uevcb-list": ["uevcb_name", "period"],
        "mms": ["start_date", "end_date", "region_id"],
        "region-list": [],
        "mms-pp-list": ["start_date"],
        "mms-uevcb-list": ["start_date", "pp_id"],
        "mms-message-type-list": [],
        "mms-region-list": [],
        "international-line-events": ["start_date", "end_date"],
        "tcat-pre-year-forecast": ["start_date", "end_date"],
        "tcat-pre-month-forecast": ["start_date", "end_date"],
        "line-capacities": ["start_date", "end_date", "intl_direction"],
        "intl-direction-list": [],
        "intl-capacity-demand-direction-list": [],
        "capacity-demand": ["start_date", "end_date", "intl_direction"],
        "nominal-capacity": ["start_date", "end_date"],
        "dams-active-fullness": [],
        "dams-daily-level": [],
        "dams-active-volume": [],
        "dams-daily-volume": [],
        "basin-list": [],
        "dam-list": [],
        "dams-level-minmax": [],
        "dams-volume-minmax": [],
        "dams-info": [],
        "dams-water-energy-provision": [],
        "idm-summary": ["start_date", "end_date"],
        "electricity-market-quantity": ["start_date", "end_date"],
        "idm-contract-list": ["se_date"],
        "idm-order-history": ["se_date", "idm_contract_id"],
        "participant-count-based-upon-license-type": ["start_date"],
        "anc-pf-qty": ["start_date", "end_date"],
        "anc-pfk": ["start_date", "end_date"],
        "anc-sf-qty": ["start_date", "end_date"],
        "anc-sfk": ["start_date", "end_date"],
        "distribution-region-list": [],
        "long-term-demand-forecast": [],
        "consumption-breakdown": [
            "period"
        ],  ## This is actually end of month period in the api but it is ok
        "province-list": [],
        "district-list": ["province_id"],
        "profile-group-list": [],
        "consumer-breakdown": ["period"],
        "ra-distribution-list": [],
        "ra-organization-list": [],
        "ra-spg-list": [],
        "ra-vspg-list": [],
        "ra-meters": ["distribution_id", "start_date", "end_date"],
        "ra-meter-volumes-period": [
            "mr_org_id",
            "period_start_date",
            "period_end_date",
        ],
        "ra-meter-volumes-version": [
            "mr_org_id",
            "version_start_date",
            "version_end_date",
        ],
        "ra-sum": ["start_date", "end_date"],
        "ng-participants": [],
        "ng-participant-list": [],
        "ng-balancing-notifications": ["start_date", "end_date"],
        "ng-balancing-price": ["start_date", "end_date"],
        "ng-bast": ["period"],
        "ng-blue-code-ops": ["start_date", "end_date"],
        "ng-daily-match-qty": ["start_date", "end_date"],
        "ng-drp": ["start_date", "end_date"],
        "ng-daily-trade-volume": ["start_date", "end_date"],
        "ng-code-four-ops": ["start_date", "end_date"],
        "ng-gddk": ["start_date", "end_date"],
        "ng-green-code-ops": ["start_date", "end_date"],
        "ng-grp-match-qty": ["start_date", "end_date"],
        "ng-grp-trade-volume": ["start_date", "end_date"],
        "ng-imbalance-amount": ["period"],
        "ng-imbalance-system": ["start_date", "end_date"],
        "ng-latest-settlement-date": [],
        "ng-match-quantity": ["start_date", "end_date"],
        "ng-orange-code-ops": ["start_date", "end_date"],
        "ng-physical-realization": ["start_date", "end_date"],
        "ng-spot-prices": ["start_date", "end_date"],
        "ng-shippers-imbalance-quantity": ["period"],
        "ng-system-direction": ["start_date", "end_date"],
        "ng-total-trade-volume": ["start_date", "end_date"],
        "ng-transaction-history": ["start_date", "end_date"],
        "ng-virtual-realization": ["start_date", "end_date"],
        "ng-weekly-matched-quantity": ["start_date", "end_date"],
        "ng-wrp": ["start_date", "end_date"],
        "ng-weekly-matched-quantity": ["start_date", "end_date"],
        "ng-weekly-trade-volume": ["start_date", "end_date"],
        ## TODO: Need to check, if any of [start_date, end_date] or ["delivery_period","delivery_year"] is required for ng-vgp-contract-price-summary. If so, separate it like ra-meter-volumes-period, ra-meter-volumes-version
        "ng-vgp-contract-price-summary": ["is_txn_period"],
        "ng-vgp-delivery-period": [],
        "ng-vgp-delivery-year": [],
        ## TODO: Same as above
        "ng-vgp-ggf": ["is_txn_period"],
        ## TODO: Same as above
        "ng-vgp-matched-quantity": ["is_txn_period"],
        "ng-vgp-open-positions": ["is_txn_period"],
        "ng-vgp-order-book": [],
        "ng-vgp-transaction-history": ["is_txn_period"],
        "ng-vgp-transaction-volumes": ["is_txn_period"],
        "ng-tr-capacity-point": ["start_date", "end_date", "point_type"],
        "ng-tr-daily-transmission": ["start_date", "end_date"],
        "ng-tr-day-ahead": ["start_date", "end_date"],
        "ng-tr-day-end": ["start_date", "end_date"],
        "ng-tr-entry-nomination": ["start_date", "end_date"],
        "ng-tr-exit-nomination": ["start_date", "end_date"],
        "ng-tr-max-entry-amount": ["start_date", "end_date"],
        "ng-tr-max-exit-amount": ["start_date", "end_date"],
        "ng-tr-actual-entry-amount": ["start_date", "end_date"],
        "ng-tr-actual-exit-amount": ["start_date", "end_date"],
        "ng-tr-reserved-entry-amount": ["start_date", "end_date"],
        "ng-tr-reserved-exit-amount": ["start_date", "end_date"],
        "ng-tr-stock-amount": ["start_date", "end_date"],
        "ng-tr-bilateral-transfer": ["start_date", "end_date"],
    }

    ## UPDATE: As a precaution every call should have an input parameter
    return d.get(key, [])


def get_optional_parameters(key):
    d = {
        "dam-clearing": ["org_id"],
        "bi-long": ["org_id"],
        "bi-short": ["org_id"],
        "imb-qty-g": ["imb_org_id"],
        "market-participants": ["org_id"],
        "kgup": ["org_id", "uevcb_id"],
        "kudup": ["org_id", "uevcb_id"],
        "eak": ["org_id", "uevcb_id"],
        "rt-gen": ["pp_id"],
        "ren-rt-gen": ["pp_id"],
        "uevm": ["pp_id"],
        "eic-x-org-list": ["org_id"],
        "eic-w-org-list": ["org_id"],
        "eic-w-uevcb-list": ["province_id"],
        "mms": ["org_id", "uevcb_id", "pp_id", "message_type_id"],
        "mms-pp-list": ["org_id"],
        "dams-active-fullness": ["basin_name", "dam_name"],
        "dams-daily-level": ["basin_name", "dam_name"],
        "dams-active-volume": ["basin_name", "dam_name"],
        "dams-daily-volume": ["basin_name", "dam_name"],
        "dam-list": ["basin_name"],
        "dams-level-minmax": ["basin_name", "dam_name"],
        "dams-volume-minmax": ["basin_name", "dam_name"],
        "dams-info": ["basin_name", "dam_name"],
        "dams-water-energy-provision": ["basin_name", "dam_name"],
        "long-term-demand-forecast": ["dist_org_id"],
        "consumption-breakdown": ["province_id", "profile_group_id"],
        "consumer-breakdown": ["province_id", "profile_group_id"],
        "idm-qty": ["org_id"],
        "ra-meters": ["ra_spg_name"],
        "ra-meter-volume-period": [
            "ra_spg_name",
            "version_start_date",
            "version_end_date",
        ],
        "ra-meter-volume-version": [
            "ra_spg_name",
            "period_start_date",
            "period_end_date",
        ],
        "ng-participants": ["org_id"],
        "ng-vgp-contract-price-summary": [
            "start_date",
            "end_date",
            "delivery_period",
            "delivery_year",
        ],
        "ng-vgp-ggf": [
            "start_date",
            "end_date",
            "delivery_period",
            "delivery_year",
        ],
        "ng-vgp-matched-quantity": [
            "start_date",
            "end_date",
            "delivery_period",
            "delivery_year",
        ],
        "ng-vgp-open-positions": [
            "start_date",
            "end_date",
            "delivery_period",
            "delivery_year",
        ],
        "ng-tr-daily-transmission": ["storage_facility_id"],
        "ng-tr-max-entry-amount": ["point_id"],
        "ng-tr-max-exit-amount": ["point_id"],
        "ng-tr-actual-entry-amount": ["point_id"],
        "ng-tr-actual-exit-amount": ["point_id"],
        "ng-tr-reserved-entry-amount": ["point_id"],
        "ng-tr-reserved-exit-amount": ["point_id"],
    }

    return d.get(key, [])
