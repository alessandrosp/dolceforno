#!/usr/bin/env bash

# Execute all the various test suites. The script **has** to be called
# from dolceforno main directory for it to work as path are relative
# to the location the script is invoked from.
#
# Usage:
#  $ ./tests/run_all_tests.sh [-v]
# * -v: Whether to execute the tests verbosely. Default, false.
#
# Example:
#  $ ./tests/run_all_tests.sh -v
#

# Default parameters.
verbose=""

# Check whether the user specified any parameter. If positive, then
# we override the default values set above.
while [ "$1" != "" ]; do
  if [[ "$1" == "-v" ]]; then
    verbose="-v"
  fi
  shift
done

echo "*** Running tests from dolceforno_test.py ***"
python -m unittest tests/unit/dolceforno_test.py $verbose

echo "*** Running tests from recipes_test.py ***"
python -m unittest tests/unit/recipes_test.py $verbose
