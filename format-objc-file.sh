#!/usr/bin/env bash
# format-objc-file.sh
# Formats an Objective-C file, replacing it without a backup.
# Copyright 2015 Square, Inc

export CDPATH=""
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PATH=$PATH:/opt/homebrew/bin

if [ ! -e ".clang-format" ]; then
	echo "Couldn't find .clang-format file, unable to format files. Please setup this repo by running the setup-repo.sh script from your repo's top level."
	echo "Also, formatting scripts should be run from the repo's top level dir."
	exit 1
fi

if [ ! -x "swiftlint" ]; then
	echo "Couldn't find swiftlint, unable to lint files. Please setup this repo by running the setup-repo.sh script from your repo's top level."
	echo "Also, formatting scripts should be run from the repo's top level dir."
	exit 1
fi

if [ ! -x "swiftformat" ]; then
	echo "Couldn't find swiftformat, unable to format files. Please setup this repo by running the setup-repo.sh script from your repo's top level."
	echo "Also, formatting scripts should be run from the repo's top level dir."
	exit 1
fi

# "#pragma Formatter Exempt" or "// MARK: Formatter Exempt" means don't format this file.
# Read the first line and trim it.
line="$(head -1 "$1" | xargs)" 
[ "$line" == "#pragma Formatter Exempt" -o "$line" == "// MARK: Formatter Exempt" ] && exit 0

# Format Swift files using swiftformat
filename=$(basename "$1")

if [[ ${filename##*.} == 'swift' ]]; then
    cat "$1" | swiftformat stdin --stdinpath "$1" --config "$DIR/.swiftformat" --quiet --output "$1"
    exit $?
fi

# Fix an edge case with array / dictionary literals that confuses clang-format
python3 "$DIR"/custom/LiteralSymbolSpacer.py "$1"
# The formatter gets confused by C++ inline constructors that are broken onto multiple lines
python3 "$DIR"/custom/InlineConstructorOnSingleLine.py "$1"
# Add a semicolon at the end of simple macros
python3 "$DIR"/custom/MacroSemicolonAppender.py "$1"
# Add an extra newline before @implementation and @interface
#python3 "$DIR"/custom/DoubleNewlineInserter.py "$1"

# Run clang-format
"$DIR"/bin/clang-format-3.8-custom -i -style=file "$1" ;
# Fix an issue with clang-format getting confused by categories with generic expressions.
#python3 "$DIR"/custom/GenericCategoryLinebreakIndentation.py "$1"
# Fix an issue with clang-format breaking up a lone parameter onto a newline after a block literal argument.
python3 "$DIR"/custom/ParameterAfterBlockNewline.py "$1"
# Fix an issue with clang-format inserting spaces in a preprocessor macro.
python3 "$DIR"/custom/HasIncludeSpaceRemover.py "$1"
# Add a newline at the end of the file
python3 "$DIR"/custom/NewLineAtEndOfFileInserter.py "$1"
# Convert "^(void) {" to "^{" in block declarations
python3 "$DIR"/custom/RemoveVoidBlockDeclaration.py "$1"
# Remove trailing semicolon from API_AVAILABLE macros
python3 "$DIR"/custom/RemoveAPIAvailableSemicolon.py "$1"
