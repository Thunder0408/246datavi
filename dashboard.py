# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wFd0Tk3bb0XzQt8CLDddjJBdC1G6LbJ1
"""

import pandas as pd
import streamlit

import gspread
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib as mpl
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from google.auth import default
from google.colab import auth
import matplotlib.font_manager as fm
from wordcloud import WordCloud
from pythainlp.tokenize import word_tokenize # เป็นตัวตัดคำของภาษาไทย
from pythainlp.corpus import thai_stopwords # เป็นคลัง Stop Words ของภาษาไทย
from collections import Counter
import random

url = 'https://drive.google.com/file/d/1QPBjNIxIwrMsOpTBQbvquOPyCWbbtkqF/view?usp=sharing'
csv_url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(csv_url, on_bad_lines='skip')

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

col = st.columns((30, 9, 4), gap='medium')

# นับจำนวนข้อมูลในแต่ละกลุ่มของนักศึกษาตามชั้นปีและคณะที่ศึกษา
grouped = df.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คณะที่คุณกำลังศึกษา"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เพื่อเก็บลำดับใหม่ของชั้นปี
reorder_map = {
    "ชั้นปีที่ 1": 0,
    "ชั้นปีที่ 2": 1,
    "ชั้นปีที่ 3": 2,
    "ชั้นปีที่ 4": 3,
    "ชั้นปีที่ 5-8": 4
}

# รวมชั้นปีที่ 5 ถึง 8 เป็นกลุ่มเดียวกัน
grouped['คุณเป็นนักศึกษาชั้นปีที่'] = grouped['คุณเป็นนักศึกษาชั้นปีที่'].replace(['ชั้นปีที่ 5', 'ชั้นปีที่ 6', 'ชั้นปีที่ 7', 'ชั้นปีที่ 8'], 'ชั้นปีที่ 5-8')

# นับจำนวนนักศึกษาใหม่ตามกลุ่มที่รวมแล้ว
grouped = grouped.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คณะที่คุณกำลังศึกษา"]).agg({'จำนวนนักศึกษา': 'sum'}).reset_index()

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ dictionary ที่สร้างขึ้น
grouped["ลำดับ"] = grouped["คุณเป็นนักศึกษาชั้นปีที่"].map(reorder_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped = grouped.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# นับจำนวนข้อมูลในแต่ละกลุ่มของนักศึกษาตามชั้นปี, เพศ, และคณะที่ศึกษา
grouped2 = df.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "เพศ", "คณะที่คุณกำลังศึกษา"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เพื่อเก็บลำดับใหม่ของชั้นปี
reorder_map = {
    "ชั้นปีที่ 1": 0,
    "ชั้นปีที่ 2": 1,
    "ชั้นปีที่ 3": 2,
    "ชั้นปีที่ 4": 3,
    "ชั้นปีที่ 5-8": 4
}

# รวมชั้นปีที่ 5 ถึง 8 เป็นกลุ่มเดียวกัน
grouped2['คุณเป็นนักศึกษาชั้นปีที่'] = grouped2['คุณเป็นนักศึกษาชั้นปีที่'].replace(['ชั้นปีที่ 5', 'ชั้นปีที่ 6', 'ชั้นปีที่ 7', 'ชั้นปีที่ 8'], 'ชั้นปีที่ 5-8')

# นับจำนวนนักศึกษาใหม่ตามกลุ่มที่รวมแล้ว
grouped2 = grouped2.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "เพศ","คณะที่คุณกำลังศึกษา"]).agg({'จำนวนนักศึกษา': 'sum'}).reset_index()

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ dictionary ที่สร้างขึ้น
grouped2["ลำดับ"] = grouped2["คุณเป็นนักศึกษาชั้นปีที่"].map(reorder_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped2 = grouped2.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# กำหนดค่าที่ต้องการเปลี่ยนใน column 'คุณเป็นนักศึกษาชั้นปีที่'
replace_values = {'ชั้นปีที่ 1': 'ชั้นปีที่ 1',
                  'ชั้นปีที่ 2': 'ชั้นปีที่ 2',
                  'ชั้นปีที่ 3': 'ชั้นปีที่ 3',
                  'ชั้นปีที่ 4': 'ชั้นปีที่ 4',
                  'ชั้นปีที่ 5': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 6': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 7': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 8': 'ชั้นปีที่ 5-8'
                  }
# สร้าง donut
donut1 = alt.Chart(grouped2).mark_arc(innerRadius=150, outerRadius=200).encode(
    theta= "count()",
    color="คุณเป็นนักศึกษาชั้นปีที่:N",
)

donut2 = alt.Chart(grouped2).mark_arc(innerRadius=100, outerRadius=150).encode(
    theta= "count()",
    color="คณะที่คุณกำลังศึกษา:N",
)

donut3 = alt.Chart(grouped2).mark_arc(innerRadius=50, outerRadius=100).encode(
    theta= "count()",
    color="เพศ:N",
)

# รวม donut
combined_donut = alt.layer(donut1, donut2, donut3).resolve_scale(color='independent').properties(
    width=1024,
    height=768,
    title='1.แนวโน้มสัดส่วนประชากรผู้ตอบแบบสอบถามในแต่ละชั้นปี')

# กำหนดค่าที่ต้องการเปลี่ยนใน column 'คุณเป็นนักศึกษาชั้นปีที่'
replace_values = {'ชั้นปีที่ 1 (รหัสนักศึกษาขึ้นต้นด้วย 66)': 'ชั้นปีที่ 1',
                  'ชั้นปีที่ 2 (รหัสนักศึกษาขึ้นต้นด้วย 65)': 'ชั้นปีที่ 2',
                  'ชั้นปีที่ 3 (รหัสนักศึกษาขึ้นต้นด้วย 64)': 'ชั้นปีที่ 3',
                  'ชั้นปีที่ 4 (รหัสนักศึกษาขึ้นต้นด้วย 63)': 'ชั้นปีที่ 4',
                  'ชั้นปีที่ 5 (รหัสนักศึกษาขึ้นต้นด้วย 62)': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 6 (รหัสนักศึกษาขึ้นต้นด้วย 61)': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 7 (รหัสนักศึกษาขึ้นต้นด้วย 60)': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 8 (รหัสนักศึกษาขึ้นต้นด้วย 59)': 'ชั้นปีที่ 5-8'
                  }

# เปลี่ยนค่าใน column 'คุณเป็นนักศึกษาชั้นปีที่' ใน DataFrame ใหม่
df_new = df.replace({'คุณเป็นนักศึกษาชั้นปีที่': replace_values})

# กำหนดลำดับของรายได้ต่อเดือน
price_order = ['มากกว่า 9,999 บาท',
               '9,000 - 9,999 บาท',
               '8,000 - 8,999 บาท',
               '7,000 - 7,999 บาท',
               'น้อยกว่า 7,000 บาท']

# กำหนดลำดับของชั้นปีที่ศึกษา
year_order = ['ชั้นปีที่ 1',
              'ชั้นปีที่ 2',
              'ชั้นปีที่ 3',
              'ชั้นปีที่ 4',
              'ชั้นปีที่ 5-8'
              ]

# สร้างกราฟแท่ง
chart2 = alt.Chart(df_new).mark_bar().encode(
    x=alt.X('count():Q', title='จำนวนนักศึกษา'),
    y=alt.Y('คุณมีรายได้ต่อเดือนเท่าไหร่ ?:N', sort=price_order, title='รายได้ต่อเดือน (บาท)'),
    color=alt.Color('คุณเป็นนักศึกษาชั้นปีที่:N', sort=year_order, legend=alt.Legend(title='ชั้นปีที่')),
    tooltip=['คุณมีรายได้ต่อเดือนเท่าไหร่ ?', 'คุณเป็นนักศึกษาชั้นปีที่', 'count()']
).properties(
    width=700,
    height=400,
    title='2.แนวโน้มรายได้ต่อเดือนของนักศึกษา โดยแบ่งตามชั้นปีที่ศึกษา'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มโดยใช้ groupby และ size
grouped_3_1 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1", "เพศ"]).size().reset_index(name="จำนวนนักศึกษา")

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ค่าจากคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1'
grouped_3_1["ลำดับ"] = grouped_3_1["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1"]

# เรียงลำดับข้อมูลตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped_3_1 = grouped_3_1.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# กรองข้อมูลที่ไม่มีค่าใช้จ่ายในอันดับนี้
filtered_data_3_1 = grouped_3_1[grouped_3_1["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1"] != "ไม่มีค่าใช้จ่ายในอันดับนี้"]

# สร้างแผนภูมิแท่งด้วย Altair
chart3_1 = alt.Chart(filtered_data_3_1).mark_bar().encode(
    x=alt.X('sum(จำนวนนักศึกษา):Q', title='จำนวนนักศึกษา'),
    y=alt.Y('เพศ:N', title='เพศของนักศึกษา'),
    color=alt.Color('ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1:N', legend=alt.Legend(title='หมวดหมู่ค่าใช้จ่าย')),
    tooltip=['เพศ', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1', 'sum(จำนวนนักศึกษา)']
).properties(
    width=700,
    height=400,
    title='5.แผนภูมิแท่ง แสดงการเปรียบเทียบเพศกับค่าใช้จ่ายโดยรวมอันดับ 1 ของนักศึกษาในมหาวิทยาลัย'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มโดยใช้ groupby และ size
grouped_3_2 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2", "เพศ"]).size().reset_index(name="จำนวนนักศึกษา")

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ค่าจากคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2'
grouped_3_2["ลำดับ"] = grouped_3_2["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2"]

# เรียงลำดับข้อมูลตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped_3_2 = grouped_3_2.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])


# กรองข้อมูลเพื่อเอาแต่ละแถวที่ไม่มีค่าใช้จ่ายในอันดับที่สองออก
filtered_data_3_2 = grouped_3_2[grouped_3_2["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2"] != "ไม่มีค่าใช้จ่ายในอันดับนี้"]

# สร้างแผนภูมิแท่งด้วย Altair
chart3_2 = alt.Chart(filtered_data_3_2).mark_bar().encode(
    x=alt.X('sum(จำนวนนักศึกษา):Q', title='จำนวนนักศึกษา'),
    y=alt.Y('เพศ:N', title='เพศของนักศึกษา'),
    color=alt.Color('ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2:N', legend=alt.Legend(title='หมวดหมู่ค่าใช้จ่าย')),
    tooltip=['เพศ', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2', 'sum(จำนวนนักศึกษา)']
).properties(
    width=700,
    height=400,
    title='6.แผนภูมิแท่ง แสดงการเปรียบเทียบเพศกับค่าใช้จ่ายโดยรวมอันดับ 2 ของนักศึกษาในมหาวิทยาลัย'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มโดยใช้ groupby และ size
grouped_3_3 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3", "เพศ"]).size().reset_index(name="จำนวนนักศึกษา")

# เพิ่มคอลัมน์ลำดับใหม่โดยใช้ค่าจากคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3'
grouped_3_3["ลำดับ"] = grouped_3_3["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3"]

# เรียงลำดับข้อมูลตามคอลัมน์ "ลำดับ" และลบคอลัมน์ "ลำดับ" ออก
grouped_3_3 = grouped_3_3.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# กรองข้อมูลเพื่อเอาแต่ละแถวที่ไม่มีค่าใช้จ่ายในอันดับที่สามออก
filtered_data_3_3 = grouped_3_3[grouped_3_3["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3"] != "ไม่มีค่าใช้จ่ายในอันดับนี้"]

# สร้างแผนภูมิแท่งด้วย Altair
chart3_3 = alt.Chart(filtered_data_3_3).mark_bar().encode(
    x=alt.X('sum(จำนวนนักศึกษา):Q', title='จำนวนนักศึกษา'),
    y=alt.Y('เพศ:N', title='เพศของนักศึกษา'),
    color=alt.Color('ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3:N', legend=alt.Legend(title='หมวดหมู่ค่าใช้จ่าย')),
    tooltip=['เพศ', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3', 'sum(จำนวนนักศึกษา)']
).properties(
    width=700,
    height=400,
    title='7.แผนภูมิแท่ง แสดงการเปรียบเทียบเพศกับค่าใช้จ่ายโดยรวมอันดับ 3 ของนักศึกษาในมหาวิทยาลัย'
)

# กำหนดค่าที่ต้องการเปลี่ยนใน column 'คุณเป็นนักศึกษาชั้นปีที่'
replace_values = {'ชั้นปีที่ 1 (รหัสนักศึกษาขึ้นต้นด้วย 66)': 'ชั้นปีที่ 1',
                  'ชั้นปีที่ 2 (รหัสนักศึกษาขึ้นต้นด้วย 65)': 'ชั้นปีที่ 2',
                  'ชั้นปีที่ 3 (รหัสนักศึกษาขึ้นต้นด้วย 64)': 'ชั้นปีที่ 3',
                  'ชั้นปีที่ 4 (รหัสนักศึกษาขึ้นต้นด้วย 63)': 'ชั้นปีที่ 4',
                  'ชั้นปีที่ 5 (รหัสนักศึกษาขึ้นต้นด้วย 62)': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 6 (รหัสนักศึกษาขึ้นต้นด้วย 61)': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 7 (รหัสนักศึกษาขึ้นต้นด้วย 60)': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 8 (รหัสนักศึกษาขึ้นต้นด้วย 59)': 'ชั้นปีที่ 5-8'
                  }

# เปลี่ยนค่าใน column 'คุณเป็นนักศึกษาชั้นปีที่' ใน DataFrame ใหม่
df_new = df.replace({'คุณเป็นนักศึกษาชั้นปีที่': replace_values})

# กำหนดลำดับของรายได้ต่อเดือน
price_order = ['มากกว่า 300 บาท',
               '201 - 300 บาท',
               '101 - 200 บาท',
               '50 - 100 บาท',
               'น้อยกว่า 50 บาท']

# กำหนดลำดับของชั้นปีที่ศึกษา
year_order = ['ชั้นปีที่ 1',
              'ชั้นปีที่ 2',
              'ชั้นปีที่ 3',
              'ชั้นปีที่ 4',
              'ชั้นปีที่ 5-8'
              ]

# สร้างกราฟแท่ง
chart6 = alt.Chart(df_new).mark_bar().encode(
    x=alt.X('count():Q', title='จำนวนนักศึกษา'),
    y=alt.Y('คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?:N', sort=price_order, title='รายได้ต่อเดือน (บาท)'),
    color=alt.Color('คุณเป็นนักศึกษาชั้นปีที่:N', sort=year_order, legend=alt.Legend(title='ชั้นปีที่')),
    tooltip=['คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?', 'คุณเป็นนักศึกษาชั้นปีที่', 'count()']
).properties(
    width=700,
    height=400,
    title='3.จำนวนนักศึกษาในแต่ละชั้นปีตามค่าใช้จ่ายเฉลี่ยต่อวัน'
)

# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1' และ 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'
grouped_8_1 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")
# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2' และ 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'
grouped_8_2 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")
# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3' และ 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'
grouped_8_3 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เพื่อกำหนดลำดับใหม่สำหรับจำนวนเงินที่ใช้จ่าย
reorder_expenses_map = {
    "ต่ำกว่า 500 บาท": 0,
    "500 - 1,500 บาท": 1,
    "1,501 - 2,500 บาท": 2,
    "2,501 - 3,500 บาท": 3,
    "3,501 - 4,500 บาท": 4,
    "4,501 - 5,500 บาท" : 5,
    "มากกว่า 5,500 บาท" : 6
}

# รวมทั้งสาม dataframe
frames = [grouped_8_1, grouped_8_2, grouped_8_3]
df_concat = pd.concat(frames)

# รวมคอลัมน์ที่มีค่าเหมือนกันและบวกค่าจำนวนนักศึกษา
grouped_df_8 = df_concat.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).sum().reset_index()

# เปลี่ยนชื่อคอลัมน์เพื่อความชัดเจน
grouped_df_8.rename(columns={'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1': 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด'}, inplace=True)
grouped_df_8.rename(columns={'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?': 'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'}, inplace=True)

# ลบคอลัมน์ที่ไม่จำเป็นออก
grouped_df_8.drop(['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2', 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?', 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3', 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'], axis=1, inplace=True)

# เพิ่มคอลัมน์ลำดับใหม่
grouped_df_8["ลำดับ"] = grouped_df_8["คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"].map(reorder_expenses_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ"
grouped_df_8 = grouped_df_8.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# สร้าง DataFrame จากข้อมูลที่มีอยู่
data = {
    'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?': grouped_df_8["คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"].tolist(),
    'จำนวนนักศึกษา': grouped_df_8["จำนวนนักศึกษา"].tolist(),
    'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด': grouped_df_8["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด"].tolist()
}
df2 = pd.DataFrame(data)

# สร้างกราฟ
chart8 = alt.Chart(df2).mark_bar().encode(
    y=alt.Y('คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?:N', title='ค่าใช้จ่ายโดยประมาณต่อหนึ่งเดือน'),
    x=alt.X('จำนวนนักศึกษา:Q', title='จำนวนนักศึกษา (คน)'),
    color='ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด:N',
    order=alt.Order(
      'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด:N',
      sort='ascending'
    )
).properties(
    width=600,
    height=400,
    title='7.แผนภูมิแท่ง แสดงการเปรียบเทียบประเภทค่าใช้จ่ายส่วนที่มากที่สุดกับปริมาณค่าใช้จ่ายที่ในส่วนนั้น'
)

# สร้าง dictionary เพื่อกำหนดลำดับใหม่สำหรับจำนวนเงินที่ใช้จ่าย
reorder_expenses_map = [
    "ต่ำกว่า 500 บาท",
    "500 - 1,500 บาท",
    "1,501 - 2,500 บาท",
    "2,501 - 3,500 บาท",
    "3,501 - 4,500 บาท",
    "4,501 - 5,500 บาท",
    "มากกว่า 5,500 บาท"
]


# นับจำนวนข้อมูลในแต่ละกลุ่มของคอลัมน์ 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1' และ 'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'
grouped_9_1 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")
grouped_9_2 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")
grouped_9_3 = df.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3", "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).size().reset_index(name="จำนวนนักศึกษา")

# เปลี่ยนชื่อคอลัมน์
grouped_9_1.rename(columns={'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1': 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด'}, inplace=True)
grouped_9_1.rename(columns={'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?': 'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'}, inplace=True)
grouped_9_2.rename(columns={'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2': 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด'}, inplace=True)
grouped_9_2.rename(columns={'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?': 'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'}, inplace=True)
grouped_9_3.rename(columns={'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3': 'ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด'}, inplace=True)
grouped_9_3.rename(columns={'จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?': 'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'}, inplace=True)

# รวม dataframe ทั้งสามอัน
group_9_concat = pd.concat([grouped_9_1, grouped_9_2, grouped_9_3])

# group ตาม column คอลัมน์ "ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด", "คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?" ที่เหมือนกัน แล้วบวกจำนวนนักศึกษา
group_9_final = group_9_concat.groupby(["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด", "คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]).sum().reset_index()

# สร้าง pivot table จากข้อมูล
pivot_table_9 = group_9_final.pivot(index="ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด", columns="คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?", values="จำนวนนักศึกษา")
# เรียงลำดับคอลัมน์ใน pivot_table
pivot_table_9 = pivot_table_9.sort_index(axis=1)

# ทำการ melt ข้อมูล
data_melted = pivot_table_9.reset_index().melt(id_vars='ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด', var_name='คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?', value_name='จำนวนนักศึกษา')

# สร้าง Heatmap
heatmap = alt.Chart(data_melted).mark_rect().encode(
    x= alt.X('คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?:O', sort=reorder_expenses_map),
    y= alt.Y('ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด:O'),
    color='จำนวนนักศึกษา:Q',
    tooltip=['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุด', 'คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?', 'จำนวนนักศึกษา']
).properties(
    title='8.Heatmap แสดงการเปรียบเทียบประเภทค่าใช้จ่ายส่วนที่มากที่สุดกับปริมาณค่าใช้จ่ายที่ในส่วนนั้น',
    width=768,
    height=1024
)

# สร้าง Text Layer สำหรับแสดงข้อความบนแต่ละ cell ของ Heatmap
text = heatmap.mark_text(baseline='middle').encode(
    text='จำนวนนักศึกษา:Q',
    color=alt.value('black')
)

# รวม Heatmap และ Text Layer เข้าด้วยกัน
chart9 = heatmap + text

# สร้าง dictionary เพื่อกำหนดลำดับใหม่สำหรับจำนวนเงินที่ใช้จ่าย
reorder_income_map = [
    "น้อยกว่า 50 บาท",
    "50 - 100 บาท",
    "101 - 200 บาท",
    "201 - 300 บาท",
    "มากกว่า 300 บาท"
]
# นับจำนวนข้อมูลในแต่ละกลุ่มของนักศึกษาตามสถานที่พักอาศัย, และคุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?
grouped_9 = df.groupby(["สถานที่พักอาศัย", "คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง Heatmap
heatmap = alt.Chart(grouped_9).mark_rect().encode(
    x= alt.X('คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?:O', sort=reorder_income_map),
    y= alt.Y('สถานที่พักอาศัย:O'),
    color='จำนวนนักศึกษา:Q',
    tooltip=['สถานที่พักอาศัย', 'คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?', 'จำนวนนักศึกษา']
).properties(
    title='4.Heatmap แสดงการเปรียบเทียบสถานที่พักอาศัยกับค่าใช้จ่ายโดยเฉลี่ยในรายวัน',
    width=600,
    height=400
)

# สร้าง Text Layer สำหรับแสดงข้อความบนแต่ละ cell ของ Heatmap
text = heatmap.mark_text(baseline='middle').encode(
    text='จำนวนนักศึกษา:Q',
    color=alt.value('black')
)

# รวม Heatmap และ Text Layer เข้าด้วยกัน
chart4 = heatmap + text


import streamlit as st

# Insert custom CSS to change sidebar color
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #FF5733;  /* Change the color to your preference */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("พฤติกรรมการใช้จ่ายของนักศึกษามหาวิทยาลัยธรรมศาสตร์")

# Widget for selecting the chart with a title
selected_chart = st.sidebar.selectbox("Select Chart:", 
                                       ["ประชากรผู้ตอบแบบสอบถาม", 
                                        "รายได้ต่อเดือน", 
                                        "ค่าใช่จ่ายเฉลี่ยต่อวัน",
                                        "เปรียบเทียบสถานที่พักกับค่าใช้จ่าย", 
                                        "เปรียบเทียบเพศกับค่าใช้จ่ายอันดับ1", 
                                        "เปรียบเทียบเพศกับค่าใช้จ่ายอันดับ2", 
                                        "เปรียบเทียบเพศกับค่าใช้จ่ายอันดับ3",
                                        "เปรียบเทียบค่าใช้จ่ายในส่วนที่มากสุด"])


# Define the layout of the charts within a single row
col1, col2, col3 = st.columns([1, 4, 1])

# Empty column on the left
with col1:
    pass

# Chart for the middle column
with col2:
    if selected_chart == "ประชากรผู้ตอบแบบสอบถาม":
        st.altair_chart(combined_donut, use_container_width=True)
    elif selected_chart == "รายได้ต่อเดือน":
        st.altair_chart(chart2, use_container_width=True)
    elif selected_chart == "ค่าใช่จ่ายเฉลี่ยต่อวัน":
        st.altair_chart(chart6, use_container_width=True)
    elif selected_chart == "เปรียบเทียบสถานที่พักกับค่าใช้จ่าย":
        st.altair_chart(chart4, use_container_width=True)
    elif selected_chart == "เปรียบเทียบเพศกับค่าใช้จ่ายอันดับ1":
        st.altair_chart(chart3_1, use_container_width=True)
    elif selected_chart == "เปรียบเทียบเพศกับค่าใช้จ่ายอันดับ2":
        st.altair_chart(chart3_2, use_container_width=True)
    elif selected_chart == "เปรียบเทียบเพศกับค่าใช้จ่ายอันดับ3":
        st.altair_chart(chart3_3, use_container_width=True)
    elif selected_chart == "เปรียบเทียบค่าใช้จ่ายในส่วนที่มากสุด":
        st.altair_chart(chart9, use_container_width=True)
    
    

# Empty column on the right
with col3:
    pass

# Define the layout of the charts within two rows
col2_top, col2_bottom = st.columns(2)

# Charts for the top row of col2
with col2_top:
    st.altair_chart(chart2, use_container_width=True)
    st.altair_chart(chart4, use_container_width=True)
    st.altair_chart(chart3_2, use_container_width=True)

# Charts for the bottom row of col2
with col2_bottom:
    st.altair_chart(chart6, use_container_width=True)
    st.altair_chart(chart3_1, use_container_width=True)
    st.altair_chart(chart3_3, use_container_width=True)

# Chart at the center bottom
st.altair_chart(chart9, use_container_width=True)
