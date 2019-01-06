import os, sys
import time
import subprocess
import pickle
import signal
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
from config import *


# preparing for start
path = os.path.dirname(os.path.abspath(__file__))
# create folders if they aren't exists
if not os.path.exists('%s\\apps'%(path)):
    os.makedirs('%s\\apps'%(path))
    print('Add your .py scripts to directory %s and restart the ')
if not os.path.exists('%s\\log'%(path)):
    os.makedirs('%s\\log'%(path))


# prepare apps processes dict
apps = {}
for app_py in os.listdir('%s\\apps'%path):
    app = app_py[:-3]
    apps[app] = {
        'command': ['python', '%s\\apps\\%s'%(path, app_py)],
        'process': None,
    }
# create log files if they are not exists
for app in apps:
    if not os.path.isfile('%s\\log\\%s.log'%(path, app)):
        with open('%s\\log\\%s.log'%(path, app), 'w') as f:
            f.write('')
# kill pids from prev user session
if os.path.isfile('%s\\pid.pickle'%(path)):
    with open('%s\\pid.pickle'%(path), 'rb') as f:
        pid = pickle.load(f)
        for app in pid:
            try:
                os.kill(pid[app], signal.SIGILL)
            except:
                pass
# prepare new pid dict
pid = {}
for app in apps:
    pid[app] = None
with open('%s\\pid.pickle'%(path), 'wb') as f:
    pickle.dump(pid, f)

        



server = dash.Dash(__name__, external_stylesheets=external_stylesheets)
for css in external_css:
    server.css.append_css({"external_url": css})




def module_switcher_row(app, status_color=colors['paused']):
    global colors
    return html.Div([
        html.Div([
            html.P(app, style={'marginTop': '0.600em', 'marginLeft': '0.600em'}),
        ],
            className='eight columns',
            style={"background": status_color, 'margin': '1px', 'height': '37px', 'width': '60%'}
        ),
        html.Div([
            html.Button('', id=app+' start', n_clicks_timestamp='0',
                className=btns['start'],
                style={'verticalAlign': 'middle', 'padding': '12px', 'margin': '1px', "color": colors['font color']}),
            html.Button('', id=app+' pause', n_clicks_timestamp='0',
                className=btns['pause'],
                style={'verticalAlign': 'middle', 'padding': '12px', 'margin': '1px', "color": colors['font color']}),
            ],
            style={'verticalAlign': 'middle', 'margin': '1px', 'width': '30%'},
            className='four columns',
        ),

    ],
        style={'width': '100%'},
        className='row '
    )


def module_log_tab_children(app):
    return dcc.Tab(label=app, value=app, style=tab_style, selected_style=tab_selected_style)


def tab_df_children(tab_df):
    return dcc.Tab(label=tab_df, value=tab_df, style=tab_style, selected_style=tab_selected_style)


##### LAYOUT
server.layout = html.Div(
    [
        html.Div(
            [
                html.H2('Apps', style={"color": colors['font color'], 'marginLeft': '10px'}),
                html.Div(
                    [html.Div([module_switcher_row(app)]) for app in apps],
                    className='row ',
                    style={"color": colors['font color']},
                    id='live-update-running-status'
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=1000
                ),
                html.Div(id='container-button-timestamp-start'),
                html.Div(id='container-button-timestamp-pause'),
            ],
            style={"backgroundColor": colors['backgroundColor'], 'marginLeft': '20px', 'fontFamily': 'Sans-Serif', 'height': '450px'},
            className='three columns',
        ),
        html.Div(
            [
                html.H2('App logs', style={"color": colors['font color'], 'marginLeft': '10px'}),
                dcc.Tabs(
                    id="tabs-log",
                    value=list(apps.keys())[0],
                    children=[module_log_tab_children(app) for app in apps],
                    style=tabs_styles,
                ),
                html.Div(id='tabs-log-content', style={'height': '100%'}),
            ],
            className='nine columns',
            style={'height': '100%', 'fontFamily': 'Sans-Serif', 'display': 'block', 'overflow': 'auto'}
        ),
    ],
    style={"background-color": colors['backgroundColor'], 'height': '100%', 'fontFamily': 'Sans-Serif'},
    className='row '
)



##### CALLBACKS
@server.callback(Output('live-update-running-status', 'children'),
                 events=[Event('interval-component', 'interval') for app in apps],
)
def check_if_module_is_running():
    output = []
    for app in apps:
        try:
            if apps[app]['process'].poll() is None:
                output.append(module_switcher_row(app, status_color=colors['running']))
            else:
                output.append(module_switcher_row(app, status_color=colors['paused']))
        except:
            try:
                os.kill(apps[app]['pid'], 0)
                output.append(module_switcher_row(app, status_color=colors['running']))
            except:
                output.append(module_switcher_row(app, status_color=colors['paused']))
    return output
    

@server.callback(
    dash.dependencies.Output('container-button-timestamp-start', 'children'),
    [dash.dependencies.Input(app+' start', 'n_clicks_timestamp') for app in apps],
)
def start(*args):
    args = [int(x) for x in args]
    if sum(args) > 0:
        i = args.index(max([int(x) for x in args]))
        app = list(apps.keys())[i]
        if not (apps[app]['process'] is not None and apps[app]['process'].poll() is None):
            
            apps[app]['process'] = subprocess.Popen(apps[app]['command'])
            pid[app] = apps[app]['process'].pid
            # save pid to pickle
            with open('%s\\pid.pickle'%(path), 'wb') as f:
                pickle.dump(pid, f)
            print(app+' start', pid[app])
        else:
            print('Already started: %s %s'%(app, pid[app]))


@server.callback(
    dash.dependencies.Output('container-button-timestamp-pause', 'children'),
    [dash.dependencies.Input(app+' pause', 'n_clicks_timestamp') for app in apps],
)
def pause(*args):
    global apps
    global pid
    args = [int(x) for x in args]
    if sum(args) > 0:
        i = args.index(max([int(x) for x in args]))
        app = list(apps.keys())[i]
        #apps[app]['process'].kill()
        try:
            os.kill(pid[app], signal.SIGILL)
            print(app+' pause', pid[app])
            apps[app]['pid'] = None
        except:
            print(sys.exc_info()[1])
        with open('%s\\pid.pickle'%(path), 'wb') as f:
            pickle.dump(pid, f)
        


@server.callback(Output('tabs-log-content', 'children'),
              [Input('tabs-log', 'value')])
def render_content(tab):
    global colors
    with open('%s\\log\\%s.log'%(path, tab), 'r') as f:
        log = f.read()
    return dcc.Textarea(
        contentEditable=False,
        value=log,
        style={'width': '100%', 'height': '700px', 'bottom':0., 'color': colors['font color'], 'marginBottom': '500px'}
    )




if __name__ == '__main__':
    server.run_server(host='localhost', port=5000, debug=True)
    #server.run_server() # deploy



