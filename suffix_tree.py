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
    def split(self,key,cut_pos):#key=(pos,len) the key of the next node, i.e. the edge
        word_pos,word_length=key
        newNode=Node()
        newNode.children[cut_pos+1,word_length+word_pos-cut_pos-1]=self.children.pop((word_pos,word_length))
        self.children[(word_pos,cut_pos-word_pos+1)]=newNode
        return newNode
    def add_child(self,pos,length):
        if (pos,length) in self.children:
            raise RekeyingError((pos,length),self.children[key])
        else:
            self.children[(pos,length)]=Node()
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
        min_string=self.text[octoPos:]
        while stack:
            #print(1)
            currentNode=stack[-1]
            if currentNode[2]: #if you have children who are parents, pop one, add it's info to stack above you
                #print(2)
                newChild=currentNode[2].pop()
                stack.append(self.process_kids(currentNode[0][newChild],octoPos,newChild))
            elif currentNode[1]:
                currentLeaf=currentNode[1].pop()
                #print(3)
                n=len(stack)
                i=1
                while stack[n-i][3]==False:#while not limited
                    i+=1
                strList=[self.text[elem[4][0]:elem[4][0]+elem[4][1]] for elem in stack[:n-i+1]]
                if i==1:
                    strList+=[self.text[currentLeaf[0]]]
                else:
                    strList+=[self.text[stack[n-i+1][4][0]]]
                new_min_string=''.join(strList)
                #print(new_min_string)
                #print(min_string)
                if len(min_string)>len(new_min_string):
                    #print(4)
                    min_string=new_min_string
            else:
                #print(5)
                stack.pop()
                if currentNode[3]:
                    #print(6)
                    if stack:
                        stack[-1][3]=True
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
            else:
                childParents.append(child)
        return [node.children, leaves, childParents, limit,nodeKey]
        

if __name__ == '__main__':
    p = sys.stdin.readline ().strip ()
    q = sys.stdin.readline ().strip ()
    text = p+'#'+q+'$'
    test=SuffixTree(text)
    print(test.min_diff_substring())
    
