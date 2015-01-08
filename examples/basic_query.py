# This example illustrates basic query functionality: selecting objects based on
# basic properties.

from mqtl.query import find

class Node(object):
  def __init__(self, name, children=[], friend=None):
    self.name     = name
    self.friend   = friend
    self.children = children
  def __str__(self): return self.name

if __name__ == "__main__":
  model = Node("root", [
            Node("left", [
              Node("left-left"),
              Node("left-mid"),
              Node("left-right")
            ], friend=Node("up", [
                        Node("left"),
                        Node("right")
                      ])
            ),
            Node("right")
          ])

  for _, obj, stack in find(model, withproperties=[("name", "left")]):
    print "{0} [{1}]".format(obj, ",".join([str(o) for o in stack]))

# output:
#
# left [root]
# left [root,left,up]
