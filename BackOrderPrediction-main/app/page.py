from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import joblib
import base64
import datetime
import io
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
loaded_pipeline = joblib.load('pipeline_model.joblib')
drop_file = html.Div([
    html.Label("======= Drop File =======",  style={"font-size": "50px", "font-weight": "Bold", "vertical-align" : "center",'color':'Black','margin-top':'20px'}),
    html.Br(),
    html.Br(),
    html.Label( "Remarks: To utilize the drop file function, users must drop a .csv file containing all features with identical names as those in the dataset.",style={'textAlign': 'justify', "font-size": "20px","font-weight": "200"}),
    html.Br(),
    html.Label("Presently, the drop file function can work only one sample per file.",style={'textAlign': 'justify', "font-size": "20px","font-weight": "200"}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            "font-size": "20px",
            'width': '100%',
            'height': '200px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            "display": "flex",
            "justify-content": "center",  
            "align-items": "center", 
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

        #Prediction
        y_pred = loaded_pipeline.predict(df)
        # Create the mapping
        mapping = {1: 'Yes, it will be a backorder.',0: "No, it won't be a backorder.",}
        # Map
        mapped_value = mapping.get(y_pred[0], 'Unknown')
        df_tran=df.T.reset_index()
        df_tran.columns = ['Features', 'Values']
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.Label(filename, style={'textAlign': 'center', 'fontSize': 25, 'color':'black',"font-weight": "2000"}),
        html.Br(),
        html.Label(datetime.datetime.fromtimestamp(date), style={'textAlign': 'center', 'fontSize': 20}),


        dash_table.DataTable(
            data=df_tran.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_tran.columns],
            style_table={'overflowX': 'auto', 'margin': 'auto', 'width': '50%'},  # Center the table
            style_cell={
                'textAlign': 'center',
                'fontSize': 15,  # Center-align the cell content
                'color':'black'
            },  # Center-align the cell content
        ),

        html.Hr(),  # horizontal line
        html.Br(),
        html.Br(),
        html.Label (mapped_value, style={'textAlign': 'center', 'fontSize': 40,"font-weight": "2000", "color":"Navy",'margin-bottom': '10vh'})
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

