class SegmentTree :

    def __init__(self, _list_) :

        def __getLen__(_size_) :

            if _size_ and _size_ & (_size_ - 1) == 0 :

                return _size_
            else :

                _bitLen_ = len(bin(_size_)) - 2
                return 1 << _bitLen_

        self._treeSize_ = 2 * __getLen__(len(_list_))

        self._tree_ = [0 for i in range(self._treeSize_)]
        self._lazy_ = [0 for i in range(self._treeSize_)]

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

    def __pointUpdate__(self, _pos_, _newVal_) :

        self._tree_[self._treeSize_ // 2 + _pos_] = _newVal_

        _node_ = (self._treeSize_ // 2 + _pos_) // 2

        while _node_ >= 1 :

            self._tree_[_node_] = self._tree_[2 * _node_] + self._tree_[2 * _node_ + 1]
            _node_ //= 2

    def rangeUpdate(self, _left_, _right_, _newVal_) :

        self.__rangeUpdate__(1, 0, self._treeSize_ // 2 - 1, _left_, _right_, _newVal_)

    def pointUpdate(self, _pos_, _newVal_) :

        self.__pointUpdate__(_pos_, _newVal_)

    def rangeQuery(self, _left_, _right_) :

        return self.__rangeQuery__(1, 0, self._treeSize_ // 2 - 1, _left_, _right_)

