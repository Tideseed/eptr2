def price_and_cost_call():
    ss = st.session_state

    pb = st.progress(0, text="Veri alınıyor...")
    df = get_hourly_price_and_cost_data(
        eptr=ss["eptr"],
        start_date=str(ss["price_cost_start_date"]),
        end_date=str(ss["price_cost_end_date"]),
        include_contract_symbol=True,
        include_wap=True,
        add_kupst_cost=True,
    )
    pb.progress(100, text="Veri alındı.")
    time.sleep(0.3)
    pb.empty()

    if ss.get("price_cost_column_names_tr", False):
        df = df.rename(
            columns={
                "date": "Tarih-Saat",
                "mcp": "PTF",
                "wap": "WAP",
                "smp": "SMF",
                "contract": "GİP Kontrat",
                "pos_imb_price": "Pozitif Deng Fiyatı",
                "neg_imb_price": "Negatif Deng Fiyatı",
                "system_direction": "Sistem Yönü",
                "sd_sign": "SY İşareti",
                "pos_imb_cost": "Pozitif Deng Maliyeti",
                "neg_imb_cost": "Negatif Deng Maliyeti",
                "kupst_cost": "Birim KÜPST",
            }
        )

    ss["price_and_cost_data"] = df.copy()


def price_and_cost_code():
    ss = st.session_state

    text = f"""
    from eptr2 import EPTR2
    from eptr2.composite import get_hourly_price_and_cost_data
    df = get_hourly_price_and_cost_data(
        eptr=eptr,
        start_date="{str(ss["price_cost_start_date"])}",
        end_date="{str(ss["price_cost_end_date"])}",
        include_contract_symbol=True,
        include_wap=True,
        add_kupst_cost=True
    )
    """

    st.code(text, language="python")


def price_and_cost_main():
    st.title("Fiyat ve Maliyetler")
    ss = st.session_state

    # st.json(ss)

    if "eptr" not in ss:
        st.badge(
            "EPTR2'ye bu servis için bağlı değilsiniz. Ana sayfadan giriş yapabilirsiniz.",
            color="red",
            icon="❌",
        )
        st.stop()
    else:
        eptr: EPTR2 = ss["eptr"]

    sidebar_common()
    tomorrow_str = offset_date_by_n_days(str(get_today_utc3()), n=1)

    date_cols = st.columns([2, 2, 3, 1])
    with date_cols[0]:
        start_date = st.date_input(
            "Başlangıç Tarihi",
            value=get_previous_day(),
            key="price_cost_start_date",
            max_value=tomorrow_str,
        )

    with date_cols[1]:
        end_date = st.date_input(
            "Bitiş Tarihi",
            value=min(
                tomorrow_str,
                max(
                    str(start_date),
                    (
                        str(ss["price_cost_end_date"])
                        if ss.get("price_cost_end_date", "") != ""
                        else get_previous_day()
                    ),
                ),
            ),
            key="price_cost_end_date",
            min_value=start_date,
            max_value=tomorrow_str,
        )

    with date_cols[2]:
        st.write('<div style="height: 28px;"></div>', unsafe_allow_html=True)
        st.button(
            "Hesapla",
            type="secondary",
            key="price_cost_calculate",
            icon="💰",
            on_click=price_and_cost_call,
        )

    st.checkbox(
        "Sütun İsimlerini Düzenle", key="price_cost_column_names_tr", value=True
    )

    if "price_and_cost_data" in ss:
        st.subheader("Fiyat ve Maliyetler")
        st.caption("Not: Bu tabloyu sağ üst köşeden csv olarak indirebilirsiniz.")

        st.dataframe(
            ss["price_and_cost_data"], use_container_width=True, hide_index=True
        )
        price_and_cost_code()


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2
    from eptr2.composite import get_hourly_price_and_cost_data
    from eptr2.util.time import get_previous_day, get_today_utc3, offset_date_by_n_days
    import re
    import pandas as pd
    from eptr2.tutorials.composite.common import sidebar_common
    import time

    st.set_page_config(
        page_title="Fiyat ve Maliyetler",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    price_and_cost_main()
