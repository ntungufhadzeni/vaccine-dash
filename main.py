from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import current_user

from app import app, server
from data import Data
from views import login, dashboard, profile, error, admin
from datetime import datetime


app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        dcc.Interval(
            id='interval',
            disabled=False,
            interval=60 * 60 * 1000,
            n_intervals=0),
        html.Div(id='page-content')
    ], style={'padding': '10px 10px 10px 10px'}
)

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/dashboard':
        if current_user.is_authenticated:
            return dashboard.layout
        else:
            return login.layout
    elif pathname == '/profile':
        if current_user.is_authenticated:
            return profile.layout
        else:
            return login.layout
    elif pathname == '/admin':
        if current_user.is_authenticated:
            if current_user.is_admin:
                return admin.layout
            else:
                return error.layout
        else:
            return login.layout
    else:
        return error.layout



@app.callback(
    [Output('date_picker_range', 'min_date_allowed'),
     Output('date_picker_range', 'max_date_allowed'),
     Output('date_picker_range', 'initial_visible_month'),
     Output('date_picker_range', 'start_date'),
     Output('date_picker_range', 'end_date')],
    Input('interval', 'n_intervals')
)
def update_date_picker(n):
    return datetime(2023, 1, 1).date(), datetime.now().date(), datetime.now().date(), datetime(2023, 1, 1).date(), datetime.now().date()


@app.callback(
    Output('table-schools', 'data'),
    [Input('table-schools', 'filter_query'),
    Input('date_picker_range', 'start_date'),
     Input('date_picker_range', 'end_date'),
    Input('interval', 'n_intervals')]
)
def update_data_table(filter,start_date, end_date, n):
    data = Data(start_date, end_date)
    df = data.data

    filtering_expressions = filter.split(' && ')
    dff = df

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.lower().str.contains(filter_value.lower())]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')


@app.callback(
    Output('hpv', 'data'),
    [Input('hpv', 'filter_query'),
    Input('date_picker_range', 'start_date'),
     Input('date_picker_range', 'end_date'),
    Input('interval', 'n_intervals')]
)
def update_first_dose_table(filter, start_date, end_date, n):
    data = Data(start_date, end_date)
    df = data.data

    filtering_expressions = filter.split(' && ')
    dff = df

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.lower().str.contains(filter_value.lower())]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')


@app.callback(
    Output('date', 'children'),
    [Input('interval', 'n_intervals'),
     Input('date_picker_range', 'start_date'),
     Input('date_picker_range', 'end_date')]
)
def update_stats(n, start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d %B %Y')
    end = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d %B %Y')
    return html.P(f'Start date: {start}, End date: {end}')


if __name__ == '__main__':
    app.run_server()