# The test result contains several statistics:

Test Statistic: This is the calculated test statistic value of the Dickey-Fuller test. It is a negative number and represents how much the test statistic is below the critical values. In your case, the test statistic is -1.496905.

p-value: This is the probability of getting a test statistic as extreme as the one calculated, assuming the null hypothesis is true. In this case, the null hypothesis is that the time series is non-stationary. If the p-value is less than a chosen significance level (e.g., 0.05), we reject the null hypothesis and conclude that the time series is stationary. In your case, the p-value is 0.535042, which is greater than 0.05, so we cannot reject the null hypothesis that the time series is non-stationary.

#Lags Used: This is the number of lags used in the Dickey-Fuller test. In your case, the number of lags used is 5.

Number of Observations Used: This is the number of observations used in the Dickey-Fuller test. In your case, the number of observations used is 8.

Critical Values: These are the critical values for the test statistic at the 1%, 5%, and 10% significance levels. If the test statistic is less than the critical value, we reject the null hypothesis that the time series is non-stationary. In your case, the critical value at the 1% significance level is -4.665186, at the 5% significance level is -3.367187, and at the 10% significance level is -2.802961.

Overall, based on the Dickey-Fuller test, the time series is likely non-stationary as the p-value is greater than 0.05.


The null hypothesis of the Dickey-Fuller test is that the time series is non-stationary (i.e., it has a unit root), while the alternative hypothesis is that the time series is stationary. The test statistic is computed and compared to a critical value from a table. If the test statistic is less than the critical value, we reject the null hypothesis and conclude that the time series is stationary.

