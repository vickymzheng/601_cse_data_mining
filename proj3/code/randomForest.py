## Random Forest implementation for project 3

import numpy as np
import collections
import re
import random
import pdb


class TreeNode:
    node_index = -1;
    children_list = []  # node indice of children nodes
    include_samples = []    # indice of samples at this node
    feature_type = []   # 0 - continuous, 1 - nominal
    condition_feature = -1
    condition_threshold = 0
    nodelabel = -1;
    
    def __init__(self, rnode_index, rchildren_list, rinclude_samples, rfeature_type):
        self.node_index = rnode_index
        self.children_list = rchildren_list
        self.include_samples = rinclude_samples
        self.feature_type = rfeature_type

    def get_labels(self,dataset_m):
        include_Sample_data = dataset_m[self.include_samples,:]
        dims = include_Sample_data.shape
        include_Sample_data_a = np.array(include_Sample_data)
        labels = include_Sample_data_a[:,dims[1]-1]
        return labels


    def isleafnode(self,dataset_m, threshold_impurity):
        labels = self.get_labels(dataset_m)
        if len(labels) == 1:
            return 1=
        if len(labels) == 0:
            return 1
        
        impurity = self.classification_error(dataset_m)
        if impurity > threshold_impurity:
            return 0
        else:
            return 1



    def classification_error(self,dataset_m):
        if len(self.include_samples) > 0:
            dims0 = len(self.include_samples)
            labels = self.get_labels(dataset_m)
            label0_num = list(labels).count(0)
            label1_num = dims0 - label0_num
            return (1 - max([label0_num, label1_num])*1.0/dims0)
        else:
            return 100

#    def test( self, feature_index):
#        #pdb.set_trace()
#        include_Sample_data = dataset_m[self.include_samples,:]
#        labels = self.get_labels(dataset_m)
#        include_Sample_data_a = np.array(include_Sample_data)
#        feature = include_Sample_data_a[:,feature_index]
#    
#        sorted_index = sorted(range(len(feature)),key=lambda x:feature[x])
#        sorted_labels = labels[sorted_index]
#        print sorted_labels
#        return sorted_labels

    

    def hunt(self, dataset_m, my_impurity, treenode_list, threshold_impurity):
        self.condition_threshold = threshold_impurity
        self.condition_feature = -1
        
        if self.isleafnode(dataset_m, threshold_impurity) == 0:
            
            ## find best condition_feature and condition_threshold and assign
            dims = dataset_m.shape
            include_Sample_data = dataset_m[self.include_samples,:]
            include_Sample_data_a = np.array(include_Sample_data)
            min_impurity = my_impurity
            
            
            for i in range(0,dims[1]-1):
                feature = include_Sample_data_a[:,i]
                parts_index_tem =  map(lambda x: x ==  self.condition_threshold, feature)
                part1_index = np.where(np.array(parts_index_tem) == True)[0]
                part2_index = np.where(np.array(parts_index_tem) == False)[0]
            
                part1_labels = []
                part2_labels = []
            
                for p1 in part1_index:
                    part1_labels.append(dataset_m[p1,dims[1]-1])
                
                
                
                for p2 in part2_index:
                    part2_labels.append(dataset_m[p2,dims[1]-1])


                n1_len = len(part1_labels)
                n2_len = len(part2_labels)
                #print 'N0 has %d points and N1 has %d points' %(n1_len, n2_len)
                if n1_len > 0 and n2_len > 0:
                    p = n1_len * 1.0 / (n1_len+n2_len)
                    new_impurity = p * labels_clf_error(part1_labels) + (1-p)*labels_clf_error(part2_labels)
                
                    #print 'using feature %d: new impurity %f N0 error %f and N1 error %f' %(i, new_impurity,labels_clf_error(part1_labels),labels_clf_error(part2_labels))
                
                    if  new_impurity < min_impurity:
                        min_impurity = new_impurity
                        self.condition_feature = i
        
            

            
            if self.condition_feature != -1 :
                feature = include_Sample_data_a[:,self.condition_feature]
                
                tem =  map(lambda x: x <= self.condition_threshold, feature)
                tem = np.array(tem)


                for i in range(0,2):    # split tree node
                    child_node_index = len(treenode_list)
                    self.children_list.append(child_node_index)
                    child_children_list = []

                    if i == 0:
                        tem_include_samples = np.where(tem == True)[0]
                    else:
                        tem_include_samples = np.where(tem == False)[0]
                
                    child_include_samples = []
                    for j in range(0, len(tem_include_samples)):
                        child_include_samples.append( self.include_samples[tem_include_samples[j]] )

                    child_feature_type = self.feature_type

                    child_treenode = TreeNode(child_node_index,child_children_list,child_include_samples,child_feature_type)

                    treenode_list.append(child_treenode)


                for i in range(0,2): # recursion for child nodes
                    test_node = treenode_list[self.children_list[i]]
                    # def hunt(self, dataset_m, my_impurity, treenode_list, threshold_impurity):
                    treenode_list = test_node.hunt( dataset_m,test_node.classification_error(dataset_m), treenode_list, threshold_impurity)

        return treenode_list

    def get_leaf_label(self,dataset_m):
        if len(self.children_list) == 0: # leaf node, no children
            labels = self.get_labels(dataset_m)
            tem = collections.Counter(labels).most_common(1)
            self.nodelabel = tem[0][0]

        return self.nodelabel


