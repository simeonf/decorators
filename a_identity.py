"""
Concepts: What is a decorator? What's up with the @ symbol?

The easiest decorator to make is one that doesn't do anything at all.

The functions in this file are decorated with a non-existent
decorator. Provide an implementation that doesn't do anything at all.

Running the exercise should result in:

    $ python a_identity.py
    [1, 2, 3]

But it doesn't because of that pesky @endpoint decorator. You probably see

    $ python a_identity.py
    Traceback (most recent call last):
      File "a_identity.py", line 18, in <module>
        @endpoint
    NameError: name 'endpoint' is not defined

We don't know what that decorator is supposed to do yet, so implement
a decorator that doesn't add any extra functionality.

"""


@endpoint
def sessions(event_id):
    """Returns the session ids for the event."""
    return [1, 2, 3]


@endpoint
def events():
    """Returns the events to which you have access"""
    return [2717]


if __name__ == "__main__":
    event_id = events()[0]
    print(sessions(event_id))
