forecast_map = {"kgup": "KGÜP", "kgup_v1": "KGÜP-V1", "kudup": "KUDÜP"}
actual_map = {
    "rt": "Gerçek Zamanlı Üretim",
    "uevm": "UEVM",
}
source_map = {
    "solar": "☀️ Güneş",
    "wind": "💨 Rüzgar",
    "other": "🥚 Diğer",
}


def load_gen_orgs_for_pc():
    """Load generation organizations (KGUP/KUDUP) for plant costs."""
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]
    # print(str(ss["plant_costs_start_date"]))
    gen_orgs_df = eptr.call(
        "gen-org",
        start_date=str(ss["plant_costs_start_date"]),
        end_date=str(ss["plant_costs_end_date"]),
    )
    gen_orgs_df.sort_values(by="organizationName", inplace=True)
    ss["gen_orgs"] = gen_orgs_df.copy()


def plants_costs_settings():
    """
    Advanced settings for plant costs.
    """
    ss = st.session_state

    with st.expander("⚙️ Gelişmiş Ayarlar"):

        forecast_sel = st.pills(
            label="Tahmin Kaynağı",
            options=["kgup", "kgup_v1", "kudup"],
            format_func=lambda x: forecast_map.get(x, x),
            default="kgup",
            key="plant_costs_forecast_source",
        )

        st.pills(
            label="Gerçekleşmeler Kaynağı",
            options=["rt", "uevm"],
            default="rt",
            format_func=lambda x: actual_map.get(x, x),
            key="plant_costs_actual_source",
        )
        if ss.get("plant_costs_actual_source", None) == "uevm":
            st.warning(
                "UEVM, sadece uzlaştırma açıklandıktan sonra alınabilir. Seçtiğiniz tarihlerde uzlaştırmanın açıklandığından emin olun.",
                icon="⚠️",
            )

        st.pills(
            label="KÜPST Kaynağı",
            options=["solar", "wind", "other"],
            format_func=lambda x: source_map.get(x, x),
            key="plant_costs_kupst_source",
            default="wind",
        )


def load_uevm_gen_pp_list_for_pc():
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]

    if (
        ss.get("uevm_gen_pp_list_sd", None) != ss["plant_costs_start_date"]
        or ss.get("uevm_gen_pp_list_ed", None) != ss["plant_costs_end_date"]
    ):
        ss["uevm_gen_pp_list_sd"] = ss["plant_costs_start_date"]
        ss["uevm_gen_pp_list_ed"] = ss["plant_costs_end_date"]
        rt_pp_list_df = eptr.call(
            "uevm-pp-list",
        )
        ss["uevm_gen_pp_list"] = rt_pp_list_df.sort_values(by="name").copy()


def load_rt_gen_pp_list_for_pc():
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]

    if (
        ss.get("rt_gen_pp_list_sd", None) != ss["plant_costs_start_date"]
        or ss.get("rt_gen_pp_list_ed", None) != ss["plant_costs_end_date"]
    ):
        ss["rt_gen_pp_list_sd"] = ss["plant_costs_start_date"]
        ss["rt_gen_pp_list_ed"] = ss["plant_costs_end_date"]
        rt_pp_list_df = eptr.call(
            "pp-list-for-date-range",
            start_date=str(ss["rt_gen_pp_list_sd"]),
            end_date=str(ss["rt_gen_pp_list_ed"]),
        )
        ss["rt_gen_pp_list"] = rt_pp_list_df.sort_values(by="name").copy()


def load_gen_uevcbs_for_pc():

    ss = st.session_state
    # st.json(ss)
    if ss.get("gen_orgs", None) is None or ss.get("gen_org_select", None) is None:
        ss["gen_uevcbs"] = None
        return

    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]
    # print(str(ss["plant_costs_start_date"]))
    gen_uevcbs_df = eptr.call(
        "gen-uevcb",
        org_id=ss["gen_org_select"]["organizationId"],
        start_date=str(ss["plant_costs_start_date"]),
    )
    gen_uevcbs_df.sort_values(by="name", inplace=True)
    # print(gen_uevcbs_df)
    ss["gen_uevcbs"] = gen_uevcbs_df.copy()


