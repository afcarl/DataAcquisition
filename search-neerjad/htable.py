"""
A hashtable represented as a list of lists with open hashing.
Each bucket is a list of (key,value) tuples
"""
import string
def htable(nbuckets):
    """Return a list of nbuckets lists"""
    table = []
    for i in range(nbuckets):
        table.append([])
    return table

def hashcode(o):
    """
    Return a hashcode for strings and integers; all others return None
    For integers, just return the integer value.
    For strings, perform operation h = h*31 + ord(c) for all characters in the string
    """
    h = 0
    if type(o) == int:
        h = o
        return h
    if o.isdigit() == True:
        h = int(o)
    else:
        for c in o:
            h = h * 31 + ord(c)
    return h

def bucket_indexof(table, key):
    """
    You don't have to implement this, but I found it to be a handy function.
    Return the element within a specific bucket; the bucket is:
    table[hashcode(key) % len(table)]. You have to linearly
    search the bucket to find the tuple containing key.
    """
    bucket = table[hashcode(key) % len(table)]
    for i in range(0, len(bucket)):
        if bucket[i][0] == key:
            return i
    return -1

def htable_put(table, key, value):
    """
    Perform the equivalent of table[key] = value
    Find the appropriate bucket indicated by key and then append value
    to that bucket. If the bucket for key already has a (key,value) pair
    with that key then replace it.  Make sure that you are only adding
    (key,value) associations to the buckets.
    """
    bucket_index = hashcode(key) % len(table)
    bucket = table[bucket_index]
    key_loc = bucket_indexof(table, key)
    if key_loc == -1:
        bucket.append((key, value))
    else:
        bucket[key_loc] = (key,bucket[key_loc][1].union(value))

    return table

def htable_get(table, key):
    """
    Return the equivalent of table[key].
    Find the appropriate bucket indicated by the key and look for the
    association with the key. Return the value (not the key and not
    the association!). Return None if key not found.
    """
    bucket_index = hashcode(key) % len(table)

    key_loc = bucket_indexof(table, key)
    if key_loc != -1:
        bucket = table[bucket_index]
        for i in range(0, len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1]
    else:
        return None



def htable_buckets_str(table):
    """
    Return a string representing the various buckets of this table.
    The output looks like:
        0000->
        0001->
        0002->
        0003->parrt:99
        0004->
    where parrt:99 indicates an association of (parrt,99) in bucket 3.
    """
    result_str = []
    for i in range(0, len(table)):
        result_str1 = '{:04d}'.format(i) + '->'
        if table[i] != None :
            for item in table[i]:
                result_str1 = result_str1 + str(item[0])+':'+str(item[1])
                if item != table[i][len(table[i])-1]:
                    result_str1 = result_str1 + ', '
        result_str.append(result_str1)
    final = "\n".join(result_str) + '\n'
    return final

def htable_str(table):
    """
    Return what str(table) would return for a regular Python dict
    such as {parrt:99}. The order should be in bucket order and then
    insertion order within each bucket. The insertion order is
    guaranteed when you append to the buckets in htable_put().
    """
    result_str = []
    for i in range(0, len(table)):
        if len(table[i]) != 0 :
            result_str1 = ''
            for item in table[i]:
                result_str1 = result_str1 + str(item[0])+':'+str(item[1])
                if item != table[i][len(table[i])-1]:
                    result_str1 = result_str1 + ', '
            result_str.append(result_str1)
    final = '{' + ', '.join(result_str) + '}'
    return final
