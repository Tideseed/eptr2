import streamlit as st
import os


def sidebar_common():
    sidebar_warning()
    connection_badge()


def sidebar_warning():
    st.sidebar.caption(
        "UYARI: Bu kütüphane ve arayüzler, verileri [EPİAŞ Şeffaflık Platformu](https://seffaflik.epias.com.tr)'ndan alan `eptr2` kütüphanesi ile entegre edilmiştir. Sadece demo ve eğitim amaçlıdır. Herhangi bir şekilde oluşabilecek kayıp ve zararlardan dolayı hukuken veya başka türlü bir sorumluluk kabul edilmemektedir. Kodlar `eptr2` kütüphanesinin [lisansına](https://github.com/Tideseed/eptr2?tab=Apache-2.0-1-ov-file#readme) tabidir. Veriler EPİAŞ Şeffaflık Platformu'nun kullanım koşullarına tabidir. Sorularınız ve iletişim talepleriniz için [tıklayın](https://robokami.com/#contact)."
    )


def connection_badge():
    ss = st.session_state
    if "eptr" in ss:
        st.sidebar.badge("EPTR2'ye bağlısınız.", color="green", icon="✅")
        st.sidebar.button("Çıkış Yap", on_click=logout_eptr)


def logout_eptr():
    ss = st.session_state
    del ss["eptr"]
    del os.environ["EPTR_USERNAME"]
    del os.environ["EPTR_PASSWORD"]
    st.switch_page("⭐️_Main_Page.py")
