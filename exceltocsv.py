import streamlit as st
import pandas as pd

def process_excel(uploaded_file, bank_option):
    # Lee el archivo Excel
    df = pd.read_excel(uploaded_file)
    
    if bank_option == "Banco Pacífico":
        # Elimina la primera fila y las tres primeras columnas
        df = df.iloc[1:, 3:]
    
    # Convierte el DataFrame a CSV
    csv = df.to_csv(index=False)
    
    return csv

def main():
    st.title("Convertidor de XLS a CSV")

    # Desplegable para seleccionar el banco
    bank_option = st.selectbox("Selecciona el banco", ["Banco Pacífico", "Otro Banco"])

    uploaded_file = st.file_uploader("Selecciona un archivo XLS", type=["xls", "xlsx"])

    if uploaded_file is not None:
        st.success("Archivo subido con éxito!")
        
        # Procesa el archivo Excel según la opción del banco
        csv = process_excel(uploaded_file, bank_option)
        
        # Muestra el contenido del archivo CSV
        st.text_area("Contenido del archivo CSV", csv, height=300)

        # Botón para descargar el archivo CSV
        st.download_button(
            label="Descargar archivo CSV",
            data=csv,
            file_name="archivo_convertido.csv",
            mime="text/csv"
        )

    # Pie de página
    display_footer()

def display_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #eaeaea;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .footer .logo {
        height: 60px; /* Increased size */
        margin-right: 20px;
    }
    .footer .separator {
        border-left: 2px solid #eaeaea;
        height: 120px;
        margin-right: 20px;
    }
    </style>
    <div class="footer">
        <img class="logo" src="http://vicherrera.net/wp-content/uploads/2023/05/VicHerrera_Logo.svg" alt="Vic Herrera Logo">
        <div class="separator"></div>
        <div>
            <p>Developed by Vic Herrera | <a href="https://vicherrera.net" target="_blank">Vic Herrera</a> | <a href="https://datawava.com" target="_blank">datawava</a></p>
            <p>© Version 1.2  - July, 2024</p>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
