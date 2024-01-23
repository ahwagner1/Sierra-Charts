import pandas as pd
import matplotlib.pyplot as plt
cols = [" Volume", " BidVolume", " AskVolume"]
df = pd.read_csv("C:\\Users\\akbla\\OneDrive\\Desktop\\Python Projects\\VOC_Analysis\\ES_2_MIN_VOL.txt", usecols=cols)

b = 75

# TODO
# GET CLOSING VIX DATA TO MATCH THE SAME TIMES AS THE VOC TO MAKE 3D PLOT
# LOOK AT OVN RETURNS AND FOLLOWING DAY RETURN CORRELATIONS BASED ON VOC

#plt.hist(df[" Volume"], b, alpha=0.33, label='Total')
plt.hist(df[" BidVolume"], b, alpha=0.50, label='Bid')
plt.hist(df[" AskVolume"], b, alpha=0.5, label="Ask")
plt.legend(loc="upper right")
plt.show()

