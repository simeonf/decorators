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
import inspect
import json
import urllib.request as request


class Endpoint:
  def __init__(self, endpoint=None, args=None):
    self.endpoint = endpoint
    self.args = args

  def __call__(self, func):
    func._mark = self  # Sure, attach this instance of the decorator to the function
    return func

def collect(klass):
    for name, val in vars(klass).items():
      if getattr(val, '_mark', False):
        klass.ENDPOINTS[name] = val
    return klass

SERVER = "http://simeonfranklin.com/labs/api"

@collect
class RemoteAPI:
    ENDPOINTS = {}

    def __init__(self, secrets=None):
        # Presumably load some secrets from a file so we can authenticate our client
        pass

    def build_authentication_headers(self):
        """Let's pretend we need to send some headers to be authenticated to our API."""
        return {}

    @Endpoint()
    def sessions(self, event_id=1):
        """Returns the session ids for the given event_id."""
        auth = self.build_authentication_headers()
        r = request.Request(SERVER + "/sessions/{}.json".format(event_id), headers=auth)
        with request.urlopen(r) as fp:
          data = json.load(fp)
        return data

    @Endpoint()
    def events(self):
        """Returns the events to which you have access"""
        auth = self.build_authentication_headers()
        r = request.Request(SERVER + "/events.json", headers=auth)
        with request.urlopen(r) as fp:
          data = json.load(fp)
        return data


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
        sig = inspect.signature(func)
        params = set(sig.parameters) - {"self"}  # Ignore self param
        for param in params:  # Any other params get added as flags to the subcommand
            sub.add_argument("--{}".format(param))

    # Pick a subcommand to run
    args = parser.parse_args()
    if not args.subcommand:
        parser.exit("Please specify a subcommand")
    function = client.ENDPOINTS[args.subcommand]
    print(function(client))
