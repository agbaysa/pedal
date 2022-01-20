# Import Libraries
import pandas as pd
import numpy as np
import streamlit as st
import random
import datetime as dt
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

rad = st.sidebar.radio('Pages', ['About PEDAL','Visualization', 'Types of Graphs'])

if rad == 'About PEDAL':

    # Title
    st.title("""Visualize Your Data with ***PEDAL***(Beta)""")
    st.image('pic1.jpg', use_column_width='always')

    st.markdown("""***PEDAL*** (Plotly Express Exploratory Data AnaLysis) is an open-source
    web application that allows you to visualize your data using Plotly Express without the
    need to write code.""")

    st.markdown("""It uses ***Plotly Express*** to visualize your data. The key features of
    ***PEDAL*** are as follows:""")

    st.write("""
        - ***Interactive:*** Allows you to generate an interactive graph using your own data in csv format 
        - ***Chart Selection:*** Select your own chart types such as bar plots, scatter plots, line charts, histograms, sunburst plots, etc.
        - ***Graph Theme:*** Choose your graph's look and feel with graph themes and aesthetics such as color, size, dimensions
        - ***Drill Down Analysis:*** Drill down on the dimensions of your data using facets
        - ***Downloadable:*** Download a static image of your graph""")

    st.write("""Click on the ***Visualization*** radio button on the left sidebar to visualize your data.""")

    st.write("""To read about the various types of graphs available in PEDAL, click ***Types of Graphs***.""")

