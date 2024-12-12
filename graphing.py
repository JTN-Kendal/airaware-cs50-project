from dash import Dash, html, dcc
import plotly.express as px
import plotly
import plotly.graph_objects as go
import json
import pandas as pd
from pprint import pprint


def build_graph():
    # Example 1: Simple line chart
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Example Line'))
    fig.update_layout(
        title='Simple Line Chart',
        xaxis_title='X Values',
        yaxis_title='Y Values',
        template='plotly_white'
    )

    # Convert the plot to JSON for embedding
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json


def create_interactive_graph(db):
    # Get data and convert to pandas DataFrame
    data = db.execute("""
        SELECT 
            sl.name as location,
            p.name as pollutant,
            m.value,
            m.measured_at as date
        FROM measurements m
        JOIN sub_locations sl ON m.sub_location_id = sl.sub_location_id
        JOIN pollutants p ON m.pollutant_id = p.pollutant_id
        ORDER BY m.measured_at DESC
    """).fetchall()

    df = pd.DataFrame([dict(row) for row in data])

    # Count unique pollutants to know the number of facets when formatting later on
    num_pollutants = len(df['pollutant'].unique())

    # Create figure
    fig = px.bar(df,
                 x='date',
                 y='value',
                 color='location',
                 facet_row="pollutant",
                 facet_row_spacing=0.05,
                 title='Air Quality Measurements - All Locations'
                 )
    # Update the facet labels to remove the prefix to make more legible
    fig.for_each_annotation(lambda a: a.update(
        text=a.text.split("=")[-1].replace(" Particulate matter", "")
        if "Particulate matter" in a.text
        else a.text.split("=")[-1])
                            )

    # Shows only the legend to start with and no data so that options can be selected
    for trace in fig.data:
        trace.visible = 'legendonly'

    # Update layout settings
    fig.update_layout(
        font_size=8,
        height=900,
        title_x=0.07,  # Align title left
        title_y=0.92,
        legend_title_text='Location',
        showlegend=True,
        title_font_size=20,
        legend=dict(
            font=dict(size=15),
            title=dict(font=dict(size=20)),
        )
    )

    # Update all x-axes to show tick labels but no axis title
    fig.update_xaxes(
        showticklabels=True,
        title_text='',
        title_font_size=20,
    )

    # Then, update only the last facet to show both tick labels and axis title
    fig.update_xaxes(
        title_text='Date',
        title_font_size=20,
        showticklabels=True,
        row=num_pollutants  # Use the actual last row number
    )

    fig.update_yaxes(title_text='(µg/m³)')

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


if __name__ == '__main__':
    build_graph()
