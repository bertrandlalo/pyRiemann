"""Design filters """

from scipy.signal import iirfilter, firwin


def design_filter(frequencies: list, order: int, fs: float = 1.0, filter_design="fir",
                  filter_type: str = 'bandpass', **kwargs):
    """ FIR / IIR filter design given order and critical points.

    Parameters
    ----------
    order: int
        Order of the FIR filter.
    frequencies: float | list
        Cutoff frequency of filter OR a list of cutoff frequencies (that is, band edges).
     fs: scalar
        Nominal rate of the data.
    filter_design: str
        Design of filter to use ('iir' or 'fir'). Default to 'fir'.
    filter_type: str
         Type of filter to use ('bandpass', 'bandstop', 'lowpass' or 'highpass').
         Default to 'bandpass'.
    kwargs:
        Keywords aruments to pass to the filter design functions:
            - when filter_type is 'fir', see additional keyword args such as rp, rs, ..., at
            scipy.signal.iirfilter:<https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.iirfilter.html>
            - when filter_type is 'iir', see additional keyword args width, window, pass_zero and scale
            at scipy.signal.firwin:<https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.firwin.html>

    Returns
    -------
    b, a : ndarray, ndarray
            Numerator (`b`) and denominator (`a`) polynomials of the filter.
    """
    if filter_type not in ['bandpass', 'bandstop', 'lowpass', 'highpass']:
        raise ValueError('type should be bandpass, bandstop, highpass or lowpass')

    if filter_design not in ['fir', 'iir']:
        raise ValueError('design should be fir or iir')

    # define the function to apply to the selected columns
    if filter_design == 'fir':
        if filter_type == 'bandpass':
            b = firwin(numtaps=order + 1, cutoff=frequencies, fs=fs, pass_zero=False, **kwargs)
        elif filter_type == 'bandstop':
            b = firwin(numtaps=order + 1, cutoff=frequencies, fs=fs, pass_zero=True, **kwargs)
        elif filter_type == 'highpass':
            b = firwin(numtaps=order + 1, cutoff=frequencies, fs=fs, pass_zero=False, **kwargs)
        elif filter_type == 'lowpass':
            b = firwin(numtaps=order + 1, cutoff=frequencies, fs=fs, pass_zero=True, **kwargs)
        a = 1
        filter_args = (b, a)
    else:  # filter_design == 'iir':
        kwargs.setdefault('output', 'ba')
        filter_args = iirfilter(order, Wn=frequencies, btype=filter_type, fs=fs, **kwargs)
    return filter_args
