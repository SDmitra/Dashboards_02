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
    ar = pd.read_csv('ARCHIVE.csv',encoding='cp1251',sep=';')
    org = pd.read_csv('org.csv',encoding='cp1251',sep=';')
    ds = pd.read_csv('ds.csv',encoding='cp1251',sep=';')
    gp = pd.read_csv('gp.csv',encoding='cp1251',sep=';')

    dc_metric_fullname_rus = 'dc_metric_fullname_rus'
    org_be_fullname_rus = 'org_be_fullname_rus'
    org_sp_rank_mixname_rus = 'org_sp_rank_mixname_rus'
    gp_group_rank_shortname_rus = 'gp_group_rank_shortname_rus'
    date_dataframe = 'date_dataframe'
    gp_sp_rank_mixname_rus = 'gp_sp_rank_mixname_rus'
    gp_subgroup_rank_shortname_rus = 'gp_subgroup_rank_shortname_rus'
    date_1 = 'date_1'

    ar[date_dataframe] = pd.to_datetime(ar[date_dataframe], format="%d.%m.%Y")
    ar[date_1] = pd.to_datetime(ar[date_1], format="%d.%m.%Y")

    selected_product_08 = "8.Просроченные заказы ТОРО"

    def dates_slider_00():
        startDateSep = [pd.to_datetime(ar[date_dataframe]).min().year,pd.to_datetime(ar[date_dataframe]).min().month,pd.to_datetime(ar[date_dataframe]).min().day]
        endDateSep = [pd.to_datetime(ar[date_dataframe]).max().year,pd.to_datetime(ar[date_dataframe]).max().month,pd.to_datetime(ar[date_dataframe]).max().day]

        dates_slider = st.sidebar.slider(
            "Диапазон слепков (включительно)",
            min_value = datetime(startDateSep[0],startDateSep[1],startDateSep[2]),
            max_value = datetime(endDateSep[0],endDateSep[1],endDateSep[2]),
            value=(datetime(startDateSep[0],startDateSep[1],startDateSep[2]),datetime(endDateSep[0],endDateSep[1],endDateSep[2])),
            format="DD.MM.YYYY")

        dates_diapazon = ar[(ar[date_dataframe] >= dates_slider[0]) & (ar[date_dataframe] <= dates_slider[1])][date_dataframe].unique().tolist()
        dates_diapazon_formatted = [date.strftime("%d.%m.%Y") for date in dates_diapazon]
        dates_diapazon_datetime = [datetime.strptime(date, "%d.%m.%Y") for date in dates_diapazon_formatted]
        sorted_dates_diapazon = sorted(dates_diapazon_datetime)  # Сортировка дат по возрастанию
        sorted_dates_diapazon_formatted = [date.strftime("%d.%m.%Y") for date in sorted_dates_diapazon]
        dates_choose = st.sidebar.multiselect('Выберите целевые даты слепков', ['Все'] + sorted_dates_diapazon_formatted, placeholder = 'Выберите даты, если это необходимо')
        return(dates_choose)
    
    def selected_be_00():
        selected_be = st.sidebar.multiselect(
            "Выберите балансовую единицу",
            ['Все'] + list(org[org_be_fullname_rus].unique()),
            default=['Все'],
        )
        return(selected_be)
    
    def selected_sp_00(selected_bes):
        filtered_sp = org[org[org_be_fullname_rus].isin(selected_bes)][org_sp_rank_mixname_rus].unique()
        selected_sp = st.sidebar.multiselect(
            "Выберите структурное подразделение",
            ['Все'] + list(filtered_sp),
            default=['Все']
        )
        return(selected_sp)
    
    def selected_gp_08(selected_sps):
        filtered_gp = gp[gp[gp_sp_rank_mixname_rus].isin(selected_sps)][gp_group_rank_shortname_rus].unique()
        selected_gp = st.sidebar.multiselect(
            "Выберите ФЦО",
            ['Все'] + list(filtered_gp),
            default=['Все']
        )
        return(selected_gp)
    
    def selected_subgp_08(selected_gps):                
        filtered_subgp = gp[gp[gp_group_rank_shortname_rus].isin(selected_gps)][gp_subgroup_rank_shortname_rus].unique()
        selected_subgp = st.sidebar.multiselect(
            "Выберите группу плановиков",
            ['Все'] + list(filtered_subgp),
            default=['Все']
        )
        return(selected_subgp)
    
    def format_date(date):
        return date.strftime("%d.%m.%Y")
    

    def dates_slider_08(buttonBSK):
        startDateBSK = [pd.to_datetime(ar[date_1]).min().year,pd.to_datetime(ar[date_1]).min().month,pd.to_datetime(ar[date_1]).min().day]
        endDateBSK = [pd.to_datetime(ar[date_1]).max().year,pd.to_datetime(ar[date_1]).max().month,pd.to_datetime(ar[date_1]).max().day]
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

    def metric_08_01(dates_chooses_00,selected_bes,selected_sps,selected_gps,selected_subgps):
        buttonBSK = st.sidebar.radio("Выберите даты БСК",["В прошлых годах", "В этом году", "Сбросить"], index=2)
        datesBSK_chooses = dates_slider_08(buttonBSK)


        df_main = pd.merge(ar, org, on='org_sp_kod', how="left")
        df_main = pd.merge(df_main, gp, on='org_sp_kod', how = "left")

        df_main = df_main[
        (pd.to_datetime(df_main[date_1], format="%d.%m.%Y") >= datesBSK_chooses[0]) &
        (pd.to_datetime(df_main[date_1], format="%d.%m.%Y") <= datesBSK_chooses[1])
        ]

        if 'Все' in selected_bes:
            df_main_pivot_table1 = pd.pivot_table(df_main,
                                        values = 'number_1',
                                        index = org_be_fullname_rus,
                                        columns = 'date_dataframe', 
                                        aggfunc = 'sum')
        if 'Все' not in selected_bes:
            df_main = df_main[df_main['org_be_fullname_rus'].isin(selected_bes)]
            df_main_pivot_table1 = pd.pivot_table(df_main,
                                        values = 'number_1',
                                        index = org_sp_rank_mixname_rus,
                                        columns = 'date_dataframe', 
                                        aggfunc = 'sum')
            if 'Все' not in selected_sps:
                df_main = df_main[df_main[org_sp_rank_mixname_rus].isin(selected_sps)]
                df_main_pivot_table1 = pd.pivot_table(df_main,
                                            values = 'number_1',
                                            index = org_sp_rank_mixname_rus,
                                            columns = 'date_dataframe', 
                                            aggfunc = 'sum')
                if 'Все' not in selected_gps:
                    df_main = df_main[df_main[gp_group_rank_shortname_rus].isin(selected_gps)]
                    df_main_pivot_table1 = pd.pivot_table(df_main,
                                                values = 'number_1',
                                                index = gp_group_rank_shortname_rus,
                                                columns = 'date_dataframe', 
                                                aggfunc = 'sum')
                    if 'Все' not in selected_subgps:
                        df_main = df_main[df_main[gp_subgroup_rank_shortname_rus].isin(selected_subgps)]
                        df_main_pivot_table1 = pd.pivot_table(df_main,
                                                    values = 'number_1',
                                                    index = gp_subgroup_rank_shortname_rus,
                                                    columns = 'date_dataframe', 
                                                    aggfunc = 'sum')
            
        df_main_pivot_table1 = df_main_pivot_table1.rename(columns=lambda x: x.strftime('%d.%m.%Y'))
        if dates_chooses_00 != []:
            df_main_pivot_table1_filtered = df_main_pivot_table1.loc[:, df_main_pivot_table1.columns.isin(dates_chooses_00)]
            metric_main_01(df_main_pivot_table1_filtered)
        if dates_chooses_00 == []:
            metric_main_01(df_main_pivot_table1)

    #Интерфейс отчетов
    def metric_main_01(df_main_pivot_table1, dates_chooses_00):
        st.header(selected_product, divider='blue')

        if not dates_chooses_00:
            st.warning("Выберите даты для расчета разницы.")
            st.dataframe(df_main_pivot_table1)
            return

        date_columns = df_main_pivot_table1.columns
        selected_dates = [date for date in date_columns if date in dates_chooses_00]

        if not selected_dates:
            st.warning("Нет данных для выбранных дат.")
            st.dataframe(df_main_pivot_table1)
            return

        # Find the indices of min and max dates
        min_date = min(selected_dates)
        max_date = max(selected_dates)
        min_index = date_columns.get_loc(min_date)
        max_index = date_columns.get_loc(max_date)

        # Calculate the difference between values for min and max dates
        differences = df_main_pivot_table1.iloc[:, max_index] - df_main_pivot_table1.iloc[:, min_index]
        differences.name = "Разница между датами {} и {}".format(min_date, max_date)

        # Add the differences as a new column to the DataFrame
        df_main_pivot_table1_with_difference = pd.concat([df_main_pivot_table1, differences], axis=1)

        st.subheader("Разница между датами {} и {}:".format(min_date, max_date))
        st.dataframe(df_main_pivot_table1_with_difference)


    #Интерфейс фильтров
    selected_product = st.sidebar.selectbox("Выберите метрику", ["Все"] + list(ds[dc_metric_fullname_rus].unique()), index=1)
    st.sidebar.header("Общие фильтры метрик")
    dates_chooses_00 = dates_slider_00()
    selected_bes = selected_be_00()
    selected_sps = []
    selected_gps = []
    selected_subgps = []
    datesBSK_chooses = []
    if 'Все' not in selected_bes:  # Изменение условия
        selected_sps = selected_sp_00(selected_bes)
        if 'Все' not in selected_sps and selected_product == selected_product_08:  # Метрика 8
            st.sidebar.header("Фильтры метрики: '" + selected_product + "'")
            selected_gps = selected_gp_08(selected_sps)
            if 'Все' not in selected_gps:  # Изменение условия
                selected_subgps = selected_subgp_08(selected_gps)

    if selected_product == selected_product_08:  # Метрика 8
        metric_08_01(dates_chooses_00,selected_bes,selected_sps,selected_gps,selected_subgps)

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv_bytes = convert_df(ar)

    st.sidebar.download_button(
        label="Экспорт в CSV",
        data=csv_bytes,
        file_name='export' + ".csv",
        mime='csv',
    )

# Run the app
if __name__ == "__main__":
    main()

