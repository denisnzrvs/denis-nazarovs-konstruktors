#!/bin/bash
# Runs all tests and then deletes the config file after the tests are successful.
# The config file is stored in ../my_secret_files

echo "Script for testing worker and config, and deleting the config file after successful tests"
echo "------------------------------------------------"

echo "Getting python3 executable loc"
python_exec_loc=$(which python3)
if [ $? -eq 0 ]; then echo "OK"; else echo "Problem getting python3 exec location"; exit 1; fi
echo "$python_exec_loc"
echo "------------------------------------------------"

echo "Worker tests"
$python_exec_loc test_worker.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Worker test FAILED"; exit 1; fi
echo "------------------------------------------------"

echo "Custom tests"
$python_exec_loc test_config.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Config test FAILED"; exit 1; fi
echo "------------------------------------------------"

echo "Custom tests"
$python_exec_loc custom_tests.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Custom tests FAILED"; exit 1; fi
echo "------------------------------------------------"

read  -n 1 -p "Do you want to delete your config file? (y/n) " delete_config
if [ "$delete_config" = "y" ]; then
    rm config.ini
    echo -e "\nCONFIG FILE DELETED"
    echo "Config file can be restored from ../my_secret_files by copying using the following command:"
    echo "cp ../my_secret_files/config.ini ./config.ini"
fi
if [ $? -eq 0 ]; then echo -e "\nOK"; else echo "\nError deleting config.ini"; exit 1; fi
echo "------------------------------------------------"

echo "ALL TESTS PASSED"
