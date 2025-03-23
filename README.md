# BFplusplus
## BrainFuck with a few additions
all basic features are inherited from brainfuck
## New features
### Random numbers
? writes a random number from 0 to 255 to the curent cell
### Module creation and import
Modules are .bfm files that can be ran from a main process, they can recive one character of stdin and return a character of stdout
importing a module is as simple as {"module_name.bfm"} wich assigns the imported module a indentifier based on the current cell
modules can be called using {module_identifier}
example:
```
+{"multiply5.bfm"},{1}.
```
### Cell clear
! sets current cell to 0
### More to come!
