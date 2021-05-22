## SINCC is not cookiecutter

SINCC is a factory for creating the initial structure for any python setup.py
based package.

#### Supported use cases
SINCC is a work in progress, we can at this time support the following use
cases.
- [ ] New project without any code.
- [ ] Transform existing `requirements.txt` based project into a `setup.py`
  based one.

#### Opionionated
By using SINCC our opinions finds a way to your code base. With time more and
more of these opionions will instead become option flags when running SINCC.


###### Structure
```
your_project
├── README.md
├── setup.cfg
├── setup.py
├── src
│   └── your_project
│       └── __init__.py
└── tests
    └── __init__.py
```

###### Tests
- [ ] Pytest

###### GNU Make
Inside your project you will find the file `Makefile` and the directory `make`.
Run `make help` if you are on a system that has GNU Make, to see all the
posibilities.
