'''This module contains functions to help with visualization of ShotLink data.

Fuctions:
    plot_strokes_gained_scatter
    plot_heatmaps
'''
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.use('Agg')


def plot_strokes_gained_scatter(df, x_var, by_cat=True):
    '''Creates a scatter plot of StrokesGained vs chosen variable.
    Ensure that '%matplotlib inline' is used in jupyter notebook for plots
    to show automatically.

    Arguments:
        df (str): input dataframe
        x_var (str): variable to plot against
        by_cat (bool): whether or not to plot by shot category, default = True

    Returns:
        Scatter plot
    '''
    if by_cat is True:
        sns.lmplot(x=x_var, y='StrokesGainedBaseline', col='StrokesGainedCategory', data=df,
                   fit_reg=False, col_order=['Off the Tee', 'Approach to the Green',
                                             'Around the Green', 'Putting'],
                   col_wrap=2, scatter_kws={'alpha': 0.35})
    else:
        sns.lmplot(x=x_var, y='StrokesGainedBaseline', data=df, fit_reg=False,
                   col_wrap=2, scatter_kws={'alpha': 0.35})

def plot_heatmaps(main_df):
    '''Creates a series of heatmaps, showing the correlation between weather columns
    and Strokes Gained. Ensure that '%matplotlib inline' is used in jupyter notebook
    for plots to show automatically.

    Arguments:
        main_df (str): input dataframe

    Returns:
        Four heatmap plots, one for each Strokes Gained category.
    '''
    heatmap_df = main_df[['StrokesGainedBaseline', 'StrokesGainedCategory',
                          'DegreesFahrenheit', 'Humidity', 'Visibility', 'WindSpeed',
                          'PrecipitationIntensity']]
    categories = ['Off the Tee', 'Approach to the Green', 'Around the Green', 'Putting']

    for cat in categories:
        plt.subplots(figsize=(6, 5))
        sns.heatmap(heatmap_df[heatmap_df['StrokesGainedCategory'] == cat].corr(),
                    cmap='BrBG', annot=True)
        plt.title(cat)
