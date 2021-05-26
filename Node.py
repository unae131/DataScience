class Node():
    def __init__(self, name, parent = None, branch_name = None):
        self.name = name
        self.parent = parent
        self.isLeaf = True

        if self.parent is not None:
            self.parent.addNodeToBranch(branch_name, self)

    def setBranches(self, branches, attr_range):
        self.branches = {value:None for value in attr_range}
        
        for b in branches:
            self.branches[b] = None

        self.isLeaf = False

    def addNodeToBranch(self, branch_name, node):
        self.branches[branch_name] = node

    def deleteBranches(self, label):
        self.name = label
        self.isLeaf = True
        self.branches = None

    def countNode(self):
        if self.isLeaf == True:
            return 1
        
        count = 1

        for branch in self.branches:
            count += self.branches[branch].countNode()
        
        return count

    def print(self, indent):

        if self.isLeaf == True:
            print(indent + "label: " + self.name)
            return

        print(indent + "name: " +  self.name)

        for branch in self.branches:
            print(indent + "\tbranch: " + branch)
            self.branches[branch].print(indent + "\t")