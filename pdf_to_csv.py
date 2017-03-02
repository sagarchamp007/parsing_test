import pandas
import os


def to_csv_(inp_path, output_csv_path, tabula_path, coord=(131, 48, 506, 685)):
    ''' convert a pdf file to csv. '''
    temp_csv_path = os.path.abspath("temp")
    if not os.path.exists(temp_csv_path):
        os.makedirs(temp_csv_path)
    temp_file_path = os.path.join(temp_csv_path, "temp.csv")
    cmd = "java -jar " + tabula_path + " -a " + str(coord[0]) + \
          "," + str(coord[1]) + "," + str(coord[2]) + "," + str(coord[3]) + \
          " -n -o " + temp_file_path + " " + inp_path

    if not os.path.exists(output_csv_path):
        os.makedirs(output_csv_path)
    output_file_path = os.path.join(output_csv_path, "output.csv")

    os.system("{}".format(cmd))
    df = pandas.read_csv(temp_file_path, header=None)
    df = df.dropna(axis=1, how='all')
    df1 = (df[2].str.extract(r'(?P<pat0>[\d.]+)(?P<pat1>.+)?', expand=True))
    df1['pat1'] = df1['pat1'].str.strip()
    df1['pat0'] = df1['pat0'].astype('float64')
    df.drop(2, axis=1, inplace=True)
    df.insert(loc=2, value=df1['pat0'], column=2)
    df.insert(loc=3, value=df1['pat1'], column=3)
    df.to_csv(
        output_file_path, index=False, header=False, float_format='%.15g')
    return output_file_path


if __name__ == "__main__":
    out_path = os.path.abspath("output")
    output_file_path = to_csv_(
        os.path.abspath('BalSheet.pdf'), out_path,
        os.path.abspath('tabula/tabula-0.9.2-jar-with-dependencies.jar'))
    print("Output csv is in path '{}'".format(output_file_path))
