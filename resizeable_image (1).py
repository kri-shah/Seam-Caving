import imagematrix
import numpy as np

class ResizeableImage(imagematrix.ImageMatrix):
    def naive_help(self, i, j):
        #base case - if at top return coordinates
        if i == 0:
            return [(i, j)]
        
        energy = self.energy(i, j)
        min_seam = [(i, j)] 
        min_energy = float('inf')

        #look at the three possible paths
        for x in [-1, 0, 1]:
            new_j = j + x
            #checking to make sure we aren't at an edge 
            if 0 <= new_j and new_j < self.width:
                #recursively find the seam in the row above 
                seam = self.naive_help(i - 1, new_j)

                #calculate the total energy of the current seam
                total_energy = energy
                for x in seam:
                    total_energy += self.energy(x[1], x[0])
                total_energy += sum(self.energy(x[1], x[0]) for x in seam)
                
                #update the minimum seam if the current seam has lower total energy
                if total_energy < min_energy:
                    min_energy = total_energy
                    min_seam = seam + [(i, j)]
                    
        
        return min_seam

    def naive(self):
        #basic declarations
        w = self.width
        h = self.height
        coordinates = []

        #we need to run the recursion for every column
        for j in range(w):
            seam = self.naive_help(h - 1, j)
            
            coordinates.append(seam)

        min_energy = float('inf')
        best_seam = []
        
        #find the best seam among all calculated seams
        for seam in coordinates:
            total_energy = 0
            for x in seam:
                total_energy += self.energy(x[1], x[0])
            if total_energy < min_energy:
                min_energy = total_energy
                best_seam = seam
        
        #so for some the tuples are backwards coordinates (compared to my DP alg)
        #couldnt find a more elegant solution so i kinda just iterate through and reverse each tuple pair
        #not great for memory since a new tuple gets made this alg is alr rlly bad
        new_seam = []
        for x in best_seam:
            new_seam.append(x[::-1])
        
        return new_seam
    
    def dp(self):
        w = self.width
        h = self.height
        matrix = np.zeros((h, w))

        #initialize the matrix with inf instead of zero
        matrix.fill(np.inf)

        #base case - top row is just the energy of that pixel
        for i in range(w):
            matrix[0][i] = self.energy(i, 0)

        # DP recursion - checks table looks for min of top three values above array (unless on edge)
        for i in range(1, h):
            for j in range(0, w):
                if j == 0:
                    matrix[i][j] = min(matrix[i-1][j], matrix[i-1][j+1]) + self.energy(j, i)
                elif j == w - 1:
                    matrix[i][j] = min(matrix[i-1][j], matrix[i-1][j-1]) + self.energy(j, i)
                else:
                    matrix[i][j] = min(matrix[i-1][j], matrix[i-1][j-1], matrix[i-1][j+1]) + self.energy(j, i)

        #base declarations for backtracking
        seam = []
        row = matrix[-1]
        start_col = np.argmin(row)
        seam.append((start_col, h - 1))
        
        #set row to bottom, set column to where the smallest row is on the bottom 
        i = h - 1
        j = start_col
        #travel til top of matrix
        for i in range(h - 2, -1, -1):
            #normal case basically looks at the three indexs direcrlty above the spot in the matrix, 
            # and picks the smallest one to go up to and logs that 
            #edge cases are j == 0 and j== w-1: 
            #     basically if its on and edge we check directly above and inside so we get no out of bounds
            if j == 0:
                j = np.argmin(matrix[i, j:j+2])
            elif j == w - 1:
                j = np.argmin(matrix[i, j-1:j+1]) + j - 1
            else:
                j = np.argmin(matrix[i, j-1:j+2]) + j - 1

            seam.append((j, i))

        seam.reverse()
        return seam

    def best_seam(self, dp=True):
        if dp:
            return self.dp()
        else:
            return self.naive()
    
    def remove_best_seam(self):
        self.remove_seam(self.best_seam()) 

#some tests
'''
vals = ["soccer_10x10.webp", "baseball_10x10.jpg"]
for v in vals:
    image = ResizeableImage(v)
    seam = print(image.best_seam())
    seam = print(image.best_seam(False))
'''

'''
image = ResizeableImage("sunset_full.png")
seam = image.best_seam()
'''


'''
image = ResizeableImage("40x40.png")
seam = print(image.best_seam())
'''
