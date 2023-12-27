def metric_main_01(df_main_pivot_table1, dates_chooses_00):
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
    differences.name = "Разница между датами {} и {}".format(min_date, max_date)

    # Add the differences as a new column to the DataFrame
    df_main_pivot_table1_with_difference = pd.concat([df_main_pivot_table1, differences], axis=1)

    # Add color-coding
    cmap = sns.diverging_palette(10, 220, as_cmap=True)
    styled_df = df_main_pivot_table1_with_difference.style.background_gradient(cmap=cmap, axis=0)

    st.subheader("Разница между датами {} и {}:".format(min_date, max_date))
    st.dataframe(styled_df, unsafe_allow_html=True)
