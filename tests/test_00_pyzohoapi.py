# This file is part of pyZohoAPI, Copyright (C) Todd D. Esposito 2021.
# Distributed under the MIT License (see http://opensource.org/licenses/MIT).

import copy
import datetime

import pytest

from pyzohoapi import ZohoInventory
from pyzohoapi.core import ZohoAPIBase
from pyzohoapi.exceptions import ZohoInsufficientAuthKeys, ZohoUnknownRegionException

from private import testdata

def test_api_bad_region():
    with pytest.raises(ZohoUnknownRegionException):
        z = ZohoAPIBase(testdata['orgid'], "really-bad-region-name", **testdata['api'])

def test_api_expired_access_token():
    tokens = copy.copy(testdata['api'])
    del tokens['refresh_token']
    del tokens['client_id']
    del tokens['client_secret']
    z = ZohoAPIBase(testdata['orgid'], testdata['region'], **tokens)
    with pytest.raises(ZohoInsufficientAuthKeys):
        z.auth_header()

def test_api_invalid_access_token():
    z = ZohoInventory(testdata['orgid'], testdata['region'], **testdata['api'])
    # Force a call so we get a valid access_token
    u = z.User().First()
    assert u.IsLoaded
    token = z.auth_header()
    z._api_keys['access_token'] = "1000.badtoken"   # but not expired
    u = z.User().First()
    assert u.IsLoaded

def test_api_refresh_access_token():
    z = ZohoAPIBase(testdata['orgid'], testdata['region'], **testdata['api'])
    new_token = z.auth_header()
    assert z._api_keys['expires_in'] >= 0

def test_api_intercall_delay():
    z = ZohoInventory(testdata['orgid'], testdata['region'], intercall_delay=4, **testdata['api'])
    start = datetime.datetime.now().timestamp()
    # We don't care about the actual results, just the timing.
    rsp1 = z.get('users', "email=testing.example.com")
    rsp2 = z.get('users', "email=testing.example.com")
    assert datetime.datetime.now().timestamp() - start >= 4
