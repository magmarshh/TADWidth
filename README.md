# TADWidth
Calculating and visualizing TAD widths from juicer file. 
*Adapted from https://github.com/magmarshh/LoopWidth*

## TADWidth_piechart
Creates a piechart in any matplotlib-accepted format of loop width distributions.

### Requirements
pandas
matplotlib
python >= 3.7

### Usage 
```{bash echo=FALSE}
python TADWidth_piechart.py --tad <juicer TAD file> --bins <user-defined bin widths>  --res <TAD resolution> --output <path to output piechart>
```
### Parameters
- --tad: **REQUIRED** TAD file in juicer format (see [juicer arrowhead documentation](https://github.com/aidenlab/juicer/wiki/Arrowhead) for more information), *WITHOUT* a header row. 
-  --bins: **OPTIONAL** string of comma-separated user-defined resolution bins for TAD widths to be binned into. Will also be used as the labels for the piechart. The ranges must start with one coordinate (ex. 1Mb) followed by a range (ex. 1Mb-4Mb), ending with one coordinate (4Mb+) with a '+' symbol at the end of the last coordinate. The coordinates may be in basepair format or Kb/Mb format. The first coordinate will be interpreted as "less than or equal to", and the last coordinate will be interpreted as "greater than". 
-  --res: **OPTIONAL** integer input of TAD file resolution. Must be 10000, 25000, 50000, or 100000. Pre-defined bins according to the resolution will be used, if different bins are preferred use the `--bins` argument. 
-  --output: **REQUIRED** file path to outputted piechart in any matplot lib accepted format (see [matplotlib picture formats](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html) for more info)

**NOTE: Either `--bins` or `--res` argument MUST be supplied, if both are supplied then the res argument will take precedence.**

### Example: 
```{bash echo=FALSE}
python TADWidth_piechart.py  --loop Examples/test_file1.bedpe --res 10000 --output Examples/piechart_test1.png
```


## TADWidth_violinplot

### Requirements
- pandas
- matplotlib
- python >=  3.7 
- seaborn
- statistics


### Usage
```{bash echo=FALSE}
python TADWidth_violinplot.py --tad <juicer file(s)> --labels <plot label(s)> --figWidth <figure width> --figHeight <figure height> --output <path to violinplot output>

```
### Parameters
- --tad: **REQUIRED** TAD file(s) in juicer format (see [juicer arrowhead documentation](https://github.com/aidenlab/juicer/wiki/Arrowhead) for more information), WITHOUT a header row. If multiple TAD files are to be plotted on the same plot, enter TAD file paths separated by commas. 
- --labels: **REQUIRED** labels for violin plot(s) corresponding to the order given in the `tad` parameter. If multiple, separate with commas. 
- --output: **REQUIRED** file path to outputted violin plot in any matplot lib accepted format (see [matplotlib picture formats](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html) for more info)
- --figWidth: **OPTIONAL** figure width in integer format. Default is 7. 
- --figHeight: **OPTIONAL** figure height in integer format. Default is 7. 


### Example:
```{bash echo=FALSE}
python TADWidth_piechart.py --tad Examples/test_file1.bedpe --labels test1 --output Examples/violin_plot_test1.png
```
Output: 
 Mean Log2(width) for  Examples/test_file1.bedpe is:  17.43684815150383
 Median Log2(width) for  Examples/test_file1.bedpe is:  17.28771237954945
