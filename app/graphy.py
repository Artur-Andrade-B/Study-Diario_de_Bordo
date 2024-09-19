import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
import base64


class Wordy:
    def __init__(self,text_entries, stp_words=STOPWORDS, w=500, h=500,
                 bg="grey",cm="Blues",dt=None):
        self.text_entries = text_entries
        self.stp_words =stp_words
        self.w = w
        self.h =h
        self.bg = bg
        self.dt = dt
        self.cm = cm

    def create_wordcloud(self):
        self.wordcloud = WordCloud(
            width=self.w, 
            height=self.h,
            random_state=1,
            background_color=self.bg,
            colormap=self.cm,
            collocations=False,
            stopwords=self.stp_words
            ).generate(self.text_entries)
        img_stream = BytesIO()
        self.wordcloud.to_image().save(img_stream, format="PNG")
        img_stream.seek(0)
        img_base64 = base64.b64encode(img_stream.getvalue()).decode("utf-8")
        self.dt = f"data:image/png;base64,{img_base64}"
        
    def get_wc(self):
        return self.dt

class Ploty:
    def __init__(self, df=None, xv=None, xlen=None, yv=None, 
                 tit="placeholder", ht=None):
        self.df = df
        self.xv = xv
        self.yv = yv
        self.tit = tit
        self.xlen = xlen
        self.ht = ht


    def create_fig(self):
        fig_v = px.line(self.df, x=self.xv, y=self.yv, title=self.tit)
        fig_v.update_layout(
            width=self.xlen,
            height=500,
            xaxis_title='Data',
            yaxis_title='Número de Entradas',
            xaxis=dict(
                tickmode='linear',
                tickvals=self.df[self.xv],
                tickformat="%Y-%m-%d",
                tickangle=-45
            )         
        )
        fig_v.update_traces(
            line_color="purple", 
            line_width=3, 
            line_dash="dash"
            )
        self.ht = pio.to_html(fig_v, full_html=False)

    def get_ht(self):
        return self.ht