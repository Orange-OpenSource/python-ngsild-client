#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from datetime import datetime, timezone
from ngsildclient.api.helper.temporal import TemporalQuery, TimeProperty


def test_build_temporal_query_before():
    dt = datetime(2022, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    tq = TemporalQuery().before(dt)
    assert tq is not None
    assert tq["timerel"] == "before"
    assert tq["timeAt"] == "2022-09-23T12:00:00Z"

def test_build_temporal_query_before_observedat():
    dt = datetime(2022, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    tq = TemporalQuery().before(dt, TimeProperty.OBSERVED_AT)
    assert tq is not None
    assert tq["timerel"] == "before"
    assert tq["timeAt"] == "2022-09-23T12:00:00Z"
    assert tq["timeproperty"] == "observedAt"

def test_build_temporal_query_before_str():
    tq = TemporalQuery().before("2022-09-23T12:00:00Z")
    assert tq is not None
    assert tq["timerel"] == "before"
    assert tq["timeAt"] == "2022-09-23T12:00:00Z"
    
def test_build_temporal_query_after():
    dt = datetime(2022, 8, 23, 12, 0, 0, tzinfo=timezone.utc)
    tq = TemporalQuery().after(dt)
    assert tq is not None
    assert tq["timerel"] == "after"
    assert tq["timeAt"] == "2022-08-23T12:00:00Z" 

def test_build_temporal_query_after_modifiedat():
    dt = datetime(2022, 8, 23, 12, 0, 0, tzinfo=timezone.utc)
    tq = TemporalQuery().after(dt, TimeProperty.MODIFIED_AT)
    assert tq is not None
    assert tq["timerel"] == "after"
    assert tq["timeAt"] == "2022-08-23T12:00:00Z"
    assert tq["timeproperty"] == "modifiedAt"

def test_build_temporal_query_after_str():
    tq = TemporalQuery().after("2022-08-23T12:00:00Z")
    assert tq is not None
    assert tq["timerel"] == "after"
    assert tq["timeAt"] == "2022-08-23T12:00:00Z"

def test_build_temporal_query_between():
    dt1 = datetime(2022, 8, 23, 12, 0, 0, tzinfo=timezone.utc)
    dt2 = datetime(2022, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    tq = TemporalQuery().between(dt1, dt2)
    assert tq is not None
    assert tq["timerel"] == "between"
    assert tq["timeAt"] == "2022-08-23T12:00:00Z"
    assert tq["endTimeAt"] == "2022-09-23T12:00:00Z"

def test_build_temporal_query_between_createdat():
    dt1 = datetime(2022, 8, 23, 12, 0, 0, tzinfo=timezone.utc)
    dt2 = datetime(2022, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    tq = TemporalQuery().between(dt1, dt2, TimeProperty.CREATED_AT)
    assert tq is not None
    assert tq["timerel"] == "between"
    assert tq["timeAt"] == "2022-08-23T12:00:00Z"
    assert tq["endTimeAt"] == "2022-09-23T12:00:00Z"
    assert tq["timeproperty"] == "createdAt"

def test_build_temporal_query_between_str():
    tq = TemporalQuery().between("2022-08-23T12:00:00Z", "2022-09-23T12:00:00Z")
    assert tq is not None
    assert tq["timerel"] == "between"
    assert tq["timeAt"] == "2022-08-23T12:00:00Z"
    assert tq["endTimeAt"] == "2022-09-23T12:00:00Z"            
