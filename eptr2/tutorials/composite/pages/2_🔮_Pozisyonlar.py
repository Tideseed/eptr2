def load_dabi_orgs():
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]
    # print(str(ss["dabi_start_date"]))
    dabi_orgs_df = eptr.call("dam-clearing-org-list", period=str(ss["dabi_start_date"]))
    dabi_orgs_df.sort_values(by="organizationName", inplace=True)
    ss["dabi_orgs"] = dabi_orgs_df.copy()


def dabi_idm_code():
    ss = st.session_state
    return f"""
    from eptr2 import EPTR2
    from eptr2.composite import get_dabi_idm_data

    eptr = EPTR2() ## Kullanıcı adı ve şifreyi yüklemeyi unutmayın
    get_dabi_idm_data(
        eptr=eptr,
        start_date="{ss["dabi_start_date"]}",
        end_date="{ss["dabi_end_date"]}",
        org_id="{ss["dabi_org_select"]["organizationId"]}",
    )

    ## Organizasyon kodlarını öğrenmek için
    ## eptr.call(
    ##    "dam-clearing-org-list", period="{str(ss["dabi_start_date"])}"
    ## )
    """


def load_dabi_idm_data():
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]

    try:
        df: pd.DataFrame = get_dabi_idm_data(
            eptr=eptr,
            start_date=ss["dabi_start_date"],
            end_date=ss["dabi_end_date"],
            org_id=ss["dabi_org_select"]["organizationId"],
        )
        ss["dabi_data_title"] = (
            f"{ss['dabi_org_select']['organizationName']} ({ss['dabi_start_date']} - {ss['dabi_end_date']})"
        )
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {str(e)}")
        st.stop()

    df.drop(columns=["org_id"], inplace=True, errors="ignore")

    if ss.get("dabi_column_names_tr"):
        df.rename(columns={"date": "Tarih", "contract": "Kontrat"}, inplace=True)

        colnames = df.columns.tolist()

        colnames = [re.sub(r"_long", "_Alış", x) for x in colnames]
        colnames = [re.sub(r"_short", "_Satış", x) for x in colnames]
        colnames = [re.sub(r"da_", "GÖP_", x) for x in colnames]
        colnames = [re.sub(r"dabi_", "GÖPİA_", x) for x in colnames]
        colnames = [re.sub(r"bi_", "İA_", x) for x in colnames]
        colnames = [re.sub(r"idm_", "GİP_", x) for x in colnames]
        df.columns = colnames

    ss["dabi_idm_data"] = df.copy()


def dabi_positions_main():
    st.title("GÖP İA GİP Pozisyonları")
    ss = st.session_state

    # st.json(ss)

    if "eptr" not in ss:
        st.badge("EPTR2'ye bu servis için bağlı değilsiniz.", color="red", icon="❌")
        st.stop()
    else:
        eptr: EPTR2 = ss["eptr"]

    sidebar_common()

    date_cols = st.columns([2, 2, 3, 1])
    with date_cols[0]:
        start_date = st.date_input(
            "Başlangıç Tarihi", value=get_previous_day(), key="dabi_start_date"
        )

    with date_cols[1]:
        end_date = st.date_input(
            "Bitiş Tarihi",
            value=get_previous_day(),
            key="dabi_end_date",
            min_value=start_date,
        )

    with date_cols[2]:
        if "dabi_orgs" in ss:
            st.write('<div style="height: 28px;"></div>', unsafe_allow_html=True)

            st.button("🏛️ Organizasyonları Güncelle", on_click=load_dabi_orgs)

    if "dabi_orgs" not in ss:

        st.badge("Henüz organizasyon listesi bağlı değil.", color="orange", icon="⚠️")
        st.button("Organizasyonları Yükle", on_click=load_dabi_orgs)

    else:
        st.selectbox(
            "Organizasyon Seçin",
            options=ss["dabi_orgs"].to_dict(orient="records"),
            format_func=lambda x: x["organizationName"],
            key="dabi_org_select",
        )
        st.checkbox("Sütun İsimlerini Düzenle", key="dabi_column_names_tr", value=True)
        st.button(
            "⚡️ Veriyi Yükle",
            on_click=load_dabi_idm_data,
        )

        if "dabi_idm_data" in ss:

            st.subheader(ss["dabi_data_title"])
            st.caption("Not: Bu tabloyu sağ üst köşeden csv olarak indirebilirsiniz.")
            st.dataframe(ss["dabi_idm_data"], width="stretch", height=800)

            st.markdown("Python kodu")
            st.code(dabi_idm_code(), language="python")


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2
    from eptr2.composite import get_dabi_idm_data
    from eptr2.util.time import get_previous_day
    import re
    import pandas as pd
    from eptr2.tutorials.composite.common import sidebar_common

    st.set_page_config(
        page_title="GÖP İA GİP Pozisyonları Kompozit",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    dabi_positions_main()
