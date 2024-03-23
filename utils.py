#Imports
# Python Imports
import os 
import json
from collections import OrderedDict

# Additional Library Imports
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.manifold import TSNE


def store_feeder_info_to_json(args,infos):
    """Store Feeeder infos in a Json file
    """
       
    feeder_info = OrderedDict()
    feeder_info['name_of_the_feeder']=args.feeder
    feeder_info['num_of_original_buses']=len(infos['bus_list_before_exclusion'])
    feeder_info['num_of_buses']=len(infos['bus_list'])
    feeder_info['num_of_excluded_buses']=len(infos['bus_list_before_exclusion'])-len(infos['bus_list'])
    feeder_info['num_single_phase_buses'],feeder_info['num_two_phase_buses'],feeder_info['num_three_phase_buses']= len(infos['bus_list_1_phase']),len(infos['bus_list_2_phases']),len(infos['bus_list_3_phases'])
    feeder_info['num_edges']=int(len(infos['edge_list_by_bus_name'])/2)
    feeder_info['number_of_buses_with_connected_loads']=len(infos['bus_with_loads_connected'])
    feeder_info['number_of_loads']=len(infos['connected_loads_name'])
    
    folder_name = os.path.splitext(args.folder)[0]
    json_file='feeder_infos' # json file name with the same name as the folder
    os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
    json_path = os.path.join('../..',folder_name, json_file)
    
  
    with open(json_path, 'w') as json_file:
        json.dump(feeder_info, json_file, indent=4)
        
        
# Perform t-SNE visualization
def visualize_tsne(args,X,fault_class,savefigure=False):
    """T-SNE visualization of generated dataset
    """
    tsne = TSNE(n_components = 2, perplexity = 20.0, early_exaggeration = 6, 
               n_iter = 1000, learning_rate = 368, verbose = 1)
    X_tsne = tsne.fit_transform(X)
    num_classes=len(set(fault_class))
    tsne_result_df = pd.DataFrame({'tsne_1': X_tsne[:,0], 'tsne_2': X_tsne[:,1], 'label': fault_class})
    # Plotting with seaborn
    
    _, ax = plt.subplots(1)
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='tsne_1', y='tsne_2', hue='label',
                    ax=ax, s=10,
                    data=tsne_result_df,
                    palette=sns.color_palette("hsv", num_classes), 
                    legend='full')
    
    lim = (tsne.min()-5, tsne.max()+5)
    X_tsne.set_xlim(lim)
    X_tsne.set_ylim(lim)
    ax.set_aspect('equal')
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.title('2D t-SNE Visualization')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.legend(title='Class')
    plt.show()
   
    if savefigure:
         plt.savefig(os.path.join('../..',os.path.splitext(args.folder)[0],'tsne_viz.png'),
                     dpi=600)