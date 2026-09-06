"""Input validation for agent-facing entry points.

The CLI and the MCP server are driven by agents that assemble calls from the
machine-readable schema rather than from prose documentation. When their input
is wrong they need an error that names the offending parameter and states the
accepted form, raised *before* any credential or network work happens, and
distinguishable from an upstream failure so the agent knows whether retrying
could ever help.

``EPTR2.call`` already rejects unknown parameters and missing required ones.
What this module adds for the agent surfaces is:

* validation that runs before the client is constructed, so a malformed date
  does not surface as an authentication error;
* date errors that name the parameter and the accepted format instead of
  ``Invalid isoformat string``;
* missing-required errors that say *which* parameters are missing;
* a distinct exception type, so callers can map agent-fixable input errors to
  their own exit codes or structured responses.
"""

from __future__ import annotations

import difflib
from datetime import datetime
from typing import Any, Iterable, Mapping

from eptr2.agentic.discovery import describe_call, search_calls

__all__ = [
    "EptrValidationError",
    "DATE_PARAMS",
    "validate_call_key",
    "validate_date_value",
    "validate_params",
    "validate_call",
]


class EptrValidationError(ValueError):
    """Agent-supplied input is invalid.

    The message is written to be actionable by the caller that produced the
    input. Distinct from the errors raised for upstream/API failures, which are
    not fixable by changing the request.
    """


#: Parameters the library formats as dates/datetimes. Kept in step with
#: ``eptr2.processing.preprocess.params.preprocess_parameter``; ``date_time``
#: is included because it is date-like at the agent surface even though it is
#: not run through the date formatter.
DATE_PARAMS = frozenset(
    {
        "date",
        "date_time",
        "end_date",
        "period",
        "period_end_date",
        "period_start_date",
        "se_date",
        "start_date",
        "version_end_date",
        "version_start_date",
    }
)

_DATE_HINT = (
    "Expected an ISO-8601 date 'YYYY-MM-DD' (e.g. '2026-07-01') or an ISO-8601 "
    "datetime (e.g. '2026-07-01T14:00:00+03:00')."
)


def _norm(name: str) -> str:
    return name.replace("_", "").lower()


def validate_call_key(key: Any) -> str:
    """Return the canonical call key, resolving aliases.

    Raises ``EptrValidationError`` naming close matches when the key is unknown.
    """
    if not isinstance(key, str) or not key.strip():
        raise EptrValidationError(
            "Call key must be a non-empty string. "
            "Use 'eptr2 list' or the get_available_eptr2_calls tool to see valid keys."
        )
    key = key.strip()
    described = describe_call(key)
    if described is not None:
        return described["key"]

    suggestions = sorted(search_calls(key))[:5]
    if not suggestions:
        from eptr2.agentic.discovery import list_calls

        suggestions = difflib.get_close_matches(key, list(list_calls()), n=5, cutoff=0.5)
    hint = f" Did you mean: {', '.join(suggestions)}." if suggestions else ""
    raise EptrValidationError(
        f"Unknown call key '{key}'.{hint} "
        "Use 'eptr2 list' or the get_available_eptr2_calls tool for the full set."
    )


def validate_date_value(field: str, value: Any) -> None:
    """Validate one date-like parameter, naming the field and accepted format."""
    if value is None or isinstance(value, datetime):
        return
    if not isinstance(value, str):
        raise EptrValidationError(
            f"Parameter '{field}' must be a date string or datetime, got "
            f"{type(value).__name__}. {_DATE_HINT}"
        )
    text = value.strip()
    if not text:
        raise EptrValidationError(f"Parameter '{field}' is empty. {_DATE_HINT}")
    try:
        datetime.fromisoformat(text)
    except ValueError as exc:
        extra = ""
        if "/" in text or ("." in text and "T" not in text):
            extra = (
                " Day-first formats such as 'DD/MM/YYYY' or 'DD.MM.YYYY' are not "
                "accepted; reorder to year-month-day."
            )
        raise EptrValidationError(
            f"Parameter '{field}' has an invalid date value {text!r} ({exc})."
            f"{extra} {_DATE_HINT}"
        ) from exc


def validate_params(
    key: str, params: Mapping[str, Any], *, strict_unknown: bool = True
) -> None:
    """Validate parameters for a resolved call key.

    Checks date formats, unknown parameter names (with case/underscore-aware
    suggestions) and missing required parameters. ``key`` must already be
    canonical -- pass the return value of :func:`validate_call_key`.

    ``strict_unknown=False`` mirrors ``EPTR2(strict_params=False)``: parameters
    the endpoint does not accept are left for the client to drop with a warning
    rather than rejected here. Dates, the call key and missing required
    parameters are still validated, because none of those can be recovered by
    dropping a value.
    """
    described = describe_call(key) or {}
    required: Iterable[str] = described.get("required_body_params") or []
    optional: Iterable[str] = described.get("optional_body_params") or []
    accepted = list(required) + list(optional)

    for field, value in params.items():
        if field in DATE_PARAMS:
            validate_date_value(field, value)

    if accepted and strict_unknown:
        normalized = {_norm(p): p for p in accepted}
        unknown = [p for p in params if p not in accepted]
        if unknown:
            suggestions = {}
            for bad in unknown:
                exact = normalized.get(_norm(bad))
                if exact:
                    suggestions[bad] = [exact]
                    continue
                close = difflib.get_close_matches(
                    _norm(bad), list(normalized), n=2, cutoff=0.6
                )
                if close:
                    suggestions[bad] = [normalized[c] for c in close]
            hint = (
                " Did you mean: "
                + "; ".join(f"{k} -> {', '.join(v)}" for k, v in suggestions.items())
                + "."
                if suggestions
                else ""
            )
            raise EptrValidationError(
                f"Call '{key}' does not accept parameter(s) {sorted(unknown)}. "
                f"Accepted parameters: {sorted(accepted)}.{hint}"
            )

    missing = [p for p in required if params.get(p) is None]
    if missing:
        raise EptrValidationError(
            f"Call '{key}' is missing required parameter(s) {sorted(missing)}. "
            f"Required: {sorted(required)}. "
            f"Use 'eptr2 describe {key}' or the describe_eptr2_call tool for details."
        )


def validate_call(
    key: Any, params: Mapping[str, Any], *, strict_unknown: bool = True
) -> str:
    """Validate a key and its parameters together; return the canonical key.

    Intended to run before any client construction or network access, so that
    input errors are reported as input errors rather than as authentication or
    connection failures.
    """
    resolved = validate_call_key(key)
    validate_params(resolved, params, strict_unknown=strict_unknown)
    return resolved
