#!/usr/bin/env python3
# pyrotoolbox, a collection of tools to work with PyroScience GmbH data.
# Copyright (C) 2025, Christoph Staudinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
from pyrotoolbox.parsers import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import get_plotlyjs
from html import escape
import numpy as np
import os

ANALYTE_TO_AXES_LABEL = {
    "oxygen_hPa": "pO<sub>2</sub> [hPa]",
    "oxygen_torr": "pO<sub>2</sub> [torr]",
    "oxygen_%O2": "O<sub>2</sub> [%]",
    "oxygen_%airsat": "Air sat. [%]",
    "oxygen_µM": "DO [µM]",
    "oxygen_µg/L": "DO [µg/L]",
    "oxygen_mg/L": "DO [mg/L]",
    "oxygen_mL/L": "DO [mL/L]",
    "pH": "pH",
    "optical_temperature": "T [°C]",
}

HTML_HEADER1 = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Measurement Report for {}</title>
  """

HTML_HEADER2 = """\
  <style>
  :root {
    color-scheme: light;
    --bg: #ffffff;
    --fg: #1a1a1a;
    --muted: #6b7280;
    --border: #e2e2e2;
    --surface: #f7f7f8;
    --stripe: #f2f2f2;
    --hover: #eaf1ff;
    --accent: #2563eb;
  }

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    background: var(--bg);
    color: var(--fg);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.4;
  }

  main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 16px 24px 64px;
  }

  h1, h2 {
    font-weight: 600;
  }

  h2 {
    margin-top: 2.5em;
    padding-top: 0.6em;
    border-top: 1px solid var(--border);
  }

  .topnav {
    position: sticky;
    top: 0;
    z-index: 10;
    display: flex;
    align-items: baseline;
    gap: 24px;
    flex-wrap: wrap;
    padding: 10px 24px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
  }

  .topnav .title {
    font-weight: 600;
    white-space: nowrap;
  }

  .topnav nav {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  .topnav a {
    color: var(--muted);
    text-decoration: none;
    font-size: 0.9em;
  }

  .topnav a:hover {
    color: var(--accent);
  }

  .row {
    display: flex;
    margin-left: -5px;
    margin-right: -5px;
    flex-wrap: wrap;
  }

  .column {
    flex: 1 1 30%;
    padding: 5px;
    min-width: 320px;
  }

  .table-wrap {
    overflow-x: auto;
    max-width: 100%;
  }

  table {
    border-collapse: collapse;
    border-spacing: 0;
    width: auto;
    min-width: 40%;
    border: 1px solid var(--border);
    font-size: 12px;
  }

  th, td {
    text-align: left;
    padding: 6px 10px;
    white-space: nowrap;
  }

  thead th {
    background: var(--surface);
  }

  tr:nth-child(even) {
    background-color: var(--stripe);
  }

  tr:hover {
    background-color: var(--hover);
  }

  details.section {
    margin: 0.5em 0;
  }

  details.section > summary {
    cursor: pointer;
    font-weight: 600;
    padding: 4px 0;
  }
</style>
</head>
<body>
"""

HTML_FOOTER = """\
</body>
</html>
"""


def generate_plotlyjs_script() -> str:
    """Embed the plotly.js library exactly once, so multiple plots on the same report page

    don't each ship their own multi-megabyte copy while still keeping the report fully
    self-contained (viewable offline). Every ``fig.to_html()`` call in this module must be
    passed ``include_plotlyjs=False`` to avoid duplicating the library.
    """
    return f"<script>{get_plotlyjs()}</script>\n"


def generate_nav(title: str, sections: list) -> str:
    """Build the sticky top navigation bar shown on every report page.

    :param title: report title shown on the left of the bar
    :param sections: list of (anchor_id, label) tuples for the sections present on the page
    """
    links = "\n".join(f'    <a href="#{anchor}">{label}</a>' for anchor, label in sections)
    return f"""\
<header class="topnav">
  <div class="title">{escape(title)}</div>
  <nav>
{links}
  </nav>
</header>
"""


def generate_multi_channel_plots(df_list: list, m_list: list, plot_raw: bool = True):
    """Create a report to combine the results from multiple channels.

    Only really useful if the channels have a very similar x-range.

    :param df_list: list of dataframe with the input data
    :param m_list: list of metadata
    """
    # find the number of analyte units. -> go through all dfs and make a list
    # check if any status problems occurred. -> if so add status plot, else add statement that nothing bad happened
    analytes = []
    status_errors = False
    df_list_o2_pH = []
    m_list_o2_pH = []
    df_list_optT = []
    m_list_optT = []
    for df, m in zip(df_list, m_list):
        for a in (
            "oxygen_hPa",
            "oxygen_torr",
            "oxygen_%O2",
            "oxygen_%airsat",
            "oxygen_µM",
            "oxygen_µg/L",
            "oxygen_mg/L",
            "oxygen_mL/L",
            "pH",
        ):
            if a in [i[4:] for i in df.columns] or a in df.columns:
                df_list_o2_pH.append(df)
                m_list_o2_pH.append(m)
                analytes.append(a)
                break
            elif "optical_temperature" in [i[4:] for i in df.columns] or "optical_temperature" in df.columns:
                df_list_optT.append(df)
                m_list_optT.append(m)
                break
        if not status_errors and sum(df["status"]) > 0:
            status_errors = True

    used_analytes = sorted(set(analytes))

    analyte_rows = len(used_analytes)

    rows = analyte_rows + 1 + int(status_errors) + int(plot_raw)

    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.03)

    for analyte, df, m in zip(analytes, df_list_o2_pH, m_list_o2_pH):
        i = used_analytes.index(analyte)
        plot_analyte_to_subplot(
            df, analyte, fig, i + 1, 1, name=f'{m["device"]} ({m["uid"]}) Ch. {m.get("channel", 1)}', legendgroup=str(i)
        )

    for df, m in zip(df_list_optT, m_list_optT):
        plot_analyte_to_subplot(
            df,
            "optical_temperature",
            fig,
            analyte_rows + 1,
            1,
            name=f'{m["device"]} ({m["uid"]}) Ch. {m["channel"]} optT',
            legendgroup="T",
        )

    for df, m in zip(df_list, m_list):
        plot_temperature_to_subplot(
            df,
            fig,
            analyte_rows + 1,
            1,
            name=f'{m["device"]} ({m["uid"]}) Ch. {m.get("channel", 1)} Pt100',
            legendgroup="T",
        )
        if status_errors:
            plot_status_to_subplot(
                df,
                fig,
                analyte_rows + 2,
                1,
                name_prefix=f'{m["device"]} ({m["uid"]}) Ch. {m.get("channel", 1)} ',
                legendgroup="status",
            )
        if plot_raw:
            plot_raw_to_subplot(
                df,
                fig,
                analyte_rows + 2 + int(status_errors),
                1,
                name=f'{m["device"]} ({m["uid"]}) Ch. {m.get("channel", 1)} ',
                legendgroup="raw",
            )

    # comments are drawn once for the whole figure. A combined logfile repeats the same file-wide
    # comment on every channel, so de-duplicate to avoid stacking identical vertical lines.
    add_comments_to_plots(df_list, fig)

    align_legends_to_subplots(fig)

    fig.update_layout(
        height=300 * rows,
        xaxis_showticklabels=True,
        hovermode="x unified",
        hoversubplots="axis",
    )

    # add xticklabels back to every axes
    fig.update_layout(**{"xaxis{}_showticklabels".format(i): True for i in range(1, rows)})

    # Set x-axis title and add a shared spike line across all subplots
    fig.update_xaxes(title_text="", showspikes=True, spikemode="across", spikesnap="cursor", spikedash="dot")

    return remove_duplicate_xdata(fig.to_html(full_html=False, include_plotlyjs=False))


def make_comparison_report(df_list, m_list, buf=None):
    """Create a html report for the given dataframes and metadata.

    :param df_list: list of dataframes with the input data
    :param m_list: list of metadata
    :param buf: file or path
    """
    s = HTML_HEADER1.format("multiple channels")
    s += HTML_HEADER2
    s += generate_plotlyjs_script()
    s += generate_nav("Comparison report", [("summary", "Summary"), ("channels", "Channels"), ("plots", "Plots")])
    s += "<main>\n"

    s += f'<h1 id="summary">Summary of {len(df_list)} datasets</h1>\n'
    s += '<h2 id="channels">Channels</h2>\n'
    s += "<ul>\n"
    for m in m_list:
        s += f'<li>{m["device"]} ({m["uid"]}) Ch. {m.get("channel", 1)}: {m["experiment_description"]}</li>\n'
    s += "</ul>\n"

    s += '<h2 id="plots">Plots</h2>\n'

    s += generate_multi_channel_plots(df_list, m_list)

    s += "</main>\n"
    s += HTML_FOOTER

    if isinstance(buf, str):
        with open(buf, "w", encoding="utf8") as f:
            f.write(s)
    elif hasattr(buf, "write"):
        buf.write(s)
    else:
        return s


def make_report(df, m, buf=None):
    """Create a html report for the given dataframe and metadata.

    :param df: dataframe with the input data
    :param m: metadata
    :param buf: file or path
    """
    is_fireplate = m["device"].startswith("FirePlate")

    sections = [("summary", "Summary"), ("settings", "Settings &amp; Calibration")]
    if not is_fireplate:
        sections.append(("status", "Status"))
    sections.append(("plots", "Plots"))

    s = HTML_HEADER1.format(m["experiment_name"])
    s += HTML_HEADER2
    s += generate_plotlyjs_script()
    s += generate_nav(m["experiment_name"], sections)
    s += "<main>\n"

    s += '<h2 id="summary">Summary</h2>\n'
    s += generate_header(df, m) + "\n"

    s += '<h2 id="settings">Settings and Calibration</h2>\n'
    # collapsed by default for FirePlate reports: the per-well calibration table is huge
    s += f'<details class="section"{"" if is_fireplate else " open"}>\n'
    s += "<summary>Show settings and calibration</summary>\n"
    if is_fireplate:
        s += '<div class="table-wrap">' + pd.DataFrame(m["settings"], index=[0]).T.to_html(header=False) + "</div>\n"
        s += "<br>\n"
        s += '<div class="table-wrap">' + generate_calibration_table(m) + "</div>\n"
    else:
        s += "<div class=row>\n"
        s += "<div class=column>\n"
        s += '<div class="table-wrap">' + pd.DataFrame(m["settings"], index=[0]).T.to_html(header=False) + "</div>\n"
        s += "</div>\n"
        s += "<div class=column>\n"
        s += '<div class="table-wrap">' + generate_calibration_table(m) + "</div>\n"
        s += "</div>\n"
        s += "</div>\n"
    s += "</details>\n"

    if is_fireplate:
        s += generate_status_report_fireplate(df)
        s += '<h2 id="plots">Plots</h2>\n'
        heatmap_html, heatmap_start_time = generate_animated_heatmap_for_fireplate(df)
        trace_html, trace_n_rows = generate_trace_plot_for_fireplate(
            df, plot_status=np.count_nonzero(df.filter(regex="status"))
        )
        s += heatmap_html
        s += trace_html + "\n"
        s += generate_heatmap_time_indicator_script(
            heatmap_start_time, trace_n_rows, "fireplate-heatmap", "fireplate-trace"
        )
    else:
        s += generate_status_report(df)
        s += '<h2 id="plots">Plots</h2>\n'
        s += generate_plots(df, plot_status=np.count_nonzero(df.filter(regex="status"))) + "\n"

    s += "</main>\n"
    s += HTML_FOOTER
    if isinstance(buf, str):
        with open(buf, "w", encoding="utf8") as f:
            f.write(s)
    elif hasattr(buf, "write"):
        buf.write(s)
    else:
        return s


def generate_status_report(df: pd.DataFrame) -> str:
    """Create a short report on the status register during the measurement.

    returns a table with statistics on the encountered problems or a short message that everything was ok.

    :param df: measurement data
    :return: html string
    """
    bit_to_error_dict = {
        0: "Warning - automatic amplification reduction active",
        1: "Warning - sensor signal low",
        2: "Error - optical detector saturated",
        3: "Warning - reference signal low",
        4: "Error - reference signal too high",
        5: "Error - sample temperature sensor failed",
        7: "Warning - high humidity",
        8: "Error - case temperature sensor failed",
        9: "Error - pressure sensor failed",
        10: "Error - humidity sensor failed",
    }
    status = np.array(df["status"], dtype=int)
    counts = {}
    for bit in bit_to_error_dict.keys():
        counts[bit_to_error_dict[bit]] = np.count_nonzero(status & 1 << bit)
    counts = {k: v for k, v in counts.items() if v > 0}
    if len(counts):
        d = pd.DataFrame(counts, index=["Count"]).T
        s = '<h2 id="status">Status Report</h2>\n'
        return s + '<div class="table-wrap">' + d.to_html() + "</div>\n"
    else:
        return '<h2 id="status">Status Report</h2>\nNo errors and warnings in status.\n'


def generate_calibration_table(m: dict) -> str:
    if not isinstance(list(m["calibration"].values())[0], dict):  # Not a Fireplate file
        return pd.DataFrame(m["calibration"], index=[0]).T.to_html(header=False)
    else:
        d = pd.DataFrame(m["calibration"])
        d.columns.name = "Channels"
        return d.T.to_html(index_names=True)


def generate_header(df: pd.DataFrame, m: dict) -> str:
    """Generate a summary table over the measurement

    :param df: dataframe with measurement data
    :param m: metadata
    :return: html-table
    """
    duration = df.index[-1] - df.index[0]
    days = duration.days
    seconds = duration.seconds
    hours = seconds // 3600
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    d = {
        "Experiment Name": m["experiment_name"],
        "Description": m["experiment_description"],
        "Analyte": m["settings"]["analyte"],
        "Sensor Code": m.get("sensor_code", ""),
        "Group": m.get("group", np.nan),
        "Channels": ", ".join([str(i) for i in m["channels"]]) if "channels" in m else np.nan,
        "Device": m["device"],
        "Device Serial": m.get("device_serial", ""),
        "Device UID": m["uid"],
        "Software": m["software_version"],
        "Firmware": m["firmware"],
        "Experiment Start": df.index[0].strftime("%Y-%m-%d %H:%M"),
        "Experiment End": df.index[-1].strftime("%Y-%m-%d %H:%M"),
        "Experiment Duration": f"{days} days, {hours:0>2}:{minutes:0>2}:{seconds:0>2}",
        "Data Points": str(len(df)),
    }
    return '<div class="table-wrap">' + pd.DataFrame(d, index=[0]).T.dropna().to_html(header=False) + "</div>"


def plot_analyte_to_subplot(df: pd.DataFrame, unit, fig, row: int, col: int, name=None, legendgroup="1"):
    """Plot the analyte data to a subfigure.

    :param df: dataframe with data
    :param m: metadata
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    :param name: optional, force a name for the trace
    """
    if unit in (
        "oxygen_hPa",
        "oxygen_torr",
        "oxygen_%O2",
        "oxygen_%airsat",
        "oxygen_µM",
        "oxygen_µg/L",
        "oxygen_mg/L",
        "oxygen_mL/L",
    ):
        if not name:
            name = "oxygen"
        fig.add_trace(go.Scatter(x=df.index, y=df[unit], name=name, legendgroup=legendgroup), row=row, col=col)
        fig.update_yaxes(title_text=ANALYTE_TO_AXES_LABEL[unit], row=row, col=col)
    elif unit == "optical_temperature":
        if not name:
            name = "temperature (optical)"
        # fig = make_subplots()  # new plot without secondary y-axis
        fig.add_trace(
            go.Scatter(x=df.index, y=df["optical_temperature"], name=name, legendgroup=legendgroup), row=row, col=col
        )
        fig.update_yaxes(title_text="T [°C]", row=row, col=col)
    elif unit == "pH":
        if not name:
            name = "pH"
        fig.add_trace(go.Scatter(x=df.index, y=df["pH"], name=name, legendgroup=legendgroup), row=row, col=col)
        fig.update_yaxes(title_text="pH", row=row, col=col)
    else:
        print('Cannot plot the following analyte: f{m["settings"]["analyte"]}')


def plot_temperature_to_subplot(df: pd.DataFrame, fig, row: int, col: int, name=None, legendgroup="2"):
    """Plot the temperature data to a subfigure.

    :param df: dataframe with data
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    :param name: optional, force a name for the trace
    :param legendgroup: can be used to adjust legend groups
    """
    if "sample_temperature" not in df:
        return
    if not name:
        name = "T"
    fig.add_trace(
        go.Scatter(x=df.index, y=df["sample_temperature"], name=name, legendgroup=legendgroup), row=row, col=col
    )
    fig.update_yaxes(title_text="T [°C]", row=row, col=col)


def plot_status_to_subplot(df: pd.DataFrame, fig, row: int, col: int, name_prefix="", legendgroup="3"):
    """Plot the status data to a subfigure.

    :param df: dataframe with data
    :param m: metadata (is ignored here)
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    :param name_prefix: name prefix for legend
    :param legendgroup: can be used to adjust legend groups
    """
    status = np.array(df["status"], dtype=int)
    for bit, msg in [
        (0, "Warning - automatic amplification reduction active"),
        (1, "Warning - sensor signal low"),
        (2, "Error - optical detector saturated"),
        (3, "Warning - reference signal low"),
        (4, "Error - reference signal too high"),
        (5, "Error - sample temperature sensor failed"),
        (7, "Warning - high humidity"),
        (8, "Error - case temperature sensor failed"),
        (9, "Error - pressure sensor failed"),
        (10, "Error - humidity sensor failed"),
    ]:
        tmp = df["status"][(status & 1 << bit).astype(bool)]
        if len(tmp):
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=(status & 1 << bit).astype(bool).astype(int),
                    name=name_prefix + msg,
                    legendgroup=legendgroup,
                ),
                row=row,
                col=col,
            )

    fig.update_yaxes(title_text="Status", row=row, col=col)


def plot_raw_to_subplot(df: pd.DataFrame, fig, row: int, col: int, name=None, legendgroup="4"):
    """Plot the raw data (R or dphi) to a subfigure.

    :param df: dataframe with data
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    """
    if name is None:
        name = ""
    else:
        name += " "
    if "pH" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["R"], name=name + "R", legendgroup=legendgroup), row=row, col=col)
        fig.update_yaxes(title_text="R", row=row, col=col)
    else:
        fig.add_trace(
            go.Scatter(x=df.index, y=df["dphi"], name=name + "dphi", legendgroup=legendgroup), row=row, col=col
        )
        fig.update_yaxes(title_text="dPhi [°]", row=row, col=col)


def plot_signal_and_ambient_to_subplot(df: pd.DataFrame, fig, row: int, col: int):
    """Plot the signal and ambient light data to a subfigure.

    :param df: dataframe with data
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    """
    fig.add_trace(go.Scatter(x=df.index, y=df["signal_intensity"], name="signal", legendgroup="5"), row=row, col=col)
    fig.add_trace(
        go.Scatter(x=df.index, y=df["ambient_light"], name="ambient light", legendgroup="5"), row=row, col=col
    )
    fig.update_yaxes(title_text="Signal / Ambient [mV]", row=row, col=col)


def generate_plots(
    df: pd.DataFrame,
    plot_analyte: bool = True,
    plot_temperature: bool = True,
    plot_status: bool = True,
    plot_raw: bool = True,
    plot_signal_and_ambient: bool = True,
    plot_comments: bool = True,
) -> str:
    """Generate a plot with shared x-axes for the important data of a measurement.

    :param df: data
    :param plot_analyte: plot analyte data
    :param plot_temperature: plot temperature data
    :param plot_status: plot status
    :param plot_raw: plot raw data (dphi or R)
    :param plot_signal_and_ambient:  plot signal and ambient light
    :param plot_comments: show comments as vertical lines in plots
    :return: html-data of plot
    """
    analyte = None
    for a in (
        "oxygen_hPa",
        "oxygen_torr",
        "oxygen_%O2",
        "oxygen_%airsat",
        "oxygen_µM",
        "oxygen_µg/L",
        "oxygen_mg/L",
        "oxygen_mL/L",
        "pH",
        "optical_temperature",
    ):
        if a in [i[4:] for i in df.columns] or a in df.columns:
            analyte = a
            break

    # Only reserve a temperature row if there is actually Pt100 data to show there, or if the
    # analyte itself is optical temperature (which is drawn into that same row). Otherwise the
    # row stayed reserved but empty whenever a device has no "sample_temperature" column.
    show_temperature_row = (plot_temperature and "sample_temperature" in df.columns) or analyte == "optical_temperature"

    row = 1
    if plot_analyte and analyte:
        if analyte != "optical_temperature":  # only increment row if analyte is not temperature
            row += 1
    if show_temperature_row:
        temperature_row = row
        row += 1
    if plot_status:
        status_row = row
        row += 1
    if plot_raw:
        raw_row = row
        row += 1
    if plot_signal_and_ambient:
        signal_ambient_row = row
        row += 1

    fig = make_subplots(rows=row - 1, cols=1, shared_xaxes=True, vertical_spacing=0.03)

    if plot_analyte and analyte:
        plot_analyte_to_subplot(df, analyte, fig, 1, 1)
    if plot_temperature and show_temperature_row:
        plot_temperature_to_subplot(df, fig, temperature_row, 1)
    if plot_status:
        plot_status_to_subplot(df, fig, status_row, 1)
    if plot_raw:
        plot_raw_to_subplot(df, fig, raw_row, 1)
    if plot_signal_and_ambient:
        plot_signal_and_ambient_to_subplot(df, fig, signal_ambient_row, 1)
    if plot_comments:
        add_comments_to_plots(df, fig)

    align_legends_to_subplots(fig)

    fig.update_layout(
        height=300 * row,  # width=600
        xaxis_showticklabels=True,
        hovermode="x unified",
        hoversubplots="axis",
    )

    # add xticklabels back to every axes
    fig.update_layout(**{"xaxis{}_showticklabels".format(i): True for i in range(2, row)})

    # Set x-axis title and add a shared spike line across all subplots
    fig.update_xaxes(title_text="", showspikes=True, spikemode="across", spikesnap="cursor", spikedash="dot")

    return remove_duplicate_xdata(fig.to_html(full_html=False, include_plotlyjs=False))


def align_legends_to_subplots(fig, groupclick="toggleitem"):
    """Give each subplot row its own legend, anchored to the top of that row.

    Replaces the previous approach of nudging a single shared legend into place with
    ``legend_tracegroupgap`` (which had to be re-tuned whenever trace counts or subplot
    heights changed). Every trace is assigned to the legend matching its y-axis, and
    that legend is positioned at the top-right of the corresponding subplot's domain.

    :param fig: figure with subplots and traces already added
    :param groupclick: legend groupclick behaviour, forwarded to every per-row legend
    """
    legend_updates = {}
    for tr in fig.data:
        suffix = tr.yaxis[1:] if tr.yaxis else ""  # "y" -> "", "y2" -> "2", ...
        legend_name = f"legend{suffix}"
        tr.legend = legend_name
        if legend_name not in legend_updates:
            domain_top = fig.layout[f"yaxis{suffix}"].domain[1]
            legend_updates[legend_name] = dict(
                yref="paper",
                y=domain_top,
                yanchor="top",
                xref="paper",
                x=1.02,
                xanchor="left",
                groupclick=groupclick,
            )
    fig.update_layout(**legend_updates)


def add_comments_to_plots(df, fig):
    """Draw the comments of one or several dataframes as vertical lines in the figure.

    :param df: a single dataframe or a list of dataframes (e.g. the channels of a combined logfile). When
        a list is passed the same comment appearing on several channels is only drawn once (at its first
        occurrence), so file-wide comments do not stack into overlapping lines.
    :param fig: the plotly figure to annotate
    """
    df_list = df if isinstance(df, (list, tuple)) else [df]
    seen = set()
    for df in df_list:
        if "comment" not in df:
            continue
        for x, text in df["comment"].dropna().items():
            if text in seen:
                continue
            seen.add(text)
            fig.add_vline(
                x=x.to_pydatetime().timestamp() * 1000,
                line_dash="dot",
                row="all",
                annotation_text=text,
                annotation_position="top right",
            )


########################################################################################################################
# FirePlate functions
########################################################################################################################


def generate_status_report_fireplate(df: pd.DataFrame) -> str:
    """Create a short report on the status register during the measurement.

    returns a table with statistics on the encountered problems or a short message that everything was ok.

    :param df: measurement data
    :return: html string
    """
    return ""  # TODO
    bit_to_error_dict = {
        0: "Warning - automatic amplification reduction active",
        1: "Warning - sensor signal low",
        2: "Error - optical detector saturated",
        3: "Warning - reference signal low",
        4: "Error - reference signal too high",
        5: "Error - sample temperature sensor failed",
        7: "Warning - high humidity",
        8: "Error - case temperature sensor failed",
        9: "Error - pressure sensor failed",
        10: "Error - humidity sensor failed",
    }
    status = np.array(df["status"], dtype=int)
    counts = {}
    for bit in bit_to_error_dict.keys():
        counts[bit_to_error_dict[bit]] = np.count_nonzero(status & 1 << bit)
    counts = {k: v for k, v in counts.items() if v > 0}
    if len(counts):
        d = pd.DataFrame(counts, index=["Count"]).T
        s = "<h2>Status Report</h2>\n"
        return s + d.to_html() + "\n"
    else:
        return "<h2>Status Report</h2>\nNo errors and warnings in status.\n"


def generate_animated_heatmap_for_fireplate(df, unit=None, bins=100, div_id="fireplate-heatmap"):
    if unit is None:  # detect unit
        for a in (
            "oxygen_hPa",
            "oxygen_torr",
            "oxygen_%O2",
            "oxygen_%airsat",
            "oxygen_µM",
            "oxygen_µg/L",
            "oxygen_mg/L",
            "oxygen_mL/L",
            "pH",
            "optical_temperature",
        ):
            if a in [i[4:] for i in df.columns]:
                unit = a
                break
    # e.g. unit = 'oxygen_%O2
    df = df.copy()
    if len(df) > bins:
        df = df.resample((df.index[-1] - df.index[0]) / bins).mean().round(2)
    import plotly.express as px

    l = []
    for c in df.filter(regex=unit):
        d = df[[c]]
        d = d.dropna()
        d.columns = [unit]
        d["x"] = int(c[1:3]) - 1
        d["y"] = "ABCDEFGH".index(c[0])
        l.append(d)
    df2 = pd.concat(l).sort_index(kind="stable")
    df2["time [min]"] = (df2.index - df2.index[0]).total_seconds() / 60
    df2["time [min]"] = df2["time [min]"].round()
    # range_color must be set explicitly: without it, plotly only auto-ranges the colorbar to the
    # first animation frame's data, so the colorbar stops matching the marker colors once the
    # slider moves to a later frame.
    fig = px.scatter(
        df2,
        x="x",
        y="y",
        animation_frame="time [min]",
        color=unit,
        range_x=[-0.5, 11.5],
        range_y=[0, 8],
        range_color=[df2[unit].min(), df2[unit].max()],
    )
    fig.update_traces(marker=dict(size=30))
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        yaxis=dict(
            tickmode="array",
            tickvals=[0, 1, 2, 3, 4, 5, 6, 7],
            ticktext=["A", "B", "C", "D", "E", "F", "G", "H"],
            title="",
        ),
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
            title="",
        ),
        height=600,
        width=1200,
    )
    # df2.index[0] is the reference the "time [min]" animation frames are offset from; the
    # time indicator on the trace plot below needs the exact same reference to stay in sync,
    # so it's handed back to the caller alongside the html.
    return fig.to_html(full_html=False, auto_play=False, include_plotlyjs=False, div_id=div_id), df2.index[0]


def plot_status_to_subplot_fireplate(df: pd.DataFrame, fig, row: int, col: int):
    """Plot the status data to a subfigure.

    :param df: dataframe with data
    :param m: metadata (is ignored here)
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    """
    for c in df.filter(regex="status"):
        status = np.array(df[c].dropna(), dtype=int)
        for bit, msg in [
            (0, "Warning - automatic amplification reduction active"),
            (1, "Warning - sensor signal low"),
            (2, "Error - optical detector saturated"),
            (3, "Warning - reference signal low"),
            (4, "Error - reference signal too high"),
            (5, "Error - sample temperature sensor failed"),
            (7, "Warning - high humidity"),
            (8, "Error - case temperature sensor failed"),
            (9, "Error - pressure sensor failed"),
            (10, "Error - humidity sensor failed"),
        ]:
            tmp = df[c][(status & 1 << bit).astype(bool)]
            if len(tmp):
                fig.add_trace(
                    go.Scattergl(
                        x=df.index,
                        y=(status & 1 << bit).astype(bool).astype(int),
                        name=c[:3],
                        legendgroup=c[:3],
                        showlegend=False,
                    ),
                    row=row,
                    col=col,
                )

    fig.update_yaxes(title_text="Status", row=row, col=col)


def plot_temperature_to_subplot_fireplate(df: pd.DataFrame, fig, row: int, col: int):
    """Plot the temperature data to a subfigure.

    :param df: dataframe with data
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    """

    for c in df.filter(regex="sample_temperature|case_temperature"):
        d = df[c].dropna()
        fig.add_trace(
            go.Scattergl(x=d.index, y=d, name="T (case)", line=dict(color="red"), marker=dict(color="red")),
            row=row,
            col=col,
        )
    fig.update_yaxes(title_text="T [°C]", row=row, col=col)


def plot_raw_to_subplot_fireplate(df: pd.DataFrame, fig, row: int, col: int):
    """Plot the raw data (R or dphi) to a subfigure.

    :param df: dataframe with data
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    """
    for c in df.filter(regex="_pH$"):  # for fireplate
        d = df[c[:3] + "_R"].dropna()
        fig.add_trace(
            go.Scattergl(x=d.index, y=d, name=c[:3] + "_R", legendgroup=c[:3], showlegend=False), row=row, col=col
        )
    for c in df.filter(regex="_oxygen|_optical_temperature"):  # for fireplate
        d = df[c[:3] + "_dphi"].dropna()
        fig.add_trace(
            go.Scattergl(x=d.index, y=d, name=c[:3] + "_dphi", legendgroup=c[:3], showlegend=False), row=row, col=col
        )
    fig.update_yaxes(title_text="R / dPhi [°]", row=row, col=col)


def plot_to_subplot_fireplate(
    df: pd.DataFrame, fig, row: int, col: int, regex, ylabel, showlegend=False, legend_suffix="", color=None
):
    """Plot the signal and ambient light data to a subfigure.

    :param df: dataframe with data
    :param fig: figure to plot to
    :param row: row of subfigure
    :param col: col of subfigure
    """
    from itertools import cycle
    import plotly.io

    i = cycle(plotly.io.templates["plotly"].layout.colorway)
    coordinate_to_color = {k: next(i) for k in [f"{l}{n:0>2}" for l in "ABCDEFGH" for n in range(1, 13)]}
    for c in df.filter(regex=regex):
        d = df[c].dropna()
        if color is None:
            try:
                lcolor = coordinate_to_color[c[:3]]
            except KeyError:
                lcolor = color
        else:
            lcolor = color
        fig.add_trace(
            go.Scattergl(
                x=d.index,
                y=d,
                name=c[:3] + legend_suffix,
                legendgroup=c[:3],
                showlegend=showlegend,
                line=dict(color=lcolor),
                marker=dict(color=lcolor),
            ),
            row=row,
            col=col,
        )
    fig.update_yaxes(title_text=ylabel, row=row, col=col)


def generate_trace_plot_for_fireplate(
    df: pd.DataFrame,
    plot_analyte: bool = True,
    plot_temperature: bool = True,
    plot_status: bool = True,
    plot_raw: bool = True,
    plot_signal: bool = True,
    plot_ambient: bool = True,
    div_id="fireplate-trace",
):
    # df = df.reset_index()
    # df.index = [i.strftime('%Y-%m-%d %H:%M:%S') for i in df.index]
    analytes = []
    for a in (
        "oxygen_hPa",
        "oxygen_torr",
        "oxygen_%O2",
        "oxygen_%airsat",
        "oxygen_µM",
        "oxygen_µg/L",
        "oxygen_mg/L",
        "oxygen_mL/L",
        "pH",
        "optical_temperature",
    ):
        if a in [i[4:] for i in df.columns] or a in df.columns:
            analytes.append(a)

    row = 1
    if plot_analyte:
        for a in analytes:
            if a == "optical_temperature":  # only increment row if analyte is not temperature
                continue
            row += 1
    if plot_temperature or "optical_temperature" in analytes:  # reserve a row for temperature
        temperature_row = row
        row += 1
    if plot_status:
        status_row = row
        row += 1
    if plot_raw:
        raw_row = row
        row += 1
    if plot_signal:
        signal_row = row
        row += 1
    if plot_ambient:
        ambient_row = row
        row += 1

    fig = make_subplots(rows=row - 1, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    if plot_analyte:
        arow = 1
        for a in analytes:
            if a == "optical_temperature":
                plot_to_subplot_fireplate(
                    df,
                    fig,
                    temperature_row,
                    1,
                    a,
                    ANALYTE_TO_AXES_LABEL[a],
                    showlegend=True,
                    legend_suffix=" (opt. temp)",
                )
            else:
                plot_to_subplot_fireplate(
                    df, fig, arow, 1, a, ANALYTE_TO_AXES_LABEL[a], showlegend=True, legend_suffix=f" ({a[:6]})"
                )
                arow += 1
    if plot_temperature:
        plot_temperature_to_subplot_fireplate(df, fig, temperature_row, 1)
        # plot_to_subplot(df, fig, temperature_row, 1, 'case_temperature|sample_temperature', 'T [°C]', color='red', legend_name='temperature')
        # todo sample_temperature and fixed_temperature
    if plot_status:
        plot_status_to_subplot_fireplate(df, fig, status_row, 1)
    if plot_raw:
        plot_raw_to_subplot_fireplate(df, fig, raw_row, 1)
    if plot_signal:
        plot_to_subplot_fireplate(df, fig, signal_row, 1, "signal_intensity", "Signal [mV]")
    if plot_ambient:
        plot_to_subplot_fireplate(df, fig, ambient_row, 1, "ambient_light", "Ambient Light [mV]")

    fig.update_layout(
        height=300 * (row + 1),  # width=600
        xaxis_showticklabels=True,
        legend=dict(groupclick="togglegroup"),
    )

    # add xticklabels back to every axes
    fig.update_layout(**{"xaxis{}_showticklabels".format(i): True for i in range(2, row)})

    # Set x-axis title and add a shared spike line across all subplots. Not using
    # hovermode="x unified" here: with up to 96 overlapping wells per subplot, a unified
    # tooltip would list every visible well at once and become unreadable.
    fig.update_xaxes(title_text="", showspikes=True, spikemode="across", spikesnap="cursor", spikedash="dot")

    # number of subplot rows is handed back so the heatmap time indicator (see
    # generate_heatmap_time_indicator_script) knows how many per-row shapes to draw
    return remove_duplicate_xdata(fig.to_html(full_html=False, include_plotlyjs=False, div_id=div_id)), row - 1


def generate_heatmap_time_indicator_script(
    start_time: pd.Timestamp, n_rows: int, heatmap_div_id: str, trace_div_id: str
) -> str:
    """Build a script that draws a vertical line on the fireplate trace plot marking the
    time point currently shown by the animated heatmap above it.

    The heatmap animates over a "time [min]" frame variable while the trace plot below uses
    real timestamps, so the frame value has to be converted back to a timestamp using the same
    reference point the heatmap used to compute "time [min]" in the first place (``start_time``).
    The indicator is read-only: it follows the heatmap's slider/play state but does not itself
    control it.

    :param start_time: reference timestamp the heatmap's animation frames are offset from
    :param n_rows: number of stacked subplot rows in the trace plot, one shape is drawn per row
    :param heatmap_div_id: div id of the animated heatmap figure (its slider/frame events are observed)
    :param trace_div_id: div id of the trace plot figure (the indicator shapes are drawn here)
    """
    import calendar

    # calendar.timegm (unlike datetime.timestamp()) treats the given fields as UTC rather than
    # the local system timezone, so this preserves the naive wall-clock value verbatim instead
    # of shifting it by whatever timezone the report happens to be generated in.
    start_ms = calendar.timegm(start_time.timetuple()) * 1000 + start_time.microsecond // 1000
    return f"""\
<script>
(function() {{
  var heatmapDiv = document.getElementById({heatmap_div_id!r});
  var traceDiv = document.getElementById({trace_div_id!r});
  if (!heatmapDiv || !traceDiv) return;

  function pad(n, w) {{
    w = w || 2;
    n = String(n);
    while (n.length < w) n = "0" + n;
    return n;
  }}

  // Formats as "YYYY-MM-DD HH:MM:SS.mmm" using UTC getters, since the underlying timestamps
  // are timezone-naive wall-clock values and must not be shifted by the browser's local zone.
  function formatPlotlyDate(ms) {{
    var d = new Date(ms);
    return d.getUTCFullYear() + "-" + pad(d.getUTCMonth() + 1) + "-" + pad(d.getUTCDate()) + " " +
      pad(d.getUTCHours()) + ":" + pad(d.getUTCMinutes()) + ":" + pad(d.getUTCSeconds()) + "." + pad(d.getUTCMilliseconds(), 3);
  }}

  function updateIndicator(frameMinutes) {{
    var xVal = formatPlotlyDate({start_ms} + frameMinutes * 60000);
    var shapes = [];
    for (var i = 0; i < {n_rows}; i++) {{
      var suffix = i === 0 ? "" : String(i + 1);
      shapes.push({{
        type: "line",
        xref: "x" + suffix,
        yref: "y" + suffix + " domain",
        x0: xVal, x1: xVal, y0: 0, y1: 1,
        line: {{color: "#e6484a", width: 1.5}}
      }});
    }}
    Plotly.relayout(traceDiv, {{shapes: shapes}});
  }}

  function frameNameToMinutes(name) {{
    var v = parseFloat(name);
    return isNaN(v) ? null : v;
  }}

  heatmapDiv.on("plotly_sliderchange", function(e) {{
    if (!e || !e.step || !e.step.args) return;
    var mins = frameNameToMinutes(e.step.args[0][0]);
    if (mins !== null) updateIndicator(mins);
  }});

  heatmapDiv.on("plotly_animatingframe", function(e) {{
    if (!e || !e.frame) return;
    var mins = frameNameToMinutes(e.frame.name);
    if (mins !== null) updateIndicator(mins);
  }});

  updateIndicator(0);
}})();
</script>
"""


def remove_duplicate_xdata(s: str):
    """Remove duplicate x-data in plotly html exports.

    The plots contain very often duplicates of x-data. This can take up a huge amount of space and cost a lot of
    performance. This function removes these duplicates and replaces them with variables
    """
    import time

    start = time.time()
    xdatas = {}
    # go through string and search for definitions of x data
    while True:
        m = re.search(r',"x":(\[.*?])', s)
        if m is None:  # break if nothing (more) is found
            break
        xdata = m.groups()[0]  # get xdata
        # if len(xdata) < 50:  # do not replace very short xdata regions
        #    continue
        xname = f"xdata{len(xdatas)}"  # create variable name
        xdatas[xname] = xdata
        s = s.replace(xdata, xname)  # replace all occurrences with variable

    # insert variable definitions
    insert_string = ""
    for name, data in xdatas.items():
        insert_string += f"const {name}={data};\n"
    # NOTE: newer plotly versions (>=6.x) no longer emit the
    # type="text/javascript" attribute on <script> tags, so the previous
    # exact-string search below silently failed (rfind returned -1),
    # causing insert_point to become 30 and the xdata definitions to be
    # inserted into the middle of an unrelated <div style="..."> attribute.
    # This broke the resulting HTML/JS ("xdata0 is not defined").
    # Fix: search for the last <script ...> tag regardless of its
    # attributes.
    script_tags = list(re.finditer(r"<script[^>]*>", s))
    insert_point = script_tags[-1].end() if script_tags else len(s)
    s = s[:insert_point] + insert_string + s[insert_point:]
    return s


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("logfiles", nargs="+", help="input logfiles")
    parser.add_argument(
        "--start_time",
        help="ignore data before this time. Input has to be parsed by pandas.Timestamp. e.g. (2025-02-13 12:05:00)",
    )
    parser.add_argument(
        "--end_time",
        help="ignore data after this time. Input has to be parsed by pandas.Timestamp. e.g. (2025-02-13 14:05:00)",
    )
    parser.add_argument("--skipfirst", help="ignore the first X datapoints", type=int, default=0)
    parser.add_argument("--skiplast", help="ignore the last X datapoints", type=int, default=0)
    parser.add_argument("--onlysummary", help="create only summary.html", action="store_true")
    # parser.add_argument('-o', '--output_file', help='output file. default: "input + _report.html"')
    args = parser.parse_args()
    # if args.output_file:
    #    output_file = args.output_file
    # else:
    #    output_file = 'report.html'
    # print(args)

    df_list = []
    m_list = []
    for path in args.logfiles:
        if "StatusLegend.txt" in path or "TempPT100Port.txt" in path:
            print(f'Skipping file "{path}"')
            continue
        print(f'Processing: "{path}"')
        result = parse(path)
        # a combined logfile parses into a dict of {channel_id: (df, m)}; a regular file into (df, m)
        if isinstance(result, dict):
            channels = [(f" ({cid})", df, m) for cid, (df, m) in result.items()]
        else:
            channels = [("", result[0], result[1])]

        for suffix, df, m in channels:
            if "settings" not in m:  # PT100 / temperature compensation channel - no report
                continue
            df = df.iloc[args.skipfirst : len(df) - args.skiplast]
            if args.start_time:
                df = df[args.start_time :]
            if args.end_time:
                df = df[: args.end_time]
            if len(df) == 0:
                print(f'No data to process. aborting "{path}"{suffix}')
                continue
            df_list.append(df)
            m_list.append(m)

            if args.onlysummary:
                continue

            report_name = os.path.split(path)[-1][:-4] + suffix + "_report.html"
            try:
                with open(report_name, "w", encoding="utf8") as f:
                    make_report(df, m, f)
            except PermissionError:  # workaround for windows "open with"
                with open(path[:-4] + suffix + "_report.html", "w", encoding="utf8") as f:
                    make_report(df, m, f)

    if len(df_list) > 1:
        print(f"Processing summary")
        try:
            with open("summary.html", "w", encoding="utf8") as f:
                make_comparison_report(df_list, m_list, f)
        except (
            PermissionError
        ):  # workaround for windows "open with". In case the cwd is not writeable use lowest common directory
            with open(os.path.join(os.path.commonprefix(args.logfiles), "summary.html"), "w", encoding="utf8") as f:
                make_comparison_report(df_list, m_list, f)


if __name__ == "__main__":
    main()
