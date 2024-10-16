class Node(object):
 def __init__(self, parent=None, action=None, state=None, utility=None):
    self.parent = parent
    self.child = []
    self.action = action
    self.state = state
    self.utility = utility