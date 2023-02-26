import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

buf = BytesIO()

st.title("Image Editing")


def validate(val):
    if val > 255:
        return 255
    if val < 0:
        return 0
    return int(val)


def contrast(im, val):  # for val ∈ [-100, 100]
    # progress_bar = st.progress(0) # progress bar slows down code by over 10x
    im = np.array(im)
    for i in range(len(im)):
        for j in range(len(im[0])):
            f = 103*(val + 99)/(99*(103-val))
            im[i][j][0] = validate(f * (im[i][j][0] - 128) + 128)  # r
            im[i][j][1] = validate(f * (im[i][j][1] - 128) + 128)  # g
            im[i][j][2] = validate(f * (im[i][j][2] - 128) + 128)  # b
            # progress_bar.progress((i) / len(im))
    im = Image.fromarray(im)
    # progress_bar.empty()
    return im


def brightness(im, val):  # for val ∈ [-100, 100]
    im = np.array(im)
    for i in range(len(im)):
        for j in range(len(im[0])):
            im[i][j][0] = validate(im[i][j][0] + val*(255/100))  # r
            im[i][j][1] = validate(im[i][j][1] + val*(255/100))  # g
            im[i][j][2] = validate(im[i][j][2] + val*(255/100))  # b
    im = Image.fromarray(im)
    return im


menu = ["Contrast", "Brightness", "Help"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Contrast":
    st.subheader("Contrast")

    # file upload widget
    uploaded_file = st.file_uploader(
        "Upload your image", type=["jpg", "jpeg"])
    if uploaded_file is not None:
        # if image uploaded, convert to PIL Image
        im = Image.open(uploaded_file)

        # contrast slider
        c_slider = st.slider("Select contrast value", -100, 100, 0)

        # toggle edited/original image button
        edited = st.checkbox("Show edited image", value=True)

        if c_slider != 0:
            edited_image = contrast(im, c_slider)
        else:
            edited_image = im

        # display image
        if(edited) and c_slider != 0:
            st.image(edited_image, caption=uploaded_file.name)
        else:
            st.image(im, caption=uploaded_file.name)

        # download edited button
        if c_slider != 0:
            edited_image.save(buf, format="JPEG")
        else:
            im.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        btn = st.download_button(
            label="Download edited image",
            data=byte_im,
            file_name=uploaded_file.name,
            mime=uploaded_file.type
        )

if choice == "Brightness":
    st.subheader("Brightness")

    # file upload widget
    uploaded_file = st.file_uploader(
        "Upload your image", type=["jpg", "jpeg"])
    if uploaded_file is not None:
        # if image uploaded, convert to PIL Image
        im = Image.open(uploaded_file)

        # contrast slider
        b_slider = st.slider("Select brightness value", -100, 100, 0)

        # toggle edited/original image button
        edited = st.checkbox("Show edited image", value=True)

        if b_slider != 0:
            edited_image = brightness(im, b_slider)
        else:
            edited_image = im

        # display image
        if(edited) and b_slider != 0:
            st.image(edited_image, caption=uploaded_file.name)
        else:
            st.image(im, caption=uploaded_file.name)

        # download edited button
        if b_slider != 0:
            edited_image.save(buf, format="JPEG")
        else:
            im.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        btn = st.download_button(
            label="Download edited image",
            data=byte_im,
            file_name=uploaded_file.name,
            mime=uploaded_file.type
        )

if choice == "Help":
    st.subheader("Help")
    st.write(
        """
Use the [command-line](https://github.com/ashishkulkarnii/image-editing-cli) for faster speeds!
"""
    )

    st.subheader("Command-line instructions")
    st.write(
        """
Note:
* [] means optional
* all values are taken as float unless mentioned otherwise

General Commands:
* load <filename>.<extension>
* save [<filename>] [<extension>]
* exit [save]
* show [<filename>.<extension>]
* undo
* redo

Image Manipulation Commands:
* greyscale
* invert
* solarize <"<" or ">"> <threshold value from 0 to 255>
* contrast <value from -100 to 100>
* resize <new number (integer) of rows> <new number (integer) of columns>
* brightness <value from -100 to 100>
* gamma correction <gamma value>
* color pop <color name in English> [invert]
* mean blur <kernel size (integer)>
* gaussian blur <kernel size (integer)> [<sigma value, default sigma = 1>]
* bgr <color name in English>
"""
    )
