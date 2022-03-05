class SegmentTree :

    """
    Represents the Segment Tree Data Structure

    Functions :

        -- Use case with example of all functions (including internal)
           is specified below each of their respective declarations --

        -- All Internal functions required to maintain the Segment Tree are represented as __[function_name]__

        -------------------------------------------------------------------------------------------------------------

        Range Query => Returns the respective query(sum, min, gcd ...) in the range [L, R]
                       as specified in the function parameter.

        Point Update => Updates the element value at the specified position [pos] by replacing
                        it with the new value [newVal], thereby updating the tree.

        Range Update => Adds new value [newVal] to each of the elements in the range [L, R] ensuring
                        the required updates using lazy propagation

        -------------------------------------------------------------------------------------------------------------

        Time Complexity : Each of the above functions of the tree is performed in O(log(N)), due to the height
                          of the tree being log(N).

        Space Complexity : The size of the main tree [tree] and the lazy tree [lazy] both consume O(2*N) memory
                           to represent each of the 2 * N - 1 nodes in the tree.

        -------------------------------------------------------------------------------------------------------------


    """

    """
        Represents the default constructor call with the initial [list]
        being the parameter in order to build the tree.
    """

    def __init__(self, _list_) :

        """
            -- Returns the closest power of 2 from the [size] of
            the initial [list]. --

            -- The return value of this function will be the size of the segment tree [tree] as well as the
            lazy tree [lazy] there by having 2 * [returned size] as the size of the array. --

        Example :

            -- Let the list size be 19, then the closest power would be 32. --
            -- Hence, the new size of the tree would be 32 before the build function is called --
        """

        def __getLen__(_size_) :

            if _size_ and _size_ & (_size_ - 1) == 0 :

                return _size_
            else :

                _bitLen_ = len(bin(_size_)) - 2
                return 1 << _bitLen_

        self._treeSize_ = 2 * __getLen__(len(_list_))

        self._tree_ = [0 for i in range(self._treeSize_)]
        self._lazy_ = [0 for i in range(self._treeSize_)]

        """
            -- Performs the build procedure for the tree
            to initialize the tree with the respective values in each of the 2 * N nodes. --
        
        Example :
        
                                    -- General Representation of the Tree --
        
                                                        |1|
                                          |2|                        |3|
                                   |4|          |5|           |6|           |7|
                                |8|   |9|   |10|   |11|   |12|   |13|   |14|   |15|
                                
            -- In the above example tree, the nodes 8...15 would store the initial [list] with additional nodes storing
            appropriate dummy values [ex: For sum => 0, For min => inf, etc.]. --
            
            -- Each of the parent nodes would then be updated by traversing in a bottom-up manner. --
        """

        def __build__(_list_) :

            _listSize_ = len(_list_)

            for i in range(_listSize_) :

                self._tree_[self._treeSize_ // 2 + i] = _list_[i]

            for i in range(_listSize_, self._treeSize_ // 2) :

                self._tree_[self._treeSize_ // 2 + i] = 0

            for i in range(self._treeSize_ // 2 - 1, 0, -1) :

                self._tree_[i] = self._tree_[2 * i] + self._tree_[2 * i + 1]

            self._root_ = self._tree_[1]

        __build__(_list_)

    """
    
        Returns the query value for the specified range [L, R] for a particular [node].
    
        [Internally called by the rangeQuery(l, r) function]
    """

    def __rangeQuery__(self, _node_, _treeLeft_, _treeRight_, _left_, _right_) :

        if self._lazy_[_node_] :

            self._tree_[_node_] += self._lazy_[_node_] * (_treeRight_ - _treeLeft_ + 1)

            if _treeLeft_ != _treeRight_ :

                self._lazy_[2 * _node_] += self._lazy_[_node_]
                self._lazy_[2 * _node_ + 1] += self._lazy_[_node_]

            self._lazy_[_node_] = 0

        if _treeLeft_ >= _left_ and _treeRight_ <= _right_ :

            return self._tree_[_node_]

        elif _treeLeft_ > _right_ or _treeRight_ < _left_ :

            return 0

        else :

            _mid_ = (_treeLeft_ + _treeRight_) // 2

            return \
                self.__rangeQuery__(2 * _node_, _treeLeft_, _mid_, _left_, _right_) + \
                self.__rangeQuery__(2 * _node_ + 1, _mid_ + 1, _treeRight_, _left_, _right_)

    """
        Updates the tree accordingly for the specified range [L, R] for a particular [node] and [newVal].
    
        [Internally called by the rangeUpdate(l, r) function]
    """

    def __rangeUpdate__(self, _node_, _treeLeft_, _treeRight_, _left_, _right_, _newVal_) :

        if self._lazy_[_node_] :

            self._tree_[_node_] += self._lazy_[_node_] * (_treeRight_ - _treeLeft_ + 1)

            if _treeLeft_ != _treeRight_ :

                self._lazy_[2 * _node_] += self._lazy_[_node_]
                self._lazy_[2 * _node_ + 1] += self._lazy_[_node_]

            self._lazy_[_node_] = 0

        if _treeLeft_ >= _left_ and _treeRight_ <= _right_ :

            self._tree_[_node_] += _newVal_ * (_treeRight_ - _treeLeft_ + 1)

            if _treeLeft_ != _treeRight_ :

                self._lazy_[2 * _node_] += _newVal_
                self._lazy_[2 * _node_ + 1] += _newVal_

        elif _treeLeft_ > _right_ or _treeRight_ < _left_ :

            return

        else :

            _mid_ = (_treeLeft_ + _treeRight_) // 2

            self.__rangeUpdate__(2 * _node_, _treeLeft_, _mid_, _left_, _right_, _newVal_)
            self.__rangeUpdate__(2 * _node_ + 1, _mid_ + 1, _treeRight_, _left_, _right_, _newVal_)

            self._tree_[_node_] = self._tree_[2 * _node_] + self._tree_[2 * _node_ + 1]

    """
        Updates the tree accordingly for the specified position [pos] with the [newVal].
    
        [Internally called by the pointUpdate(l, r) function]
    """

    def __pointUpdate__(self, _pos_, _newVal_) :

        self._tree_[self._treeSize_ // 2 + _pos_] = _newVal_

        _node_ = (self._treeSize_ // 2 + _pos_) // 2

        while _node_ >= 1 :

            self._tree_[_node_] = self._tree_[2 * _node_] + self._tree_[2 * _node_ + 1]
            _node_ //= 2

    """
    -- All functions below are the User Functions which invoke the necessary
       Internal Functions as mentioned earlier. --
    """

    def rangeUpdate(self, _left_, _right_, _newVal_) :

        self.__rangeUpdate__(1, 0, self._treeSize_ // 2 - 1, _left_, _right_, _newVal_)

    def pointUpdate(self, _pos_, _newVal_) :

        self.__pointUpdate__(_pos_, _newVal_)

    def rangeQuery(self, _left_, _right_) :

        return self.__rangeQuery__(1, 0, self._treeSize_ // 2 - 1, _left_, _right_)

    def printTree(self) :

        print("Seg Tree : ", self._tree_)
        print("Lazy Tree : ", self._lazy_)

    """
    Example for using the SegmentTree class :
    
            a = [3, 5, 4, 8, 1, 4] => List of elements.
            tree = SegmentTree(a) => New object of class Segment Tree by passing the list.
        
            print(tree.rangeQuery(2, 4)) => Sum of [2, 4] = 13
         
        [Let's say we want to update the element at position 3 with the value 18]
        
            tree.pointUpdate(3, 18)
         
            print(tree.rangeQuery(2, 5)) => Sum of [2, 5] = 27
        
        [Let's say we want to add 9 to elements in the range [0, 2]]
        
            tree.rangeUpdate(0, 2, 9)
        
            print(tree.rangeQuery(0, 4) => Sum of [0, 4] = 58
    """
