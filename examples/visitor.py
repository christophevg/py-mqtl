# This example illustrates the foundation of the query functionality. A visitor
# behaves as a generator, returning every object in the model along with
# information about its location in the model.

from mqtl.visitor import visit

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
                        Node("up1"),
                        Node("up2")
                      ])
            ),
            Node("right")
          ])
  for link, obj, stack in visit(model):
    if not link: link = "_"
    print "{0}{1}:{2} [{3}]".format("  " * len(stack), link, obj,
                                    ",".join([str(o) for o in stack]))

# output:
#
# _:root []
#   children:left [root]
#     children:left-left [root,left]
#     children:left-mid [root,left]
#     children:left-right [root,left]
#     friend:up [root,left]
#       children:up1 [root,left,up]
#       children:up2 [root,left,up]
#   children:right [root]
