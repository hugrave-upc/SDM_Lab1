#!/bin/bash

# Instantiate the reccomender

. ../Utility/utility.sh

create_community_script="create_community.cyph"
related_community_script="related_communities.cyph"
materialize_top_articles="materialize_top_articles.py"
top_authors_no_mat="top_authors_no_mat.py"
top_authors_with_mat="top_authors_with_mat.py"

if [[ ! ( -f "$create_community_script" || \
            -f "$related_community_script" || \
            -f "$materialize_top_articles" || \
            -f "$top_authors_no_mat" || \
            -f "$top_authors_with_mat" ) ]]
then
    header "Missing files!"
    exit 1
fi


which cypher-shell > /dev/null
verify_result "Impossible to use cypher-shell."

# Create the communities
header "Create communities..."
cat "$create_community_script" | cypher-shell
verify_result "Impossible to create communities"

# Relate Conferences/Journals to communities
header "Relate Conferences/Journals to communities"
cat "$related_community_script" | cypher-shell
verify_result "Impossible to relate conferences and journals to communities"

WITH_MAT=False
while [[ "$WITH_MAT" -eq "False" ]]; do
    print_line
    echo "Materialize the top articles? (Y|n)"
    read answer
    case "$answer" in
        N|n|no|No|NO)
        ;;
        *)
        WITH_MAT=True
        header "Materializing top Articles per community"
        python "$materialize_top_articles"
        verify_result "Impossible to materialize the top articles."
        ;;
    esac

    header "Finding top authors for each community:"
    if [[ "$WITH_MAT" -eq "True" ]]; then
        time python "$top_authors_with_mat"
    else
        time python "$top_authors_no_mat"
    fi
done
