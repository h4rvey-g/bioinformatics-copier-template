from __future__ import annotations

import getpass
import platform
import shutil
import subprocess
from collections import defaultdict
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


_MANUAL_CHOICE = "__manual__"
_NULL_GRES_VALUES = {"", "(null)", "null", "n/a"}


def _choice(label: str, value: str) -> list[str]:
    return [label, value]


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique_values.append(value)
    return unique_values


def _split_top_level_commas(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0

    for char in value:
        if char == "(":
            depth += 1
        elif char == ")" and depth > 0:
            depth -= 1

        if char == "," and depth == 0:
            token = "".join(current).strip()
            if token:
                parts.append(token)
            current = []
            continue

        current.append(char)

    token = "".join(current).strip()
    if token:
        parts.append(token)
    return parts


def _gpu_request_from_gres_token(token: str) -> str | None:
    core = token.strip().split("(", 1)[0].strip()
    if not core or core.lower() in _NULL_GRES_VALUES:
        return None

    parts = [part for part in core.split(":") if part]
    if not parts or parts[0] != "gpu":
        return None

    tail = parts[1:]
    if tail and tail[-1].isdigit():
        tail = tail[:-1]

    if not tail:
        return "gpu:1"

    return f"gpu:{':'.join(tail)}:1"


def _gpu_requests_from_gres(gres: str) -> list[str]:
    requests = [
        request
        for request in (_gpu_request_from_gres_token(token) for token in _split_top_level_commas(gres))
        if request is not None
    ]
    return _unique_preserve_order(requests)


def _build_gres_choices(requests: list[str], *, add_generic_fallback: bool = False) -> list[list[str]]:
    choices = [_choice("Do not set --gres (configure later)", "")]

    if requests:
        choices.extend(_choice(f"--gres={request}", request) for request in requests)
    elif add_generic_fallback:
        choices.append(_choice("--gres=gpu:1", "gpu:1"))

    choices.append(_choice("Other (enter manually)", _MANUAL_CHOICE))
    return choices


def _detect_slurm() -> dict[str, Any]:
    partitions: list[str] = []
    gpu_partitions: list[str] = []
    gpu_requests_all: list[str] = []
    gpu_requests_by_partition: dict[str, list[str]] = defaultdict(list)
    default_partition = ""
    sinfo_detected = False

    sinfo = shutil.which("sinfo")
    if sinfo:
        try:
            result = subprocess.run(
                [sinfo, "-h", "-o", "%P|%G"],
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            result = None
        else:
            sinfo_detected = True

        if result is not None:
            for raw_line in result.stdout.splitlines():
                line = raw_line.strip()
                if not line or "|" not in line:
                    continue

                raw_partition, raw_gres = line.split("|", 1)
                raw_partition = raw_partition.strip()
                if not raw_partition:
                    continue

                is_default = raw_partition.endswith("*")
                partition = raw_partition.rstrip("*").strip()
                if not partition:
                    continue

                if partition not in partitions:
                    partitions.append(partition)
                if is_default and not default_partition:
                    default_partition = partition

                gpu_requests = _gpu_requests_from_gres(raw_gres)
                if gpu_requests and partition not in gpu_partitions:
                    gpu_partitions.append(partition)

                for request in gpu_requests:
                    if request not in gpu_requests_by_partition[partition]:
                        gpu_requests_by_partition[partition].append(request)
                    if request not in gpu_requests_all:
                        gpu_requests_all.append(request)

    if not partitions:
        partitions = ["compute"]
        default_partition = "compute"
    elif not default_partition:
        default_partition = partitions[0]

    partition_choices = [_choice(partition, partition) for partition in partitions]
    partition_choices.append(_choice("Other (enter manually)", _MANUAL_CHOICE))

    gpu_partition_choices = [_choice("Use default partition / no dedicated GPU partition", "")]
    if gpu_partitions:
        gpu_partition_choices.extend(_choice(partition, partition) for partition in gpu_partitions)
    else:
        gpu_partition_choices.append(_choice("gpu", "gpu"))
    gpu_partition_choices.append(_choice("Other (enter manually)", _MANUAL_CHOICE))

    gpu_gres_choices_by_partition = {
        partition: _build_gres_choices(requests)
        for partition, requests in gpu_requests_by_partition.items()
    }

    return {
        "detected_sinfo_available": sinfo_detected,
        "detected_slurm_partitions": partitions,
        "detected_slurm_partition_values": partitions,
        "detected_default_slurm_partition": default_partition,
        "detected_slurm_partition_choices": partition_choices,
        "detected_slurm_gpu_partitions": gpu_partitions,
        "detected_slurm_gpu_partition_values": gpu_partitions,
        "detected_slurm_gpu_partition_choices": gpu_partition_choices,
        "detected_slurm_gpu_gres_values_by_partition": dict(gpu_requests_by_partition),
        "detected_slurm_gpu_gres_choices_by_partition": gpu_gres_choices_by_partition,
        "detected_slurm_gpu_gres_values": gpu_requests_all,
        "detected_slurm_gpu_gres_choices": _build_gres_choices(gpu_requests_all, add_generic_fallback=True),
    }


@lru_cache(maxsize=1)
def _detect() -> dict[str, Any]:
    system = platform.system().lower()
    machine = platform.machine().lower()
    username = getpass.getuser()

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

    return {
        "detected_host_os": system or "unknown",
        "detected_host_arch": arch,
        "detected_pixi_platforms": pixi_platforms,
        "detected_username": username or "unknown",
        **_detect_slurm(),
    }


class PlatformContext(BaseContextHook):
    update = False

    def hook(self, context: dict[str, Any]) -> dict[str, Any]:
        return _detect()
