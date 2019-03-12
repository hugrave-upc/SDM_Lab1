#!/bin/bash

. ../Utility/utility.sh


query1="query1.cyph"
query2="query2.cyph"
query3="query3.cyph"
query4a="query4_a.cyph"
query4b="query4_b.cyph"

# verify the existance of the files
if [[ ! ( -f "$query1" || -f "$query2" || \
        -f "$query3" || -f "$query4a" || -f "$query4b" ) ]]
then
    header "Missing queries!"
    exit 1
fi


which cypher-shell > /dev/null
verify_result "cypher-shell utility needs to be in the PATH."

query=$1
if [[ -z "$2" ]]; then
    limit=1000
else
    limit=$2
fi

tmp=tmp.cyph
echo ":param limit $limit;" > "$tmp"

case "$query" in
    1)
    cat "$tmp" "$query1" | cypher-shell --format verbose
    verify_result "Execution of query1 failed"
    ;;
    2)
    cat "$tmp" "$query2" | cypher-shell --format verbose
    verify_result "Execution of query2 failed"
    ;;
    3)
    cat "$tmp" "$query3" | cypher-shell --format verbose
    verify_result "Execution of query3 failed"
    ;;
    4a)
    cat "$tmp" "$query4a" | cypher-shell --format verbose
    verify_result "Execution of query4a failed"
    ;;
    4b)
    cat "$tmp" "$query4b" | cypher-shell --format verbose
    verify_result "Execution of query4b failed"
    ;;
    *)
    echo "Unrecognized query."
    ;;
esac
