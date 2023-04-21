#!/usr/bin/python
# -*- coding: <encoding name> -*-

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

fig = px.bar(buyer, x="year", y="거래처코드", title='연도별 거래처수 변동추이')

app = Dash(__name__)
# app layout: html과 dcc 모듈을 이용
app.layout = html.Div(children=[
    # Dash HTML Components module로 HTML 작성 
    html.H1(children='첫번째 Dash 화면'),
    html.Div(children='''
        대시를 이용하여 웹어플리케이션 작성 연습...
    '''),
    
    
    # dash.core.component(dcc)의 그래프컴포넌트로 plotly 그래프 렌더링
    dcc.Graph(
        id='graph1',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False, host='0.0.0.0', port=8888)