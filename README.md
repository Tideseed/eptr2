![PyPI - Version](https://img.shields.io/pypi/v/eptr2) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2) 

> [!IMPORTANT]  
> 🇬🇧 EPIAS has declared on July 30, 2024 that they will require credentials when using their Transparency API platform. [According to announcement](https://seffaflik.epias.com.tr/announcements/announcements) changes will be in effect from August 19, 2024 on live servers. Starting from `eptr2` version `0.5.0` you can try the new method on test servers. Don't forget to register from [here](https://giris-prp.epias.com.tr/cas/login) for test access.

> [!ÖNEMLİ]  
> 🇹🇷 EPİAŞ 30 Temmuz 2024 tarihinde Şeffaflık API platformuna erişim için giriş bilgileri istemeye başlayacağını bildirmiştir. [İlgili duyuruya](https://seffaflik.epias.com.tr/announcements/announcements) göre değişiklikler 19 Ağustos 2024 tarihinde canlıya geçecektir. `eptr2` sürüm `0.5.0` itibariyle bu değişikilkleri test sunucularında deneyebilirsiniz. Test erişimi şifreleri için [buradan](https://giris-prp.epias.com.tr/cas/login) kayıt olmayı unutmayın.

```python
from eptr2 import EPTR2

cred_d = {
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "is_test": True, ## Needed to access to test server, default is always False
}

eptr = EPTR2(
    username=cred_d["username"], password=cred_d["password"], is_test=cred_d["is_test"]
)

res = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```


_🇹🇷 Türkçe açıklama için aşağıya bakınız._

> [!IMPORTANT]  
> `eptr2` is still in active development. Breaking changes can be expected. Fill an [issue](https://github.com/tideseed/eptr2/issues) if you encounter any problem.

# EPIAS Transparency Platform v2.0 Python client by Robokami Data

`eptr2` (**EP**IAS **Tr**ansparency **2**.0) package is a thin wrapper around [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) API brought to you by [Robokami](https://robokami.com). It is an unofficial package with Apache License 2.0 (free and permissable use for commercial applications, [see details](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)).


`eptr2` currently more than 110 services with convenience methods. You can also use `transparency_call` function to call any service with any method and body.

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

You can simply use `EPTR2` class to call services with convenience methods. Main object call has some parameters to control the behavior of the package. You can set `ssl_verify` to `False` if you have SSL verification problems. You can set `postprocess` to `False` if you don't want to get data frames as response. You can set `get_raw_response` to `True` if you want to get raw urllib3 response object.

```python
from eptr2 import EPTR2

eptr = EPTR2(
        ssl_verify=True,  ## SSL verification (default: True)
        postprocess=True, ## If you want to get data frames as response (default: True) install pandas
        get_raw_response=False ## If you want to get raw urllib3 response object (default: False)
        )

mcp_call = eptr.call("mcp",start_date="2023-10-10",end_date="2023-10-10")
print(mcp.json())
```

You can search for available calls with `eptr.get_available_calls()` function. We plan to include all transparency services in the future.

```python
available_calls = eptr.get_available_calls()
print(available_calls)
```

You can also directly call the transparency calls but you need to know what you are doing (paths and correct parameters).

```python
from eptr2 import transparency_call

mcp = transparency_call(
    call_path="electricity-service/v1/markets/dam/data/mcp",
    call_method="POST",
    call_body={"startDate":"2023-10-10T00:00:00+03:00","endDate":"2023-10-10T00:00:00+03:00"}
    )

print(mcp.json())
```


## EPİAŞ Şeffaflık Platformu 2.0 Python kütüphanesi (Robokami Data)

`eptr2` (**EP**İAŞ **Tr**ansparency **2**.0) paketi [Robokami](https://robokami.com) tarafından [EPİAŞ Şeffaflık Platformu 2.0](https://seffaflik.epias.com.tr/home) API'si üzerine geliştirilmiş bir Python paketidir. Apache License 2.0 ile lisanslanmıştır ([ücretsiz ve büyük ölçüde serbest kullanım](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)).

Yukarıdaki yükleme ve kullanım talimatları ile hızlıca başlayabilirsiniz.

> [!IMPORTANT]  
> `eptr2` hala aktif olarak geliştirilmektedir. Büyük değişiklikler beklenebilir. Herhangi bir sorunda, [issue](https://github.com/tideseed/eptr2) kısmından istek açabilirsiniz.
