import datetime
import plotly.graph_objects as go
import pysolar
import pandas as pd
import pytz
import os

lat, lon = 44.40315431075402, 8.944491973014737  # Piazza della Vittoria, 99
starting_year = 2022
Name = 'Piazza della Vittoria, 99'
years = 2
altitudes_deg, radiations = list(), list()
CWD = os.getcwd()


def time_variables(starting_year, years):
    start = datetime.datetime(starting_year, 1, 1, tzinfo=pytz.utc)

    hourly_periods = 8760 * years
    days = 365 * years
    nhr = 24 * days
    return start, hourly_periods, days, nhr


def annual_range(date_str, hourly_periods, days):
    start = pd.to_datetime(date_str) - pd.Timedelta(days)
    drange = pd.date_range(start, periods=hourly_periods, freq='H').round('min')  # rounding to exact minute
    drange = drange.strftime("%d.%m.%Y %H:%M:%S")  # changing representaion format
    return drange


def radiation_list(start, nhr, lat, lon):
    for ihr in range(nhr):
        date = start + datetime.timedelta(hours=ihr)

        altitude_deg = pysolar.solar.get_altitude(lat, lon, date)
        if altitude_deg <= 0:
            radiation = 0.
        else:
            radiation = pysolar.radiation.get_radiation_direct(date, altitude_deg)

        altitudes_deg.append(altitude_deg)
        radiations.append(radiation)
    return radiations, altitudes_deg


def plotting(date_list, radiations, Name, save_path):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_list, y=radiations,
                             mode='lines',
                             name='lines'))

    title = {'text': f"{Name} Solar Irradiance per m2",
             'y': 0.95,
             'x': 0.5,
             'xanchor': 'center',
             'yanchor': 'top'}

    fig.update_layout(
        template="seaborn",
        font_color="black",
        font_family="Times New Roman",
        legend_title_font_color="green",
        title=title

    )
    fig.update_xaxes(
        title_text="Time")  # ,

    fig.update_yaxes(
        title_text="Irradiance, W/m2"
    )

    fig.show()
    fig.write_html(save_path)


if __name__ == '__main__':
    start, hourly_periods, days, nhr = time_variables(starting_year, years)

    date_list = annual_range(start, hourly_periods, days)

    radiations, altitudes_deg = radiation_list(start, nhr, lat, lon)

    df = pd.DataFrame({"radiations": radiations, "altitudes_deg": altitudes_deg})

    df = df.set_index(date_list)

    df.to_csv(CWD + '/radiations_altitudes.csv')
    save_path_rad = CWD + "/radiations.html"
    save_path_alt = CWD + "/altitudes.html"
    plotting(date_list, radiations, Name, save_path=save_path_rad)
    plotting(date_list, altitudes_deg, Name, save_path=save_path_alt)
