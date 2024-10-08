import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import re

service = Service('./SeleniumDrivers/chromedriver.exe')  # Asegúrate de tener la ruta correcta
driver = webdriver.Chrome(service=service)

# Cargar el archivo de Excel
df = pd.read_excel('./assets/Curriculums.xlsx')

# Copia
df_copia = df.copy()

# Iniciar sesión en Google
driver.get('')

# Completa la información de inicio de sesión
email_input = driver.find_element(By.ID, 'username')
email_input.send_keys('')  # Cambia esto por tu correo
email_input.send_keys(Keys.RETURN)

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys('')  # Cambia esto por tu contraseña
password_input.send_keys(Keys.RETURN)
time.sleep(5)  # Espera a que se inicie sesión y se cargue Google Drive

#Botón de confirmación de cuenta
continue_button = driver.find_element(By.XPATH, "")  # Reemplaza 'nombreDelJsname' con el valor real
continue_button.click()
time.sleep(6)

# Función para extraer el ID del enlace de Google Drive
def extract_file_id(link):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)/', link)
    return match.group(1) if match else None

# Reemplazar los enlaces con los nombres de los archivos
for index, row in df.iterrows():
    file_link = row['CV']
    driver.get(file_link)  # Acceder al archivoc

    try:
        page_title = driver.title
        print(index+2)
        print(page_title)  # Imprime el nombre del archivo
        df_copia.loc[index,'CV'] = page_title
    except Exception as e:
        print(f"No se pudo para {file_link}")

    time.sleep(3)  # Espera a que se cargue la página del archivo

# Guardar el nuevo archivo de Excel
df_copia.to_excel('./out/Curriculums_out.xlsx', index=False)

# Mantén el navegador abierto
#input("Presiona Enter para cerrar el navegador...")
driver.quit()