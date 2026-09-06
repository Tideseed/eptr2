[![PyPI - Version](https://img.shields.io/pypi/v/eptr2)](https://pypi.org/project/eptr2/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2)](https://pypi.org/project/eptr2/)
[![PyPI - Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Ftideseed%2Feptr2%2Fmain%2Fpyproject.toml)](https://pypi.org/project/eptr2/)
[![PyPI - License](https://img.shields.io/pypi/l/eptr2)](https://github.com/Tideseed/eptr2/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-tideseed.github.io%2Feptr2-blue)](https://tideseed.github.io/eptr2/)
[![AI agents](https://img.shields.io/badge/AI%20agents-MCP%20%7C%20CLI%20%7C%20Skills-8A2BE2)](https://tideseed.github.io/eptr2/ai-integration/mcp-server/)

# eptr2

`eptr2` (**EP**IAS **Tr**ansparency **2**.0) is a Python client for the [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) API, covering **231 services** of the Turkish electricity and natural gas markets — prices (PTF/SMF), consumption, generation, production plans, market operations and imbalance costs.

It is an unofficial package by [Robokami](https://robokami.com) / [Tideseed](https://tideseed.com), Apache License 2.0.

📖 **Full documentation: <https://tideseed.github.io/eptr2/>** · 🇹🇷 **[Türkçe bölüm aşağıda](#türkçe)**

---

## Getting Started

**1. Get credentials.** [Register with the EPIAS Transparency Platform](https://kayit.epias.com.tr/epias-transparency-platform-registration-form). Your username is the registration e-mail. The platform has an English version too.

**2. Install.**

```bash
pip install "eptr2[allextras]"
```

`[allextras]` adds pandas (DataFrame output) and MCP server support. For a thin client with almost no dependencies, `pip install eptr2` also works. Everything works with `uv pip install` as well.

**3. Store your credentials** in a `.env` file next to your script:

```
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

**4. Make your first call.**

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Market Clearing Price (MCP / PTF) for a single day
df = eptr.call("mcp", start_date="2026-07-01", end_date="2026-07-01")
print(df)
```

`recycle_tgt=True` caches the authentication ticket, so repeated runs do not log in again.

You can also pass credentials directly — handy for notebooks:

```python
eptr = EPTR2(username="your.email@example.com", password="yourpassword")
```

**5. Or skip Python entirely** and use the command line:

```bash
eptr2 call mcp --start-date 2026-07-01 --end-date 2026-07-01 --format csv
```

## Usage

### One call pattern for all 231 services

Every service is reached with the same `call` method and an endpoint key:

```python
eptr.call("mcp",         start_date="2026-07-01", end_date="2026-07-01")  # PTF
eptr.call("smp",         start_date="2026-07-01", end_date="2026-07-01")  # SMF
eptr.call("rt-cons",     start_date="2026-07-01", end_date="2026-07-01")  # Real-time consumption
eptr.call("rt-gen",      start_date="2026-07-01", end_date="2026-07-01")  # Generation by source
eptr.call("mcp-smp-imb", start_date="2026-07-01", end_date="2026-07-01")  # Imbalance prices
```

Turkish aliases work too: `ptf` → `mcp`, `smf` → `smp`.

### Finding the right service

You do **not** need credentials to explore the API:

```bash
eptr2 list                     # all 231 keys grouped by category
eptr2 search dengesizlik       # keyword search, Turkish or English
eptr2 describe mcp             # parameters, method, path, description
```

```python
from eptr2.agentic import search_calls, describe_call

describe_call("uevm")          # required/optional parameters and meaning
```

### Typed convenience wrappers

If you prefer autocomplete and type hints over string keys:

```python
from eptr2.calls import get_mcp, get_smp, get_rt_gen

df = get_mcp(start_date="2026-07-01", end_date="2026-07-01", eptr=eptr)
```

### Composite functions

Ready-made combinations of several calls, cleaned and merged:

```python
from eptr2.composite import (
    get_hourly_price_and_cost_data,        # MCP + SMP + WAP + imbalance/KUPST costs
    get_hourly_consumption_and_forecast_data,
    get_dabi_idm_data,                     # day-ahead + bilateral + intraday volumes
    get_bpm_range,                         # balancing market (YAL/YAT) with SMP
    get_kgup_bulk_range,                   # bulk production PLANS (by UEVCB id)
    get_rt_gen_bulk_range,                 # bulk REALIZED generation (by powerplant id)
)

df = get_hourly_price_and_cost_data(
    start_date="2026-07-01", end_date="2026-07-31", eptr=eptr
)
```

Note the argument order: dates first, the client as the `eptr` keyword.

### Imbalance and KÜPST cost calculations

Pure functions — no API call, no credentials. The regulation period (pre-2026 / 2026) and the price floor/ceiling are derived from the contract code:

```python
from eptr2.util.costs import calculate_unit_price_and_costs_by_contract

calculate_unit_price_and_costs_by_contract(
    contract="PH26070101",          # PHYYMMDDhh
    mcp=4000, smp=4000,
    system_direction="Enerji Açığı", # required when MCP == SMP
)
```

⚠️ When MCP equals SMP the system direction cannot be inferred from prices, and assuming a balanced system **understates the negative imbalance price**. Pass `system_direction` (or `sd_sign`) explicitly; the `systemStatus` field of `mcp-smp-imb` gives it.

### Options for unattended / production use

```python
eptr = EPTR2(
    use_dotenv=True,
    recycle_tgt=True,
    strict_params=True,     # raise on unknown parameters instead of warning
    connect_timeout=10.0,   # seconds (per operation, not a total deadline)
    read_timeout=60.0,
)
```

`strict_params` matters more than it looks: an unknown parameter is dropped from the request, so a misspelled filter (`ppID` instead of `pp_id`) silently turns a filtered query into an unfiltered one. By default eptr2 warns and names the correct parameter; `strict_params=True` makes it an error.

---

## Using eptr2 with AI Agents

`eptr2` ships provider-agnostic tooling — nothing is tied to one model vendor. There are three ways to use it, depending on what your agent is.

### 1. Chat assistants — connect the MCP server

Gives any [Model Context Protocol](https://modelcontextprotocol.io) client (VS Code agent mode, Claude Desktop/Code, Cursor, …) **18 tools**: prices, consumption, generation, market operations, credential-free discovery, and pure imbalance/KÜPST calculators.

```bash
pip install "eptr2[allextras]"
eptr2 mcp-config --client vscode     # or claude-desktop, claude-code, cursor, generic
```

Paste the printed snippet into your client's MCP configuration, fill in your credentials, and ask questions in plain language:

> "What was the market clearing price in Turkey yesterday, and how did it compare with SMP?"

### 2. Coding agents — let them write eptr2 code for you

Point the agent at **[AGENTS.md](AGENTS.md)**, the canonical agent guide (VS Code and Claude Code read it automatically inside this repo). Away from the repo, the agent can learn the whole API on its own, without credentials:

```bash
eptr2 schema --stdout        # machine-readable description of all 231 endpoints
eptr2 describe rt-gen        # exact parameters for one endpoint
eptr2 search üretim          # find endpoints by keyword
```

Install the 7 bundled skills (prices, consumption, generation, imbalance costs, market operations, API discovery, typed wrappers) into any SKILL.md-compatible runtime:

```bash
eptr2 install-skills                 # into ./.agents/skills
eptr2 install-skills --dest user     # into ~/.agents/skills
eptr2 install-skills --client claude  # into ./.claude/skills
eptr2 install-skills --client claude --dest user  # into ~/.claude/skills
```

The skills and MCP server are also packaged together as a portable [Agent Plugin](https://agent-plugins.org): `eptr2 plugin-path`.

### 3. Shell-driven agents — use the CLI

Data goes to stdout (JSON or CSV), diagnostics to stderr, nonzero exit codes on failure, so output pipes cleanly:

```bash
eptr2 call mcp --start-date 2026-07-01 --end-date 2026-07-01 --format json | jq '.[0]'
```

📚 Details: [MCP server](https://tideseed.github.io/eptr2/ai-integration/mcp-server/) · [MCP client setup](https://tideseed.github.io/eptr2/ai-integration/mcp-clients/) · [agent skills](https://tideseed.github.io/eptr2/ai-integration/agent-skills/) · [Agent Plugin](https://tideseed.github.io/eptr2/ai-integration/agent-plugin/) · [CLI](https://tideseed.github.io/eptr2/ai-integration/cli/)

---

## Going Further

| Topic | Documentation |
|-------|---------------|
| All 231 API calls, categories and parameters | [Available API Calls](https://tideseed.github.io/eptr2/user-guide/api-calls/) |
| Typed `get_*` wrapper functions (`eptr2.calls`) | [Convenience Wrappers](https://tideseed.github.io/eptr2/user-guide/convenience-wrappers/) |
| Aliases, bulk calls, DataFrames | [Basic Usage](https://tideseed.github.io/eptr2/user-guide/basic-usage/) · [DataFrames](https://tideseed.github.io/eptr2/user-guide/dataframes/) |
| Composite functions | [Composite Functions](https://tideseed.github.io/eptr2/user-guide/composite-functions/) |
| Imbalance / KÜPST cost calculations | [Utilities API](https://tideseed.github.io/eptr2/api/util/) |
| Turkish market abbreviations (PTF, SMF, KGÜP, …) | [Abbreviations](https://tideseed.github.io/eptr2/reference/abbreviations/) |
| Release history | [Changelog](https://tideseed.github.io/eptr2/reference/changelog/) |

### Development versions

```bash
pip install --pre "eptr2[allextras]"                                          # latest pre-release
pip install "eptr2[allextras] @ git+https://github.com/Tideseed/eptr2.git"    # straight from GitHub
```

Pin a released version with `eptr2==1.3.8` if you need to stay off dev builds.

---

## Türkçe

`eptr2` (**EP**İAŞ **Tr**ansparency **2**.0), [EPİAŞ Şeffaflık Platformu 2.0](https://seffaflik.epias.com.tr/home) API'si üzerine geliştirilmiş bir Python paketidir. Türkiye elektrik ve doğal gaz piyasalarına ait **231 veri servisine** tek bir yapıyla erişim sağlar: PTF/SMF fiyatları, tüketim, üretim, üretim planları (KGÜP/KUDÜP), piyasa işlemleri (GÖP, GİP, DGP, İA) ve dengesizlik maliyetleri.

[Robokami](https://robokami.com) / [Tideseed](https://tideseed.com) tarafından geliştirilen resmi olmayan bir pakettir. Apache License 2.0 ile lisanslanmıştır; ticari kullanım dahil geniş ölçüde serbesttir.

### Kurulum ve ilk adımlar

**1. Kayıt.** [EPİAŞ Şeffaflık Platformu'na kayıt olun](https://kayit.epias.com.tr/epias-transparency-platform-registration-form). Kullanıcı adınız kayıt e-postanızdır.

**2. Kurulum.**

```bash
pip install "eptr2[allextras]"
```

`[allextras]` seçeneği pandas (DataFrame çıktısı) ve MCP sunucu desteğini de kurar. Sadece temel istemci için `pip install eptr2` yeterlidir.

**3. Kimlik bilgileri.** Betiğinizin yanına bir `.env` dosyası oluşturun:

```
EPTR_USERNAME=eposta@ornek.com
EPTR_PASSWORD=sifreniz
```

**4. İlk çağrı.**

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Piyasa Takas Fiyatı (PTF)
df = eptr.call("ptf", start_date="2026-07-01", end_date="2026-07-01")
print(df)
```

`recycle_tgt=True` giriş biletini (TGT) saklar; her çalıştırmada yeniden giriş yapılmaz.

### Kullanım

Tüm servisler aynı desenle çağrılır. Türkçe kısaltmalar takma ad olarak kullanılabilir (`ptf` → `mcp`, `smf` → `smp`):

```python
eptr.call("ptf",         start_date="2026-07-01", end_date="2026-07-01")  # Piyasa Takas Fiyatı
eptr.call("smf",         start_date="2026-07-01", end_date="2026-07-01")  # Sistem Marjinal Fiyatı
eptr.call("rt-cons",     start_date="2026-07-01", end_date="2026-07-01")  # Gerçek zamanlı tüketim
eptr.call("rt-gen",      start_date="2026-07-01", end_date="2026-07-01")  # Kaynak bazlı üretim
eptr.call("mcp-smp-imb", start_date="2026-07-01", end_date="2026-07-01")  # Dengesizlik fiyatları
```

Hangi servisin ne olduğunu **kimlik bilgisi gerekmeden** keşfedebilirsiniz:

```bash
eptr2 list                 # 231 servisin tamamı, kategorilere göre
eptr2 search dengesizlik   # Türkçe veya İngilizce anahtar kelime araması
eptr2 describe uevm        # parametreler, yöntem, açıklama
```

Birden fazla çağrıyı birleştiren hazır fonksiyonlar (composite) da mevcuttur:

```python
from eptr2.composite import get_hourly_price_and_cost_data

# PTF, SMF, AOF ve dengesizlik/KÜPST maliyetleri tek tabloda
df = get_hourly_price_and_cost_data(
    start_date="2026-07-01", end_date="2026-07-31", eptr=eptr
)
```

### Dengesizlik ve KÜPST maliyetleri

API çağrısı gerektirmeyen saf hesaplama fonksiyonlarıdır. Mevzuat dönemi (2026 öncesi / 2026) ve taban-tavan fiyatlar sözleşme kodundan otomatik belirlenir:

```python
from eptr2.util.costs import calculate_unit_price_and_costs_by_contract

calculate_unit_price_and_costs_by_contract(
    contract="PH26070101",           # PHYYAAGGss formatında saatlik sözleşme
    mcp=4000, smp=4000,
    system_direction="Enerji Açığı",  # PTF == SMF ise zorunlu
)
```

⚠️ **Önemli:** PTF ile SMF eşit olduğunda sistem yönü fiyatlardan anlaşılamaz. Bu durumda sistemin dengede olduğu varsayılırsa **negatif dengesizlik fiyatı olduğundan düşük hesaplanır**. `system_direction` değerini (`Enerji Açığı` / `Enerji Fazlası` / `Dengede`) mutlaka belirtin; bu bilgi `mcp-smp-imb` çağrısındaki `systemStatus` alanından alınabilir.

### Yapay zeka ajanlarıyla kullanım

`eptr2`, herhangi bir yapay zeka sağlayıcısına bağlı olmayan araçlar sunar:

- **MCP sunucusu** — VS Code, Claude, Cursor gibi istemcilere 18 araç kazandırır. Yapılandırma çıktısı için: `eptr2 mcp-config --client vscode`
- **Ajan becerileri (skills)** — fiyat analizi, tüketim, üretim, dengesizlik maliyetleri, piyasa işlemleri ve API keşfi için 7 hazır beceri: `eptr2 install-skills`
- **[AGENTS.md](AGENTS.md)** — kod yazan ajanlar için başvuru rehberi
- **Makine tarafından okunabilir şema** — 231 servisin tamamı parametreleriyle: `eptr2 schema --stdout`

Böylece bir yapay zeka asistanına doğrudan "geçen ayın PTF ortalamasını hesapla" ya da "rüzgar santralim için dengesizlik maliyetini çıkar" diyebilir, ajanın sizin için doğru çağrıları yazmasını sağlayabilirsiniz.

### Dokümantasyon

Ayrıntılı ve güncel dokümantasyon: **<https://tideseed.github.io/eptr2/>**
