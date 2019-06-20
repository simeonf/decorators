"""
Concepts: you can decorate methods. And classes!

Same thing but for classes. This introduces a new wrinkle when decorating methods.

The problem is that our decorator is invoked as each method is defined - we get
the function that results from the definition.

But to store that function function we're going to need to have access to the
containing class to get to the `ENDPOINTS` class variable... and the class
hasn't been defined when our decorator runs!

We need to defer actually collecting the methods until after the class has been
defined - when it can be done by a class decorator!

Update the `endpoint` decorator to mark decorated methods and then update the
`collect` decorator to loop through the attributes of the class finding the
methods we marked and storing them in the `RemoteAPI.ENDPOINTS` dict.

Hint: help(vars). Also - functions are objects like anything else, open by
default so its totally fine to say `function._my_mark = 1`.

"""
import argparse


def endpoint(f):
    return f


def collect(klass):
    return klass


@collect
class RemoteAPI:
    ENDPOINTS = {}

    def __init__(self, secrets=None):
        # Presumably load some secrets from a file so we can authenticate our client
        pass

    @endpoint
    def sessions(self, event_id=None):
        """Returns the session ids for the event."""
        return [1, 2, 3]

    @endpoint
    def events(self):
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
    client = RemoteAPI()
    # Using inspect to add flags for endpoint arguments ommitted for brevity
    for (name, func) in client.ENDPOINTS.items():
        sub = subparsers.add_parser(name, help=func.__doc__)

    # Pick a subcommand to run
    args = parser.parse_args()
    if not args.subcommand:
        parser.exit("Please specify a subcommand")
    function = client.ENDPOINTS[args.subcommand]

    print(function(client))  # Passing instance of RemoteAPI to self. Do you know why?
