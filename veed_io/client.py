"""Client for the ``veed/subtitles`` model on fal.ai.

Wraps the ``fal-client`` package. Auth is the ``FAL_KEY`` environment variable
(set it before constructing the client, or pass ``api_key=``).

Two ways to run a job:

  * :meth:`VeedSubtitlesClient.subtitle` — blocking; streams logs; returns a
    :class:`SubtitleResult`. Best for short clips / scripts.
  * :meth:`VeedSubtitlesClient.submit` + :meth:`status` + :meth:`result` — the
    queue API, with optional ``webhook_url``. Best for long videos / servers.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, Optional
from urllib.request import urlopen

from .env import ensure_fal_key
from .models import SubtitleRequest, SubtitleResult
from .pricing import CostEstimate, estimate_cost

MODEL_ID = "veed/subtitles"


class VeedError(RuntimeError):
    """Base error for the veed_io client."""


def _require_fal_client():
    try:
        import fal_client  # type: ignore
    except ImportError as exc:  # pragma: no cover - import guard
        raise VeedError(
            "fal-client is not installed. Run:  pip install fal-client\n"
            "(see veed_io/requirements.txt)"
        ) from exc
    return fal_client


class VeedSubtitlesClient:
    """Thin, typed wrapper over ``fal_client`` for ``veed/subtitles``."""

    def __init__(self, api_key: Optional[str] = None, *, model_id: str = MODEL_ID):
        self.model_id = model_id
        if api_key:
            os.environ["FAL_KEY"] = api_key
        self._fal = _require_fal_client()
        ensure_fal_key()  # best-effort load from veed_io/.env or repo-root .env
        if not os.environ.get("FAL_KEY"):
            raise VeedError(
                "FAL_KEY is not set. Export it or pass api_key=... to the client.\n"
                "  PowerShell:  $env:FAL_KEY = 'your-key'\n"
                "  bash:        export FAL_KEY='your-key'"
            )

    # ----------------------------------------------------------------- files

    def upload_file(self, path: str | Path) -> str:
        """Upload a local file to fal storage and return its public URL."""
        path = Path(path)
        if not path.is_file():
            raise VeedError(f"file not found: {path}")
        return self._fal.upload_file(str(path))

    def download(self, result: SubtitleResult, dest: str | Path) -> Path:
        """Download a finished video to ``dest`` (a file path or directory)."""
        dest = Path(dest)
        if dest.is_dir():
            name = result.file_name or "veed_subtitled.mp4"
            dest = dest / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(result.video_url) as resp, open(dest, "wb") as fh:
            fh.write(resp.read())
        return dest

    # -------------------------------------------------------------- blocking

    def subtitle(
        self,
        request: SubtitleRequest,
        *,
        with_logs: bool = True,
        on_log: Optional[Callable[[str], None]] = None,
    ) -> SubtitleResult:
        """Run a job and block until it completes.

        ``on_log`` (if given) receives each progress log line.
        """
        arguments = request.to_arguments()

        def on_queue_update(update: Any) -> None:
            if on_log and isinstance(update, self._fal.InProgress):
                for entry in update.logs or []:
                    msg = entry.get("message") if isinstance(entry, dict) else str(entry)
                    if msg:
                        on_log(msg)

        response = self._fal.subscribe(
            self.model_id,
            arguments=arguments,
            with_logs=with_logs,
            on_queue_update=on_queue_update if on_log else None,
        )
        return SubtitleResult.from_response(response)

    # ----------------------------------------------------------------- queue

    def submit(
        self, request: SubtitleRequest, *, webhook_url: Optional[str] = None
    ) -> str:
        """Submit a job to the queue and return its ``request_id``."""
        handler = self._fal.submit(
            self.model_id,
            arguments=request.to_arguments(),
            webhook_url=webhook_url,
        )
        return handler.request_id

    def status(self, request_id: str, *, with_logs: bool = True) -> Any:
        """Fetch the current queue status object for ``request_id``."""
        return self._fal.status(self.model_id, request_id, with_logs=with_logs)

    def result(self, request_id: str) -> SubtitleResult:
        """Fetch the completed result for ``request_id``."""
        response = self._fal.result(self.model_id, request_id)
        return SubtitleResult.from_response(response, request_id=request_id)

    # ------------------------------------------------------------- estimate

    @staticmethod
    def estimate(duration_seconds: float, preset: str) -> CostEstimate:
        """Client-side USD cost estimate. See :mod:`veed_io.pricing`."""
        return estimate_cost(duration_seconds, preset)
