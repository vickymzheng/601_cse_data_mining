randCentroid.py takes in two arguments: The name of your dataset file and the name of the file where you want to put your random clusters. 
getClusterAssignments.py takes in two arguments: The name of the dataset file and the name of the file where you want to put your assignments. 

Mapper requires you to cat your inputs into it. Such as: cat dummyData.txt | mapper.py. In mapper.py is a line where you store which centroid file you're reading from to get the centroids and calculate distances between each centroid. We calculate all the distances with the getDist function and then print out all of the ID of the entry and its distance between each centroid. We print it out because this will then be fed into reducer.py

In reducer.py, we take in what mapper.py printed out. Now, we determine whether or not we should reassign this entry to a new centroid and reassign it if necessary. Once all centroids are reassigned, we calculate the new centroids and write into the centroid file. We also check if the assignments have changed by looking into the assignment file. If they have, then we update the assignment file. 

setUp* are scripts that get your environment ready for hadoop
run* are scripts that run hadoop on an input file. For example, ./runCho runs kmeans map reduce with hadoop on cho.txt. You must run ./setUpCho first.

visualize.py visualizes your cluster assignments by using PCA.