import time
from enum import Enum

import streamlit as st


class StateKey(Enum):
    HAS_PHOTO = 'has photo'
    PHOTO_FILE = 'photo file'
    SHOULD_UPLOAD = 'should upload'


def change_photo_state():
    st.session_state[StateKey.HAS_PHOTO] = True


def on_upload():
    st.session_state[StateKey.HAS_PHOTO] = True
    st.session_state[StateKey.SHOULD_UPLOAD] = True
    # st.info(f'on upload {st.session_state[StateKey.SHOULD_UPLOAD]}')


def load_img(promotion="upload a photo"):
    file = st.file_uploader(promotion, on_change=on_upload)
    if file is not None and st.session_state[StateKey.SHOULD_UPLOAD]:
        st.session_state[StateKey.PHOTO_FILE] = file
        progress_bar = st.progress(0)
        for percent in range(100):
            time.sleep(0.02)
            progress_bar.progress((percent + 1))
        st.success("photo upload successfully.")
        st.session_state[StateKey.SHOULD_UPLOAD] = False


if __name__ == '__main__':
    if StateKey.HAS_PHOTO not in st.session_state:
        st.session_state[StateKey.HAS_PHOTO] = False
        st.session_state[StateKey.PHOTO_FILE] = None
        st.session_state[StateKey.SHOULD_UPLOAD] = False

    header_col, metric_col = st.columns([3, 1])
    header_col.markdown("# Welcome to my app!")
    header_col.markdown("Here is some info for the app.")
    metric_col.metric(label="temperature", value="27度", delta="3度")
    load_img()
    capture_input = st.camera_input(label="take a photo",
                                    on_change=change_photo_state,
                                    label_visibility='hidden')
    if capture_input is not None:
        st.session_state[StateKey.HAS_PHOTO] = True
        st.session_state[StateKey.PHOTO_FILE] = capture_input
    if not st.session_state[StateKey.HAS_PHOTO]:
        st.stop()
    with st.expander("click to show photo"):
        st.write("Check your photo here")
        st.image(st.session_state[StateKey.PHOTO_FILE])
