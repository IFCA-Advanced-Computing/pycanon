# Copyright 2022 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Module with different functions which calculate properties about anonymity.

k-anonymity, (alpha,k)-anonymity, l-diversity, entropy l-diversity,
(c,l)-diversity, basic beta-likeness, enhanced beta-likeness, t-closeness and
delta-disclosure privacy.
"""

from ._beta_likeness import basic_beta_likeness
from ._beta_likeness import enhanced_beta_likeness
from ._delta_disclosure import delta_disclosure
from ._k_anonymity import k_anonymity
from ._k_anonymity import alpha_k_anonymity
from ._l_diversity import l_diversity
from ._l_diversity import entropy_l_diversity
from ._l_diversity import recursive_c_l_diversity
from ._t_closeness import t_closeness

__all__ = [
    "basic_beta_likeness",
    "enhanced_beta_likeness",
    "delta_disclosure",
    "k_anonymity",
    "alpha_k_anonymity",
    "l_diversity",
    "entropy_l_diversity",
    "recursive_c_l_diversity",
    "t_closeness",
]
