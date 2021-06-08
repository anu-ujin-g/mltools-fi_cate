class SHAP_FI():

    def __init__(self, seed_num = None, time = True, trace = False, max_display = 999):
        '''
        Instantiates the SHAP_FI class.
        @param seed_num : Random seed for reproducibility.
        @param time: Set time functionality for runtime.
        @param trace : Turn on/off trace messages for debugging.
        @param max_display : Set max display of features.
        @return ICE data (dataframe) with N observations.
        @examples
        SHAP_FI(420, time = True, trace = False, max_display = 10)
        '''
        self.seed_num = seed_num
        self.trace = trace
        self.time = time
        self.max_display = max_display

        self.shapley = []

    def fit(self, X, model):
        '''
        Uses Shapley values to explain any machine learning model.
        @param X : Covariate matrix
        @param model : Model to interpet
        '''
        start = datetime.now()
        shap_values = shap.Explainer(model).shap_values(X)
        end = datetime.now()

        if self.time:
            print(f"Fit in {(end - start).total_seconds():.2f} seconds")

        self.shapley.append(shap_values)

        return

    def plot(self, save_path = None):
        '''
        Plot the SHAP values in a chart. Save to save_path
        '''

        fig = shap.summary_plot(self.shapley[0][1], X, plot_type = "bar", max_display = self.max_display)


        '''
        if save_path is not None:
            fig.savefig(save_path,
                        bbox_inches = 'tight',
                        pad_inches = 1)
        '''


    def fi_table(self, X):
        '''
        Return shapley value table
        '''

        features, vals = X.columns, np.abs(self.shapley[0][1]).mean(0)

        fi_df = pd.DataFrame(list(zip(features, vals)), columns=['Feature','Shapley Value']).\
               sort_values('Shapley Value', ascending = False).\
                head(self.max_display).\
                reset_index().\
                drop(['index'], axis=1)


        return fi_df
    