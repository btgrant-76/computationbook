class Number:
    def __init__(self, value):
        self.value = value


class Add:
    def __init__(self, left, right):
        pass


class Multiply:
    def __init__(self, left, right):
        pass


ast = Add(
    Multiply(Number(1), Number(2)),
    Multiply(Number(3), Number(4))
)

print(ast)
