from models import *
from tkinter import ttk
import tkinter as tk

interface = tk.Tk()
interface.title('Trading model simulator')
interface.geometry('1000x550')

selected_model = tk.StringVar()

def show_selected_frame(model):
    for f in model_frames.values():
        f.pack_forget() #here I am basically removing all the frames and on the next line below I only show the frames for the model thats selected
    frame = model_frames.get(model) 
    if frame:
        frame.pack(fill = 'x',padx = 20,pady=15)

def selection(event=None):
    model = selected_model.get()
    model_label.config(text = f'selected model : {model}')
    show_selected_frame(model)

model_label = tk.Label(interface,text = 'select a model')
model_label.pack(pady=(11,4))

combo_box = ttk.Combobox(
    interface,
    textvar= selected_model,
    values=["Rsi Mean Reversion", "Moving Average Crossover", "Logistic Regression"],
    state="readonly",
    width=30
)
combo_box.pack(pady = (0,8))
combo_box.bind("<<ComboboxSelected>>", selection)
combo_box.set("Moving Average Crossover")

container = tk.Frame(interface)
container.pack(fill="both", expand=False)

model_frames = {

}

rsi_frame = tk.Frame(container)

tk.Label(rsi_frame, text="RSI Period:").grid(row=0, column=0)
rsi_period = tk.IntVar(value=14)
tk.Entry(rsi_frame, textvariable=rsi_period).grid(row=0, column=1, padx=6, pady=2)

tk.Label(rsi_frame, text="Overbought Threshold:").grid(row=1, column=0)
rsi_overbought = tk.DoubleVar(value=70.0)
tk.Entry(rsi_frame, textvariable=rsi_overbought).grid(row=1, column=1, padx=6, pady=2)

tk.Label(rsi_frame, text="Oversold Threshold:").grid(row=2, column=0)
rsi_oversold = tk.DoubleVar(value=30.0)
tk.Entry(rsi_frame, textvariable=rsi_oversold).grid(row=2, column=1, padx=6, pady=2)

model_frames["Rsi Mean Reversion"] = rsi_frame

#moving average frame
ma_frame = tk.Frame(container)

tk.Label(ma_frame, text="Short MA Period:").grid(row=0, column=0)
ma_short = tk.IntVar(value=10)
tk.Entry(ma_frame, textvariable=ma_short).grid(row=0, column=1, padx=6, pady=2)

tk.Label(ma_frame, text="Long MA Period:").grid(row=1, column=0)
ma_long = tk.IntVar(value=50)
tk.Entry(ma_frame, textvariable=ma_long).grid(row=1, column=1, padx=6, pady=2)


model_frames["Moving Average Crossover"] = ma_frame

#logistic regression frame type shit
logreg_frame = tk.Frame(container)

tk.Label(logreg_frame, text="Features:").grid(row=0, column=0)
logreg_features = tk.StringVar(value="open,high,low,close") #gonna change these inputs to stuff required for log reg
tk.Entry(logreg_frame, textvariable=logreg_features, width=30).grid(row=0, column=1, padx=6, pady=2)

tk.Label(logreg_frame, text="Regularisation:").grid(row=1, column=0)
logreg_C = tk.DoubleVar(value=1.0)
tk.Entry(logreg_frame, textvariable=logreg_C).grid(row=1, column=1, padx=6, pady=2)

tk.Label(logreg_frame, text=":").grid(row=2, column=0)
logreg_split = tk.DoubleVar(value=0.2)
tk.Entry(logreg_frame, textvariable=logreg_split).grid(row=2, column=1, padx=6, pady=2)

model_frames["Logistic Regression"] = logreg_frame

show_selected_frame(combo_box.get())

#stock and date range selection below
tk.Label(interface, text="Ticker:").pack()
stock = tk.Entry(interface, width=30)
stock.insert(0,'AAPL')
stock.pack(pady=5)

dates_frame = tk.Frame(interface)
dates_frame.pack(pady=10)

tk.Label(dates_frame, text="start:").grid(row=0, column=0, padx=10, pady=5)
start = tk.Entry(dates_frame)
start.insert(0,'2023-12-01')
start.grid(row=0, column=1, padx=10, pady=5)

tk.Label(dates_frame, text="end:").grid(row=0, column=2, padx=10, pady=5)
end = tk.Entry(dates_frame)
end.insert(0,'2025-12-01')
end.grid(row=0, column=3, padx=10, pady=5)

def run():
    model = selected_model.get()

    if model == "Rsi Mean Reversion":
        data = {
            "model": model,
            "rsi_period": rsi_period.get(),
            "overbought": rsi_overbought.get(),
            "oversold": rsi_oversold.get(),
        }

    elif model == "Moving Average Crossover":
        data = {
            "model": model,
            "short_ma": ma_short.get(),
            "long_ma": ma_long.get(),
        }
        model = moving_average_crossover(start.get(),end.get(),stock.get())
        returns = model.get_returns(data['short_ma'],data['long_ma'])
        print(model.plot_returns(returns))

    elif model == "Logistic Regression":
        data = {
            "model": model,
            "features": [f.strip() for f in logreg_features.get().split(",") if f.strip()],
            "C": logreg_C.get(),
            "test_split": logreg_split.get(),
        }
    else:
        data = {"model": model}

returns_frame = tk.Frame(interface)
returns_frame.pack(pady=10)
returns_label = tk.Label(returns_frame, text="Percentage return:")
returns_label.pack(side="left")

returns_box = tk.Text(returns_frame, height=1, width=10)
returns_box.pack(side="left")

submit_btn = tk.Button(interface, text="Run", command=run)
submit_btn.pack(pady=12)

interface.mainloop()