# Defect Log

## D-01 - Implicit product selection on generic PRICE
Found in review. Fixed by requiring explicit/current/stored product for PRICE, QUOTE, DEMO and LEAD. Regression passed.

## D-02 - Single-field contact continuation missed
Found in review. Fixed by detecting any requested contact field. Regression passed.

## D-03 - Stale import artifact
Acceptance parameter comparison found three reverted router lines. Root cause was a container copy made before final review fixes. Correct host artifact was recopied and imported; exact comparison then passed.
