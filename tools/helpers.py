from __future__ import print_function


# this is a printing function for limiting the amount of characters for print
def limited_print(limit=100, *args, d**kwargs):
    if len(args[0]) > limit:
        print(args[0][:limit] + "... (truncated)", *args[1:], **kwargs)
    else:
        print(*args, **kwargs)


