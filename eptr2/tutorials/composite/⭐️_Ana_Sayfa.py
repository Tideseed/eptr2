def assign_eptr():
    ss = st.session_state
    os.environ["EPTR_USERNAME"] = ss["eptr_username"]
    os.environ["EPTR_PASSWORD"] = ss["eptr_password"]
    try:
        ss["eptr"] = ss.get("eptr", EPTR2())
    except Exception as e:
        if str(e).startswith("Request failed with status code: 401"):
            st.error(
                "EPTR2 bağlantısı kurulurken kimlik doğrulama hatası oluştu. Lütfen kullanıcı adı ve şifrenizi kontrol edin."
            )
        else:
            st.error(f"EPTR2 bağlantısı kurulurken hata oluştu: {str(e)}")


# def logout_eptr():
#     ss = st.session_state
#     del ss["eptr"]
#     del os.environ["EPTR_USERNAME"]
#     del os.environ["EPTR_PASSWORD"]
#     st.switch_page("⭐️_Main_Page.py")


def composite_main():

    ss = st.session_state
    try:
        ss["eptr"] = ss.get(
            "eptr",
            EPTR2(),
        )
    except Exception as e:
        # print(f"EPTR2 bağlantısı kurulurken hata oluştu: {e}")
        pass

    st.title("Kompozit Fonksiyonlar Demo")
    st.markdown(
        """
    EPTR2 kompozit fonksiyonlar arayüzüne hoşgeldiniz. Bu arayüz size kompozit fonksiyonları kullanmak konusunda rehberlik edecektir. Hem çalışan bir arayüz kullanacaksınız hem de ilgili Python fonksiyonları hakkında bilgi edineceksiniz. Hazırsanız başlayalım!
    """
    )

    # st.sidebar.caption(
    #     "UYARI: Bu ürün ve arayüz, verileri EPİAŞ Şeffaflık Platformu'ndan alan EPTR2 kütüphanesi ile entegre edilmiştir. Sadece demo amaçlıdır. Herhangi bir şekilde oluşabilecek kayıp ve zararlardan dolayı Robokami/Tideseed hukuken veya başka türlü bir sorumluluk kabul etmemektedir. Kodlar EPTR2 kütüphanesinin lisansına tabidir. Veriler EPİAŞ Şeffaflık Platformu'nun kullanım koşullarına tabidir."
    # )
    sidebar_common()

    if "eptr" in ss:
        pass
        # st.sidebar.badge("EPTR2'ye bağlısınız.", color="green", icon="✅")
        # st.sidebar.button("Çıkış Yap", on_click=logout_eptr)
    else:
        with st.form("login_form"):
            st.info(
                "Lütfen EPİAŞ Şeffaflık Platformu kullanıcı adınızı (e-posta) ve şifrenizi giriniz. (_Not: eğer lokalde (ör. kendi bilgisayarınız) çalıştırıyorsanız, bilgileriniz lokal ortamda geçici olarak saklanmaktadır. Başka bir sistemde (ör. sunucu ortamı, bulut, servis) çalıştırıyorsanız sisteme güvendiğinize emin olun._). Üye değilseniz EPİAŞ Şeffaflık Platformu kayıt sayfasına gitmek için [tıklayın](https://kayit.epias.com.tr/epias-transparency-platform-registration-form)."
            )
            st.text_input(
                "Kullanıcı",
                value="",
                key="eptr_username",
                placeholder="EPİAŞ Şeffaflık Platformu kullanıcısı e-posta adresiniz",
            )
            st.text_input(
                "Şifre",
                value="",
                key="eptr_password",
                type="password",
                placeholder="EPİAŞ Şeffaflık Platformu kullanıcısı şifreniz",
            )
            st.form_submit_button("Giriş Yap", on_click=assign_eptr)

        st.stop()

    st.divider()
    st.page_link(
        "pages/1_👩‍💻_Demo.py",
        label="**EPTR2 Kullanım Demosu**",
        icon="👩‍💻",
    )
    st.markdown(
        """
            Bu sayfa, eptr2 kütüphanesinin Python kodlarının nasıl kullanılabileceğini örnekleri ile gösterir."""
    )
    st.divider()
    st.page_link(
        "pages/2_🔮_Pozisyonlar.py",
        label="**GİP İA GÖP Pozisyonları**",
        icon="🔮",
    )
    st.markdown(
        """
            Bu sayfa, istediğiniz organizasyon ve istediğiniz dönem aralığı için GÖP, İA ve GİP pozisyonlarını bir arada çekmenizi sağlayan kompozit fonksiyonu çalıştırır."""
    )
    st.divider()
    st.page_link(
        "pages/3_⚡️_Üretim_Planlama.py",
        label="**Üretim Planlama**",
        icon="⚡️",
    )
    st.markdown(
        """
            Bu sayfa, istediğiniz organizasyon, istediğiniz UEVÇB ve istediğiniz dönem aralığı için KGÜP ve KUDÜP verilerini bir arada çekmenizi sağlayan kompozit fonksiyonu çalıştırır."""
    )

    st.divider()
    st.markdown("Diğer kompozit fonksiyonlar da yakında burada...")


if __name__ == "__main__":

    import streamlit as st
    from eptr2 import EPTR2
    import os
    from eptr2.tutorials.composite.common import sidebar_common

    st.set_page_config(
        page_title="eptr2 Kompozit Fonksiyonlar",
        page_icon="👩‍💻",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    composite_main()
