# Defect Log

## D1: Python bytecode committed

The compile test created `scripts/__pycache__`, and the first explicit staging set included it. Containment: remove it from Git and add ignore patterns. Verified absent from the tracked file list. State: accepted.

## D2: repeated patch mismatch on untracked backup script

A cosmetic attempt to add `deploy/` to the recurring staging list failed because the untracked script's generated line layout differed from the expected patch context. After repeated failures, patch-forward stopped. Root-cause review showed deployment files only need initial staging and do not change during daily export. They were staged explicitly for the initial commit. No partial edit occurred. State: accepted.
