# TODO before merging back to main, review this code vs. final state from the book

class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return False

    def evaluate(self, environment):
        return self


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} + {self.right}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Add(self.left.reduce(environment), self.right), environment
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(environment)), environment
        else:
            return Number(self.left.value + self.right.value), environment

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value + self.right.evaluate(environment).value)


class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} * {self.right}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value * self.right.evaluate(environment).value)


class Machine:
    def __init__(self, statement, environment):
        self.statement = statement
        self.environment = environment

    def step(self):
        self.statement, self.environment = self.statement.reduce(self.environment)

    def run(self):
        while self.statement.reducible():
            print(f'{self.statement}, {self.environment}')
            self.step()

        print(f'{self.statement}, {self.environment}')


class Boolean:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return False

    def __eq__(self, other):
        if not isinstance(other, Boolean):
            return False

        return other.value == self.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def evaluate(self, environment):
        return self


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} < {self.right}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)

    def evaluate(self, environment):
        return Boolean(self.left.evaluate(environment).value < self.right.evaluate(environment).value)


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        return environment[self.name]

    def evaluate(self, environment):
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

    @staticmethod
    def reducible():
        return False

    def evaluate(self, environment):
        return environment


class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return f'{self.name} = {self.expression}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        if self.expression.reducible():
            return Assign(self.name, self.expression.reduce(environment)), environment
        else:
            return DoNothing(), environment | {self.name: self.expression}

    def evaluate(self, environment):
        return environment | {self.name: self.expression.evaluate(environment)}


class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return f'if ({self.condition}) {{ {self.consequence} }} else {{ {self.alternative} }}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        if self.condition.reducible():
            return If(self.condition.reduce(environment), self.consequence, self.alternative), environment
        else:
            if self.condition == Boolean(True):
                return self.consequence, environment
            elif self.condition == Boolean(False):
                return self.alternative, environment

    def evaluate(self, environment):
        evaluated = self.condition.evaluate(environment)
        if evaluated == Boolean(True):
            return self.consequence.evaluate(environment)
        elif evaluated == Boolean(False):
            return self.alternative.evaluate(environment)


class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return f'{self.first}; {self.second}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        if isinstance(self.first, DoNothing):
            return self.second, environment
        else:
            reduced_first, reduced_environment = self.first.reduce(environment)
            return Sequence(reduced_first, self.second), reduced_environment

    def evaluate(self, environment):
        return self.second.evaluate(self.first.evaluate(environment))


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f'while ({self.condition}) {{ {self.body} }}'

    def __repr__(self):
        return f'<<{self}>>'

    @staticmethod
    def reducible():
        return True

    def reduce(self, environment):
        return If(self.condition, Sequence(self.body, self), DoNothing()), environment

    def evaluate(self, environment):
        cond_evaluation = self.condition.evaluate(environment)
        if cond_evaluation == Boolean(True):
            return self.evaluate(self.body.evaluate(environment))
        elif cond_evaluation == Boolean(False):
            return environment
