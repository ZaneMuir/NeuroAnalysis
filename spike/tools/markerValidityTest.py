import matplotlib.pyplot as plt

def markerPlot(matMarker, csvMarker, size=(100,5)):
    plt.figure(figsize=size)
    plt.vlines(matMarker, 1, 2.5, color='r', label='matMarker')
    plt.vlines(csvMarker, 0, 1.5, color='g', label='csvMarker')
    plt.xlim((0, max([max(matMarker), max(csvMarker)])))
    plt.legend()
    return 