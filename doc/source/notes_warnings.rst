Notes and Warnings
######################

.. note::
    In the case of multiple sensitve attributes, two approaches can be
    considered:

    * Calculate the different properties for each sensitive attribute
      individually, and take the maximum or minimum as appropriate (for
      example, the minumum value of :math:`\ell` for :math:`\ell`-diversity and
      the maximum value for :math:`\alpha` in the case of
      (:math:`\alpha`,k)-anonymity).
    * Calculate the different properties for each sensitive attribute
      individually but modifying the set of quasi-identifiers by adding to this
      set, in addition to the initial quasi-identifiers, all the sensitive
      attributes except the one under analysis. Then, as in the previous
      approach, the minimum or maximum of each parameter as appropriate is
      taken. It is important to note that since the set of quasi-identifiers is
      updated each time the calculations are made for each SA, the
      computational cost is much higher in this case.

    Specifically, in order to address this challenge, a parameter gen is
    introduced in all functions except k-anonymity (not applicable). If
    *gen=True* (default value), the process of the first approach is followed:
    generalizing. Otherwise, the second approach is followed, updating the
    quasi-identifiers.


.. warning::
    It's important to take into account that the values of *t* and
   :math:`\delta` for t-closeness and :math:`\delta`-disclosure privacy
   respectively must be strictly greater than the ones obtained using *pyCANON*
   (see the definition of that techniques).

