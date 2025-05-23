# -*- coding: utf-8 -*-
"""APP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n6QQKuG2MPsJ6NpZNkryygKRaBBcQC47
"""

#!pip install ipywidgets xgboost --quiet

#!pip install gradio

import joblib
import numpy as np
#import ipywidgets as widgets
#from IPython.display import display, clear_output
import pandas as pd
import gradio as gr

def preprocess_input(ohlc_list):
    df = pd.DataFrame(np.array(ohlc_list).reshape(8, 4), columns=['Open', 'High', 'Low', 'Close'])
    ohlc = ['Open', 'High', 'Low', 'Close']
    lag_days = [3, 5, 7]

    lagged_cols = []
    for i in lag_days:
      for col in ohlc:
          lagged = df[col].shift(i).rename(f'{col}_lag{i}')
          lagged_cols.append(lagged)

    df = pd.concat([df] + lagged_cols, axis=1)
    #print(df)

    df['HL_range'] = df['High'] - df['Low']
    df['OC_diff'] = df['Close'] - df['Open']
    df['HL_ratio'] = df['High'] / df['Low']
    df['OC_ratio'] = df['Close'] / df['Open']
    df['MA3'] = df['Close'].rolling(window=3).mean()
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['STD3'] = df['Close'].rolling(window=3).std()
    df['EMA3'] = df['Close'].ewm(span=3, adjust=False).mean()
    df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['EMA_diff'] = df['EMA3'] - df['EMA5']
    df['momentum'] = df['Close'] / df['Close'].shift(3) - 1
    df['Adj Close'] = df['Close']
    df = df.fillna(0)

    features = [
        'Open_lag3', 'High_lag3', 'Low_lag3', 'Close_lag3',
        'Open_lag5', 'High_lag5', 'Low_lag5', 'Close_lag5',
        'Open_lag7', 'High_lag7', 'Low_lag7', 'Close_lag7',
        'HL_range', 'OC_diff', 'HL_ratio', 'OC_ratio',
        'MA5', 'STD3',
        'EMA_diff',
        'momentum'
    ]
    #print(df.iloc[-1][features].values.reshape(1, -1))
    return df.iloc[-1][features].values.reshape(1, -1)

model = joblib.load('xgboost_best.pkl')

# paste_box = widgets.Textarea(
#     value='',
#     placeholder='Paste 32 values copied from Excel (separated by space, comma, or tab)',
#     description='Paste',
#     layout=widgets.Layout(width='750px', height='80px')
# )

# def on_paste_clicked(b):
#     with output:
#         clear_output()
#         try:
#             # Split pasted content by space/comma/tab
#             raw_values = paste_box.value.replace('\t', ' ').replace(',', ' ').split()
#             values = [float(v) for v in raw_values if v.strip() != '']

#             if len(values) != 32:
#                 print("❌ Please paste exactly 32 numeric values!")
#                 return

#             for i, v in enumerate(values):
#                 input_boxes[i].value = round(v, 5)

#             print("✅ Successfully filled 32 OHLC values!")
#         except Exception as e:
#             print("❌ Invalid format or non-numeric content:", e)

## paste_button = widgets.Button(description="📥 Parse Paste", button_style='info')
# paste_button.on_click(on_paste_clicked)

# ohlc_fields = ['Open', 'High', 'Low', 'Close']
# input_boxes = [widgets.FloatText(description=f'{field}_{day}', layout=widgets.Layout(width='180px'))
#                for day in range(1, 9) for field in ohlc_fields]

# delta_box = widgets.FloatText(value=0.008, description='Δ', layout=widgets.Layout(width='180px'))
# output = widgets.Output()

# # 阈值设定
# THRESHOLD = 0.55

# # 点击逻辑（整合 preprocessing）
# def on_predict_clicked(b):
#     with output:
#         clear_output()
#         try:
#             values = [box.value for box in input_boxes]
#             if len(values) != 32:
#                 raise ValueError("Please enter complete OHLC data for 8 days (a total of 32 values)")

#             X_processed = preprocess_input(values)
#             #print(X_processed)
#             prob = model.predict_proba(X_processed)[0][1]
#             decision = "✅ YES" if prob >= THRESHOLD else "❌ NO"