if rad == 'Visualization':

    # Dummy Dataset
    random.seed(1)

    my_date = list(pd.date_range(start='01-01-2021', end='03-31-2021'))
    my_branch = [1,2,3,4,5]
    my_gender = ['Male','Female']
    my_status = ['Single','Married','Widow']
    my_status_wts = [0.2, 0.7, 0.1]
    my_job =  ['Employed','Business','OFW','Retired','OFW']
    my_job_wts = [0.5,0.1,0.1, 0.05, 0.25]

    n = 100
    salary = np.random.normal(30000,5000, n)
    balance = np.random.normal(50000,2000, n)
    percentage = np.random.normal(.025, .0001, n)

    df = pd.DataFrame()
    df['date'] = random.choices(my_date, k=n)
    df['date'] = df['date'].dt.date
    df['branch'] = random.choices(my_branch, k=n)
    df['gender'] = random.choices(my_gender, k=n)
    df['status'] = random.choices(my_status, k=n, weights=my_status_wts)
    df['job'] = random.choices(my_job, k=n, weights=my_job_wts)
    df['salary'] = salary
    df['balance'] = balance
    df['percentage'] = percentage
    df['percentage'] = df['percentage']/100
    df.dropna(inplace=True)


    # Dataset Upload
    st.header('Upload Dataset')
    st.markdown("""You can upload your own dataset (in csv format) for visualization by clicking the
    ***Browse files*** button below. Note that NaNs will be automatically dropped in order to visualize the data.
    In the absence of your own dataset, a sample dataset is also provided belows
    so you can tinker with the app's visualization capabilities.""")

    df1 = st.file_uploader('Upload csv:', type='csv')


    # Drop NA if any
    if df1:
        df1 = pd.read_csv(df1)
        df1.dropna(inplace=True)
    else:
        df1=df


    st.dataframe(df1)

    st.header('Descriptive Statistics')
    st.markdown("""The following is the descriptive statistics for the dataset's numeric features:""")

    num_col = df1.select_dtypes(include='number').columns
    st.write(df1[num_col].describe())


    # Visualization
    st.header('Visualization')
    st.markdown("""Follow these steps to visualize your data:""")
    st.write("""
              - You can either use the sample dataset provided or use your uploaded dataset
              - After uploading your dataset, select the plot type you would like to generate in the left sidebar.
              - Next, choose the dimension of your graph (e.g. Salary column for x-axis, etc.)
              - You may opt to visualize other dimensions of your data by using aesthetics such as
                color, size, etc. Note that some graph types have other parameters you can use which is
                applicable for that specific type of graph only 
              - You can also have the option to facet your data. Facets splits your graphs by
                categories (e.g. scatter plot by gender generate graphs for male and female categories)
              - For facets, you can further define the layout of your facet graphs. Adjust the slider
                to tweak the layout of your facet graphs.
              - Indicate the title of your graph by typing in the Graph Title text box
              - Check out the various themes available to adjust the look and feel of your graph
              - Press the ***Click to generate graph*** button. Remember to always click this button
                after changing the graph parameters
              - Hover over your graph to see the details of the data points
              - You can download a static image of your graph by clicking the camera icon on the upper right
                side of the graph""")



    rad = st.sidebar.selectbox('Select plot type:', ['Area','Bar','Box','Density Contour','Density Heatmap',
                                                 'Histogram','Line','Pie','Polar (Bar)','Polar (Line)',
                                                 'Polar (Scatter)','Scatter','Scatter Geo','Scatter Matrix','Strip',
                                                 'Sunburst','Treemap','Violin'])

    col_all = list(df1.columns)
    col_all.insert(0, None)


    # Scatter Plot
    if rad == 'Scatter':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='x_sp')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_sp')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_sp')
        size = st.sidebar.selectbox('Size:', col_all, key='size_sp')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc_sp')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1, key='sl_sp')
        marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx_sp')
        marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx_sp')
        trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx_sp')

        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order, key='fo_sc')
            facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title',key='t_sc')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"],key='te_sc')


        if st.sidebar.button('Click to generate graph'):
            fig = px.scatter(df1, x=x, y=y,
                             color=color,
                             size=size,
                             facet_col=facet_col,
                             facet_col_wrap=facet_col_wrap,
                             category_orders=facet_order2,
                             marginal_x=marginal_x,
                             marginal_y=marginal_y,
                             trendline=trendline,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass


    # Bar Plot
    if rad == 'Bar':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='x_bp')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_bp')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_bp')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc_bp')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1, key='fw_bp')
        barmode = st.sidebar.selectbox('Select barmode:', [None, 'group','relative','overlay'], key='bm_bp')


        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order, key='fo_bp')
            facet_order2 = {facet_col: facet_order}

        #hline and vline:
        y_hline = st.sidebar.number_input('Select value of horizontal line', value=0, key='hl_bp')
        annotation_text = st.sidebar.text_input('Type comments for horizontal line:', value='', key='hl_bp')
        annotation_position = st.sidebar.selectbox('Select position of horizontal line comment:', [None, 'top left', 'bottom right'], key='ap_bp')

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_bp')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"], key='te_bp')


        if st.sidebar.button('Click to generate graph', key='b_bp'):
            fig = px.bar(df1, x=x, y=y,
                             color=color,
                             # size=size,
                             facet_col=facet_col,
                             facet_col_wrap=facet_col_wrap,
                             category_orders=facet_order2,
                             barmode=barmode,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)


            fig.add_hline(y=y_hline,
                          line_dash="dot",
                          annotation_text=annotation_text,
                          annotation_position=annotation_position)

            st.plotly_chart(fig)


        else:
            pass


    # Line Plot
    if rad == 'Line':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='x_ln')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_ln')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_ln')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc_ln')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1, key='fc_ln')
        line_group = st.sidebar.selectbox('Select Line Groupings:', col_all, key='lg_ln')

        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order, key='fo_ln')
            facet_order2 = {facet_col: facet_order}

        #hline and vline:
        y_hline = st.sidebar.number_input('Select value of horizontal line', value=0, key='hl_ln')
        annotation_text = st.sidebar.text_input('Type comments for horizontal line:', value='', key='at_ln')
        annotation_position = st.sidebar.selectbox('Select position of horizontal line comment:', [None, 'top left', 'bottom right'], key='ap_ln')

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_ln')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"], key='t_ln')



        if st.sidebar.button('Click to generate graph', key='b_ln'):
            fig = px.line(df1, x=x, y=y,
                             color=color,
                             # size=size,
                             facet_col=facet_col,
                             facet_col_wrap=facet_col_wrap,
                             category_orders=facet_order2,
                             template=template,
                             line_group=line_group)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)


            fig.add_hline(y=y_hline,
                          line_dash="dot",
                          annotation_text=annotation_text,
                          annotation_position=annotation_position)

            st.plotly_chart(fig)


        else:
            pass

    # Scatter Matrix
    if rad == 'Scatter Matrix':

        st.sidebar.markdown('Select Dimensions:')
        dimensions = st.sidebar.multiselect('Dimensions (select numeric only):', col_all, key='dim_sm')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_sm')
        size = st.sidebar.selectbox('Size:', col_all, key='size_sm')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
        #     facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_sm')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"], key='te_sm')


        if st.sidebar.button('Click to generate graph', key='b_sm'):
            fig = px.scatter_matrix(df1, dimensions=dimensions,
                             color=color,
                             size=size,
                             # facet_col=facet_col,
                             # facet_col_wrap=facet_col_wrap,
                             # category_orders=facet_order2,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass

    # Area Plot
    if rad == 'Area':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='x_ap')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_ap')


        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_ap')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')


        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc_ap')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1, key='fc_ap')
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
        #     facet_order2 = {facet_col: facet_order}

        # hline and vline:
        y_hline = st.sidebar.number_input('Select value of horizontal line', value=0, key='hl_ap')
        annotation_text = st.sidebar.text_input('Type comments for horizontal line:', value='', key='at_ap')
        annotation_position = st.sidebar.selectbox('Select position of horizontal line comment:',
                                                   [None, 'top left', 'bottom right'], key='ap_ap')

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_ap')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"], key='te_ap')


        if st.sidebar.button('Click to generate graph'):
            fig = px.area(df1, x=x, y=y,
                             color=color,
                             # size=size,
                             facet_col=facet_col,
                             facet_col_wrap=facet_col_wrap,
                             # category_orders=facet_order2,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             template=template)

            fig.add_hline(y=y_hline,
                          line_dash="dot",
                          annotation_text=annotation_text,
                          annotation_position=annotation_position)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass


    # Pie Plot
    if rad == 'Pie':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='x_pie')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_pie')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_pie')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
        #     facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_pie')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"], key='te_pie')


        if st.sidebar.button('Click to generate graph', key='b_pie'):
            fig = px.pie(df1, names=x, values=y,
                             color=color,
                             # size=size,
                             # facet_col=facet_col,
                             # facet_col_wrap=facet_col_wrap,
                             # category_orders=facet_order2,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass



    # Sunburst
    if rad == 'Sunburst':

        st.sidebar.markdown('Select Dimensions:')
        path = st.sidebar.multiselect('Select Path in order:', col_all, key='path1_sun')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_sun')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_sun')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
        #     facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_sun')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"], key='te_sun')


        if st.sidebar.button('Click to generate graph', key='b_sun'):
            fig = px.sunburst(df1, path=path, values=y,
                             color=color,
                             # size=size,
                             # facet_col=facet_col,
                             # facet_col_wrap=facet_col_wrap,
                             # category_orders=facet_order2,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass


    # Treemap
    if rad == 'Treemap':

        st.sidebar.markdown('Select Dimensions:')
        path = st.sidebar.multiselect('Select Path in order:', col_all, key='path2_tm')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_tm')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_tm')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
        #     facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_tm')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"], key='te_tm')


        if st.sidebar.button('Click to generate graph', key='b_tm'):
            fig = px.treemap(df1, path=path, values=y,
                             color=color,
                             # size=size,
                             # facet_col=facet_col,
                             # facet_col_wrap=facet_col_wrap,
                             # category_orders=facet_order2,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass





    # Histogram
    if rad == 'Histogram':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path4')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])

        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
            facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"])


        if st.sidebar.button('Click to generate graph'):
            fig = px.histogram(df1, x=x, y=y,
                             color=color,
                             # size=size,
                             facet_col=facet_col,
                             # facet_col_wrap=facet_col_wrap,
                             category_orders=facet_order2,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             marginal=marginal,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass


    # Box Plot
    if rad == 'Box':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path5')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])


        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
            facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"])


        if st.sidebar.button('Click to generate graph'):
            fig = px.box(df1, x=x, y=y,
                             color=color,
                             # size=size,
                             facet_col=facet_col,
                             facet_col_wrap=facet_col_wrap,
                             category_orders=facet_order2,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             # marginal=marginal,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass


    # Violin Plot
    if rad == 'Violin':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path6')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])


        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:', my_col_order)
            facet_order2 = {facet_col: facet_order}


        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:', ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"])


        if st.sidebar.button('Click to generate graph'):
            fig = px.violin(df1, x=x, y=y,
                             color=color,
                             # size=size,
                             facet_col=facet_col,
                             facet_col_wrap=facet_col_wrap,
                             category_orders=facet_order2,
                             points='all',
                             box=True,
                             # marginal_x=marginal_x,
                             # marginal_y=marginal_y,
                             # trendline=trendline,
                             # marginal=marginal,
                             template=template)

            fig.update_layout(
                title=title)
                # xaxis_title=xaxis_title,
                # yaxis_title=yaxis_title,
                # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass

    # Strip Plot
    if rad == 'Strip':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path7')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])
        orientation = st.sidebar.selectbox('Select orientation:',['h','v'], key='or')

        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:',
                                                 my_col_order)
            facet_order2 = {facet_col: facet_order}

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:',
                                        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white",
                                         "none"])

        if st.sidebar.button('Click to generate graph'):
            fig = px.violin(df1, x=x, y=y,
                            color=color,
                            # size=size,
                            facet_col=facet_col,
                            facet_col_wrap=facet_col_wrap,
                            category_orders=facet_order2,
                            # points='all',
                            # box=True,
                            # marginal_x=marginal_x,
                            # marginal_y=marginal_y,
                            # trendline=trendline,
                            # marginal=marginal,
                            orientation=orientation,
                            template=template)

            fig.update_layout(
                title=title)
            # xaxis_title=xaxis_title,
            # yaxis_title=yaxis_title,
            # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass


    # Density Contour
    if rad == 'Density Contour':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path8')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y')

        # st.sidebar.markdown('Select Aesthetics:')
        # color = st.sidebar.selectbox('Color:', col_all, key='color')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['box','violin'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['box','violin'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])
        # orientation = st.sidebar.selectbox('Select orientation:',['h','v'], key='or')

        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:',
                                                 my_col_order)
            facet_order2 = {facet_col: facet_order}

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:',
                                        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white",
                                         "none"])

        if st.sidebar.button('Click to generate graph'):
            fig = px.density_contour(df1, x=x, y=y,
                            # color=color,
                            # size=size,
                            facet_col=facet_col,
                            facet_col_wrap=facet_col_wrap,
                            category_orders=facet_order2,
                            # points='all',
                            # box=True,
                            # marginal_x=marginal_x,
                            # marginal_y=marginal_y,
                            # trendline=trendline,
                            # marginal=marginal,
                            # orientation=orientation,
                            template=template)

            fig.update_layout(
                title=title)
            # xaxis_title=xaxis_title,
            # yaxis_title=yaxis_title,
            # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass



    # Density Heatmap
    if rad == 'Density Heatmap':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path9')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_dh')

        # st.sidebar.markdown('Select Aesthetics:')
        # color = st.sidebar.selectbox('Color:', col_all, key='color')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')

        st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        marginal_x= st.sidebar.selectbox('Select Marginal x:', ['rug','box','violin','histogram'], key='mx')
        marginal_y= st.sidebar.selectbox('Select Marginal y:', ['rug','box','violin','histogram'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])
        # orientation = st.sidebar.selectbox('Select orientation:',['h','v'], key='or')

        if facet_col is None:
            facet_order2 = None
        else:
            my_col_order = df1[facet_col].unique()
            facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:',
                                                 my_col_order)
            facet_order2 = {facet_col: facet_order}

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:',
                                        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white",
                                         "none"])

        if st.sidebar.button('Click to generate graph'):
            fig = px.density_heatmap(df1, x=x, y=y,
                            # color=color,
                            # size=size,
                            facet_col=facet_col,
                            facet_col_wrap=facet_col_wrap,
                            category_orders=facet_order2,
                            # points='all',
                            # box=True,
                            marginal_x=marginal_x,
                            marginal_y=marginal_y,
                            # trendline=trendline,
                            # marginal=marginal,
                            # orientation=orientation,
                            template=template)

            fig.update_layout(
                title=title)
            # xaxis_title=xaxis_title,
            # yaxis_title=yaxis_title,
            # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass


    # Polar (Scatter)
    if rad == 'Polar (Scatter)':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path10')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_ps')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_ps')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')
        symbol = st.sidebar.selectbox('Symbol:', col_all, key='symbol_ps')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['rug','box','violin','histogram'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['rug','box','violin','histogram'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])
        # orientation = st.sidebar.selectbox('Select orientation:',['h','v'], key='or')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:',
        #                                          my_col_order)
        #     facet_order2 = {facet_col: facet_order}

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:',
                                        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white",
                                         "none"])

        if st.sidebar.button('Click to generate graph'):
            fig = px.scatter_polar(df1,r=x, theta=y,
                            color=color,
                            # size=size,
                            # facet_col=facet_col,
                            # facet_col_wrap=facet_col_wrap,
                            # category_orders=facet_order2,
                            # points='all',
                            # box=True,
                            # marginal_x=marginal_x,
                            # marginal_y=marginal_y,
                            # trendline=trendline,
                            # marginal=marginal,
                            # orientation=orientation,
                            symbol=symbol,
                            color_discrete_sequence=px.colors.sequential.Plasma_r,
                            template=template)

            fig.update_layout(
                title=title)
            # xaxis_title=xaxis_title,
            # yaxis_title=yaxis_title,
            # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass



    # Polar (Line)
    if rad == 'Polar (Line)':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='path11')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')
        # symbol = st.sidebar.selectbox('Symbol:', col_all, key='symbol')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['rug','box','violin','histogram'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['rug','box','violin','histogram'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])
        # orientation = st.sidebar.selectbox('Select orientation:',['h','v'], key='or')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:',
        #                                          my_col_order)
        #     facet_order2 = {facet_col: facet_order}

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:',
                                        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white",
                                         "none"])

        if st.sidebar.button('Click to generate graph'):
            fig = px.line_polar(df1,r=x, theta=y,
                            color=color,
                            # size=size,
                            # facet_col=facet_col,
                            # facet_col_wrap=facet_col_wrap,
                            # category_orders=facet_order2,
                            # points='all',
                            # box=True,
                            # marginal_x=marginal_x,
                            # marginal_y=marginal_y,
                            # trendline=trendline,
                            # marginal=marginal,
                            # orientation=orientation,
                            # symbol=symbol,
                            line_close=True,
                            color_discrete_sequence=px.colors.sequential.Plasma_r,
                            template=template)

            fig.update_layout(
                title=title)
            # xaxis_title=xaxis_title,
            # yaxis_title=yaxis_title,
            # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass





    # Scatter Geo
    if rad == 'Scatter Geo':

        st.sidebar.markdown('Select Dimensions:')
        my_long = st.sidebar.selectbox('Longitude:', col_all, key='long1')
        my_lat = st.sidebar.selectbox('Latitude:', col_all, key='lat1')

        st.sidebar.markdown('Select Aesthetics:')
        # color = st.sidebar.selectbox('Color:', col_all, key='color')
        size = st.sidebar.selectbox('Size:', col_all, key='size_sg')
        # symbol = st.sidebar.selectbox('Symbol:', col_all, key='symbol')
        my_hover = st.sidebar.selectbox('Hover name:', col_all, key='h_sg')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['rug','box','violin','histogram'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['rug','box','violin','histogram'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])
        # orientation = st.sidebar.selectbox('Select orientation:',['h','v'], key='or')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:',
        #                                          my_col_order)
        #     facet_order2 = {facet_col: facet_order}

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_sg')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:',
                                        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white",
                                         "none"], key='te_sg')

        if st.sidebar.button('Click to generate graph', key='b_sg'):
            fig = px.scatter_geo(df1,lon=my_long, lat=my_lat,
                            # color=color,
                            size=size,
                            # facet_col=facet_col,
                            # facet_col_wrap=facet_col_wrap,
                            # category_orders=facet_order2,
                            # points='all',
                            # box=True,
                            # marginal_x=marginal_x,
                            # marginal_y=marginal_y,
                            # trendline=trendline,
                            # marginal=marginal,
                            # orientation=orientation,
                            # symbol=symbol,
                            # line_close=True,
                            # color_discrete_sequence=px.colors.sequential.Plasma_r,
                            hover_name=my_hover,
                            template=template)

            fig.update_layout(
                title=title)
            # xaxis_title=xaxis_title,
            # yaxis_title=yaxis_title,
            # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass



    # Polar (Bar)
    if rad == 'Polar (Bar)':

        st.sidebar.markdown('Select Dimensions:')
        x = st.sidebar.selectbox('x-axis:', col_all, key='x_pb')
        y = st.sidebar.selectbox('y-axis:', col_all, key='y_pb')

        st.sidebar.markdown('Select Aesthetics:')
        color = st.sidebar.selectbox('Color:', col_all, key='color_pb')
        # size = st.sidebar.selectbox('Size:', col_all, key='size')
        # symbol = st.sidebar.selectbox('Symbol:', col_all, key='symbol')

        # st.sidebar.markdown('Select Facet Dimension:')
        # facet_row = st.sidebar.selectbox('Facet Row:', col_all, key='fr')
        # facet_col = st.sidebar.selectbox('Facet Column:', col_all, key='fc')
        # facet_col_wrap = st.sidebar.slider('Choose number of graph per facet column:', min_value=1, max_value=6, step=1)
        # marginal_x= st.sidebar.selectbox('Select Marginal x:', ['rug','box','violin','histogram'], key='mx')
        # marginal_y= st.sidebar.selectbox('Select Marginal y:', ['rug','box','violin','histogram'], key='mx')
        # trendline = st.sidebar.selectbox('Choose Trendline:', [None,'ols'], key='mx')
        # marginal = st.sidebar.selectbox('Select Marginal:',['rug','box','violin'])
        # orientation = st.sidebar.selectbox('Select orientation:',['h','v'], key='or')

        # if facet_col is None:
        #     facet_order2 = None
        # else:
        #     my_col_order = df1[facet_col].unique()
        #     facet_order = st.sidebar.multiselect('Click the categories in order you want it to appear in the graph:',
        #                                          my_col_order)
        #     facet_order2 = {facet_col: facet_order}

        st.sidebar.markdown('Define Labels and Theme:')
        title = st.sidebar.text_input('Graph Title', key='t_pb')
        # xaxis_title = st.sidebar.text_input('x-axis title')
        # yaxis_title = st.sidebar.text_input('y-axis title')
        # legend_title = st.sidebar.selectbox('Legend Title:', col_all, key='lt')
        template = st.sidebar.selectbox('Choose theme:',
                                        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn",
                                         "simple_white",
                                         "none"], key='te_bp')

        if st.sidebar.button('Click to generate graph', key='b_pb'):
            fig = px.bar_polar(df1, r=x, theta=y,
                               color=color,
                               # size=size,
                               # facet_col=facet_col,
                               # facet_col_wrap=facet_col_wrap,
                               # category_orders=facet_order2,
                               # points='all',
                               # box=True,
                               # marginal_x=marginal_x,
                               # marginal_y=marginal_y,
                               # trendline=trendline,
                               # marginal=marginal,
                               # orientation=orientation,
                               # symbol=symbol,
                               # line_close=True,
                               color_discrete_sequence=px.colors.sequential.Plasma_r,
                               template=template)

            fig.update_layout(
                title=title)
            # xaxis_title=xaxis_title,
            # yaxis_title=yaxis_title,
            # legend_title=legend_title)

            st.plotly_chart(fig)
        else:
            pass




