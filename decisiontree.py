"""
Created on Nov 1, 2019

@author: Mohammed Farhaan Shaikh
"""


import pandas as pd
import sys
import getopt
import math


output_data = "" # Stores the data in the xml format as a string throughout the program 


def read_csv(file_name):

    csv_data = pd.read_csv(file_name, header=None, sep=',', engine='python')
    return csv_data


def write_to_xml(name, data):

    f = open(name, "w")
    f.write(data)

''' calculates and returns the entropy of a node '''
def calculate_entropy(data, col, count_of_target_variable):
    
    unique_elements = data[col].unique()
    # print (unique_elements)
    if len(unique_elements) == 1:
        return 0
    total = 0
    p_denominator = data.count()[0]
    # print("denominator = ", p_denominator)
    for x in unique_elements:
        p_numerator = data[data[col] == x].count()[0]
        # print("numerator = ", p_numerator)
        total = total + (p_numerator / p_denominator) * math.log((p_numerator / p_denominator), count_of_target_variable)
        
    entropy = total * -1
    
    return entropy


''' This function runs recursively for each of the non leaf nodes until a leaf node is achieved '''
def split(data, parent_entropy, target_col_number, count_of_target_variable, level):

    global output_data
    information_gain = []           # Collection of all information gains
    entropy_collection = []         # Collection of all entropies
    unique_element_collection = []  # Collection of all unique values of each attribute
    target_output_collection = []   # Collection of all the target attributes

    for x in range (target_col_number):
        unique_elements = data[x].unique()
        target_outputs = []
        child_entropies = []
        child_entropy_sum = 0

        for y in unique_elements:
            # print (data[data[x] == y])
            child_entropy = calculate_entropy(data[data[x] == y], target_col_number, count_of_target_variable)
            child_entropies.append(child_entropy)
            # print (child_entropies)

            if child_entropy == 0:
                target_outputs.append(data[data[x] == y][target_col_number].unique()[0])
                # print ("target >> ", data[data[x] == y][target_col_number].unique()[0])
            else:
                target_outputs.append("nan")
            # print (data[data[x] == y].count()[0], "    ", data.count()[0])
            # print (child_entropy)

            child_entropy_sum = child_entropy_sum + (data[data[x] == y].count()[0] / data.count()[0]) * child_entropy

        information_gain.append(parent_entropy - child_entropy_sum)
        entropy_collection.append(child_entropies)
        unique_element_collection.append(unique_elements)
        target_output_collection.append(target_outputs)
        
        # print (entropy_collection)
    
    # print ("Information Gain = ", information_gain)
    # print (entropy_collection)
    split_index = information_gain.index(max(information_gain))

    # print ("|"*level, "split on ", split_index, "Entropy = ", parent_entropy)
    # unique_elements = data[split_index].unique()

    selected_unique_elements = unique_element_collection[split_index]
    selected_entropies = entropy_collection[split_index]
    selected_target_outputs = target_output_collection[split_index]
    # print(unique_elements)
    # print(selected_entropies)
    
    for x in range(len(selected_entropies)):
        # print (x)
        if selected_entropies[x] == 0:
            ''' leaf node achieved here '''
            # print ("|"*(level+1), "Leaf node achived at value = ", selected_unique_elements[x],
            #        "Entropy = ",selected_entropies[x], "feature =", split_index, "target = ",
            #        selected_target_outputs[x])
            # output_data = output_data + "|"*(level+1)+"Leaf node achived at value = "+str(selected_unique_elements[x])+"Entropy = "+str(selected_entropies[x])+"feature ="+str(split_index)+"target = "+str(selected_target_outputs[x])+"\n"
            output_data = output_data + "<node entropy=\""+str(selected_entropies[x]*1.0)+"\" feature=\"att"+str(split_index)+"\" value=\""+str(selected_unique_elements[x])+"\">"+str(selected_target_outputs[x])+"</node>"

        else:
            # print (data[data[split_index] == selected_unique_elements[x]])
            # print("|"*(level+1), "splitting at value = ", selected_unique_elements[x], "Entropy = ",
            #       selected_entropies[x], "feature =", split_index)
            output_data = output_data + "<node entropy = \""+str(selected_entropies[x])+"\" feature = \"att"+str(split_index)+"\" value = \""+str(selected_unique_elements[x])+"\">"
            split(data[data[split_index] == selected_unique_elements[x]], selected_entropies[x], target_col_number, count_of_target_variable, (level+1))
            output_data = output_data + "</node>"
        

def main(argv):

    input_file_name = ""
    output_file_name = ""

    global output_data

    ''' This part is for the command line input '''
    unix_options = "hd:o"
    gnu_options = ["help", "data=", "output="]

    try:
        arguments, values = getopt.getopt(argv, unix_options, gnu_options)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        print("decisiontree.py --data <PathToData> --output <PathToOutput>")
        sys.exit(2)

    if len(arguments) < 1:
        print("ERROR in input parameters !! \nPlease use this format")
        print("decisiontree.py --data <PathToData> --output <PathToOutput>")
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("decisiontree.py --data <PathToData> --output <PathToOutput>")
            sys.exit()
        elif currentArgument in ("-d", "--data"):
            input_file_name = currentValue
        elif currentArgument in ("-o", "--output"):
            output_file_name = currentValue

    data = read_csv(input_file_name)
    target_col_number = len(data.columns)-1                 # Finds the target column number
    unique_elements = data[target_col_number].unique()
    count_of_target_attribute = len(unique_elements)        # Gets the count of unique of number of target attributes

    # print(data)
    entropy = calculate_entropy(data, target_col_number, count_of_target_attribute)
    # print(entropy)

    output_data = output_data + "<tree entropy = \""+str(entropy)+"\">"

    print("Running...")
    split(data, entropy, target_col_number, count_of_target_attribute, 0)

    output_data = output_data + "</tree>"
    # print(output_data)

    write_to_xml(output_file_name, output_data)
    print("Program complete! \nData stored in >> ", output_file_name)
    

if __name__ == "__main__":
    main(sys.argv[1:])
