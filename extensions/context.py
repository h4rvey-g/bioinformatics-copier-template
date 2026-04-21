from __future__ import annotations

import platform
from functools import lru_cache
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:

    class BaseContextHook:
        update = False

        def hook(self, context: dict[str, Any]) -> dict[str, Any]:
            return context

else:
    try:
        from copier_templates_extensions import ContextHook as BaseContextHook
    except ImportError:  # pragma: no cover - editor/lint fallback when extension pkg isn't importable here

        class BaseContextHook:
            update = False

            def hook(self, context: dict[str, Any]) -> dict[str, Any]:
                return context


@lru_cache(maxsize=1)
def _detect() -> tuple[str, str, list[str]]:
    system = platform.system().lower()
    machine = platform.machine().lower()

    if machine in {"amd64", "x86_64", "x64"}:
        arch = "x86_64"
    elif machine in {"aarch64", "arm64"}:
        arch = "arm64"
    else:
        arch = machine or "unknown"

    if system == "linux":
        if arch == "arm64":
            pixi_platforms = ["linux-aarch64"]
        else:
            pixi_platforms = ["linux-64"]
    elif system == "darwin":
        if arch == "arm64":
            pixi_platforms = ["osx-arm64", "linux-64"]
        else:
            pixi_platforms = ["osx-64", "linux-64"]
    else:
        pixi_platforms = ["linux-64"]

    return system or "unknown", arch, pixi_platforms


class PlatformContext(BaseContextHook):
    update = False

    def hook(self, context: dict[str, Any]) -> dict[str, Any]:
        detected_host_os, detected_host_arch, detected_pixi_platforms = _detect()
        return {
            "detected_host_os": detected_host_os,
            "detected_host_arch": detected_host_arch,
            "detected_pixi_platforms": detected_pixi_platforms,
        }
