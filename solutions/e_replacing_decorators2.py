"""
Concepts: functional closures for implementing original + new behavior. functools.wraps

Let's take this one step further: what if we want to do something with the
arguments in some way but still call the original function to do what the
original function does?

The identity decorator won't help us here - we need to replace the original
function with a new function that accepts the arguments, does something with
them, then calls the original function. It also needs to "just know" what
function it is replacing since that info won't be passed in.

One way is to use a functional closure - nested function definitions and access
to the enclosing functions' scope let each new definition of `wrapper` remember
which function it is replacing.

This works as is - but I'm unhappy that now I can see the `wrapper` function
when I think I'm looking at the functions we decorated.

    $ python e_replacing_decorators2.py
    LOG:  (10,) {}
    One arg and it was: 10
    LOG:  (1, 2, 3) {'y': 10}
    Called a variety of ways: (1, 2, 3), {'y': 10}
    Access metadata for <function replace.<locals>.wrapper at 0x1031b1ae8>
    None

Fix this with functools.wraps! Look at the help if you've never used `wraps`.

"""
import inspect
import functools

def replace(f):
  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    print("LOG: ", args, kwargs)
    return f(*args, **kwargs)
  return wrapper
  # wrapper = functools.wraps(f)(wrapper)

@replace
def one_arg(x):
    "Function of one argument"
    print("One arg and it was: {}".format(x))


@replace
def super_flexible(*args, **kwargs):
    print("Called a variety of ways: {}, {}".format(args, kwargs))

if __name__ == "__main__":
  one_arg(10)
  super_flexible(1, 2, 3, y=10)
  print("Access metadata for {}".format(one_arg))
  print(inspect.getdoc(one_arg))
