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


def previewSingleChannel_aligned(train, markers, roi, offset=0,
                                 size=(15, 6), xlims=None, width=1, newfigure=True, 
                                 colorset='black', markersize=(2, 5), newmarker=True,
                                 labelsize='x-large'):
    start, end, submarkers = roi
    if newfigure:
        plt.figure(figsize=size)
    for (idx, mark) in enumerate(markers):
        roi_train = train[(mark+start < train) & (train < mark+end)]
        plt.vlines(roi_train-mark, idx-0.5+offset, idx+0.5+offset, linewidth=width, color=colorset)
    if newmarker:
        plt.vlines(submarkers, -1-markersize[0], -1,
                   color='#78C2C4', linewidth=markersize[1])
    plt.xlabel('time (seconds)',fontsize=labelsize)
    plt.ylabel('trial number #',fontsize=labelsize)
    if xlims:
        plt.xlim(xlims)
    else:
        plt.xlim((start, end))
    return

