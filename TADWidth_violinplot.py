#!/usr/local/bin/python3.9

"""
Executable python script that will take in however many tad files and plot them
onto a violin plot to be compared or just one.
"""

import pandas
import seaborn as sns
import argparse
from math import log2
import statistics
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

'''
Function to parse the tad dataframe and obtain all of the tad widths 
to be plotted in a violin plot
'''


def get_tad_widths(tad_df):
    # list to contain log-transformed tad_widths
    plotting_tad_widths = []
    # iterate through the tad_df tads
    for index, row in tad_df.iterrows():
        # calculate the tad_width
        tad_width = tad_df['x2'][index] - tad_df['x1'][index]
        # log transform the tad_widths for better visualization
        # if they aren't 0 then add it to the tad_width list
        if tad_width != 0:
            plotting_tad_widths.append(log2(tad_width))
        # if it is 0 then add 1 to the tad width b/c cannot take log of 0
        else:
            plotting_tad_widths.append(log2(tad_width + 1))

    return plotting_tad_widths


def main():
    # Create the parser
    parser = argparse.ArgumentParser(usage="Python script to create a violin plot showing tad width distribution.")
    # Add an argument
    parser.add_argument('--tad', type=str, required=True, help="REQUIRED: Path to the tad file(s) in bedpe format "
                                                                "(https://bedtools.readthedocs.io/en/latest/content/general-usage.html) "
                                                                " with a header line. If more than one tad file is to be plotted, "
                                                                "enter in the tad_files separated by commas.")
    parser.add_argument('--labels', type=str, required=True, help="REQUIRED: string of x-axis labels for the violin plots. If"
                                                                  "more than one tad file is to be plotted, enter in the "
                                                                  "labels in comma-separated format.")
    parser.add_argument('--output', type=str, required=True, help="REQUIRED: Path for output violin plot. Only in matplotlib accepted picture format.")
    parser.add_argument('--figWidth', type=int, required=False, help="OPTIONAL: integer for output figure width. Default is 7.")
    parser.add_argument('--figHeight', type=int, required=False,
                        help="OPTIONAL: integer for output figure height. Default is 7.")

    # Parse the argument
    args = parser.parse_args()
    # split the files by commas
    files = args.tad.split(',')
    # split the labels by commas
    labels_split = args.labels.split(',')
    # create empty list to add the tad widths onto for that file
    combined_data_to_plot = []
    if len(files) != len(labels_split):
        raise argparse.ArgumentTypeError("Error. Number of tad files does not equal number of labels.")
    else:
        # iterate through all the tad files given
        for file in files:
            # read in the tad file into a pandas dataframe
            tad_df = pandas.read_csv(file,
                                  usecols=[0, 1, 2, 3, 4, 5],
                                  names=['chr1', 'x1', 'x2', 'chr2', 'y1', 'y2'],
                                  delimiter='\t')
            # get the log-transformed tad_widths of the tad file
            plotting_tad_widths = get_tad_widths(tad_df)
            # Print out the mean and median of the log2(width) for the specific file
            print(" Mean Log2(width) for ", file, "is: ", statistics.mean(plotting_tad_widths))
            print(" Median Log2(width) for ", file, "is: ", statistics.median(plotting_tad_widths))
            # append the list of tad_widths onto the combined_data_to_plot list for plotting
            combined_data_to_plot.append(plotting_tad_widths)
        sns.set()
        if args.figWidth is not None:
            if args.figHeight is not None:
                fig, axes = plt.subplots(figsize=(args.figWidth, args.figHeight))
            else:
                fig, axes = plt.subplots(figsize=(args.figWidth, 7))
        elif args.figHeight is not None:
            if args.figWidth is None:
                fig, axes = plt.subplots(figsize=(7, args.figHeight))
        else:
            fig, axes = plt.subplots(figsize=(7, 7))
        sns.set(style="whitegrid")
        # get list for axes
        axis_ticks = list(range(1, len(files) + 1))
        # set the x axis ticks
        axes.set_xticks(axis_ticks)
        axes.set_ylabel('log2(Tad Width)')
        ax = sns.violinplot(data=combined_data_to_plot, ax=axes, orient='v', inner='box')
        # set the x axis tick labels
        ax.set_xticklabels(labels_split)
        # Save figure
        fig.savefig(args.output)




if __name__ == "__main__":
    main()







