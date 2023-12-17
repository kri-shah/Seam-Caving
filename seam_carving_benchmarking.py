from resizeable_image import ResizeableImage
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

#vals = ["plane_6x6.jpg", "baseball_10x10.jpg", "soccer_10x10.webp", "40x40.png", "cat_fortress_small.jpg", "sunset_full.png"]
vals = ["cat_fortress_small_ 408×306.jpg", "Adam_672x318.png", "Mountain_600x602.png", "Donkey_820x820.png", "NYC_1000x1000.png"]

num_iters = 25

avg_runtimes = {'DP': [], 'Non DP': []}

for v in vals:
    avg_runtimes_for_image = {'DP': [], 'Non DP': []}
    for i in range(num_iters):
        for algorithm in ['DP']:
            print(f"processing {algorithm} for image {v} (Iteration {i+1})")
            image = ResizeableImage(v)
            t0 = time.time()
            if algorithm == 'DP':
                seam = image.best_seam()
            elif algorithm == 'Non DP':  
                seam = image.best_seam(False)
            t1 = time.time()
            avg_runtimes_for_image[algorithm].append(t1 - t0)
            del image  #without this the code took forever to run 
            
    
    avg_runtimes['DP'].append(np.mean(avg_runtimes_for_image['DP']))
    avg_runtimes['Non DP'].append(np.mean(avg_runtimes_for_image['Non DP']))


df = pd.DataFrame(avg_runtimes, index=vals)


plt.scatter(df.index, df['DP'], label='DP', color='blue', marker='o', alpha=0.7)
plt.scatter(df.index, df['Non DP'], label='Non DP', color='red', marker='o', alpha=0.7)



dp_coeffs = np.polyfit(range(len(df.index)), df['DP'], 1)
non_dp_coeffs = np.polyfit(range(len(df.index)), df['Non DP'], 1)


plt.plot(range(len(df.index)), np.polyval(dp_coeffs, range(len(df.index))), linestyle='--', color='blue', label='DP Fit')
plt.plot(range(len(df.index)), np.polyval(non_dp_coeffs, range(len(df.index))), linestyle='--', color='red', label='Non DP Fit')

#making sure all the data is visible by forcing the y axis to be within 
dp_min = min(df['DP'])
dp_max = max(df['DP'])
non_dp_max = max(df['Non DP'])
plt.ylim(dp_min - 0.1, max(dp_max, non_dp_max) + 0.1)


plt.title('Average Runtimes Comparison')
plt.xlabel('Image File (w size of image in pixel x pixel)')
plt.ylabel(f'Average Runtime (seconds) for {num_iters} trials')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
