#!/usr/bin/env python

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

import pathlib
import typing

import tabulate
import typer

from pycanon import anonymity
from pycanon.anonymity.utils import aux_functions

app = typer.Typer()


@app.command()
def k_anonimity(
    filename: pathlib.Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    qi: typing.List[str] = typer.Option(
        ...,
        help="Quasi-identifier, pass it multiple times to define multiple "
             "quasi-identifiers (QI)."
    )
):
    """Calculate k-anonimity."""
    dataset = aux_functions.read_file(filename)
    typer.echo(anonymity.k_anonymity(dataset, qi))


@app.command()
def report(
    filename: pathlib.Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    qi: typing.List[str] = typer.Option(
        ...,
        help="Quasi-identifier, pass it multiple times to define multiple "
             "quasi-identifiers (QI)."
    ),
    sa: typing.List[str] = typer.Option(
        ...,
        help="Sensible attribute, pass it multiple times to define "
             "multiple sensible attributes (SA)."
    ),
    gen: bool = typer.Option(
        True,
        help="Whether to generalize for the case of "
             "multiple SA, if False, the set of QI "
             "is updated for each SA."
    )
):
    """Generate a complete privacy report."""
    dataset = aux_functions.read_file(filename)

    headers = ["Technique", "Values"]

    k_anon = anonymity.k_anonymity(dataset, qi)
    alpha, alpha_k = anonymity.alpha_k_anonymity(dataset, qi, sa, gen=gen)
    l_div = anonymity.l_diversity(dataset, qi, sa, gen=gen)
    entropy_l = anonymity.entropy_l_diversity(dataset, qi, sa, gen=gen)
    c_div, l_c_div = anonymity.recursive_c_l_diversity(dataset, qi, sa,
                                                       imp=False, gen=gen)
    basic_beta = anonymity.basic_beta_likeness(dataset, qi, sa, gen=gen)
    enhanced_beta = anonymity.enhanced_beta_likeness(dataset, qi, sa, gen=gen)
    delta_disc = anonymity.delta_disclosure(dataset, qi, sa, gen=gen)
    t_clos = anonymity.t_closeness(dataset, qi, sa, gen=gen)

    vals = [
        ["k-anonimity", f"k = {k_anon}"],
        ["(alpha, k)-anonymity", f"alpha {alpha}; k = {alpha_k}"],
        ["l-diversity", f"l = {l_div}"],
        ["Entropy l-diversity", f"l = {entropy_l}"],
        ["Recursive (c,l)-diversity", f"c = {c_div}; l = {l_c_div}"],
        ["basic beta-likeness", f"beta = {basic_beta}"],
        ["Enhanced beta-likeness", f"beta = {enhanced_beta}"],
        ["t-closeness", f"t = {t_clos}"],
        ["delta-disclosure", f"delta = {delta_disc}"],
    ]

    typer.echo(tabulate.tabulate(vals, headers=headers))


if __name__ == "__main__":
    app()
