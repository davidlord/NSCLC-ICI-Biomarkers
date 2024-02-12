#!/usr/bin/env python3


import itertools
import random
from textwrap import wrap
from typing import Any, Dict, List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
import sklearn
from matplotlib import colors as mcolors
from matplotlib.ticker import MaxNLocator
from sklearn.manifold import TSNE

# Constants.
PLT_COLORS_BASE = list(dict(mcolors.BASE_COLORS).keys())
PLT_COLORS_CSS4 = list(dict(mcolors.CSS4_COLORS).keys())
PLT_TABLEU_COLORS = list(dict(mcolors.TABLEAU_COLORS).keys())


def scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    category_column: Optional[str] = None,
    plotargs: Dict[str, Any] = {},
) -> None:
    """Generates a scatter plot over two variables.

    Arguments:
        df -- a data frame containing the values to plot
        x_column -- the name of the column used for the x values
        y_column -- the name of the column used for the y values

    Keyword Arguments:
        category_column -- The name of a column containing categories
            for the plot color of each data point. (default: {None})
        plotargs -- Any additional arguments for the scatter plot.

    Returns:
        The resulting plot as a seaborn facet grid.
    """
    fig = plt.figure(facecolor="w", edgecolor="k")
    ax = fig.add_subplot(1, 1, 1)

    color_cycler = color_cycler_plt()
    for group in df[category_column].unique():
        ix = np.where(df[category_column] == group)
        ax.scatter(
            df.iloc[ix][x_column].to_numpy(),
            df.iloc[ix][y_column].to_numpy(),
            c=next(color_cycler),
            label=f"{category_column}_{group}",
            s=100,
            **plotargs
        )
    ax.set_xlabel(x_column, fontsize=14)
    ax.set_ylabel(y_column, fontsize=14)
    ax.legend()


def confusion_matrix(
    predicted_labels: np.ndarray,
    ground_truth_labels: np.ndarray,
    class_labels: Optional[List[str]] = None,
    normalize: bool = False,
    x_label: str = "Prediction",
    y_label: str = "Ground Truth",
    ax: Optional[plt.Axes] = None,
    imshow_kwargs: Dict[str, Any] = {},
):
    """Creates a confusion matrix given a ground truth values and prediction values.

    Arguments:
        predicted_labels -- The predicted values from the model.
        ground_truth_labels -- The ground truth values.

    Keyword Arguments:
        class_labels -- The names of the labels (default: {None})
        normalize -- If the presented values should be ratios. (default: {False})
        x_label -- The x-axis plot label. (default: {"Prediction"})
        y_label -- The y-axis plot label. (default: {"Ground Truth"})
        ax -- A matplotlib axis to plot on. (default: {None})
        imshow_kwargs -- Any additional arguments to configure the plot. (default: {{}})
    """
    if ax is None:
        fig = plt.figure(facecolor="w", edgecolor="k")
        fig.tight_layout()
        ax = fig.add_subplot(1, 1, 1)

    n_classes = predicted_labels.shape[0]
    confusion_matrix = sklearn.metrics.confusion_matrix(
        ground_truth_labels,
        predicted_labels,
        labels=[i for i in range(n_classes)],
    )
    _confusion_matrix(
        ax, confusion_matrix, class_labels, normalize, x_label, y_label, imshow_kwargs
    )


def _confusion_matrix(
    ax: plt.Axes,
    confusion_matrix: np.ndarray,  # array, shape = [n_classes, n_classes]
    class_labels: Optional[List[str]] = None,
    normalize: bool = False,
    x_label: str = "Prediction",
    y_label: str = "Ground Truth",
    imshow_kwargs: Dict[str, Any] = {},
) -> None:
    """Function to plot the supplied confusion matrix.

    Other things to note:
        - Depending on the number of category and the data, you may have to modify
            the figsize, font sizes etc. to make the plot look good.
        - Currently, some of the ticks dont line up due to rotations.

    Arguments:
        ax -- A matplotlib axis to plot on.
        confusion_matrix -- The confusion matrix array with the shape [n_classes, n_classes]

    Keyword Arguments:
        class_labels -- The names of the labels (default: {None})
        normalize -- If the presented values should be ratios. (default: {False})
        x_label -- The x-axis plot label. (default: {"Prediction"})
        y_label -- The y-axis plot label. (default: {"Ground Truth"})
        imshow_kwargs -- Any additional arguments to configure the plot. (default: {{}})
    """
    if normalize:
        confusion_matrix = (
            confusion_matrix.astype("float")
            * 10
            / confusion_matrix.sum(axis=1)[:, np.newaxis]
        )
        confusion_matrix = np.nan_to_num(confusion_matrix, copy=True)
        confusion_matrix = confusion_matrix.astype("int")

    ax.imshow(confusion_matrix, cmap="Oranges", **imshow_kwargs)

    # Parse effective labels.
    if class_labels is None:
        n_classes = confusion_matrix.shape[0]
        class_labels = [str(i) for i in range(n_classes)]
    class_labels = ["\n".join(wrap(l, 11)) for l in class_labels]

    tick_marks = np.arange(len(class_labels))

    ax.set_xlabel(x_label, fontsize=14)
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(class_labels, rotation=-90, ha="center")
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.tick_bottom()
    ax.set_xlim(min(tick_marks) - 0.5, max(tick_marks) + 0.5)

    ax.set_ylabel(y_label, fontsize=14)
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(class_labels, va="center")
    ax.yaxis.set_label_position("left")
    ax.yaxis.tick_left()
    ax.set_ylim(max(tick_marks) + 0.5, min(tick_marks) - 0.5)

    for i, j in itertools.product(
        range(confusion_matrix.shape[0]), range(confusion_matrix.shape[1])
    ):
        ax.text(
            j,
            i,
            format(confusion_matrix[i, j], "d") if confusion_matrix[i, j] != 0 else ".",
            horizontalalignment="center",
            verticalalignment="center",
            color="black",
        )


