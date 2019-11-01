'''
Created on Nov 1, 2019

@author: farhaan
'''

import pandas as pd
import math
from _operator import index


def read_csv(file_name):
    

    csv_data =  pd.read_csv(file_name, header=None, sep=','  , engine='python')
    return csv_data


def calculate_entropy(data, col, count_of_target_variable):
    
    unique_elements = data[col].unique()
    #print (unique_elements)
    if (len(unique_elements) == 1):
        return 0
    total = 0
    p_denominator = data.count()[0]
    #print ("denominator = ", p_denominator)
    for x in unique_elements:
        p_numerator = data[data[col] == x].count()[0]
        #print ("numerator = ", p_numerator)
        total = total + (p_numerator / p_denominator) * math.log((p_numerator / p_denominator), count_of_target_variable)
        
    entropy = total * -1
    
    return entropy


def split(data, parent_entropy, target_col_number, count_of_target_variable, level):
    
    information_gain = []
    entropy_collection = []
    unique_element_collection = []
    target_output_collection = []
    for x in range (target_col_number):
        unique_elements = data[x].unique()
        target_outputs = []
        child_entropies = []
        child_entropy_sum = 0
        for y in unique_elements:
            #print (data[data[x] == y])
            child_entropy = calculate_entropy(data[data[x] == y], target_col_number, count_of_target_variable)
            child_entropies.append(child_entropy)
            #print (child_entropies)
            if (child_entropy == 0):
                target_outputs.append(data[data[x] == y][target_col_number].unique()[0])
                #print ("target >> ", data[data[x] == y][target_col_number].unique()[0])
            else:
                target_outputs.append("nan")
            #print (data[data[x] == y].count()[0], "    ", data.count()[0])
            #print (child_entropy)
            child_entropy_sum = child_entropy_sum + (data[data[x] == y].count()[0] / data.count()[0])* child_entropy
        
            
        information_gain.append(parent_entropy - child_entropy_sum)
        entropy_collection.append(child_entropies)
        unique_element_collection.append(unique_elements)
        target_output_collection.append(target_outputs)
        
        #print (entropy_collection)
    
    #print ("Information Gain = ", information_gain)   
    #print (entropy_collection) 
    split_index = information_gain.index(max(information_gain))
    
    
    
    
    #print ("|"*level, "split on ", split_index, "Entropy = ", parent_entropy) 
    
    
    
    
    
    #unique_elements = data[split_index].unique()
    selected_unique_elements = unique_element_collection[split_index]
    selected_entropies = entropy_collection[split_index]
    selected_target_outputs = target_output_collection[split_index]
    #print (unique_elements)
    #print (selected_entropies)
    
    for x in range(len(selected_entropies)):
        #print (x)
        if (selected_entropies[x] == 0):
            ''' leaf node comes here '''
            print ("|"*(level+1), "Leaf node achived at value = ", selected_unique_elements[x], "Entropy = ",selected_entropies[x], "feature =", split_index, "target = ", selected_target_outputs[x])
        else :
            #print (data[data[split_index] == selected_unique_elements[x]])
            print ("|"*(level+1), "splitting at value = ", selected_unique_elements[x], "Entropy = ", selected_entropies[x], "feature =", split_index)
            split(data[data[split_index] == selected_unique_elements[x]], selected_entropies[x], target_col_number, count_of_target_variable, (level+1))
        
    
    
def main():

    file_name = "car.csv"
    
    
    data = read_csv(file_name)
    target_col_number = len(data.columns)-1
    unique_elements = data[target_col_number].unique()
    count_of_target_variable = len(unique_elements)

    #print (data)
    entropy = calculate_entropy(data, target_col_number, count_of_target_variable)
    print (entropy)
    
    
    split(data, entropy, target_col_number, count_of_target_variable, 0)
    
    
    
    
    
if __name__ == "__main__":
    main()