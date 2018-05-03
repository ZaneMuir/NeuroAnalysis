import matplotlib.pyplot as plt

def markerPlot(matMarker, csvMarker, size=(100,5)):
    """
Plot markers of mat file and csv file in the same figure,
to check the validity with human eyes.

Args:
    - matMarker: 1-d list/array
    - csvMarker: 1-d list/array
    - size: figure size
    """
    plt.figure(figsize=size)
    plt.vlines(matMarker, 1, 2.5, color='r', label='matMarker')
    plt.vlines(csvMarker, 0, 1.5, color='g', label='csvMarker')
    plt.xlim((0, min([max(matMarker), max(csvMarker)])+10))
    plt.legend()
    return
