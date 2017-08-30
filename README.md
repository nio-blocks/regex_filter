RegExFilter
===========
A block for filtering incoming signals by regular expression matching. For performance reasons, this block pre-compiles the regular expression at block configuration time.

Properties
----------
- **ignore_case**: Perform a case insensitive search if `True`.
- **pattern**: The regular expression against which incoming signals are matched.
- **string**: Evaluated against each signal, emits the match string.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **false**: The subset of inbound signals `s` such that *string(s)* does not match the configured `pattern`.
- **true**: The subset of inbound signals `s` such that *string(s)* matches the configured `pattern`.

Commands
--------
None

Dependencies
------------
None
