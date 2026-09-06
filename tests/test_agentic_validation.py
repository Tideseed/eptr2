"""Tests for input validation on the agent-facing entry points.

These cover the failure modes an agent actually produces: a key that does not
exist, a date in the wrong order, a camelCase parameter name, and a required
parameter left out. In each case the point is not only that the call is
rejected, but that the message names what to change.
"""

import pytest

from eptr2.agentic.validation import (
    DATE_PARAMS,
    EptrValidationError,
    validate_call,
    validate_call_key,
    validate_date_value,
    validate_params,
)


class TestCallKey:
    def test_canonical_key_passes_through(self):
        assert validate_call_key("mcp") == "mcp"

    def test_alias_resolves_to_canonical(self):
        assert validate_call_key("ptf") == "mcp"

    def test_surrounding_whitespace_is_tolerated(self):
        assert validate_call_key("  mcp  ") == "mcp"

    def test_unknown_key_names_alternatives(self):
        with pytest.raises(EptrValidationError) as exc:
            validate_call_key("mcp_price")
        message = str(exc.value)
        assert "Unknown call key 'mcp_price'" in message
        assert "Did you mean" in message
        assert "mcp" in message

    @pytest.mark.parametrize("bad", ["", "   ", None, 7])
    def test_non_string_or_empty_is_rejected(self, bad):
        with pytest.raises(EptrValidationError):
            validate_call_key(bad)


class TestDateValues:
    @pytest.mark.parametrize(
        "value",
        ["2026-07-01", "2026-07-01T14:00:00+03:00", "2026-07-01T14:00:00"],
    )
    def test_iso_dates_and_datetimes_accepted(self, value):
        validate_date_value("start_date", value)

    def test_none_is_left_to_the_required_check(self):
        validate_date_value("start_date", None)

    @pytest.mark.parametrize("value", ["06/09/2026", "01.02.2026"])
    def test_day_first_formats_are_called_out(self, value):
        with pytest.raises(EptrValidationError) as exc:
            validate_date_value("start_date", value)
        message = str(exc.value)
        assert "start_date" in message
        assert "Day-first" in message
        assert "YYYY-MM-DD" in message

    def test_impossible_date_names_the_field(self):
        with pytest.raises(EptrValidationError) as exc:
            validate_date_value("end_date", "2026-13-45")
        assert "end_date" in str(exc.value)

    @pytest.mark.parametrize("value", ["", "yesterday", "last week"])
    def test_prose_is_rejected(self, value):
        with pytest.raises(EptrValidationError):
            validate_date_value("start_date", value)

    def test_date_time_is_covered(self):
        ## date_time is date-like at the agent surface even though the library
        ## does not run it through the date formatter.
        assert "date_time" in DATE_PARAMS
        with pytest.raises(EptrValidationError):
            validate_date_value("date_time", "not-a-datetime")


class TestParams:
    def test_valid_combination_passes(self):
        validate_params("mcp", {"start_date": "2026-07-01", "end_date": "2026-07-02"})

    def test_optional_param_accepted(self):
        validate_params(
            "dam-clearing",
            {"start_date": "2026-07-01", "end_date": "2026-07-02", "org_id": 195},
        )

    def test_missing_required_is_named(self):
        with pytest.raises(EptrValidationError) as exc:
            validate_params("mcp", {"start_date": "2026-07-01"})
        message = str(exc.value)
        assert "missing required parameter(s)" in message
        assert "end_date" in message

    def test_unknown_param_lists_accepted_names(self):
        with pytest.raises(EptrValidationError) as exc:
            validate_params(
                "mcp",
                {"start_date": "2026-07-01", "end_date": "2026-07-02", "org_id": 1},
            )
        message = str(exc.value)
        assert "does not accept parameter(s)" in message
        assert "org_id" in message
        assert "start_date" in message  # the accepted list is shown

    def test_camel_case_mixup_is_suggested(self):
        with pytest.raises(EptrValidationError) as exc:
            validate_params(
                "mms",
                {
                    "start_date": "2026-07-01",
                    "end_date": "2026-07-02",
                    "region_id": 1,
                    "ppID": 7,
                },
            )
        message = str(exc.value)
        assert "ppID" in message
        assert "pp_id" in message

    def test_strict_unknown_false_defers_to_the_client(self):
        ## Mirrors EPTR2(strict_params=False): the parameter is left for the
        ## client to drop rather than rejected here.
        validate_params(
            "mcp",
            {"start_date": "2026-07-01", "end_date": "2026-07-02", "org_id": 1},
            strict_unknown=False,
        )

    def test_dates_still_checked_when_unknown_is_relaxed(self):
        ## A dropped parameter is recoverable; a malformed date is not.
        with pytest.raises(EptrValidationError):
            validate_params(
                "mcp",
                {"start_date": "06/09/2026", "end_date": "2026-07-02"},
                strict_unknown=False,
            )

    def test_missing_required_still_checked_when_unknown_is_relaxed(self):
        with pytest.raises(EptrValidationError):
            validate_params(
                "mcp", {"start_date": "2026-07-01"}, strict_unknown=False
            )


class TestValidateCall:
    def test_returns_canonical_key_for_alias(self):
        assert (
            validate_call(
                "ptf", {"start_date": "2026-07-01", "end_date": "2026-07-02"}
            )
            == "mcp"
        )

    def test_key_is_validated_before_params(self):
        ## An unknown key should be reported as such, not as a missing-parameter
        ## error for an endpoint that does not exist.
        with pytest.raises(EptrValidationError) as exc:
            validate_call("no-such-endpoint", {})
        assert "Unknown call key" in str(exc.value)
