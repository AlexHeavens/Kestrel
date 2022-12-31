import pandas as pd
from geopandas import gpd
from pyproj import CRS

import paths

data_dir = f"{paths.data_dir}"

local_gov_elections_2022 = pd.read_excel(
    f"{data_dir}/Local_Government_Elections_2022___Results_Updated_with_postals_station_split.xlsx",
    sheet_name="Results (City of Edinburgh)",
)

all_wards = gpd.read_file(f"{data_dir}/ward_boundaries/All_Scotland_wards_4th.shp")


def _get_all_wards_prj() -> str:
    with open(f"{data_dir}/ward_boundaries/All_Scotland_wards_4th.prj", "r") as f:
        prj_string = f.read().rstrip()
    return prj_string


all_wards_prj = _get_all_wards_prj()


def _get_ward_boundaries(
    all_wards_df: gpd.GeoDataFrame = all_wards, prj_string: str = all_wards_prj
) -> gpd.GeoDataFrame:

    wards_df = all_wards_df.copy()
    wards_df.crs = CRS.from_wkt(prj_string)
    wards_df = wards_df[wards_df.Council == "City of Edinburgh"][["Ward_No", "geometry"]]
    wards_df = wards_df.to_crs({"init": "epsg:4326"})  # folium expects lat / longs

    return wards_df


def _get_votes_by_ward(election_results: pd.DataFrame = local_gov_elections_2022) -> pd.DataFrame:

    df = election_results.copy()
    split_column_index = df.columns.get_loc("Total Ballot Papers Included In Count") + 1
    df_split_1 = df.iloc[:, :split_column_index]
    df_split_2 = df.iloc[:, split_column_index:]
    df_split_2 = df_split_2.fillna(0)
    df_split_2 = df_split_2.astype(int)
    df_split_1[["Ward_No", "Name"]] = df_split_1["Ward Number and Description"].str.extract(r"Ward (\d+) - (.*)")
    df_split_1["Ward_No"] = df_split_1["Ward_No"].astype("int64")
    df_split_1["Name"] = df_split_1["Name"].astype("str")

    df_split_1 = df_split_1.drop(columns=["Ward Number and Description"])
    df_split_1["votes"] = df_split_2.to_dict(orient="records")
    df = df_split_1

    return df


def get_all_data_by_ward() -> gpd.GeoDataFrame:

    ward_boundaries = _get_ward_boundaries()
    votes_by_ward = _get_votes_by_ward()

    combined_df = ward_boundaries.merge(votes_by_ward, on="Ward_No")

    return combined_df
