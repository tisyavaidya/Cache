class Node:
    def __init__(self, content):
        self.value = content
        self.next = None
        self.previous = None

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__


class ContentItem:
    '''
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1005, 18, "another header", "111110")
        >>> hash(content1)
        0
        >>> hash(content2)
        1
        >>> hash(content3)
        2
        >>> hash(content4)
        1
    '''
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

    __repr__=__str__

    def __eq__(self, other):
        if isinstance(other, ContentItem):
            return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
        return False

    def __hash__(self):
        '''
        initialising value to 0
        traversing through self.header
            adds ASCII value of letters in header to value
        returns value%3
        '''
        # YOUR CODE STARTS HERE
        value=0
        for i in self.header:
            value+=ord(i)
        return value%3
    



class CacheList:
    ''' 

        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 180, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1006, 18, "another header", "111110")
        >>> content5 = ContentItem(1008, 2, "items", "11x1110")
        >>> lst=CacheList(200)
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> lst.put(content2, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> lst.put(content4, 'mru')
        'INSERTED: CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110'
        >>> lst.put(content5, 'mru')
        'INSERTED: CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110'
        >>> lst.put(content3, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> 1006 in lst
        True
        >>> contentExtra = ContentItem(1034, 2, "items", "other content")
        >>> lst.update(1008, contentExtra)
        'UPDATED: CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content'
        >>> lst
        REMAINING SPACE:170
        ITEMS:3
        LIST:
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        >>> lst.tail.value
        CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA
        >>> lst.tail.previous.value
        CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110
        >>> lst.tail.previous.previous.value
        CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content
        >>> lst.tail.previous.previous is lst.head
        True
        >>> lst.tail.previous.previous.previous is None
        True
        >>> lst.clear()
        'Cleared cache!'
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
    '''
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.maxSize = size
        self.remainingSpace = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)  

    __repr__=__str__

    def __len__(self):
        return self.numItems
    
    def put(self, content, evictionPolicy):
        '''
        if content's size is greater than the maximum size of cache
            returns string "Insertion not allowed"
        if the contents id is already in self
            returns string saying "Content content id already in cache, insertion not allowed"
        while contents size is greater than the remaining space of cahe
            if evictionPolicy passed is mru
                called mruEvict function
            if evictionPolicy is lru
                calls lruEvict function
        if linked list is empty
            creates node of content
            head points to the new node
            tail points to the new node
            number of items increase by 1
            remainingSpace is now equal to maxsize of cache minus size of the new node
            returns a string "Inserted content"
        else
            creates node of content
            previous of head points to new node
            next of new node points to head
            head now points to new node
            number of items increase by 1
            remainingSpace is now equal to maxsize of cache minus size of the new node
            returns a string "Inserted content"
        '''
        
        # YOUR CODE STARTS HERE
        if content.size > self.maxSize:
            return "Insertion not allowed"
        if content.cid in self:
            return f'Content {content.cid} already in cache, insertion not allowed'
        while content.size > self.remainingSpace:
            if evictionPolicy == 'mru':
                self.mruEvict()
            else:
                self.lruEvict()
        if self.head == None:
            node = Node(content)
            self.head = node
            self.tail = node
            self.numItems += 1
            self.remainingSpace -= self.head.value.size
            return f'INSERTED: {content}'
        else:
            node = Node(content)
            self.head.previous = node
            node.next = self.head
            self.head = node
            self.numItems += 1
            self.remainingSpace -= self.head.value.size
            return f'INSERTED: {content}'
        

    def __contains__(self, cid):
        '''
        current stores value of head
        if linked list is empty
            returns False
        else
            while current is not None
                if currents values id is equal to cid
                    if current is head
                        return True
                    elif current is not head or tail
                        prev stores currents previous
                        prev's next is linked to the node after current
                        the node after currents previous is linked to prev
                        temp stores value of self.head
                        currents previous is equal to None
                        currents next is linked to temp
                        self.head is equal to current
                    else if its Tail:
                        tail is initialised to self.tail
                        prev is initialised to the node before tail
                        prev's next is initialised to None
                        self.tail now points to prev
                        tails previous points to None
                        heads previous points to tail
                        head now points to tail
                    returns True
                current becomes next element in linked list
            return False
        '''
        # YOUR CODE STARTS HERE
        current=self.head
        if self.head==None:
            return False
        else:
            while current!=None:
                if current.value.cid==cid:
                    if current.previous==None:
                        return True
                    elif current.next!=None:
                        prev=current.previous
                        prev.next=current.next
                        current.next.previous=prev
                        temp=self.head
                        temp.previous=current
                        current.previous=None
                        current.next=temp
                        self.head=current
                    else:
                        tail=self.tail
                        prev=tail.previous
                        prev.next=None
                        self.tail=prev
                        tail.previous=None
                        tail.next=self.head
                        self.head.previous=tail
                        self.head=tail
                    return True
                current=current.next
            return False
            
        
    def update(self, cid, content):
        '''
        if linked list is empty
            returns string "Cache miss!"
        else
            if cid is in self (calls contain method)
                if the content to be updated size- the original contents size is less than or equal to remaining Space of cache
                    update remaining space of cache to remaining space minus difference between updated contents size and original contents size
                    heads value is initialised to content
                    returns string "UPDATED: content"
                returns string "Cache miss!"
            returns string "Cache miss!"
        '''
        # YOUR CODE STARTS HERE
        if self.head==None:
            return "Cache miss!"
        else:
            if cid in self:
                if content.size-self.head.value.size<=self.remainingSpace:
                    self.remainingSpace-=content.size-self.head.value.size
                    self.head.value=content
                    return f"UPDATED: {str(content)}"
                return "Cache miss!"
            return "Cache miss!"
       

    def mruEvict(self):
        '''
        updates remaining space to remaining space plus the size of content evicted
        reduces numItems by 1
        if numItems is 0
            head points to None
            tail points to None
        else
            currents is initialised to head
            head points to the next element
            heads previous points to None
            currents next points to None
        '''
        # YOUR CODE STARTS HERE
        self.remainingSpace+=self.head.value.size
        self.numItems-=1
        if self.numItems==0:
            self.head=None
            self.tail=None
        else:
            current=self.head
            self.head=self.head.next
            self.head.previous=None
            current.next=None
       

    def lruEvict(self):
        '''
        updates remaining space to remaining space plus the size of content evicted
        reduces numItems by 1
        if numItems is 0
            head points to None
            tail points to None
        else
            current points to tail
            tail points to the element previous to tail
            tails next points to None
            currents previous points to None
        '''
        # YOUR CODE STARTS HERE
        self.remainingSpace+=self.tail.value.size
        self.numItems-=1
        if self.numItems==0:
            self.head=None
            self.tail=None
        else:
            current=self.tail
            self.tail=self.tail.previous
            self.tail.next=None
            current.previous=None
    
    def clear(self):
        '''
        while linked list is not empty
            calls function mruEvict
        returns string "Cleared cache!"
        '''
        # YOUR CODE STARTS HERE
        while len(self)>0:
                self.mruEvict()
        return "Cleared cache!"
            