def histogram(
    data: pd.Series,
    type: str,
    plotargs: Dict,
) -> None:
    """Create a histogram plot.

    Arguments:
        data -- The data to use for the histogram.
        type -- The type of histogram plot. [categorical, continuous]
        plotargs -- Any additional arguments for the histogram plot.
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    if type == "categorical":
        _histogram_categorical(ax, data.value_counts(), data.unique(), **plotargs)
    elif type == "continuous":
        _histogram(ax, data.to_numpy(), **plotargs)


def _histogram_categorical(
    ax: plt.Axes,
    counts: np.ndarray,
    labels: List[str],
    title: str = "",
    xtick_label_rotation: float = 90,
    xtick_label_font_size=None,
    tight_fit=False,
    bar_kwargs: Dict[str, Any] = {},
):
    """Plot a histogram for categorical data.

    Arguments:
        ax -- The matplotlib axis to draw on.
        counts -- The number of values in each category.
        labels -- Labels for each category.

    Keyword Arguments:
        title -- The plot title. (default: {""})
        xtick_label_rotation -- The rotation of the x-tick labels. (default: {90})
        xtick_label_font_size -- The font size of the x-tick labels. (default: {None})
        tight_fit -- If the x-labels should fit tight to the plot. (default: {False})
        bar_kwargs -- Extra arguments for configuring the plot. (default: {{}})
    """
    TIGHT_WIDTH = 1
    assert len(counts) == len(labels)
    xticks = [x for x in range(len(counts))]
    ax.bar(xticks, counts, width=TIGHT_WIDTH if tight_fit else 0.8, **bar_kwargs)
    ax.set_xticks(xticks)
    ax.set_xticklabels(
        labels,
        rotation=xtick_label_rotation,
        rotation_mode="anchor",
        ha="right",
        fontsize=xtick_label_font_size,
    )
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title(title)

    if tight_fit:
        ax.set_xlim(xticks[0] - TIGHT_WIDTH / 2, xticks[-1] + TIGHT_WIDTH / 2)


def _histogram(
    ax: plt.Axes,
    data: np.ndarray,
    bins: Optional[np.ndarray] = None,
    bin_width: Optional[float] = None,
    title: str = "",
    hist_kwargs: Dict[Any, Any] = {},
):
    """Plot a histogram for the given values (continuous).

    Arguments:
        ax -- The matplotlib axis to draw on.
        data -- The data to fill the histogram with.

    Keyword Arguments:
        bins -- The number of bins. (default: {None})
        bin_width -- The width of the bin. (default: {None})
        title -- The plot title. (default: {""})
        hist_kwargs -- Extra arguments for configuring the plot. (default: {{}})
    """
    if bins is None and bin_width is not None:
        bins = get_bins(data, bin_width)

    ax.hist(data, bins=bins, **hist_kwargs)
    ax.set_title(title)


def scatter_tsne_2d(
    data: pd.DataFrame,
    columns: List[str],
    groupby: str,
    scatter_kwargs: Dict[str, Any] = {},
) -> None:
    """Wrapper function for the scatter 2D TSNE plot. Scatter the 2D
        TSNE decomoposition of a dataset.

    NOTE: TSNE can only be used with numerical data.

    Arguments:
        data -- The input data.
        columns -- Which columns to use in the TSNE decomposition.
        groupby -- How to group the data (a.k.a. the colors of the data points).
        scatter_kwargs -- Any additional arguments for the histogram plot.
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    groups = []
    labels = []
    for g in data[groupby].unique():
        ix = np.where(data[groupby] == g)
        groups.append(data.iloc[ix][columns].to_numpy())
        labels.append(f"{groupby}_{g}")

    _scatter_tsne_2d(ax, groups, labels, **scatter_kwargs)


