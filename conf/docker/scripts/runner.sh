#!/usr/bin/env bash
###############################################################################
# This acts like a helper to execute a command (python or bash) with(out)
# a log showing what is the script about.
###############################################################################
set -e

# Runs script checking for breaking points
run() {
    local RED='\033[1;31m'
    local NC='\033[0m' # No Color
    local RESULT=`$@`
    if [ -z "$RESULT" ]; then
        printf "OK"
        echo ;
    else
        echo ;
        echo ;
        echo -e "${RED}$RESULT${NC}"
        echo ;
        echo ;
        exit 1
    fi
}

# Runs python script checking for breaking points
run_python_script() {
    printf " > $1: "
    python $2
    echo ;
}

# Runs bash script checking for breaking points
run_bash_script() {
    printf " > $1: "
    chmod +x "$2"
    run $2
    echo ;
}

# Runs python script without checking for breaking points
run_python_script_with_output() {
    echo ;
    echo "========================================================================"
    echo " > $1: "
    python $2
    echo ;
    echo "========================================================================"
    echo ;
}

# Runs bash script without checking for breaking points
run_bash_script_with_output() {
    echo ;
    echo "========================================================================"
    echo " > $1: "
    chmod +x "$2"
    $2
    echo ;
    echo "========================================================================"
    echo ;
}