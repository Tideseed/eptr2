from eptr2.composite import get_ancillary_reserve_data

df = get_ancillary_reserve_data(
    start_date="2026-01-01",
    end_date="2026-01-02",
    verbose=True,
)
