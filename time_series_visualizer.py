import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from calendar import month_name
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])
df = df.set_index('date')

# Clean data
df = df.loc[(df['value'] > df['value'].quantile(0.025))]
df = df.loc[(df['value'] < df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    df_line = df.copy()
    fig, ax = plt.subplots()
    ax.plot(df)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    months = month_name[1:]
    df_bar['months'] = pd.Categorical(df_bar.index.strftime('%B'), categories=months, ordered=True)
    df_bar['Years'] = pd.Categorical(df_bar.index.strftime('%Y'), ordered=True)
    df_bar = pd.DataFrame(df_bar.groupby(['Years', 'months'])['value'].mean()).rename(columns={'value':'Average Page Views'}).reset_index()
    

    # Draw bar plot
    fig2 = plt.figure(figsize=(14, 6))
    fig = sns.catplot(
            x = "Years", 
            y = "Average Page Views", 
            hue="months", 
            data=df_bar,
            kind="bar",
            palette=sns.color_palette("tab10")
            )


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months = [month[0:3] for month in month_name]
    df_box['month'] = pd.Categorical(df_box.date.dt.strftime('%b'), categories=months, ordered=True)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    g = sns.boxplot(
        x="year",
        y="value",
        data=df_box,
        ax=ax1,
        palette=sns.color_palette("tab10")
        )
    g.set(xlabel='Year', ylabel='Page Views')

    g = sns.boxplot(
        x="month",
        y="value",
        data=df_box,
        ax=ax2,
        palette=sns.color_palette("tab10")
        )
    g.set(xlabel='Month', ylabel='Page Views')





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig