class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def is_reducible():
        return False


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} + {self.right}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def is_reducible():
        return True

    def reduce(self):
        if self.left.is_reducible():
            return Add(self.left.reduce(), self.right)
        elif self.right.is_reducible():
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left.value + self.right.value)


class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} * {self.right}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def is_reducible():
        return True

    def reduce(self):
        if self.left.is_reducible():
            return Multiply(self.left.reduce(), self.right)
        elif self.right.is_reducible():
            return Multiply(self.left, self.right.reduce())
        else:
            return Number(self.left.value * self.right.value)


class Machine:
    def __init__(self, expression):
        self.expression = expression

    def step(self):
        self.expression = self.expression.reduce()

    def run(self):
        while self.expression.is_reducible():
            print(self.expression)
            self.step()

        print(self.expression)


class Boolean:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def is_reducible():
        return False


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} < {self.right}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def is_reducible():
        return True

    def reduce(self):
        if self.left.is_reducible():
            return LessThan(self.left.reduce(), self.right)
        elif self.right.is_reducible():
            return LessThan(self.left, self.right.reduce())
        else:
            return Boolean(self.left.value < self.right.value)







