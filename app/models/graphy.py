import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
import base64


class Wordy:
    r"""Classe feita para gerar grafico WordCloud, tem duas funções, uma para gerar o grafico e a outra para renderizar o grafico.

    Parameters
    ----------
    text_entries : string
        É o conjunto de strings usado para fazer o wordcloud.
    stp_words : set[str]
        É o set de strings utilzado como stopwords, não precisa ser definido, o default está com a lista STOPWORDS do wordcloud.
    w : int
        É o parametro de largura do wordcloud, também já tem valor default.
    h : int
        É o parametro de altura do wordcloud, também já tem valor default.
    bg : str
        É o campo de cor de fundo, usa o padrão de cores do matplotlib, https://matplotlib.org/stable/gallery/color/named_colors.html
    cm : str
        É o campo de colormap das palavras, usa o padrão de colormaps do matplotlib, https://matplotlib.org/stable/users/explain/colors/colormaps.html
    dt : str
        Este campo não deve ser preenchido, ele é o atributo de Data fstring, onde está sendo armazenado o dado em .png para ser utilizado no hrml
        para renderizar o grafico.

"""
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
        r"""Utilize desta função para criar o wordcloud, 
        intanciando os dados no objeto, assim conseguindo usar a proxima função
        .. code-block:: python
            obj = Wordy(text_entries,stp_words,w,h,bg,dt,cm)
            obj.create_wordcloud()
            
        .. seealso::

            :ref:`get_wc`"""
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
        r"""Utilize desta função para conseguir uma saida dos 
        dados do wordcloud, made estes dados para o html para a renderizar o grafico        
        .. code-block:: python

            @app.route("/")
            def index():
                return render_template(wordcloud=obj.get_wc())"""
        return self.dt

class Ploty:
    r"""Classe feita para gerar grafico Plotly interativo, 
    tem duas funções, uma para gerar o grafico e a outra para renderizar o grafico.

    Parameters
    ----------
    df : DataFrame
        É o dataframe que vai ser utilizado para gerar o grafico.
    xv : str
        É o eixo 'x', neste caso deve ser informado o nome da coluna do dataframe que vai ser utilizado.
    xlen : int
        É o parametro de largura do grafico.
    yv : str
        É o eixo 'y', neste caso deve ser informado o nome da coluna do dataframe que vai ser utilizado.
    tit : str
        É o campo de titulo.
    ht : str
        Este campo não deve ser preenchido, ele é a representação da figura em html <div>figure</div>


"""
    def __init__(self, df=None, xv=None, xlen=None, yv=None, 
                 tit="placeholder", ht=None):
        self.df = df
        self.xv = xv
        self.yv = yv
        self.tit = tit
        self.xlen = xlen
        self.ht = ht


    def create_fig(self):
        r"""Utilize desta função para criar o grafico plotly, 
        intanciando os dados no objeto, assim conseguindo usar a proxima função
        .. code-block:: python
            fig = Ploty(df,xv,xlen,yv,tit)
            fig.create_fig()
            
        
        .. seealso::

            :ref:`get_ht`"""
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
        r"""Utilize desta função para conseguir uma figura em html do grafico, 
        mande este dado para o html para renderizar o grafico interativo
        .. code-block:: python

            @app.route("/")
            def index():
                return render_template(graph_html=fig.get_ht())"""
        return self.ht