#!/usr/local/bin/python3.9


import pandas
import matplotlib.pyplot as plt
import argparse

'''
Function to parse the user-defined bins to get them into numeric values 
and the labels for the piechart
'''


def parse_bins(bin_string):
    # split the string by commas to get different bins
    split_bins = bin_string.split(",")
    # add "under" to the first bin.
    user_labels = ["under " + split_bins[0]]
    # iterate through the rest of the split bins except for the first one
    for x in range(1, len(split_bins)):
        # add them to the labels list
        user_labels.append(split_bins[x])
    # convert to basepairs for Mb and Kb
    bin_string = bin_string.replace("Mb", "000000")
    bin_string = bin_string.replace("mb", "000000")
    bin_string = bin_string.replace("Kb", "000")
    bin_string = bin_string.replace("kb", "000")
    # list that contains the different numeric bins
    numeric_bins = bin_string.split(',')
    # return the labels and the bins reformatted as numbers
    return user_labels, numeric_bins


def get_user_bin_widths(tad_df, numeric_bins):
    # empty list to contain all counts that will be returned at the end
    all_counts = []
    # empty list to contain the counts for the middle bins
    middle_counts = []

    # iterate through all the numeric bins except the first and last
    for bin_pair in range(1, len(numeric_bins) - 1):
        # set the count to be 0, will set back to 0 for each bin
        count = 0
        # split the bin by a - to get the left and right hand side
        split_bins = numeric_bins[bin_pair].split("-")
        # iterate through each tad in the df
        for index, row in tad_df.iterrows():
            # calculate the tad_width
            tad_width = tad_df['x2'][index] - tad_df['x1'][index]
            # print(tad_width)
            # if the tad is in the range of the left and right hand bin add it to the count
            if int(split_bins[0]) < tad_width <= int(split_bins[1]):
                count += 1
        # append the final count of tads in that bin to the middle count list
        middle_counts.append(count)
    # now iterate through the tads again and check and see which correspond to the first bin and last bin
    # initiate counts for first and last bins to 0
    first_counts = 0
    last_counts = 0
    # iterate through the tads and add 1 to the corresponding count
    for index, row in tad_df.iterrows():
        tad_width = tad_df['x2'][index] - tad_df['x1'][index]
        # the number will be everything
        if tad_width <= int(numeric_bins[0]):
            first_counts += 1
        # the number will be everything but the last character in the string (a + symbol)
        if tad_width > int(numeric_bins[len(numeric_bins) - 1][:-1]):
            last_counts += 1

    # add the first counts to the final count list
    all_counts.append(first_counts)
    # iterate through the middle counts and add each count
    for count in middle_counts:
        all_counts.append(count)
    # add the last count
    all_counts.append(last_counts)

    return all_counts


'''
Function to get the tad widths using the user-defined resolution 
that is either 10000, 25000, 50000, or 100000.
Will return a list of width counts and corresponding labels for the pie chart
'''


