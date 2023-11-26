# EPIAS Transparency Platform v2.0 Python client by Robokami Data

`eptr2` (**EP**IAS **Tr**ansparency **2**.0) package is a thin wrapper around [EPIAS Transparency Platform v2.0](https://seffaflik-prp.epias.com.tr/home) API brought to you by [Robokami](https://robokami.com). It is an unofficial package with Apache License 2.0 (free and permissable use for commercial applications, [see details]()).

> [!IMPORTANT]  
> EPIAS Transparency Platform v2.0 is still in "simulation" mode and expected to go live on Dec. 4, 2023. Breaking changes can be expected.
> A url change is expected at the minimum (<https://seffaflik-prp.epias.com.tr> to <https://seffaflik.epias.com.tr>)

> [!IMPORTANT]  
> `eptr2` is still in active development. Breaking changes can be expected. Fill an [issue](https://github.com/tideseed/eptr2) if you encounter any problem.


## Installation

You can simply use PyPI to install `eptr2` package.

```bash
pip install eptr2
```

or directly through GitHub.

```bash
pip install git+https://github.com/Tideseed/eptr2.git
```

## Usage

There are two types of calls. For instance, let's try to get MCP (PTF) of 2023-10-10.

+ First type is limited with a number of services, but with a better interface. 

```python
from eptr2 import EPTR2

eptr = EPTR2()

mcp = eptr.mcp(start_date="2023-10-10T00:00:00+03:00",end_date="2023-10-10T00:00:00+03:00")
print(mcp.json())

## or directly with the call function
mcp_call = eptr.call("mcp",start_date="2023-10-10T00:00:00+03:00",end_date="2023-10-10T00:00:00+03:00")
print(mcp.json())

## from v0.1.1 you can use date strings instead of datetime objects
mcp = eptr.mcp(start_date="2023-10-10",end_date="2023-10-10")
print(mcp.json())
```

You can search for available calls with `eptr.services` attribute. We plan to include all transparency services in the future.

```python
available_calls = eptr.get_available_calls()
print(available_calls)
```
+ Second type is more flexible, but you need to know the API endpoints and parameters.

```python
from eptr2 import transparency_call

mcp = transparency_call(
    call_path="electricity-service/v1/markets/dam/data/mcp",
    call_method="POST",
    call_body={"startDate":"2023-10-10T00:00:00+03:00","endDate":"2023-10-10T00:00:00+03:00"}
    )

print(mcp.json())
```

> [!IMPORTANT]  
> API requests are currently without local SSL certificate verification (`verify=False`) by default, because of repeated errors encountered due to OpenSSL 3.0 and local system certificate issues. We are aware that this is not a [good safety practice](https://stackoverflow.com/a/66776261/3608936). This issue is expected to be fixed soon. Meanwhile, you can simply add `verify_with_local_ssl=True` to your call to enable local SSL certificate verification.
