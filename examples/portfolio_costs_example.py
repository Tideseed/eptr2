from eptr2.composite.plant_costs import calculate_portfolio_costs
import os
import pandas as pd

### Have .env file with EPTR2 API credentials in the current directory ###
main_dir = os.path.join("data", "portfolio_costs_example")

####
## Use the below script to create a template ID dataframe
# from eptr2.composite.plant_costs import create_template_id_df
# create_template_id_df(export_to_excel=True, export_dir=main_dir)
##
####

## Normally you can load your ID dataframe from an Excel or CSV file.
## e.g. id_df = pd.read_excel("path_to_your_file.xlsx")
## Here, for demonstration purposes, we create it manually.

id_df = pd.DataFrame(
    [
        {
            "plant_name": "ÇATALCA RES",
            "org_id": 103420,
            "uevcb_id": 3208554,
            "rt_id": 1216,
            "uevm_id": 610,
            "source": "wind",
        },
        {
            "plant_name": "METRİSTEPE RES",
            "org_id": 103420,
            "uevcb_id": 3218490,
            "rt_id": 776,
            "uevm_id": 5120,
            "source": "wind",
        },
    ]
)

res_d = calculate_portfolio_costs(
    start_date="2026-01-01",
    end_date="2026-01-31",
    id_df=id_df,
    export_dir=main_dir,
    check_existing=False,
    portfolio_name="example_jan_26",
    use_uevm=False,
    translate=True,
    export_to_excel=True,
    verbose=True,
    forecast_source="kgup",
    ignore_org_id=True,
    reduce_cost_details=False,
    use_latest_regulation=False,
)

print("End")
