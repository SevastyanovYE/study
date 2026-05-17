# AGENTS instructions (repo-wide)

Scope: entire repository.

## Purpose
This repository stores assignments/projects across multiple university subjects.

## Structure rules
- Put cross-subject assets under `common/`.
- Put subject-specific assets under `subjects/<subject>/`.
- Keep reusable agent skills and rules that apply to all subjects in `common/skills/` and `common/rules/`.
- Keep subject-only skills and rules in `subjects/<subject>/skills/` and `subjects/<subject>/rules/`.

## Language/tool policy
- Default implementation language: Go.
- If the task strongly benefits from scientific ecosystem (numerics, plotting, PDE/ODE solvers), Python is allowed and preferred for that subtask.
- MATLAB/Octave can be used when explicitly required by assignment or when parity with provided lab materials is required.

## Plotting policy
- For scientific report plots, prefer Python + Matplotlib with consistent style templates.
- Accept MATLAB/Octave plots when assignment asks for it explicitly.
- If using Go, use plotting only when visual quality remains report-grade.

## Delivery checklist
- Every assignment folder should contain: source code, reproducible run instructions, generated figures, and final report artifacts.
