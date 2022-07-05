from tkinter import Image
from turtle import onclick, title
import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu
import streamlit_modal as modal 
from PIL import Image

img = Image.open('logo.jpg')
st.set_page_config(page_title='Lalptop Price Predictor', page_icon=img)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))


if"button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def callback():
    st.session_state.button_clicked = True

st.title("Laptop Price Predictor")

form1 = st.sidebar.form('form1', clear_on_submit=False)

company = form1.selectbox('Brand',df['Company'].unique())

type = form1.selectbox('Type',df['TypeName'].unique())

ram = form1.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

weight = form1.number_input('Weight of the Laptop')

touchscreen = form1.selectbox('Touchscreen',['No','Yes'])

ips = form1.selectbox('IPS',['No','Yes'])

screen_size = form1.number_input('Screen Size')

resolution = form1.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

cpu = form1.selectbox('CPU',df['Cpu brand'].unique())

hdd = form1.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

ssd = form1.selectbox('SSD(in GB)',[0,8,128,256,512,1024])

gpu = form1.selectbox('GPU',df['Gpu brand'].unique())

os = form1.selectbox('OS',df['os'].unique())

predict = form1.form_submit_button('Predict')

select = option_menu(menu_title=None, options=['Selections','Prediction'])

ppi = None
if touchscreen == 'Yes':
    touchscreen = 1
else:
    touchscreen = 0

if ips == 'Yes':
    ips = 1
else:
    ips = 0
    
try:
    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
except ZeroDivisionError:
    st.write('')

query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,os])
query = query.reshape(1,12)
if predict:
    st.sidebar.warning('Prediction in Progress')
    st.snow()

if select == 'Prediction':
    try:
        predictor = str(int(np.exp(pipe.predict(query)[0])))
        st.header("The predicted price of this configuration is " + predictor + " INR")
    except:
        st.info('Prediction failed due to invalid input')
        st.warning('Please enter valid values for all the fields')


if select == 'Selections':
    callback()
    st.write("Company: ",company)
    st.write("Type: ",type)
    st.write("RAM: ",str(ram),'GB')
    st.write("Weight: ",str(weight),'kg')
    st.write("Touchscreen: ",str(touchscreen))
    st.write("IPS: ",str(ips))
    st.write("Screen Size: ",str(screen_size),'inch')
    st.write("Screen Resolution: ",str(resolution))
    st.write("CPU: ",cpu)
    st.write("HDD: ",str(hdd),'GB')
    st.write("SSD: ",str(ssd),'GB')
    st.write("GPU: ",gpu)
    st.write("OS: ",os)

