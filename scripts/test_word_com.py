import win32com.client
import pythoncom
import time

pythoncom.CoInitialize()

try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = 0
    
    docs = word.Documents
    print(f"Documents type: {type(docs)}")
    print(f"Documents: {docs}")
    
    if docs is None:
        print("Documents is None!")
    else:
        file_path = r"C:\Users\changhaoyan\Desktop\template.docx"
        print(f"Opening: {file_path}")
        doc = docs.Open(file_path)
        print(f"Doc type: {type(doc)}")
        
        if doc is not None:
            doc.PrintOut(False, False, 1)
            time.sleep(5)
            doc.Close(False)
            print("SUCCESS")
        else:
            print("Doc is None!")
    
    word.Quit()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    pythoncom.CoUninitialize()
