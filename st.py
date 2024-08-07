import streamlit as st
import os
from PIL import Image
import pillow_heif
import shutil
import google.generativeai as genai
import os
from expiry_date_prompt import PROMPT
import json
import pandas as pd

st.set_page_config(layout="wide")
upload_folder = "uploaded_images"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
else:
    shutil.rmtree('uploaded_images')
    os.makedirs(upload_folder)
st.title("Image Upload and Storage")
uploaded_files = st.file_uploader("Choose images", type=['png', 'jpg', 'jpeg', 'heic'], accept_multiple_files=True)

if uploaded_files:
    with st.spinner(text="In progress..."):
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            file_path = os.path.join(upload_folder, uploaded_file.name)
        
            if file_extension == 'heic':
                heif_file = pillow_heif.read_heif(uploaded_file)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
                file_path = os.path.splitext(file_path)[0] + '.jpg'
                image.save(file_path, "JPEG")
            else:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                image = Image.open(uploaded_file)
    st.success("Images uploaded successfully")
        #st.success(f"Saved file: {uploaded_file.name}")
        #st.image(image, caption=uploaded_file.name, width=50)



#PART 2
genai.configure(api_key="AIzaSyAbz47y3xigQw295DYXdG5arLbknOoZsqw")
model = genai.GenerativeModel(model_name="gemini-1.5-flash-001")
folder_path = "uploaded_images"

results = []
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    myfile = genai.upload_file(path=file_path)
    result = model.generate_content([myfile, "\n\n", PROMPT])
    op=result.text
    try :
        corrected_json_str = op.replace(',\n}', '}')
        data=json.loads(corrected_json_str)
        manufacturing_date = data.get("Manufacturing Date", None)
        expiry_date = data.get("Expiry Date", None)
        expiry_duration = data.get("Expiry Duration", None)
        results.append({"filename": filename, "Manufacturing Date": manufacturing_date, "Expiry Date": expiry_date, "Expiry Duration" : expiry_duration})
    except:
        print(f"Error parsing JSON for {filename}: {e}")
        print(f"Result text: {result.text}")
df = pd.DataFrame(results)
df.to_csv('mfg_exp_result.csv')

st.dataframe(data=df)

st.download_button(
        label="Download CSV file",
        data=open("mfg_exp_result.csv", "rb").read(),
        file_name='mfg_exp_result.csv',
        mime="text/csv"
    )
#if st.button("Clean and Restart"):
#    shutil.rmtree('uploaded_images')
#    st.experimental_rerun()

