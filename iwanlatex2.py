import streamlit as st
import pypandoc
import tempfile
import os

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="LaTeX to DOCX Converter Pro", layout="wide")

# --- Inisialisasi Session State (Untuk Fitur View: Clear) ---
if 'latex_content' not in st.session_state:
    st.session_state['latex_content'] = ""

# --- Sidebar (Pengganti Menu Bar) ---
st.sidebar.title("📌 Menu")
menu_choice = st.sidebar.radio("Navigasi", ["File & Editor", "View Settings", "About"])

# --- Fungsi Konversi ---
def perform_conversion(text):
    if not text.strip():
        st.error("Editor masih kosong!")
        return None

    # Tambahkan preamble jika tidak ada
    if "\\documentclass" not in text:
        text = f"\\documentclass{{article}}\n\\begin{{document}}\n{text}\n\\end{{document}}"

    try:
        # Gunakan file sementara untuk output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            output_path = tmp.name
        
        pypandoc.convert_text(text, 'docx', format='latex', outputfile=output_path)
        
        with open(output_path, "rb") as f:
            data = f.read()
        
        os.remove(output_path) # Bersihkan file temp
        return data
    except Exception as e:
        st.error(f"Konversi Gagal: {e}")
        return None

# --- LOGIKA MENU ---

if menu_choice == "File & Editor":
    st.title("📄 LaTeX to DOCX Converter")
    
    # Fitur File -> Open
    uploaded_file = st.file_uploader("Upload file .tex (Opsional)", type=["tex"])
    if uploaded_file is not None:
        st.session_state['latex_content'] = uploaded_file.read().decode("utf-8")

    # Area Editor (LaTeX Input)
    latex_input = st.text_area(
        "Editor LaTeX:", 
        value=st.session_state['latex_content'], 
        height=400,
        placeholder="\\section{Judul}\nKetik kode LaTeX di sini...",
        key="main_editor"
    )
    
    # Update session state jika ada perubahan manual
    st.session_state['latex_content'] = latex_input

    # Tombol Convert (File -> Save As)
    if st.button("Convert to DOCX", type="primary"):
        docx_data = perform_conversion(latex_input)
        if docx_data:
            st.download_button(
                label="📥 Klik untuk Download File DOCX",
                data=docx_data,
                file_name="converted_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

elif menu_choice == "View Settings":
    st.title("👁️ View Options")
    
    # Fitur View -> Clear
    if st.button("Clear Editor Content"):
        st.session_state['latex_content'] = ""
        st.rerun()

    # Fitur View -> Zoom (Di web berupa slider ukuran font)
    font_size = st.slider("Ukuran Font Editor (px)", 12, 30, 16)
    st.markdown(f"""
        <style>
        .stTextArea textarea {{
            font-size: {font_size}px !important;
            font-family: 'Courier New', Courier, monospace !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    st.info("Gunakan slider di atas untuk mengatur kenyamanan membaca di tab 'File & Editor'.")

elif menu_choice == "About":
    st.title("ℹ️ About App")
    st.markdown("""
    ### LaTeX to DOCX Converter Pro
    Aplikasi berbasis web untuk mengubah dokumen LaTeX menjadi Microsoft Word (.docx).
    
    by
    Iwan Gunawan, Ph.D.\n
    sholat dulu baru kerja
    .
    """)