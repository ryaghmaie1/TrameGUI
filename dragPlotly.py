# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 11:34:55 2022

@author: RYaghmaie173178
"""

import json
from textwrap import dedent as d
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

app = dash.Dash(__name__)
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/dZVMbK.css'})

styles = {'pre': {'border': 'thin lightgrey solid', 'overflowX': 'scroll'}}


figks = go.Figure()

figks.add_shape(type="circle",
    xref= 'x', yref="y",
    fillcolor='grey',
    x0=-2, y0=-2, x1=2, y1=2,
    line_color='grey',opacity=0.25,
)
figks.add_shape(type="circle",
    xref= 'x', yref="y",
    fillcolor="white",
    x0=-1, y0=-1, x1=1, y1=1,
    line_color="white",opacity=0.5,
)
    
figks.update_xaxes(range=[-2, 2], zeroline=False)
figks.update_yaxes(range=[-2, 2])
figks.update_layout(width=600, height=600,
                    title = "<b>Plot-1</b>")

devx = [-0.3, 0.3]
devy = [-0.2, 0.2]
figks.add_shape(type="rect",
    xref= 'x', yref="y",
    fillcolor='blue',
    x0=devx[0], y0=devy[0],
    x1=devx[1], y1=devy[1],
    line_color='blue',opacity=0.75, editable=True
)


figks.add_shape(type="rect",
    xref= 'x', yref="y",
    fillcolor='red',
    x0=1.2, y0=-1.2,
    x1=1.4, y1=-1.4,
    line_color='red',opacity=0.75, editable=True
)

figks.add_shape(type="rect",
    xref= 'x', yref="y",
    fillcolor='green',
    x0=1.5, y0=0,
    x1=1.8, y1=0.3,
    line_color='green',opacity=0.75, editable=True
)

app.layout = html.Div(className='row', children=[
    dcc.Graph(
        id='basic-interactions',
        className='six columns',
        figure=figks,
        config={
            'editable': True,
            'edits': {
                'shapePosition': True
            }
        }
    ),
    html.Div(
        className='six columns',
        children=[
            html.Div(
                [
                    dcc.Markdown(
                        d("""
                **Zoom and Relayout Data**

            """)),
                    html.Pre(id='relayout-data', style=styles['pre']),
                ]
            )
        ]
    )
])


@app.callback(
    Output('relayout-data', 'children'),
    [Input('basic-interactions', 'relayoutData')])
def display_selected_data(relayoutData):
    
    print('relayoutData=', relayoutData)
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=False)