class Cache:
    """

        >>> cache = Cache()
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1003, 13, "Content-Type: 0", "0xD")
        >>> content3 = ContentItem(1008, 242, "Content-Type: 0", "0xF2")

        >>> content4 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content5 = ContentItem(1001, 51, "Content-Type: 1", "110011")
        >>> content6 = ContentItem(1007, 155, "Content-Type: 1", "10011011")

        >>> content7 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content8 = ContentItem(1002, 14, "Content-Type: 2", "<html><h2>'PSU'</h2></html>")
        >>> content9 = ContentItem(1006, 170, "Content-Type: 2", "<html><button>'Click Me'</button></html>")

        >>> cache.insert(content1, 'lru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'lru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.insert(content3, 'lru')
        'Insertion not allowed'

        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'

        >>> cache.insert(content7, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 18 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'lru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'lru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:177
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:45
        ITEMS:1
        LIST:
        [CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:16
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>]
        <BLANKLINE>
        <BLANKLINE>
        >>> cache[content9].next.value
        CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>
    """

    def __init__(self):
        self.hierarchy = [CacheList(200), CacheList(200), CacheList(200)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__


    def clear(self):
        for item in self.hierarchy:
            item.clear()
        return 'Cache cleared!'

    def insert(self, content, evictionPolicy):
        '''
        hash_value stores the value of __hash__ method of contents object
        value stores the list element of hierarchy at hash_value
        return_str stores the string returned by put method of value object after passing content and evictionPolicy
        returns return_str
        '''
        # YOUR CODE STARTS HERE
        hash_value = content.__hash__()
        value = self.hierarchy[hash_value]
        return_str = value.put(content, evictionPolicy)
        return return_str

    def __getitem__(self, content):
        '''
        hash_value stores the value of __hash__ method of contents object
        if content is already present in self.hierarchy[hash_value]
            returns value of self.hierarchy[hash_value] at head of linked list
        else
            returns string "cache miss!"
        '''
        # YOUR CODE STARTS HERE
        hash_value = content.__hash__()
        if content.cid in self.hierarchy[hash_value]:
            return self.hierarchy[hash_value].head
        else:
            return "Cache miss!"

    def updateContent(self, content):
        '''
        hash_value stores the value of __hash__ method of contents object
        value stores the list element of hierarchy at hash_value
        return_str stores the string returned by update method of value object after passing contents cid and content
        if return_str is "Cache miss!"
            returns the return_str
        else
            returns the linked list value's head's value
        '''
        # YOUR CODE STARTS HERE
        hash_value = content.__hash__()
        value = self.hierarchy[hash_value]
        return_str = value.update(content.cid, content)
        if return_str == "Cache miss!":
            return return_str
        else:
            return value.head.value
        
if __name__ == "__main__":
    print("test")
    import doctest
    doctest.run_docstring_examples(CacheList, globals(), name="Cache", verbose=True)