# NOTE: scikit-learn recommends using PCA to reduce the number of dimensions to
# less than 50 if it is higher than that before transforming with TSNE.
def _scatter_tsne_2d(
    ax: plt.Axes,
    data: List[np.ndarray],
    labels: Optional[List[str]] = None,
    keep_ratio: float = 1.0,
    scatter_kwargs: Dict[str, Any] = {},
):
    """Scatter the 2D TSNE decomoposition of a dataset.

    NOTE: scikit-learn recommends using PCA to reduce the number of dimensions to
        less than 50 if it is higher than that before transforming with TSNE.

    Arguments:
        ax -- the matplotlib axis to draw on
        data -- list of arrays of values represents the features of samples of one category
            and has shape shape=[n_samples, n_features]. n_samples may vary between categories.

    Keyword Arguments:
        labels -- the labels for the legende (default: {None})
        keep_ratio -- keep keep_ratio of the data for plotting. TSNE transform is unaffected. (default: {1.0})
        scatter_kwargs -- extra arguments for configuring the plot (default: {{}})
    """
    # Data downsampling (1/2) - Calculate downsampling indices.
    downsampling_indices = []
    if keep_ratio < 1.0:
        for i, category_data in enumerate(data):
            n_new_samples = int(keep_ratio * len(category_data))
            downsampling_indices.append(
                np.random.permutation(len(category_data))[:n_new_samples].astype(int)
            )

    # Concatenate all data for compability with TSNE fit_transform().
    x_all = np.concatenate(tuple(data), axis=0)

    # Calculate TSNE transform.
    tsne = TSNE(n_components=2)
    x_transformed = tsne.fit_transform(x_all)

    # Data downsampling (2/2) - Apply downsampling.
    if downsampling_indices:
        for i in range(1, len(downsampling_indices)):
            downsampling_indices[i] += len(downsampling_indices[i - 1])
        downsampling_indices = np.concatenate(tuple(downsampling_indices), axis=0)
        x_transformed = x_all[downsampling_indices]

    # Create dummy labels if none.
    n_labels = len(data)
    labels = [str(i + 1) for i in range(n_labels)] if labels is None else labels

    # Scatter the TSNE transofrmed data.
    color_cycler = color_cycler_plt()
    prev_idx = 0
    scatter_handles = []
    for i in range(n_labels):
        this_n_samples = data[i].shape[0]
        x = x_transformed[prev_idx : prev_idx + this_n_samples, :]
        prev_idx += this_n_samples
        color = next(color_cycler)
        scatter_handle = ax.scatter(x[:, 0], x[:, 1], c=color, **scatter_kwargs)
        scatter_handles.append(scatter_handle)

    ax.legend(labels=labels, handles=scatter_handles)


# Plot utils below
##########################################################


def get_bins(data: np.ndarray, bin_width: float):
    """Generate bin edges for a histogram with specified width for target data.

    Arguments:
        data -- Data to be plotted in a histogram.
        bin_width -- Target bin width of histogram bins.

    Returns:
        bins -- List of bin edges, including right edge of rightmost bin.
    """
    lower = min(data)
    upper = max(data)
    n_bins = int(np.ceil((upper - lower) / bin_width))
    eps = (n_bins * bin_width - (upper - lower)) / 2
    bins = [lower - eps + i * bin_width for i in range(n_bins + 1)]
    return bins


def color_cycler_plt(colormap="tableu", order=None, n_colors=None):
    """Returns an iterator for matplotlib colors.

    Keyword Arguments:
        colormap -- Name of colormap to use. (default: {"tableu"})
        order -- Order used for selectings colors
            If order is a string ('random'), the number of colors can be specified with n_colors.
            If order is a list, the number of colors is taken to be the length of the list.
            (default: {None})
        n_colors -- Number of colors used when order is set to 'random'. (default: {None})

    Returns:
        plt_color_cycler -- Iterator for matplotlib colors.
    """

    if colormap == "base":
        plt_colors = PLT_COLORS_BASE
    elif colormap == "css4":
        plt_colors = PLT_COLORS_CSS4
    elif colormap == "tableu":
        plt_colors = PLT_TABLEU_COLORS
    else:
        print("plt_color_cycler: Please specify a valid colormap. Using base for now.")
        plt_colors = PLT_COLORS_BASE

    if order is not None:
        if order == "random":
            order = list(range(len(plt_colors)))
            random.shuffle(order)
            if n_colors is not None:
                order = [order[i] for i in range(n_colors)]  # Shrink the list

        assert isinstance(order, list)
        plt_colors = [plt_colors[i] for i in order]

    plt_color_cycler = itertools.cycle(plt_colors)

    return plt_color_cycler