#             print(f"📈 Predicted Probability: {prob*100:.2f}%")
#             print(f"🚀 Entry Recommendation: {decision}")
#         except Exception as e:
#             print("❌ Error:", e)

# # 显示界面
# predict_button = widgets.Button(description="Run Prediction", button_style='success')
# predict_button.on_click(on_predict_clicked)

# input_grid = widgets.GridBox(input_boxes, layout=widgets.Layout(grid_template_columns="repeat(4, 180px)"))

# display(widgets.HTML("<h3>Enter or paste the most recent 8 days of OHLC data</h3>"))

# # 粘贴区域：textarea + 按钮
# display(paste_box, paste_button)

# # 输入框（28 个 OHLC）
# display(input_grid)

# # 底部参数区和运行按钮
# display(widgets.HBox([delta_box, predict_button]), output)



# """##You may try these data(1)

# 1.0837	1.0839	1.0787	1.084
# 1.0795	1.0808	1.0784	1.0795
# 1.081	1.0821	1.078	1.081
# 1.0788	1.0864	1.0788	1.0788
# 1.0839	1.0864	1.0808	1.0839
# 1.0849	1.0882	1.0832	1.0849
# 1.0881	1.0904	1.0856	1.0882
# 1.0886	1.1006	1.0886	1.0886

# 0 data:
# 1.1117	1.1145	1.1114	1.1117

# 1.1134	1.1146	1.1106	1.1136

# 1.113	1.1163	1.112	1.1131

# 1.1153	1.1172	1.113	1.1154

# 1.1138	1.1145	1.1088	1.114

# 1.1095	1.1105	1.1078	1.1095

# 1.1096	1.112	1.1086	1.1097

# 1.1086	1.1098	1.1072	1.1086
# """

def predict_ohlc(pasted_text, delta=0.008, threshold=0.55):
    try:
        # 处理输入数据
        values = [float(v) for v in pasted_text.replace(",", " ").replace("\t", " ").split()]
        if len(values) != 32:
            return "❌ Please enter exactly 32 OHLC values (8 days × 4 = 32)"

        X = preprocess_input(values)
        prob = model.predict_proba(X)[0][1]
        decision = "✅ YES (enter trade)" if prob >= threshold else "❌ NO (do not enter)"

        return f"📈 Predicted Probability: {prob:.2%}\n🚀 Entry Recommendation: {decision}"
    except Exception as e:
        return f"❌ Error: {e}"

# 创建 Gradio 网页界面
interface = gr.Interface(
    fn=predict_ohlc,
    inputs=[
        gr.Textbox(lines=4, label="Paste 32 OHLC values (Open, High, Low, Close × 8 days)"),
        gr.Number(value=0.008, label="Δ (Delta)"),
        gr.Slider(0.0, 1.0, value=0.55, step=0.01, label="Threshold for Entry")
    ],
    outputs="text",
    title="EUR/USD Trading Entry Predictor",
    description="""
 **Instructions**:
Paste OHLC (Open, High, Low, Close) data for the past 8 days — total 32 values, separated by spaces.  
Adjust Δ and threshold if needed, then click **Run** to get the prediction.

 **Example - Entry Recommended**:  
1.0837 1.0839 1.0787 1.084  1.0795 1.0808 1.0784 1.0795  
1.081 1.0821 1.078 1.081  1.0788 1.0864 1.0788 1.0788  
1.0839 1.0864 1.0808 1.0839  1.0849 1.0882 1.0832 1.0849  
1.0881 1.0904 1.0856 1.0882  1.0886 1.1006 1.0886 1.0886

 **Example - Entry Not Recommended**:  
1.1117 1.1145 1.1114 1.1117  1.1134 1.1146 1.1106 1.1136  
1.113 1.1163 1.112 1.1131  1.1153 1.1172 1.113 1.1154  
1.1138 1.1145 1.1088 1.114  1.1095 1.1105 1.1078 1.1095  
1.1096 1.112 1.1086 1.1097  1.1086 1.1098 1.1072 1.1086
"""
)

import os
port = int(os.environ.get("PORT", 8080))
interface.launch(server_name="0.0.0.0", server_port=port)