def plant_costs_code():
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

    forecast_source = ss["plant_costs_forecast_source"]
    actual_source = ss["plant_costs_actual_source"]

    if ss["plant_costs_actual_source"] == "rt":
        pp_id = ss.get("rt_gen_pp_select", None)
    elif ss["plant_costs_actual_source"] == "uevm":
        pp_id = ss.get("uevm_gen_pp_select", None)
    else:
        st.error("Gerçekleşme kaynağı hatalı seçilmiş.")
        st.stop()
    the_pp_id = pp_id.get("id", None)
    return f"""
    from eptr2 import EPTR2
    from eptr2.composite import get_hourly_plant_costs_data

    eptr = EPTR2() ## Kullanıcı adı ve şifreyi yüklemeyi unutmayın
    get_hourly_plant_costs_data(
        eptr=eptr,
        start_date="{ss["plant_costs_start_date"]}",
        end_date="{ss["plant_costs_end_date"]}",
        org_id={the_org_id},
        uevcb_id={the_uevcb_id},
        pp_id={the_pp_id},
        plant_type="{ss["plant_costs_kupst_source"]}",
        forecast_source="{forecast_source}",
        actual_source="{actual_source}",
        verbose=False,
        postprocess=True,
    )

    ## Organizasyon kodlarını öğrenmek için
    ## eptr.call(
    ##    "gen-org", start_date="{str(ss["plant_costs_start_date"])}", end_date="{str(ss["plant_costs_end_date"])}"
    ## )

    ## UEVÇB kodlarını öğrenmek için
    ## Not: org_id = None değerini almamalı! Örnekler otomatik gerçekleştiği için None değeri görülebilir ama asıl kod için listeden bir organizasyon seçin.
    ## eptr.call(
    ##    "gen-uevcb", org_id={the_org_id}, start_date="{str(ss["plant_costs_start_date"])}"
    ## )

    ## Gerçek Zamanlı Üretim santrallerinin kodlarını öğrenmek için
    ## eptr.call(
    ##    "pp-list-for-date-range", start_date="{str(ss["plant_costs_start_date"])}", end_date="{str(ss["plant_costs_end_date"])}"
    ## )

    ## UEVM santrallerinin kodlarını öğrenmek için
    ## eptr.call("uevm-pp-list")
    """


def load_plant_costs_data():
    ss = st.session_state
    eptr: EPTR2 = ss["eptr"]

    input_params = {
        "start_date": str(ss["plant_costs_start_date"]),
        "end_date": str(ss["plant_costs_end_date"]),
        "plant_type": ss["plant_costs_kupst_source"],
        "forecast_source": ss["plant_costs_forecast_source"],
        "actual_source": ss["plant_costs_actual_source"],
    }

    try:

        the_org_d = ss.get("gen_org_select", {})
        if the_org_d:
            input_params["org_id"] = the_org_d.get("organizationId", None)
        else:
            input_params["org_id"] = None

        the_uevcb_id = ss.get("gen_uevcb_select", {})
        if the_uevcb_id:
            input_params["uevcb_id"] = the_uevcb_id.get("id", None)
        else:
            input_params["uevcb_id"] = None

        if ss["plant_costs_actual_source"] == "rt":
            pp_id = ss.get("rt_gen_pp_select", None)
        elif ss["plant_costs_actual_source"] == "uevm":
            pp_id = ss.get("uevm_gen_pp_select", None)
        else:
            st.error("Gerçekleşme kaynağı hatalı seçilmiş.")
            st.stop()
        input_params["pp_id"] = pp_id.get("id", None)

        # st.json(input_params)

        input_params["postprocess"] = True
        res: pd.DataFrame | dict = gather_and_calculate_plant_costs(
            eptr=eptr,
            **input_params,
        )

        # if ss.get("gen_org_select", None):
        #     org_name = ss["gen_org_select"]["organizationName"]
        # else:
        #     org_name = "Tüm Organizasyonlar"

        # if ss.get("gen_uevcb_select", None):
        #     uevcb_name = ss["gen_uevcb_select"]["name"]
        # else:
        #     uevcb_name = "Tüm UEVÇB'ler"

        # ss["plant_costs_data_title"] = (
        #     f"{org_name} - {uevcb_name} ({ss['plant_costs_start_date']} - {ss['plant_costs_end_date']})"
        # )

        ss["plant_costs_data_title"] = (
            f"Sonuçlar ({ss['plant_costs_start_date']} - {ss['plant_costs_end_date']})"
        )
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {str(e)}")
        st.stop()

    # df.drop(columns=["org_id"], inplace=True, errors="ignore")

    ss["plant_costs_data"] = copy.deepcopy(res)


