#print("test hellooooo")
#print("changes on the local computer 1")

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
#import descartes

gdf=gpd.read_file('GU_CountyOrEquivalent.shp')
df = pd.DataFrame(gdf)
df_seg=pd.read_csv("seg.csv")
new_df = df[df["State_Name"] == 'Kansas' ]
new_df.reset_index(drop=True, inplace=True)
merge_df=pd.merge(new_df, df_seg, left_on='County_Nam', right_on='County', how='inner')

gdf2 = gpd.GeoDataFrame(merge_df)

gdf2['coords'] = gdf2['geometry'].apply(lambda x: x.representative_point().coords[:])
gdf2['coords'] = [coords[0] for coords in gdf2['coords']]

#print(gdf.shape)
#print(gdf.head())
#gdf2.plot(column='County_Nam')

print(gdf2.head())
plt.rcParams['figure.figsize']=(20,15)
ax = gdf2.plot(column='Segment')
gdf2.apply(lambda x: ax.annotate(s=x.County_Nam, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
plt.show()

seg2=merge_df[['County_Nam','Segment']]
print(merge_df[['County_Nam','Segment']])
seg2.to_csv('seg2_out.csv',encoding='utf-8')
#new_df.to_csv('new-df.csv',encoding='utf-8')
print(new_df.head())