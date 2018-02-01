## experiment - use ast to inject code to prevent decorator slowdown

In short, yes.

It does break self inspection for the inspect library but things can still be self evaluated if you use `ast` inspection methods.

The code below proves you could technically modify the code in a function to inject added functionality of a decorator without adding the slowdown that comes with the typical uses of `functools.wraps`.

```python
In [168]: my_adder??
Signature: my_adder(a, b, c)
Source:
def my_adder(a,b,c):
    d = a+b
    if c%2:
        return a+b
    else:
        return a+d
File:      ~/<ipython-input-2-5c25a0aecdc7>
Type:      function

In [169]: code_to_inject = 'assert type(a) == int, "a needs to be an int"'

In [171]: ast.dump(ast.parse(code_to_inject).body[0])
Out[171]: "Assert(test=Compare(left=Call(func=Name(id='type', ctx=Load()), args=[Name(id='a', ctx=Load())], keywords=[]), ops=[Eq()], comparators=[Name(id='int', ctx=Load())]), msg=Str(s='a needs to be an int'))"

In [172]: ast_obj_to_inject = ast.parse(code_to_inject).body[0]

In [173]: my_adder_ast = ast.parse(inspect.getsource(my_adder))

In [174]: my_adder_ast.body[0].body.insert(0, ast_obj_to_inject)

In [175]: new_adder_code = compile(my_adder_ast, '<string>', 'exec')

In [176]: exec(new_adder_code)

In [177]: # now that `new_adder_code` has been ran, `my_adder` should now raise an assertion if argument `a` is not an int.

In [178]: my_adder(1,2,3)
Out[178]: 3

In [179]: my_adder(1.0,2,3)
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-179-8ae9d1301a63> in <module>()
----> 1 my_adder(1.0,2,3)

<string> in my_adder(a, b, c)

AssertionError: a needs to be an int

In [180]: # yay! added functionality without the overhead of nested function calls
```
