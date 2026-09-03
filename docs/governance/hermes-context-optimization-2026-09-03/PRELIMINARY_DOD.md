# Preliminary Definition of Done

Success: an optimized draft is saved, exact caps are verified, node/connection counts and credential references are preserved, production remains active on its original version, webhook GET/POST registrations remain unchanged, and a sanitized Git snapshot is pushed.

Failure: import changes production version, workflow registration changes, structure changes outside asserted fields, or rollback cannot restore the original state.

Forbidden: exposing raw workflow secrets, publishing the unavailable Hermes backend, or modifying other workflows.
