#!/bin/bash

. ../Utility/utility.sh



create_coauthors="./TriangleCounting/create_coauthorhip.cyph"
triangles="./TriangleCounting/influencing_authors.cyph"
create_communities="./Louvan/createCommunities.cyph"
abs_communities="./Louvan/absCommunities.cyph"
rel_communities="./Louvan/relativeCommunities.cyph"

if [[ ! ( -f "$create_coauthors" ||  -f "$triangles" || \
            -f "$create_communities" ||  \
            -f "$abs_communities" || -f "$rel_communities" ) ]]
then
    header "Cypher script files missing"
    exit 1
fi

# Check for the presence of the cypher-shell
which cypher-shell > /dev/null
verify_result "cypher-shell not available. Exiting..."

if [[ -z "$1" || ! "$1" -eq "skip" ]]; then
    header "Create co-authorhip relations..."
    cat "$create_coauthors" | cypher-shell > /dev/null

    header "Cluster authors in communities..."
    cat "$create_communities" | cypher-shell > /dev/null
fi

header "Get bridging authors through triangle counting..."
cat "$triangles" | cypher-shell > /dev/null

header "Get the number of communities for each author..."
cat "$abs_communities" | cypher-shell > /dev/null

header "Get the normalized number of communities.."
cat "$rel_communities" | cypher-shell > /dev/null
