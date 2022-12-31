import tempfile

import folium
import geopandas as gpd
import plotly.graph_objects as go

import crs


def _create_map(data: gpd.GeoDataFrame, visible_parties: dict) -> folium.Map:
    boundaries = data["geometry"].to_crs(crs.british_national_grid)  # recrsect to avoid pycrs centroid error complaints
    centroid = boundaries.centroid
    map_center = (centroid.x.mean(), centroid.y.mean())
    map_center = crs.bng_to_wgs.transform(*map_center)
    return folium.Map(location=map_center, zoom_start=12)


def _create_polygons(data: gpd.GeoDataFrame, visible_parties: dict, map_obj: folium.Map) -> None:
    for index, row in data.iterrows():
        polygon = row["geometry"]
        if polygon.geom_type == "MultiPolygon":
            polygons = [p for p in polygon.geoms]
        else:
            polygons = [polygon]
        for p in polygons:
            boundary = [point for point in zip(p.exterior.coords.xy[1], p.exterior.coords.xy[0])]
            party = max(row["votes"], key=row["votes"].get)
            color = visible_parties.get(party, "gray")
            displayed_polygon = folium.Polygon(boundary, color=color, fill=True, fill_color=color)
            displayed_polygon.add_to(map_obj)


def _create_pie_charts(data: gpd.GeoDataFrame, visible_parties: dict, map_obj: folium.Map) -> None:
    for index, row in data.iterrows():
        name = row["Name"]
        polygon = row["geometry"]
        total_votes = sum(row["votes"].values())
        data = []
        for party, votes in row["votes"].items():
            vote_share = 100 * votes / total_votes
            if vote_share > 0:
                data.append((party, vote_share))

        marker_colors = [visible_parties.get(label, "gray") for (label, _) in data]

        # Create a plotly pie chart
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=[x[0] for x in data],
                    values=[x[1] for x in data],
                    marker_colors=marker_colors,
                    title=name,
                )
            ]
        )
        # Set the text and autotext of the pie slices to be visible only on hover
        fig.data[0]["textinfo"] = "none"
        fig.data[0]["hoverinfo"] = "label+percent"

        icon_width = 300
        icon_height = icon_width
        icon_fig = go.Figure(
            data=[
                go.Pie(
                    labels=[x[0] for x in data],
                    values=[x[1] for x in data],
                    marker_colors=marker_colors,
                )
            ],
            layout={
                "width": icon_width,
                "height": icon_height,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "showlegend": False,
            },
        )

        # Set the text and autotext of the pie slices to be visible only on hover
        icon_fig.data[0]["textinfo"] = "none"
        icon_fig.data[0]["hoverinfo"] = "label+percent"

        # Create a temporary file to store the plotly figure
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            icon_fig.write_image(f, format="png")
            filename = f.name

        # Create a folium Marker object with the plotly figure embedded as an HTML element
        raw_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
        folium.Marker(
            location=(polygon.centroid.y, polygon.centroid.x),
            icon=folium.CustomIcon(filename, icon_size=(icon_width, icon_height)),
            popup=folium.Popup(folium.IFrame(html=raw_html, width=600, height=400)),
        ).add_to(map_obj)


def generate_interactive_map(ward_data):
    visible_parties = {
        "Scottish Labour Party": "red",
        "Scottish Conservative and Unionist Party": "blue",
        "Scottish Green Party": "green",
        "Scottish National Party": "yellow",
        "Scottish Liberal Democrats": "orange",
    }
    m = _create_map(ward_data, visible_parties)
    _create_polygons(ward_data, visible_parties, m)
    _create_pie_charts(ward_data, visible_parties, m)
    return m
