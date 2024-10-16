#!/usr/bin/env bash

white_heuristics=("defensive" "aggresor")
black_heuristics=("evasive" "conqueror")

for black_heuristic in "${black_heuristics[@]}"; do
    echo "Testing against $black_heuristic"
    for white_heuristic in "${white_heuristics[@]}"; do
        echo "Testing heuristic: $white_heuristic"
        win_count=0
        total_count=50
        
        for ((i=1; i<=$total_count; i++)); do
            result=$(python3 main.py -r 8 -c 8 -p 2 -w "$white_heuristic" -b "$black_heuristic" -t)
            if [ "$result" = "O" ]; then
                ((win_count++))
            fi
        done
        
        win_rate=$(bc <<< "scale=2; $win_count / $total_count * 100")

        echo "Win rate for player white vs $black_heuristic with heuristic $white_heuristic: $win_rate%"
    done
    echo "----------------------------------------------------------"
done