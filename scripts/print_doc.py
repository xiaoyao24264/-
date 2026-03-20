import win32com.client
import pythoncom
import time

pythoncom.CoInitialize()
try:
    w = win32com.client.Dispatch('Word.Application')
    w.Visible = 0
    d = w.Documents.Open(r'C:\Users\changhaoyan\Desktop\template.docx')
    print('doc:', d)
    if d:
        d.PrintOut()
        time.sleep(6)
        d.Close(0)
        print('printed ok')
    else:
        print('ERROR: doc is None')
    w.Quit()
except Exception as e:
    print('ERROR:', e)
finally:
    pythoncom.CoUninitialize()
