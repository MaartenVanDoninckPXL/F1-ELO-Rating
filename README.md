# F1-ELO-Rating

## Formula 1 Elo Rating System
### Calculate the expected win probability for each based on their current ELO difference:

``` python
expected_score_winner = 1 / (1 + 10 ** ((elo_loser - elo_winner) / 400))
expected_score_loser = 1 - expected_score_winner
```

### ELO update formula:
``` python
K = 20  # Sensitivity factor, can be tuned

elo_winner += K * (1 - expected_score_winner)
elo_loser  += K * (0 - expected_score_loser)
```