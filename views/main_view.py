import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table


table_columns = ['School', 'EMIS number', 'Subdistrict', 'District', 'Total learners', 'Consent \u22659 years', 'First dose',
                 'Second dose', 'AEFI', 'Absent', 'Left school', 'Contra', 'Underage (<9 years)', 'Doses used', 'Doses wasted']
data_columns = ['school_name', 'emis_number', 'subdistrict_name', 'district_name', 'total_girl_learners', 'consent >=9', 'first_dose',
                'second_dose', 'aefi', 'absent', 'left', 'contra', 'underage', 'doses_used',
                'doses_wasted']

hpv_table_data = [{'name': ['', 'School'], 'id':'school_name'}, {'name': ['', 'EMIS'], 'id': 'emis_number'}, {'name': ['', 'Subdistrict name'], 'id': 'subdistrict_name'}, {'name': ['', 'District'], 'id': 'district_name'}, {'name': ['First dose', '9'], 'id':'first_dose_9'}, {'name': ['First dose', '10'], 'id':'first_dose_10'}, {'name': ['First dose', '11'], 'id':'first_dose_11'}, {'name': ['First dose', '12'], 'id':'first_dose_12'},
                         {'name': ['First dose', '13'], 'id':'first_dose_13'}, {'name': ['First dose', '14'], 'id':'first_dose_14'}, {'name': ['First dose', '\u226515'], 'id':'first_dose_15'},  {'name': [
                             'Second dose', '9'], 'id':'second_dose_9'}, {'name': ['Second dose', '10'], 'id':'second_dose_10'}, {'name': ['Second dose', '11'], 'id':'second_dose_11'}, {'name': ['Second dose', '12'], 'id':'second_dose_12'},
                         {'name': ['Second dose', '13'], 'id':'second_dose_13'}, {'name': ['Second dose', '14'], 'id':'second_dose_14'}, {'name': ['Second dose', '\u226515'], 'id':'second_dose_15'}]
main_table = zip(table_columns, data_columns)
textStyle = {'color': '#7FDBFF'}
headStyle = {'font-weight': 'bold'}
cards = {'display': 'inline-block', 'border-radius': '20px',
         'box-shadow': '0 0 3rem 1rem rgba(0,0,0,0,2'}
style_card = {'border-radius': '20px', 'box-shadow': '0 0 3rem 1rem rgba(0,0,0,0,2'}


date_picker = dcc.DatePickerRange(
    id='date_picker_range',
    calendar_orientation='horizontal',
    day_size=39,
    end_date_placeholder_text='Return',
    with_portal=False,
    first_day_of_week=0,
    reopen_calendar_on_clear=True,
    is_RTL=False,
    clearable=True,
    number_of_months_shown=1,
    display_format='DD MMM YYYY',
    month_format='MMMM, YYYY',
    minimum_nights=2,

    persistence=True,
    persisted_props=['start_date'],
    persistence_type='session',
    updatemode='singledate'
)


table_data = html.Div(
    [
        html.Div(
            [
                html.Br(),
                html.Div(id='date'),
                html.Br(),
                dash_table.DataTable(
                    id="table-schools",
                    columns=[{'name': c, 'id': i} for c, i in main_table],
                    page_size=10,
                    fixed_rows={'headers': True, 'data': 0},
                    style_cell={
                        'whiteSpace': 'normal', 'textAlign': 'left'},
                    sort_action='native',
                    filter_action='custom',
                    style_header={
                        'backgroundColor': 'rgb(0,0,255)',
                        'color': 'white'
                    },
                    filter_query='',
                    virtualization=True,
                    page_action='none',
                    style_data_conditional=[
                        {'if': {'column_id': 'school_name'},
                         'width': '60px'},
                        {'if': {'column_id': 'emis_number'},
                         'width': '40px'},
                        {'if': {'column_id': 'subdistrict_name'},
                         'width': '80px'},
                         {'if': {'column_id': 'district_name'},
                         'width': '80px'},
                         {'if': {'column_id': 'total_girl_learners'},
                         'width': '60px'},
                         {'if': {'column_id': 'consent >=9'},
                         'width': '80px'},
                         {'if': {'column_id': 'first_dose'},
                         'width': '80px'},
                         {'if': {'column_id':'second_dose'},
                          'width': '80px'},
                          {'if': {'column_id': 'aefi'},
                          'width': '40px'},
                          {'if': {'column_id': 'absent'},
                          'width': '40px'},
                          {'if': {'column_id': 'left'},
                           'width': '80px'},
                           {'if': {'column_id': 'contra'},
                           'width': '40px'},
                           {'if': {'column_id': 'underage'},
                           'width': '40px'},
                           {'if': {'column_id': 'doses_used'},
                            'width': '60px'},
                            {'if': {'column_id': 'doses_wasted'},
                            'width': '60px'},
                        
                    ],


                )
            ]
        )
    ]
)

hpv_table = html.Div(
    [
        html.Div(
            [
                html.Br(),
                html.Br(),
                dash_table.DataTable(
                    id="hpv",
                    columns=hpv_table_data,
                    page_size=10,
                    fixed_rows={'headers': True, 'data': 0},
                    style_cell={
                        'whiteSpace': 'normal', 'textAlign': 'left'},
                    sort_action='native',
                    filter_action='custom',
                    merge_duplicate_headers=True,
                    filter_query='',
                    virtualization=True,
                    style_header={
                        'backgroundColor': 'rgb(0,0,255)',
                        'color': 'white'
                    },
                    page_action='none',
                    style_data_conditional=[
                        {'if': {'column_id': 'school_name'},
                         'width': '80px'},
                        {'if': {'column_id': 'emis_number'},
                         'width': '40px'},
                        {'if': {'column_id': 'subdistrict_name'},
                         'width': '80px'},
                         {'if': {'column_id': 'district_name'},
                         'width': '80px'},
                         {'if': {'column_id': 'first_dose_9'},
                         'width': '40px'},
                         {'if': {'column_id': 'first_dose_10'},
                         'width': '40px'},
                         {'if': {'column_id': 'first_dose_11'},
                          'width': '40px'},
                          {'if': {'column_id': 'first_dose_12'},
                          'width': '40px'},
                          {'if': {'column_id': 'first_dose_13'},
                          'width': '40px'},
                          {'if': {'column_id': 'first_dose_14'},
                           'width': '40px'},
                           {'if': {'column_id': 'first_dose_15'},
                           'width': '50px'},
                         {'if': {'column_id': 'second_dose_9'},
                         'width': '40px'},
                         {'if': {'column_id': 'second_dose_10'},
                         'width': '40px'},
                         {'if': {'column_id': 'second_dose_11'},
                         'width': '40px'},
                         {'if': {'column_id': 'second_dose_12'},
                         'width': '40px'},
                         {'if': {'column_id': 'second_dose_13'},
                         'width': '40px'},
                         {'if': {'column_id': 'second_dose_14'},
                         'width': '40px'},
                         {'if': {'column_id': 'second_dose_15'},
                         'width': '40px'},
                    ],

                )
            ]
        )
    ]
)

table_card = html.Div([dbc.Card([table_data])])
hpv_table_card = html.Div([dbc.Card([hpv_table])])

main_left = html.Div(dbc.Card(
    [html.Br(), html.H6('Filter', style=headStyle), html.Br(), html.Br(), dbc.Card(date_picker, style={'height':'50vh'}), html.Br(),]))


seg1 = dbc.Row([dbc.Col(html.Div(main_left),width={'size': 3}), dbc.Col(table_card), dbc.Col(hpv_table_card)])


content = [html.Br(), seg1, html.Br()]