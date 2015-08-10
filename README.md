RegExFilter
===========

A block for filtering incoming signals by regular expression matching.

For performance reasons, this block pre-compiles the regular expression at block configuration time.

Properties
-----------

-   **Pattern (RegEx)**(str): The regular expression against which incoming signals are matched.
-   **Match String**(expr): Evaluated against each signal, emits the match string.
-   **Ignore Case**(bool, default=False): Perform a case insensitive search if True.

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
Every signal is output to either `true` or `false`.

### true

The subset of inbound signals *s* such that *string(s)* matches the configured *pattern*.

### false

The subset of inbound signals *s* such that *string(s)* does not match the configured *pattern*.
