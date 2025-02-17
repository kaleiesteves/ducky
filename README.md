# Ducky
A command-line tool for saving documentation to plain text files.

---
## Installation
Install Ducky by cloning the repo and activating the virtual environment.

**Cloning the repository**
```
git clone git@github.com:kaleiesteves/ducky.git
```
*You may need to add an SSH key for access*


**Acitving the virtual environment**
```
source .ducky/bin/activate
```

## Usage
With the environment script activated, the following commands can be used.

**Add a file**
```
ducky add <file.pdf>
```
This adds the file to ducky's pond, then converts it to plain text and puts it in its nest.

**Delete a file**
```
ducky del <file.pdf>
```
This removes the plain text from its nest and also the original file from the pond.

**Search for terms in a file**
```
ducky search <file.pdf> <keyword> <keyword> ...
```
This searches for sentences containing the specified keywords.