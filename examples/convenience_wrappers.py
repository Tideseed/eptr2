from eptr2 import EPTR2
from eptr2.calls import get_mcp, get_ptf


## https://github.com/Tideseed/eptr2/blob/main/src/eptr2/calls.py
eptr = EPTR2()

start_date = "2026-05-03"
end_date = "2026-05-03"

mcp_df = eptr.call("mcp", start_date=start_date, end_date=end_date)

mcp_df_call = get_mcp(start_date=start_date, end_date=end_date)

ptf_df_call = get_ptf(start_date=start_date, end_date=end_date)
print("=====")
print("Regular call")
print("=====")
print(mcp_df)
print("=====")
print("Convenience wrapper call")
print("=====")
print(mcp_df_call)
print("=====")
print("Alias convenience wrapper call")
print("=====")
print(ptf_df_call)
