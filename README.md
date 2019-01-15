NaturalLanguagePrediction
=========================
Description:
------------
An on going project of single word and sentence prediction from a statistical language model using a 2nd order (and 1st order where applicable) Markov Model approach.

This project can also be found [in this repo](https://github.com/alexchernous/Projects) with original commits as well as other small work. I've since separated that repo into its own repos for each type of project.

Version and Info:
-----------------
* python version: 3.7.2
* literature used to train models: [A Tale of Two Cities](https://www.gutenberg.org/ebooks/98) from [Project Gutenberg](https://www.gutenberg.org/wiki/Main_Page)
* imports:
```python
import tkinter, re, urllib.request, json, random, math, numpy
from operator import itemgetter
```
* models are included in the 4 *.txt* files

Running program:
----------------
1. Update python version **(IF APPLICABLE)**
2. Use *pip/conda* to install any python packages **(IF APPLICABLE)**
3. Run *GUI.py*

Note: if you want to test the training of the model, run *trainer.py*