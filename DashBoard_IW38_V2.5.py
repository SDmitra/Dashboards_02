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
    endex = []

    ar['date_dataframe'] = pd.to_datetime(ar['date_dataframe'], format="%d.%m.%Y")
    ar['date_1'] = pd.to_datetime(ar['date_1'], format="%d.%m.%Y")

    startDate = pd.to_datetime(ar["date_dataframe"]).min()
    endDate = pd.to_datetime(ar["date_dataframe"]).max()
    startDateBSK = pd.to_datetime(ar["date_1"]).min()
    endDateBSK = pd.to_datetime(ar["date_1"]).max()

    # Получаем текущую дату
    current_date = datetime.now()
    # Получаем последний день текущего года
    last_day_of_current_year = datetime(current_date.year, 12, 31)
    # Получаем последний день прошлого года
    last_day_of_previous_year = last_day_of_current_year - timedelta(days=365)
    # Выводим последний день прошлого года
    #print(last_day_of_previous_year)
    
    #st.header("Демоверсия отчетов для сервиса: ")
    st.sidebar.header("Фильтры отчетов",)
    selected_be = st.sidebar.selectbox("Выберите балансовую единицу", ['Все'] + list(org['org_be_fullname_rus'].unique()), index=1)
    filtered_sp = org[org['org_be_fullname_rus'] == selected_be]['org_sp_mixname_rus'].unique()
    selected_sp = st.sidebar.selectbox("Выберите структурное подразделение", ['Все','Несколько СП'] + list(filtered_sp))

    #selected_product = st.selectbox("Выберите метрику", ['Все'] + list(ds['dc_metric_fullname_rus'].unique()))
    # selected_product = st.sidebar.radio("Выберите метрику", ['Все'] + list(ds['dc_metric_fullname_rus'].unique()),
    #     index='Все',
    # )
    selected_product = st.sidebar.radio(
        "Выберите метрику",
        ["Все"] + list(ds['dc_metric_fullname_rus'].unique()), index=1,
    )

    start_year = startDate.year
    start_month = startDate.month
    start_day = startDate.day

    startDateBSK_year = startDateBSK.year
    startDateBSK_month = startDateBSK.month
    startDateBSK_day = startDateBSK.day

    end_year = endDate.year
    end_month = endDate.month
    end_day = endDate.day

    endDateBSK_year = endDateBSK.year
    endDateBSK_month = endDateBSK.month
    endDateBSK_day = endDateBSK.day

    date_dataframe = pd.DataFrame({"dates": ar['date_dataframe'].unique()})
    dateBSK_dataframe = pd.DataFrame({"datesBSK": ar['date_1'].unique()})

    dates = st.sidebar.slider(
        "Даты слепков (включительно)",
        min_value = datetime(start_year, start_month, start_day),
        max_value = datetime(end_year, end_month, end_day),
        value=(datetime(start_year, start_month, start_day),datetime(end_year, end_month, end_day)),
        format="DD.MM.YYYY")
    
    buttonBSK = st.sidebar.radio(
    "Выберите даты БСК",
    ["До 2023 г.", "В 2023 г.", "Сбросить"], index=2)

    if buttonBSK =='До 2023 г.':
        datesBSK = st.sidebar.slider(
            "Даты базисного срока конца (включительно)",
            min_value = datetime(startDateBSK_year, startDateBSK_month, startDateBSK_day),
            max_value = datetime(endDateBSK_year, endDateBSK_month, endDateBSK_day),
            value=(datetime(startDateBSK_year, startDateBSK_month, startDateBSK_day),datetime(2022,12,31)),
            format="DD.MM.YYYY")
    elif buttonBSK == 'В 2023 г.':
        datesBSK = st.sidebar.slider(
            "Даты базисного срока конца (включительно)",
            min_value = datetime(startDateBSK_year, startDateBSK_month, startDateBSK_day),
            max_value = datetime(endDateBSK_year, endDateBSK_month, endDateBSK_day),
            value=(datetime(2023,1,1),datetime(2023,12,31)),
            format="DD.MM.YYYY")
    elif buttonBSK == 'Сбросить':
        datesBSK = st.sidebar.slider(
            "Даты базисного срока конца (включительно)",
            min_value = datetime(startDateBSK_year, startDateBSK_month, startDateBSK_day),
            max_value = datetime(endDateBSK_year, endDateBSK_month, endDateBSK_day),
            value=(datetime(startDateBSK_year, startDateBSK_month, startDateBSK_day),datetime(endDateBSK_year, endDateBSK_month, endDateBSK_day)),
            format="DD.MM.YYYY")
                 
    # Фильтруйте DataFrame по выбранному диапазону дат
    filtered_dataframe = date_dataframe[
        (pd.to_datetime(date_dataframe["dates"], format="%Y.%m.%d") >= dates[0]) &
        (pd.to_datetime(date_dataframe["dates"], format="%Y.%m.%d") <= dates[1])
    ]

    filtered_dataframeBSK = dateBSK_dataframe[
        (pd.to_datetime(dateBSK_dataframe["datesBSK"], format="%Y.%m.%d") >= datesBSK[0]) &
        (pd.to_datetime(dateBSK_dataframe["datesBSK"], format="%Y.%m.%d") <= datesBSK[1])
    ]

    #st.dataframe(filtered_dataframe, hide_index=True)
    # Преобразуйте столбец 'date_dataframe' в формат datetime
    ar['date_dataframe'] = pd.to_datetime(ar['date_dataframe'], format="%d.%m.%Y")
    ar['date_1'] = pd.to_datetime(ar['date_1'], format="%d.%m.%Y")

    # Получите уникальные даты из filtered_dataframe
    selected_dates = pd.to_datetime(filtered_dataframe['dates'], format="%d.%m.%Y")
    selected_datesBSK = pd.to_datetime(filtered_dataframeBSK['datesBSK'], format="%d.%m.%Y")

    # Фильтруйте DataFrame ar по выбранным датам
    ar = ar[ar['date_dataframe'].isin(selected_dates)]
    ar = ar[ar['date_1'].isin(selected_datesBSK)]


    if selected_product == 'Все':
        ar['new'] = None

    # elif selected_product == '8. Просроченные заказы ТОРО':
    #     metric = ds[ds['dc_metric_fullname_rus'] == selected_product]['dc_metric_fullname_rus'].values[0]
    #     st.subheader("Метрика: " + metric)
    #     ar['date_1'] = pd.to_datetime(ar['date_1'], format="%d.%m.%Y")
    #     ar = ar[ar['date_1'] <= last_day_of_previous_year]
    #     ar['new'] = None
    #     prosr_year_zkz = (ar['text_2'] != "ТЗКР") & (ar['date_1'] <= current_date)
    #     ar.loc[prosr_year_zkz, 'new'] = 'Просроченные заказы прошлого года'

    elif selected_product == '8.Просроченные заказы ТОРО':
        metric = ds[ds['dc_metric_fullname_rus'] == selected_product]['dc_metric_fullname_rus'].values[0]
        st.header(metric, divider='rainbow')
        ar['date_1'] = pd.to_datetime(ar['date_1'], format="%d.%m.%Y")
        #ar = ar[(ar['date_1'] < last_day_of_current_year) & (ar['date_1'] > last_day_of_previous_year)]

        ar['new'] = None
        #print(ar)

        zakr_zkz =  (ar['text_2'] == "ТЗКР") & (ar['date_1'] <= ar['date_dataframe'])
        ar.loc[zakr_zkz, 'new'] = '1. Закрытые заказы'

        prosr_zkz = (ar['text_2'] != "ТЗКР") & (ar['date_1'] <= ar['date_dataframe'])
        ar.loc[prosr_zkz, 'new'] = '2. Просроченные заказы'

        aktual_zkz = (ar['text_2'] != "ТЗКР") & (ar['date_1'] > ar['date_dataframe'])
        ar.loc[aktual_zkz, 'new'] = '3. Актуальные заказы'

        predzakr_zkz = (ar['text_2'] == "ТЗКР") & (ar['date_1'] > ar['date_dataframe'])
        ar.loc[predzakr_zkz, 'new'] = '4. Предзакрытые заказы'

        # Создаем список из таблиц, которые нужно объединить
        #print(ar)


    if selected_sp == 'Все':
        filtered_sp_data = ar

    if selected_sp != 'Все' and selected_sp != 'Несколько СП':
        # получение значения org_sp_kod для выбранной строки
        org_sp_kod_value = org[org['org_sp_mixname_rus'] == selected_sp]['org_sp_kod'].values[0]
        filtered_sp_data = ar[ar['org_sp_kod'] == org_sp_kod_value]
        st.write("Код структурного подразделения: " + org_sp_kod_value)

    if selected_sp == 'Несколько СП':
        spMultiFilter = st.sidebar.multiselect("Выберите несколько СП", list(filtered_sp))
        org_sp_kod_values = org[org['org_sp_mixname_rus'].isin(spMultiFilter)]['org_sp_kod'].unique()
        filtered_sp_data = ar[ar['org_sp_kod'].isin(org_sp_kod_values)]
    #print(filtered_sp_data)

    selected_gp = st.sidebar.selectbox("Выберите группу плановиков", ['Все','Несколько ГП'] + list(gp['gp_shortname_rus'].unique()))
    uniq_gp = gp['gp_shortname_rus'].unique()

    if selected_gp == 'Все':
        filtered_sp_gp_data = filtered_sp_data

    if selected_gp != 'Все' and selected_gp != 'Несколько ГП':
        gp_kod_value = gp[gp['gp_shortname_rus'] == selected_gp]['gp_kod'].values[0]
        #print(gp_kod_value)
        filtered_sp_gp_data = filtered_sp_data[filtered_sp_data['gp_kod'] == gp_kod_value]
        st.write("Код группы плановиков: " + gp_kod_value)

    if selected_gp == 'Несколько ГП':
        gpMultiFilter = st.sidebar.multiselect("Выберите несколько ГП", list(uniq_gp))
        org_sp_gp_kod_values = gp[gp['gp_shortname_rus'].isin(gpMultiFilter)]['gp_kod'].unique()
        filtered_sp_gp_data = filtered_sp_data[filtered_sp_data['gp_kod'].isin(org_sp_gp_kod_values)]
    #print(filtered_sp_gp_data)



    #tb_count = ar.groupby('org_sp_kod')['number_1'].sum()
    tb_countMerged = pd.merge(filtered_sp_gp_data, org, on='org_sp_kod', how="right")
    tb_countMerged = pd.merge(tb_countMerged, gp, on = 'gp_kod', how = "right")
    #print(tb_countMerged)
    tb_countMerged['date_dataframe'] = pd.to_datetime(tb_countMerged['date_dataframe']).dt.strftime('%d.%m.%Y')
    #tb_price = ar.groupby('org_sp_kod')['number_2'].sum()
    if selected_be !="Все":
        endex = ['org_sp_mixname_rus']
        if selected_sp !="Все" and selected_sp !="Несколько СП":    
            endex = ['gp_kod']
    else: endex = ['org_sp_mixname_rus']
    
    pivot_table1 = pd.pivot_table(tb_countMerged,
                                values='number_1',
                                index=endex,
                                columns='date_dataframe', 
                                aggfunc='sum')
    
    date_columns = pivot_table1.columns.tolist()
    date_columns_datetime = pd.to_datetime(date_columns, format="%d.%m.%Y")
    sorted_dates = date_columns_datetime.sort_values()
    pivot_table1_sorted = pivot_table1.reindex(columns=sorted_dates.strftime("%d.%m.%Y"))
    #pivot_table1.dropna(how='all', inplace=True)
    cols1 = st.columns(2)
    # Первая таблица
    with cols1[0]:
        st.dataframe(
            pivot_table1_sorted,
            column_config={
                "org_sp_mixname_rus": "Завод"
            },
            width=False, height=False, hide_index=False, use_container_width=True
        )

    
        date1 = dates[0]  # Первая выбранная дата
        date2 = dates[1]  # Вторая выбранная дата

        # Преобразование выбранных дат к нужному формату, если это необходимо
        date1 = pd.to_datetime(date1, format="%Y-%m-%d")  # Замените форматом дат, используемым в вашем случае
        date2 = pd.to_datetime(date2, format="%Y-%m-%d")

        date2_form = date2.strftime("%d.%m.%Y") 
        

        grouped_data_date1 = pd.DataFrame(filtered_sp_gp_data[filtered_sp_gp_data['date_dataframe'] >= date1])
        # Находим минимальную дату из отфильтрованных данных
        min_date_filtered_data_date1 = grouped_data_date1['date_dataframe'].min()
        date1_form = min_date_filtered_data_date1.strftime("%d.%m.%Y") 
        # Получаем данные для минимальной даты
        grouped_data_date1 = pd.DataFrame(grouped_data_date1[grouped_data_date1['date_dataframe'] == min_date_filtered_data_date1])
        grouped_data_date1 = grouped_data_date1.groupby('org_sp_kod')['number_1'].sum().reset_index()
        

        grouped_data_date2 = pd.DataFrame(filtered_sp_gp_data[filtered_sp_gp_data['date_dataframe'] <= date2])
        # Находим минимальную дату из отфильтрованных данных
        min_date_filtered_data_date2 = grouped_data_date2['date_dataframe'].max()
        date2_form = min_date_filtered_data_date2.strftime("%d.%m.%Y") 
        # Получаем данные для минимальной даты
        grouped_data_date2 = pd.DataFrame(grouped_data_date2[grouped_data_date2['date_dataframe'] == min_date_filtered_data_date2])
        grouped_data_date2 = grouped_data_date2.groupby('org_sp_kod')['number_1'].sum().reset_index()
        
        # Объединяем данные по заводу из двух дат в один DataFrame
        merged_data = pd.merge(grouped_data_date1, grouped_data_date2, on='org_sp_kod', suffixes=('_date1', '_date2'), how='outer')   
        
        # Создаем столбец с разницей между суммами для двух дат
        merged_data['difference'] = merged_data['number_1_date2'] - merged_data['number_1_date1']
        merged_data = pd.merge(merged_data,org, on = 'org_sp_kod', how = 'right')
        columns_to_keep = ['org_sp_mixname_rus', 'number_1_date1', 'number_1_date2', 'difference']
        # Отображаем полученную сводную таблицу с разницей между датами
        merged_data = merged_data[columns_to_keep]


    # Функция для стилизации цвета ячеек в зависимости от значения в столбце "difference"
    def color_negative_red(val):
        val = val.replace(',', '')  # Удаляем запятые из числовых значений
        val = float(val)  # Преобразуем строку обратно в число
        if val > 0:
            color = 'rgba(255, 0, 0, 0.5)'  # Красный с прозрачностью
        elif val < 0:
            color = 'rgba(0, 255, 0, 0.5)'  # Зеленый с прозрачностью
        else:
            color = 'rgba(255, 255, 0, 0.5)'  # Желтый с прозрачностью
        return f'background-color: {color}'  # Возвращаем CSS для установки цвета фона ячейки

    # Применение функции к столбцу "difference" в DataFrame
    merged_data_styled = merged_data.copy()
    merged_data_styled['difference'] = merged_data_styled['difference'].apply(lambda x: f'{x:,}')

    # Вывод DataFrame с добавленной стилизацией для столбца "Разница"
    with cols1[1]:
        st.dataframe(
            merged_data_styled.style.applymap(color_negative_red, subset=['difference']),
            column_config={
                "org_sp_mixname_rus": "Завод",
                "number_1_date1": date1_form,
                "number_1_date2": date2_form,
                "difference": "Разница"
            },
            width=False, height=False, hide_index=True, use_container_width=True
        )

    grouped_data_sp = filtered_sp_gp_data.groupby(['date_dataframe', 'org_sp_kod'])['number_2'].sum().reset_index()
    grouped_data_zkz = filtered_sp_gp_data.groupby(['date_dataframe', 'org_sp_kod','new'])['number_2'].sum().reset_index()
    grouped_data_zkz_monthly = grouped_data_zkz.groupby(pd.Grouper(key='date_dataframe', freq='M')).sum().reset_index()
    # # Создание линейного графика с использованием Seaborn
    # plt.figure(figsize=(6, 3))
    # sns.lineplot(data=grouped_data_sp, x='date_dataframe', y='number_2', hue='org_sp_kod')
    # plt.title('График количества заказов по СП')
    # plt.xlabel('Дата')
    # plt.ylabel('Количество заказов')
    # plt.legend(title='org_sp_kod')

    # # Отображение графика
    # st.pyplot()
    
    # if selected_product == '8.1.Просроченные заказы ТОРО прошлых лет':
    #     fig1 = px.line(grouped_data_sp, x='date_dataframe', y='number_2', color='org_sp_kod',
    #                 title='График количества заказов по СП', labels={'date_dataframe': 'Дата', 'number_2': 'Количество заказов'},
    #                 line_group='org_sp_kod')

    #     fig1.update_layout(
    #         xaxis_title='Дата',
    #         yaxis_title='Количество заказов',
    #         legend_title='org_sp_kod',
    #         margin=dict(l=0, r=50, t=0, b=0),  # устанавливаем отступы графика по краям
    #         width=1400
    #     )
    #     st.plotly_chart(fig1)

    if selected_product == '8.Просроченные заказы ТОРО': 
        cols2 = st.columns(2)
        with cols2[0]:
            fig1 = px.line(grouped_data_sp, x='date_dataframe', y='number_2', color='org_sp_kod',
                        title='График количества заказов по СП', labels={'date_dataframe': 'Дата', 'number_2': 'Количество заказов'},
                        line_group='org_sp_kod')

            fig1.update_layout(
                xaxis_title='Дата',
                yaxis_title='Количество заказов',
                legend_title='org_sp_kod'
            )
            st.plotly_chart(fig1)

        with cols2[1]:
            fig2 = px.bar(grouped_data_zkz, x='date_dataframe', y='number_2', color='new',
                        title='График количества типов заказов по СП', labels={'org_sp_kod': 'Завод', 'number_2': 'Количество заказов'})

            fig2.update_layout(
                xaxis_title='Дата',
                yaxis_title='Заказы',
                legend_title='Тип заказа'
            )
            st.plotly_chart(fig2)
            


    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(filtered_sp_data)

    st.sidebar.download_button(
        label="Экспорт в CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

# Run the app
if __name__ == "__main__":
    main()