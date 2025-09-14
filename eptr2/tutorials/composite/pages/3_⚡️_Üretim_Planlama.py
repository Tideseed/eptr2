def load_gen_orgs():
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]
    # print(str(ss["production_plan_start_date"]))
    gen_orgs_df = eptr.call(
        "gen-org",
        start_date=str(ss["production_plan_start_date"]),
        end_date=str(ss["production_plan_end_date"]),
    )
    gen_orgs_df.sort_values(by="organizationName", inplace=True)
    ss["gen_orgs"] = gen_orgs_df.copy()


def load_gen_uevcbs():

    ss = st.session_state
    # st.json(ss)
    if ss.get("gen_orgs", None) is None or ss.get("gen_org_select", None) is None:
        ss["gen_uevcbs"] = None
        return

    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]
    # print(str(ss["production_plan_start_date"]))
    gen_uevcbs_df = eptr.call(
        "gen-uevcb",
        org_id=ss["gen_org_select"]["organizationId"],
        start_date=str(ss["production_plan_start_date"]),
    )
    gen_uevcbs_df.sort_values(by="name", inplace=True)
    # print(gen_uevcbs_df)
    ss["gen_uevcbs"] = gen_uevcbs_df.copy()


def production_planning_code():
    ss = st.session_state
    the_org_id = ss.get("gen_org_select", {})
    if the_org_id:
        the_org_id = '"' + str(the_org_id.get("organizationId", None)) + '"'
    else:
        the_org_id = "None"

    the_uevcb_id = ss.get("gen_uevcb_select", {})
    if the_uevcb_id:
        the_uevcb_id = '"' + str(the_uevcb_id.get("id", None)) + '"'
    else:
        the_uevcb_id = "None"

    return f"""
    from eptr2 import EPTR2
    from eptr2.composite import get_hourly_production_plan_data

    eptr = EPTR2() ## Kullanıcı adı ve şifreyi yüklemeyi unutmayın
    get_hourly_production_plan_data(
        eptr=eptr,
        start_date="{ss["production_plan_start_date"]}",
        end_date="{ss["production_plan_end_date"]}",
        org_id={the_org_id},
        uevcb_id={the_uevcb_id},
    )

    ## Organizasyon kodlarını öğrenmek için
    ## eptr.call(
    ##    "gen-org", start_date="{str(ss["production_plan_start_date"])}", end_date="{str(ss["production_plan_end_date"])}"
    ## )

    ## UEVÇB kodlarını öğrenmek için
    ## Not: org_id = None değerini almamalı! Örnekler otomatik gerçekleştiği için None değeri görülebilir ama asıl kod için listeden bir organizasyon seçin.
    ## eptr.call(
    ##    "gen-uevcb", org_id={the_org_id}, start_date="{str(ss["production_plan_start_date"])}"
    ## )
    """


def load_hourly_production_plan_data():
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]

    try:

        the_org_d = ss.get("gen_org_select", {})
        if the_org_d:
            the_org_id = the_org_d.get("organizationId", None)
        else:
            the_org_id = None

        the_uevcb_id = ss.get("gen_uevcb_select", {})
        if the_uevcb_id:
            the_uevcb_id = the_uevcb_id.get("id", None)
        else:
            the_uevcb_id = None

        df: pd.DataFrame = get_hourly_production_plan_data(
            eptr=eptr,
            start_date=str(ss["production_plan_start_date"]),
            end_date=str(ss["production_plan_end_date"]),
            org_id=the_org_id,
            uevcb_id=the_uevcb_id,
        )

        if ss.get("gen_org_select", None):
            org_name = ss["gen_org_select"]["organizationName"]
        else:
            org_name = "Tüm Organizasyonlar"

        if ss.get("gen_uevcb_select", None):
            uevcb_name = ss["gen_uevcb_select"]["name"]
        else:
            uevcb_name = "Tüm UEVÇB'ler"

        ss["production_plan_data_title"] = (
            f"{org_name} - {uevcb_name} ({ss['production_plan_start_date']} - {ss['production_plan_end_date']})"
        )
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {str(e)}")
        st.stop()

    df.drop(columns=["org_id"], inplace=True, errors="ignore")

    ss["production_plan_data"] = df.copy()


def production_plan_main():
    st.title("Üretim Planlama Verileri (KGÜP-KUDÜP)")
    ss = st.session_state

    # st.json(ss)

    if "eptr" not in ss:
        st.badge("EPTR2'ye bu servis için bağlı değilsiniz.", color="red", icon="❌")
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
            key="production_plan_start_date",
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
                        str(ss["production_plan_end_date"])
                        if ss.get("production_plan_end_date", "") != ""
                        else get_previous_day()
                    ),
                ),
            ),
            key="production_plan_end_date",
            min_value=start_date,
            max_value=tomorrow_str,
        )

    if "gen_orgs" not in ss:
        load_gen_orgs()

    with date_cols[2]:
        if "gen_orgs" in ss:
            st.write('<div style="height: 28px;"></div>', unsafe_allow_html=True)

            st.button("🏛️ Organizasyonları Güncelle", on_click=load_gen_orgs)

    if "gen_uevcbs" not in ss:
        load_gen_uevcbs()

        # st.badge("Henüz organizasyon listesi bağlı değil.", color="orange", icon="⚠️")
        # st.button("Organizasyonları Yükle", on_click=load_gen_orgs)

    if "gen_orgs" in ss:
        st.selectbox(
            "Organizasyon Seçin",
            options=ss["gen_orgs"].to_dict(orient="records"),
            format_func=lambda x: x["organizationName"],
            key="gen_org_select",
            index=None,
            on_change=load_gen_uevcbs,
        )

        if ss.get("gen_org_select", None):
            st.selectbox(
                "UEVÇB Seçin",
                options=ss["gen_uevcbs"].to_dict(orient="records"),
                format_func=lambda x: x["name"],
                key="gen_uevcb_select",
                index=None,
            )
        # st.checkbox("Sütun İsimlerini Düzenle", key="gen_column_names_tr", value=True)
        st.button(
            "⚡️ Veriyi Yükle",
            on_click=load_hourly_production_plan_data,
        )

        if "production_plan_data" in ss:

            st.subheader(ss["production_plan_data_title"])
            st.caption("Not: Bu tabloyu sağ üst köşeden csv olarak indirebilirsiniz.")
            st.dataframe(ss["production_plan_data"], width="stretch", height=800)

            st.markdown("Python kodu")
            st.code(production_planning_code(), language="python")


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2
    from eptr2.composite import get_hourly_production_plan_data
    from eptr2.util.time import get_previous_day, get_today_utc3, offset_date_by_n_days
    import re
    import pandas as pd
    from eptr2.tutorials.composite.common import sidebar_common

    st.set_page_config(
        page_title="Üretim Planlama (KGÜP, KUDÜP)",
        page_icon="⚡️",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    production_plan_main()
