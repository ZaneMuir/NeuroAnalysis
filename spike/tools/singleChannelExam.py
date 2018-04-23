import matplotlib.pyplot as plt
def previewSingleChannel(train, curve, marker,
                        size=(150,3), xlims=None):
    plt.figure(figsize=size)
    plt.vlines(train, 0, 1)
    plt.vlines(marker, -2, 1)
    plt.plot(curve[0], curve[1])
    if xlims:
        plt.xlim(xlims)
    else:
        plt.xlim((0, int(train[-1])))
    return 


def previewSingleChannel_aligned(train, markers, roi,
                        size=(15,6), xlims=None, width=1):
    start, end, submarkers = roi
    plt.figure(figsize=size)
    for (idx, mark) in enumerate(markers):
        roi_train = train[(mark+start < train) & (train < mark+end)]
        plt.vlines(roi_train-mark, idx-0.5, idx+0.5, linewidth=width)
    plt.vlines(submarkers, -3, -1, color='#78C2C4', linewidth=5)
    plt.xlabel('time (seconds)')
    plt.ylabel('trial number #')
    if xlims:
        plt.xlim(xlims)
    else:
        plt.xlim((start, end))
    return
