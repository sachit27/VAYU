# Required  Packages
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

import pandas as pd
import csv
from datetime import datetime
from pathlib import Path

import plotly.express as px
import matplotlib.pyplot as plt
plt.style.use('seaborn')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn import metrics
import numpy as np
import seaborn as sns


# Class to display plotting canvas
class CorrelationCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 11, height = 9, dpi = 130):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 7, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

class LR_Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 7, height = 12, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

class Plotting_Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 1.5, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

# ---FileConversion class Starts---
class FileConversion(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 780
        height = 310
        title = 'File Conversion'
        self.excelFileName = ''
        self.fc_browse_file_flag = False

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)

        self.MyUI()

    def MyUI(self):

        label_2 = QLabel("Convert Excel To CSV",self)
        label_2.setGeometry(QtCore.QRect(270, 10, 270, 31))
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        label_2.setFont(font)
        label_2.setObjectName("label_2")


        label_3 = QLabel("Browse .xlsx file",self)
        label_3.setGeometry(120, 70, 121, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        label_3.setFont(font)

        file1_browse_btn = QPushButton("Browse",self)
        file1_browse_btn.setGeometry(230, 70, 291, 31)
        file1_browse_btn.clicked.connect(self.da_fileOpener)


        self.data_file_back_btn = QPushButton("Back",self)
        self.data_file_back_btn.setGeometry(600, 185, 121, 31)
        self.data_file_back_btn.clicked.connect(self.backToMainWindow)



        self.selec_file_lbl = QLabel("Selected .xlsx File",self)
        self.selec_file_lbl.setGeometry(QtCore.QRect(120, 110, 401, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.selec_file_lbl.setFont(font)

        file_conversion_button = QtWidgets.QPushButton("Convert To CSV File",self)
        file_conversion_button.setGeometry(110, 185, 411, 31)
        file_conversion_button.clicked.connect(self.fc_action)

    def backToMainWindow(self):
        self.close()

    def da_fileOpener(self):
        fname = QFileDialog.getOpenFileName(filter="Excel Files (*.xlsx)")
        self.excelFileName = fname[0]

        self.selec_file_lbl.setText("Selected .xlsx File Path : " + str(fname[0]))
        self.selec_file_lbl.setStyleSheet('color : green')

        if len(self.excelFileName) > 0:
            self.fc_browse_file_flag = True

    def fc_action(self):

        if self.fc_browse_file_flag == True:
            read_file = pd.read_excel (self.excelFileName)
            read_file.to_csv (r'dataset_csv_file.csv', index = None, header=True)
            da_no_file_input = QMessageBox()
            da_no_file_input.setIcon(QMessageBox.Information)
            da_no_file_input.setWindowTitle("Message")
            da_no_file_input.setText("File successfully converted and save it as dataset_csv_file.csv")
            da_no_file_input.exec_()

        else:
            da_no_file_input = QMessageBox()
            da_no_file_input.setIcon(QMessageBox.Critical)
            da_no_file_input.setWindowTitle("Action Not Possible")
            da_no_file_input.setText("Please input MS Excel file for converting into Comma Seperated Version file")
            da_no_file_input.exec_()

# ---FileConversion class Ends---

# ---DataInterpolation class Starts----
class DataInterpolationWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 540
        height = 318
        title = 'Data Interpolation'
        self.csvFileName = ''
        self.interpolated_data_frame = {}

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)
        self.MyUI()

    def MyUI(self):

        self.label_2 = QtWidgets.QLabel("Data Interpolation",self)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 181, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame()
        self.line.setGeometry(QtCore.QRect(60, 30, 401, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_3 = QtWidgets.QLabel("Enter .csv file",self)
        self.label_3.setGeometry(QtCore.QRect(60, 50, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.browse_file_btn = QtWidgets.QPushButton("Browse",self)
        self.browse_file_btn.setGeometry(QtCore.QRect(150, 50, 311, 31))
        self.browse_file_btn.setObjectName("browse_file_btn")

        self.data_interpolation_btn = QtWidgets.QPushButton("Data Interpolation",self)
        self.data_interpolation_btn.setGeometry(QtCore.QRect(60, 120, 401, 31))
        self.data_interpolation_btn.setObjectName("data_interpolation_btn")

        self.data_intrplt_back_btn = QtWidgets.QPushButton("Back",self)
        self.data_intrplt_back_btn.setGeometry(QtCore.QRect(10, 210, 121, 41))
        self.data_intrplt_back_btn.setObjectName("data_intrplt_back_btn")
        self.data_intrplt_back_btn.clicked.connect(self.DataInterpolationackButton)

        self.download_csv_file_btn = QtWidgets.QPushButton("Download CSV File",self)
        self.download_csv_file_btn.setGeometry(QtCore.QRect(60, 160, 401, 31))
        self.download_csv_file_btn.setObjectName("download_csv_file_btn")

        self.selected_label = QtWidgets.QLabel("Selected .csv File Path",self)
        self.selected_label.setGeometry(QtCore.QRect(60, 90, 401, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.selected_label.setFont(font)
        self.selected_label.setObjectName("selected_label")

        self.download_csv_file_btn.clicked.connect(self.downloadFile)
        self.browse_file_btn.clicked.connect(self.fileOpener)
        self.data_interpolation_btn.clicked.connect(self.interpolation_action)

    def DataInterpolationackButton(self):
        self.close()


    def fileOpener(self):
        fname = QFileDialog.getOpenFileName(filter="Comma Seperated Files (*.csv)")
        self.csvFileName = fname[0]
        self.selected_label.setText("Selected .csv File Path : " + str(fname[0]))
        self.selected_label.setStyleSheet('color : red')

    def _toCSV(self,data_frame,csvFilePath):
        data_frame.to_csv(csvFilePath)

    def downloadFile(self):

        ''' Function for downloading the file '''
        if len(self.interpolated_data_frame) == 0:
            no_input_message_box = QMessageBox()
            no_input_message_box.setIcon(QMessageBox.Critical)
            no_input_message_box.setWindowTitle("Alert!")
            no_input_message_box.setText("Please you need to perform Data Interpolation then you are able to download .csv file")
            x = no_input_message_box.exec_()
        else:
            fileName = self.create_csv_file_name()
            self._toCSV(self.interpolated_data_frame,fileName)

            csvFileAfter_message_box = QMessageBox()
            csvFileAfter_message_box.setIcon(QMessageBox.Information)
            csvFileAfter_message_box.setWindowTitle("Congratulations!")
            csvFileAfter_message_box.setText("Interpolated dataset file saves at " + fileName)
            csvFileAfter_message_box.exec_()


    def create_csv_file_name(self):
        now = datetime.now() # current date and time
        path = str(os.getcwd())
        path += '/'
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        date_time = date_time.replace(":","_")
        date_time = date_time.replace(" ","")
        date_time = date_time.replace(",","")
        date_time = date_time.replace("/","_")
        date_time += '_data.csv'
        path += date_time
        path = path.replace('/','\\')
        return path

    def interpolation_action(self):
        ''' Function for performing interpolation '''
        if len(self.csvFileName) == 0:
            no_input_message_box = QMessageBox()
            no_input_message_box.setIcon(QMessageBox.Critical)
            no_input_message_box.setWindowTitle("Alert!")
            no_input_message_box.setText("Please Input .csv file for dataset!!")
            x = no_input_message_box.exec_()
        else:

            df = pd.read_csv(self.csvFileName)
            cdf = df.dropna(how='all')
            ndf = cdf.interpolate()
            self.interpolated_data_frame = ndf

            sucs_message_box = QMessageBox()
            sucs_message_box.setIcon(QMessageBox.Information)
            sucs_message_box.setWindowTitle("Congratulations!")
            sucs_message_box.setText("Dataset is successfully Interpolated...")
            sucs_message_box.exec_()
# ---DataInterpolation class Ends---

# ---Data Aggregation class Starts---
class DataAggregation(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 780
        height = 400
        title = 'Data Aggregation'
        self.csvFileName = ''
        self.da_browse_file_flag = False

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)

        self.MyUI()

    def MyUI(self):


        label_2 = QLabel("Data Aggregation",self)
        label_2.setGeometry(QtCore.QRect(240, 10, 221, 31))
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        label_2.setFont(font)
        label_2.setObjectName("label_2")

        label_3 = QLabel("Browse .csv file",self)
        label_3.setGeometry(120, 70, 121, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_3.setFont(font)

        file1_browse_btn = QPushButton("Browse",self)
        file1_browse_btn.setGeometry(230, 70, 291, 31)
        file1_browse_btn.clicked.connect(self.da_fileOpener)


        self.data_file_back_btn = QPushButton("Back",self)
        self.data_file_back_btn.setGeometry(600, 260, 121, 41)
        self.data_file_back_btn.clicked.connect(self.DataAggregationBackButton)


        heading_label = QLabel("NOTE :- You must browse .csv file after performing Data Interpolation",self)
        heading_label.setGeometry(120, 40, 441, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        heading_label.setFont(font)

        self.selec_file_lbl = QLabel("Selected .csv File",self)
        self.selec_file_lbl.setGeometry(QtCore.QRect(120, 110, 401, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.selec_file_lbl.setFont(font)

        label_7 = QtWidgets.QLabel("Enter Column name",self)
        label_7.setGeometry(QtCore.QRect(120, 150, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_7.setFont(font)

        self.file_x = QLineEdit(self)
        self.file_x.setGeometry(320, 150, 200, 20)
        self.file_x.adjustSize()

        label_8 = QtWidgets.QLabel("Select the type of Resampling",self)
        label_8.setGeometry(110, 190, 175, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_8.setFont(font)

        self.resampling_type_comboBox = QComboBox(self)
        self.resampling_type_comboBox.setGeometry(310, 190, 210, 22)
        self.resampling_type_comboBox.addItems(['Hourly basis','Daily basis','Monthly basis'])
        self.resampling_type_comboBox.adjustSize()

        label_9 = QtWidgets.QLabel("Select Resampling Calculation type",self)
        label_9.setGeometry(110, 240, 175, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_9.setFont(font)

        self.calculation_type_comboBox = QComboBox(self)
        self.calculation_type_comboBox.setGeometry(310, 240, 210, 22)
        self.calculation_type_comboBox.addItems(['Mean','Median','Sum','Standard Deviation'])
        self.calculation_type_comboBox.adjustSize()


        data_aggregation = QtWidgets.QPushButton("Data Aggregation",self)
        data_aggregation.setGeometry(110, 320, 411, 31)
        data_aggregation.clicked.connect(self.da_action)

    def DataAggregationBackButton(self):
        self.close()

    def checkColumns(self,x,df):

        count = 0
        cols_list = list(df.columns)
        if x in cols_list:
            count += 1

        if count == 1:
            return True
        else:
            return False

    def da_fileOpener(self):
        fname = QFileDialog.getOpenFileName(filter="Comma Seperated Files (*.csv)")
        self.csvFileName = fname[0]

        self.selec_file_lbl.setText("Selected .csv File Path : " + str(fname[0]))
        self.selec_file_lbl.setStyleSheet('color : green')

        if len(self.csvFileName) > 0:
            self.da_browse_file_flag = True

    def da_action(self):

        new_df_csv_fileName = ''
        df = pd.read_csv(self.csvFileName)
        if self.da_browse_file_flag == True:
            x_var = str(self.file_x.text())

            resample_opt = str(self.resampling_type_comboBox.currentText())
            calc_opt = str(self.calculation_type_comboBox.currentText())

            if len(x_var) > 0 and self.checkColumns(x_var,df) == True:
                # just re-read the dataframe and convert to DateTimeIndex
                ndf = pd.read_csv(self.csvFileName,parse_dates=[x_var],index_col=x_var)

                if resample_opt == 'Hourly basis':
                    if calc_opt == 'Mean':

                        mean_df = ndf.resample('H').mean()
                        mean_df.to_csv (r'Data_Aggregation_Mean_HourlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Mean_HourlyBasis_dataframe.csv'

                    elif calc_opt == 'Median':

                        md_df = ndf.resample('H').median()
                        md_df.to_csv (r'Data_Aggregation_Median_HourlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Median_HourlyBasis_dataframe.csv'

                    elif calc_opt == 'Sum':

                        sum_df = ndf.resample('H').sum()
                        sum_df.to_csv (r'Data_Aggregation_Sum_HourlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Sum_HourlyBasis_dataframe.csv'

                    elif calc_opt == 'Standard Deviation':

                        std_df = ndf.resample('H').std()
                        std_df.to_csv (r'Data_Aggregation_StandardDeviation_HourlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_SumDeviation_HourlyBasis_dataframe.csv'

                elif resample_opt == 'Daily basis':
                    if calc_opt == 'Mean':

                        mean_df = ndf.resample('D').mean()
                        mean_df.to_csv (r'Data_Aggregation_Mean_DailyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Mean_DailyBasis_dataframe.csv'

                    elif calc_opt == 'Median':

                        md_df = ndf.resample('D').median()
                        md_df.to_csv (r'Data_Aggregation_Median_DailyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Median_DailyBasis_dataframe.csv'

                    elif calc_opt == 'Sum':

                        sum_df = ndf.resample('D').sum()
                        sum_df.to_csv (r'Data_Aggregation_Sum_DailyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Sum_DailyBasis_dataframe.csv'

                    elif calc_opt == 'Standard Deviation':

                        std_df = ndf.resample('D').std()
                        std_df.to_csv (r'Data_Aggregation_StandardDeviation_DailyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_SumDeviation_DailyBasis_dataframe.csv'

                elif resample_opt == 'Monthly basis':
                    if calc_opt == 'Mean':

                        mean_df = ndf.resample('M').mean()
                        mean_df.to_csv (r'Data_Aggregation_Mean_MonthlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Mean_MonthlyBasis_dataframe.csv'

                    elif calc_opt == 'Median':

                        md_df = ndf.resample('M').median()
                        md_df.to_csv (r'Data_Aggregation_Median_MonthlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Median_MonthlyBasis_dataframe.csv'

                    elif calc_opt == 'Sum':

                        md_df = ndf.resample('M').sum()
                        md_df.to_csv (r'Data_Aggregation_Sum_MonthlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_Sum_MonthlyBasis_dataframe.csv'

                    elif calc_opt == 'Standard Deviation':

                        md_df = ndf.resample('M').std()
                        md_df.to_csv (r'Data_Aggregation_StandardDeviation_MonthlyBasis_dataframe.csv', index = True, header=True)
                        new_df_csv_fileName = 'Data_Aggregation_StandardDeviation_MonthlyBasis_dataframe.csv'

                csv_File_Storage = QMessageBox()
                csv_File_Storage.setIcon(QMessageBox.Information)
                csv_File_Storage.setWindowTitle("Message")
                csv_File_Storage.setText("Data frame is successfully aggregated and stored into a new file " + new_df_csv_fileName)
                csv_File_Storage.exec_()

            else:
                da_zero_input = QMessageBox()
                da_zero_input.setIcon(QMessageBox.Critical)
                da_zero_input.setWindowTitle("Action Not Possible")
                da_zero_input.setText("The variable you entered isn't match with the set of columns in dataset.")
                da_zero_input.exec_()
        else:
            da_no_file_input = QMessageBox()
            da_no_file_input.setIcon(QMessageBox.Critical)
            da_no_file_input.setWindowTitle("Action Not Possible")
            da_no_file_input.setText("Please input .csv file for dataset")
            da_no_file_input.exec_()
# ---Data Aggregation class Ends---

# Data Correlation Class starts
class DataCorrelation(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 710
        height = 320
        title = 'Data Correlation'

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)

        self.MyUI()

    def MyUI(self):


        self.csvFileName = ''
        self.data_correlation_browse_file_flag = False

        label_2 = QLabel("Data Correlation",self)
        label_2.setGeometry(200, 10, 181, 21)
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        label_2.setFont(font)
        self.line = QFrame(self)
        self.line.setGeometry(40, 30, 471, 20)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        label_3 = QtWidgets.QLabel("Enter .csv file",self)
        label_3.setGeometry(QtCore.QRect(50, 70, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_3.setFont(font)

        method_selection_variable = QLabel("Select Data Correlation Type",self)
        method_selection_variable.setGeometry(500,100,220,40)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        method_selection_variable.setFont(font)

        self.method_selection_box = QComboBox(self)
        self.method_selection_box.setGeometry(500,140,180,30)
        self.method_selection_box.addItems(['Pearson Correlation','Kendall Tau Correlation','Spearman Correlation'])

        data_correlation_browse_button = QtWidgets.QPushButton("Browse",self)
        data_correlation_browse_button.setGeometry(150, 70, 311, 31)
        data_correlation_browse_button.clicked.connect(self.fileOpener)


        data_correlation = QPushButton("Data Correlation",self)
        data_correlation.setGeometry(50, 140, 411, 31)
        data_correlation.clicked.connect(self.data_correlation_action)

        self.data_correlation_back_btn = QPushButton("Back",self)
        self.data_correlation_back_btn.setGeometry(QtCore.QRect(30, 250, 121, 41))
        self.data_correlation_back_btn.clicked.connect(self.DataCorrelationBackButton)



        heading_label = QLabel("NOTE :- You must browse .csv file after performing Data Interpolation",self)
        heading_label.setGeometry(80, 30, 441, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        heading_label.setFont(font)

        self.data_corr_slec_label = QLabel("Selected .csv File Path ",self)
        self.data_corr_slec_label.setGeometry(50, 110, 401, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.data_corr_slec_label.setFont(font)


    def fileOpener(self):

        fname = QFileDialog.getOpenFileName(filter="Comma Seperated Files (*.csv)")
        self.csvFileName = fname[0]

        self.data_corr_slec_label.setText("Selected .csv File Path : " + str(fname[0]))
        self.data_corr_slec_label.setStyleSheet('color : green')

        if len(self.csvFileName) > 0:
            self.data_correlation_browse_file_flag = True

    def DataCorrelationBackButton(self):
        self.close()

    def data_correlation_action(self):
        if self.data_correlation_browse_file_flag == False and len(self.csvFileName) == 0:

            data_summary_zero_input = QMessageBox()
            data_summary_zero_input.setIcon(QMessageBox.Critical)
            data_summary_zero_input.setWindowTitle("Action Not Possible")
            data_summary_zero_input.setText("Please input .csv file.")
            data_summary_zero_input.exec_()
        else:
            df = pd.read_csv(self.csvFileName)

            if str(self.method_selection_box.currentText()) == 'Pearson Correlation':
                m = 'pearson'
            elif str(self.method_selection_box.currentText()) == 'Kendall Tau Correlation':
                m = 'kendall'
            elif str(self.method_selection_box.currentText()) == 'Spearman Correlation':
                m = 'spearman'

            corr = df.corr(method=m)
            corr = corr.round(decimals=2)
            corr.to_csv('correlation_matrix.csv')


            plt.figure(figsize=(13, 13))
            data_corr_map = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap='BrBG')
            data_corr_map.figure.savefig('data_corr_output_fig.png')
            data_corr_img_save = QMessageBox()
            data_corr_img_save.setIcon(QMessageBox.Information)
            data_corr_img_save.setWindowTitle("Message")

            import numpy as np
            numpy_array = corr.to_numpy()
            np.savetxt("data_correlation_matrix.txt", numpy_array, fmt = "%d")

            if m == 'pearson':
                data_corr_img_save.setText("You have successfully performed Pearson Data Correlation. Image saved as data_corr_output_fig.png and Correlation Matrix is saved as data_correlation_matrix.txt")
            elif m == 'kendall':
                data_corr_img_save.setText("You have successfully performed Kendall Data Correlation. Image saved as data_corr_output_fig.png and Correlation Matrix is saved as data_correlation_matrix.txt")
            elif m == 'spearman':
                data_corr_img_save.setText("You have successfully performed Spearman Data Correlation. Image save as data_corr_output_fig.png and Correlation Matrix is saves as data_correlation_matrix.txt")

            data_corr_img_save.exec_()
# Data Correlation Class Ends

# data File Plotting Class Start

class dataFilePlotting(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 765
        height = 350

        title = 'Visualization'
        self.csvFileName = ''
        self.sfp_browse_file_flag = False

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width,height)

        self.MyUI()

    def MyUI(self):

        label_2 = QLabel("Visualization",self)
        label_2.setGeometry(QtCore.QRect(240, 10, 161, 31))
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        label_2.setFont(font)
        label_2.setObjectName("label_2")

        label_3 = QLabel("Browse .csv file",self)
        label_3.setGeometry(120, 70, 121, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)

        file1_browse_btn = QPushButton("Browse",self)
        file1_browse_btn.setGeometry(230, 70, 291, 31)
        file1_browse_btn.clicked.connect(self.sfp_fileOpener)


        self.data_file_back_btn = QPushButton("Back",self)
        self.data_file_back_btn.setGeometry(740, 510, 111, 41)
        self.data_file_back_btn.clicked.connect(self.BackButtonSF)

        heading_label = QLabel("NOTE :- You should select a .csv file",self)
        heading_label.setGeometry(120, 40, 441, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        heading_label.setFont(font)

        self.selec_file_lbl = QLabel("Selected .csv File",self)
        self.selec_file_lbl.setGeometry(QtCore.QRect(120, 110, 401, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.selec_file_lbl.setFont(font)

        label_7 = QLabel("Select X-axis variable",self)
        label_7.setGeometry(120, 150, 131, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_7.setFont(font)


        self.file_x_comboBox = QComboBox(self)
        self.file_x_comboBox.setGeometry(250, 150, 271, 20)
        self.file_x_comboBox.adjustSize()

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(250, 230, 271, 22)


        self.comboBox.addItem('Scatter Plot')
        self.comboBox.addItem('Line Plot')
        self.comboBox.addItem('Bar Plot')
        self.comboBox.adjustSize()

        label_8 = QtWidgets.QLabel("Select Graph Plotting",self)
        label_8.setGeometry(110, 230, 131, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_8.setFont(font)

        graph_plot_data_file = QtWidgets.QPushButton("Plot",self)
        graph_plot_data_file.setGeometry(540, 210, 190, 31)
        graph_plot_data_file.clicked.connect(self.sfp_action)

        label_9 = QLabel("Select Y-axis variable",self)
        label_9.setGeometry(120, 190, 131, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_9.setFont(font)

        self.file_y_comboBox = QComboBox(self)
        self.file_y_comboBox.setGeometry(250, 190, 271, 20)
        self.file_y_comboBox.adjustSize()

    def BackButtonSF(self):
        self.close()

    def checkColumns(self,x,y,df):

        count = 0
        cols_list = list(df.columns)
        if x == y:
            return False
        else:
            if x in cols_list:
                count += 1
            if y in cols_list:
                count += 1

            if count <= 1:
                return False
            else:
                return True

    def sfp_fileOpener(self):
        fname = QFileDialog.getOpenFileName(filter="Comma Seperated Files (*.csv)")
        self.csvFileName = fname[0]

        self.selec_file_lbl.setText("Selected .csv File Path : " + str(fname[0]))
        self.selec_file_lbl.setStyleSheet('color : green')


        if len(self.csvFileName) > 0:
            self.sfp_browse_file_flag = True

        df = pd.read_csv(self.csvFileName)

        self.file_x_comboBox.clear()
        self.file_y_comboBox.clear()

        self.file_x_comboBox.addItems(list(df.columns))
        self.file_y_comboBox.addItems(list(df.columns))

    def sfp_action(self):
        if self.sfp_browse_file_flag == True:
            df = pd.read_csv(self.csvFileName)

            x_var = str(self.file_x_comboBox.currentText())
            y_var = str(self.file_y_comboBox.currentText())

            if len(x_var) > 0 and len(y_var) > 0 and self.checkColumns(x_var,y_var,df) == True:
                option = self.comboBox.currentText()
                if self.checkColumns(x_var,y_var,df) == True:
                    X = df[x_var]
                    Y = df[y_var]
                    if option == 'Scatter Plot':

                        fig = px.scatter(df, X, Y)
                        fig.show()
                        fig.write_html('scatter_plot.html')
                        fig.write_image('scatter_plot.png')

                        scatter_plotting_graph_mgsBox = QMessageBox()
                        scatter_plotting_graph_mgsBox.setIcon(QMessageBox.Information)
                        scatter_plotting_graph_mgsBox.setWindowTitle("Message")
                        scatter_plotting_graph_mgsBox.setText("You have successfully performed Scatter Plotting and the plot is saved as scatter_plotting_graph.png")
                        scatter_plotting_graph_mgsBox.exec_()

                    elif option == 'Line Plot':

                        fig = px.line(df, X, Y)
                        fig.show()
                        fig.write_html('line_plotting_graph.html')
                        fig.write_image('line_plotting_graph.png')

                        line_plotting_graph_mgsBox = QMessageBox()
                        line_plotting_graph_mgsBox.setIcon(QMessageBox.Information)
                        line_plotting_graph_mgsBox.setWindowTitle("Message")
                        line_plotting_graph_mgsBox.setText("You have successfully performed Line Plotting and the plot is saved self.assert_(boolean expression, 'message') line_plotting_graph.png")
                        line_plotting_graph_mgsBox.exec_()

                    elif option == 'Bar Plot':
                            fig = px.bar(df, X, Y)
                            fig.show()
                            fig.write_html('bar_plot.html')
                            fig.write_image('bar_plot.png')

                            line_plotting_graph_mgsBox = QMessageBox()
                            line_plotting_graph_mgsBox.setIcon(QMessageBox.Information)
                            line_plotting_graph_mgsBox.setWindowTitle("Message")
                            line_plotting_graph_mgsBox.setText("You have successfully performed Bar Plotting and the plot is saved self.assert_(boolean expression, 'message') bar_plot.png")
                            line_plotting_graph_mgsBox.exec_()

            else:
                sfp_zero_input = QMessageBox()
                sfp_zero_input.setIcon(QMessageBox.Critical)
                sfp_zero_input.setWindowTitle("Action Not Possible")
                sfp_zero_input.setText("Please enter X-axis and Y-axis variables for dataset. The variable you choose for data visualization must not match to each other.")
                sfp_zero_input.exec_()

        else:
            sfp_no_file_input = QMessageBox()
            sfp_no_file_input.setIcon(QMessageBox.Critical)
            sfp_no_file_input.setWindowTitle("Action Not Possible")
            sfp_no_file_input.setText("Please input .csv file for dataset")
            sfp_no_file_input.exec_()

# data File Plotting Class End
# Linear Regression Class Start

class LinearRegression(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 865
        height = 700
        title = 'Linear Regression'
        self.csvFileName = ''
        self.lr_browse_flag = False
        self.linear_regression_action_flag = False

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)
        self.MyUI()

    def MyUI(self):

        self.canvas = LR_Canvas(self, width=6.4, height=3.67)
        self.canvas.move(100,280)
        self.plotting_file_name = ''

        label_2 = QtWidgets.QLabel("Linear Regression",self)
        label_2.setGeometry(230, 10, 221, 21)
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        label_2.setFont(font)
        line = QFrame(self)
        line.setGeometry(30, 30, 531, 20)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        label_3 = QLabel("Enter .csv file",self)
        label_3.setGeometry(QtCore.QRect(60, 70, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_3.setFont(font)
        browse_file_btn = QtWidgets.QPushButton("Browse",self)
        browse_file_btn.setGeometry(150, 70, 411, 31)
        browse_file_btn.clicked.connect(self.fileOpener)

        graph_plotting_lbl = QLabel("Select X-Axis variable for graph plotting",self)
        graph_plotting_lbl.setGeometry(600,110,250,30)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        graph_plotting_lbl.setFont(font)

        self.graph_plot_select_option = QComboBox(self)
        self.graph_plot_select_option.setGeometry(600,150,200,30)

        linear_regression_btn = QPushButton("Linear Regression",self)
        linear_regression_btn.setGeometry(60, 190, 181, 41)
        linear_regression_btn.clicked.connect(self.linear_regression_action)
        label_4 = QLabel("NOTE :- You must browse .csv file after performing Data Interpolation",self)
        label_4.setGeometry(80, 30, 441, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_4.setFont(font)
        self.lr_target_col_field = QTextEdit("",self)
        self.lr_target_col_field.setGeometry(260, 110, 301, 31)
        label_8 = QLabel("Enter X-axis Variable(s) in dataset",self)
        label_8.setGeometry(60, 160, 200, 21)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_8.setFont(font)
        self.lr_input_independent_cols = QPlainTextEdit(self)
        self.lr_input_independent_cols.setGeometry(260, 150, 301, 81)

        self.lr_windowback_btn = QPushButton("Back",self)
        self.lr_windowback_btn.setGeometry(740, 510, 111, 41)
        self.lr_windowback_btn.clicked.connect(self.Back_LR)

        label_9 = QLabel("Enter Y-axis Variable in dataset",self)
        label_9.setGeometry(QtCore.QRect(60, 110, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        label_9.setFont(font)
        self.lr_help_btn = QPushButton("Help",self)
        self.lr_help_btn.setGeometry(580, 230, 111, 41)
        self.lr_help_btn.clicked.connect(self.help_dialog_box)

    def Back_LR(self):
        self.close()

    def removeEspecial(self,l):

        lister = []
        for word in l:
            if len(word) > 0:
                data = str(word)
                data = data.lstrip()
                data = data.rstrip()
                lister.append(data)
        return lister

    def perform_linear_regression(self,X_variables,y_variable,X_axis,X_plot_var):

        model_output_list = []

        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_squared_error

        reg = LinearRegression()

        reg.fit(X_variables,y_variable)
        Y_pred = reg.predict(X_variables)

        r2_score = reg.score(X_variables , y_variable)
        model_output_list.append(r2_score)


        self.canvas.axes.clear()

        self.canvas.axes.scatter(X_axis,y_variable,c=['red'],label='Sample Data')
        self.canvas.axes.plot(X_axis,Y_pred,color='blue',label='Regression Line')
        self.canvas.axes.set_xlabel(X_plot_var)
        self.canvas.axes.legend()
        self.canvas.axes.text(0.5, 0.15, '$y = %.2f x_1 - %.2f $' % (reg.coef_[0], abs(reg.intercept_)), fontsize=12,transform=self.canvas.axes.transAxes)
        self.canvas.draw()

        plt.scatter(X_axis,y_variable,c=['red'])
        plt.plot(X_axis,Y_pred,color='blue')
        plt.xlabel(X_plot_var)
        plt.legend(['Sample Data','Regression Line'],loc="lower right")


        plt.title('Linear Regression Plotting Graph')
        self.plotting_file_name = 'linear_regression_image_' +str(X_plot_var)+'.png'
        plt.savefig(self.plotting_file_name)

        image_save_pltBox = QMessageBox()
        image_save_pltBox.setIcon(QMessageBox.Information)
        image_save_pltBox.setWindowTitle("Message")
        image_save_pltBox.setText("You successfully performed Scatter Plotting and the plot is saved as "+self.plotting_file_name)
        image_save_pltBox.exec_()

        return model_output_list

    def write_details_to_file(self,independent_variables,target_vars,algorithm_details):

        ''' this function is used to write the details in a .txt file. '''

        text_file = open('Linear Regression Algorithm Details','w')

        text_file.write('Dataset File Path : ' + str(self.csvFileName))
        text_file.write('\n')

        text_file.write('Algorithm Type : Linear Regression')
        text_file.write('\n')

        text_file.write('Target variable : ' +target_vars)
        text_file.write('\n')

        text_file.write('Independent variable : '+str(independent_variables))
        text_file.write('\n')

        text_file.write('---------')
        text_file.write('\n')

        text_file.write('OUTPUT')
        text_file.write('\n')

        text_file.write('---------')
        text_file.write('\n')

        text_file.write('Model Accuracy : '+str(algorithm_details[0]))
        text_file.write('\n')


    def linear_regression_action(self):

        if self.lr_browse_flag == True:
            target_var = self.lr_target_col_field.toPlainText()

            target_var = target_var.lstrip()
            target_var = target_var.rstrip()

            independent_var = self.lr_input_independent_cols.toPlainText()
            lister_ivc = self.removeEspecial(independent_var.split('\n'))

            if len(target_var) > 0 and len(independent_var) > 0 and self.check_target_variable(target_var) == True and self.check_independent_variables(lister_ivc) == True:
                if target_var not in lister_ivc:

                    df = pd.read_csv(self.csvFileName)
                    X_variables = self.collectIndepedentVariables(df,lister_ivc)
                    results = self.perform_linear_regression(X_variables,df[[target_var]],df[[self.graph_plot_select_option.currentText()]],self.graph_plot_select_option.currentText())
                    self.write_details_to_file(independent_var,target_var,results)
                    self.linear_regression_action_flag = True

                    lr_performed = QMessageBox()
                    lr_performed.setIcon(QMessageBox.Information)
                    lr_performed.setWindowTitle("Congratulations!")
                    lr_performed.setText("You succesfully performed Linear Regression on dataset "+self.csvFileName+" , all details are saved inside Linear Regression Algorithm Details.txt")
                    lr_performed.exec_()

                else:
                    lr_same_input = QMessageBox()
                    lr_same_input.setIcon(QMessageBox.Critical)
                    lr_same_input.setWindowTitle("Action Not Possible")
                    lr_same_input.setText("Target variable must not match with the set of Independent variables you enter.")
                    lr_same_input.exec_()
            else:
                lr_zero_input = QMessageBox()
                lr_zero_input.setIcon(QMessageBox.Critical)
                lr_zero_input.setWindowTitle("Action Not Possible")
                lr_zero_input.setText("Please enter the independent and the target variables. These values are needed to run Linear Regression.")
                lr_zero_input.exec_()
        else:
            help_dialog_box = QMessageBox()
            help_dialog_box.setIcon(QMessageBox.Critical)
            help_dialog_box.setWindowTitle("Action Not Possible")
            help_dialog_box.setText("Please input .csv file for dataset")
            x = help_dialog_box.exec_()

    def help_dialog_box(self):
            ''' this is used to open the help dialog box '''

            help_dialog_box = QMessageBox()
            help_dialog_box.setIcon(QMessageBox.Information)
            help_dialog_box.setWindowTitle("Message")
            help_dialog_box.setText("Enter Independent Variable or Feature column in dataset file")
            x = help_dialog_box.exec_()

    def fileOpener(self):

        fname = QFileDialog.getOpenFileName(filter="Comma Seperated Files (*.csv)")
        self.csvFileName = fname[0]
        self.lr_browse_flag = True

        df = pd.read_csv(self.csvFileName)
        self.graph_plot_select_option.addItems(list(df.columns))

        csvFile_dialog_box = QMessageBox()
        csvFile_dialog_box.setIcon(QMessageBox.Information)
        csvFile_dialog_box.setWindowTitle("Message")
        csvFile_dialog_box.setText("Selected .csv dataset file " +self.csvFileName)
        y = csvFile_dialog_box.exec_()


    def check_target_variable(self,target_variable):

        df = pd.read_csv(self.csvFileName)
        try:
            column = df[target_variable]
            return True
        except KeyError:
            return False

    def collectIndepedentVariables(self,dataframe,I_var_list):
        # this function is used to collect X-axis or Independent variables from dataset .csv file .
        X_variables_list = []
        if len(I_var_list) == 1:
            X_variables_list = dataframe[[I_var_list[0]]]
        elif len(I_var_list) == 2:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1]]]
        elif len(I_var_list) == 3:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2]]]
        elif len(I_var_list) == 4:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3]]]
        elif len(I_var_list) == 5:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4]]]
        elif len(I_var_list) == 6:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5]]]
        elif len(I_var_list) == 7:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6]]]
        elif len(I_var_list) == 8:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7]]]
        elif len(I_var_list) == 9:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8]]]
        elif len(I_var_list) == 10:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9]]]
        elif len(I_var_list) == 11:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10]]]
        elif len(I_var_list) == 12:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11]]]
        elif len(I_var_list) == 13:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12]]]
        elif len(I_var_list) == 14:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12],I_var_list[13]]]
        elif len(I_var_list) == 15:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12],I_var_list[13],I_var_list[14]]]
        elif len(I_var_list) == 16:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12],I_var_list[13],I_var_list[14],I_var_list[15]]]
        elif len(I_var_list) == 17:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12],I_var_list[13],I_var_list[14],I_var_list[15],I_var_list[16]]]
        elif len(I_var_list) == 18:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12],I_var_list[13],I_var_list[14],I_var_list[15],I_var_list[16],I_var_list[17]]]
        elif len(I_var_list) == 19:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12],I_var_list[13],I_var_list[14],I_var_list[15],I_var_list[16],I_var_list[17],I_var_list[18]]]
        elif len(I_var_list) == 20:
            X_variables_list = dataframe[[I_var_list[0] , I_var_list[1] , I_var_list[2] , I_var_list[3],I_var_list[4],I_var_list[5],I_var_list[6],I_var_list[7],I_var_list[8],I_var_list[9],I_var_list[10],I_var_list[11],I_var_list[12],I_var_list[13],I_var_list[14],I_var_list[15],I_var_list[16],I_var_list[17],I_var_list[18],I_var_list[19]]]

        return X_variables_list

    def check_independent_variables(self,independent_vars_list):
        # this function is used to check the independent variables occurs in the dataset
        # if any variable mismatch it will return False Boolean value
        flag = 0
        df = pd.read_csv(self.csvFileName)
        # print(independent_vars_list)
        for ivl in independent_vars_list:
            try:
                column = df[ivl]
            except KeyError as e:
                flag = 1
                break
        if flag > 0:
            return False
        else:
            return True

