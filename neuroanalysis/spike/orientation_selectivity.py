import numpy as np


def calc_gOSI(R, theta=None, unit='rad', scalar=False):
    """
    to calculate the global OSI from the tunning curve.

    argument:
    - R: the response of each direction.

    keyword arguments:
    - theta: the directions. if None, theta will be calculated automatically
             as evenly distributed from [0, 2pi). [default: None]
    - unit: the unit of the theta, either be 'deg' or 'rad'. [default: rad]
    - scalar: if True, return a tuple as (phase, gOSI value) or (angle, gOSI value);
             otherwise, return the complex format. [default: False]

    return:
    - the gOSI complex number or tuple of (phase, gOSI value) or (angle, gOSI value).

    reference:
    - prefOgOSI.m, from Gu's lab
    - Shi et al., Retinal Origin of Direction Selectivity in the Superior Colliculus. [10.1038/nn.4498]
    """

    assert np.ndim(R) == 1, "R must be one dimensional."
    assert isinstance(R, list) or isinstance(R, np.ndarray), "R must be list or numpy.ndarray."

    if isinstance(R, list):
        R = np.array(R)

    if theta == None:
        theta = np.linspace(0,2, len(R)+1)[:-1] * np.pi

    elif isinstance(theta, list) or isinstance(theta, np.ndarray):
        if unit == 'deg':
            theta = np.deg2rad(theta)
        elif unit == 'rad':
            if isinstance(theta, list):
                theta = np.array(theta)
            else:
                pass
        else:
            raise ValueError('unknown unit: %s. choose from \"rad\" or \"deg\".'%unit)


    _gOSI = np.sum(np.exp(theta * 2j) * R) / np.sum(R)

    if scalar:
        _gOSI_v = np.abs(_gOSI)
        _phase = np.angle(_gOSI) / 2

        if unit == 'deg':
            return np.rad2deg(_phase), _gOSI_v
        else:
            return _phase, _gOSI_v
    else:
        return _gOSI


def calc_gDSI(R, theta=None, unit='rad', scalar=False):
    """
    to calculate the global DSI from the tuing curve.

    argument:
    - R: the response of each direction.

    keyword arguments:
    - theta: the directions. if None, theta will be calculated automatically
             as evenly distributed from [0, 2pi). [default: None]
    - unit: the unit of the theta, either be 'deg' or 'rad'. [default: rad]
    - scalar: if True, return a tuple as (phase, gDSI value) or (angle, gDSI value);
             otherwise, return the complex format. [default: False]

    return:
    - the gDSI complex number or tuple of (phase, gDSI value) or (angle, gDSI value).

    reference:
    - prefOgOSI.m, from Gu's lab
    - Shi et al., Retinal Origin of Direction Selectivity in the Superior Colliculus. [10.1038/nn.4498]
    """

    assert np.ndim(R) == 1, "R must be one dimensional."
    assert isinstance(R, list) or isinstance(R, np.ndarray), "R must be list or numpy.ndarray."

    if isinstance(R, list):
        R = np.array(R)

    if theta == None:
        theta = np.linspace(0,2, len(R)+1)[:-1] * np.pi

    elif isinstance(theta, list) or isinstance(theta, np.ndarray):
        if unit == 'deg':
            theta = np.deg2rad(theta)
        elif unit == 'rad':
            if isinstance(theta, list):
                theta = np.array(theta)
            else:
                pass
        else:
            raise ValueError('unknown unit: %s. choose from \"rad\" or \"deg\".'%unit)


    _gDSI = np.sum(np.exp(theta * 1j) * R) / np.sum(R)

    if scalar:
        _gDSI_v = np.abs(_gDSI)
        _phase = np.angle(_gDSI)

        if unit == 'deg':
            return np.rad2deg(_phase), _gDSI_v
        else:
            return _phase, _gDSI_v
    else:
        return _gDSI


def _calc_gDSI(R, theta):
    """
    global direction selectivity index.

    $$ gDSI = \frac{\sum R_{\theta} e^{i \theta}}{\sum R_{\theta}} $$

    arguments:
    - R: 1d array, response
    - theta: 1d array, direction of the stimuli

    return:
    - gDSI: complex number
    """
    assert np.ndim(R) == np.ndim(theta) == 1, "make sure inputs are 1d array."
    assert np.size(R) == np.size(theta), "the size of R is not equal to the size of theta."

    return np.sum(R * np.exp(theta * 1j)) / np.sum(R)


def _calc_gOSI(R, theta):
    """
    global orientation selectivity index.

    $$ gOSI = \frac{\sum R_{\theta} e^{2i \theta}}{\sum R_{\theta}} $$

    arguments:
    - R: 1d array, response
    - theta: 1d array, direction of the stimuli

    return:
    - gOSI: complex number
    """
    assert np.ndim(R) == np.ndim(theta) == 1, "make sure inputs are 1d array."
    assert np.size(R) == np.size(theta), "the size of R is not equal to the size of theta."

    return np.sum(R * np.exp(theta * 2j)) / np.sum(R)


def calc_DSI():
    pass


def calc_OSI():
    pass
