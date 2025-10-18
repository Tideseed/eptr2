import os
from eptr2.tutorials.main import run_app
from eptr2.util.costs import calculate_imb_cost, calculate_diff_cost
from eptr2.composite.price_and_cost import get_hourly_price_and_cost_data


def run_calc_app(username: str, password: str, port: int | None = None):
    script_path = os.path.abspath(__file__)
    run_app(username=username, password=password, script_path=script_path, port=port)


def map_source(source: str):
    if source == "wind":
        return "💨 Rüzgar"
    elif source == "solar":
        return "☀️ Güneş"
    elif source == "other":
        return "Diğer"


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2
    from datetime import datetime, timedelta
    import pytz
    import pandas as pd

    username = os.getenv("EPTR_USERNAME")
    password = os.getenv("EPTR_PASSWORD")

    st.set_page_config(
        page_title="Dengesizlik/Imbalance",
        page_icon="👩‍💻",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    ss = st.session_state
    ss["lang"] = ss.get("lang", "tr")
    ss["eptr"] = ss.get(
        "eptr",
        EPTR2(
            username=username,
            password=password,
            postprocess=True,
        ),
    )

    ss["cdf"] = ss.get("cdf", None)

    ss["stats"] = ss.get("stats", None)
    ss["gen_type"] = ss.get("gen_type", None)

    def get_data():
        refresh_data = True
        if ss["cdf"] is not None:
            print("cdf is not None")
            if ss["date"] == ss["cdf"]["date"][0].date():
                refresh_data = False

        if refresh_data:
            print("Getting data...")
            ss["cdf"] = get_hourly_price_and_cost_data(
                eptr=ss["eptr"],
                start_date=str(ss["date"]),
                end_date=str(ss["date"]),
                include_wap=True,
                add_kupst_cost=True,
                verbose=False,
            )
            # ss["cdf"] = ss["eptr"].call(
            #     "mcp-smp-imb", start_date=str(ss["date"]), end_date=str(ss["date"])
            # )
            ss["cdf"]["date"] = pd.to_datetime(ss["cdf"]["date"])

        ss["stats"] = dict(ss["cdf"][ss["cdf"]["date"].dt.hour == ss["hour"]].iloc[0])

        print("==*****==")
        print(ss["org_type"])
        print(ss["gen_type"])
        print("==*****==")

        ss["stats"]["costs"] = calculate_diff_cost(
            actual=ss["actual"],
            forecast=ss["forecast"],
            prod_source=ss.get("gen_type", None),
            mcp=ss["stats"]["mcp"],
            smp=ss["stats"]["smp"],
            dsg_absorption_rate=1.0,
            return_detail=True,
        )

    st.sidebar.subheader("Parametreler")

    st.sidebar.date_input(
        "Tarih",
        value=datetime.now(tz=pytz.timezone("Europe/Istanbul")) - timedelta(days=1),
        key="date",
    )

    st.sidebar.selectbox(
        "Saat", list(range(24)), format_func=lambda x: f"{x:02d}:00", key="hour"
    )

    st.sidebar.radio(
        "Organizasyon Türü", options=["Tüketici", "Üretici"], key="org_type"
    )

    if ss["org_type"] == "Üretici":
        st.sidebar.radio(
            "Santral Tipi",
            options=["wind", "solar", "other"],
            format_func=lambda x: map_source(x),
            index=2,
            key="gen_type",
        )

    st.sidebar.number_input(
        "Tahmin (MWh)", min_value=0.0, max_value=5000.0, step=0.1, key="forecast"
    )
    st.sidebar.number_input(
        "Gerçekleşme (MWh)", min_value=0.0, max_value=5000.0, step=0.1, key="actual"
    )

    st.sidebar.button("💰 Hesapla", key="calc", on_click=get_data, type="primary")

    st.sidebar.caption(
        "Bu uygulama eptr2 Python kütüphanesinden çalıştırılmaktadır. Fiyat ve maliyetlerde EPİAŞ Şeffaflık Platformu verileri kullanılmaktadır. Bütün hesap ve işlemler bilgilendirme ve eğitimr amaçlıdır. Tideseed/Robokami bilgilerin doğruluğu ile ilgili ve/veya kullanımdan dolayı herhangi bir sorumluluk kabul etmemektedir. Detaylı bilgi için [iletişim formu](https://robokami.com/#iletisim)nu kullanabilirsiniz."
    )

    st.header("eptr2: Fiyat ve Maliyet Hesaplama Eğitimi")

    with st.expander("Fiyat ve Maliyet Tablosu", expanded=False):
        if ss["cdf"] is not None:
            st.dataframe(ss["cdf"])
        else:
            st.warning(
                "Henüz fiyat ve maliyet verileri çekilmedi. Bir tarih seçip Hesapla tuşuna basın."
            )

    # with st.expander("Debug", expanded=False):

    #     st.json(ss)

    if ss["stats"]:
        st.caption(
            "⚡️ Miktar (MWh), 💰 Fiyat (TL/MWh), 💸 Maliyet (TL), 💸💸 Toplam Maliyet (TL)"
        )
        cols = st.columns([3, 3, 3, 3])

        with cols[0]:
            st.metric(
                "PTF 💰", round(ss["stats"]["mcp"], 2), help="Piyasa Takas Fiyatı"
            )
            st.metric(
                "SMF 💰", round(ss["stats"]["smp"], 2), help="Sistem Marjinal Fiyatı"
            )
            st.metric(
                "PDF 💰",
                round(ss["stats"]["pos_imb_price"], 2),
                help="Pozitif Dengesizlik Fiyatı: min(PTF, SMF)*0.97",
            )
            st.metric(
                "NDF 💰",
                round(ss["stats"]["neg_imb_price"], 2),
                help="Negatif Dengesizlik Fiyatı: max(PTF, SMF)*1.03",
            )

        with cols[1]:
            st.metric(
                "PDM 💸",
                round(ss["stats"]["pos_imb_cost"], 2),
                help="Pozitif Dengesizlik Maliyeti: PTF - min(PTF, SMF)*0.97",
            )
            st.metric(
                "NDM 💸",
                round(ss["stats"]["neg_imb_cost"], 2),
                help="Negatif Dengesizlik Maliyeti: max(PTF, SMF)*1.03 - PTF",
            )
            st.metric(
                "Birim KÜPST 💸",
                round(ss["stats"]["kupst_cost"], 2),
                help="Birim KÜPST maliyeti max(PTF,SMF) * 0.03",
            )
            st.metric(
                "Sistem Yönü 🔛",
                ss["stats"]["sd_sign"],
                help="1: Enerji Fazlası, -1: Enerji Açığı, 0: Dengede",
            )

        with cols[2]:
            st.metric(
                "Brüt Dengesizlik ⚡️",
                ss["stats"]["costs"]["imbalances"]["diff"],
                help="Eksi değer negatif dengesizlik, artı deger pozitif dengesizlik demektir.",
            )
            st.metric(
                "DSG Tolerans ⚡️",
                ss["stats"]["costs"]["imbalances"]["imb_tol_value"],
                help="DSG Tolerans Miktarı (Tolerans Oranı: 10%)",
            )
            st.metric(
                "Bireysel Dengesizlik ⚡️",
                ss["stats"]["costs"]["imbalances"]["individual_imbalance"],
                help="DSG toleransı üzerinde kalan dengesizlik miktarı.",
            )

            if ss["org_type"] == "Üretici" and "kupst" in ss["stats"]["costs"].keys():
                st.metric(
                    "KÜPSM Tolerans ⚡️",
                    round(ss["stats"]["costs"]["kupst"]["kupsm_tol"], 2),
                    help="KÜPSM toleransı. Kaynak "
                    + map_source(ss["gen_type"])
                    + "("
                    + format(ss["stats"]["costs"]["kupst"]["kupst_tol_perc"], ".2f")
                    + ")",
                )
                st.metric(
                    "KÜPSM ⚡️",
                    round(ss["stats"]["costs"]["kupst"]["kupsm"], 2),
                    help="KÜPSM",
                )

        with cols[3]:
            ind_cost = round(ss["stats"]["costs"]["costs"]["ind_imbalance_cost"], 2)
            st.metric(
                "Bireysel Dengesizlik Maliyeti 💸",
                ind_cost,
                help="DSG toleransının üzerinde kalan dengesizlik maliyeti.",
            )

            dsg_cost = round(ss["stats"]["costs"]["costs"]["net_dsg_imb_cost"], 2)
            st.metric(
                "DSG İçi Dengesizlik Maliyeti 💸",
                dsg_cost,
                help="DSG toleransında kalıp absorbe edilemeyen dengesizlik maliyeti.",
            )

            if ss["org_type"] == "Üretici" and "kupst" in ss["stats"]["costs"].keys():
                kupst_cost = round(ss["stats"]["costs"]["kupst"]["kupst_cost"], 2)
                st.metric(
                    "KÜPST 💸",
                    kupst_cost,
                    help="KÜPSM",
                )
            else:
                kupst_cost = 0

            total_cost = ind_cost + dsg_cost + kupst_cost

            st.metric(
                "Toplam Maliyet 💸💸",
                f"{total_cost} TL",
                help="Dengesizlik maliyetleri + KÜPST maliyeti.",
            )

            unit_cost = round(total_cost / max(1, ss["actual"]))

            st.metric(
                "Birim Maliyet 💸⚖️",
                f"{unit_cost} TL/MWh",
                help="Birim dengesizlik maliyetleri + KÜPST maliyeti.",
            )
    else:
        st.info("Hesapla tuşuna basarak değerleri görüntüleyebilirsiniz.")
    # if ss["cdf"] is not None:
    #     st.dataframe(ss["cdf"])
