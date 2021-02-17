# Reading [Understanding Computation](https://www.oreilly.com/library/view/understanding-computation/9781449330071/) book code


- [Book site](https://computationbook.com/)
  - [Sample code](https://computationbook.com/code)
  

This project was written using Python 3.9.


# Tips and Tricks
The book uses Ruby, but I'm using Python. 
- `from src.meaning import *`
- https://stackoverflow.com/questions/1436703/difference-between-str-and-repr/1436756#1436756

## [Reloading Modules from Python REPL](https://stackoverflow.com/questions/437589/how-do-i-unload-reload-a-python-module)
1. `from importlib import reload`
1. `import module`
1. `from module import *`
1. run some code
1. make changes to code
1. `reload(module)`
1. `from module import *`
1.  run updated code
