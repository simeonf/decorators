"""
Concepts. Configurable decorators. Implementing decorators with classes.

Remember this? Our API client just as before (+ inspecting methods for
arguments and adding them as flags).

It should work like:


    $ python f_eliminate_boilerplate.py events
    {'ids': [1, 4]}
    $ python f_eliminate_boilerplate.py sessions --help
    usage: f_eliminate_boilerplate.py sessions [-h] [--event_id EVENT_ID]

    optional arguments:
      -h, --help           show this help message and exit
      --event_id EVENT_ID
    $ python f_eliminate_boilerplate.py sessions --event_id=4
    {'sessions': [{'title': 'Decorator Tutorial'}, {'title': 'Data Science SIG'}]}

But now that we talk to a real (well, imaginary-real) API our endpoints are full
of boilerplate. Wouldn't it be cool if our endpoints looked more like:

    @Endpoint("/sessions/{}.json", args=('event_id'))
    def sessions(self, data):
      return data

    @Endpoint("/events.json")
    def sessions(self, data):
      return data

Can you make our @Endpoint decorator eliminate that duplicate setup code?

For this you need a configurable decorator! That's a callable you can call that
returns a callable that is a decorator. A class returns an object... and an
object is callable if it has a __call__ method... See the Decorator class below
for some ideas.

"""
import argparse
import functools
import inspect
import json
import urllib.request as request

class Endpoint:

    class ApiException(Exception):
        """Exception for error calling API endpoints"""


    def __init__(self, path, args=()):
        self.path = path
        self.args = args
    def __call__(self, f):
        f._endpoint = self
        @functools.wraps(f)
        def wrapper(self, **kwargs):  # Takes self because we're replacing a method but self is RemoteAPI, not Endpoint
            for k, v in kwargs.items():
              if v is None:
                raise f._endpoint.ApiException("Argument {} cannot be empty".format(k))
              if k not in args:
                raise f._endpoint.ApiException("Argument {} not found in args list".format(k))

            auth = self.build_authentication_headers()
            url = self.SERVER + f._endpoint.path
            r = request.Request(url.format(**kwargs), headers=auth)
            with request.urlopen(r) as fp:
              data = json.load(fp)
            return f(self, data)
        return wrapper


def collect(klass):
    for name, val in vars(klass).items():
      if getattr(val, '_endpoint', False):
        klass.ENDPOINTS[name] = val
    return klass



@collect
class RemoteAPI:
    ENDPOINTS = {}
    SERVER = "http://simeonfranklin.com/labs/api"
    def __init__(self, secrets=None):
        # Presumably load some secrets from a file so we can authenticate our client
        pass

    def build_authentication_headers(self):
        """Let's pretend we need to send some headers to be authenticated to our API."""
        return {}

    @Endpoint("/sessions/{event_id}.json", args=('event_id',))
    def sessions(self, data):
        """Returns the session ids for the given event_id."""
        return data['sessions']

    @Endpoint('/events.json')
    def events(self, data):
        """Returns the events to which you have access"""
        return data['ids']


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
        for param in func._endpoint.args:  # We attached the decorator intstance to the method and it has the args
            sub.add_argument("--{}".format(param))

    # Pick a subcommand to run
    args = parser.parse_args()
    if not args.subcommand:
        parser.exit("Please specify a subcommand")
    function = client.ENDPOINTS[args.subcommand]
    call_args = vars(args)
    call_args.pop('subcommand') # remove the subcommand arg, everything left is passed to endpoint
    print(function(client, **call_args))
