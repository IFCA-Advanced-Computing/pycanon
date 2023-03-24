# -*- coding: utf-8 -*-

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

"""Module with different auxiliary functions."""

import os
import pathlib
import typing

import numpy as np
import pandas as pd


def read_file(
    file_name: typing.Union[str, pathlib.Path], sep: str = ","
) -> pd.DataFrame:
    """Read the given file. Returns a pandas dataframe.

    :param file_name: file with the data under study.
    :type file_name: string or pathlib.Path

    :param sep: delimiter to use for a csv file.
    :type sep: string

    :return: dataframe with the data.
    :rtype: pandas dataframe.
    """
    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    _, file_extension = os.path.splitext(file_name)
    if file_extension in [".csv", ".xlsx", ".sav", ".txt"]:
        if file_extension in [".csv", ".txt"]:
            data = pd.read_csv(file_name)
        elif file_extension == ".xlsx":
            data = pd.read_excel(file_name)
        else:
            data = pd.read_spss(file_name)
    else:
        raise ValueError("Invalid file extension.")
    return data


def check_qi(
    data: pd.DataFrame, quasi_ident: typing.Union[typing.List, np.ndarray]
) -> None:
    """Check if the entered quasi-identifiers are valid.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings
    """
    cols = data.columns
    err_val = [
        i for i, v in enumerate([qi in cols for qi in quasi_ident]) if v is False
    ]
    if len(err_val) > 0:
        raise ValueError(
            f"Values not defined: {[quasi_ident[i] for i in err_val]}. "
            "Cannot be quasi-identifiers"
        )


def check_sa(
    data: pd.DataFrame, sens_att: typing.Union[typing.List, np.ndarray]
) -> None:
    """Check if the entered sensitive attributes are valid.

    :param data: dataframe with the data under study.
    :type data: pandas dataframe

    :param sens_att: list with the name of the columns of the dataframe
        that are the sensitive attributes.
    :type sens_att: is a list of strings
    """
    cols = data.columns
    err_val = [i for i, v in enumerate([sa in cols for sa in sens_att]) if v is False]
    if len(err_val) > 0:
        raise ValueError(
            f"Values not defined: {[sens_att[i] for i in err_val]}. "
            "Cannot be sensitive attributes"
        )


def intersect(tmp: list) -> list:
    """Intersect two sets: the first and the second of the given list.

    :param tmp: list of sets sorted in decreasing order of
        cardinality
    :type tmp: list of numpy arrays

    :return: list obtained when intersecting the first and the second sets
        of the given list.
    :rtype: list.
    """
    i, j = 0, 0
    tmp_new = []
    while i < len(tmp[0]):
        tmp1 = tmp[0][i]
        tmp2 = tmp[1][j]
        tmp_new.append(np.intersect1d(tmp1, tmp2))
        if j < len(tmp[1]) - 1:
            j += 1
        else:
            j = 0
            i += 1
    tmp[1] = tmp_new
    tmp = tmp[1:]
    return tmp


def convert(ec_set: set) -> list:
    """Convert a set with an equivalence class to a list.

    :param ec_set: set which will be convert into a list.
    :type ec_set: set

    :return: equivalence class into a list.
    :rtype: list.
    """
    return [
        *ec_set,
    ]
