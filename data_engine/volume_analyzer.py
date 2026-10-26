import pandas as pd

class VolumeAnalyzer:
    def __init__(self):
        pass

    def analyze_volume_spikes(self, df: pd.DataFrame, window: int = 20, multiplier: float = 2.0) -> pd.DataFrame:
        """
        تحليل الفوليوم واكتشاف الشموع ذات السيولة العالية (Volume Spikes)
        """
        if df.empty or 'Volume' not in df.columns:
            return df
            
        # حساب المتوسط المتحرك للفوليوم لفترة معينة (افتراضياً 20 شمعة)
        df['Volume_MA'] = df['Volume'].rolling(window=window).mean()
        
        # رصد الشموع التي يتجاوز فيها الحجم ضعف المتوسط المتحرك
        df['Is_Volume_Spike'] = df['Volume'] > (df['Volume_MA'] * multiplier)
        
        return df

    def get_liquidity_summary(self, df: pd.DataFrame) -> str:
        """
        إصدار ملخص لحالة السيولة والفوليوم في آخر الشموع
        """
        analyzed_df = self.analyze_volume_spikes(df)
        if analyzed_df.empty or 'Is_Volume_Spike' not in analyzed_df.columns:
            return "لا توجد بيانات كافية لتحليل الفوليوم."
            
        recent_spikes = analyzed_df[analyzed_df['Is_Volume_Spike'] == True]
        
        if not recent_spikes.empty:
            return f"تم رصد {len(recent_spikes)} شمعة ذات سيولة عالية (Volume Spikes) في الفترة الأخيرة، مما يدل على دخول أموال مؤسسية."
        else:
            return "حركة الفوليوم طبيعية ولا توجد طفرات سيولة استثنائية حالياً."
