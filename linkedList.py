#!/usr/bin/env python

class Node :
  def __init__( self, data ) :
    self.data = data
    self.next = None
    self.prev = None

class LinkedList :
  def __init__( self ) :
    self.head = None    

  def add( self, data ) :
    node = Node( data )
    if self.head == None :  
      self.head = node
    else :
      node.next = self.head
      node.next.prev = node           
      self.head = node      

  def search( self, k ) :
    p = self.head
    if p != None :
      while p.next != None :
        if ( p.data == k ) :
          return p        
        p = p.next
      if ( p.data == k ) :
        return p
    return None

  def length( self ) :
    p = self.head
    count = 0
    if p != None :
      count = count + 1
      while p.next != None :
        count = count + 1
        p = p.next
    return count 


  def remove( self, p ) :
    tmp = p.prev
    p.prev.next = p.next
    p.prev = tmp    

  def __str__( self ) :
    s = ""
    p = self.head
    if p != None :    
      while p.next != None :
        s += p.data
        p = p.next
      s += p.data
    return s

  def deleteNode(self, key):
    temp = self.head
    if (temp is not None):
      if (temp.data == key):
        self.head = temp.next
        temp = None
        return
    
    while(temp is not None):
      if temp.data == key:
        break
      prev = temp
      temp = temp.next


    if(temp == None):
      return
    
    prev.next = temp.next
    temp=None


  def printList(self):
      llist=[]
      temp = self.head
      while(temp):
        print " %s" %(temp.data)
        llist.append(temp.data)
        temp = temp.next

      return llist
        

"""
# Driver program
llist = LinkedList()
llist.add(str(7))
llist.add(str(1))
llist.add(str(3))
llist.add(str(2))
#  
#  print "Created Linked List: "
llist.printList()
llist.deleteNode(str(1)) 
llist.deleteNode(str(3)) 
llist.deleteNode(str(7)) 
print "\nLinked List after Deletion of 1:"
llist.printList()
"""
