import numpy as np
import itertools as it

"""
Splits given dimensions
"""
def split(X, partSet, repeatDim):
    finalSet = ()
    if len(partSet) == 2:
        return finalSet
    if len(partSet) == 1:
        for i in range(1, len(X) + 1):
            lst = list(it.combinations(X, i))
            for j in range(len(lst)):
                finalSet = finalSet + ((partSet + (lst[j],)),)
        return finalSet
    for i in range(1, len(X)):
        lst = list(it.combinations(X, i))
        for j in range(len(lst)):
            s1 = tuple(set(lst[j] + repeatDim))
            s2 = [x for x in X if x not in s1]
            s1 = (s1,)
            finalSet += split(s2, s1, repeatDim)
    return finalSet


def tensorSum(X, dim, var, ecInd):
    newdim = range(len(X.shape))
    newdim = list(set(newdim) - set(dim))
    dim = newdim
    outputMatSize = []
    outputMatLoop = ()
    for i in range(len(dim)):
        outputMatSize.append(len(var[dim[i]]))
        outputMatLoop += (range(len(var[dim[i]])),)
    outputTensor = np.zeros(outputMatSize)
    for multiIndex in it.product(*outputMatLoop):
        a = []
        dimension = len(X.shape)
        for i in range(dimension):
            a.append(slice(0, X.shape[i]))
        for i in range(len(dim)):
            a[dim[i]] = multiIndex[i]
        outputTensor[multiIndex] = np.sum(X[tuple(a)])
    if ecInd == 1:
        return int(outputTensor.max(axis=0))
    #    plt.hist(outputTensor.ravel(),bins='auto')
    #    plt.show()
    return np.amax(outputTensor).astype(np.int64), np.amin(outputTensor).astype(np.int64)


def tensorIndicator(X, dim, var):
    outputMatSize = []
    outputMatLoop = ()
    for i in range(len(dim)):
        outputMatSize.append(len(var[dim[i]]))
        outputMatLoop += (range(len(var[dim[i]])),)
    outputTensor = np.zeros(outputMatSize)
    for multiIndex in it.product(*outputMatLoop):
        a = []
        dimension = len(X.shape)
        for i in range(dimension):
            a.append(slice(0, X.shape[i]))
        for i in range(len(dim)):
            a[dim[i]] = multiIndex[i]
        if np.count_nonzero(X[tuple(a)]) != 0:
            outputTensor[multiIndex] = 1

    return outputTensor