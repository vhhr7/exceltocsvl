import streamlit as st
import pandas as pd
import openpyxl

# Añadir el código de seguimiento de Google Analytics
st.markdown("""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-P0B9JCSYFW"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-P0B9JCSYFW');
    </script>
    """, unsafe_allow_html=True)

def process_excel(uploaded_file, bank_option):
    if bank_option == "Banco Pacífico":
        # Lee el archivo Excel sin encabezado y aplica las transformaciones específicas para Banco Pacífico
        df = pd.read_excel(uploaded_file, header=None)  
        df = df.iloc[1:, 3:]  # Elimina la primera fila y las tres primeras columnas
    elif bank_option == "Banco Diners Club":
        # Fila de encabezado que deseas agregar
        header_row = ["FECHA", "DOCUMENTO", "DESCRIPCION", "OPERACION", "CUOTA", "VALOR (USD)", "SALDO DIFERIDO (USD)", "DEPOSITO"]
        
        # Lee el archivo Excel con encabezado y aplica las transformaciones específicas para Diners Club
        df = pd.read_excel(uploaded_file, skiprows=6)  # Saltar las primeras 6 filas
        df.dropna(subset=["DOCUMENTO"], inplace=True)  # Eliminar filas con NaN en la columna "DOCUMENTO"
        
        # Crear un DataFrame con la fila de encabezado
        header_df = pd.DataFrame([header_row], columns=df.columns.tolist() + ["DEPOSITO"])
        
        # Concatenar la fila de encabezado con los datos originales
        df = pd.concat([header_df, df], ignore_index=True)
        
        # Procesar la columna "VALOR (USD)" para mover valores entre paréntesis a la nueva columna "DEPOSITO"
        df["DEPOSITO"] = df["VALOR (USD)"].apply(lambda x: x.strip('()') if pd.notna(x) and x.startswith('(') and x.endswith(')') else '')
        df["VALOR (USD)"] = df["VALOR (USD)"].apply(lambda x: '' if pd.notna(x) and x.startswith('(') and x.endswith(')') else x)

    else:
        df = pd.read_excel(uploaded_file, header=None)  # Leer el archivo por defecto
    
    # Eliminar filas vacías
    df.dropna(how='all', inplace=True)
    
    # Convierte el DataFrame a CSV sin incluir el encabezado
    csv = df.to_csv(index=False, header=False)
    
    return csv

def main():
    st.title("Convertidor de XLS a CSV")

    # Desplegable para seleccionar el banco
    bank_option = st.selectbox("Selecciona el banco", ["Banco Pacífico", "Banco Diners Club", "Otro Banco"])

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