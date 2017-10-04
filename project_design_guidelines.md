# LipPy_4.x API Project Requirements

### Style Guide:

+ Style guide must follow this: https://www.python.org/dev/peps/pep-0008/#comments, and this https://gist.github.com/CatDTran/20077c89348879c4e1fd4fbdda6427d3.
+ In addition, these rules are applied:
    + Short comments can be written inline.
    + Longer/block comment should be written before the relevant code to explain what the following code does.
    + Use proper English, check for spelling/grammar ...etc.
    + For Docstring, we use the standard reST format (default format in PyCharm) (https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format)
    which allow Sphinx documentation generator to generate documentation effortlessly.

### Project Design Principles:

+ Using the newer python, Python 3.x
+ Design as an API. Which allow a more modular structure. This means other projects can use some parts of this API in their code. All API code must be written inside *./api* directory.
Other directories contains code that is specific for LipPy_4.x
+ Operations that transform/mutate a DataFrame must return a NEW pandas.DataFrame() object. In place mutation of dataframe is not allowed, in other word, original DataFrame passed in as argument should be unchanged.
+ It's okay to define related classes in a same file (aka, module). However, nested definitions of classes are extremely discouraged. Module name should be relevant to classes it contains.
+ A method of a class that will return an object of the same class should return the same instance of that class (aka, `return self`). This would allow methods chaining, for example:

> import myClass
>
> myObject = New myClass()
>
> myObject.someMemberMethod().someMemberMethod2().someMemberMethod3()

### Functionalities:

LipPy_4.x API should have the following functionalities, these are common tasks/challenges that a researcher in Lipidomics is expected to deal with. The reason for this API is that it makes it easier for Lipidomics researchers to intergrate  this API to make their lives easier.
- Filter:
  - Given a dataset of precursor/fragment mass and intensities, it should be able to filter out background noise. No instrument is perfect, thus the ability to filter out background noise is important.
  - The filter policy should also be adjustable by specifying arguments.
- Naming molecules:
  - The API should be able to name a molecule's formula based on a known list of precursor/fragment mass pair and formula.
  What this function does is simply search and match the found mass pair from and compare it to the list. This list is might be different for each labs and probably customized to different lab's lipids of interest.
  - It should be able to return a formula based on the passed in lipids group and their fatty acid chains.
  - It should be able to return a formula based on the num of carbons, num of double bonds, and lipid group passed in as arguments.
  - It should be able to calculate molecule mass given a formula string.
- Statistic:
  - Be able to normalize to an internal standard. Internal standard in this context means the known lipids and concentration that is mixed directly into samples.
  - Be able to perform isotopic correction. At the moment, only carbon isotopes are considered. Isotopes of other elements such as Hydrogen, Oxygen ... are ignored due to the fact that the major contribution in the mass of a lipid molecules is carbons;
  in addition, since carbon atoms usually outnumber other elements in a lipid, there's also more chance of carbon isotopes compare to other elements. For these 2 reasons, only carbon isotopes are considered.
  - Be able to check for saturation. To be explained...
  - Be able to perform other statistic such as parametrics test...
- Database:
  - Provide a common interface to input data into mySQL database server of each lab's choosing.
- Static data:
  - Static data in this context mean the files which contains data in interest, since each lab might
  have different lipids classes of interest, database server, internal standard, element masses... The API must be built
  to allow each lab to use their own static data.

### Lipids Naming and Nomenclature:

The lipids naming conventions use in this API follow the common lipids naming convention. A neutral lipid,
in its unaltered form, its name will be represented as follow:
  > `Lipid Group`|`total_cbs:total_dbs`|(`chain1_cbs`:`chain1_dbs`~`chain2_cbs`:`chain2_dbs`~ ...)

In this convention, `Lipid Group` is the group of a lipid (ex: TAG, PI, DAG...), `total_cbs` is the total number
of carbons, `total_dbs` is the total number of double bonds in the lipid (ex: 16:0, 18:1 ...). If a lipid has
more than 1 chains and these chains are known, the parenthesis follow contains that information: `chain1_cbs` is
 the number of carbons, and `chain1_dbs` is the number of double bonds in chain 1, while `chain2_cbs` and `chain2_dbs`
 are the number of carbons and double bonds in chain 2, and so on.