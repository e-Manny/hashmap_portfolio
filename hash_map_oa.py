# Name: Manuel Espinoza
# OSU Email: espinman@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/2/2022
# Description: # Description:  Implementation of methods for the Hash Map ADT with Open Addressing for
# collision handling

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Update the key/value pair in the HashMap at the determined index. If the key already exists in the determined
        index, replace the key with the given value. If the load value is over 0.5 then double the capacity.
        """
        load_factor = self.table_load()
        if load_factor >= 0.5:
            self.resize_table(self._capacity * 2)
        hash_val = self._hash_function(key)
        quad_val = 0
        index_val = (hash_val + quad_val ** 2) % self._capacity
        if self.contains_key(key):
            #find key and replace its value
            for ll_index in range(self._buckets.length()):
                if self._buckets[ll_index] is not None:
                    if self._buckets[ll_index].key == key:
                        self._buckets[ll_index].value = value
                        return
        while self._buckets[index_val] is not None and self._buckets[index_val].is_tombstone is False:
            quad_val += 1
            index_val = (hash_val + quad_val ** 2) % self._capacity
        self._buckets.set_at_index(index_val, HashEntry(key, value))
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        counter = 0
        for i in range(self._capacity):
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                counter += 1
        return counter

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. If new_capacity is 1 or more, make sure it is a prime number.
        If not, change it to the next highest prime number.
        """
        if new_capacity < self._size:
            return
        if new_capacity == 2:
            new_table = HashMap(4, self._hash_function)
        elif self._is_prime(new_capacity):
            new_table = HashMap(new_capacity - 1, self._hash_function)
        else:
            new_cap = self._next_prime(new_capacity)
            new_table = HashMap(new_cap, self._hash_function)
        for ll_index in range(self._buckets.length()):
            if self._buckets[ll_index] is not None and self._buckets[ll_index].is_tombstone is False:
                new_table.put(self._buckets[ll_index].key, self._buckets[ll_index].value)
        self._capacity = new_table._capacity
        self._buckets = new_table._buckets
        self._size = new_table._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, return None.
        """
        # for ll_index in range(self._buckets.length()):
        #     if self._buckets[ll_index] is not None and self._buckets[ll_index].is_tombstone is False:
        #         if self._buckets[ll_index].key == key:
        #             return self._buckets[ll_index].value
        # return None

        if self.contains_key(key) is False:
            return None
        hash_val = self._hash_function(key)
        quad_val = 0
        index_val = (hash_val + quad_val ** 2) % self._capacity
        while self._buckets[index_val].key != key:
            quad_val += 1
            index_val = (hash_val + quad_val ** 2) % self._capacity
        return self._buckets[index_val].value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        """
        # for ll_index in range(self._buckets.length()):
        #     if self._buckets[ll_index] is not None and self._buckets[ll_index].is_tombstone is False and \
        #             self._buckets[ll_index].key == key:
        #         return True
        # return False

        if self._buckets.length() == 0:
            return False
        hash_val = self._hash_function(key)
        quad_val = 0
        index_val = (hash_val + quad_val ** 2) % self._capacity
        if self._buckets[index_val] is None:
            return False
        if self._buckets[index_val].is_tombstone is False and self._buckets[index_val].key == key:
            return True
        if self._buckets[index_val].key != key:
            for i in range(self._buckets.length()):
                quad_val += 1
                index_val = (hash_val + quad_val ** 2) % self._capacity
                if self._buckets[index_val] is None:
                    return False
                if self._buckets[index_val].is_tombstone is False and self._buckets[index_val].key == key:
                    return True
            return False
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. Set the tombstone value to True.
        """
        # for ll_index in range(self._buckets.length()):
        #     if self._buckets[ll_index] is not None and self._buckets[ll_index].is_tombstone is False:
        #         if self._buckets[ll_index].key == key:
        #             self._buckets[ll_index].is_tombstone = True
        #             self._size -= 1
        #             return

        if self.contains_key(key) is False:
            return
        hash_val = self._hash_function(key)
        quad_val = 0
        index_val = (hash_val + quad_val ** 2) % self._capacity
        while self._buckets[index_val].key != key:
            quad_val += 1
            index_val = (hash_val + quad_val ** 2) % self._capacity
        self._buckets[index_val].is_tombstone = True
        self._size -= 1
        return

    def clear(self) -> None:
        """
        Clear the contents of the hash map.
        """
        for i in range(self._capacity):
            self._buckets[i] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        """
        return_da = DynamicArray()
        for ll_index in range(self._buckets.length()):
            if self._buckets[ll_index] is not None and self._buckets[ll_index].is_tombstone is False:
                return_da.append((self._buckets[ll_index].key, self._buckets[ll_index].value))
        return return_da

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """

        try:
            value = self._buckets[self._index]
            while value is None or value.is_tombstone:
                self._index = self._index + 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        return value



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
