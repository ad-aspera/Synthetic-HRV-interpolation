"""
Created on Wed Jan 29 15:35:35 2025

@author: henryhollingworth

Based on the review:

Shaffer, F. and Ginsberg, J.P., 2017. An overview of heart rate variability metrics and norms. Frontiers in Public Health, 5, p.258. Available at: https://pmc.ncbi.nlm.nih.gov/articles/PMC5624990/ [Accessed 28 Jan. 2025].

Priority for time domain measures: RMSSD, SDNN, pNN50
Priority for Frequency domain measures: LF Bands, HF Bands, LF/HF
"""
#Dependencies
import numpy as np
import pandas as pd


class TD_metrics:
    """class calculates time domain metrics for a pd.series type list of RR intervals"""
    def __init__(self, data: pd.Series):
        if not isinstance(data, pd.Series):#establish correct type should be pd.series
            raise TypeError(f"Expected a pandas Series, but got {type(HRV_data).__name__}")
        self.data = data.dropna().values #drop Nan values


    def SDRR(self):
        """Standard deviation of RR intervals"""
        return np.std(self.data, ddof=1)
    def pNN50(self):
        """Percentage of successive RR intervals that differ by more than 50 ms"""
        diff_rr = np.abs(np.diff(self.data))
        return np.sum(diff_rr > 50) / len(diff_rr) * 100
    def RMSSD(self):
        """Root mean square of successive RR interval differences"""
        diff_rr = np.diff(self.data)
        return np.sqrt(np.mean(diff_rr ** 2))
    def mean_hr(self):
        """mean HR in bpm"""
        mean_rr = np.mean(self.data)
        return 60000 / mean_rr  # Convert ms to bpm
    def get_all_metrics(self):
        """Dictionary of time domain metrics (all vals as should be np.float64)"""
        return {
            "SDRR": self.SDRR(),
            "RMSSD": self.RMSSD(),
            "pNN50 (%)": self.pNN50(),
            "Mean HR (bpm)": self.mean_hr()
        }
