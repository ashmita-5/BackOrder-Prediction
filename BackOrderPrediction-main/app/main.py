from dash import Dash, html, callback, Output, Input, State, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import joblib
import numpy as np
from dash.dependencies import Input, Output

import pandas as pd
from page import drop_file

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)


# load all components 
loaded_pipeline = joblib.load('pipeline_model.joblib')
columns = ['national_inv', 'lead_time', 'in_transit_qty', 'sales_1_month',
       'sales_3_month', 'sales_6_month', 'sales_9_month', 'min_bank',
       'potential_issue', 'pieces_past_due', 'perf_6_month_avg',
       'perf_12_month_avg', 'local_bo_qty', 'deck_risk', 'oe_constraint',
       'ppap_risk', 'stop_auto_buy', 'rev_stop']

# Define the layout for the Main Page
main_layout = html.Div([
    
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Prediction Model (manual)", href="/manual")),
            dbc.NavItem(dbc.NavLink("Drop File", href="/drop_file")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="BACKORDER PREDICTION",
        brand_href="/",
        color="primary",
        dark=True,
    ),
    
    html.Div(id="page-content")
],
    style={"text-align": "center"})

# Set up URL routing
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    main_layout
],
    style={"text-align": "center"})

intro_layout=  html.Div([
    html.Img(src='/assets/pic.jpg', style={'display': 'block', 'margin': '0 auto','width': '40%', 'height': 'auto'}),
    html.Br(),
    html.Label('BACKORDER Prediction', style={'textAlign': 'center', 'fontSize': 80, 'marginTop': '5vh',"font-weight": "1000"}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Label( "At Backorder Predictor, we specialize in assisting businesses and organizations in predicting the likelihood of product backorders. Our platform leverages advanced machine learning algorithms to forecast the probability of items going on backorder, enabling companies to optimize inventory management and maintain customer satisfaction.", style={'textAlign': 'justify', 'fontSize': 20,"font-weight": "200"}),
        html.Br(),
        html.Br(),
        html.Label("To access the model, click the right-upper navigation link 'Prediction Model (Manual)' or 'Drop File'.", style={'textAlign': 'center', 'fontSize': 20,"font-weight": "800"})
    ], style={'margin-left': '10%', 'margin-right': '10%', 'margin-bottom': '10vh'})
    
])
# Callback to update page content based on the URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/manual":
        return content_layout
    elif pathname == "/":
        return intro_layout
    elif pathname == "/about":
        return about_layout
    elif pathname =="/drop_file":
        return drop_file

