#!/bin/bash

# change to the script directory and calculate needed variables
cd `dirname $0`
PACKAGE_PATH=`pwd`
PACKAGE_NAME=`basename $PACKAGE_PATH`
VENV=$PACKAGE_PATH/.$PACKAGE_NAME	# virtualenv location as hidden subfolder
PYTHON=$VENV/bin/python 			# the virtualenv's python interpreter
PACKAGE_PARAMS=$1					# any package config parameters can be passed via $1: JSON object string

# create a python virtual environment for this package
echo "creating virtual environment in $VENV"
rm -rf $VENV
python3 -m virtualenv $VENV
SYMLINK=$PACKAGE_PATH/venv 			# so you can type "source venv" in the package directory
rm -f $SYMLINK
ln -s $VENV/bin/activate $SYMLINK

# install this package and its dependencies in the virtual environment
while read -r line; do 
	name=`echo $line | sed -E -e 's|==.*||g;s|^.*github.com/[^/]+/||g;s|(\.git)?\@.*$||g'`
	echo $name
	if [ -d "$PACKAGE_PATH/../$name" ]; then
		$PYTHON -m pip -q install -e $PACKAGE_PATH/../$name
	else
		$PYTHON -m pip -q install $name
	fi
done < "$PACKAGE_PATH/requirements.txt" 
$PYTHON -m pip -q install -e $PACKAGE_PATH

echo "Installation complete. 
You can activate this package's virtualenv at the command prompt by typing
	$ source `basename $SYMLINK`
in the package directory."

