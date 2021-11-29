import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 'date', parse_dates = True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize = (15, 6))
    plt.plot(df.index, df['value'], 'r')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df1 = df.copy()
    df1['year'] = pd.DatetimeIndex(df1.index).year
    df1['month'] = pd.DatetimeIndex(df1.index).month

    # Copy and modify data for monthly bar plot
    df_bar = df1.groupby(['year', 'month'])['value'].mean().reset_index()
    
    # Dictionary of months for mapping
    months = {
      1: 'January',
      2: 'February',
      3: 'March',
      4: 'April',
      5: 'May',
      6: 'June',
      7: 'July',
      8: 'August',
      9: 'September',
      10: 'October',
      11: 'November',
      12: 'December',
    }
    df_bar['month'] = df_bar['month'].map(months)

    # Draw bar plot
    fig = plt.figure(figsize = (10, 10))
    sns.barplot(x = 'year', y = 'value', data = df_bar, hue = 'month', hue_order = months.values(), palette = 'bright')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(loc = 'upper left', title = 'Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Box plot ticks and labels
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ticks = range(0, 220000, 20000)

    # Draw box plots (using Seaborn)
    fig = plt.figure(figsize = (12, 6))
    fig.add_subplot(121)
    sns.boxplot(x = 'year', y = 'value', data = df_box)
    plt.xlabel('Year')
    plt.ylabel('Page Views')
    plt.ylim(top = 200000)
    plt.yticks(ticks)
    plt.title('Year-wise Box Plot (Trend)')
    
    fig.add_subplot(122)
    sns.boxplot(x = 'month', y = 'value', data = df_box, order = labels)
    plt.xlabel('Month')
    plt.ylabel('Page Views')
    plt.ylim(top = 200000)
    plt.yticks(ticks)
    plt.title('Month-wise Box Plot (Seasonality)')
    plt.tight_layout()
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig