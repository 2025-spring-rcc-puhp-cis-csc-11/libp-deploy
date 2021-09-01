
# libPuhfessorP Function Documentation

This document describes some of the functions available inside the *libPuhfessorP* library.

## Input Functions

### libPuhfessorP_inputLine

The ```libPuhfessorP_inputLine``` function will read a line of input from the console (whatever characters the user submits until they hit enter).

Arguments:

1. Pointer to your input buffer
2. Size of your input buffer

### libPuhfessorP_inputSignedInteger64

The ```libPuhfessorP_inputSignedInteger64``` function will read a signed 64-bit integer from the console.

Arguments: none

Returns: A 64-bit signed integer


## Output Functions

### libPuhfessorP_printSignedInteger64

The ```libPuhfessorP_printSignedInteger64``` function will print a signed 64-bit integer to the console.

Arguments:

1. The integer you wish to print

## Parsing and Conversion Functions

### libPuhfessorP_lTrim, libPuhfessorP_rTrim, and libPuhfessorP_trim

The functions ```libPuhfessorP_lTrim```, ```libPuhfessorP_rTrim```, and ```libPuhfessorP_trim``` will trim a string from the left side, right side, and both sides.

Arguments:

1. A pointer to the string to be trimmed

### libPuhfessorP_parseSignedInteger64

The ```libPuhfessorP_parseSignedInteger64``` function converts a string to a signed 64-bit integer.

Arguments:

1. A pointer to the string's first character

Returns: a 64-bit integer if the string was valid, or the special number ```0x8000000000000000``` if the string was invalid.

### libPuhfessorP_signedInteger64ToString

The ```libPuhfessorP_signedInteger64ToString``` function will convert a signed 64-bit integer to a string.

Arguments:

1. The integer you wish to convert
2. The address of a character buffer where the string can be written



## Debugging Functions

### libPuhfessorP_printRegisters

The function ```libPuhfessorP_printRegisters``` will dump the contents of (most) registers to the console.











