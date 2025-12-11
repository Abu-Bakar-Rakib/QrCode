import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="QR Code Generator")
st.title("🔗 QR Code Generator")

# Sidebar inputs
with st.sidebar:
    st.write("Made by Abu Bakar Rakib")
    text = st.text_input("Enter text or URL", value="")
    err_choice = st.selectbox("Error Correction", ["L", "M", "Q", "H"])
    box_size = st.slider("Box Size", 5, 20, 10)
    border = st.slider("Border", 0, 10, 4)
    fill_color = st.color_picker("Fill Color", "#000000")
    back_color = st.color_picker("Background Color", "#FFFFFF")
    logo_file = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
    logo_scale = st.slider("Logo Scale (%)", 5, 40, 15)

error_map = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}

st.subheader("Preview")

if not text.strip():
    st.info("Enter some text or a URL in the sidebar to generate a QR code.")

else:
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_map[err_choice],
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    if logo_file is not None:
        try:
            logo = Image.open(logo_file).convert("RGBA")
            img_w, img_h = img.size

            logo_w = int(img_w * (logo_scale / 100.0))
            logo.thumbnail((logo_w, logo_w), Image.LANCZOS)

            lx = (img_w - logo.width) // 2
            ly = (img_h - logo.height) // 2

            img.paste(logo, (lx, ly), logo)

        except Exception as e:
            st.error(f"Failed to process logo: {e}")

    st.image(img, width=300)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download PNG",
        data=byte_im,
        file_name="qrcode.png",
        mime="image/png",
    )

    st.caption(f"Image size: {len(byte_im)} bytes")

st.markdown("---")
col1, col2 = st.columns(2)

