from models import *
from tkinter import ttk
import tkinter as tk

interface = tk.Tk()
interface.title('Trading model simulator')
interface.geometry('1000x600')

selected_model = tk.StringVar()

def show_selected_frame(model):
    for f in model_frames.values():
        f.pack_forget() #removing all the frames
    frame = model_frames.get(model) #showing the frame of chosen model
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

tk.Label(ma_frame, text="Short MA period:").grid(row=0, column=0)
ma_short = tk.IntVar(value=10)
tk.Entry(ma_frame, textvariable=ma_short).grid(row=0, column=1, padx=6, pady=2)

tk.Label(ma_frame, text="Long MA period:").grid(row=1, column=0)
ma_long = tk.IntVar(value=50)
tk.Entry(ma_frame, textvariable=ma_long).grid(row=1, column=1, padx=6, pady=2)


model_frames["Moving Average Crossover"] = ma_frame

#logistic regression frame
logreg_frame = tk.Frame(container)

tk.Label(logreg_frame, text="Train Features :(period,short,long)").grid(row=0, column=0)
logreg_features = tk.StringVar(value="14,5,20") #temporary
tk.Entry(logreg_frame, textvariable=logreg_features, width=30).grid(row=0, column=1, padx=6, pady=2)

tk.Label(logreg_frame, text="Strategy Bounnds (High,Low)").grid(row=1, column=0)
logreg_bounds = tk.StringVar(value="0.53,0.50")
tk.Entry(logreg_frame, textvariable=logreg_bounds).grid(row=1, column=1, padx=6, pady=2)

tk.Label(logreg_frame, text="Train Split (between 1.0-0.0):").grid(row=2, column=0)#temporary
logreg_split = tk.DoubleVar(value=0.7)
tk.Entry(logreg_frame, textvariable=logreg_split).grid(row=2, column=1, padx=6, pady=2)

model_frames["Logistic Regression"] = logreg_frame
show_selected_frame(combo_box.get())


tick_dates_frame = tk.Frame(interface)
tick_dates_frame.pack(pady=10)

tk.Label(tick_dates_frame, text="Ticker:").grid(row=0, column = 1, padx=10, pady=5)
tick = tk.Entry(tick_dates_frame, width=30)
tick.insert(0,'AAPL')
tick.grid(row=1,column =1,padx= 10, pady = 5)

tk.Label(tick_dates_frame, text="start:").grid(row=2, column=0,padx = 10, pady=5)
start = tk.Entry(tick_dates_frame)
start.insert(0,'2018-01-01')
start.grid(row=2, column=1, padx=10, pady=5)

tk.Label(tick_dates_frame, text="end:").grid(row=2, column=2, pady=5)
end = tk.Entry(tick_dates_frame)
end.insert(0,'2025-12-01')
end.grid(row=2, column=3, padx=10, pady=5)

def run():
    model = selected_model.get()
    pct_return = 0
    returns = None

    if model == "Rsi Mean Reversion":
        data = {
            "model": model,
            "rsi_period": rsi_period.get(),
            "overbought": rsi_overbought.get(),
            "oversold": rsi_oversold.get(),
        }
        model = rsi_mean_reversion(start.get(),end.get(),tick.get())
        returns = model.get_money(data['rsi_period'],data['overbought'],data['oversold'])
        pct_return = model.plot_returns(returns)

    elif model == "Moving Average Crossover":
        data = {
            "model": model,
            "short_ma": ma_short.get(),
            "long_ma": ma_long.get(),
        }
        model = moving_average_crossover(start.get(),end.get(),tick.get())
        returns = model.get_returns(data['short_ma'],data['long_ma'])
        pct_return = model.plot_returns(returns)

    elif model == "Logistic Regression":
        data = {
            "model": model,
            "features": [int(f.strip()) for f in logreg_features.get().split(",")],#period,short,long
            "bounds": [float(f.strip()) for f in logreg_bounds.get().split(",")],#High,Low
            "test_split": logreg_split.get(),
        }
        model = logistic_regression(start.get(),end.get(),tick.get())
        model.get_features(data['features'][0],data['features'][1],data['features'][2])
        model.train(data['test_split'])
        returns = model.strategy(data['bounds'][0],data['bounds'][1])
        pct_return = model.plot_returns(returns)

    else:
        data = {"model": model}
        
    returns_box.delete("1.0", tk.END)
    returns_box.insert(tk.END, f"{pct_return}%")

returns_frame = tk.Frame(interface)
returns_frame.pack(pady=10)
returns_label = tk.Label(returns_frame, text="Percentage return:")
returns_label.pack(side="left")

returns_box = tk.Text(returns_frame, height=1, width=10)
returns_box.pack(side="left")

submit_btn = tk.Button(interface, text="Run", command=run)
submit_btn.pack(pady=12)

interface.mainloop()
