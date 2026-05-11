import subprocess
import sys

def test_dry_run_flag_inverted():
    """Without --dry-run, supervisor should spawn simulated subagent, not dry_run."""
    result = subprocess.run(
        [sys.executable, "supervisor.py", "test query"],
        capture_output=True, text=True, cwd="/home/exedev/autonomy/labs/supervisor-agent"
    )
    output = result.stdout + result.stderr
    # After fixing the bug: without flag it should be simulated
    assert "\"status\": \"simulated\"" in output, f"Expected simulated without flag, got:\n{output[:500]}"

def test_dry_run_flag_respected():
    """With --dry-run, supervisor should return dry_run status."""
    result = subprocess.run(
        [sys.executable, "supervisor.py", "test query", "--dry-run"],
        capture_output=True, text=True, cwd="/home/exedev/autonomy/labs/supervisor-agent"
    )
    output = result.stdout + result.stderr
    assert "\"status\": \"dry_run\"" in output, f"Expected dry_run with --dry-run flag, got:\n{output[:500]}"

if __name__ == "__main__":
    test_dry_run_flag_inverted()
    test_dry_run_flag_respected()
    print("All tests passed")
