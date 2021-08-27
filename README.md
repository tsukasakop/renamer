# Renamer
#### Video Demo:  <https://www.youtube.com/watch?v=Hdynn4sO0ZY>
#### Description:
#### Feature:
  &emsp;
  Command line tool to rename files in a directory at once  
#### Getting started:
  &emsp;
  Inside of the `renamer` directory, run `pip3 install -r requirements.txt` to install this project’s dependencies: `natsort` for sorting.
#### File structure:
  - `README.md`:  
    this file.
  - `requirements.txt`:  
    list of mojule.
  - `renamer.py`:  
    Ask for a naming convention and  
    rename all files in the given directory.
  - `config`:  
    Where to save the options set in rename.py as `.csv` file.  
    Settings can be changed manually using a text editor.
#### Usage: `python renamer.py [directory_path] [option.csv]`
  - `python renamer.py`
    > Prompt for the path of the target directory  
    > Ask the user to choose a naming convention
  - `python renamer.py directory_path`
    > Target the argument directory  
    > Ask the user to choose a naming convention
  - `python renamer.py directory_path option.csv`
    > Target the argument directory  
    > Rename according to argument naming convention
#### Specification:
  - The `Directory` class requires a directory name when an instance is created.
    - When an instance is created, it gets information about the argument directory and recursively creates a new instance with the subordinate directories contained in it as an argument.
    - Subordinate instances are recorded in the `children` attribute, and information on subordinate directories can also be obtained.

    - Other attributes that are retrieved when the instance is created are:
      - `path`: Directory path
      - `mother`: instance of the parent directory
      - `file_count`: number of files in the directory
      - `depth`: Depth from the first directory

    - The methods defined by the class are:
      - `show`: Shows the instance information as follows:` depth directory name (number of files) in whitespace`
      - `show_all`: Executes the` show` method on all subordinate instances and themselves
      - `rename`: Renames all files in the instance based on ` prefex`:the user-set prefix / suffix information , and `joint` the word joint information.
      - `rename_all`: Executes the` rename` method for the instance and all of its instances

  - The `question_YN` function takes the string given as an argument as a question sentence, asks for a yes or no answer, and returns the answer as true or false value.
    - If the answer is neither `y`,` n`, `yes`,` no`, repeat the question until you get the correct answer.
