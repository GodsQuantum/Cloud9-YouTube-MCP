from google.api_core.client_options import ClientOptions
import youtube_mcp.auth.accounts as accounts

_original_build = accounts.build


def _build_with_ipv4_safe_youtube_endpoint(service_name, version, *args, **kwargs):
    """Force YouTube Data v3 through the IPv4-capable Google API frontend.

    In some IPv4-only container networks, youtube.googleapis.com resolves to IPv6-only addresses while this
    container has no usable IPv6 route. www.googleapis.com resolves to IPv4 and
    serves the same youtube/v3 paths from the bundled discovery document.
    Analytics and Reporting keep their upstream endpoints unchanged.
    """
    if service_name == "youtube":
        kwargs["client_options"] = ClientOptions(
            api_endpoint="https://www.googleapis.com/"
        )
    return _original_build(service_name, version, *args, **kwargs)


accounts.build = _build_with_ipv4_safe_youtube_endpoint

from youtube_mcp.cli import (
    _runtime,
    _configure_tool_framework,
    _log_startup_context,
    _import_tool_modules,
)
from youtube_mcp.server import serve

runtime = _runtime()
_configure_tool_framework(runtime)
_import_tool_modules()
_log_startup_context(runtime)
serve(transport="http", host="0.0.0.0", port=8765)
