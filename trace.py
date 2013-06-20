# Copyright 2013 litl, LLC. All Rights Reserved
# coding: utf-8

import contextlib
import functools
import inspect
import sys


def trace_cb(frame, event, arg):
#    print frame, event, arg

    if event == "line":
        print "%s:%d" % (inspect.getfile(frame), frame.f_lineno)

    if event == "return":
        print "locals on return:", frame.f_locals

    return trace_cb


@contextlib.contextmanager
def tracecontext(trace_cb):
    oldtrace = sys.gettrace()
    if oldtrace and oldtrace != trace_cb:
        raise Exception("A trace function is already installed; aborting")

    sys.settrace(trace_cb)
    yield
    sys.settrace(oldtrace)

    if oldtrace is None:
        # This is the highest tracecontext in the stack; dump locals info
        print "Ending a trace"
    


def trace(callable):
    with tracecontext(trace_cb):
        callable()


def tracedecorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with tracecontext(trace_cb):
            return f(*args, **kwargs)

    return wrapper

@tracedecorator
def another():
    print "Another entry"


@tracedecorator
def entry():
    foo = "bar"
    print "Whee"
    print "Whee again"
    another()
