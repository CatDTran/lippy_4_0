#### Style Guide:
+ Style guide must follow this: https://www.python.org/dev/peps/pep-0008/#comments, and this https://gist.github.com/CatDTran/20077c89348879c4e1fd4fbdda6427d3.
+ In addition, these rules are applied:
    + Short comments can be written inline.
    + Longer/block comment should be written before the relevant code to explain what the following code does.
    + Use proper English, check for spelling/grammar ...etc.
    + For Docstring, we use the standard reST format (default format in PyCharm) (https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format)
    which allow Sphinx documentation generator to generate documentation effortlessly.


#### Project Design Principles:
+ Using the newer python, Python 3.x
+ Design as an API. Which allow a more modular structure. This means other projects can use some parts of this API in their code. All API code must be written inside *./libs/* directory.
Other directories contains code that is specific for LipPy_4.x
+ Operations that work on a DataFrame must return a NEW pandas.DataFrame() object. In place mutation of dataframe is not allowed, in other word, original DataFrame passed in as argument should be unchanged.
+ It's okay to define related classes in a same file (aka, module). However, nested definitions of classes are extremely discouraged. Module name should be relevant to classes it contains.
+ A method of a class that will return an object of the same class should return the same instance of that class (aka, `return self`). This would allow methods chaining, for example:
> import myClass
> myObject = New myClass()
> myObject.someMemberMethod().someMemberMethod2().someMemberMethod3()
+ Use reactive programming concept (aka asynchronous and event-based programming). In other words, chains of operations that depend on each other should listen to events to know whether a piece data is ready to perform the next transformation.
For example, operation_2 must listen to 'completed' event from operation_1(my_data). RxPY is a library designed for such purpose https://github.com/ReactiveX/RxPY/tree/develop. *???*

