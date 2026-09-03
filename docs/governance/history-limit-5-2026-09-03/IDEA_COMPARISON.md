# Idea Comparison

1. Summarize old history with another model call. Rejected because it adds inference load.
2. Reduce the existing SQL history limit from 8 to 5. Selected because it deterministically reduces tokens without adding compute or schema.
