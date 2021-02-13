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

    def reduce(self, environment):
        if self.left.is_reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return Add(self.left, self.right.reduce(environment))
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

    def reduce(self, environment):
        if self.left.is_reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)


class Machine:
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression = self.expression.reduce(self.environment)

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

    def reduce(self, environment):
        if self.left.is_reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.is_reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def is_reducible():
        return True

    def reduce(self, environment):
        return environment[self.name]


class DoNothing:
    def __str__(self):
        return 'do-nothing'

    def __repr__(self):
        return f'<<{self}>>'

    def __eq__(self, other_statement):
        return isinstance(other_statement, DoNothing)

    def __ne__(self, other):
        return not self.__eq__(other)
