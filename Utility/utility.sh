#!/bin/bash

verify_result() {
    if [[ $? -ne 0 ]]; then
        header $1
        exit 1
    fi
}

print_line() {
    echo "========================"
}

header() {
    print_line
    echo $1
    print_line
}