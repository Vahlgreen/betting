import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv("fodbold.csv")

def LowBet(data):
    lowestWon = []
    for index,row in data.iterrows():
        if (row["away_odds"]<row["home_odds"] and row["away_score"]>row["home_score"]) or (row["away_odds"]>row["home_odds"] and row["away_score"]<row["home_score"]):
            lowestWon.append(True)
        else:
            lowestWon.append(False)

    data["lowestWon"] = lowestWon



    print(f"This strategy is winning in {data['lowestWon'].sum()/len(data)}% of the matches")

    profit = 0
    profit_list = []
    stake = 100

    for index,row in data.iterrows():
        if row["lowestWon"]==True:
            profit += stake*(min(row["away_odds"],row["home_odds"])-1)
            profit_list.append(profit)
        else:
            profit -= stake
            profit_list.append(profit)

        print(f"{row['lowestWon']}, {row['home_odds']}, {row['away_odds']}, {profit}")

    print(f"profit by betting the same amount on each game: {profit}")
    plt.plot(profit_list)
    plt.show()


LowBet(data)