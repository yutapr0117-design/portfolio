# ALife Research Package: Autonomous Commons (Physarum Trace)

This is a minimal research package structured according to the `OpenLife Research Package Protocol v0.1`.

## Core Concept
This package provides a deterministic/statistical reproduction of the **Physarum (Slime Mold) trace deposition model**. It serves as structural evidence of metabolism and environmental reaction (Hybrid Agency), proving that the agent's habitat can process traces and reach statistical stability (R5S) across multiple executions.

## Execution
- **Quick Test:** `./quicktest.sh` (Runs a fast headless trace simulation, < 1 min)
- **Full Reproduction:** `./reproduce.sh` (Runs multi-seed validation)

## File Structure
- `openlife.yaml`: Package manifest.
- `claims.yaml`: Machine-readable claims of statistical reproducibility.
- `src/simulate.py`: Headless python simulation for ALife tracing.
- `human_intervention.md`: Log of external/human interference.
- `limitations.md`: Boundaries of the current simulation.
