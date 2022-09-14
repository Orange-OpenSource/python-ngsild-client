#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import asyncio
import httpx
from ngsildclient import Entity, AsyncClient, iso8601, Auto

COINGECKO_BTC_CAP_ENDPOINT = "https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin"
DATA_PROVIDER = "CoinGecko API"


def build_entity(company: dict) -> Entity:
    market, symbol = [x.strip() for x in company["symbol"].split(":")]
    e = Entity("BitcoinCapitalization", f"{market}:{symbol}:{iso8601.utcnow()}")
    e.obs()
    e.prop("dataProvider", DATA_PROVIDER)
    e.prop("companyName", company["name"])
    e.prop("stockMarket", market)
    e.prop("stockSymbol", symbol)
    e.prop("country", company["country"])
    e.prop("totalHoldings", company["total_holdings"], unitcode="BTC", observedat=Auto)
    e.prop("totalValue", company["total_current_value_usd"], unitcode="USD", observedat=Auto)
    return e


async def main():
    client = AsyncClient()
    r = httpx.get(COINGECKO_BTC_CAP_ENDPOINT)
    r.raise_for_status()
    companies = r.json()["companies"]
    for company in companies:
        entity = build_entity(company)
        await client.upsert(entity)


if __name__ == "__main__":
    asyncio.run(main())
