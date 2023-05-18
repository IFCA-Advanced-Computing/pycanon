Utility metrics
######################

  The details of the three utility metrics implemented are presented below:
  
  - *Average equivalence class size* (:math:`C_{avg}`): Two versions are implemented depending on whether or not complete rows have been deleted from the original dataset (in this case, *sup=True* in ``get_utility_report_values``). Be *DB* the original database and *DB'* the anonymized one. Be *|EC|* the number of equivalence classes in the anonymized dataset and *k* the verified value for *k-anonymity*: 
  
  .. math::
	  C_{avg} = \left\{ \begin{array}{ll}
		    \frac{|DB'|}{k \hspace{0.1cm} |EC|} & \hspace{0.3cm} \mbox{if } sup=True\\
		    \frac{|DB|}{k \hspace{0.1cm} |EC|} & \mbox{if } sup=False\\
		\end{array}
	    \right.
  
  - *Classification metric (CM)*: This metric is calculted for only one sensitive attribute. Be *N* the number of rows of the raw datatset. Be :math:`penalty(r_{i})=1` if the row :math:`r_{i}` has been suppresed or if its associated sensitive attribute takes a value other than the majority in the equivalence class to which it belongs, and 0 otherwise. The classification metric is defined as folows:
  
  .. math::
  	CM = \frac{1}{N}\sum_{i=1}^{N}penalty(r_{i}),
  	
  
  
  - *Discernability metric* (:math:`DM^{*}`): A version of the classical discernability metric has been considered in order to penalize the deletion of records. Thus, it has been implemented according to the following equation, with *DB* the raw database, *DB'* the anonymized one, :math:`N_{ec}` the number of equivalence classes and :math:`EC_{i}` the *i-th* equivalence class:

  .. math::
  	DM^{*} = \sum_{i=0}^{N_{ec}}|EC_{i}|^{2} + |DB|^{2}-|DB||DB'|
  
**Note:** for the calculation of these three metrics, it is necessary to enter the original dataset prior to anonymization.

