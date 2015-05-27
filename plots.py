import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Plots(object):
    def __init__(self, 
             X,
             style= 'fivethirtyeight', 
             dashboard_scaled=False, 
             grey = '0.6', 
             rwidth=0.95,
             *args,
             **kargs):
        '''
            Doc String HERE!!!
        '''
        self.X_=X
        self.style=style
        self.dashboard_scaled=dashboard_scaled
        self.grey=grey
        self.rwidth=rwidth

        print 'init plot class!'
        print 'style', self.style
        print 'dashboard scaled', self.dashboard_scaled
        print 'rwidth', self.rwidth
        print 'grey', self.grey
        print plt.style.available

    def cat_plot(self, color='0.6'):
        '''
            df_plot(self)
        '''
        import matplotlib.pyplot as plt
        import seaborn as sns

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height),
                    ha='center', va='bottom')
        sns.set_palette("deep", desat=.6)
        sns.set(style="white", context="talk")
        didnt_plot = []
        plotted = []
        w = 0.5 # width of bar
        i = 0
        for coln in self.X_.columns:
            if not self.X_[coln].empty and self.X_[coln].dtype == object:
                i += 1
                plt.figure(i)
                sns.set_context(rc={"figure.figsize": (8, 6)})  
                vals = pd.value_counts(self.X_[coln]).values 
                print 'vals', vals
                ind = np.arange(len(vals))  
                rect  = plt.bar(ind + w/len(vals), vals, width=w, color=color)
                plt.xticks(ind+w,(self.X_[coln].unique()))
                autolabel(rect)
                plt.title(coln)
                plotted.append(coln)
            elif not self.X_[coln].empty and self.X_[coln].dtype != object:
                didnt_plot.append(coln)
        print "Plot categorical data from:"
        print plotted   
        print "Couldn't plot categorical data from:"
        print didnt_plot
        return plt

    def df_plot(self):
        '''
            df_plot(self)
        '''
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.set_palette("deep", desat=.6)
        sns.set(style="white", context="talk")
        count = 0
        didnt_plot = []
        plotted = []
        for coln in self.X_.columns:
            if not self.X_[coln].empty and self.X_[coln].dtype != 'object' and \
                self.X_[coln].dtype != 'datetime64':
                count += 1 
                plotted.append(coln)
            elif not self.X_[coln].empty:
                didnt_plot.append(coln)
        sns.set_context(rc={"figure.figsize": (8, count*2)})     
        self.X_.hist(layout = (count, 1), bins = 100) 
        print "Plotted numerical data from:"
        print plotted
        print "Couldn't plot numerical data from:"
        print didnt_plot
        return plt

    def dt_plot(self, interval = 'week', color = '0.6'):
        import matplotlib.pyplot as plt
        import seaborn as sns
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height),
                    ha='center', va='bottom')

        def plot_that(groupby, coln, color, interval):
            print 'inside plot_that'
            print 'groupby', groupby
            plt.figure(1)
            sns.set_palette("deep", desat=.6)
            sns.set(style="white", context="talk")
            sns.set_context(rc={"figure.figsize": (8, 6)})  
            w = 0.5 # width of bar
            vals = groupby.values 
            print 'vals', vals
            ind = np.arange(len(vals))  
            rect  = plt.bar(ind + w/len(vals), vals, width=w, color=color)
            plt.xticks(ind + w/2., (groupby.index))
            plt.xlim(groupby.index.min(),np.ceil(groupby.index.max()))
            autolabel(rect)
            plt.title('%s by %s' %(coln, interval))
            print "Plot datetime data from:"
            print coln 
            plt.show()    

        for coln in self.X_.columns:
            print 'looking at coln', coln
            if self.X_[coln].dtype == 'datetime64[ns]':
                print 'datetime column'
                if interval == 'day':
                    print 'interval day'
                    plot_that(self.X_.groupby(self.X_[coln].dt.day)[coln].count(),\
                             coln, color, interval)
                elif interval == 'week':
                    print 'interval week'
                    plot_that(self.X_.groupby(self.X_[coln].dt.week)[coln].count(),\
                             coln, color, interval)
                else:
                    print 'interval month'
                    plot_that(self.X_.groupby(self.X_[coln].dt.month)[coln].count(),\
                             coln, color, interval)
        return plt

    def series_plot(self, series_name, histtype = 'bar', normed=False, color = '0.6', bins=None):
        '''
            series_plot(self, series_name, histtype = 'bar', normed=False, color = '0.6', bins=None)
        '''
        import matplotlib.pyplot as plt
        import seaborn as sns
        from scipy import stats
        import numpy as np

        plt.subplot(1, 1, 1)
        sns.set_context(rc={"figure.figsize": (8, 4)})
        sns.set_palette("deep", desat=.6)
        sns.set(style="white", context="talk")
        serie = self.X_[series_name]
        serie_scl = int(np.sqrt(np.sqrt(serie.max()-serie.min()))/2.)
        if bins==None:
            bin_size = serie_scl; min_edge = serie.min(); max_edge = serie.max()
            N = (max_edge-min_edge)/bin_size
            bin_list = np.linspace(min_edge, max_edge, N+1)
        else:
            bin_list=bins           
        plt.hist(x=serie, bins=bin_list, histtype=histtype, normed=normed,\
                 label=series_name, color=color)
        if normed:
            plt.ylabel("Percentage %s%s%s" %("'",series_name,"'"))
            plt.ylim(-0.001)
        else:
            plt.ylabel("Count %s%s%s" %("'",series_name,"'"))
            plt.ylim(-serie_scl*100)
        plt.xlim(serie.min(),np.ceil(serie.max()))
        plt.xlabel("%s%s%s values" %("'",series_name,"'"))         
        sns.despine()
        plt.title(series_name)
        return plt

    def joining_plot(self, x_name, y_name, kind='scatter', stat_func=None, color='0.6'):
        '''
            joining_plot(self, x_name, y_name, kind='scatter', stat_func=None, color='0.6')
        '''
        import matplotlib.pyplot as plt
        import seaborn as sns
        plt.subplot(1, 1, 1)
        sns.set_context(rc={"figure.figsize": (8, 4)})
        sns.set(style="ticks")
        sns.set_palette("deep", desat=.6)
        sns.jointplot(x_name, y_name, data=self.X_, kind=kind, stat_func=stat_func, color=color)
        sns.despine()
        # plt.title("%s joined to %s"%(x_name,y_name))
        return plt

    def show(self):
        '''
            Show function for plotting wrapper functions.
        '''
        self.plt.show()




