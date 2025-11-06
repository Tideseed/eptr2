![PyPI - Version](https://img.shields.io/pypi/v/eptr2) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2) 

**!! CRITICAL: Due to authentication method changes you are strongly recommended to update the eptr2 version to 1.2.4+**

**Note: From 1.3.0 and onwards, eptr2 starts to evolve to be an AI oriented tool. You can use it as an MCP server, directly use them in your LLMs and AI agents to write your code for you.**

# Quickstart

This document is a quickstart guide for `eptr2` package. It is a Python client for [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) API. It is an unofficial package with Apache License 2.0.

+ For live demo, please visit <https://eptr2demo.streamlit.app/>
+ For local demo, you can run `eptr2demo` at terminal after installing the library.


# MCP Server Quick Reference

+ You can use Claude Desktop configuration to connect to the MCP server in VS Code as well. See Claude Desktop configuration details [here](https://modelcontextprotocol.io/docs/develop/connect-local-servers).
+ Make sure in VS Code settings `chat.mcp.discovery.enabled` is enabled and `chat.mcp.access` is set to the correct value. See details in [VS Code documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers).


## Installation

RECOMMENDED: Install `eptr2` with "allextras" option to get additional features. Extras currently include `pandas` and `streamlit` libraries. You can install the package with the following command.

```bash
pip install "eptr2[allextras]"
```

**Note:** The `[allextras]` option includes MCP server support for AI agent integration, along with pandas and streamlit.

Otherwise you can easily install it from PyPI with the following commmand.

```bash
pip install eptr2
```

You can also use `uv` tool to install the package with extras or plain.

```bash
uv pip install "eptr2[allextras]"
```

```bash
uv pip install eptr2
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


### Alternative: Using .env file for credentials and TGT recycling

Starting from version `1.2.3`, you can use ".env" file to store credentials and recycle TGT (Ticket Granting Ticket) automatically. Recycling TGT allows you to create wrapper functions without the need to carry `EPTR2` object directly or having to create TGTs for each call (which may be throttled). TGT information is stored in the target path (default is current directory) under the file name `.eptr2-tgt` and reused until it expires.

```python
from eptr2 import EPTR2

eptr = EPTR2(
    use_dotenv=True,  ## Default: True
    recycle_tgt=True, ## Default: False
    dotenv_path=".env" ## Default: "".env"
    tgt_path="." ## Default: ".", included as a kwarg
    )

df = eptr.call("mcp", start_date="2025-08-01",end_date="2025-08-31")
```

`.env` file is simply a text file with the following content. You need to create it in the same directory where you run your script.

```
EPTR_USERNAME=youremail@something.com
EPTR_PASSWORD=yourpassword
```

### Deprecated: Credentials JSON

*This method is being deprecated and will be removed soon.*

From eptr2 version 1.1.0, you can use a new login method that automatically handles TGT (Ticket Granting Ticket) management. This way, TGT is automatically renewed when it expires, and credentials are loaded from a file or environment variables. You need a credentials file (e.g. `creds/eptr_credentials.json`) with the following structure:

```json
{
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}
```

Or, you can generate the credentials file with the following code (ps. you can change the `cred_path` to your desired path, default is `creds/eptr_credentials.json`):

```python
from eptr2 import generate_eptr2_credentials_file

generate_eptr2_credentials_file(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD"
)
```

You can use the following code to create an `EPTR2` object with the new login method (ps. you can change the `cred_path` to your desired path, default is `creds/eptr_credentials.json`):

```python
from eptr2 import eptr_w_tgt_wrapper

eptr = eptr_w_tgt_wrapper()
```


### Live Tutorial

Starting from version 1.0.0, `eptr2` package includes a live tutorial feature as a Streamlit app (p.s. You need to have Streamlit installed). You can run the following code to start the tutorial. Its functionality is almost the same as [eptr2demo app](https://eptr2demo.streamlit.app/).

```python
from eptr2.tutorials import run_demo_app

run_demo_app(username="YOUR_USERNAME",password="YOUR_PASSWORD")
```

### Calculator Tutorial

With version 1.0.2 you can get a calculator tutorial to get imbalance and KÜPST cost estimates for any date and hour with custom actual and forecast values.

```python
from eptr2.tutorials import run_calc_app

run_calc_app(username="YOUR_USERNAME",password="YOUR_PASSWORD")
```


_More tutorials are expected to be added in the future._

## AI Agent Integration (MCP Server)

Starting from version 1.2.4, `eptr2` includes a Model Context Protocol (MCP) server for AI agent integration. This allows AI assistants like Claude to directly query Turkish electricity market data.

### Quick Start

Install with all extras (includes MCP support):

```bash
pip install "eptr2[allextras]"
```

Run the MCP server:

```bash
eptr2-mcp-server
```

Or programmatically:

```python
from eptr2.mcp import run_mcp_server
import asyncio

asyncio.run(run_mcp_server(use_dotenv=True, recycle_tgt=True))
```

### Configuration

Create a `.env` file with your credentials:

```env
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

For Claude Desktop integration, add to your config file:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "eptr2-mcp-server",
      "env": {
        "EPTR_USERNAME": "your.email@example.com",
        "EPTR_PASSWORD": "yourpassword"
      }
    }
  }
}
```

### Available MCP Tools

The server exposes 10 tools for querying electricity market data:
- Market Clearing Price (MCP/PTF)
- System Marginal Price (SMP/SMF)
- Real-time Consumption and Generation
- Demand Forecasts
- Imbalance Prices
- Generic API calls (213+ endpoints)
- Composite data functions

For complete Claude Desktop setup, see [CLAUDE_SETUP.md](CLAUDE_SETUP.md).

For AI agent reference documentation, see [AGENTS.md](AGENTS.md) and [src/eptr2/mcp/README.md](src/eptr2/mcp/README.md).

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

+ `get_hourly_price_and_cost_data`: It returns a data frame with a combination of MCP, SMP, WAP (optional) and associated imbalance and KUPST (optional) costs.
+ `get_imbalance_data`: It returns a data frame with a combination of Imbalance Prices, Imbalance Volumes and Imbalance Costs (optional).

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_price_and_cost_data, get_imbalance_data

eptr = EPTR2(username="YOUR_USERNAME",password="YOUR_PASSWORD")
df_cost = get_hourly_price_and_cost_data(eptr, start_date="2024-07-29", end_date="2024-07-29")
print(df_cost)
df_imbalance = get_imbalance_data(eptr, start_date="2024-07-29", end_date="2024-07-29")
print(df_imbalance)
```