# Types of Graphs
if rad == 'Types of Graphs':
    st.title('Types of Graphs')
    my_type = st.selectbox('Select the graph type to see the description',['Area','Bar','Box','Density Contour','Density Heatmap',
                                                 'Histogram','Line','Pie','Polar (Bar)','Polar (Line)',
                                                 'Polar (Scatter)','Scatter','Scatter Geo','Scatter Matrix','Strip',
                                                 'Sunburst','Treemap','Violin'])

    if my_type=='Area':

        st.image('area.png')
        st.markdown('In a stacked area plot, each row of data_frame is represented as vertex of a polyline mark in 2D space. The area between successive polylines is filled.')
        st.write('')
        st.caption('Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type=='Bar':

        st.image('bar.png')
        st.markdown('In a bar plot, each row of data_frame is represented as a rectangular mark.')
        st.write('')
        st.caption('Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Box':

        st.image('box.png')
        st.markdown('In a box plot, rows of data_frame are grouped together into a box-and-whisker mark to visualize their distribution.'
                    ' The box spans from quartile 1 (Q1) to quartile 3 (Q3). The second quartile (Q2) is marked by a line inside the box. .')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Density Contour':

        st.image('density_contour.png')
        st.markdown('In a density contour plot, rows of data_frame are grouped together into contour marks to visualize the 2D distribution of an aggregate function histfunc (e.g. the count or sum) of the value z.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Density Heatmap':

        st.image('density_heatmap2.png')
        st.markdown('In a density heatmap, rows of data_frame are grouped together into colored rectangular tiles to visualize the 2D distribution of an aggregate function histfunc (e.g. the count or sum) of the value z.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Histogram':

        st.image('Histogram.png')
        st.markdown('In a histogram, rows of data_frame are grouped together into a rectangular mark to visualize the 1D distribution of an aggregate function histfunc (e.g. the count or sum) of the value y (or x if orientation is "h").')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Line':

        st.image('line.png')
        st.markdown('In a 2D line plot, each row of data_frame is represented as vertex of a polyline mark in 2D space.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Pie':

        st.image('pie.png')
        st.markdown('In a pie plot, each row of data_frame is represented as a sector of a pie.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Polar (Bar)':
        st.image('polar_bar.png')
        st.markdown('In a polar bar plot, each row of data_frame is represented as a wedge mark in polar coordinates.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Polar (Line)':
        st.image('polar_line.png')
        st.markdown('In a polar line plot, each row of data_frame is represented as vertex of a polyline mark in polar coordinates.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Polar (Scatter)':
        st.image('polar_scatter.png')
        st.markdown('In a polar scatter plot, each row of data_frame is represented by a symbol mark in polar coordinates.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Scatter':
        st.image('scatter_plot.png')
        st.markdown('In a scatter plot, each row of data_frame is represented by a symbol mark in 2D space.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Scatter Matrix':
        st.image('scatter_matrix.png')
        st.markdown('In a scatter plot matrix (or SPLOM), each row of data_frame is represented by a multiple symbol marks, one in each cell of a grid of 2D scatter plots, which plot each pair of dimensions against each other.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Strip':
        st.image('strip_plot.png')
        st.markdown('In a strip plot each row of data_frame is represented as a jittered mark within categories.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Sunburst':
        st.image('sunburst.png')
        st.markdown('A sunburst plot represents hierarchial data as sectors laid out over several levels of concentric rings.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Treemap':
        st.image('treemap.png')
        st.markdown('A treemap plot represents hierarchical data as nested rectangular sectors.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Violin':
        st.image('violin_plot.png')
        st.markdown('In a violin plot, rows of data_frame are grouped together into a curved mark to visualize their distribution.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')

    if my_type == 'Scatter Geo':
        st.image('scatter_geo.png')
        st.markdown('In a geographic scatter plot, each row of data_frame is represented by a symbol mark on a map.')
        st.write('')
        st.caption(
            'Note: Plot descriptions taken from [plotly.express](https://plotly.com/python-api-reference/generated/plotly.express.area.html)')




