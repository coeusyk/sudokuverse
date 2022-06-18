# Sudoku Game Project

Creating a game of Sudoku using Python, having basic features:-
* Graphical UI
* Multi-complexity
* Time keeper
* Hints


## Project Structure

```
/game-sudoku
    |__ /src
        |-- __init__.py
        |-- app.py
        |-- game-sudoku_database.sql
        |__ /module
            |-- *.py
        |__ /templates
            |__ /module
                |-- *.html
            |__ ..
            |__ .
        |__ /static
            |__ /css
                |-- *.css
            |__ /js
                |-- *.js
        |__ ..
        |__ .
        
    |__ /tests
        |__ /code-tests
            |__ /gui
                |-- *.html
                |-- *.css
                |-- *.js
            |__ /python
                |-- *.py
            |__ /database
                |-- *.sql
        |__ /unit-tests
            |__ *.py
```

Given above is the **project structure** of our project. Files have to be added as required (shown above).


## Module Info

### 1. [/src](https://github.com/alp-comp-project/game-sudoku/tree/develop/src)

Contains the source code of the project.

Only [`app.py`](), [`__init__.py`](), and [`game-sudoku_database.sql`]() files go into this (other files go under the sub-folders).

### 2. [/tests](https://github.com/alp-comp-project/game-sudoku/tree/develop/tests)

Contains the files that are currently in progress or need review.

Any type of file will go in to the respective folders in this.

### 3. /module

Contains the backend part of different parts of the project, having certain functionalities.

All python files will go in to these folders.

### 4. [/templates](https://github.com/alp-comp-project/game-sudoku/tree/develop/src/templates)

Contains the files for the backbone of the frontend part, divided into separate modules.

All HTML files will go in to the subfolders of this folder.

### 5. [/static](https://github.com/alp-comp-project/game-sudoku/tree/develop/src/static)

Contains the files for the styling and functionality of the HTML files.

All CSS and JavaScript files will go in to their respective subfolders of this folder.


## Guidelines

Use `develop` branch for active development.

Mention "Closes #(the number given to the issue)" at the end of the description of the commit you do if the issue
is solved.

After you have solved an issue, create a **pull request** to make changes to the `main` branch.
