#### Style Guide:
+ Style guide must follow this: https://www.python.org/dev/peps/pep-0008/#comments and this https://gist.github.com/CatDTran/20077c89348879c4e1fd4fbdda6427d3

#### Project Design Principles:
+ Design as an API. Which allow a more modular structure.
+ Operations that work on a DataFrame must return a NEW pandas.DataFrame() object. In place mutation of dataframe is not allowed, in other word, original DataFrame passed in as argument should be unchanged.
+ Each class live in its own file. Nested definitions of classes are extremely discouraged. File name must match class name defined in that file (name case don't have to match).
+ A method that return an object of its class must return that instance of that class. This would allow methods chaining, for example:
> import class
> myObject = New class()
> meObject.someMemberMethod().someMemberMethod2().someMemberMethod3()
