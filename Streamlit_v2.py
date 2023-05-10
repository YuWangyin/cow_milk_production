import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import chardet
import openpyxl
import streamlit as st
import os
from io import StringIO
from PIL import Image
from io import BytesIO
import io
import scipy
import plotly.figure_factory as ff

#################################################################################
coloums_ID=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
coloumsName_ID=['Порода','Регион','Хозяйство','Район','Категория хоз-ва','Кличка','Идентиф-ый №','Инвентарный №','Линия','Дата рождения','Группа','Назначение','Fin №  лактации','Fin Удой, кг','Fin Жир , %','Белок , %','Max №  лактации','Max Удой, кг','Max Жир , %','Max Белок , %','Отец Кличка ','Отец Порода ','Отец Идентиф-ый №','Отец Инвентарный №','Мать Кличка ','Мать Порода ','Мать Идентиф-ый №','Мать Инвентарный №']
st.set_option('deprecation.showPyplotGlobalUse', False)


###############################################################################
# markdown
st.markdown('Made by Yu Wangyin and Thai-khoo')
# 设置网页标题 Set page title
st.title('Data visualization analysis of milk production of cows on the farm')


# 在左侧栏中添加一个文本输入框 Add a text input box to the left column
file_path = st.sidebar.text_input('Entry file Path', 'C:\\path\\to\\files')

# 列出指定路径下的所有文件 List all files under the specified path
files = os.listdir(file_path)

# 在下拉菜单中显示所有文件 Show all files in dropdown menu
selected_file = st.sidebar.selectbox('Choose file', files)

# 添加一个“确认”按钮 Add a "Confirm" button
if st.sidebar.button('confirm'):
    # 打开所选文件 # open the selected file
    path_file=os.path.join(file_path, selected_file)

    # 读取Excel文件，并将前三行作为索引 Read the Excel file and use the first three rows as indexes
    # 读取Excel文件，并检测编码格式 Read the Excel file and detect the encoding format
    df = pd.read_excel(path_file, sheet_name='Лист1', header=2)
    #df.set_index(df.columns[0], inplace=True)

##########################################################################################################################
st.header('1.Read the file and view data')
# 显示数据框信息 Display data frame information
with st.beta_expander("NumberID with Column Name"):
    st.text('We chose to use numeric IDs as column names for ease of management.')
    for i in range(len(coloums_ID)):
        st.write(coloums_ID[i]+'============'+coloumsName_ID[i])


st.text('Data are as follows: ')
# 显示数据 Display Data
st.dataframe(df)

# 显示数据框信息 Display dataframe information
with st.beta_expander("data information"):
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.write(info_str)

st.text('Most of the data are strings and a few are numbers.\nA lot of data is missing.')



###################################################################################################
st.header('2.Show missing values for each set of data')
# 绘制柱状图显示每列缺失值数量 Draw a histogram showing the number of missing values in each column
fig, ax = plt.subplots(dpi=200,figsize=(12,6))
ax = df.isnull().sum().plot(kind='bar', title='Missing values by column', width=0.7)
bar_space = 0.3
plt.rcParams.update({'font.size': 12})

# 遍历每个柱子，在上方添加数值 Iterate through each column, adding values above
for i, v in enumerate(df.isnull().sum()):
    ax.text(i, v+10, str(v), horizontalalignment='center')

plt.title('Missing Values by Column')
plt.xlabel('Columns')
plt.ylabel('Number of Missing Values')
plt.tight_layout()

# 将Matplotlib图形嵌入Streamlit应用程序中 # Embed Matplotlib graphics into Streamlit applications
st.pyplot(fig)

st.text('Some groups have more missing values. \nOperations such as removing duplicate rows and cleaning missing values will be performed.')

# 去除重复行 remove duplicate rows
df = df.drop_duplicates()


# 清除缺失值 Clear missing values
df1 = df.dropna(subset=['14', '15', '16', '18', '19', '20'])


# 显示数据框信息 Display dataframe information
with st.beta_expander("data information after clean"):
    buffer = StringIO()
    df1.info(buf=buffer)
    info_str = buffer.getvalue()
    st.write(info_str)


# 显示DataFrame的描述性统计信息 Display descriptive statistics for a DataFrame
st.write(df1.describe())

st.text('The cleaned data has 874 samples.')




st.header('3.Find correlations in data')
st.text('In order to find potential regression relationships.')
#寻找相关性 find correlation
#поиск корреляций

sns.pairplot(df1)
# 显示图表 show chart
st.pyplot()
st.text('There is likely to be a linear regression relationship \nbetween the data of the Fin milk production and Max milk production.')
# Jointplot
# Комбинация гистограмм и диаграмм рассеивания.
sns.jointplot(x='18', y='14', data=df1,)
st.pyplot()
sns.jointplot(x='18', y='14', data=df1, kind="hex")
st.pyplot()
sns.jointplot(x='18', y='14', data=df1, kind="kde")
st.pyplot()
st.text('It is not difficult to see that the maximum milk production and the last production are highly correlated.  \nBecause the highest milk yield of most dairy cows is the last milk yield.  \nMost of the time, we can use the maximum milk production instead of the last milk production.')






st.header('4.View the string classification information in each column')
# 设置分类标准 set classification criteria

st.text('In order to show the major groups under each column classification.')

Categories = ['1', '2', '3', '4', '5','9','11','22']
for i in Categories:
    st.write('No.'+i+' '+coloumsName_ID[coloums_ID.index(i)]+' ====== '+str(df1[i].unique()))
st.text('The sample of the mother cow was not used because it was too single.\nAlmost all Бестужевская')


##############################################################################################
st.header('4.Data visualization')
st.text('In order to find out which groups are better.')
times=1
for i in Categories:
    st.write(str(times)+'. '+coloumsName_ID[coloums_ID.index(i)]+' и Max Удой, кг')
    times+=1
    # 获取指定列的唯一值列表 Get a list of unique values for the specified column
    categories = df1.iloc[:, coloums_ID.index(i)].unique()
    st.write(categories)


    # 配置Seaborn样式 Configure Seaborn styles
    sns.set(style="whitegrid")
    hist_data=[]
    # 遍历每个分类 iterate over each category
    for category in categories:
        # 筛选出该分类的数据 Filter out the data for this category
        data = df1[df1.iloc[:, coloums_ID.index(i)] == category]
        # 取出第18列的数据 Get the data in column 18
        values = data.iloc[:, 17]
        hist_data.append(values)

    fig=ff.create_distplot(hist_data,categories)

    # 显示图形 display graphics
    st.plotly_chart(fig, use_container_width=True)