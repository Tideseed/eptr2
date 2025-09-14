import os
from eptr2.tutorials.main import run_app


def run_demo_app(username: str, password: str, port: int | None = None):
    script_path = os.path.abspath(__file__)
    run_app(username=username, password=password, script_path=script_path, port=port)


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2
    from eptr2.mapping import get_call_help, get_help_d
    from datetime import datetime, timedelta
    from eptr2.mapping.processing import get_postprocess_function
    from eptr2.tutorials.composite.common import sidebar_common

    st.set_page_config(
        page_title="eptr2 Demo",
        page_icon="👩‍💻",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    ss = st.session_state
    ss["lang"] = ss.get("lang", "tr")

    st.title("EPTR2 Demo")

    tra_map = {
        "fm": {
            "tr": "[eptr2](https://www.pypi.org/project/eptr2) Python paketini kullanarak Şeffaflık 2.0 üzerinden istediğiniz API'yi aşağıdaki kodları kullanarak çağırabilirsiniz.",
            "en": "You can call any API on Transparency 2.0 using the [eptr2](https://www.pypi.org/project/eptr2) Python package with the following code.",
        },
        "fw": {
            "tr": "Demo bütün APIler için örnek çağırma yapılamayabilir. İyileştirme çalışmalarımız devam etmektedir.",
            "en": "A sample call may not be made for all APIs. Our improvement works continue.",
        },
    }

    if "eptr" not in ss:
        st.badge("EPTR2'ye bu servis için bağlı değilsiniz.", color="red", icon="❌")
        st.stop()
    else:
        eptr: EPTR2 = ss["eptr"]

    sidebar_common()

    ss["lang"] = ss.get("lang", "tr")

    d = get_help_d()
    # x = get_call_help()
    d2 = {v["title"][ss["lang"]]: {"key": k, **v} for k, v in d.items()}

    all_calls = ss["eptr"].get_available_calls()
    missing_calls = [k for k in all_calls if k not in d.keys()]

    default_values = {
        "start_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "se_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "date_time": (datetime.now() - timedelta(days=1)).strftime(
            "%Y-%m-%dT%H:00:00+03:00"
        ),
        "period": (datetime.now() - timedelta(days=1))
        .replace(day=1)
        .strftime("%Y-%m-%d"),
        "org_id": "294",
        "uevcb_id": "3205891",
        "pp_id": "2800",  ## Real Time generation
        "idm_contract_id": "2066419679",  # PH23050120
        "year": "2021",
        "intl_direction": "TRGR",
        "uevcb_name": "AFY",
    }

    ss["call_data"] = ss.get("call_data", {})

    def call_code(help_d, key, just_body_params=False):
        req_params = help_d["required_body_params"]

        opt_params = help_d["optional_body_params"]
        req_params = req_params + opt_params

        body_param_d = ", ".join(
            [x + "=" + '"' + default_values.get(x, "") + '"' for x in req_params]
        )

        if just_body_params:
            bod_params = {
                x: default_values.get(x, "")
                for x in req_params
                if x in default_values.keys()
            }
            return bod_params

        txt = f"""from eptr2 import EPTR2
    eptr = EPTR2(username="YOUR_EPTR_USERNAME", password="YOUR_EPTR_PASSWORD")

    eptr.call("{key}", {body_param_d})
    """

        return txt

    if st.toggle("🇬🇧 English", value=False):
        if ss["lang"] == "tr":
            ss["lang"] = "en"
            st.rerun()
    elif ss["lang"] == "en":
        ss["lang"] = "tr"
        st.rerun()

    st.markdown(
        "![PyPI - Version](https://img.shields.io/pypi/v/eptr2) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2)"
    )
    st.markdown(tra_map["fm"][ss["lang"]])
    st.warning(tra_map["fw"][ss["lang"]])
    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    with col1:
        st.link_button(
            "✉️ İletişim" if ss["lang"] == "tr" else "✉️ Contact",
            "https://robokami.com/#iletisim",
            type="primary",
            width="stretch",
        )
    with col2:
        try:
            seffaflik_url = ss["call_data"]["help"].get(
                "url", "https://seffaflik.epias.com.tr/transparency"
            )
        except:
            seffaflik_url = "https://seffaflik.epias.com.tr/transparency"

        st.link_button(
            "⚡️ EPİAŞ Şeffaflık" if ss["lang"] == "tr" else "⚡️ EPIAS TP",
            url=seffaflik_url,
            type="secondary",
            width="stretch",
        )
    with col3:
        st.link_button(
            "🔎 Github",
            "https://www.github.com/Tideseed/eptr2",
            width="stretch",
        )
    with col4:
        st.link_button(
            "🐍 PyPI",
            "https://www.pypi.org/project/eptr2",
            width="stretch",
        )

    st.selectbox(
        "Veri seti seçin" if ss["lang"] == "tr" else "Choose a data set",
        list(d2.keys()) + missing_calls,
        key="eptr2_call",
    )

    if ss.get("eptr2_call", None) is not None:
        ss["call_data"] = get_call_help(
            d2[ss["eptr2_call"]]["key"]
            if d2.get(ss["eptr2_call"], None) is not None
            else ss["eptr2_call"]
        )
        st.subheader(
            ss["call_data"]["help"]["title"][ss["lang"]]
            if d2.get(ss["eptr2_call"], None) is not None
            else "_(başlık yok)_"
        )
        st.markdown(
            ss["call_data"]["help"]["desc"][ss["lang"]]
            if d2.get(ss["eptr2_call"], None) is not None
            else "_(açıklama yok)_"
        )

        st.subheader("Örnek Kullanım" if ss["lang"] == "tr" else "Example Usage")

        keyval = (
            d2[ss["eptr2_call"]]["key"]
            if d2.get(ss["eptr2_call"], None) is not None
            else ss["eptr2_call"]
        )
        st.code(
            call_code(
                help_d=ss["call_data"],
                key=keyval,
            ),
            language="python",
        )

        st.subheader("API Sonucu" if ss["lang"] == "tr" else "API Result")

        get_result = st.button(
            "API Sonucunu Getir" if ss["lang"] == "tr" else "Get API Result"
        )

        if get_result:

            try:
                bod_params = call_code(
                    help_d=ss["call_data"],
                    key=d2[ss["eptr2_call"]]["key"],
                    just_body_params=True,
                )

                res_df = ss["eptr"].call(d2[ss["eptr2_call"]]["key"], **bod_params)
                # res_df = get_postprocess_function(keyval)(res=res, key=keyval)
                st.dataframe(res_df)
            except Exception as e:
                print(e)
                st.warning("Bu API için örnek çağırma yapılamadı.")


# st.divider()
# st.subheader("Debug")
# st.json(ss)
