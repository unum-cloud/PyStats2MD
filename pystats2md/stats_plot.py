import copy

import plotly.graph_objects as go
import plotly.express as px

from pystats2md.helpers import *


class StatsPlot(object):

    def __init__(self, table, title: str, show_values=False):
        self.table = table
        self.title = title
        self.show_values = show_values

    def save_to(self, path: str = '') -> str:
        comparisons = self.table.header_row
        variants = self.table.header_col
        availiable_colors = px.colors.qualitative.Prism

        fig = go.Figure()
        for i, v in enumerate(variants):
            fig.add_trace(go.Bar(
                name=v,
                x=comparisons,
                #
                y=self.table.content[i],
                marker_color=availiable_colors[i % len(availiable_colors)],
                #
                text=(self.table.content[i] if self.show_values else None),
                texttemplate=('%{text:.2s}' if self.show_values else None),
                textposition='auto',
            ))

        # https://plotly.com/python/bar-charts/
        fig.update_layout(
            title_text=self.title,
            #
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
