def new_temp_imbalances_code():
    ss = st.session_state
    code = f"""
    from eptr2.util.costs import temp_calculate_imbalance_price_and_costs_new
    temp_calculate_imbalance_price_and_costs_new(
        mcp={round(ss.mcp, 2)}, smp={round(ss.smp, 2)}
    )
    """

    return code


def new_temp_imbalance_calculation():
    ss = st.session_state
    st.title("👨‍💻 Yeni Dengesizlik Hesabı (Geçici)")
    st.warning(
        "Buradaki hesaplama EPDK'nın 22 Eylül 2025 tarihli duyurusundaki değişiklik taslağına dayanmaktadır. Uygulamada hatalar veya değişiklikler olabilir. İlgili duyuru için [tıklayınız](https://epdk.gov.tr/Detay/Icerik/5-16180/elektrik-piyasasina-iliskin-cesitli-mevzuatlarda-)."
    )

    sidebar_common()

    calc_cols = st.columns([2, 1, 3, 3])
    with calc_cols[0]:
        st.number_input(
            "PTF", key="mcp", value=2500.0, min_value=0.0, max_value=3400.0, step=0.1
        )
        st.number_input(
            "SMF", key="smp", value=2500.0, min_value=0.0, max_value=3400.0, step=0.1
        )

    res = temp_calculate_imbalance_price_and_costs_new(
        mcp=round(ss.mcp, 2), smp=round(ss.smp, 2)
    )

    # res_cols = st.columns(4)
    with calc_cols[2]:
        st.metric(
            "Pozitif Dengesizlik Fiyatı (₺/MWh)", f"{res['pos_price']:.2f}", delta=None
        )
        st.metric(
            "Negatif Dengesizlik Fiyatı (₺/MWh)", f"{res['neg_price']:.2f}", delta=None
        )
    with calc_cols[3]:
        st.metric(
            "Pozitif Dengesizlik Maliyeti (₺/MWh)", f"{res['pos_cost']:.2f}", delta=None
        )
        st.metric(
            "Negatif Dengesizlik Maliyeti (₺/MWh)", f"{res['neg_cost']:.2f}", delta=None
        )

    st.subheader("Notlar")

    st.markdown(
        """
        + Eğer dengesizlik sistem yönü ile aynı ise (örneğin sistem yönü negatif ve bireysel dengesizlik negatif ise) yüksek maliyet katsayısı (6%) uygulanır. Yoksa düşük maliyet katsayısı (3%) uygulanır.
        + Sistem yönü dengedeyse her zaman düşük maliyet katsayısı (3%) uygulanır.
        + Varsayım: SMF tavan fiyat (3400 ₺/MWh) olursa her zaman enerji açığı, taban fiyat (0 ₺/MWh) olursa her zaman enerji fazlasıdır. Bunun dışında PTF ve SMF eşit ise sistem dengededir. 
        + max(PTF,SMF) tavan fiyata eşit olursa ekstra 5\\% bir maliyet katsayısı eklenir.
        + Bir _V_ değeri (150 ₺/MWh) bulunmaktadır. Bu _V_ değeri negatif dengesizlik fiyatında bir taban fiyat olarak kullanılmaktadır. Pozitif dengesizlik fiyatında ise bir eşik olarak kullanılmaktadır.
        + Pozitif dengesizlik fiyatı V değerinden düşük ise, B (100 ₺/MWh) değeri devreye girer. Pozitif dengesizlik fiyatı - B * (1 - l) olarak hesaplanır. l değeri sistem yönü enerji açığı ise 0.03, enerji fazlası ise 0.06 olarak alınır. Diğer durumda eski yöntem ile hesaplanır (ancak l gene 0.03 veya 0.06 değerini alabilir).
        """
    )

    st.subheader("Python kodu")
    st.code(new_temp_imbalances_code(), language="python")


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2

    from eptr2.util.costs import temp_calculate_imbalance_price_and_costs_new
    import copy
    import pandas as pd
    from eptr2.tutorials.composite.common import sidebar_common

    st.set_page_config(
        page_title="Yeni Dengesizlik Hesabı",
        page_icon="👨‍💻",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    new_temp_imbalance_calculation()
