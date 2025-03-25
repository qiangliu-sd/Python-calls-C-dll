
from ctypes import *

class PyC_struct(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]

    def ql2String(self): return f"[{self.x}, {self.y}, {self.z}]"
        
        
class QlDllC:
    """---used directly as arguments in Python C-function calls--- 
		None: passed as a C NULL pointer 
		integers: passed as the default C int type
		bytes objects & strings: passed as pointer to the memory block that contains their data (char* or wchar_t*)
    """
    def __init__(self, dll_path):
        """---Two ways to load C-DLL---"""
        self.libc1 = CDLL(dll_path)  #CDLL('../libc/winCDynamic.dll')
        self.libc2 = cdll.winCDynamic
        
        self.testRun(dll_path)

    def qlStrArg(self, str_i: str):
        """Pass string-buffer to C: [qlStrArg(char *s)]"""
        _str = create_string_buffer(str_i)
        self.libc1.qlStrArg(_str)

    def qlIntRetArgs(self,a: int, b: int)->int:
        """Integers work directly as arguments & return types"""
        return self.libc2.qlIntRetArgs(a,b)

    def qlDblRetArgs(self,x: float, y: float)->float:
        """MUST set arguments & return types for Doubles"""
        self.libc1.qlDblRetArgs.argtypes = [c_double, c_double]
        self.libc1.qlDblRetArgs.restype = c_double 
        return self.libc1.qlDblRetArgs(x,y)
                
    def qlArrayArg(self, list_i: list)->float:
        """Pass ctypes-array[c_double *8] to C: [qlArrayArg(double arr[], int size)]"""
        _num = len(list_i)
        _dbl_arr = (c_double * _num)(*list_i) # *: unpack list
        self.libc2.qlArrayArg.restype = c_double
        return self.libc2.qlArrayArg(_dbl_arr, _num)
        
    def qlArrayFetch(self, num_i: int) -> list:
        """Pass ctypes-array to C: [qlArrayFetch(double arr[])]"""
        _da3 = (c_double * num_i)() 
        self.libc2.qlArrayFetch(_da3, num_i)
        return _da3[:num_i]     # ctypes-array to list
        
    def qlArrayRet(self, num_i: int)-> list:
        """Return [POINTER(c_double)] via C: [void* qlArrayRet()]""" 
        self.libc2.qlArrayRet.restype = POINTER(c_double)
        _da3 = self.libc2.qlArrayRet(num_i)
        return _da3[:num_i]
       
    def qlStructFetch(self, xyz: Structure):
        """Pass [POINTER(PyC_struct)] to C: [qlStructFetch( C_struct* ptr)]"""
        self.libc2.qlStructFetch.argtypes = [POINTER(PyC_struct)]
        self.libc2.qlStructFetch(xyz)
 
    def qlStructRet(self)->Structure:
        """Return [PyC_struct] via C: [C_struct qlMultiVals()]"""
        self.libc2.qlStructRet.restype = PyC_struct
        return self.libc2.qlStructRet()
        
    
    def testRun(self,dll_path):
        print(f"obj<CDLL({dll_path})>: {self.libc1}")
        print(f"obj<cdll.winCDynamic>: {self.libc2}\n")
        
        print("C qlStrArg:")
        self.qlStrArg(b"byte string literal from <Python>\n")
        
        a,b = 3, 5
        _sum = self.qlIntRetArgs(a,b)        # 3.0 does NOT work
        print(f"C qlIntRetArgs: {a} + {b} = {_sum}")

        x,y = 2.3,5
        _sum = self.qlDblRetArgs(x,y)   # int(5) OK
        print(f"C qlDblRetArgs: {x} + {y} = {_sum}")
        
        _list8 = [i*i for i in range(8)]
        _std = self.qlArrayArg(_list8)
        print(f"C qlArrayArg(std): {_std}\n")
        
        _list3 = self.qlArrayFetch(3)        
        print(f"C qlArrayFetch: {_list3}")
        
        _list3 = self.qlArrayRet(3)
        print(f"C qlArrayRet: {_list3}\n")
 
        _xyz = PyC_struct()
        self.qlStructFetch(_xyz)
        print(f"C qlStructFetch: {_xyz.ql2String()}")
        
        _xyz = self.qlStructRet()
        print(f"C qlStructRet: {_xyz.ql2String()}")

   
if __name__ == "__main__":
    #print(f"\n{__file__} ... started\n")
    _C_DLL_PATH = '../libc/winCDynamic.dll'
    QlDllC(_C_DLL_PATH)