def plant_costs_call_check():
    ss = st.session_state
    org_d = ss.get("gen_org_select", None)
    ss["can_call"] = True
    if org_d:
        st.markdown("Organizasyon ✅: (" + org_d.get("organizationName", "HATA") + ")")
    else:
        st.error("Organizasyon Seçilmedi ❌")
        ss["can_call"] = False

    uevcb_d = ss.get("gen_uevcb_select", None)
    if uevcb_d:
        st.markdown("UEVÇB ✅: (" + uevcb_d.get("name", "HATA") + ")")
    else:
        st.error("UEVÇB Seçilmedi ❌")
        ss["can_call"] = False

    st.markdown(
        f"Seçilen Tahmin/Gerçekleşme Kaynağı: **{forecast_map.get(ss['plant_costs_forecast_source'], None)} / {actual_map.get(ss['plant_costs_actual_source'], None)}**"
    )

    if ss["plant_costs_actual_source"] == "uevm":
        actual_d = ss.get("uevm_gen_pp_select", None)
    else:
        actual_d = ss.get("rt_gen_pp_select", None)

    if actual_d:
        st.markdown(
            f"Gerçekleşme Santrali ✅: {actual_d.get('shortName', 'HATA')} ({actual_d.get('eic', 'HATA')})"
        )
    else:
        st.error("Gerçekleşme Santrali Seçilmedi ❌")
        ss["can_call"] = False

    st.markdown(
        f"Üretim Kaynağı: **{source_map.get(ss['plant_costs_kupst_source'], None)}**. Tolerans değeri: **{get_kupst_tolerance(ss['plant_costs_kupst_source'])}** _(Yanlışsa yukarıdaki ayarlardan değiştirebilirsiniz.)_"
    )
    st.warning("Santral bilgilerinin uyumlu olduğundan emin olun.", icon="⚠️")