#### Production

With v1.0.2, you can get production and production plan data as well with composite functions. If you know the necessary ids, you can get the specific production values (omit the parameters to get totals).

There are three composite functions. One for getting actual production data (real time, UEVM), one for getting plan data (KGUP v1, KGUP, KUDUP), and one to get both and merge into a single table. Each column except date/time/hour get their own suffix from the data source (e.g. "wind_uevm").

```python
from eptr2 import EPTR2
from eptr2.composite import wrapper_hourly_production_plan_and_realized, get_hourly_production_data, get_hourly_production_plan_data

eptr = EPTR2(username="YOUR_USERNAME",password="YOUR_PASSWORD")

actual_df = get_hourly_production_data(
    eptr=eptr,
    start_date="2024-11-01",
    end_date="2024-11-01",
    rt_pp_id=641,  ## ATATÜRK HES
    uevm_pp_id=142,  ## ATATÜRK HES
    verbose=True,
)


plan_df = get_hourly_production_plan_data(
    eptr=eptr,
    start_date="2024-11-01",
    end_date="2024-11-01",
    org_id=195, ## EÜAŞ
    uevcb_id=3525325, ## ATATÜRK HES
    verbose=True,
)

wrap_df = wrapper_hourly_production_plan_and_realized(
        eptr=eptr, start_date="2024-11-01", end_date="2024-11-01", verbose=True
    )
```

#### Intraday Market (IDM) Logs

You can get the Intraday Market (IDM) logs with the following composite function. It returns a data frame with a combination of IDM logs and their details.

```python
from eptr2 import EPTR2
from eptr2.composite import idm_log_longer, idm_log_period

eptr = EPTR2(credentials_file_path="creds/eptr_credentials.json")

idm_log_longer(eptr=eptr, start_date="2023-01-01", end_date="2023-01-31", verbose=True)
idm_log_period(eptr=eptr, period="2023-01-01", verbose=True)
```

#### Day Ahead and Bilateral Trade Data

```python
from eptr2 import EPTR2
from eptr2.composite import get_day_ahead_and_bilateral_matches, get_day_ahead_detail_info

eptr = EPTR2(credentials_file_path="creds/eptr_credentials.json")

df = get_day_ahead_and_bilateral_matches(eptr=eptr,start_date="2023-01-01", end_date="2023-01-31", verbose=True, include_contract_symbol=True)

df2 = get_day_ahead_detail_info(
    eptr=eptr, start_date="2023-01-01", end_date="2023-01-31", verbose=True
)
```

#### Balancing Power Market Data

```python
from eptr2 import EPTR2
from eptr2.composite import get_bpm_period, get_bpm_range

eptr = EPTR2(credentials_file_path="creds/eptr_credentials.json")
start_date = "2025-05-01"
end_date = "2025-05-31"
df1 = get_bpm_range(
    eptr=eptr, start_date=start_date, end_date=end_date, verbose=True
)

period = "2025-05-01"  # Example period
df2 = get_bpm_period(
    period=period, eptr=eptr, max_lives=2, verbose=True, strict=True
)
```

#### Plant Costs

```python
from eptr2 import EPTR2
from eptr2.composite import gather_and_calculate_plant_costs

eptr = EPTR2(credentials_file_path="creds/eptr_credentials.json")

df = gather_and_calculate_plant_costs(
    eptr=eptr,
    start_date="2023-01-01",
    end_date="2023-01-31",
    pp_id=120,  ## BOZCAADA RES
    org_id=195,  ## EÜAŞ
    uevcb_id=3204384,  ## BOZCAADA RES
    plant_type="wind",
    verbose=True,
    forecast_source = "kgup",
    actual_source = "uevm"
)
```

### Bulk Function Calls

There are three bulk function calls for daily operations: daily production plan (DPP/KGÜP), real time generation and uevcb ids. 

```python
### DPP / KGÜP bulk
dpp_df = eptr.call("dpp-bulk", date="2025-08-31", uevcb_ids=[3208611, 723724, 335505, 106710, 4094])
### Real Time Generation bulk
rt_gen_df = eptr.call("rt-gen-bulk", date="2025-08-31", pp_ids=[11162, 17889, 605, 5005121, 20764])
### UEVCB list bulk
uevcb_df = eptr.call("uevcb-list-bulk", date="2025-08-31", org_ids=[166, 12297, 648, 19880, 162])
```
