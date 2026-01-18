# Bootstrap: Add package to path when run directly by Streamlit
import sys
from pathlib import Path

_package_root = Path(__file__).parent.parent.parent
if str(_package_root) not in sys.path:
    sys.path.insert(0, str(_package_root))


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


def composite_main():
    ss = st.session_state
    try:
        ss["eptr"] = ss.get(
            "eptr",
            EPTR2(),
        )
    except Exception:
        pass

    st.title("Kompozit Fonksiyonlar Demo")
    st.markdown(
        """
    EPTR2 kompozit fonksiyonlar arayüzüne hoşgeldiniz. Bu arayüz size kompozit fonksiyonları kullanmak konusunda rehberlik edecektir. Hem çalışan bir arayüz kullanacaksınız hem de ilgili Python fonksiyonları hakkında bilgi edineceksiniz. Hazırsanız başlayalım!
    """
    )

    sidebar_common()

    if "eptr" in ss:
        pass
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
                autocomplete="eptr_username",
            )
            st.text_input(
                "Şifre",
                value="",
                key="eptr_password",
                type="password",
                placeholder="EPİAŞ Şeffaflık Platformu kullanıcısı şifreniz",
                autocomplete="eptr_password",
            )
            st.form_submit_button("Giriş Yap", on_click=assign_eptr)

        st.stop()

    st.divider()
    st.page_link(
        "pages/1_Demo.py",
        label="**EPTR2 Kullanım Demosu**",
        icon="👩‍💻",
    )
    st.markdown(
        """
            Bu sayfa, eptr2 kütüphanesinin Python kodlarının nasıl kullanılabileceğini örnekleri ile gösterir."""
    )
    st.divider()
    st.page_link(
        "pages/2_Pozisyonlar.py",
        label="**GİP İA GÖP Pozisyonları**",
        icon="🔮",
    )
    st.markdown(
        """
            Bu sayfa, istediğiniz organizasyon ve istediğiniz dönem aralığı için GÖP, İA ve GİP pozisyonlarını bir arada çekmenizi sağlayan kompozit fonksiyonu çalıştırır."""
    )
    st.divider()
    st.page_link(
        "pages/3_Uretim_Planlama.py",
        label="**Üretim Planlama**",
        icon="⚡️",
    )
    st.markdown(
        """
            Bu sayfa, istediğiniz organizasyon, istediğiniz UEVÇB ve istediğiniz dönem aralığı için KGÜP ve KUDÜP verilerini bir arada çekmenizi sağlayan kompozit fonksiyonu çalıştırır."""
    )
    st.divider()
    st.page_link(
        "pages/4_Fiyat_ve_Maliyetler.py",
        label="**Fiyat ve Maliyetler**",
        icon="💰",
    )
    st.markdown(
        """
            Bu sayfa, istediğiniz tarih aralığı için PTF, SMF, AOF verilerini ve ilgili hesaplamaları (dengesizlik fiyat ve maliyetleri, KÜPST) bir arada çekmenizi sağlayan kompozit fonksiyonu çalıştırır."""
    )
    st.divider()
    st.page_link(
        "pages/5_Santral_Dengesizlik.py",
        label="**Santral Dengesizlik Maliyetleri**",
        icon="💸",
    )
    st.markdown(
        """
            Bu sayfa, istediğiniz tarih aralığı için bir santralin dengesizlik maliyetlerini hesaplamanızı sağlayan kompozit fonksiyonu çalıştırır."""
    )
    st.divider()
    st.page_link(
        "pages/6_Yeni_Dengesizlik_Hesabi.py",
        label="**Yeni Dengesizlik Hesabı**",
        icon="👨‍💻",
    )
    st.markdown(
        """
            Bu sayfa, EPDK'nın yeni taslağına uygun bir şekilde dengesizlik hesabı yapmanıza yardımcı olur. Geçici olarak eklenmiştir."""
    )
    st.divider()
    st.markdown("Diğer kompozit fonksiyonlar da yakında burada...")


if __name__ == "__main__":
    import streamlit as st
    from eptr2 import EPTR2
    import os
    from eptr2_tutorials.composite.common import sidebar_common

    streamlit_cloud_warning = False

    st.set_page_config(
        page_title="eptr2 Kompozit Fonksiyonlar",
        page_icon="👩‍💻",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    if streamlit_cloud_warning:
        st.warning(
            "Bu site dış bir platform olan [Streamlit Community Cloud](https://share.streamlit.io/) üzerinde çalışmaktadır ve sadece demo amaçlıdır. Erişim bilgilerinizi paylaşırken dikkatli olmanızı ve sık sık güncellemenizi tavsiye ederiz."
        )
    composite_main()
