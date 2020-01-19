import pickle as p
import json, scipy.misc, math
import numpy as np
from skimage.draw import line
from skimage.morphology import thin
import matplotlib.pyplot as plt
from PIL import Image
import xml.etree.ElementTree as ET
from io import StringIO
from tqdm import tqdm
import os

labls = ['!', '(', ')', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '[', '\\alpha', '\\beta', '\\cos', '\\div', '\\exists', '\\forall', '\\gamma', '\\geq', '\\gt', '\\in', '\\infty', '\\int', '\\ldots', '\\leq', '\\lim', '\\log', '\\lt', '\\neq', '\\phi', '\\pi', '\\pm', '\\rightarrow', '\\sin', '\\sqrt', '\\sum', '\\tan', '\\theta', '\\times', '\\{', '\\}', ']', 'a', 'b', 'c', 'capital_A', 'capital_B', 'capital_C', 'capital_F', 'capital_X', 'capital_Y', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'm', 'n', 'p', 'r', 't', 'x', 'y', 'z']

new_dict = {}
i = 0
for labl in labls:
    new_dict[labl] = str(i)
    i = i+1


def get_traces_data(inkml_file_abs_path):

    traces_data = []

    tree = ET.parse(inkml_file_abs_path)
    root = tree.getroot()
    doc_namespace = "{http://www.w3.org/2003/InkML}"

    'Stores traces_all with their corresponding id'
    traces_all = [{'id': trace_tag.get('id'),
                    'coords': [[round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
                                    for axis_coord in coord[1:].split(' ')] if coord.startswith(' ') \
                                else [round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
                                    for axis_coord in coord.split(' ')] \
                            for coord in (trace_tag.text).replace('\n', '').split(',')]} \
                            for trace_tag in root.findall(doc_namespace + 'trace')]

    'Sort traces_all list by id to make searching for references faster'
    traces_all.sort(key=lambda trace_dict: int(trace_dict['id']))

    'Always 1st traceGroup is a redundant wrapper'
    traceGroupWrapper = root.find(doc_namespace + 'traceGroup')

    if traceGroupWrapper is not None:
        for traceGroup in traceGroupWrapper.findall(doc_namespace + 'traceGroup'):

            label = traceGroup.find(doc_namespace + 'annotation').text

            'traces of the current traceGroup'
            traces_curr = []
            for traceView in traceGroup.findall(doc_namespace + 'traceView'):

                'Id reference to specific trace tag corresponding to currently considered label'
                traceDataRef = int(traceView.get('traceDataRef'))

                'Each trace is represented by a list of coordinates to connect'
                single_trace = traces_all[traceDataRef]['coords']
                traces_curr.append(single_trace)


            traces_data.append({'label': label, 'trace_group': traces_curr})

    else:
        'Consider Validation data that has no labels'
        [traces_data.append({'trace_group': [trace['coords']]}) for trace in traces_all]

    return traces_data


def inkml2img(input_path, output_path):
#     print(input_path)
#     print(pwd)
    traces = get_traces_data(input_path)
#     print(traces)
    path = input_path.split('/')
    path = path[len(path)-1].split('.')
    path = path[0]+'_'
    file_name = 0
    for elem in traces:

#         print(elem)
#         print('-------------------------')
#         print(elem['label'])

        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axes().get_xaxis().set_visible(False)
        plt.axes().get_yaxis().set_visible(False)
        plt.axes().spines['top'].set_visible(False)
        plt.axes().spines['right'].set_visible(False)
        plt.axes().spines['bottom'].set_visible(False)
        plt.axes().spines['left'].set_visible(False)
        ls = elem['trace_group']
        output_path = output_path

        for subls in ls:
#             print(subls)

            data = np.array(subls)
#             print(data)
            x,y=zip(*data)
            plt.plot(x,y,linewidth=2,c='black')

        capital_list = ['A','B','C','F','X','Y']
        if elem['label'] in capital_list:
            label = 'capital_'+elem['label']
        else:
            label = elem['label']

        if label in new_dict.keys():
            label = new_dict[label]
        else:
            label = 'other'

        ind_output_path = output_path + label
#         print(ind_output_path)
        try:
            os.mkdir(ind_output_path)
        except OSError:
#             print ("Folder %s Already Exists" % ind_output_path)
#             print(OSError.strerror)
            pass
        else:
#             print ("Successfully created the directory %s " % ind_output_path)
            pass
#         print(ind_output_path+'/'+path+str(file_name)+'.png')
        if(os.path.isfile(ind_output_path+'/'+path+str(file_name)+'.png')):
            # print('1111')
            file_name += 1
            plt.savefig(ind_output_path+'/'+path+str(file_name)+'.png', bbox_inches='tight', dpi=100)
        else:
            plt.savefig(ind_output_path+'/'+path+str(file_name)+'.png', bbox_inches='tight', dpi=100)
        plt.gcf().clear()
