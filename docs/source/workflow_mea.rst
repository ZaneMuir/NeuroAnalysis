
Workflow for Multiple Electrode Array recording
***********************************************

Basic workflow and protocols for this project.

Data Recording
==============

Apollo System (Plexon format)
-----------------------------
.. TODO:

NeuroLynx System
----------------
for room 1013

#. Run cheetah.exe
#. choose configuration file: ``20150430.cfg`` 
#. confirm the data directory
#. press ``ACQ`` for acquiring
#. setup visual stimuli (using `Sesame`_)
#. press ``REC`` for recording

Spike Sorting
=============

Offline Sorter
--------------

#. waveform > filter continuous data ``Bessel 4-pole low-cut 300Hz``
#. waveform > detect ``-5 sigma``
#. sort > automatic sorting ``K-means``
#. Tools > invalidate cross-channel ...  ``2 ticks  75%``
#. Tools > remove short ISI waveform ``1ms``
#. mannually check each channel, remove or merge some spikes
#. export to \*.nex file


Spike2
------
#. import \*.nex file 
#. export spike train channels into \*.mat format file (using version7)


Spike Train Analysis
====================

Normalization
-------------
.. TODO:

Linear Filter
-------------

refering to the linear filter formula:

.. math::
    r_{\mathrm{approx}}(t) = \sum_{i=1}^N w(t-t_i) = \int w(\tau) \rho(t-\tau) \; \mathrm{d}\tau

where ``w`` as the kernel function.
here, we use the gaussian kernel with sigma=0.4.

.. math::
    w(\tau) = \frac{1}{\sigma_w \sqrt{2 \pi}} \exp(- \frac{\tau^2}{2 \sigma_w^2})

Python3
^^^^^^^

.. code-block:: python

.. TODO:


Visualization
-------------
.. TODO:



.. _Sesame: https://github.com/ZaneMuir/Sesame