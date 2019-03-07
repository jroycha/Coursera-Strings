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
        self.is_end=False
    def add_child(self,letter,ID):
        if letter in self.children:
            raise RekeyingError(letter,self.children[letter])
        else:
            self.children[letter]=Node(ID)
    def set_end(self):
        self.is_end=True
    def print(self):
        for child in self.children:
            otherID=self.children[child].ID
            print('{}->{}:{}'.format(self.ID,otherID,child))
            self.children[child].print()

from collections import defaultdict


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
        currentNode.set_end()
    def print(self):
        self.root.print()
    def match(self,text):# find occurrences of words in Trie in a text
        pattern_occurrence=defaultdict(list)
        for i in range(len(text)):
            idx=i 
            curNode=self.root
            try:
                while True and curNode.children:
                    curNode=curNode.children[text[idx]]
                    idx+=1
                    if curNode.is_end:
                        pattern_occurrence[text[i:idx]].append(i)
                #pattern_occurrence[text[i:idx]].append(i)
            except KeyError:
                """ we get this error when we search for a trie node that
                isn't present. this is fine, it means we're done looking at
                this growing substring"""
                continue
            except IndexError:
                """this means we went to far in the text. basically, we're
                requiring more text than we have to match a pattern, so again
                we're done with this growing substring"""
                continue
        return pattern_occurrence
                
if __name__ == '__main__':
    text = sys.stdin.readline ().strip ()
    n = int (sys.stdin.readline ().strip ())
    patterns = []
    for i in range (n):
        patterns += [sys.stdin.readline ().strip ()]
    wordTrie=Trie(patterns)
    out=list(wordTrie.match(text).values())
    val_print=[]
    for a in out:
        val_print+=a
    print(*sorted(set(val_print)))
    #sys.stdout.write (' '.join (map (str, ans)) + '\n')
