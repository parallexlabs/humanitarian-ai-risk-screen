"""Tests for HTML escaping and URL validation."""

from __future__ import annotations

from ai_risk_screen.security import (
    collect_url_errors,
    escape_html,
    is_safe_https_url,
    validate_url_field,
)


class TestEscapeHtml:
    def test_escapes_script(self) -> None:
        assert escape_html("<script>alert('x')</script>") == (
            "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;"
        )

    def test_escapes_ampersand(self) -> None:
        assert escape_html("Tom & Jerry") == "Tom &amp; Jerry"

    def test_plain_text_unchanged(self) -> None:
        assert escape_html("Hello world") == "Hello world"


class TestUrlValidation:
    def test_valid_https(self) -> None:
        assert is_safe_https_url("https://example.org/path")

    def test_rejects_http(self) -> None:
        assert not is_safe_https_url("http://example.org")

    def test_rejects_javascript(self) -> None:
        assert not is_safe_https_url("javascript:alert(1)")

    def test_rejects_data_uri(self) -> None:
        assert not is_safe_https_url("data:text/html,<script>")

    def test_rejects_protocol_relative(self) -> None:
        assert not is_safe_https_url("//example.org/path")

    def test_rejects_empty(self) -> None:
        assert not is_safe_https_url("")

    def test_validate_url_field_optional_empty(self) -> None:
        assert validate_url_field(None, "test") == []
        assert validate_url_field("", "test") == []

    def test_validate_url_field_rejects_bad(self) -> None:
        errors = validate_url_field("javascript:void(0)", "meta.reference_url")
        assert len(errors) == 1
        assert "meta.reference_url" in errors[0]

    def test_collect_url_errors_in_document(self) -> None:
        data = {
            "meta": {"reference_url": "https://good.example.org"},
            "steps": {"tool": {"vendor_url": "javascript:bad()"}},
        }
        errors = collect_url_errors(data)
        assert len(errors) == 1
        assert "vendor_url" in errors[0]