def plant_costs_main():
    st.title("Santral Dengesizlik Maliyetleri")
    st.warning("Deneme sürümü. Sonuçlar güvenilir olmayabilir.", icon="⚠️")

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

    plants_costs_settings()

    tomorrow_str = offset_date_by_n_days(str(get_today_utc3()), n=1)

    date_cols = st.columns([2, 2, 3, 1])
    with date_cols[0]:
        start_date = st.date_input(
            "Başlangıç Tarihi",
            value=get_previous_day(),
            key="plant_costs_start_date",
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
                        str(ss["plant_costs_end_date"])
                        if ss.get("plant_costs_end_date", "") != ""
                        else get_previous_day()
                    ),
                ),
            ),
            key="plant_costs_end_date",
            min_value=start_date,
            max_value=tomorrow_str,
        )

    if "gen_orgs" not in ss:
        load_gen_orgs_for_pc()

    with date_cols[2]:
        if "gen_orgs" in ss:
            st.write('<div style="height: 28px;"></div>', unsafe_allow_html=True)

            st.button("🏛️ Organizasyonları Güncelle", on_click=load_gen_orgs_for_pc)

    if "gen_uevcbs" not in ss:
        load_gen_uevcbs_for_pc()

        # st.badge("Henüz organizasyon listesi bağlı değil.", color="orange", icon="⚠️")
        # st.button("Organizasyonları Yükle", on_click=load_gen_orgs_for_pc)

    if "gen_orgs" in ss:
        st.selectbox(
            "Organizasyon Seçin (KGÜP/KUDÜP)",
            options=ss["gen_orgs"].to_dict(orient="records"),
            format_func=lambda x: x["organizationName"],
            key="gen_org_select",
            index=None,
            on_change=load_gen_uevcbs_for_pc,
        )

        if ss.get("gen_org_select", None):
            st.selectbox(
                "UEVÇB Seçin (KGÜP/KUDÜP)",
                options=ss["gen_uevcbs"].to_dict(orient="records"),
                format_func=lambda x: x["name"],
                key="gen_uevcb_select",
                index=None,
            )

        if ss.get("plant_costs_actual_source", None) == "rt":
            if "rt_gen_pp_list" not in ss:
                load_rt_gen_pp_list_for_pc()
            st.selectbox(
                "Gerçek Zamanlı Üretim Santralleri",
                options=ss["rt_gen_pp_list"].to_dict(orient="records"),
                format_func=lambda x: f"{x['shortName']} ({x['eic']})",
                key="rt_gen_pp_select",
                index=None,
            )

        elif ss.get("plant_costs_actual_source", None) == "uevm":
            if "uevm_gen_pp_list" not in ss:
                load_uevm_gen_pp_list_for_pc()
            st.selectbox(
                "UEVM Üretim Santralleri",
                options=ss["uevm_gen_pp_list"].to_dict(orient="records"),
                format_func=lambda x: f"{x['shortName']} ({x['eic']})",
                key="uevm_gen_pp_select",
                index=None,
            )

        with st.expander("Seçimleriniz"):
            plant_costs_call_check()

        # st.checkbox("Sütun İsimlerini Düzenle", key="gen_column_names_tr", value=True)

        if not ss["can_call"]:
            st.caption("⚠️ 👆 Seçimleriniz menüsünden uyarıları kontrol edin.")

        st.button(
            "⚡️ Veriyi Yükle",
            on_click=load_plant_costs_data,
            disabled=not ss["can_call"],
        )

        if "plant_costs_data" in ss:

            st.subheader(ss["plant_costs_data_title"])

            if isinstance(ss["plant_costs_data"], dict):
                d = ss["plant_costs_data"]
                df = d["data"]
                summary_d = d["summary"]
                with st.expander("Özet Bilgiler", expanded=True):
                    st.subheader("Özet Veriler")
                    summary_d = d["summary"]
                    st.markdown(
                        f"""
                    - Tahmin: **{round(summary_d['total_forecast'],1)} MWh**
                    - Gerçekleşen: **{round(summary_d['total_actual'],1)} MWh**
                    - Fark: **{round(summary_d['total_bias'],1)} MWh**
                    - Mutlak Fark: **{round(summary_d['total_mae'],1)} MWh**
                    - KÜPST Maliyeti: **{round(summary_d['total_kupst_cost'],1)} TL**
                    - Dengesizlik Maliyeti: **{round(summary_d['total_imb_cost'],1)} TL**
                    - Toplam Maliyet: **{round(summary_d['total_cost'],1)} TL**
                    """
                    )
            else:
                df = ss["plant_costs_data"]

            st.caption(
                "🟡 Maliyetler brüt maliyetlerdir DSG veya toplayıcı sönümlemelerini içermez."
            )
            st.caption(
                "🟡 Eğer maliyetlerden emin değilseniz, Seçimleriniz menüsünden santrallerin bire bir uyduğundan emin olun. Gerekirse Şeffaflık Platformu üzerinden kontrol edebilirsiniz. Bazı santraller eksik veri (ör. DSG ve yan hizmetler katılımı) yüzünden fazla maliyet gösterebilir."
            )

            res_tabs = st.tabs(["Grafik", "Veri"])
            with res_tabs[1]:
                st.caption(
                    "Not: Bu tabloyu sağ üst köşeden csv olarak indirebilirsiniz."
                )
                st.dataframe(
                    df,
                    width="stretch",
                    height=800,
                    hide_index=True,
                )

            with res_tabs[0]:
                df_plot: pd.DataFrame = df.copy()
                df_plot = df_plot[
                    [
                        "dt",
                        "cumulative_kupst_cost",
                        "cumulative_imb_cost",
                        "cumulative_total_cost",
                    ]
                ].rename(
                    columns={
                        "cumulative_kupst_cost": "KÜPST",
                        "cumulative_imb_cost": "Dengesizlik",
                        "cumulative_total_cost": "Toplam",
                    }
                )

                df_plot = df_plot.melt(
                    id_vars=["dt"], value_name="Maliyet", var_name="Maliyet Türü"
                )
                df_plot["dt"] = pd.to_datetime(df_plot["dt"])

                st.line_chart(
                    df_plot,
                    x="dt",
                    y="Maliyet",
                    color="Maliyet Türü",
                    height=600,
                    y_label="Maliyet (TL)",
                )

            st.subheader("Python kodu")
            st.code(plant_costs_code(), language="python")


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2
    from eptr2.composite import gather_and_calculate_plant_costs
    from eptr2.util.time import get_previous_day, get_today_utc3, offset_date_by_n_days
    from eptr2.util.costs import get_kupst_tolerance
    import copy
    import pandas as pd
    from eptr2.tutorials.composite.common import sidebar_common

    st.set_page_config(
        page_title="Santral Dengesizlik Maliyetleri",
        page_icon="💸",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    plant_costs_main()
