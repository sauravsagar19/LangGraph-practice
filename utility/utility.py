from IPython.display import display, Image
import os
import shutil

def deleteGraphPNG(folder_path: str):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Successfully deleted {folder_path}")
    else:
        print("Folder does not exist")


def savePNG(folderpath:str,file_name,graph):
    full_path=os.path.join(folderpath,file_name)
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    display(Image(graph.get_graph().draw_mermaid_png()))
    # print(display)

    with open(f"{full_path}.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
    print("Graph compiled! Saved schema visualizer workflow to 'graph_workflow.png'")
    