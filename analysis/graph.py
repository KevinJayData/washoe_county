import matplotlib.pyplot as plt
from IPython import embed


def histograms(long_df):

    fig, axs = plt.subplots(3)
    fig.suptitle('Histogram showing the importance of deflating and normalizing this data')
    axs[0].hist(long_df.SAMT_value, bins=100)
    axs[1].hist(long_df.cpi_samt_value, bins=100)
    axs[2].hist(long_df.cpi_samt_value_log, bins=100)
    plt.savefig('analysis/plots/triple_eda.png')

