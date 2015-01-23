RegExFilter
===========

A block for filtering incoming signals by regular expression matching.

For performance reasons, this block precompiles the regular expression at block configuration time.

Properties
-----------

-   **pattern**(str): The regular expression against which incoming signals are matched.
-   **string**(expr): Evaluated against each signal, emits the match string.
-   **case_sensitive**(bool): Should the matching be case sensitive?

Dependencies
----------------
None

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
The subset of inbound signals *s* such that *string(s)* matches the configured *pattern*.
