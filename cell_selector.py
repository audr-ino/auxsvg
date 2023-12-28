import pandas as pd
cells_df = pd.read_csv("cells_df.csv")

def find_cell(exp,range=.01):
    
    if (range<.001):
        print('warning: small range, may be impossible to find cells')

    exp_min = exp-range
    exp_max = exp+range

    above_min = cells_df['expL']>=exp_min
    below_max = cells_df['expL']<=exp_max

    potential_cells = cells_df[below_max & above_min]
    potential_cells = potential_cells.sort_values(by=['Energy_Barrier'],ascending=False).reset_index(drop=True)
    
    return (potential_cells['t'][0],potential_cells['theta'][0])

print(find_cell(1.8))