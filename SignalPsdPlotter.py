from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class SignalPsdPlotter():
    """This is a plotter used to simplify plotting and exploring a paired signal and its psd"""
    def __init__(self, title:str = None, alpha =0.7):
        self.fig = make_subplots(rows=2, cols=1, subplot_titles=('<b>Signal</b>', '<b>PSD</b>'))
        self.fig.update_layout(height=600, margin=dict(l=20, r=20, t=50, b=20), title_text="Signal and PSD")
        self.alpha = alpha

        d_vert = 0.06
        self.fig.update_layout(yaxis2=dict(domain=[0, 0.5-d_vert]), yaxis=dict(domain=[0.5+d_vert, 1]))
        
        self.fig.update_annotations(font=dict(size=14))  # Ensure subplot titles don't move
        self.fig['layout']['annotations'][1]['y']+=0.06

        title = title or "HRV Signal and PSD plot"
        self.fig.update_layout(title={'text': title, 'x': 0.5, 'xanchor': 'center'} ,
            title_font=dict(family='Arial Black', size=16))

    def plot_signal_and_psd(self, signal: pd.Series, psd: pd.Series, label: str, color: str):
        """Plots the signal and its PSD"""
        self.plot_signal(signal, label, color)
        self.plot_psd(psd, label, color)
        

    def plot_signal(self, signal: pd.Series, label: str, color: str):
        """Plots the signal on the first subplot"""
        self.fig.add_trace(go.Scatter(x=signal.index, y=signal.values, mode='lines', name=label, 
            line=dict(color=color, width=2), opacity=self.alpha), row=1, col=1)
        self.fig.update_xaxes(title_text='Time', range=[0, 100], row=1, col=1)
        self.fig.update_yaxes(title_text='Amplitude', row=1, col=1)

    def plot_psd(self, psd: pd.Series, label: str, color: str, range = [0,0.5]):
        """Plots the PSD on the second subplot"""
        psd = psd[(psd.index >= range[0]) & (psd.index <= range[1])]

        self.fig.add_trace(go.Scatter(x=psd.index, y=psd.values / psd.max(), mode='lines', name=label, 
            line=dict(color=color), opacity=self.alpha), row=2, col=1)
        self.fig.update_xaxes(title_text='Frequency', range=range, row=2, col=1)
        self.fig.update_yaxes(title_text='Normalized Power', row=2, col=1, )

    def show(self):
        def _update_legend():
            unique_labels = set()
            for trace in self.fig['data']:
                if trace['name'] not in unique_labels:
                    unique_labels.add(trace['name'])
                else:
                    trace['showlegend'] = False
            self.fig.update_layout(legend=dict(title='Signals', y=1, xanchor='right'))
            self.fig.update_layout(xaxis1=dict(domain=[0, .85]))

        _update_legend()

        self.fig.show()