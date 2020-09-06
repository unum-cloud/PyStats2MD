import copy

import plotly.graph_objects as go
import plotly.express as px

from pystats2md.helpers import *


class StatsPlot(object):

    def __init__(self, table, title: str, print_height=True, print_cols_names=True, print_rows_names=True):
        self.table = table
        self.title = title
        self.print_height = print_height
        self.print_cols_names = print_cols_names
        self.print_rows_names = print_rows_names

    def save_to(self, path: str = '') -> str:
        cols_names = self.table.header_row if self.print_cols_names else ([''] * len(self.table.header_row))
        rows_names = self.table.header_col if self.print_rows_names else ([''] * len(self.table.header_col))
        availiable_colors = px.colors.qualitative.Prism

        fig = go.Figure()
        for row_idx, row_name in enumerate(rows_names):
            fig.add_trace(go.Bar(
                name=row_name,
                x=cols_names,
                #
                y=self.table.content[row_idx],
                marker_color=availiable_colors[row_idx % len(availiable_colors)],
                #
                text=(self.table.content[row_idx] if self.print_height else None),
                texttemplate=('%{text:.2s}' if self.print_height else None),
                textposition='auto',
            ))

        # https://plotly.com/python/bar-charts/
        # https://plotly.com/python/tick-formatting/
        # https://plotly.com/python/axes/
        fig.update_layout(
            title_text=self.title,
            #
            # xaxis_tickfont=dict(
            #     family='Rockwell', 
            #     color='crimson', 
            #     size=14,                
            # ),
            xaxis_tickangle=-45,
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            #
            barmode='group',
            # gap between bars of adjacent location coordinates.
            bargap=0.15,
            # gap between bars of the same location coordinate.
            bargroupgap=0.1,
        )
        fig.write_image(path)
        return path
