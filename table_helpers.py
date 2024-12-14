import pandas as pd
import plotly.graph_objects as go


def basic_table(data, location_name: str = "Oxford"):
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
