
import numpy as np

def gaussian_kernel(sigma):
    """The gaussian kernel.
    $$w(\tau) = \\frac{1}{\sqrt{2 \pi} \sigma_w}
    \exp(-\\frac{\\tau^2}{2 \sigma^2_w})$$
    """
    return lambda t: 1/(np.sqrt(2*np.pi)*sigma) * np.exp(-t**2/(2*sigma**2))

def causal_kernel(alpha):
    """The causal kernel.
    $$w(\\tau) = [\\alpha^2 \\tau \exp(- \\alpha \\tau)]_+$$
    """
    def causal(t):
        v = alpha**2 * t * np.exp(-alpha*t)
        v[v<0] = 0
        return v
    return causal

def rectangular_kernel(delta):
    """Moving rectangular kernel.
    $$ w(\tau) = \begin{cases}
    \frac{1}{\Delta t} &,\ -\frac{\Delta t}{2} \leq t \leq \frac{\Delta t}{2} \\
    0 &,\ otherwise
    \end{cases}$$
    """
    return lambda t: np.ones_like(t[(t>=-delta/2)&(t<=delta/2)]) / delta

def kernel(name, **args):
    """Get the kernel function.

    Kernels:
        - gaussian, args: [sigma]
        - causal, args: [alpha]
        - square, args: [delta]

    Args:
        name:   name of the kernel
        **args: arguments for each kernel.

    Return:
        kernel function in lambda.
    """
    if name == "gaussian":
        return gaussian_kernel(**args)
    elif name == "causal":
        return causal_kernel(**args)
    elif name=="square":
        return rectangular_kernel(**args)
    else:
        raise NameError("unkown kernel: "+str(name))


def _check_and_convert_to_ndarray(subject):
    if isinstance(subject,SpikeUnit.SpikeUnit):
        target = subject.spike_train
    elif isinstance(subject,list):
        target = np.array(subject)
    elif isinstance(subject, np.array):
        target = subject
    else:
        raise ValueError("type of to is not supported: "+str(type(to)))
    return target


def generate_linear_filter(to, kernel):
    target = _check_and_convert_to_ndarray(to)
    return lambda t: np.sum(kernel(train - t))


def apply_linear_filter(to, kernel, x_range=None, step=10000):
    target = _check_and_convert_to_ndarray(to)
    linear_filter = generate_linear_filter(to, kernel)

    if x_range == None:
        x_range = np.linspace(0, target[-1], step)
    return x_range, np.array(list(map(linear_filter, x_range)))  # XXX
