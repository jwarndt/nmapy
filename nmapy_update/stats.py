import numpy as np

def calc_stat(arr, stat_name, axis=None):
    """
    Parameters:
    -----------
    arr: ndarray
        the input array
    stat_name: str
        the name of the statistics.
        "max", "min", "mean", "var", "std"
    axis: int, optional
        the axis over which the statistics is calculated
        
    Returns:
    --------
    out: ndarray
    """
    if stat_name == "all":
        out = np.array([np.amin(arr, axis), np.amax(arr, axis), np.mean(arr, axis), np.var(arr, axis), np.sum(arr, axis)])
    elif stat_name == "min":
        out = np.amin(arr, axis)
    elif stat_name == "max":
        out = np.amax(arr, axis)
    elif stat_name == "var":
        out = np.var(arr, axis)
    elif stat_name == "mean":
        out = np.mean(arr, axis)
    elif stat_name == "std":
        out = np.std(arr, axis)
    else: # stat_name == "sum":
        out = np.sum(arr, axis)
    return out