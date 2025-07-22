# def load():
#     import

def method_with_unused_parameter(used, redundant):
    print("It is used parameter: " + str(used))


def intention_example(a, b):
    if not (a and b):
        return 1
    return 2


# method_with_unused_parameter("first", "second")
# method_with_unused_parameter("used", "unused")
# intention_example(True, False)

foo = False

# athing = lambda : if foo:
#                     print('foo')
#                     return 'foo'
#                   else:
#                     print('bar')
#                     return 'bar'


a_thing = lambda: 'foo' if foo else 'bar'

print(a_thing())
