"""Bokeh visualisation of selected functions, mappings, and deviations."""

from collections.abc import Iterable
from pathlib import Path

import pandas as pd
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, Div, HoverTool
from bokeh.plotting import figure, save
from bokeh.resources import CDN

from .exceptions import VisualizationError
from .models import MappedPoint, MappingReport, SelectionResult, TestPoint


class BokehVisualizer:
    """Create a readable, interactive HTML visualisation for one completed run."""

    _colours = ("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728")

    def __init__(self, output_path: Path) -> None:
        """Create a visualiser for one generated HTML path.

        Parameters
        ----------
        output_path:
            HTML target beneath the ignored output directory.
        """
        self.output_path = output_path

    def create(
        self,
        training_data: pd.DataFrame,
        ideal_functions: pd.DataFrame,
        selections: Iterable[SelectionResult],
        mapping_report: MappingReport,
    ) -> Path:
        """Generate the four comparison panels and a deviation-oriented view.

        Returns
        -------
        Path
            Written Bokeh HTML file.

        Raises
        ------
        VisualizationError
            If Bokeh or the output filesystem cannot create the visualisation.
        """
        selected = tuple(selections)
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            panels = [
                self._comparison_panel(
                    training_data,
                    ideal_functions,
                    selection,
                    mapping_report.assignments,
                    mapping_report.unassigned_points,
                    colour,
                )
                for selection, colour in zip(selected, self._colours, strict=True)
            ]
            layout = column(
                gridplot(panels, ncols=2),
                self._deviation_panel(selected, mapping_report.assignments),
                Div(
                    text=(
                        "<p><strong>Unassigned test points:</strong> "
                        f"{mapping_report.unassigned_count}</p>"
                    )
                ),
            )
            save(
                layout,
                filename=str(self.output_path),
                title="DLMDSPWP01 Ideal Function Assignment",
                resources=CDN,
            )
        except (OSError, ValueError, RuntimeError) as error:
            raise VisualizationError(
                f"Could not create Bokeh visualisation: {self.output_path}"
            ) from error
        return self.output_path

    def _comparison_panel(
        self,
        training_data: pd.DataFrame,
        ideal_functions: pd.DataFrame,
        selection: SelectionResult,
        assignments: tuple[MappedPoint, ...],
        unassigned_points: tuple[TestPoint, ...],
        colour: str,
    ):
        """Build one independently scaled training/ideal/mapping comparison panel."""
        training = training_data.loc[:, ["x", selection.training_series]].sort_values("x")
        ideal_column = f"y{selection.ideal_function}"
        ideal = ideal_functions.loc[:, ["x", ideal_column]].sort_values("x")
        panel_assignments = tuple(
            mapping
            for mapping in assignments
            if mapping.ideal_function == selection.ideal_function
        )
        point_source = ColumnDataSource(
            {
                "x": [point.x for point in panel_assignments],
                "y": [point.y for point in panel_assignments],
                "delta_y": [point.delta_y for point in panel_assignments],
                "ideal_function": [point.ideal_function for point in panel_assignments],
                "threshold": [selection.threshold for _ in panel_assignments],
            }
        )
        plot = figure(
            title=(
                f"{selection.training_series} and selected y{selection.ideal_function} "
                f"(threshold {selection.threshold:.6g})"
            ),
            x_axis_label="x",
            y_axis_label="y",
            width=520,
            height=340,
            tools="pan,wheel_zoom,box_zoom,reset,save",
        )
        plot.line(
            training["x"].tolist(),
            training[selection.training_series].tolist(),
            color="#222222",
            line_width=2,
            legend_label=f"training {selection.training_series}",
        )
        plot.line(
            ideal["x"].tolist(),
            ideal[ideal_column].tolist(),
            color=colour,
            line_width=2,
            line_dash="dashed",
            legend_label=f"ideal {ideal_column}",
        )
        mapped_renderer = plot.scatter(
            "x",
            "y",
            source=point_source,
            color=colour,
            marker="circle",
            size=7,
            alpha=0.85,
            legend_label="mapped test point",
        )
        unassigned_source = ColumnDataSource(
            {
                "x": [point.x for point in unassigned_points],
                "y": [point.y for point in unassigned_points],
                "source_row": [point.source_row for point in unassigned_points],
            }
        )
        unassigned_renderer = plot.scatter(
            "x",
            "y",
            source=unassigned_source,
            color="#6b7280",
            marker="x",
            size=7,
            alpha=0.75,
            legend_label="unassigned test point",
        )
        plot.add_tools(
            HoverTool(
                renderers=[mapped_renderer],
                tooltips=[
                    ("x", "@x"),
                    ("test y", "@y"),
                    ("absolute delta_y", "@delta_y"),
                    ("ideal function", "@ideal_function"),
                    ("threshold", "@threshold"),
                ],
            )
        )
        plot.add_tools(
            HoverTool(
                renderers=[unassigned_renderer],
                tooltips=[("x", "@x"), ("test y", "@y"), ("source row", "@source_row")],
            )
        )
        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"
        return plot

    def _deviation_panel(
        self, selections: tuple[SelectionResult, ...], assignments: tuple[MappedPoint, ...]
    ):
        """Build a separate view of absolute deviations and their thresholds."""
        plot = figure(
            title="Assigned test-point deviations and selection thresholds",
            x_axis_label="x",
            y_axis_label="absolute delta_y",
            width=1060,
            height=320,
            tools="pan,wheel_zoom,box_zoom,reset,save",
        )
        all_x_values = [point.x for point in assignments]
        for selection, colour in zip(selections, self._colours, strict=True):
            selected_points = [
                point for point in assignments if point.ideal_function == selection.ideal_function
            ]
            source = ColumnDataSource(
                {
                    "x": [point.x for point in selected_points],
                    "delta_y": [point.delta_y for point in selected_points],
                    "ideal_function": [point.ideal_function for point in selected_points],
                    "threshold": [selection.threshold for _ in selected_points],
                }
            )
            renderer = plot.scatter(
                "x",
                "delta_y",
                source=source,
                color=colour,
                size=7,
                alpha=0.85,
                legend_label=f"y{selection.ideal_function} deviations",
            )
            plot.add_tools(
                HoverTool(
                    renderers=[renderer],
                    tooltips=[
                        ("x", "@x"),
                        ("absolute delta_y", "@delta_y"),
                        ("ideal function", "@ideal_function"),
                        ("threshold", "@threshold"),
                    ],
                )
            )
            if all_x_values:
                plot.line(
                    [min(all_x_values), max(all_x_values)],
                    [selection.threshold, selection.threshold],
                    color=colour,
                    line_dash="dotted",
                    line_alpha=0.8,
                    legend_label=f"y{selection.ideal_function} threshold",
                )
        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"
        return plot
