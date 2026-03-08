import streamlit as st
import pypandoc
import tempfile
import os

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="LaTeX to DOCX Converter Pro", layout="wide")

# --- CSS Custom untuk Font Editor ---
if 'font_size' not in st.session_state:
    st.session_state['font_size'] = 16

st.markdown(f"""
    <style>
    .stTextArea textarea {{
        font-size: {st.session_state['font_size']}px !important;
        font-family: 'Courier New', Courier, monospace !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Fungsi Konversi ---
def perform_conversion(text):
    if not text or not text.strip():
        st.error("Konten kosong! Silakan upload file atau ketik sesuatu.")
        return None

    if "\\documentclass" not in text:
        text = f"\\documentclass{{article}}\n\\begin{{document}}\n{text}\n\\end{{document}}"

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            output_path = tmp.name
        
        pypandoc.convert_text(text, 'docx', format='latex', outputfile=output_path)
        
        with open(output_path, "rb") as f:
            data = f.read()
        
        os.remove(output_path)
        return data
    except Exception as e:
        st.error(f"Konversi Gagal: {e}")
        return None

# --- Sidebar ---
st.sidebar.title("📌 Menu")
menu_choice = st.sidebar.radio("Navigasi", ["File & Editor", "View Settings", "About"])

if menu_choice == "File & Editor":
    st.title("📄 LaTeX to DOCX Converter")
    st.info("Sholat dulu baru kerja.")

    # --- BAGIAN 1: UPLOAD FILE ---
    st.subheader("1. Upload File .tex")
    uploaded_file = st.file_uploader("Pilih file LaTeX Anda", type=["tex"])
    
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        st.success(f"File '{uploaded_file.name}' berhasil dimuat!")
        
        # Tombol konversi khusus untuk file yang di-upload
        if st.button("Convert Uploaded File Now"):
            data = perform_conversion(file_content)
            if data:
                st.download_button("📥 Download Hasil Konversi (File)", data, f"{uploaded_file.name}.docx")

    st.divider()

    # --- BAGIAN 2: EDITOR MANUAL ---
    st.subheader("2. Editor LaTeX (Manual)")
    
    # Ambil isi dari upload jika ada, jika tidak kosongkan
    default_text = ""
    if uploaded_file is not None:
        default_text = file_content

    latex_input = st.text_area(
        "Edit atau ketik kode LaTeX di sini:", 
        value=default_text,
        height=400,
        key="editor_area"
    )

    if st.button("Convert Editor Content", type="primary"):
        data = perform_conversion(latex_input)
        if data:
            st.download_button("📥 Download Hasil Konversi (Editor)", data, "document_from_editor.docx")

elif menu_choice == "View Settings":
    st.title("👁️ View Options")
    st.session_state['font_size'] = st.slider("Ukuran Font Editor (px)", 12, 40, st.session_state['font_size'])
    st.write(f"Ukuran font saat ini: {st.session_state['font_size']}px")

elif menu_choice == "About":
    st.title("ℹ️ About App")
    st.markdown("""
    ### LaTeX to DOCX Converter Pro
    Aplikasi berbasis web untuk mengubah dokumen LaTeX menjadi Microsoft Word (.docx).
    
    **Oleh:**
    **Iwan Gunawan, Ph.D.**
    
    *Pesan: Sholat dulu baru kerja.*
    """)