# Linear Regression Class End

# Naive Bayes Class Start

class NaiveBayesClassifier(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 450
        height = 582
        title = 'Naive Bayes Classifier'

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)
        self.MyUI()

    def MyUI(self):
        self.csvFileName = ''
        self.naive_bayes_browse_file_flag = False
        self.nb_target_var_flag = False
        self.nb_independent_var_flag = False
        self.setFixedSize(800, 582)

        self.label_2 = QtWidgets.QLabel("Naive Bayes (NB) Classification",self)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 221, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(60, 30, 401, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.label_3 = QtWidgets.QLabel("Enter .csv file",self)
        self.label_3.setGeometry(QtCore.QRect(60, 70, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.naive_bayes_browse_file_btn = QtWidgets.QPushButton("Browse",self)
        self.naive_bayes_browse_file_btn.setGeometry(QtCore.QRect(150, 70, 331, 31))


        self.naive_bayes_action_btn = QtWidgets.QPushButton("Run NB Classifier",self)
        self.naive_bayes_action_btn.setGeometry(QtCore.QRect(60, 330, 221, 41))

        self.label_4 = QtWidgets.QLabel("NOTE :- You must browse .csv file after performing Data Interpolation",self)
        self.label_4.setGeometry(QtCore.QRect(80, 30, 441, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.naive_bayes_col_input_field = QtWidgets.QTextEdit(self)
        self.naive_bayes_col_input_field.setGeometry(QtCore.QRect(260, 140, 221, 31))

        self.label_6 = QtWidgets.QLabel("Enter Target Variable in dataset",self)
        self.label_6.setGeometry(QtCore.QRect(60, 150, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.naive_bayes_output_table = QtWidgets.QTableWidget(self)
        self.naive_bayes_output_table.setGeometry(QtCore.QRect(60, 400, 331, 91))
        self.naive_bayes_output_table.setColumnCount(0)
        self.naive_bayes_output_table.setRowCount(0)

        self.naive_bayes_textField = QtWidgets.QPlainTextEdit(self)
        self.naive_bayes_textField.setGeometry(QtCore.QRect(60, 210, 271, 91))

        self.label_7 = QtWidgets.QLabel("Prediction Output",self)
        self.label_7.setGeometry(QtCore.QRect(60, 370, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_7.setFont(font)

        self.naive_bayes_back_btn = QtWidgets.QPushButton("Back",self)
        self.naive_bayes_back_btn.setGeometry(QtCore.QRect(60, 500, 111, 41))
        self.naive_bayes_back_btn.clicked.connect(self.NB_BackButton)

        self.label_8 = QtWidgets.QLabel("Enter Independent Variables in dataset. ",self)
        self.label_8.setGeometry(QtCore.QRect(60, 180, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_8.setFont(font)

        self.label_5 = QtWidgets.QLabel("NOTE :- How to enter Independent Variables in text area , you must click on HELP button",self)
        self.label_5.setGeometry(QtCore.QRect(60, 300, 441, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(False)
        self.label_5.setFont(font)

        self.naive_bayes_help = QtWidgets.QPushButton("Help",self)
        self.naive_bayes_help.setGeometry(QtCore.QRect(340, 260, 131, 41))

        self.naive_bayes_selected_variable = QtWidgets.QLabel("Selected .csv File Path",self)
        self.naive_bayes_selected_variable.setGeometry(QtCore.QRect(60, 110, 421, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.naive_bayes_selected_variable.setFont(font)


        self.naive_bayes_output_table.setColumnCount(2)
        self.naive_bayes_output_table.setRowCount(1)
        self.naive_bayes_output_table.setItem(0,0, QTableWidgetItem("Model Accuracy"))

        self.naive_bayes_browse_file_btn.clicked.connect(self.naive_bayes_window_fileOpener)
        self.naive_bayes_action_btn.clicked.connect(self.naive_bayes_action)
        self.naive_bayes_help.clicked.connect(self.open_help_dialog_box)


    def NB_BackButton(self):
        self.close()

    def open_help_dialog_box(self):
        ''' this function is used to display the Dialog box when user press the HELP button '''

        invalid_var_entry_nb = QMessageBox()
        invalid_var_entry_nb.setIcon(QMessageBox.Question)
        invalid_var_entry_nb.setWindowTitle("Help!")
        invalid_var_entry_nb.setText("Enter Independent Variables or Feature column in dataset file LINE BY LINE. \n If 'k' number of variables in dataset file then you need to follow this following format(E.g). \nVariable_1\nVariable_2\nVariable_3\nVariable_4\n.\n.\n.\nVariable_k")
        invalid_var_entry_nb.exec_()

    def naive_bayes_window_fileOpener(self):

        fname = QFileDialog.getOpenFileName(filter="Comma Seperated Files (*.csv)")
        self.csvFileName = fname[0]
        self.naive_bayes_selected_variable.setText("Selected .csv File Path : " + str(fname[0]))
        self.naive_bayes_selected_variable.setStyleSheet('color : green')
        self.naive_bayes_browse_file_flag = True

    def removeEspecial(self,l):
        lister = []
        for word in l:
            if len(word) > 0:
                data = str(word)
                data = data.lstrip()
                data = data.rstrip()
                lister.append(data)
        return lister

    def check_independent_variables(self,independent_vars_list):
        # this function is used to check the independent variables occurs in the dataset
        # if any variable mismatch it will return False Boolean value
        flag = 0
        df = pd.read_csv(self.csvFileName)
        # print(independent_vars_list)
        for ivl in independent_vars_list:
            try:
                column = df[ivl]
            except KeyError as e:
                print(ivl)
                flag = 1
                break
        if flag > 0:
            return False
        else:
            return True

    def check_target_variable(self,target_variable):
        df = pd.read_csv(self.csvFileName)
        try:
            column = df[target_variable]
            return True
        except KeyError:
            return False

    def encodeIndependentVariables(self,dataframe,variables_list):

        #creating labelEncoder
        le = preprocessing.LabelEncoder()
        data_list = []
        for vl in variables_list:
            data = str(vl)
            data_list.append(le.fit_transform(dataframe[data]))

        if len(data_list) == 2:
            return list(zip(data_list[0],data_list[1]))
        elif len(data_list) == 3:
            return list(zip(data_list[0],data_list[1],data_list[2]))
        elif len(data_list) == 4:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3]))
        elif len(data_list) == 5:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4]))
        elif len(data_list) == 6:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5]))
        elif len(data_list) == 7:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6]))
        elif len(data_list) == 8:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7]))
        elif len(data_list) == 9:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8]))
        elif len(data_list) == 10:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9]))
        elif len(data_list) == 12:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10]))
        elif len(data_list) == 13:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12]))
        elif len(data_list) == 14:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13]))
        elif len(data_list) == 15:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14]))
        elif len(data_list) == 16:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14],data_list[15]))
        elif len(data_list) == 17:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14],data_list[15],data_list[16]))
        elif len(data_list) == 18:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14],data_list[15],data_list[16],data_list[17]))
        elif len(data_list) == 19:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14],data_list[15],data_list[16],data_list[17],data_list[18]))
        elif len(data_list) == 20:
            return list(zip(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14],data_list[15],data_list[16],data_list[17],data_list[18],data_list[19]))

    def encodeTargetVariables(self,variable_data):
        from sklearn import preprocessing

        le = preprocessing.LabelEncoder()

        variable_data = le.fit_transform(variable_data)
        return variable_data

    def write_details_to_file(self,independent_variables,target_vars,algorithm_details):

        ''' this function is used to write the details in a .txt file. '''
        # text_file_path = self.create_text_file_name()

        text_file = open('Naive Bayes Algorithm Details','w')

        text_file.write('Dataset File Path : ' + str(self.csvFileName))
        text_file.write('\n')
        text_file.write('Algorithm Type : Naive Bayes Classifier')
        text_file.write('\n')

        text_file.write('Target variable : ' +target_vars)
        text_file.write('\n')

        text_file.write('Independent variable : '+str(independent_variables))
        text_file.write('\n')

        text_file.write('---------')
        text_file.write('\n')

        text_file.write('OUTPUT')
        text_file.write('\n')

        text_file.write('---------')
        text_file.write('\n')

        text_file.write('Prediction Matrix : '+str(algorithm_details[0]))
        text_file.write('\n')

        text_file.write('Model Accuracy : '+str(algorithm_details[1]))
        text_file.write('\n')


    def TestAndPredict(self,target_vars,independent_vars):
        t_n_p_data = []

        X_train, X_test, y_train, y_test = train_test_split(independent_vars, target_vars, test_size=0.25,random_state=1)

        #Create a Gaussian Classifier
        gnb = GaussianNB()

        #Train the model using the training sets
        gnb.fit(X_train, y_train)

        #Predict the response for test dataset
        y_pred = gnb.predict(X_test)
        cnf_matrix = metrics.confusion_matrix(y_test, y_pred)


        confusion_matrix = metrics.accuracy_score(y_test, y_pred)
        lr = LogisticRegression()
        lr.fit(X_train, y_train)
        Y_lr_score = lr.decision_function(X_test)
        #confusion_matrix_lr = metrics.accuracy_score(y_test, Y_lr_score)
        fpr_gnb, tpr_gnb, thresholds_gnb = roc_curve(y_test, y_pred)
        fpr_lr, tpr_lr, thresholds_lr = roc_curve(y_test, Y_lr_score)
        roc_auc = auc(fpr_gnb, tpr_gnb)
        roc_auc_lr = auc(fpr_lr, tpr_lr)
        roc_auc
        roc_auc_lr
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,10))
        plt.title('ROC curve')
        plt.plot(fpr_gnb, tpr_gnb, color='red',label = 'AUC_NB = %0.2f' % roc_auc)
        plt.plot(fpr_lr, tpr_lr, color='green',label = 'AUC_LR = %0.2f' % roc_auc_lr)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],linestyle='--')
        plt.axis('tight')
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        self.plotting_file_name = 'roc curve' +str(gnb)+'.png'
        plt.savefig(self.plotting_file_name)

        plt.figure(figsize=(10,10))
        plt.title('')
        plt.plot(fpr_gnb, tpr_gnb, color='red',label = 'AUC_NB = %0.2f' % roc_auc)
        plt.plot(fpr_lr, tpr_lr, color='green',label = 'AUC_LR = %0.2f' % roc_auc_lr)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],linestyle='--')
        plt.axis('tight')
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        self.plotting_file_name = 'roc curve_compare.png'
        plt.savefig(self.plotting_file_name)

        class_names=[0,1] # name  of classes
        plt.figure(figsize=(10,10))
        fig, ax = plt.subplots()
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names)
        plt.yticks(tick_marks, class_names)
        #Confusion matrix
        sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
        ax.xaxis.set_label_position("top")
        plt.axis('tight')
        plt.title('Confusion matrix')
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')

        self.plotting_file_name = 'matrix.png'
        plt.savefig(self.plotting_file_name)

        t_n_p_data.append(y_pred)
        t_n_p_data.append(confusion_matrix)


        return t_n_p_data

    def naive_bayes_action(self):
        ''' this function is used to perform naive bayes classification algorithm '''
        df = pd.read_csv(self.csvFileName)

        target_var_col = str(self.naive_bayes_col_input_field.toPlainText())
        target_var_col = target_var_col.rstrip()
        target_var_col = target_var_col.lstrip()

        independent_var_cols = self.naive_bayes_textField.toPlainText()
        lister_ivc = self.removeEspecial(independent_var_cols.split('\n'))

        if len(target_var_col) > 0:
            self.nb_target_var_flag = True
        if len(independent_var_cols) > 0:
            self.nb_independent_var_flag = True

        if self.nb_target_var_flag == True and self.nb_independent_var_flag == True and self.naive_bayes_browse_file_flag == True:

            if self.check_target_variable(target_var_col) == True and self.check_independent_variables(lister_ivc) == True:
                #target variables and independent variables must not be same.
                if target_var_col not in lister_ivc:

                    tdf = list(df[target_var_col])
                    target_label_encoded_list = self.encodeTargetVariables(tdf)
                    print(lister_ivc)
                    independent_label_encoded_list = self.encodeIndependentVariables(df,lister_ivc)
                    details = self.TestAndPredict(target_label_encoded_list,independent_label_encoded_list)
                    self.write_details_to_file(lister_ivc,target_var_col,details)
                    self.naive_bayes_output_table.setItem(0,1, QTableWidgetItem(str(details[1])))

                    invalid_var_entry_nb = QMessageBox()
                    invalid_var_entry_nb.setIcon(QMessageBox.Information)
                    invalid_var_entry_nb.setWindowTitle("Congratulations!")
                    invalid_var_entry_nb.setText("You succesfully performed Naive Bayes Classification on dataset "+self.csvFileName+" , all details are saved as Naive Bayes Algorithm Details.txt")
                    invalid_var_entry_nb.exec_()
                else:
                    # if the target variables and independent variables are matched ...
                    matching_variables_nb = QMessageBox()
                    matching_variables_nb.setIcon(QMessageBox.Critical)
                    matching_variables_nb.setWindowTitle("ALERT!")
                    matching_variables_nb.setText("Independent Variables and Target Variables can't be same. Please enter Target Variable and Independent which they must not match to each other. You can also performed classification methods and label your data perfectly in order to avoid such type of errors.")
                    matching_variables_nb.exec_()

            else:
                invalid_var_entry_nb = QMessageBox()
                invalid_var_entry_nb.setIcon(QMessageBox.Critical)
                invalid_var_entry_nb.setWindowTitle("INVALID VARIABLE")
                invalid_var_entry_nb.setText("Please enter a valid Target and Independent Variables. The variable(s) you entered isn't mentioned within in dataset file")
                invalid_var_entry_nb.exec_()

        else:

            naive_bayes_msgBox = QMessageBox()
            naive_bayes_msgBox.setIcon(QMessageBox.Critical)
            naive_bayes_msgBox.setWindowTitle("Action Not Possible")
            naive_bayes_msgBox.setText("Please input .csv file for dataset and enter all values of Independent and Target variables. These values must needed to run Naive Bayes Classifier.")
            naive_bayes_msgBox.exec_()

