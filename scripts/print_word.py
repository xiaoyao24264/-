# Windows Word Print via Python
import win32com.client
import pythoncom
import os
import sys

# Initialize COM for the current thread
pythoncom.CoInitialize()

try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = 0
    
    file_path = r"C:\Users\changhaoyan\Desktop\template.docx"
    
    doc = word.Documents.Open(file_path)
    doc.PrintOut(False, False, 1)  # Print page 1 only
    
    import time
    time.sleep(5)
    
    doc.Close(False)
    word.Quit()
    
    print("SUCCESS: Printed")
except Exception as e:
    print(f"ERROR: {e}")
finally:
    pythoncom.CoUninitialize()