def get_standardized_bin_widths(tad_df, res):
    # 100kb
    if res == 100000:
        labels = ['under 1Mb', '1Mb-4Mb', '4Mb-8Mb', '8Mb+']
        count_under_1Mb = 0
        count_1Mb_4Mb = 0
        count_4Mb_8Mb = 0
        count_8Mb = 0
        for index, row in tad_df.iterrows():
            tad_width = tad_df['x2'][index] - tad_df['x1'][index]
            if 1000000 < tad_width <= 4000000:
                count_1Mb_4Mb += 1
            elif 4000000 < tad_width <= 8000000:
                count_4Mb_8Mb += 1
            elif 8000000 < tad_width:
                count_8Mb += 1
            else:
                count_under_1Mb += 1

        # Put the counts of each tad width bin into a list to plot in a pie chart
        width_counts = [count_under_1Mb, count_1Mb_4Mb, count_4Mb_8Mb, count_8Mb]

    # 50kb
    elif res == 50000:
        labels = ['under 500kb', '500kb-1Mb', '1Mb-2Mb', '2Mb+']
        count_under_500kb = 0
        count_500kb_1Mb = 0
        count_1Mb_2Mb = 0
        count_2Mb = 0

        for index, row in tad_df.iterrows():
            tad_width = tad_df['x2'][index] - tad_df['x1'][index]
            if 500000 < tad_width <= 1000000:
                count_500kb_1Mb += 1
            elif 1000000 < tad_width <= 2000000:
                count_1Mb_2Mb += 1
            elif 2000000 < tad_width:
                count_2Mb += 1
            else:
                count_under_500kb += 1
        width_counts = [count_under_500kb, count_500kb_1Mb, count_1Mb_2Mb, count_2Mb]

    # 25 kb
    elif res == 25000:
        labels = ['under 250kb', '250kb-500kb', '500kb-1Mb', '1Mb-2Mb', '2Mb+']
        count_under_250kb = 0
        count_250kb_500kb = 0
        count_500kb_1Mb = 0
        count_1Mb_2Mb = 0
        count_2Mb = 0

        for index, row in tad_df.iterrows():
            tad_width = tad_df['x2'][index] - tad_df['x1'][index]
            if 250000 < tad_width <= 500000:
                count_250kb_500kb += 1
            elif 500000 < tad_width <= 1000000:
                count_500kb_1Mb += 1
            elif 1000000 < tad_width <= 2000000:
                count_1Mb_2Mb += 1
            elif 2000000 < tad_width:
                count_2Mb += 1
            else:
                count_under_250kb += 1
        width_counts = [count_under_250kb, count_250kb_500kb, count_500kb_1Mb, count_1Mb_2Mb, count_2Mb]

    # 10kb
    elif res == 10000:
        labels = ['under 100kb', '100kb-250kb', '250kb-500kb', '500kb-1Mb', '1Mb+']
        count_under_100kb = 0
        count_100kb_250kb = 0
        count_250kb_500kb = 0
        count_500kb_1Mb = 0
        count_1Mb = 0

        for index, row in tad_df.iterrows():
            tad_width = tad_df['x2'][index] - tad_df['x1'][index]
            if 100000 < tad_width <= 250000:
                count_100kb_250kb += 1
            elif 250000 < tad_width <= 500000:
                count_250kb_500kb += 1
            elif 500000 < tad_width <= 1000000:
                count_500kb_1Mb += 1
            elif 1000000 < tad_width:
                count_1Mb += 1
            else:
                count_under_100kb += 1
        width_counts = [count_under_100kb, count_100kb_250kb, count_250kb_500kb, count_500kb_1Mb, count_1Mb]

    else:
        print("Functionality only for 100kb, 50kb, 25kb, and 10kb resolution so far.")

    return labels, width_counts


def main():
    # Create the parser
    parser = argparse.ArgumentParser(usage="Python script to create a piechart showing tad width distribution.")
    # Add an argument
    parser.add_argument('--tad', type=str, required=True, help="REQUIRED: Path to the TAD file in juicer format "
                                                                "(https://github.com/aidenlab/juicer/wiki/Arrowhead) "
                                                                " without a header line.")
    parser.add_argument('--res', type=int, required=False, help="Optional: resolution of tad file in basepair format, "
                                                                "acceptable values are 10000, 25000, 50000, or 100000. Either "
                                                                "resolution or labels argument must be provided.")
    parser.add_argument('--bins', type=str, required=False, help="Optional: bins for separating the tad widths into,"
                                                                 "for example: '1Mb,1Mb-4Mb,4Mb-8Mb,8Mb+'. The first bin"
                                                                 " MUST have a '<' symbol in front, and the last bin must "
                                                                 "include a '+' at the end. Ranges must be separated by '-'."
                                                                 "Lengths may be in basepair format (10000) or Kb/Mb format"
                                                                 "(10Kb).")
    parser.add_argument('--output', type=str, required=True,
                        help="REQUIRED: Path for output piechart. Only in matplotlib accepted picture format.' ")
    # Parse the argument
    args = parser.parse_args()
    # Check if they included either of the resolution or bins arguments
    if args.res is None and args.bins is None:
        raise argparse.ArgumentTypeError("Error. Must include either resolution or user-specified bins.")
    # Check if they had the resolution and they inputted the correct value
    elif args.res is not None and args.res not in [10000, 25000, 50000, 100000]:
        raise argparse.ArgumentTypeError("Error. Resolution must be 10000, 25000, 50000, or 100000. "
                                         "If not, use --bins argument for user-specified bins.")
    else:
        # read in the tad file into a pandas dataframe
        tad_df = pandas.read_csv(args.tad,
                                  usecols=[0, 1, 2, 3, 4, 5],
                                  names=['chr1', 'x1', 'x2', 'chr2', 'y1', 'y2'],
                                  delimiter='\t')
        # if the resolution argument is not None
        if args.res is not None:
            # use the standardized width function to get the labels and width counts
            labels, width_counts = get_standardized_bin_widths(tad_df, args.res)
        # else if the resolution argument is None, the bins argument will not be so we will use that
        elif args.bins is not None:
            # parse bins to get the labels and numeric bins
            labels, numeric_bins = parse_bins(args.bins)
            # calculate the width_counts
            width_counts = get_user_bin_widths(tad_df, numeric_bins)
        # print(labels, width_counts)
        # now we can plot using the width_counts and labels
        ### Plot
        plt.pie(width_counts, autopct='%1.1f%%',
                shadow=False, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.legend(labels)
        plt.savefig(args.output)


if __name__ == "__main__":
    main()
