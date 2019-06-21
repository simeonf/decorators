"""
Concepts: identity decorators are a way to have side effects at function definition time.


Here's the same exercise with an argparse CLI addded. The idea is that we
should see a subcommand for each endpoint supported. It should work like:

    $ python b_mark.py --help
    usage: b_mark.py [-h] {events,sessions} ...

    optional arguments:
      -h, --help         show this help message and exit

    Endpoints:
      {events,sessions}  The following endpoints are supported:
        events           Returns the events to which you have access
        sessions         Returns the session ids for the event.
    $ python b_mark.py events
    [2717]
    $ python b_mark.py sessions
    [1, 2, 3]

However currently you probably see:

    $ python b_mark.py --help
    usage: b_mark.py [-h] {} ...

    optional arguments:
      -h, --help  show this help message and exit

    Endpoints:
      {}          The following endpoints are supported:

Go ahead and work on the identity decorator `endpoint` - it really is useful! It
should still return the function it received but it also provides an opportunity
to also store information about which functions were decorated in the ENDPOINTS
dictionary which is expected to be a mapping of `{"name": function}`.

This pattern is super useful any time you need to do function discovery or
registration: eg these functions are tests, these functions are plugins, these
functions are string filters and safe to call in the template, these functions
are "views" and can be routed to, etc etc...

"""
import argparse

ENDPOINTS = {}

def endpoint(f):
    ENDPOINTS[f.__name__] = f
    return f


@endpoint
def sessions(event_id=None):
    """Returns the session ids for the event."""
    return [1, 2, 3]


@endpoint
def events():
    """Returns the events to which you have access"""
    return [2717]



if __name__ == "__main__":
    # Setup CLI options
    parser = argparse.ArgumentParser()
    # Add a subcommand for every endpoint we've implemented
    subparsers = parser.add_subparsers(
        title="Endpoints",
        help="The following endpoints are supported:",
        dest="subcommand",
    )
    # Using inspect to add flags for endpoint arguments ommitted for brevity
    for (name, func) in ENDPOINTS.items():
        sub = subparsers.add_parser(name, help=func.__doc__)

    # Pick a subcommand to run
    args = parser.parse_args()
    if not args.subcommand:
        parser.exit("Please specify a subcommand")
    function = ENDPOINTS[args.subcommand]
    print(function())
