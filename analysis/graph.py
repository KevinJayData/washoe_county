import matplotlib.pyplot as plt


def histograms(long_df):
    fig, axs = plt.subplots(3)
    fig.suptitle('Histogram showing the importance of deflating and normalizing this data')
    axs[0].hist(long_df.SAMT_value, bins=100)
    axs[1].hist(long_df.cpi_samt_value, bins=100)
    axs[2].hist(long_df.cpi_samt_value_log, bins=100)
    plt.savefig('analysis/plots/triple_eda.png')

def median_housing_price_per_year(long_df):
    long_df.rename(columns={'cpi_year': 'Year', 'cpi_samt_value_log': 'Logged Sale Price (2018 $s)'}, inplace=True)
    agg = long_df.groupby(long_df.Year)[['Logged Sale Price (2018 $s)']].median()
    plt.plot(agg)
    plt.title('Median House Price per Year - 2020 Update\nDifferences can be attributed to new data structure\nand Zoning changes.')
    plt.savefig('analysis/plots/median_housing_price_per_year.png')
