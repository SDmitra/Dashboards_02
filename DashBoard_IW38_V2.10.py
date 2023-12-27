def main():
    import matplotlib.pyplot as plt
    import streamlit as st
    import pandas as pd
    from datetime import datetime, timedelta
    import seaborn as sns
    import numpy as np
    import plotly.express as px

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.set_page_config(page_title="Отчет для сервиса НН", page_icon=":bar_chart:",layout="wide")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
    
    # Загрузка файла
    
    ar = pd.read_csv('ar.csv',encoding='cp1251',sep=';')
    ds = pd.read_csv('ds.csv',encoding='cp1251',sep=';')
    be = pd.read_csv('be.csv',encoding='cp1251',sep=';')
    sp = pd.read_csv('sp.csv',encoding='cp1251',sep=';')
    gp = pd.read_csv('gp.csv',encoding='cp1251',sep=';')
    
    merged_ar = pd.merge(ar, sp, on='org_sp_kod', how='left')
    merged_ar = pd.merge(merged_ar, gp, on='gp_kod', how='left')
    merged_ar = pd.merge(merged_ar, be, on='org_be_kod', how='left')

    dc_metric_fullname_rus = 'dc_metric_fullname_rus'
    org_be_fullname_rus = 'org_be_fullname_rus'
    org_sp_rank_mixname_rus = 'org_sp_rank_mixname_rus'
    org_be_kod = 'org_be_kod'
    gp_group_rank_shortname_rus = 'gp_group_rank_shortname_rus'
    date_dataframe = 'date_dataframe'
    gp_sp_rank_mixname_rus = 'gp_sp_rank_mixname_rus'
    gp_subgroup_rank_shortname_rus = 'gp_subgroup_rank_shortname_rus'
    date_1 = 'date_1'

    merged_ar[date_dataframe] = pd.to_datetime(merged_ar[date_dataframe], format="%d.%m.%Y")
    merged_ar[date_1] = pd.to_datetime(merged_ar[date_1], format="%d.%m.%Y")

    selected_product_08 = "8.Просроченные заказы ТОРО"


    def dates_slider_00():
        startDateSep = [pd.to_datetime(merged_ar[date_dataframe]).min().year,pd.to_datetime(merged_ar[date_dataframe]).min().month,pd.to_datetime(merged_ar[date_dataframe]).min().day]
        endDateSep = [pd.to_datetime(merged_ar[date_dataframe]).max().year,pd.to_datetime(merged_ar[date_dataframe]).max().month,pd.to_datetime(merged_ar[date_dataframe]).max().day]

        dates_slider = st.sidebar.slider(
            "Диапазон слепков (включительно)",
            min_value = datetime(startDateSep[0],startDateSep[1],startDateSep[2]),
            max_value = datetime(endDateSep[0],endDateSep[1],endDateSep[2]),
            value=(datetime(startDateSep[0],startDateSep[1],startDateSep[2]),datetime(endDateSep[0],endDateSep[1],endDateSep[2])),
            format="DD.MM.YYYY")

        dates_diapazon = merged_ar[(merged_ar[date_dataframe] >= dates_slider[0]) & (merged_ar[date_dataframe] <= dates_slider[1])][date_dataframe].unique().tolist()
        dates_diapazon_formatted = [date.strftime("%d.%m.%Y") for date in dates_diapazon]
        dates_diapazon_datetime = [datetime.strptime(date, "%d.%m.%Y") for date in dates_diapazon_formatted]
        sorted_dates_diapazon = sorted(dates_diapazon_datetime)  # Сортировка дат по возрастанию
        sorted_dates_diapazon_formatted = [date.strftime("%d.%m.%Y") for date in sorted_dates_diapazon]
        dates_choose = st.sidebar.multiselect('Выберите целевые даты слепков', ['Все'] + sorted_dates_diapazon_formatted, placeholder = 'Выберите даты, если это необходимо')
        return(dates_choose)
    
    def selected_be_00():
        selected_be = st.sidebar.multiselect(
            "Выберите балансовую единицу",
            ['Все'] + list(be[org_be_fullname_rus].unique()),
            default=['Все'],
        )
        if 'Все' in selected_be:
            return(selected_be)
        else:
            selected_be = be.loc[be['org_be_fullname_rus'].isin(selected_be), 'org_be_kod'].tolist()
            return(selected_be)
    
    def selected_sp_00(selected_bes):
        filtered_sp = sp[sp[org_be_kod].isin(selected_bes)][org_sp_rank_mixname_rus].unique()
        selected_sp = st.sidebar.multiselect(
            "Выберите структурное подразделение",
            ['Все'] + list(filtered_sp),
            default=['Все']
        )
        if 'Все' in selected_sp:
            return(selected_sp)
        else:
            selected_sp = sp.loc[sp['org_sp_rank_mixname_rus'].isin(selected_sp), 'org_sp_kod'].tolist()
            return(selected_sp)
    
    def selected_plsp_00(selected_sps):
        selected_plsp = sp.loc[sp['org_sp_kod'].isin(selected_sps), 'gp_plansp_kod'].tolist()
        return(selected_plsp)
    
    def selected_fco_08(selected_plsps):
        filtered_fco = gp[gp['gp_plansp_kod'].isin(selected_plsps)][gp_group_rank_shortname_rus].unique()
        selected_fco = st.sidebar.multiselect(
            "Выберите ФЦО",
            ['Все'] + list(filtered_fco),
            default=['Все']
        )
        if 'Все' in selected_fco:
            return(selected_fco)
        else:
            selected_fco = gp.loc[gp['gp_group_rank_shortname_rus'].isin(selected_fco), 'gp_kod'].tolist()
            return(selected_fco)
    
    def selected_gp_08(selected_fco):                
        filtered_gp = gp[gp['gp_kod'].isin(selected_fco)][gp_subgroup_rank_shortname_rus].unique()
        selected_gp = st.sidebar.multiselect(
            "Выберите группу плановиков",
            ['Все'] + list(filtered_gp),
            default=['Все']
        )
        if 'Все' in selected_gp:
            return(selected_gp)
        else:
            selected_gp = gp.loc[gp['gp_subgroup_rank_shortname_rus'].isin(selected_gp), 'gp_kod'].tolist()
            return(selected_gp)
    

    def dates_slider_08(buttonBSK):
        startDateBSK = [pd.to_datetime(merged_ar[date_1]).min().year,pd.to_datetime(merged_ar[date_1]).min().month,pd.to_datetime(merged_ar[date_1]).min().day]
        endDateBSK = [pd.to_datetime(merged_ar[date_1]).max().year,pd.to_datetime(merged_ar[date_1]).max().month,pd.to_datetime(merged_ar[date_1]).max().day]
        if buttonBSK =='В прошлых годах':
            datesBSK = st.sidebar.slider(
                "Даты базисного срока конца (включительно)",
                min_value = datetime(startDateBSK[0], startDateBSK[1], startDateBSK[2]),
                max_value = datetime(endDateBSK[0], endDateBSK[1], endDateBSK[2]),
                value=(datetime(startDateBSK[0], startDateBSK[1], startDateBSK[2]),datetime(2022,12,31)),
                format="DD.MM.YYYY")
        elif buttonBSK == 'В этом году':
            datesBSK = st.sidebar.slider(
                "Даты базисного срока конца (включительно)",
                min_value = datetime(startDateBSK[0], startDateBSK[1], startDateBSK[2]),
                max_value = datetime(endDateBSK[0], endDateBSK[1], endDateBSK[2]),
                value=(datetime(2023,1,1),datetime(2023,12,31)),
                format="DD.MM.YYYY")
        elif buttonBSK == 'Сбросить':
            datesBSK = st.sidebar.slider(
                "Даты базисного срока конца (включительно)",
                min_value = datetime(startDateBSK[0], startDateBSK[1], startDateBSK[2]),
                max_value = datetime(endDateBSK[0], endDateBSK[1], endDateBSK[2]),
                value=(datetime(startDateBSK[0], startDateBSK[1], startDateBSK[2]),datetime(endDateBSK[0], endDateBSK[1], endDateBSK[2])),
                format="DD.MM.YYYY")
        return (datesBSK)

    def metric_08_01(dates_chooses_00, selected_bes, selected_sps, selected_fcos, selected_gps):
        buttonBSK = st.sidebar.radio("Выберите даты БСК",["В прошлых годах", "В этом году", "Сбросить"], index=2)
        datesBSK_chooses = dates_slider_08(buttonBSK)

        
        df_main = pd.merge(ar, sp, on='org_sp_kod', how="right")
        df_main = pd.merge(df_main, gp, on='gp_kod', how="right")
        df_main = pd.merge(df_main, be, on='org_be_kod', how="right")


        df_main = df_main[
            (pd.to_datetime(df_main[date_1], format="%d.%m.%Y") >= datesBSK_chooses[0]) &
            (pd.to_datetime(df_main[date_1], format="%d.%m.%Y") <= datesBSK_chooses[1])
        ]
        if 'Все' in selected_bes:
            #st.dataframe(df_main)
            df_main_pivot_table1 = pd.pivot_table(df_main,
                                                values='number_1',
                                                index=org_be_fullname_rus,
                                                columns='date_dataframe',
                                                aggfunc='sum')
            
            grouped_data = merged_ar.groupby([date_dataframe, 
                                              org_be_fullname_rus])['number_1'].sum().reset_index()
            level = org_be_fullname_rus
            level_name = "Балансовая единица"


        if 'Все' not in selected_bes:
            df_main = df_main[df_main[org_be_kod].isin(selected_bes)]
            df_main_pivot_table1 = pd.pivot_table(df_main,
                                                values='number_1',
                                                index=org_sp_rank_mixname_rus,
                                                columns='date_dataframe',
                                                aggfunc='sum')
            
            grouped_data = merged_ar[merged_ar[org_be_kod].isin(selected_bes)]
            grouped_data = grouped_data.groupby([date_dataframe, 
                                              org_sp_rank_mixname_rus])['number_1'].sum().reset_index()
            level = org_sp_rank_mixname_rus
            level_name = "Балансовая единица"
            #print(df_main_pivot_table1)
            #print(grouped_data)

            if 'Все' not in selected_sps:
                df_main = df_main[df_main['org_sp_kod'].isin(selected_sps)]
                df_main_pivot_table1 = pd.pivot_table(df_main,
                                                    values='number_1',
                                                    index=org_sp_rank_mixname_rus,
                                                    columns='date_dataframe',
                                                    aggfunc='sum')
                
                grouped_data = merged_ar[merged_ar['org_sp_kod'].isin(selected_sps)]
                grouped_data = grouped_data.groupby([date_dataframe, 
                                                org_sp_rank_mixname_rus])['number_1'].sum().reset_index()
                level = org_sp_rank_mixname_rus
                level_name = "Структурное подразделение"
                #print(df_main_pivot_table1)
                #print(grouped_data)

                if 'Все' not in selected_fcos:
                    df_main = df_main[df_main['gp_kod'].isin(selected_fcos)]
                    df_main_pivot_table1 = pd.pivot_table(df_main,
                                                        values='number_1',
                                                        index=gp_group_rank_shortname_rus,
                                                        columns='date_dataframe',
                                                        aggfunc='sum')
                    
                    grouped_data = merged_ar[merged_ar['gp_kod'].isin(selected_fcos)]
                    grouped_data = grouped_data.groupby([date_dataframe, 
                                                    gp_group_rank_shortname_rus])['number_1'].sum().reset_index()
                    level = gp_group_rank_shortname_rus
                    level_name = "ФЦО"
                    if 'Все' not in selected_gps:
                        df_main = df_main[df_main['gp_kod'].isin(selected_gps)]
                        df_main_pivot_table1 = pd.pivot_table(df_main,
                                                            values='number_1',
                                                            index=gp_subgroup_rank_shortname_rus,
                                                            columns='date_dataframe',
                                                            aggfunc='sum')
                        grouped_data = merged_ar[merged_ar['gp_kod'].isin(selected_gps)]
                        grouped_data = grouped_data.groupby([date_dataframe, 
                                                             gp_subgroup_rank_shortname_rus])['number_1'].sum().reset_index()
                        level = gp_subgroup_rank_shortname_rus
                        level_name = "Группа плановиков"

        #df_main_pivot_table1 = df_main_pivot_table1.rename(columns=lambda x: x.strftime('%d.%m.%Y'))
        #df_main_pivot_table1.columns = pd.to_datetime(df_main_pivot_table1.columns, format='%d.%m.%Y')
        df_main_pivot_table1 = df_main_pivot_table1.reindex(sorted(df_main_pivot_table1.columns, key=lambda x: pd.to_datetime(x, format='%d.%m.%Y')), axis=1)
        if dates_chooses_00 != []:
            df_main_pivot_table1 = df_main_pivot_table1.loc[:, df_main_pivot_table1.columns.isin(dates_chooses_00)]
            #print(df_main_pivot_table1)
            metric_main_01(df_main_pivot_table1, dates_chooses_00, grouped_data, level, level_name, df_main)
        if dates_chooses_00 == []:
            metric_main_01(df_main_pivot_table1, dates_chooses_00,grouped_data,level,level_name,df_main)
            







    def metric_main_01(df_main_pivot_table1, dates_chooses_00, grouped_data, level, level_name, df_main):
        #print(df_main_pivot_table1)
        #print(dates_chooses_00)
        #print(grouped_data)
        #print(level)
        #print(level_name)
        #print(df_main)

        st.header(selected_product_08, divider='blue')

        if not dates_chooses_00:
            st.warning("Выберите даты для расчета разницы.")
            st.dataframe(df_main_pivot_table1)
            return

        date_columns = df_main_pivot_table1.columns

        # Convert date columns to datetime format
        date_columns_datetime = pd.to_datetime(date_columns, format='%d.%m.%Y', errors='coerce')

        # Filter selected dates that are present in the DataFrame
        selected_dates = [date.strftime('%d.%m.%Y') for date in date_columns_datetime if date.strftime('%d.%m.%Y') in dates_chooses_00]

        if not selected_dates:
            st.warning("Нет данных для выбранных дат.")
            st.dataframe(df_main_pivot_table1)
            return
        
        # Find the indices of min and max dates
        min_date = min(selected_dates, key=lambda x: datetime.strptime(x, "%d.%m.%Y"))
        max_date = max(selected_dates, key=lambda x: datetime.strptime(x, "%d.%m.%Y"))
        min_index = date_columns.get_loc(min_date)
        max_index = date_columns.get_loc(max_date)

        # Calculate the difference between values for min and max dates
        differences = df_main_pivot_table1.iloc[:, max_index] - df_main_pivot_table1.iloc[:, min_index]
        differences.name = "Разница {} и {}".format(min_date, max_date)

        # Add the differences as a new column to the DataFrame
        df_main_pivot_table1_with_difference = pd.concat([df_main_pivot_table1, differences], axis=1)
        def format_number(x):
            if isinstance(x, (int, float)):
                return '{:,.0f}'.format(x).replace(',', ' ')
            return str(x)

        df_main_pivot_table1_with_difference = pd.concat([df_main_pivot_table1, differences], axis=1)
        df_styled = df_main_pivot_table1_with_difference.style.applymap(
            lambda x: 'background-color: #ff6666' if x > 0 else 'background-color: #99ff99', subset=[differences.name]
        ).format(format_number)
        st.dataframe(df_styled)

        filtered_grouped_data = grouped_data[grouped_data[date_dataframe].isin(selected_dates)]
        filtered_grouped_data[date_dataframe] = pd.to_datetime(filtered_grouped_data[date_dataframe], format="%d.%m.%Y")
        filtered_grouped_data = filtered_grouped_data.sort_values(by=date_dataframe)
        print(filtered_grouped_data)
        cols1 = st.columns(2)
        with cols1[0]:
            fig1 = px.line(filtered_grouped_data, x=date_dataframe, y='number_1', color=level,
                        title='График количества заказов', labels={date_dataframe: 'Дата', 'number_1': 'Количество заказов'},
                        line_group=level, markers = True)
            fig1.update_layout(
                xaxis_title='Дата',
                yaxis_title='Количество заказов',
                legend_title=level_name,
                xaxis=dict(type='date', tickformat='%d.%m.%Y')
            )
            st.plotly_chart(fig1)


        #ДЛЯ ГРАФИКА
        
        zakr_status = ['ТЗКР', 'ЗАКР', 'ОТМЕ']
        def check_order_status(row):
            if row['date_1'] < row['date_dataframe'] and row['text_2'] in zakr_status:
                return "1. Заказ закрыт"
            elif row['date_1'] < row['date_dataframe'] and row['text_2'] not in zakr_status:
                return "3. Заказ просрочен"
            elif row['date_1'] > row['date_dataframe'] and row['text_2'] not in zakr_status:
                return "4. Заказ актуален"
            else:
                return "2. Заказ закрыт в будущем"
        # Добавление нового столбца с помощью apply и функции check_order_status
        df_main[date_dataframe] = pd.to_datetime(df_main[date_dataframe], format="%d.%m.%Y")
        df_main[date_1] = pd.to_datetime(df_main[date_1], format="%d.%m.%Y")

        df_main['order_status'] = df_main.apply(check_order_status, axis=1)

        with cols1[1]:
            #ГРАФИК

            grouped_data_zkz = df_main.groupby(['date_dataframe', level,'order_status'])['number_1'].sum().reset_index()
            grouped_data_zkz = grouped_data_zkz[grouped_data_zkz['date_dataframe'] == max_date]
            fig2 = px.bar(grouped_data_zkz, x=level, y='number_1', color='order_status',
                                    title='График количества типов заказов', labels={level: level_name, 'order_status': 'Количество заказов'})
            fig2.update_layout(
                xaxis_title='СП',
                yaxis_title='Заказы',
                legend_title='Тип заказа'
            )

            # Визуализация
            st.plotly_chart(fig2)


        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv_bytes = convert_df(df_main)

        st.sidebar.download_button(
            label="Экспорт в CSV",
            data=csv_bytes,
            file_name='export' + ".csv",
            mime='csv',
        )









    #Интерфейс фильтров
    selected_product = st.sidebar.selectbox("Выберите метрику", ["Все"] + list(ds[dc_metric_fullname_rus].unique()), index=1)
    st.sidebar.header("Общие фильтры метрик")
    dates_chooses_00 = dates_slider_00()
    selected_bes = selected_be_00()
    selected_sps = []
    selected_fcos = []
    selected_gps = []

    if 'Все' not in selected_bes:  # Изменение условия
        selected_sps = selected_sp_00(selected_bes)
        selected_plsps = selected_plsp_00(selected_sps)
        if 'Все' not in selected_sps and selected_product == selected_product_08:  # Метрика 8
            st.sidebar.header("Орг. фильтры метрики: '" + selected_product + "'")
            selected_fcos = selected_fco_08(selected_plsps)
            if 'Все' not in selected_fcos:  # Изменение условия
                selected_gps = selected_gp_08(selected_fcos)
                #if 'Все' not in selected_gps:  # Изменение условия
                    
                
    if selected_product == selected_product_08:  # Метрика 8
        st.sidebar.header("Даты фильтры метрики: '" + selected_product + "'")
        metric_08_01(dates_chooses_00,selected_bes,selected_sps,selected_fcos,selected_gps)

# Run the app
if __name__ == "__main__":
    main()

