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

    #print(ar.dtypes)
    endex = []
    startDate = pd.to_datetime(ar["date_dataframe"]).min()
    endDate = pd.to_datetime(ar["date_dataframe"]).max()
    # Получаем текущую дату
    current_date = datetime.now()
    # Получаем последний день текущего года
    last_day_of_current_year = datetime(current_date.year, 12, 31)
    # Получаем последний день прошлого года
    last_day_of_previous_year = last_day_of_current_year - timedelta(days=365)
    # Выводим последний день прошлого года
    #print(last_day_of_previous_year)
    
    st.header("Демоверсия отчетов для сервиса: ")
    st.sidebar.header("Фильтры отчетов")
    selected_be = st.sidebar.selectbox("Выберите балансовую единицу", ['Все'] + list(org['org_be_fullname_rus'].unique()))
    filtered_sp = org[org['org_be_fullname_rus'] == selected_be]['org_sp_mixname_rus'].unique()
    selected_sp = st.sidebar.selectbox("Выберите структурное подразделение", ['Все','Несколько СП'] + list(filtered_sp))

    selected_product = st.selectbox("Выберите метрику", ['Все'] + list(ds['dc_metric_fullname_rus'].unique()))


    start_year = startDate.year
    start_month = startDate.month
    start_day = startDate.day

    end_year = endDate.year
    end_month = endDate.month
    end_day = endDate.day

    date_dataframe = pd.DataFrame({"dates": ar['date_dataframe'].unique()})

    dates = st.slider(
        "Даты слепков",
        min_value = datetime(start_year, start_month, start_day),
        max_value = datetime(end_year, end_month, end_day),
        value=(datetime(start_year, start_month, start_day),datetime(end_year, end_month, end_day)),
        format="DD.MM.YYYY")
    
    # Фильтруйте DataFrame по выбранному диапазону дат
    filtered_dataframe = date_dataframe[
        (pd.to_datetime(date_dataframe["dates"], format="%d.%m.%Y") >= dates[0]) &
        (pd.to_datetime(date_dataframe["dates"], format="%d.%m.%Y") <= dates[1])
    ]
    st.dataframe(filtered_dataframe, hide_index=True)
    # Преобразуйте столбец 'date_dataframe' в формат datetime
    ar['date_dataframe'] = pd.to_datetime(ar['date_dataframe'], format="%d.%m.%Y")

    # Получите уникальные даты из filtered_dataframe
    selected_dates = pd.to_datetime(filtered_dataframe['dates'], format="%d.%m.%Y")

    # Фильтруйте DataFrame ar по выбранным датам
    ar = ar[ar['date_dataframe'].isin(selected_dates)]

    if selected_product == '8.1.Просроченные заказы ТОРО прошлых лет':
        metric = ds[ds['dc_metric_fullname_rus'] == selected_product]['dc_metric_fullname_rus'].values[0]
        st.subheader("Метрика: " + metric)
        ar['date_1'] = pd.to_datetime(ar['date_1'])
        ar = ar[ar['date_1'] <= last_day_of_previous_year]


    if selected_product == '8.2.Просроченные заказы ТОРО текущего года':
        metric = ds[ds['dc_metric_fullname_rus'] == selected_product]['dc_metric_fullname_rus'].values[0]
        st.subheader("Метрика: " + metric)
        ar['date_1'] = pd.to_datetime(ar['date_1'])
        ar = ar[(ar['date_1'] < last_day_of_current_year) & (ar['date_1'] > last_day_of_previous_year)]

        ar['new'] = None
        print(ar)

        zakr_zkz =  (ar['text_2'] == "ТЗКР") & (ar['date_1'] <= current_date)
        ar.loc[zakr_zkz, 'new'] = '1. Закрытые заказы'

        prosr_zkz = (ar['text_2'] != "ТЗКР") & (ar['date_1'] <= current_date)
        ar.loc[prosr_zkz, 'new'] = '2. Просроченные заказы'

        aktual_zkz = (ar['text_2'] != "ТЗКР") & (ar['date_1'] > current_date)
        ar.loc[aktual_zkz, 'new'] = '3. Актуальные заказы'

        predzakr_zkz = (ar['text_2'] == "ТЗКР") & (ar['date_1'] > current_date)
        ar.loc[predzakr_zkz, 'new'] = '4. Предзакрытые заказы'

        # Создаем список из таблиц, которые нужно объединить
        print(ar)


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
        print(gp_kod_value)
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

    #pivot_table1.dropna(how='all', inplace=True)
    cols1 = st.columns(2)
    # Первая таблица
    with cols1[0]:
        st.dataframe(
            pivot_table1.style.background_gradient(cmap='RdYlGn_r', axis=None),
            column_config={
                "org_sp_mixname_rus": "Завод"
            },
            width=False, height=False, hide_index=False, use_container_width=True
        )

    # Вторая таблица
    with cols1[1]:
        st.dataframe(
            pivot_table1.style.background_gradient(cmap='RdYlGn_r', axis=1),
            column_config={
                "org_sp_mixname_rus": "Завод"
            },
            width=False, height=False, hide_index=False, use_container_width=True
        )

    # Группировка данных
    grouped_data = filtered_sp_data.groupby(['date_dataframe', 'org_sp_kod'])['number_2'].sum().reset_index()

    # # Создание линейного графика с использованием Seaborn
    # plt.figure(figsize=(6, 3))
    # sns.lineplot(data=grouped_data, x='date_dataframe', y='number_2', hue='org_sp_kod')
    # plt.title('График количества заказов по СП')
    # plt.xlabel('Дата')
    # plt.ylabel('Количество заказов')
    # plt.legend(title='org_sp_kod')

    # # Отображение графика
    # st.pyplot()
    if selected_product == '8.1.Просроченные заказы ТОРО прошлых лет':
        fig1 = px.line(grouped_data, x='date_dataframe', y='number_2', color='org_sp_kod',
                    title='График количества заказов по СП', labels={'date_dataframe': 'Дата', 'number_2': 'Количество заказов'},
                    line_group='org_sp_kod')

        fig1.update_layout(
            xaxis_title='Дата',
            yaxis_title='Количество заказов',
            legend_title='org_sp_kod',
            margin=dict(l=0, r=50, t=0, b=0),  # устанавливаем отступы графика по краям
            width=1400
        )
        st.plotly_chart(fig1)

    if selected_product == '8.2.Просроченные заказы ТОРО текущего года': 
        cols2 = st.columns(2)
        with cols2[0]:
            fig1 = px.line(grouped_data, x='date_dataframe', y='number_2', color='org_sp_kod',
                        title='График количества заказов по СП', labels={'date_dataframe': 'Дата', 'number_2': 'Количество заказов'},
                        line_group='org_sp_kod')

            fig1.update_layout(
                xaxis_title='Дата',
                yaxis_title='Количество заказов',
                legend_title='org_sp_kod'
            )
            st.plotly_chart(fig1)
        
        with cols2[1]:
            fig2 = px.bar(grouped_data, x='org_sp_kod', y='number_2', color='new',
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

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

    
# Run the app
if __name__ == "__main__":
    main()