#!/usr/bin/env bash
# format-objc-file-dry-run.sh
# Outputs a formatted Objective-C file to stdout (doesn't alter the file).
# Copyright 2015 Square, Inc

export CDPATH=""
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PATH=$PATH:/opt/homebrew/bin

# "#pragma Formatter Exempt" or "// MARK: Formatter Exempt" means don't format this file.
# Read the first line and trim it.
line="$(head -1 "$1" | xargs)" 
if [ "$line" == "#pragma Formatter Exempt" -o "$line" == "// MARK: Formatter Exempt" ]; then
  cat "$1" && exit 0
fi

# Format Swift files using swiftformat
filename=$(basename "$1")

if [[ ${filename##*.} == 'swift' ]]; then
    swiftformat "$1" --config "$DIR/.swiftformat" --output stdout --quiet
    exit $?
fi

cat "$1" | \
python3 "$DIR"/custom/LiteralSymbolSpacer.py | \
python3 "$DIR"/custom/InlineConstructorOnSingleLine.py | \
python3 "$DIR"/custom/MacroSemicolonAppender.py | \
#python3 "$DIR"/custom/DoubleNewlineInserter.py | \
"$DIR"/bin/clang-format-3.8-custom -style=file | \
#python3 "$DIR"/custom/GenericCategoryLinebreakIndentation.py | \
python3 "$DIR"/custom/ParameterAfterBlockNewline.py | \
python3 "$DIR"/custom/HasIncludeSpaceRemover.py | \
python3 "$DIR"/custom/NewLineAtEndOfFileInserter.py | \
python3 "$DIR"/custom/RemoveVoidBlockDeclaration.py | \
python3 "$DIR"/custom/RemoveAPIAvailableSemicolon.py
