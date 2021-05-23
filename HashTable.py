import hashlib
import struct
import sys

"""
Hash Tables implementations
"""


class HashTable():

    def __init__(self, size):
        #initiliaze the data array
        self.data = [None] * size
    
    # O(1)
    def add(self, key, value):
        # address: where we want to store the information
        # through the _hash function
        address = self._hash(key)
        
        # if the space in address is still empty, assign 'value'
        if not self.data[address]:
            self.data[address] = [(key, value)]
        else:
            self.data[address].append((key, value))
    
    # If no collision: O(1)
    def get(self, key):
        # find the address of the given key, through the _hash function
        address = self._hash(key)    
        current_list = self.data[address]
        
        # if there is something at this address return saved value
        if current_list:
            # Loop over the items saved at address
            # O(N) worst case with collisions
            for i in range(len(current_list)):
                if current_list[i][0] == key:
                    return current_list[i][1]
            raise Exception("Key not found")
        else:
            raise Exception("Key not found")

            
    # iterate over the saved keys on our Hash Table
    # That's a drawback of hashtables, we have to loop over 
    # each space even if it's empty and they are unordered
    def keys(self):
        keys_array = []
        
        # loop over the spaces of self.data 
        for i in range(len(self.data)):
            # if array is saved in space, loop over and append keys
            if self.data[i]:
                
                if len(self.data[i]) > 1:
                    for j in range(len(self.data[i])):
                        keys_array.append(self.data[i][j][0])
                else:
                    keys_array.append(self.data[i][0][0])
        
        return keys_array
    

        
class NaiveHashTable(HashTable):

    def _hash(self, key):
        assert (type(key) == str or type(key) == int or type(key) == float), "Key type not allowed"
        if type(key) == str:
            hash_value = 0
            for i in range(len(key)):
                hash_value = (hash_value + ord(key[i]) * i) % len(self.data)
            return hash_value
        else:
            return int(key) % len(self.data)
        
        
class DefaultHashTable(HashTable):

    def _hash(self, key):
        """
        Return the hash value of the object (if it has one). Hash values are integers. 
        They are used to quickly compare dictionary keys during a dictionary lookup. 
        Numeric values that compare equal have the same hash value 
        (even if they are of different types, as is the case for 1 and 1.0).
        https://docs.python.org/2/library/functions.html#hash
        """
        return hash(key) % len(self.data)
    
    
class MD5HashTable(HashTable):

    def _hash(self, key):
        if type(key) == str:
            md5_hash_hex = hashlib.md5(key.encode()).hexdigest()
        elif type(key) == int:
            md5_hash_hex = hashlib.md5(struct.pack('<i', key)).hexdigest()
        elif type(key) == float:
            md5_hash_hex = hashlib.md5(struct.pack('<f', key)).hexdigest()
        return int(md5_hash_hex, 16) % len(self.data)
    
    
class SHA256HashTable(HashTable):

    def _hash(self, key):
        md5_hash_hex = hashlib.sha256(key.encode()).hexdigest()
        return int(md5_hash_hex, 16) % len(self.data)
    
    