def assign_label1( treenode_list, features):
    mylabel = treenode_list[0].nodelabel
    this_node = treenode_list[0]
    
    
    while( len(this_node.children_list) != 0 ):
        to_child = this_node.children_list[ int(features[0,this_node.condition_feature]) ]
        this_node = treenode_list[to_child]
        mylabel = this_node.nodelabel

    return mylabel

def assign_labels(treenode_list, test_index, dataset_m):
    num = len(test_index)
    mylabels = [-1] * num
    dims = dataset_m.shape

    for i in range(0,num):
        
        features = dataset_m[ test_index[i] ,0:dims[1]-1]
        mylabels[i] = assign_label1( treenode_list, features)

    return mylabels






def labels_clf_error(labels):
    if len(labels) > 0:
        dims0 = len(labels)
        label0_num = list(labels).count(0)
        label1_num = dims0 - label0_num
        return (1 - max([label0_num, label1_num])*1.0/dims0)
    else:
        return 100


def create_dataset(filename):
    text_file = open(filename, "r")
    lines = text_file.readlines()
    dataset = []
    for line in lines:
        parts = line.split('\t')
        if filename == "project3_dataset2.txt":
            if parts[4] == "Present":
                parts[4] = 1
            else:
                parts[4] = 0

            ints = [0,5,8,9]
            floats = [1,2,3,6,7]


        if filename == "project3_dataset1.txt":
            ints = [30]
            floats = range(0,30)

        for i in ints:
            parts[i] = int(parts[i])
        for f in floats:
            parts[f] = float(parts[f])
            
        dataset.append(parts)


    return dataset


def easy_process(dataset_m, dims, feature_type):
    new_dataset = dataset_m
    dataset_m_a = np.array(dataset_m)
    
    for i in range(0,dims[1]-1):
        if feature_type[i] == 0:
            feature = dataset_m_a[:,i]
            average = np.mean(feature)
            tem = np.zeros(dims[0])
            larger_index_tem =  map(lambda x: x > average, feature)
            larger_index = np.where(np.array(larger_index_tem) == True)[0]
            smaller_index = np.where(np.array(larger_index_tem) == False)[0]
        
            for l in larger_index:
                new_dataset[l,i] = 1
            for s in smaller_index:
                new_dataset[s,i] = 0


    return new_dataset

def treenode_list_label(treenode_list, dataset_m):
    for i in range(0,len(treenode_list)):
        node_label = treenode_list[i].get_leaf_label(dataset_m)
        #print node_label


def print_tree(treenode_list, dataset_m):
    node_num = len(treenode_list)
    dims = dataset_m.shape

    for i in range(0,node_num):
        thisnode = treenode_list[i]
        print "node index is %d" % thisnode.node_index



def calcPerformance(ground_truth, mylabels):
    truePositive = 0.0
    falsePositive = 0.0
    trueNegative = 0.0
    falseNegative = 0.0
    numSamples = len(ground_truth)
    for i in range(0,numSamples):
        if (ground_truth[i] == 1 and mylabels[i] == 1):
                truePositive+=1
        elif (ground_truth[i] == 0 and mylabels[i] == 1):
                falsePositive+=1
        elif (ground_truth[i] == 0 and mylabels[i] == 0):
                trueNegative+=1
        else:
                falseNegative+=1
    
    print "True positive: " + str(truePositive)
    print "False negative: " + str(falsePositive)
    print "True negative: " + str(trueNegative)
    print "False negative: " + str(falseNegative)

    accuracy = (truePositive+trueNegative)/numSamples
    if truePositive + falsePositive > 0:
        precision = truePositive / (truePositive + falsePositive)
    else:
        precision = 0
    if truePositive + falseNegative > 0:
        recall = truePositive / (truePositive + falseNegative)
    else:
        recall = 0
    if 2*truePositive + falsePositive + falseNegative> 0:
        F = (2 * truePositive) / (2*truePositive + falsePositive + falseNegative)
    else:
        F = 0
    
    print "Accuracy: " + str(accuracy)
    print "Precision: " + str(precision)
    print "Recall: " + str(recall)
    print "F: " + str(F)

    return [accuracy, precision, recall, F]



