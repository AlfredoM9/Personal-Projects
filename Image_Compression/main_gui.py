# img_viewer.py

import PySimpleGUI as sg
import os.path
import compressor

if __name__ == '__main__':
    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    image_viewer_column = [
        [sg.Text("Choose an image from list on left:")],
        [sg.Text(size=(40,1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeparator(),
            sg.Column(image_viewer_column),
        ],
        [sg.Text("Enter K-Means")],
        [sg.Input(key="-IN-")],
        [sg.Button('Compress', key="-BUTTON-"), sg.Exit()],
        [sg.Text("Warning: Compression may freeze the application and take several minutes to respond.")],
        [sg.Text("After it responds, the compressed image should be saved. Refresh the folder by selecting the folder "
                 "again.")]
    ]

    window = sg.Window("Image Compressor", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        k_means = -1

        if event == "-FOLDER-":
            folder = values["-FOLDER-"]

            try:
                file_list = os.listdir(folder)

            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder,f))
                and f.lower().endswith((".png"))
            ]
            window["-FILE LIST-"].update(fnames)

        elif event == "-FILE LIST-":
            try:
                filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])

                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(filename=filename)

            except:
                pass

        elif event == "-BUTTON-":
            print("Hello")
            try:
                if filename != "":
                    print("Hello2")
                    k_means = 2
                    if values["-IN-"] != "":
                        k_means = int(values["-IN-"])
                    compressor.main(filename, k_means)

            except:
                pass

    window.close()