class JenkinsHashTable(HashTable):
    
    # -*- coding: utf-8 -*-
    # Need to constrain U32 to only 32 bits using the & 0xFFFFFFFF
    # since Python has no native notion of integers limited to 32 bit
    # http://docs.python.org/library/stdtypes.html#numeric-types-int-float-long-complex
    """Original copyright notice:
        By Bob Jenkins, 1996.  bob_jenkins@burtleburtle.net.  You may use this
        code any way you wish, private, educational, or commercial. Its free.
    来自七仔个人补充说明：
        这个是纯Python实现的，运行的速度还是蛮快的，温馨提示，您将可以通过修改某些位操作，可以作为自己的私有的加密方式，
        然后可以作为一个校验码来使用！欢迎大家一起交流学习，感谢！

    Github: https://github.com/qqizai/Jenkins-Hash/blob/master/jenkinshash.py
    """



    def _hash(self, key):
        return self.hashlittle(key) % len(self.data)
        
        
    def rot(self, x, k):
        return (((x)<<(k)) | ((x)>>(32-(k))))

    def mix(self, a, b, c):
        a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF
        a -= c; a &= 0xFFFFFFFF; a ^= self.rot(c,4);  a &= 0xFFFFFFFF; c += b; c &= 0xFFFFFFFF
        b -= a; b &= 0xFFFFFFFF; b ^= self.rot(a,6);  b &= 0xFFFFFFFF; a += c; a &= 0xFFFFFFFF
        c -= b; c &= 0xFFFFFFFF; c ^= self.rot(b,8);  c &= 0xFFFFFFFF; b += a; b &= 0xFFFFFFFF
        a -= c; a &= 0xFFFFFFFF; a ^= self.rot(c,16); a &= 0xFFFFFFFF; c += b; c &= 0xFFFFFFFF
        b -= a; b &= 0xFFFFFFFF; b ^= self.rot(a,19); b &= 0xFFFFFFFF; a += c; a &= 0xFFFFFFFF
        c -= b; c &= 0xFFFFFFFF; c ^= self.rot(b,4);  c &= 0xFFFFFFFF; b += a; b &= 0xFFFFFFFF
        return a, b, c


    def final(self, a, b, c):
        a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF
        c ^= b; c &= 0xFFFFFFFF; c -= self.rot(b,14); c &= 0xFFFFFFFF
        a ^= c; a &= 0xFFFFFFFF; a -= self.rot(c,11); a &= 0xFFFFFFFF
        b ^= a; b &= 0xFFFFFFFF; b -= self.rot(a,25); b &= 0xFFFFFFFF
        c ^= b; c &= 0xFFFFFFFF; c -= self.rot(b,16); c &= 0xFFFFFFFF
        a ^= c; a &= 0xFFFFFFFF; a -= self.rot(c,4);  a &= 0xFFFFFFFF
        b ^= a; b &= 0xFFFFFFFF; b -= self.rot(a,14); b &= 0xFFFFFFFF
        c ^= b; c &= 0xFFFFFFFF; c -= self.rot(b,24); c &= 0xFFFFFFFF
        return a, b, c


    def hashlittle2(self, data, initval=0, initval2=0):
        length = lenpos = len(data)

        a = b = c = (0xdeadbeef + (length) + initval)

        c += initval2; c &= 0xFFFFFFFF

        p = 0  # 字符串偏移，进行位操作运算
        while lenpos > 12:
            a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24)); a &= 0xFFFFFFFF
            b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); b &= 0xFFFFFFFF
            c += (ord(data[p+8]) + (ord(data[p+9])<<8) + (ord(data[p+10])<<16) + (ord(data[p+11])<<24)); c &= 0xFFFFFFFF
            a, b, c = mix(a, b, c)
            p += 12
            lenpos -= 12

        if lenpos == 12:
            c += (ord(data[p+8]) + (ord(data[p+9])<<8) + (ord(data[p+10])<<16) + (ord(data[p+11])<<24)); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
        if lenpos == 11:
            c += (ord(data[p+8]) + (ord(data[p+9])<<8) + (ord(data[p+10])<<16)); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
        if lenpos == 10:
            c += (ord(data[p+8]) + (ord(data[p+9])<<8)); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
        if lenpos == 9:
            c += (ord(data[p+8])); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
        if lenpos == 8:
            b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
        if lenpos == 7:
            b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
        if lenpos == 6:
            b += ((ord(data[p+5])<<8) + ord(data[p+4])); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24))
        if lenpos == 5:
            b += (ord(data[p+4])); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
        if lenpos == 4:
            a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24))
        if lenpos == 3:
            a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16))
        if lenpos == 2:
            a += (ord(data[p+0]) + (ord(data[p+1])<<8))
        if lenpos == 1:
            a += ord(data[p+0])
        a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF
        if lenpos == 0:
            return c, b

        a, b, c = self.final(a, b, c)

        return c, b  # 这里是原版，您可以修改这里，返回不同的结果，
        # 例如py3写法(py2可能要注意int和long的转换)：
        # return ((int(a)) << 24) | (int(b) & 0xFFFFFF)  # 这里返回的值是一个，后面的记得也相应修改   


    def hashlittle(self, data, initval=0):
        c, b = self.hashlittle2(data, initval, 0)
        return c
        