def kCrossVal(dataset_m, feature_type,K):
    k = K
    dims = dataset_m.shape
    numSamples = dims[0]
    sizeTestSet = numSamples/k
    sizeTraining = numSamples - sizeTestSet
        
    all_index = range(0,numSamples)
    
    
    performance = []
    perf_sum = np.zeros(4)
    for i in range(0,k):
        startIndex = sizeTestSet*i
        endIndex = startIndex + sizeTestSet
        test_index = range(startIndex,endIndex+1)
        train_index = np.delete(all_index,test_index)
        
        test_data_m = dataset_m[test_index,:]
        train_data_m = dataset_m[train_index,:]
    
        treenode_list = []
        threshold_impurity = 0
        
        root = TreeNode(0,[],train_index,feature_type)
        treenode_list.append(root)
        root_impurity = treenode_list[0].classification_error(dataset_m)
        treenode_list = treenode_list[0].hunt(dataset_m, root_impurity, treenode_list, threshold_impurity)
        treenode_list_label(treenode_list, dataset_m)

        #for i in range(0,len(treenode_list)):
            #print 'node label', treenode_list[i].nodelabel
        
        
        test_labels = assign_labels(treenode_list, test_index, dataset_m)
        ground_truth = []
        for j in range(0,len(test_index)):
            ground_truth.append(dataset_m[test_index[j],dims[1]-1])
        
        
        print 'cross validation round ', i+1
        this_perf = calcPerformance(ground_truth, test_labels)
        print this_perf
        performance.append(this_perf)
        perf_sum = perf_sum + this_perf
        print '\n'


    perf_sum = perf_sum * 1.0 / k
    return [performance, perf_sum]

        



filename = "project3_dataset2.txt"
dataset = create_dataset(filename)
dataset_m = np.matrix(dataset)
dims = dataset_m.shape

if filename == "project3_dataset2.txt":
    feature_type = [0,0,0,0,1,0,0,0,0]
else:
    feature_type = np.zeros(dims[1]-1)


dataset_new = easy_process(dataset_m, dims, feature_type)
pdb.set_trace()
# shuffle dataset_new for cross validation
all_index = range(0,dims[0])
random.shuffle(all_index)
dataset_new = dataset_new[all_index,:]


[performance, perf_sum] = kCrossVal(dataset_new, feature_type,10)
print performance
print perf_sum

#treenode_list = []
#threshold_impurity = 0
#root = TreeNode(0,[],range(0,dims[0]),feature_type)
#treenode_list.append(root)
#root_impurity = treenode_list[0].classification_error(dataset_new)
#treenode_list = treenode_list[0].hunt(dataset_new, root_impurity, treenode_list, threshold_impurity)
#print len(treenode_list)
#
#print 'node label init'
#for i in range(0,len(treenode_list)):
#    print treenode_list[i].nodelabel
#
#treenode_list_label(treenode_list, dataset_m)
#print 'vote label init'
#for i in range(0,len(treenode_list)):
#    print treenode_list[i].nodelabel
#

#test_index = [2,5,7,8,9,34]
#pdb.set_trace()
#test_labels = assign_labels(treenode_list, test_index, dataset_m)
#print 'test labels:'
#for l in test_labels:
#    print l

#print 'vote node label'
#for i in range(0,len(treenode_list)):
#    print treenode_list[i].get_leaf_label(dataset_m)


#pdb.set_trace()
########## test class func isleafnode ##########
#onenode = TreeNode(0,[1],range(0,dims[0]),feature_type)
#nodes = []
#nodes.append(onenode)
#onenode = TreeNode(1,[],range(0,5),feature_type)
#nodes.append(onenode)
##pdb.set_trace()
#res = nodes[1].isleafnode(dataset_m)
#print res
#pdb.set_trace()
#sorted_labels = onenode.test(4)
########## end of test #########################

########## test class func classification_error ####
#pdb.set_trace()
#error = nodes[0].classification_error(dataset_m)
#print error

########## end of test ########################