# Naive Bayes Class End

# Data Summary Class Start
class DataSummary(QMainWindow):

    def __init__(self):
        super().__init__()
        top = 100
        left = 70
        width = 540
        height = 477
        title = 'Data Summarization'

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)

        self.MyUI()

    def MyUI(self):

        # self.data_summary_back_btn.setText(_translate("MainWindow", "Back"))

        self.label_2 = QtWidgets.QLabel("Data Summarization",self)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 181, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("background-color: teal")
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_2.setFont(font)

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(60, 30, 401, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.label_3 = QtWidgets.QLabel("Enter .csv file",self)
        self.label_3.setGeometry(QtCore.QRect(60, 70, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_3.setFont(font)

        self.data_sumr_browse = QtWidgets.QPushButton("Browse",self)
        self.data_sumr_browse.setGeometry(QtCore.QRect(150, 70, 311, 31))

        self.data_sumrzt = QtWidgets.QPushButton("Summarization",self)
        self.data_sumrzt.setGeometry(QtCore.QRect(290, 190, 171, 31))

        self.data_summary_back_btn = QtWidgets.QPushButton("Back",self)
        self.data_summary_back_btn.setGeometry(QtCore.QRect(60, 380, 121, 41))
        self.data_summary_back_btn.clicked.connect(self.DataSummaryBackButton)

        self.heading_label = QtWidgets.QLabel("NOTE :- You must browse .csv file after performing Data Interpolation",self)
        self.heading_label.setGeometry(QtCore.QRect(80, 30, 441, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.heading_label.setFont(font)

        self.col_input_field = QtWidgets.QTextEdit(self)
        self.col_input_field.setGeometry(QtCore.QRect(60, 190, 221, 31))

        self.data_sum_slec_label = QtWidgets.QLabel("Selected .csv File Path ",self)
        self.data_sum_slec_label.setGeometry(QtCore.QRect(60, 110, 401, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.data_sum_slec_label.setFont(font)

        self.label_6 = QtWidgets.QLabel("Enter Column name in dataset file ",self)
        self.label_6.setGeometry(QtCore.QRect(60, 140, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel("Output details of Data Summarization",self)
        self.label_7.setGeometry(QtCore.QRect(60, 240, 401, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_7.setFont(font)

        self.output_table = QtWidgets.QTableWidget(self)
        self.output_table.setGeometry(QtCore.QRect(60, 270, 401, 91))
        self.output_table.setObjectName("output_table")
        self.output_table.setColumnCount(0)
        self.output_table.setRowCount(0)

        self.data_sumr_browse.clicked.connect(self.data_summary_window_fileOpener)
        # self.data_sumrzt.setText(_translate("MainWindow", "Data Summarization"))
        self.data_sumrzt.clicked.connect(self.data_summarization_action)

        self.output_table.setColumnCount(2)
        self.output_table.setRowCount(4)

    def DataSummaryBackButton(self):
        self.close()

    def data_summary_window_fileOpener(self):

        fname = QFileDialog.getOpenFileName(filter="Comma Seperated Files (*.csv)")
        self.csvFileName = fname[0]
        self.data_sum_slec_label.setText("Selected .csv File Path : " + str(fname[0]))
        self.data_sum_slec_label.setStyleSheet('color : green')

        if len(self.csvFileName) > 0:
            self.data_summary_browse_file_flag = True

    def data_summarization_action(self):
        ''' this is used to perform the data summary action , when the button pressed '''

        ds_col_name = self.col_input_field.toPlainText()

        if len(ds_col_name) == 0 and self.data_summary_browse_file_flag == False:

            data_summary_zero_input = QMessageBox()
            data_summary_zero_input.setIcon(QMessageBox.Critical)
            data_summary_zero_input.setWindowTitle("Action Not Possible")
            data_summary_zero_input.setText("Please input .csv file and Enter columns details to proceed.")
            data_summary_zero_input.exec_()

        elif len(ds_col_name) > 0 and self.data_summary_browse_file_flag == False:

            data_summary_zero_inputType1 = QMessageBox()
            data_summary_zero_inputType1.setIcon(QMessageBox.Critical)
            data_summary_zero_inputType1.setWindowTitle("Action Not Possible")
            data_summary_zero_inputType1.setText("Please input .csv file.")
            data_summary_zero_inputType1.exec_()

        elif len(ds_col_name) == 0 and self.data_summary_browse_file_flag == True:
            data_summary_zero_inputType2 = QMessageBox()
            data_summary_zero_inputType2.setIcon(QMessageBox.Critical)
            data_summary_zero_inputType2.setWindowTitle("Action Not Possible")
            data_summary_zero_inputType2.setText("Please enter column detail for performing Data Summarization")
            data_summary_zero_inputType2.exec_()

        elif len(ds_col_name) > 0 and self.data_summary_browse_file_flag == True:

            data_frame = pd.read_csv(self.csvFileName)
            try:
                mode = ''
                m_c = list(data_frame.loc[:,ds_col_name].mode())
                for mc in m_c:
                    mode += str(mc) + ','

                mode = mode[0:len(mode)-1]
                standard_deviation = data_frame[ds_col_name].std(skipna=True)
                mean = data_frame[ds_col_name].mean()
                median = data_frame[ds_col_name].median()

                self.output_table.setItem(0,0, QTableWidgetItem("Mean"))
                self.output_table.setItem(1,0, QTableWidgetItem("Median"))
                self.output_table.setItem(2,0, QTableWidgetItem("Mode"))
                self.output_table.setItem(3,0, QTableWidgetItem("Standard Deviation"))

                self.output_table.setItem(0,1, QTableWidgetItem(str(data_frame[ds_col_name].mean())))
                self.output_table.setItem(1,1, QTableWidgetItem(str(data_frame[ds_col_name].median())))
                self.output_table.setItem(2,1, QTableWidgetItem(mode))
                self.output_table.setItem(3,1, QTableWidgetItem(str(data_frame[ds_col_name].std(skipna=True))))

                with open('data_summary.csv', 'w', newline='') as file:

                    writer = csv.writer(file)
                    writer.writerow([1, "Mean", mean])
                    writer.writerow([2, "Standard Deviation", standard_deviation])
                    writer.writerow([3, "Median", median])
                    writer.writerow([3, "Mode", mode])

                    data_summary_save_file = QMessageBox()
                    data_summary_save_file.setIcon(QMessageBox.Information)
                    data_summary_save_file.setWindowTitle("Message")
                    data_summary_save_file.setText("Data summary is saved in data_summary.csv")
                    data_summary_save_file.exec_()

            except KeyError:

                data_summary_invalid_col = QMessageBox()
                data_summary_invalid_col.setIcon(QMessageBox.Critical)
                data_summary_invalid_col.setWindowTitle("Action Not Possible")
                data_summary_invalid_col.setText("This column is not found inside dataset file. Please enter correct column name.")
                data_summary_invalid_col.exec_()

# Data Summart Class End

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(732, 571)
        MainWindow.setFixedSize(732, 571)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 10, 341, 41))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setAutoFillBackground(True)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(160, 50, 421, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(230, 190, 20, 271))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(480, 190, 21, 271))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        self.data_aggregation_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_aggregation_button.setGeometry(QtCore.QRect(20, 250, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.data_aggregation_button.setFont(font)
        self.data_aggregation_button.setObjectName("pushButton")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 190, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
                # self.pushButton_2.setText(_translate("MainWindow", "Data Summarization"))

        self.data_summary_btn = QtWidgets.QPushButton(self.centralwidget)
        self.data_summary_btn.setGeometry(QtCore.QRect(20, 320, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.data_summary_btn.setFont(font)

        self.dataCorrelationButton = QtWidgets.QPushButton(self.centralwidget)
        self.dataCorrelationButton.setGeometry(QtCore.QRect(20, 390, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.dataCorrelationButton.setFont(font)
        self.dataCorrelationButton.setObjectName("pushButton_3")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 190, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.linear_regression_btn = QtWidgets.QPushButton(self.centralwidget)
        self.linear_regression_btn.setGeometry(QtCore.QRect(270, 250, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.linear_regression_btn.setFont(font)
        self.linear_regression_btn.setObjectName("pushButton_4")

        self.naive_bayes_button = QtWidgets.QPushButton("Naive Bayes Classifier",self.centralwidget)
        self.naive_bayes_button.setGeometry(QtCore.QRect(270, 390, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.naive_bayes_button.setFont(font)
        # self.naive_bayes_button.setObjectName("pushButton_5")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(560, 190, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.dataFilePlotting = QtWidgets.QPushButton(self.centralwidget)
        self.dataFilePlotting.setGeometry(QtCore.QRect(520, 250, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.dataFilePlotting.setFont(font)
        self.dataFilePlotting.setObjectName("dataFilePlotting")

        self.data_interpolation_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_interpolation_button.setGeometry(QtCore.QRect(160, 130, 421, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.data_interpolation_button.setFont(font)
        self.data_interpolation_button.setObjectName("data_interpolation_button")

        self.fileConversion_button = QtWidgets.QPushButton(self.centralwidget)
        self.fileConversion_button.setGeometry(QtCore.QRect(160, 70, 421, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.fileConversion_button.setFont(font)
        self.fileConversion_button.setObjectName("fileConversion_button")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 732, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "VAYU"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("background-color: teal")

        self.data_aggregation_button.setText(_translate("MainWindow", "Data Aggregation"))
        self.label_2.setText(_translate("MainWindow", "Data Analysis"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("background-color: teal")

        self.data_summary_btn.setText(_translate("MainWindow", "Data Summarization"))
        self.dataCorrelationButton.setText(_translate("MainWindow", "Data Correlation"))

        self.label_3.setText(_translate("MainWindow", "Data Prediction"))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setStyleSheet("background-color: teal")
        self.linear_regression_btn.setText(_translate("MainWindow", "Linear Regression"))
        self.label_4.setText(_translate("MainWindow", "Data Visulaization"))
        self.label_4.setStyleSheet("background-color: teal")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.dataFilePlotting.setText(_translate("MainWindow", "Data Plots"))

        self.data_interpolation_button.setText(_translate("MainWindow", "Data Interpolation"))
        self.fileConversion_button.setText(_translate("MainWindow", "Convert Excel to CSV"))

        self.fileConversion_button.clicked.connect(self.file_conversion_window)
        self.data_interpolation_button.clicked.connect(self.data_interpolation_window)
        self.data_aggregation_button.clicked.connect(self.data_aggregation_window)
        self.dataCorrelationButton.clicked.connect(self.data_corr_window)
        self.dataFilePlotting.clicked.connect(self.sfp_window)
        #self.DoubleFilePlotting.clicked.connect(self.dfp_window)
        self.linear_regression_btn.clicked.connect(self.lr_window)
        self.naive_bayes_button.clicked.connect(self.nb_window_action)
        self.data_summary_btn.clicked.connect(self.data_summary_window)


    def data_summary_window(self):

        self.Data_Summary = DataSummary()
        self.Data_Summary.show()

    def lr_window(self):

        self.LR = LinearRegression()
        self.LR.show()

    def nb_window_action(self):

        self.NBC = NaiveBayesClassifier()
        self.NBC.show()

    def sfp_window(self):

        self.SFP = dataFilePlotting()
        self.SFP.show()

    def data_corr_window(self):
        self.DC = DataCorrelation()
        self.DC.show()

    def data_interpolation_window(self):

            self.diw = DataInterpolationWindow()
            self.diw.show()

    def data_aggregation_window(self):
        self.DA = DataAggregation()
        self.DA.show()


    def file_conversion_window(self):

        self.fc = FileConversion()
        self.fc.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    apply_stylesheet(app, theme='dark_teal.xml')
    MainWindow.show()
    sys.exit(app.exec_())
