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
                print(text[child[0]:child[0]+child[1]])
                nodeStack.append(node.children[child])
                
        


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    test=SuffixTree(text)
    test.print_iterative()