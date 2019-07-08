from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def plot_barplot(file):
    """
        Generate bar plot, can be used for both daily and weekly
        if the table has the same columns ['date', 'borrows', 'returns']
    :param file: path to CSV file
    :return: pop up figure
    """
    sns.set()
    daily_df = pd.read_csv(file)
    daily_df = pd.melt(daily_df, id_vars='date', var_name='type', value_name='count')

    with sns.color_palette('husl'):
        fig, ax = plt.subplots(1)
        sns.barplot(x='date', y='count', hue='type', data=daily_df, ax=ax)
    plt.show()

plot_barplot('weekly.csv')