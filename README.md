# Call Windows C-dll (foreign) functions directly via ctypes inside Python: A Complete Template

With Python ctypes (see [1](#notes), Python can directly call (foreign) C functions defined in Windows dll. This makes the speed-up of Python via C truly easy. The details, especially with Windows dll, can be confusing, unfortunately. This package provides the necessary step-by-step guide on how to achieve calling C functions in Python (version 3.13).

### Build Windows Dll
To create a dll project in Visual Studio 2022:
1.	On VS2022 start-up, choose _Create a new project_.
2.	Choose C++, and choose _Dynamic-link Library (DLL)_.
3.	Enter a name, in my case winCDynamic, for your project.
4.	Delete dllmain.cpp, framework.h, pch.h, pch.cpp from Project.
5.	Move **qlcfuncs.cpp** to the project folder (i.e., winCDynamic) and add to the project. Note: If you provide a header file **qlcfuncs.h**, it will NOT work!
6.	Set the VS2022 Compiler by opening the _Property Pages dialog_ and _Configuration Properties_ in the left pane:
- C/C++ -> Precompiled Headers: set [Precompiled Headers] to [Not Using Precompiled Headers]

Note: the default calling convention should be [__cdecl] in the VS2022 Compiler. If not, set as follows:
- C/C++ -> Advanced: set [Calling Convention] to [__cdecl (/Gd)]
  
Now, you can build your Windows dll for Python and copy **winCDynamic.dll** to your desired folder (in my case libc, see [2](#notes)).

### Python calls C-dll functions
To call dll functions in Python, you must pass the correct argument types (i.e., buffered byte string, c_double, ctypes Structure, or ctypes array) and specify the return type. Read the documentation directly in **c4Python.py** for what most of you need to know.

If you run c4Python.py (under Command, type: py c4Python.py), you will find three successful calls, such as qlDblRetArgs(). But you will see the following error as well:
- AttributeError: function 'qlArrayArg' not found

The error is caused by missing the qlArrayArg() function that depends on a C++ function defined in a static library. Let’s build the static library then.

### Build Windows (Static) Lib
To create a static library project in Visual Studio 2022:
1.	On VS2022 start-up, choose _Create a new project_.
2.	Choose C++, and choose _Static Library_.
3.	Enter a name, in my case winCppStatic, for your project.
4.	Delete framework.h, pch.h, pch.cpp, winCppStatic.cpp from Project.
5.	Move qlcpptools.h and qlcpptools.cpp to the project folder (i.e., winCppStatic).
6.	Set up the VS2022 Compiler:	set [Precompiled Headers] to [Not Using Precompiled Headers].

Note: The default calling convention should be [__cdecl] in the VS2022 Compiler. If not, set it as in the Build Windows Dll section.

Build your Windows static library and move **qlcpptools.h** and **winCppStatic.lib** to libc (see [2](#notes)).

### Re-build Windows Dll
To rebuild the dll, first set up the VS2022 Compiler options:
- Linker -> Input: add [../libc/winCppStatic.lib] to [Additional Dependencies]
- C/C++ -> Preprocessor: Add [\_QL__INCLUDE_STATIC_LIB_] to [Preprocessor Definitions]

Rebuild and run c4Python.py. qlArrayArg() will be successful this time.

### ctypes in Python or PyObject in C++
Suppose you have a big and complex C++ application (such as my own convertible bonds pricing tool). In that case, it makes more sense to wrap functionalities from static libraries inside a function and export the function in a Windows DLL to the Python client. On the other hand, with a few functions to extend Python by C++, you can use PyObject defined in Python.h to define modules and functions in C++ within a Python package directly (see [3](#notes) and my [Cpp-Inside-Python](../../../Cpp-Inside-Python) Github package).

### Notes:
[1] [ctypes — A foreign function library for Python](https://docs.python.org/3/library/ctypes.html)

[2] To automatically copy files after the build, select _Configuration Properties > Build Events > Post-Build Event_, and in the *Command Line* field, enter this command (for the dll project):
> xcopy /y /d $(TargetPath)  ..\\libc

or for the static lib project:
> xcopy /y /d $(ProjectDir) qlcpptools.h ..\\libc

> xcopy /y /d $(TargetPath) ..\\libc

[3] [Extending Python with C or C++ — Python 3.13.2](https://docs.python.org/3/extending/extending.html)
