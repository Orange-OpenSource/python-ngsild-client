#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import pandas as pd
from ngsildclient import Entity, Client, iso8601


def build_entity(specimen: tuple) -> Entity:
    e = Entity("SpecimenObserved", f"{specimen[0]}:{iso8601.utcnow()}")
    e.obs()
    e.prop("specimenName", specimen[0])
    e.prop("legs", specimen[1])
    e.prop("wings", specimen[2])
    e.prop("amountObserved", specimen[3])
    return e


def main():
    client = Client()
    df = pd.DataFrame(
        {"num_legs": [2, 4, 8, 0], "num_wings": [2, 0, 0, 0], "num_specimen_seen": [10, 2, 1, 8]},
        index=["falcon", "dog", "spider", "fish"],
    )
    entities = [build_entity(specimen) for specimen in df.itertuples()]
    client.upsert(entities)


if __name__ == "__main__":
    main()
