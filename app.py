import ast
import json

from flask import *
import os
import pandas as pd
from models.ml_algos import ML_ALGOS
from flask_cors import CORS
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.jinja_env.globals.update(zip=zip)
cors = CORS(app)
#from flask_restful import Resource
import pandas as pd

UPLOAD_FOLDER='static/datasets'
dataset=None
def load_csv(path):
    global dataset
    dataset=pd.read_csv(path)
    return [dataset.to_html(classes='data table-responsive', header="true")]
def getoutput(do_list,filename):
    dataset=pd.read_csv('static/datasets/{0}'.format(filename))
    algo_obj=ML_ALGOS(dataset)
    result_list={}
    if isinstance(do_list,dict):
        do_list=do_list.keys()
    for i in do_list:
        if i==1:
            result_list[i]=(algo_obj.FIND_S())
            continue
        elif i==2:
            result_list[i]=(algo_obj.CANDIDATE_ALGO())
            continue
        elif i==3:
            result_list[i]=(algo_obj.ID3())
            continue
        elif i==4:
            result_list[i]=(algo_obj.BackPropagation())
            continue
        elif i==5:
            result_list[i]=(algo_obj.naive_bayes_GNB())
            continue
        elif i==6:
            result_list[i]=(algo_obj.naive_bayes_MNB())
            continue
        elif i==7:
            result_list[i]=(algo_obj.naive_bayes_BNB())
            continue
        elif i==8:
            result_list[i]=(algo_obj.bayesian_network())
            continue
        elif i==9:
            result_list[i]=(algo_obj.EM_GMM())
            continue
        elif i==10:
            result_list[i]=(algo_obj.K_Means())
            continue
        else:
            pass

    return result_list


@app.route('/')
def index():# put application's code here
    return render_template('index.html')
@app.route('/UpdateDateSet/', methods=['GET','POST'])
def UpdateDateSet():
    if request.method=='POST':
        file=request.files['file']
        filename=file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        dat=load_csv(UPLOAD_FOLDER+'/'+filename)
        return render_template('index.html',tables=dat,filename=filename)
    else:
        return 's'
@app.route('/getresult/',methods=['POST','GET'])
def getresult():
    if request.method=='POST':
        do_algo={}
        filename=request.form['filename']
        data=request.form['dataset']
        data=ast.literal_eval(data)
        for i in range(1,11):
            if request.form.get(str(i)):
                do_algo[i]=request.form[str(i)]
        result=getoutput(do_algo,filename)
        print(result)
        return render_template('index.html',tables=data,filename=filename,result=result,do_algov=do_algo)
    else:
        return abort(500)
'''#@app.route('/getcsvFile/',methods=['POST'])
def getcsvFile():
    if request.method=='POST':
        file =request.data
        data = pd.read_csv(file)
        print('sucess')
    return data'''
@app.route('/upload/',methods=['POST'])
def upload_dataset():
    if request.method=='POST':
        target=os.path.join(UPLOAD_FOLDER, 'test_docs')
        if not os.path.isdir(target):
            os.mkdir(target)
        csv_file=request.files['csv_file']
        print(request.files)
        filename=csv_file.filename
        destination="/".join([target, filename])
        print(destination)
        csv_file.save(destination)
        return {"status":0,"filename":filename}
    else:
        return {"status":1}
@app.route('/GetResultAsJson/',methods=['GET'])
def GetResultAsJson():
    filename=request.args.get('filename')
    do_list=ast.literal_eval(request.args.get('do_algo'))
    load_csv('static/datasets/test_docs/{0}'.format(filename))
    result_list=getoutput(do_list,filename)
    print(result_list)
    return result_list


if __name__ == '__main__':
    app.run()
