from eptr2 import EPTR2
from eptr2.composite.production import wrapper_hourly_production_plan_and_realized

### Have .env file with EPTR2 API credentials in the current directory ###
eptr = EPTR2()
### Alternative:
# eptr = EPTR2(username="your_username", password="your_password", use_dotenv=False)

id_d = {
    "plant_name": "ÇATALCA RES",
    "org_id": 103420,
    "uevcb_id": 3208554,
    "rt_id": 1216,
    "uevm_id": 610,
    "source": "wind",
}


### With a single composite function call, you can get the hourly production plan (KGÜP V1, KGÜP, KUDÜP) and realized data (real time generation and UEVM, if exists) for a plant, streamlined for your convenience.
result = wrapper_hourly_production_plan_and_realized(
    start_date="2026-01-01",
    end_date="2026-01-31",
    eptr=eptr,
    org_id=id_d["org_id"],
    rt_pp_id=id_d["rt_id"],
    uevcb_id=id_d["uevcb_id"],
    uevm_pp_id=id_d["uevm_id"],
    skip_uevm=True,
    verbose=True,
)

result.to_excel(id_d["plant_name"] + "_production_plan_and_realized.xlsx")
