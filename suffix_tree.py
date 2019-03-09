# python3
import sys

class RekeyingError(Exception):
    """
    Raise this exception when Node Class attempts to add another child of the
    same letter
    """
    def __init__(self,key,node_val):
        self.key=key
        self.node_val=node_val

class Node:
    def __init__(self):
        self.children=dict()#what kinda key do you use (pos,length)
        self.is_end=False
        self.limit=False
        self.Parent=None
        self.Parent_key=None
    def split(self,key,cut_pos):#key=(pos,len) the key of the next node, i.e. the edge
        word_pos,word_length=key
        newNode=Node()
        newNode.Parent=self
        newNode.Parent_key=(word_pos,cut_pos-word_pos+1)
        self.children[(word_pos,word_length)].Parent=newNode
        self.children[(word_pos,word_length)].Parent_key=(cut_pos+1,word_length+word_pos-cut_pos-1)
        newNode.children[(cut_pos+1,word_length+word_pos-cut_pos-1)]=self.children.pop((word_pos,word_length))
        self.children[(word_pos,cut_pos-word_pos+1)]=newNode
        return newNode
    def add_child(self,pos,length):
        if (pos,length) in self.children:
            raise RekeyingError((pos,length),self.children[key])
        else:
            self.children[(pos,length)]=Node()
            self.children[(pos,length)].Parent=self
            self.children[(pos,length)].Parent_key=(pos,length)
    def print(self,text):
        for child in self.children:
            print(text[child[0]:child[0]+child[1]])
            self.children[child].print(text)
    def set_end(self):
        self.is_end=True
      

from copy import copy

class SuffixTree:
    def __init__(self,text):
        self.root=Node()
        self.text=text
        n=len(text)
        for i in range(len(text)):
            self.add_word(i,n-i)
    def find_child(self,word_pos,parent_node):
        for child in parent_node.children:
            if self.text[child[0]]==self.text[word_pos]:
                return child
        return False
    def add_word(self,word_pos,word_length):
        currentNode=self.root
        while True:
            #self.print()
            edge=self.find_child(word_pos,currentNode)
            if edge:
                min_length=min(word_length,edge[1])
                for i in range(1,min_length):
                    if self.text[edge[0]+i]!=self.text[word_pos+i]:
                        currentNode=currentNode.split(edge,edge[0]+i-1)
                        word_pos+=i
                        word_length-=i
                        currentNode.add_child(word_pos,word_length)
                        currentNode.children[(word_pos,word_length)].set_end()
                        return
                    else:
                        pass
                word_length-=min_length
                if word_length==0:
                    if edge[1]>min_length:
                        currentNode=currentNode.split(edge,edge[0]+min_length-1)
                    else:
                        currentNode=currentNode.children[edge]
                    currentNode.set_end()
                    return
                word_pos+=min_length
                currentNode=currentNode.children[edge]
            else:
                currentNode.add_child(word_pos,word_length)
                currentNode.children[(word_pos,word_length)].set_end()
                return
    def print(self):
        self.root.print(self.text)
    def print_iterative(self):
        root=self.root
        if root is None:
            return
        nodeStack=[root]
        while(len(nodeStack)>0):
            node=nodeStack.pop()
            for child in node.children:
                print(self.text[child[0]:child[0]+child[1]])
                nodeStack.append(node.children[child])
    def min_diff_substring(self):
        octoPos=self.text.find('#')
        stack=[self.process_kids(self.root,octoPos)]
        leafStack=[]
        min_string=self.text[octoPos:]
        while stack:
            #print(1)
            #print('printing stack')
            #for element in stack:
                #print(element[1:])
            currentNode=stack[-1]
            if currentNode[2]: #if you have children who are parents, pop one, add it's info to stack above you
                #print(2)
                newChild=currentNode[2].pop()
                #print(newChild)
                stack.append(self.process_kids(currentNode[0][newChild],octoPos,newChild))
            elif currentNode[1]: #if you have a leaf, add it to the leafStack with a link to it's parentNode
                currentLeaf=currentNode[1].pop()
                leafStack.append([currentLeaf,currentNode[5]])
            else:
                #print(5)
                stack.pop()
                if currentNode[5].limit:
                    #print(6)
                    if currentNode[5].Parent:
                        currentNode[5].Parent.limit=True
        while leafStack:
            #print('in leaf stack')
            currentString,parent=leafStack.pop()
            last_letter=[]
            strCollection=[]
            while parent.limit==False:
                currentString=parent.Parent_key
                parent=parent.Parent
            last_letter=[self.text[currentString[0]]]
            while parent.Parent:
                currentString=parent.Parent_key
                parent=parent.Parent
                strCollection.append(self.text[currentString[0]:currentString[0]+currentString[1]])
            strCollection.reverse()
            new_min_string="".join(strCollection+last_letter)
            if len(new_min_string)<len(min_string):
                min_string=new_min_string
        if min_string==self.text[octoPos:]:
            return False
        else:
            return min_string
    def process_kids(self,node,octoPos,nodeKey=(0,0)):
        leaves=[]
        childParents=[]
        limit=False
        for child in node.children:
            if child[0]==octoPos:
                #node.children.pop(child)
                pass
            elif child[0]<octoPos and child[0]+child[1]==len(self.text):
                leaves.append(child)
            elif child[0]+child[1]==len(self.text):
                limit=True
                node.limit=True
            else:
                childParents.append(child)
        return [node.children, leaves, childParents, limit, nodeKey, node]
        
def all_substrings(word):
    length=len(word)
    return sorted(list(set([word[i:j+1] for i in range(length)
                            for j in range(i,length)])),key =lambda x:len(x))
def naive_min_sub(p,q):
    p_set=all_substrings(p)
    q_set=all_substrings(q)
    matches=[]
    for element in p_set:
        if matches and len(element)>len(matches[-1]):
            break
        if element in q_set:
            pass
        else:
            matches.append(element)
    return matches
from random import choice
from random import randint
def stress_test():
    Alpha=['A','C','G','T']
    while True:
        length=randint(1,18)
        p_list=[]
        q_list=[]
        for _ in range(length):
            p_list+=[choice(Alpha)]
            q_list+=[choice(Alpha)]
        p="".join(p_list)
        q="".join(q_list)
        matches=naive_min_sub(p,q)
        test=SuffixTree(p+'#'+q+'$')
        test_res=test.min_diff_substring()
        if not test_res and not matches:
            print("OK")
        elif  test_res in matches:
            print("OK")
        else:
            print("Incorrect Answer")
            print(p)
            print(q)
            print(test_res)
            print(matches)
            break
        

if __name__ == '__main__':
##    stress_test()
    p = sys.stdin.readline ().strip ()
    q = sys.stdin.readline ().strip ()
    text = p+'#'+q+'$'
    test=SuffixTree(text)
    print(test.min_diff_substring())
    
