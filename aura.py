
def aura_ranking():
    leaderboard = ['Leul', 'Dilsh', 'Sathvik', 'Kush', 'David', 'Adi']
    ranking = "=" * 50 + "\n"
    ranking += "Aura Leaderboard: " + "\n"
    ranking += "=" * 50 + "\n"

    for i, person in enumerate(leaderboard, 1):
        ranking += f"{i}. {person}" + "\n"

    return ranking