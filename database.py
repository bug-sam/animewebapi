recommendations = []

def getNextId():
    if recommendations:
        return recommendations[-1].id + 1
    return 1