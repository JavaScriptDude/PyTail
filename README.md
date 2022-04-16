### pytail
Tail Implementation In Python (wrapper for *nix tail)

Written to demonstrate how to write a cross platform tool that executes long running sub processes and capturing stderr and stdout in separate code paths for handling.

Although it may seem redundant, it provides an example of automating the processing log files of other processes, like web servers, in python.

This implementation of tail is non-blocking and thus will not interrupt the tool creating or rotating the log file.

To get `tail` for windows that works with this demo, see: https://github.com/JavaScriptDude/cygtail. This should work out of the box with Linux, BSD, Mac.
