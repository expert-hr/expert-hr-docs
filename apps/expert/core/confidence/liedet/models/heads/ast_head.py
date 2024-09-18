from __future__ import annotations

from apps.expert.core.confidence.liedet.models.heads.timesformer_head import (
    TimeSformerHead,
)
from apps.expert.core.confidence.liedet.models.registry import registry


@registry.register_module()
class ASTHead(TimeSformerHead):
    """Similar to TimeSformerHead."""

    pass
