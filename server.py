    
from flask import Flask,request,Response,jsonify
import json
import os
import pandas as pd
import sys
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def sunburst(df):
    li=list()
    grouped = df.groupby(['NOM_DEPAR','NOM_MUN'], as_index=False)["NETO_CDP"].sum()
    departamentos = grouped.NOM_DEPAR.unique()
    for departamento in departamentos:
        df_act = grouped[grouped['NOM_DEPAR'] == departamento]
        info = {'name': departamento, 'children': []}
        for index, row in df_act.iterrows():
            info['children'].append({'name': row['NOM_MUN'], 'value': row['NETO_CDP']})
        
        data = sorted(info['children'],key=lambda x: x['value'],reverse=True)
        info['children']=data[:min(40,len(data))]
        li.append(info)
        
    return {"name":"departamentos", "children":li}


@app.route('/',methods=['POST'])
def hello_world():
    return jsonify(request.json)

@app.route('/sunburst',methods=['GET'])
def sunburst_r():
    return Response(json.dumps(sunburst(df)),mimetype='application/json')



def pa(path):
	current = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(current, path)



df = pd.read_pickle('datos.pkl')
if __name__ == "__main__":
	app.run(debug=True, port=8000, host='0.0.0.0')
