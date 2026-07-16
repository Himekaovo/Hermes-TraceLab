import tempfile
import unittest
from pathlib import Path

from tracelab.phase0 import (
    FeasibilityMatrix,
    FeasibilityStatus,
    ReleaseDecision,
    missing_spike_artifacts,
)


class Phase0DecisionTests(unittest.TestCase):
    def test_full_go_when_binding_path_is_observable_and_replay_is_at_least_partial(self):
        matrix = FeasibilityMatrix(
            f1=FeasibilityStatus.SUPPORTED,
            f2=FeasibilityStatus.SUPPORTED,
            f3=FeasibilityStatus.SUPPORTED,
            f4=FeasibilityStatus.PARTIALLY_SUPPORTED,
        )

        self.assertEqual(matrix.decision(), ReleaseDecision.GO_TOOL_BINDING_MVP)

    def test_conditional_go_when_binding_and_replay_are_only_partial(self):
        matrix = FeasibilityMatrix(
            f1=FeasibilityStatus.SUPPORTED,
            f2=FeasibilityStatus.PARTIALLY_SUPPORTED,
            f3=FeasibilityStatus.SUPPORTED,
            f4=FeasibilityStatus.PARTIALLY_SUPPORTED,
        )

        self.assertEqual(
            matrix.decision(),
            ReleaseDecision.CONDITIONAL_GO_LIFECYCLE_CORRELATION,
        )

    def test_rejected_binding_seam_blocks_binding_detector(self):
        matrix = FeasibilityMatrix(
            f1=FeasibilityStatus.SUPPORTED,
            f2=FeasibilityStatus.REJECTED,
            f3=FeasibilityStatus.SUPPORTED,
            f4=FeasibilityStatus.SUPPORTED,
        )

        self.assertEqual(matrix.decision(), ReleaseDecision.NO_GO_BINDING_DETECTOR)

    def test_rejected_recorder_fidelity_blocks_trusted_diagnosis(self):
        matrix = FeasibilityMatrix(
            f1=FeasibilityStatus.SUPPORTED,
            f2=FeasibilityStatus.SUPPORTED,
            f3=FeasibilityStatus.REJECTED,
            f4=FeasibilityStatus.SUPPORTED,
        )

        self.assertEqual(matrix.decision(), ReleaseDecision.NO_GO_RECORDER_FIDELITY)

    def test_rejected_replay_removes_component_replay_claim(self):
        matrix = FeasibilityMatrix(
            f1=FeasibilityStatus.SUPPORTED,
            f2=FeasibilityStatus.SUPPORTED,
            f3=FeasibilityStatus.SUPPORTED,
            f4=FeasibilityStatus.REJECTED,
        )

        self.assertEqual(matrix.decision(), ReleaseDecision.NO_GO_COMPONENT_REPLAY)

    def test_unknown_identity_or_binding_means_sut_is_not_bound_yet(self):
        matrix = FeasibilityMatrix(
            f1=FeasibilityStatus.UNKNOWN,
            f2=FeasibilityStatus.UNKNOWN,
            f3=FeasibilityStatus.UNKNOWN,
            f4=FeasibilityStatus.UNKNOWN,
        )

        self.assertEqual(matrix.decision(), ReleaseDecision.NO_GO_MISSING_SUT)

    def test_spike_artifact_checker_reports_only_missing_required_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            spike_dir = root / "spike"
            spike_dir.mkdir()
            (spike_dir / "execution-path.md").write_text("present\n")
            (spike_dir / "identity-ownership.md").write_text("present\n")

            self.assertEqual(
                missing_spike_artifacts(root),
                [
                    "spike/instrumentation-seams.md",
                    "spike/f1-f4-results.md",
                    "spike/go-no-go.md",
                ],
            )


if __name__ == "__main__":
    unittest.main()
