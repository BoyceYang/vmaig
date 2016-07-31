# !/usr/bin/python
# -*-coding:utf-8-*-


class StringOfTitle(str):
    """
    用来修改admin中显示的app名称,因为admin app名称使用str.title()显示,所以修改str类的title方法可以实现名称修改。
    """
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self
