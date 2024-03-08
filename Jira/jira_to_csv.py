import pandas

df = pandas.read_csv("Amtran.csv")
df_out = df[['Priority','Issue key','Status','Assignee','Created','Custom field (VendorCR)']]
df_out.to_csv('Amtran_out.csv')