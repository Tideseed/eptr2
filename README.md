![PyPI - Version](https://img.shields.io/pypi/v/eptr2) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2) 

# Quickstart

This document is a quickstart guide for `eptr2` package. It is a Python client for [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) API. It is an unofficial package with Apache License 2.0.

## Installation

You can easily install it from PyPI with the following commmand.

```bash
pip install eptr2
```

If you want to the additional features, it is recommended to install it with the extras. Extras currently include `pandas` and `streamlit`. You can install the package with the following command.

```bash
pip install "eptr2[allextras]"
```

## Usage

You can simply use `EPTR2` class to call services with convenience methods. You need to [register](https://kayit.epias.com.tr/epias-transparency-platform-registration-form) with the [EPIAS Transparency Platform](https://seffaflik.epias.com.tr/) to get your username (i.e. registration email) and password. The platform also accommodates an English version.

Below is an example of getting Market Clearing Price (MCP) / Piyasa Takas Fiyatı (PTF). All services use the same pattern.

```python
from eptr2 import EPTR2

eptr = EPTR2(
    username="YOUR_USERNAME", password="YOUR_PASSWORD"
)

res = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

There are more than 213 calls available. You can search for available calls with `eptr.get_available_calls()` function. This is almost an exhaustive list of available calls in the platform currently. 

### Live Tutorial

Starting from version 1.0.0, `eptr2` package includes a live tutorial feature as a Streamlit app (p.s. You need to have Streamlit installed). You can run the following code to start the tutorial. Its functionality is almost the same as [eptr2demo app](https://eptr2demo.streamlit.app/).

```python
from eptr2.tutorials import run_demo_app

run_demo_app(username="YOUR_USERNAME",password="YOUR_PASSWORD")
```

_More tutorials are expected to be added in the future._

# About EPIAS Transparency Platform v2.0 Python client by Robokami Data

🇬🇧 `eptr2` (**EP**IAS **Tr**ansparency **2**.0) package is a thin wrapper around [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) API brought to you by [Robokami](https://robokami.com). It is an unofficial package with Apache License 2.0 (free and permissable use for commercial applications, [see details](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)). `eptr2` accesses currently more than 213 services with convenience methods.


🇹🇷 `eptr2` (**EP**İAŞ **Tr**ansparency **2**.0) paketi [Robokami](https://robokami.com) tarafından [EPİAŞ Şeffaflık Platformu 2.0](https://seffaflik.epias.com.tr/home) API'si üzerine geliştirilmiş bir Python paketidir. Apache License 2.0 ile lisanslanmıştır ([ücretsiz ve büyük ölçüde serbest kullanım](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)). `eptr2` 213'ten fazla veri servisine erişim sağlar.


## Advanced Topics

### Aliases

There are default aliases for the calls. For instance, "ptf" is an alias for "mcp". You can use aliases to call services. 

```python
res = eptr.call("ptf", start_date="2024-07-29", end_date="2024-07-29")
```

You can also create aliases for your calls. Just prepare an alias dictionary and add it to the `EPTR2` object. 

```python
custom_aliases = {"market-clearing-price": "mcp", "system-marginal-price": "smp"}

eptr = EPTR2(username="YOUR_USERNAME",password="YOUR_PASSWORD", custom_aliases=custom_aliases)
```

As a warning aliases may overwrite the default keys and default aliases. For instance if your alias is "mcp" pointing to "smp", now default "mcp" call is overwritten with "mcp" alias pointing to "smp".

Library will also have default aliases. You can check aliases with `eptr.get_aliases()` function. If you want to include custom aliases, you can get them with `include_custom_aliases` parameter. `eptr.get_available_calls()` function may also include aliases.

```python
eptr.get_aliases(include_custom_aliases = True)

eptr.get_available_calls(include_aliases = True)
```

### Composite Functions

_New feature from version 1.0.0_

Composite functions are combinations of multiple calls under a single table for a purpose. That purpose might be to gather reporting data or training data for forecast models. You can create your own composite functions with `eptr2` package or use already available ones. 

An side note: We process and manipulate data in composite functions so it is not just the merged data frames of base eptr2 calls.

#### Hourly Consumption and Forecast Data

Our first composite function is `get_hourly_consumption_and_forecast_data`. It returns a data frame with a combination of Load Plan, UECM and Real Time Consumption.

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_consumption_and_forecast_data

eptr = EPTR2(username="YOUR_USERNAME",password="YOUR_PASSWORD")
df = get_hourly_consumption_and_forecast_data(eptr, start_date="2024-07-29", end_date="2024-07-29")
print(df)
```

#### Price and Cost

Our second set of composite functions is about prices and costs. 

+ `get_price_and_cost`: It returns a data frame with a combination of MCP, SMP, WAP (optional) and associated imbalance and KUPST (optional) costs.
+ `get_imbalance_data`: It returns a data frame with a combination of Imbalance Prices, Imbalance Volumes and Imbalance Costs (optional).

```python
from eptr2 import EPTR2
from eptr2.composite import get_price_and_cost, get_imbalance_data

eptr = EPTR2(username="YOUR_USERNAME",password="YOUR_PASSWORD")
df_cost = get_price_and_cost(eptr, start_date="2024-07-29", end_date="2024-07-29")
print(df_cost)
df_imbalance = get_imbalance_data(eptr, start_date="2024-07-29", end_date="2024-07-29")
print(df_imbalance)
```