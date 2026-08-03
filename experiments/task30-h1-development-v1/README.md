# Task30 H1 development freeze v1

This directory is the tracked, aggregate-only identity of Task30's CSMV H1 development evidence. It is not formal-test evidence and does not authorize Task40.

- `nonsecret-freeze.json` retains the selected teacher/student-v1 configurations, seed-20260802 dev metrics, train-only teacher audit and train-only confidence diagnostic.
- `completion-freeze.json` binds the clean code commit, input hashes, four clean run manifests, same-seed reproducibility, three-seed development stability and the explicit unavailable/evaluation boundaries.
- Private predictions, epoch logs and six selected model states remain only in the Git-ignored local run bundles. Their hashes are retained, but their bytes are prohibited from commit, publication or redistribution.
- The decision is `NOT_PASSED_MECHANISM_NOT_STABLE`; independent 00 review remains required and is not self-approvable by Task30.

Validate without loading restricted data:

```powershell
.\.venv-task30\Scripts\python.exe scripts\validate_task30_completion.py
```
