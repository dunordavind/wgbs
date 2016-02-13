__author__ = 'med-pvo'


class Sample():
    def __init__(self, mates, name):
        """

        :param mates: [Mate]
        """
        self.__mates = mates
        self.__name = name

    @property
    def mates(self):
        return self.__mates

    @property
    def name(self):
        return self.__name
