"""
Concepts: A decorator doesn't have to return the original function. *args and **kwargs.

Decorators often take a callable and return some other callable in its place!

The only trick is that the replacement callable probably needs to
allow being called with the signature of the original callable.

Running the exercise should result in successfully calling some_other_function
every time we think we're calling `no_args`, `one_args`, and so forth.

We should report what arguments were passed to our surprise function:

    $ python d_replacing_decorators.py
    surprise! () {}
    surprise! (10,) {}
    surprise! (10,) {'y': 1}
    surprise! (1, 2, 3) {'y': 10}

But it doesn't work because `some_other_function` doesn't have a signature that
allows it to be called in all those ways. Currently you should see:

    $ python d_replacing_decorators.py
    surprise!
    Traceback (most recent call last):
      File "d_replacing_decorators.py", line 57, in <module>
        one_arg(10)
    TypeError: some_other_function() takes 0 positional arguments but 1 was given

Can you fix `some_other_function` so it can be called any way a function can be called?

Hint: This is simple if you know about *args and **kwargs

"""

def some_other_function():
  print("surprise!")

def replace(f):
  return some_other_function

@replace
def no_args():
    print("No args")

@replace
def one_arg(x):
    print("One arg and it was: {}".format(x))


@replace
def more_args(x, y=None):
    print("One positional arg, one named arg: {}, {}".format(x, y))


@replace
def super_flexible(*args, **kwargs):
    print("Called a variety of ways: {}, {}".format(args, kwargs))

if __name__ == "__main__":
  no_args()
  one_arg(10)
  more_args(10, y=1)
  super_flexible(1, 2, 3, y=10)
