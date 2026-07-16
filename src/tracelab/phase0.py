from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, List


class FeasibilityStatus(str, Enum):
    """Allowed Phase 0 F1-F4 feasibility states."""

    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class ReleaseDecision(str, Enum):
    """Release gate decisions derived from Phase 0 findings."""

    GO_TOOL_BINDING_MVP = "GO_TOOL_BINDING_MVP"
    CONDITIONAL_GO_LIFECYCLE_CORRELATION = "CONDITIONAL_GO_LIFECYCLE_CORRELATION"
    NO_GO_BINDING_DETECTOR = "NO_GO_BINDING_DETECTOR"
    NO_GO_RECORDER_FIDELITY = "NO_GO_RECORDER_FIDELITY"
    NO_GO_COMPONENT_REPLAY = "NO_GO_COMPONENT_REPLAY"
    NO_GO_MISSING_SUT = "NO_GO_MISSING_SUT"
    NO_GO_FEASIBILITY = "NO_GO_FEASIBILITY"


REQUIRED_SPIKE_ARTIFACTS = (
    "spike/execution-path.md",
    "spike/identity-ownership.md",
    "spike/instrumentation-seams.md",
    "spike/f1-f4-results.md",
    "spike/go-no-go.md",
)


@dataclass(frozen=True)
class FeasibilityMatrix:
    """Phase 0 F1-F4 result matrix."""

    f1: FeasibilityStatus
    f2: FeasibilityStatus
    f3: FeasibilityStatus
    f4: FeasibilityStatus

    def decision(self) -> ReleaseDecision:
        if self._has_unknown_core_path():
            return ReleaseDecision.NO_GO_MISSING_SUT

        if self.f3 == FeasibilityStatus.REJECTED:
            return ReleaseDecision.NO_GO_RECORDER_FIDELITY

        if self.f2 == FeasibilityStatus.REJECTED:
            return ReleaseDecision.NO_GO_BINDING_DETECTOR

        if self.f4 == FeasibilityStatus.REJECTED:
            return ReleaseDecision.NO_GO_COMPONENT_REPLAY

        if (
            self.f1 == FeasibilityStatus.SUPPORTED
            and self.f2 == FeasibilityStatus.SUPPORTED
            and self.f3 == FeasibilityStatus.SUPPORTED
            and self.f4
            in {
                FeasibilityStatus.SUPPORTED,
                FeasibilityStatus.PARTIALLY_SUPPORTED,
            }
        ):
            return ReleaseDecision.GO_TOOL_BINDING_MVP

        if (
            self.f1 == FeasibilityStatus.SUPPORTED
            and self.f2 == FeasibilityStatus.PARTIALLY_SUPPORTED
            and self.f3 == FeasibilityStatus.SUPPORTED
            and self.f4 == FeasibilityStatus.PARTIALLY_SUPPORTED
        ):
            return ReleaseDecision.CONDITIONAL_GO_LIFECYCLE_CORRELATION

        return ReleaseDecision.NO_GO_FEASIBILITY

    def _has_unknown_core_path(self) -> bool:
        return self.f1 == FeasibilityStatus.UNKNOWN or self.f2 == FeasibilityStatus.UNKNOWN


def missing_spike_artifacts(root: Path, required: Iterable[str] = REQUIRED_SPIKE_ARTIFACTS) -> List[str]:
    """Return required Phase 0 spike files that do not exist under root."""

    return [artifact for artifact in required if not (root / artifact).is_file()]
