![PyPI - Version](https://img.shields.io/pypi/v/eptr2) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2) 

> [!IMPORTANT]  
> 🇬🇧 You will need username and password credentials from EPIAS to access Transparency Platform data. Register through [EPIAS Registration Platform](https://kayit.epias.com.tr/home) and get your username (your email) and password. English version is available. `eptr2` is still in active development. Breaking changes can be expected. Fill an [issue](https://github.com/tideseed/eptr2/issues) if you encounter any problem.

> [!ÖNEMLİ]  
> 🇹🇷 Şeffaflık Platformu verilerine erişmek için EPİAŞ üzerinden kayıt yaparak kullanıcı adı ve şifre almanız gerekmektedir. [EPİAŞ Kayıt Platformu](https://kayit.epias.com.tr/home) üzerinden kullanıcı adınızı (kayıt e-postası) ve şifrenizi alabilirsiniz. `eptr2` hala aktif olarak geliştirilmektedir. Büyük değişiklikler beklenebilir. Herhangi bir sorunda, [issue](https://github.com/tideseed/eptr2) kısmından istek açabilirsiniz.


# EPIAS Transparency Platform v2.0 Python client by Robokami Data

🇬🇧 `eptr2` (**EP**IAS **Tr**ansparency **2**.0) package is a thin wrapper around [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) API brought to you by [Robokami](https://robokami.com). It is an unofficial package with Apache License 2.0 (free and permissable use for commercial applications, [see details](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)). `eptr2` accesses currently more than 175 services with convenience methods.


🇹🇷 `eptr2` (**EP**İAŞ **Tr**ansparency **2**.0) paketi [Robokami](https://robokami.com) tarafından [EPİAŞ Şeffaflık Platformu 2.0](https://seffaflik.epias.com.tr/home) API'si üzerine geliştirilmiş bir Python paketidir. Apache License 2.0 ile lisanslanmıştır ([ücretsiz ve büyük ölçüde serbest kullanım](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)). `eptr2` 175'ten fazla veri servisine erişim sağlar.


## Installation

You can simply use PyPI to install `eptr2` package or directly through GitHub. See [eptr2demo](https://eptr2demo.streamlit.app) page for available calls and examples.

```bash
pip install eptr2
```

NOTE: Starting from v0.4.0, data frame returns will be optional. If pandas is not installed, data frames will not be returned. You can install "dataframe" version with the following command. _(Not implemented yet)_

```bash
pip install "eptr2[dataframe]"
```

```bash
pip install git+https://github.com/Tideseed/eptr2.git
```

## Usage

You can simply use `EPTR2` class to call services with convenience methods. 

```python
from eptr2 import EPTR2

cred_d = {
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "is_test": False, ## (optional) Default: False. Set only to True for transparency test servers.
}

eptr = EPTR2(
    username=cred_d["username"], password=cred_d["password"], is_test=cred_d["is_test"]
)

res = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

You can search for available calls with `eptr.get_available_calls()` function. We plan to include all transparency services in the future.

```python
available_calls = eptr.get_available_calls()
print(available_calls)
```

### Aliases

Starting from `v0.7.0` you can create aliases for your calls. Just prepare an alias dictionary and add it to the `EPTR2` object. 

```python
custom_aliases = {"market-clearing-price": "mcp", "system-marginal-price": "smp"}

eptr = EPTR2(
    username=cred_d["username"], password=cred_d["password"], is_test=cred_d["is_test"], custom_aliases=custom_aliases
)
```

As a warning aliases may overwrite the default keys and default aliases. For instance if your alias is "mcp" pointing to "smp", now default "mcp" call is overwritten with "mcp" alias pointing to "smp".

Library will also have default aliases. You can check aliases with `eptr.get_aliases()` function. If you want to include custom aliases, you can get them with `include_custom_aliases` parameter. `eptr.get_available_calls()` function may also include aliases.

```python
eptr.get_aliases(include_custom_aliases = True)

eptr.get_available_calls(include_aliases = True)
```

## Notes

Main object call has some parameters to control the behavior of the package. 

+ You can set `ssl_verify` to `False` if you have SSL verification problems. 
+ You can set `postprocess` to `False` if you don't want to get data frames as response. 
+ You can set `get_raw_response` to `True` if you want to get raw urllib3 response object.
