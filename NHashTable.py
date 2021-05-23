from HashTable import HashTable


class NHashTable(HashTable):
    
    def append(self, keyvalue):
        # address: where we want to store the information
        # through the _hash function
        key, value = keyvalue
        address = self._hash(key)
        
        # insted of a python list, use a Nested Default HT for collisions
        if not self.data[address]:
            if len(self.data) != 1:
                self.data[address] = DefaultNHashTable(int(len(self.data) / 10)+1)
                self.data[address].append((key, value))
            else:
                self.data[address] = [(key, value)]
        else:
            self.data[address].append((key, value))
         
    def get(self, key):
        # find the address of the given key, through the _hash function
        address = self._hash(key)
        
        #return the key in the address HT
        return self.data[address].get(key)

    
class DefaultNHashTable(NHashTable):

    def _hash(self, key):
        """
        Return the hash value of the object (if it has one). Hash values are integers. 
        They are used to quickly compare dictionary keys during a dictionary lookup. 
        Numeric values that compare equal have the same hash value 
        (even if they are of different types, as is the case for 1 and 1.0).
        https://docs.python.org/2/library/functions.html#hash
        """
        return hash(key) % len(self.data)