content_layout= dbc.Container([
    dbc.Row([
        html.Div([
            html.Br(),
            html.Label("BackOrder Prediction",  style={"font-size": "50px", "font-weight": "Bold", "vertical-align" : "center",'color':'Blue'}),
            html.Div([
                html.Label( "For instruction, users need to define 18 features: 'national_inv', 'lead_time', 'in_transit_qty', 'sales_1_month',\
                            'sales_3_month', 'sales_6_month', 'sales_9_month', 'min_bank',\
                            'potential_issue', 'pieces_past_due', 'perf_6_month_avg',\
                            'perf_12_month_avg', 'local_bo_qty', 'deck_risk', 'oe_constraint',\
                            'ppap_risk', 'stop_auto_buy', 'rev_stop' After selecting or defining all features, click the 'PREDICTION' button below to submit all of the inputs. \
                            Then the result will show the predicted result in the form of classification which are 'Yes, it will be a backorder.' and 'No, it won't be a backorder.'.", 
                            style={'textAlign': 'justify', "font-size": "20px","font-weight": "200"}),
                html.Br(),
                html.Br(),
                html.Label("Remarks: There are default values in each feature in case the user does not type or select those inputs. ",style={'textAlign': 'justify', "font-size": "20px","font-weight": "1000"})
                             ], style={'margin-left': '10%', 'margin-right': '10%'}),
                html.Label("[national_inv=77.0, \
                            lead_time=8.0, \
                            in_transit_qty=1.0, \
                            sales_1_month=9.0, \
                            sales_3_month=27.0, \
                            sales_6_month=67.0, \
                            sales_9_month=104.0, \
                            min_bank=18.0, \
                            ",style={'textAlign': 'justify', "font-size": "15px","font-weight": "800"}),
                html.Label("potential_issue=No, \
                            pieces_past_due= 0.0, \
                            perf_6_month_avg=0.91, \
                            perf_12_month_avg=0.96, \
                            local_bo_qty=0.0, \
                            deck_risk=No, \
                            oe_constraint=No, \
                            stop_auto_buy=Yes ,\
                            rev_stop=No]",style={'textAlign': 'justify', "font-size": "15px","font-weight": "800"}),
                

                           
            html.Br(),
            html.Br(),
            html.Label("============ Manual Inputs ============",  style={"font-size": "40px", "font-weight": "Bold","vertical-align" : "center",'color':'Navy'}),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                dbc.Label("Current inventory level of component", style={"font-size": "25px"}),
                dbc.Input(id="national_inv", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Amount of the product in transit from source", style={"font-size": "25px"}),
                dbc.Input(id="in_transit_qty", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                 dbc.Label("Sales quantity for the prior 3 months", style={"font-size": "25px"}),
                dbc.Input(id="sales_3_month", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Sales quantity for the prior 9 months", style={"font-size": "25px"}),
                dbc.Input(id="sales_9_month", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Source issue for part identified", style={"font-size": "25px"}),
                dbc.Select(id='potential_issue', size="lg", options=[
                    {"label": "some issues are identified", "value": "Yes"},
                    {"label": "no issue", "value": "No"}
                    ]
                ),
                html.Br(),
                dbc.Label("Source performance for the prior 6 months", style={"font-size": "25px"}),
                dbc.Input(id="perf_6_month_avg", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Amount of stock orders overdue", style={"font-size": "25px"}),
                dbc.Input(id="local_bo_qty", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("OE Constraint Risk", style={"font-size": "25px"}),
                dbc.Select(id='oe_constraint', size="lg", options=[
                    {"label": "risk identified", "value": "Yes"},
                    {"label": "no risk", "value": "No"}
                    ]
                ),
                html.Br(),
                dbc.Label("Stop Auto Buy Risk", style={"font-size": "25px"}),
                dbc.Select(id='stop_auto_buy', size="lg", options=[
                    {"label": "risk identified", "value": "Yes"},
                    {"label": "no risk", "value": "No"}
                    ]
                ),
                html.Br(),
                ], width=6),
                 dbc.Col([
                dbc.Label("Transit time for the product", style={"font-size": "25px"}),
                dbc.Input(id="lead_time", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Sales quantity for the prior 1 months", style={"font-size": "25px"}),
                dbc.Input(id="sales_1_month", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Sales quantity for the prior 6 months", style={"font-size": "25px"}),
                dbc.Input(id="sales_6_month", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Minimum recommend amount to stock", style={"font-size": "25px"}),
                dbc.Input(id="min_bank", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Amount overdue from source", style={"font-size": "25px"}),
                dbc.Input(id="pieces_past_due", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Source performance for the prior 12 months", style={"font-size": "25px"}),
                dbc.Input(id="perf_12_month_avg", type="number", placeholder="Please type the number", size="lg"),
                html.Br(),
                dbc.Label("Deck Risk", style={"font-size": "25px"}),
                dbc.Select(id='deck_risk', size="lg", options=[
                    {"label": "risk identified", "value": "Yes"},
                    {"label": "no risk", "value": "No"}
                    ]
                ),
                html.Br(),
                dbc.Label("PPAP Risk", style={"font-size": "25px"}),
                dbc.Select(id='ppap_risk', size="lg", options=[
                    {"label": "risk identified", "value": "Yes"},
                    {"label": "no risk", "value": "No"}
                    ]
                ),
                html.Br(),
                dbc.Label("Revision Stop Risk", style={"font-size": "25px"}),
                dbc.Select(id='rev_stop', size="lg", options=[
                    {"label": "risk identified", "value": "Yes"},
                    {"label": "no risk", "value": "No"}
                    ]
                ),
                html.Br(),
                ], width=6),
                html.Br(),         
                html.Br(),
                html.Button(id="SUBMIT", children="Prediction", className="btn btn-outline-primary"), 
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Card([
                    dbc.CardHeader("Predicted BackOrder",style={"font-size": "30px", "font-weight": "700", "color":"white"}),
                    dbc.CardBody(html.Output(id="backorder",style={"font-size": "30px", "font-weight": "700", "color":"white"}))
                    ],style={   
                                "display": "flex",
                                "justify-content": "center",  
                                "align-items": "center",      
                                "width": "500px",             
                                "margin": "auto",
                                'marginTop': '5vh'             
                            }, color="info", inverse=True)], style={'margin-left': '10%', 'margin-right': '10%'})
        ],
        className="mb-3")
    ],justify='center')

], fluid=True)



about_layout=  html.Div([
    html.Label( 'About BackOrder Prediction Project', style={'textAlign': 'center', 'fontSize': 40,"font-weight": "400",'marginTop': '5vh'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Label( "This project revolves around the field of Computer Programs for Data Science and Artificial Intelligence at the Asian Institute of Technology. Its primary objective is to explore the domains of Data Science and Deployment, emphasizing the study and practical application of real-world data across various domains", style={'textAlign': 'justify', 'fontSize': 20,"font-weight": "200"}),
        html.Br(),
        html.Br(),
        html.Label("Developers: Sitthiwat D., Ashmita P.", style={'textAlign': 'center', 'fontSize': 20,"font-weight": "800"}),
        html.Br(),
        html.Br(),
        html.Label("GitHub Repository: ", style={'textAlign': 'center', 'fontSize': 20, 'fontWeight': '800'}),
        html.A("https://github.com/SitthiwatDam/BackOrderPrediction.git", href="https://github.com/SitthiwatDam/BackOrderPrediction.git", target="_blank", style={'textAlign': 'center', 'fontSize': 20, 'fontWeight': '800'}),
    ], style={'margin-left': '10%', 'margin-right': '10%', 'margin-bottom': '10vh'})
    
])


@callback(
    Output(component_id="backorder", component_property="children"),
    State(component_id='national_inv', component_property='value'),
    State(component_id='lead_time', component_property='value'),
    State(component_id='in_transit_qty', component_property='value'),
    State(component_id='sales_1_month', component_property='value'),
    State(component_id='sales_3_month', component_property='value'),
    State(component_id='sales_6_month', component_property='value'),
    State(component_id='sales_9_month', component_property='value'),
    State(component_id='min_bank', component_property='value'),
    State(component_id='potential_issue', component_property='value'),
    State(component_id='pieces_past_due', component_property='value'),
    State(component_id='perf_6_month_avg', component_property='value'),
    State(component_id='perf_12_month_avg', component_property='value'),
    State(component_id='local_bo_qty', component_property='value'),
    State(component_id='deck_risk', component_property='value'),
    State(component_id='oe_constraint', component_property='value'),
    State(component_id='ppap_risk', component_property='value'),
    State(component_id='stop_auto_buy', component_property='value'),
    State(component_id='rev_stop', component_property='value'),
    Input(component_id="SUBMIT", component_property='n_clicks'),
    
    prevent_initial_call=True
)


# Mapping the results
def Prediction(national_inv,lead_time,in_transit_qty,sales_1_month,sales_3_month,sales_6_month,sales_9_month,min_bank
               ,potential_issue,pieces_past_due,perf_6_month_avg,perf_12_month_avg,local_bo_qty,deck_risk,oe_constraint
               ,ppap_risk,stop_auto_buy,rev_stop,SUBMIT):
    # default values
    dict_default= {'national_inv': 77.0,
    'lead_time': 8.0,
    'in_transit_qty': 1.0,
    'sales_1_month': 9.0,
    'sales_3_month': 27.0,
    'sales_6_month': 67.0,
    'sales_9_month': 104.0,
    'min_bank': 18.0,
    'potential_issue': 'No',
    'pieces_past_due': 0.0,
    'perf_6_month_avg': 0.91,
    'perf_12_month_avg': 0.96,
    'local_bo_qty': 0.0,
    'deck_risk': 'No',
    'oe_constraint': 'No',
    'ppap_risk': 'No',
    'stop_auto_buy': 'Yes',
    'rev_stop': 'No'
    }
    single_sample = [national_inv,lead_time,in_transit_qty,sales_1_month,sales_3_month,sales_6_month,sales_9_month,min_bank,potential_issue,pieces_past_due,perf_6_month_avg,perf_12_month_avg,local_bo_qty,deck_risk,oe_constraint,ppap_risk,stop_auto_buy,rev_stop]
    # Replace None values with default values from dict_default
    for i in range(len(single_sample)):
        if single_sample[i] is None:
            single_sample[i] = dict_default[columns[i]]
    
    single_sample_df = pd.DataFrame([single_sample], columns=columns)
    result = loaded_pipeline.predict(single_sample_df)
    # Create the mapping
    mapping = {
    1: 'Yes, it will be a backorder.',
    0: "No, it won't be a backorder.",
    }
    # Map the price
    mapped_value = mapping.get(result[0], 'Unknown')
    return mapped_value

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050) # AWS server
    # app.run_server(debug=True) # dev
