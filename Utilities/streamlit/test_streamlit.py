import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit Exploration")

st.header("Uploading a CSV file")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data.head())

# st.header("Generating Random Data")
# random_data = np.random.randn(100, 2)
# st.write("100 random points with 2 dimensions")
# st.scatter_chart(pd.DataFrame(random_data, columns=["X", "Y"]))

st.header("Slider and Selectbox")
slider_value = st.slider("Select a value between 0 and 100", 0, 100, 25)
select_value = st.selectbox("Select a value between A and D", ["A", "B", "C", "D"])
st.write("Slider value: ", slider_value)
st.write("Select value: ", select_value)

st.header("Checkbox and Radio Button")
checkbox_value = st.checkbox("Check me if you agree")
radio_value = st.radio("Select one option", ["Option 1", "Option 2", "Option 3"])
st.write("Checkbox value: ", checkbox_value)
st.write("Radio value: ", radio_value)

st.header("Text Input")
text_input = st.text_input("Enter some text")
st.write("Text input: ", text_input)

st.header("Text Area")
text_area = st.text_area("Enter some longer text")
st.write("Text area: ", text_area)

st.header("Markdown")
markdown_text = """
# Heading 1
## Heading 2
### Heading 3

- List item 1
- List item 2
- List item 3

**Bold text**
*Italic text*
"""
st.markdown(markdown_text)

st.header("Audio and Video")
audio_file = st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
video_file = st.video("https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_20mb.mp4")


st.header("Date Picker")
date_picker = st.date_input("Select a date")
st.write("The selected date is:", date_picker)

st.header("Time Picker")
time_picker = st.time_input("Select a time")
st.write("The selected time is:", time_picker)


st.header("Button")
button_option = st.button("Click me to proceed")
if button_option:
    st.write("You have clicked the button.")

st.header("Progress Bar")
import time

bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)
    time.sleep(0.002)

st.header("Selectbox")
select_option = st.selectbox("Select your favorite color", ["Red", "Green", "Blue", "Yellow"])
st.write("Your favorite color is:", select_option)

st.header("Select Multiple")
multi_select = st.multiselect("Select multiple favorite colors", ["Red", "Green", "Blue", "Yellow"])
st.write("Your favorite colors are:", multi_select)

st.header("Date Input")
date_input = st.date_input("Choose a date")
st.write("The selected date is:", date_input)

st.header("Time Input")
time_input = st.time_input("Choose a time")
st.write("The selected time is:", time_input)

st.header("Number Input")
number_input = st.number_input("Enter a number")
st.write("The entered number is:", number_input)

st.header("Select Slider")
select_slider = st.slider("Select a value between 0 and 100", 0, 100, 25, step=5)
st.write("The selected value is:", select_slider)

st.header("Spinbox")
spinbox_input = st.spinner("Spin a number between 0 and 100")
st.write("The selected number is:", spinbox_input)

st.header("Text Input")
text_input = st.text_input("Enter your name")
if text_input:
    st.write("Your name is:", text_input)

st.header("Password Input")
password_input = st.text_input("Enter password", type='password')
if password_input:
    st.write("Password entered successfully.")

st.header("File Uploader")
file_uploader = st.file_uploader("Upload your file", type=["txt", "pdf", "png"])
if file_uploader:
    st.write("File uploaded successfully.")
    

