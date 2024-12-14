import pandas as pd
import plotly.graph_objects as go


def basic_table(data, location_name: str = "Oxford"):
    """Create a styled Plotly table visualization of air quality measurements.

    Converts database query results into a Pandas DataFrame and creates an
    interactive Plotly table with custom styling and formatting.

    Args:
        data (list[sqlite3.Row]): Database query results containing measurement data
            with the following expected fields:
            - loc_name: Location name
            - sub_name: Sub-location name
            - pollutant_name: Pollutant name
            - value: Measurement value
            - status: Measurement status
            - measured_at: Measurement date
        location_name (str, optional): Location name for the table title. Defaults to "Oxford".

    Returns:
        plotly.graph_objects.Figure: Styled Plotly table figure with the following features:
            - Grey header with left-aligned 12pt font
            - Lavender cells with left-aligned 10pt font
            - 600px height
            - Custom title position and margins
            - Automatic column width adjustment

    Notes:
        - Automatically converts measured_at column to datetime format
        - Column headers are derived from DataFrame columns
        - All columns from input data are displayed in the table
    """

    # Convert the raw db data into a df for easy use
    df = pd.DataFrame(dict(row) for row in data)
    df["measured_at"] = pd.to_datetime(df["measured_at"])

    # Create the table using the go object
    tbl = go.Figure(
        data=[go.Table(
            header=(
                dict(
                    values=list(df.columns),
                    fill_color="darkgrey",
                    align="left",
                    font=dict(size=12)
                )
            ),
            cells=(dict(
                values=[df[col] for col in df.columns],
                fill_color="lavender",
                align="left",
                font=dict(size=10)
            )
            ),
        )]
    )

    tbl.update_layout(
        title=f"Air Quality Measurement for: {location_name}",
        title_x=0.07,
        height=600,
        margin=dict(t=30, b=10),
    )

    return tbl


if __name__ == "__main__":
    pass
