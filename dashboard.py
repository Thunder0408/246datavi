import streamlit as st
import pandas as pd
import altair as alt

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Number of students in each year according to average daily expenses')
    # สร้างกราฟแท่ง
    plt.figure(figsize=(12, 8), facecolor='lightgrey')

    # กำหนดสีแต่ละกลุ่ม
    colors_6 = sns.color_palette("hsv")

    # สร้างกราฟแท่ง
    for i, (ค่าใช้จ่าย, group6) in enumerate(grouped_6.groupby("คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?")):
        plt.bar(group6["คุณเป็นนักศึกษาชั้นปีที่"], group6["จำนวนนักศึกษา"], label=ค่าใช้จ่าย, color=colors_6[i], edgecolor='blue', alpha=0.8)
        # เพิ่มจำนวนคนลงบนกราฟ
        for x, y in zip(group6["คุณเป็นนักศึกษาชั้นปีที่"], group6["จำนวนนักศึกษา"]):
          plt.text(x, y, str(y), ha="center", va="bottom")

    # เพิ่มป้ายชื่อและตกแต่งกราฟ
    plt.xlabel('ชั้นปี')
    plt.ylabel('จำนวนนักศึกษา (คน)')
    plt.title('จำนวนนักศึกษาในแต่ละชั้นปีตามค่าใช้จ่ายเฉลี่ยต่อวัน')
    plt.legend()

    # แสดงกราฟ
    plt.show()
