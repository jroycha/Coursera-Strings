#Uses python3
import sys

# Return the trie built from patterns
# in the form of a dictionary of dictionaries,
# e.g. {0:{'A':1,'T':2},1:{'C':3}}
# where the key of the external dictionary is
# the node ID (integer), and the internal dictionary
# contains all the trie edges outgoing from the corresponding
# node, and the keys are the letters on those edges, and the
# values are the node IDs to which these edges lead.

class RekeyingError(Exception):
    """
    Raise this exception when Node Class attempts to add another child of the
    same letter
    """
    def __init__(self,key,node_val):
        self.key=key
        self.node_val=node_val
        

class Node:
    def __init__(self,ID):
        self.ID=ID
        self.children=dict()#key=edge letter, value is Node
    def add_child(self,letter,ID):
        if letter in self.children:
            raise RekeyingError(letter,self.children[letter])
        else:
            self.children[letter]=Node(ID)
    def print(self):
        for child in self.children:
            otherID=self.children[child].ID
            print(f'{self.ID}->{otherID}:{child}')
            self.children[child].print()

class Trie:
    def __init__(self,words):
        self.root=Node(0)
        self.num_nodes=0
        for word in words:
            self.addWord(word)
    def addWord(self,word):
        currentNode=self.root
        for letter in word:
            try:#try try to add a child of the current node,
                #if it already exists, skip it, move on down that node
                currentNode.add_child(letter,self.num_nodes+1)
            except RekeyingError as RE:
                currentNode=RE.node_val
                continue
            currentNode=currentNode.children[letter]
            self.num_nodes+=1
    def print(self):
        self.root.print()

                



if __name__ == '__main__':
    patterns = sys.stdin.read().split()[1:]
    tree = Trie(patterns)
    tree.print()
