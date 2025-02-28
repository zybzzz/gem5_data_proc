import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os.path as osp
from typing import Dict

spec2006_int = [
    "perlbench", "bzip2", "gcc", "mcf", "gobmk", "hmmer", "sjeng", "libquantum", "h264ref", "omnetpp", "astar","xalancbmk"
]

spec2006_fp = [
    "bwaves", "gamess", "milc", "zeusmp", "gromacs", "cactusADM", "leslie3d", "namd", "dealII", "soplex", "povray",
    "calculix", "GemsFDTD", "tonto", "lbm", "wrf", "sphinx3"
]

tags = ["baseline", "addvp", "lvp", "al-hybrid"]
weighted_data_path: Dict[str, str] = {tag: osp.join("/home/zybzzz/proj/openxiangshan/tools/gem5_result/im-bug-fix/results",
                                    tag, "weighted_df.csv") for tag in tags}
weighted_df_map: Dict[str, pd.DataFrame] = {tag: pd.read_csv(path, index_col=0) for tag, path in weighted_data_path.items()}

for tag in weighted_df_map:
    weighted_df_map[tag] = weighted_df_map[tag].drop(index=spec2006_fp)
    weighted_df_map[tag] = weighted_df_map[tag][['cpi']]
    weighted_df_map[tag] = weighted_df_map[tag].rename(columns={'cpi':'ipc'})
    weighted_df_map[tag]['ipc'] = 1 / weighted_df_map[tag]['ipc']
    weighted_df_map[tag].loc['average'] = weighted_df_map[tag].mean()

weighted_df_all = pd.concat(weighted_df_map.values(), axis=1).round(2)
weighted_df_all.columns = tags
species = weighted_df_all.index.tolist()
datamap = weighted_df_all.to_dict(orient="list")
print(datamap)

x = np.arange(len(species))  # the label locations
x = x * 2.5
width = 0.5  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in datamap.items():
    offset = width * multiplier
    print(len(x))
    print(len(measurement))
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3, fontsize=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('IPC')
ax.set_title('IPC compare')
ax.set_xticks(x + width, species, fontsize=6)
# ax.legend(loc='upper left', ncols=4)
ax.set_ylim(0, 6)
plt.savefig(osp.join("/home/zybzzz/proj/openxiangshan/tools/gem5_result/im-bug-fix/results","ipc.png"), dpi=1000, bbox_inches='tight')


#print(datamap)
#print(weighted_df_all)
#print(weighted_df_map["addvp"])


