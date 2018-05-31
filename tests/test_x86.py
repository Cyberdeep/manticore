from builtins import *
import unittest
import functools
from manticore.core.cpu.x86 import *
from manticore.core.smtlib import *
from manticore.core.memory import *

def skipIfNotImplemented(f):
    # XXX(yan) the inner function name must start with test_
    @functools.wraps(f)
    def test_inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except NotImplementedError as e:
            raise unittest.SkipTest(str(e))

    return test_inner

def forAllTests(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if not attr.startswith('test_'):
                continue
            method = getattr(cls, attr)
            if callable(method):
                setattr(cls, attr, decorator(method))
        return cls

    return decorate

@forAllTests(skipIfNotImplemented)
class CPUTest(unittest.TestCase):
    _multiprocess_can_split_ = True

    # Used while transitioning to py3
    def assertEqual(self, a, b):
        if isinstance(b, str):
            b = bytes([ord(c) for c in b])
        return super(CPUTest, self).assertEqual(a, b)

    class ROOperand(object):
        ''' Mocking class for operand ronly '''
        def __init__(self, size, value):
            self.size = size
            self.value = value
        def read(self):
            return self.value & ((1<<self.size)-1)

    class RWOperand(ROOperand):
        ''' Mocking class for operand rw '''
        def write(self, value):
            self.value = value & ((1<<self.size)-1)
            return self.value



    def test_AAD_1(self):
        ''' Instruction AAD_1
            Groups: not64bitmode
            0x80702ff:	aad	0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x08070300] = '\xff'
        mem[0x080702ff] = '\xd5'
        cpu.EIP = 0x80702ff
        cpu.AH = 0x0
        cpu.ZF = False
        cpu.AL = 0x30
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x8070300], '\xff')
        self.assertEqual(mem[0x80702ff], '\xd5')
        self.assertEqual(cpu.EIP, 134677249)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.AL, 48)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AAD_2(self):
        ''' Instruction AAD_2
            Groups: not64bitmode
            0x8070301:	aad	0
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x08070301] = '\xd5'
        mem[0x08070302] = '\x00'
        cpu.EIP = 0x8070301
        cpu.AH = 0x0
        cpu.ZF = False
        cpu.AL = 0x30
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x8070301], '\xd5')
        self.assertEqual(mem[0x8070302], '\x00')
        self.assertEqual(cpu.EIP, 134677251)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.AL, 48)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AAD_3(self):
        ''' Instruction AAD_3
            Groups: not64bitmode
            0x8070303:	aad	0
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x08070303] = '\xd5'
        mem[0x08070304] = '\x00'
        cpu.EIP = 0x8070303
        cpu.AH = 0x0
        cpu.ZF = False
        cpu.AL = 0x30
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x8070303], '\xd5')
        self.assertEqual(mem[0x8070304], '\x00')
        self.assertEqual(cpu.EIP, 134677253)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.AL, 48)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AAD_4(self):
        ''' Instruction AAD_4
            Groups: not64bitmode
            0x80702fb:	aad
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x080702fb] = '\xd5'
        mem[0x080702fc] = '\n'
        cpu.EIP = 0x80702fb
        cpu.AH = 0xec
        cpu.ZF = True
        cpu.AL = 0xf8
        cpu.PF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x80702fb], '\xd5')
        self.assertEqual(mem[0x80702fc], '\n')
        self.assertEqual(cpu.EIP, 134677245)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.AL, 48)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AAD_5(self):
        ''' Instruction AAD_5
            Groups: not64bitmode
            0x80702fd:	aad	0xf
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x080702fd] = '\xd5'
        mem[0x080702fe] = '\x0f'
        cpu.EIP = 0x80702fd
        cpu.AH = 0x0
        cpu.ZF = False
        cpu.AL = 0x30
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x80702fd], '\xd5')
        self.assertEqual(mem[0x80702fe], '\x0f')
        self.assertEqual(cpu.EIP, 134677247)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.AL, 48)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AAM_1(self):
        ''' Instruction AAM_1
            Groups: not64bitmode
            0x8070306:	aam
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x08070306] = '\xd4'
        mem[0x08070307] = '\n'
        cpu.EIP = 0x8070306
        cpu.AH = 0x0
        cpu.ZF = True
        cpu.AL = 0x0
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x8070306], '\xd4')
        self.assertEqual(mem[0x8070307], '\n')
        self.assertEqual(cpu.EIP, 134677256)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AAM_2(self):
        ''' Instruction AAM_2
            Groups: not64bitmode
            0x807030a:	aam	0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x0807030a] = '\xd4'
        mem[0x0807030b] = '\xff'
        cpu.EIP = 0x807030a
        cpu.AH = 0x0
        cpu.ZF = True
        cpu.AL = 0x0
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x807030a], '\xd4')
        self.assertEqual(mem[0x807030b], '\xff')
        self.assertEqual(cpu.EIP, 134677260)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AAM_3(self):
        ''' Instruction AAM_3
            Groups: not64bitmode
            0x8070308:	aam	0xf
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x08070308] = '\xd4'
        mem[0x08070309] = '\x0f'
        cpu.EIP = 0x8070308
        cpu.AH = 0x0
        cpu.ZF = True
        cpu.AL = 0x0
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x8070308], '\xd4')
        self.assertEqual(mem[0x8070309], '\x0f')
        self.assertEqual(cpu.EIP, 134677258)
        self.assertEqual(cpu.AH, 0)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_ADD_1(self):
        ''' Instruction ADD_1
            Groups:
            0xf7fec387:	add	ecx, edi
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec388] = '\xf9'
        mem[0xf7fec387] = '\x01'
        cpu.EIP = 0xf7fec387
        cpu.PF = False
        cpu.ECX = 0x5c6b
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0xf7e22474
        cpu.CF = False
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fec388], '\xf9')
        self.assertEqual(mem[0xf7fec387], '\x01')
        self.assertEqual(cpu.EIP, 4160668553)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.ECX, 4158816479)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 4158792820)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, True)

    def test_ADD_10(self):
        ''' Instruction ADD_10
            Groups:
            0xf7fe71b9:	add	dword ptr [eax], edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fbf000, 0x1000, 'rwx')
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fbf780] = '\xa0'
        mem[0xf7fbf781] = '\xe9'
        mem[0xf7fbf782] = '\x06'
        mem[0xf7fbf783] = '\x00'
        mem[0xf7fe71b9] = '\x01'
        mem[0xf7fe71ba] = '\x10'
        cpu.EIP = 0xf7fe71b9
        cpu.EAX = 0xf7fbf780
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xf7e15000
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fbf780], '\xa0')
        self.assertEqual(mem[0xf7fbf781], '9')
        self.assertEqual(mem[0xf7fbf782], '\xe8')
        self.assertEqual(mem[0xf7fbf783], '\xf7')
        self.assertEqual(mem[0xf7fe71b9], '\x01')
        self.assertEqual(mem[0xf7fe71ba], '\x10')
        self.assertEqual(cpu.EIP, 4160647611)
        self.assertEqual(cpu.EAX, 4160485248)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EDX, 4158738432)
        self.assertEqual(cpu.SF, True)

    def test_ADD_11(self):
        ''' Instruction ADD_11
            Groups:
            0xf7ff41d7:	add	ebx, 0x1315
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff41d7] = '\x81'
        mem[0xf7ff41d8] = '\xc3'
        mem[0xf7ff41d9] = '\x15'
        mem[0xf7ff41da] = '\x13'
        mem[0xf7ff41db] = '\x00'
        mem[0xf7ff41dc] = '\x00'
        cpu.EIP = 0xf7ff41d7
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EBX = 0xf7ff41d7
        cpu.CF = True
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7ff41d7], '\x81')
        self.assertEqual(mem[0xf7ff41d8], '\xc3')
        self.assertEqual(mem[0xf7ff41d9], '\x15')
        self.assertEqual(mem[0xf7ff41da], '\x13')
        self.assertEqual(mem[0xf7ff41db], '\x00')
        self.assertEqual(mem[0xf7ff41dc], '\x00')
        self.assertEqual(cpu.EIP, 4160700893)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EBX, 4160705772)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, True)

    def test_ADD_12(self):
        ''' Instruction ADD_12
            Groups:
            0xf7fe71b9:	add	dword ptr [eax], edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fbf000, 0x1000, 'rwx')
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fbfb0c] = '\xf0'
        mem[0xf7fbfb0d] = '\x1e'
        mem[0xf7fbfb0e] = '\x07'
        mem[0xf7fbfb0f] = '\x00'
        mem[0xf7fe71b9] = '\x01'
        mem[0xf7fe71ba] = '\x10'
        cpu.EIP = 0xf7fe71b9
        cpu.EAX = 0xf7fbfb0c
        cpu.PF = True
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xf7e15000
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fbfb0c], '\xf0')
        self.assertEqual(mem[0xf7fbfb0d], 'n')
        self.assertEqual(mem[0xf7fbfb0e], '\xe8')
        self.assertEqual(mem[0xf7fbfb0f], '\xf7')
        self.assertEqual(mem[0xf7fe71b9], '\x01')
        self.assertEqual(mem[0xf7fe71ba], '\x10')
        self.assertEqual(cpu.EIP, 4160647611)
        self.assertEqual(cpu.EAX, 4160486156)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EDX, 4158738432)
        self.assertEqual(cpu.SF, True)

    def test_ADD_13(self):
        ''' Instruction ADD_13
            Groups:
            0xf7fe7299:	add	eax, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe7299] = '\x01'
        mem[0xf7fe729a] = '\xc0'
        cpu.EIP = 0xf7fe7299
        cpu.EAX = 0x0
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe7299], '\x01')
        self.assertEqual(mem[0xf7fe729a], '\xc0')
        self.assertEqual(cpu.EIP, 4160647835)
        self.assertEqual(cpu.EAX, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_ADD_14(self):
        ''' Instruction ADD_14
            Groups:
            0xf7fe71aa:	add	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71aa] = '\x01'
        mem[0xf7fe71ab] = '\xd0'
        cpu.EIP = 0xf7fe71aa
        cpu.EAX = 0x1aacdc
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xf7e15000
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe71aa], '\x01')
        self.assertEqual(mem[0xf7fe71ab], '\xd0')
        self.assertEqual(cpu.EIP, 4160647596)
        self.assertEqual(cpu.EAX, 4160486620)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EDX, 4158738432)
        self.assertEqual(cpu.SF, True)

    def test_ADD_15(self):
        ''' Instruction ADD_15
            Groups:
            0xf7fe9c44:	add	dword ptr [ebp - 0x20], 1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7fe9c44] = '\x83'
        mem[0xf7fe9c45] = 'E'
        mem[0xf7fe9c46] = '\xe0'
        mem[0xf7fe9c47] = '\x01'
        mem[0xffffd478] = '\x0e'
        mem[0xffffd479] = '\x00'
        mem[0xffffd47a] = '\x00'
        mem[0xffffd47b] = '\x00'
        cpu.EIP = 0xf7fe9c44
        cpu.EBP = 0xffffd498
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe9c44], '\x83')
        self.assertEqual(mem[0xf7fe9c45], 'E')
        self.assertEqual(mem[0xf7fe9c46], '\xe0')
        self.assertEqual(mem[0xf7fe9c47], '\x01')
        self.assertEqual(mem[0xffffd478], '\x0f')
        self.assertEqual(mem[0xffffd479], '\x00')
        self.assertEqual(mem[0xffffd47a], '\x00')
        self.assertEqual(mem[0xffffd47b], '\x00')
        self.assertEqual(cpu.EIP, 4160658504)
        self.assertEqual(cpu.EBP, 4294956184)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_ADD_16(self):
        ''' Instruction ADD_16
            Groups:
            0xf7fe56a2:	add	edx, 1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem[0xf7fe56a2] = '\x83'
        mem[0xf7fe56a3] = '\xc2'
        mem[0xf7fe56a4] = '\x01'
        cpu.EIP = 0xf7fe56a2
        cpu.EDX = 0xf7e25acc
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe56a2], '\x83')
        self.assertEqual(mem[0xf7fe56a3], '\xc2')
        self.assertEqual(mem[0xf7fe56a4], '\x01')
        self.assertEqual(cpu.EIP, 4160640677)
        self.assertEqual(cpu.EDX, 4158806733)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, True)

    def test_ADD_17(self):
        ''' Instruction ADD_17
            Groups:
            0xf7fe71b9:	add	dword ptr [eax], edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fbf000, 0x1000, 'rwx')
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71b9] = '\x01'
        mem[0xf7fe71ba] = '\x10'
        mem[0xf7fbf09c] = '\x88'
        mem[0xf7fbf09d] = '\x1e'
        mem[0xf7fbf09e] = '\x16'
        mem[0xf7fbf09f] = '\x00'
        cpu.EIP = 0xf7fe71b9
        cpu.EAX = 0xf7fbf09c
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xf7e15000
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe71b9], '\x01')
        self.assertEqual(mem[0xf7fe71ba], '\x10')
        self.assertEqual(mem[0xf7fbf09c], '\x88')
        self.assertEqual(mem[0xf7fbf09d], 'n')
        self.assertEqual(mem[0xf7fbf09e], '\xf7')
        self.assertEqual(mem[0xf7fbf09f], '\xf7')
        self.assertEqual(cpu.EIP, 4160647611)
        self.assertEqual(cpu.EAX, 4160483484)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EDX, 4158738432)
        self.assertEqual(cpu.SF, True)

    def test_ADD_18(self):
        ''' Instruction ADD_18
            Groups:
            0xf7fe71aa:	add	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71aa] = '\x01'
        mem[0xf7fe71ab] = '\xd0'
        cpu.EIP = 0xf7fe71aa
        cpu.EAX = 0x1aa628
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xf7e15000
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe71aa], '\x01')
        self.assertEqual(mem[0xf7fe71ab], '\xd0')
        self.assertEqual(cpu.EIP, 4160647596)
        self.assertEqual(cpu.EAX, 4160484904)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EDX, 4158738432)
        self.assertEqual(cpu.SF, True)

    def test_ADD_19(self):
        ''' Instruction ADD_19
            Groups:
            0xf7fe4d33:	add	esp, 0x2c
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4d33] = '\x83'
        mem[0xf7fe4d34] = '\xc4'
        mem[0xf7fe4d35] = ','
        cpu.EIP = 0xf7fe4d33
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.ESP = 0xffffd2b0
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe4d33], '\x83')
        self.assertEqual(mem[0xf7fe4d34], '\xc4')
        self.assertEqual(mem[0xf7fe4d35], ',')
        self.assertEqual(cpu.EIP, 4160638262)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ESP, 4294955740)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, True)

    def test_ADD_2(self):
        ''' Instruction ADD_2
            Groups:
            0xf7fe7213:	add	ecx, dword ptr [ebp - 0x78]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd480] = '\xd4'
        mem[0xffffd481] = '\x8e'
        mem[0xffffd482] = '\xe1'
        mem[0xffffd483] = '\xf7'
        mem[0xf7fe7213] = '\x03'
        mem[0xf7fe7214] = 'M'
        mem[0xf7fe7215] = '\x88'
        cpu.EIP = 0xf7fe7213
        cpu.EBP = 0xffffd4f8
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.ECX = 0x0
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffd480], '\xd4')
        self.assertEqual(mem[0xffffd481], '\x8e')
        self.assertEqual(mem[0xffffd482], '\xe1')
        self.assertEqual(mem[0xffffd483], '\xf7')
        self.assertEqual(mem[0xf7fe7213], '\x03')
        self.assertEqual(mem[0xf7fe7214], 'M')
        self.assertEqual(mem[0xf7fe7215], '\x88')
        self.assertEqual(cpu.EIP, 4160647702)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 4158754516)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, True)

    def test_ADD_20(self):
        ''' Instruction ADD_20
            Groups:
            0xf7fe71fc:	add	esi, dword ptr [edi]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7e2c000, 0x1000, 'rwx')
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7e2c18c] = '\x18'
        mem[0xf7e2c18d] = '\xaf'
        mem[0xf7e2c18e] = '\x1a'
        mem[0xf7e2c18f] = '\x00'
        mem[0xf7fe71fc] = '\x03'
        mem[0xf7fe71fd] = '7'
        cpu.EIP = 0xf7fe71fc
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0xf7e2c18c
        cpu.CF = False
        cpu.ESI = 0xf7e15000
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7e2c18c], '\x18')
        self.assertEqual(mem[0xf7e2c18d], '\xaf')
        self.assertEqual(mem[0xf7e2c18e], '\x1a')
        self.assertEqual(mem[0xf7e2c18f], '\x00')
        self.assertEqual(mem[0xf7fe71fc], '\x03')
        self.assertEqual(mem[0xf7fe71fd], '7')
        self.assertEqual(cpu.EIP, 4160647678)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 4158833036)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4160487192)
        self.assertEqual(cpu.SF, True)

    def test_ADD_21(self):
        ''' Instruction ADD_21
            Groups:
            0xf7fe56aa:	add	edi, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem[0xf7fe56aa] = '\x01'
        mem[0xf7fe56ab] = '\xc7'
        cpu.EIP = 0xf7fe56aa
        cpu.EAX = 0x72
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0x2f2c5d89
        cpu.CF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe56aa], '\x01')
        self.assertEqual(mem[0xf7fe56ab], '\xc7')
        self.assertEqual(cpu.EIP, 4160640684)
        self.assertEqual(cpu.EAX, 114)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 791436795)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_ADD_3(self):
        ''' Instruction ADD_3
            Groups:
            0xf7fe56aa:	add	edi, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem[0xf7fe56aa] = '\x01'
        mem[0xf7fe56ab] = '\xc7'
        cpu.EIP = 0xf7fe56aa
        cpu.EAX = 0x69
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0x6f268490
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe56aa], '\x01')
        self.assertEqual(mem[0xf7fe56ab], '\xc7')
        self.assertEqual(cpu.EIP, 4160640684)
        self.assertEqual(cpu.EAX, 105)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 1864795385)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_ADD_4(self):
        ''' Instruction ADD_4
            Groups:
            0xf7eaa0d9:	add	eax, 1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7eaa000, 0x1000, 'rwx')
        mem[0xf7eaa0d9] = '\x83'
        mem[0xf7eaa0da] = '\xc0'
        mem[0xf7eaa0db] = '\x01'
        cpu.EIP = 0xf7eaa0d9
        cpu.EAX = 0x26
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7eaa0d9], '\x83')
        self.assertEqual(mem[0xf7eaa0da], '\xc0')
        self.assertEqual(mem[0xf7eaa0db], '\x01')
        self.assertEqual(cpu.EIP, 4159348956)
        self.assertEqual(cpu.EAX, 39)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_ADD_5(self):
        ''' Instruction ADD_5
            Groups:
            0x8070234:	add	byte ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\xfe'
        mem[0x08070234] = '\x80'
        mem[0x08070235] = 'E'
        mem[0x08070236] = '\x00'
        mem[0x08070237] = '\xff'
        cpu.EIP = 0x8070234
        cpu.EBP = 0xffffb600
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\xfd')
        self.assertEqual(mem[0x8070234], '\x80')
        self.assertEqual(mem[0x8070235], 'E')
        self.assertEqual(mem[0x8070236], '\x00')
        self.assertEqual(mem[0x8070237], '\xff')
        self.assertEqual(cpu.EIP, 134677048)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.SF, True)

    def test_ADD_6(self):
        ''' Instruction ADD_6
            Groups:
            0xf7fe71b6:	add	esi, 8
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71b8] = '\x08'
        mem[0xf7fe71b6] = '\x83'
        mem[0xf7fe71b7] = '\xc6'
        cpu.EIP = 0xf7fe71b6
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.ESI = 0xf7e2b534
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe71b8], '\x08')
        self.assertEqual(mem[0xf7fe71b6], '\x83')
        self.assertEqual(mem[0xf7fe71b7], '\xc6')
        self.assertEqual(cpu.EIP, 4160647609)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4158829884)
        self.assertEqual(cpu.SF, True)

    def test_ADD_7(self):
        ''' Instruction ADD_7
            Groups:
            0xf7fe71aa:	add	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71aa] = '\x01'
        mem[0xf7fe71ab] = '\xd0'
        cpu.EIP = 0xf7fe71aa
        cpu.EAX = 0x1a9498
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xf7e15000
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe71aa], '\x01')
        self.assertEqual(mem[0xf7fe71ab], '\xd0')
        self.assertEqual(cpu.EIP, 4160647596)
        self.assertEqual(cpu.EAX, 4160480408)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EDX, 4158738432)
        self.assertEqual(cpu.SF, True)

    def test_ADD_8(self):
        ''' Instruction ADD_8
            Groups:
            0xf7fe56a2:	add	edx, 1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem[0xf7fe56a2] = '\x83'
        mem[0xf7fe56a3] = '\xc2'
        mem[0xf7fe56a4] = '\x01'
        cpu.EIP = 0xf7fe56a2
        cpu.EDX = 0xf7e23c44
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe56a2], '\x83')
        self.assertEqual(mem[0xf7fe56a3], '\xc2')
        self.assertEqual(mem[0xf7fe56a4], '\x01')
        self.assertEqual(cpu.EIP, 4160640677)
        self.assertEqual(cpu.EDX, 4158798917)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, True)

    def test_ADD_9(self):
        ''' Instruction ADD_9
            Groups:
            0xf7fe56a8:	add	edi, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem[0xf7fe56a8] = '\x01'
        mem[0xf7fe56a9] = '\xcf'
        cpu.EIP = 0xf7fe56a8
        cpu.PF = False
        cpu.ECX = 0xfecf2720
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0xc7f67939
        cpu.CF = False
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe56a8], '\x01')
        self.assertEqual(mem[0xf7fe56a9], '\xcf')
        self.assertEqual(cpu.EIP, 4160640682)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.ECX, 4274988832)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 3334840409)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.SF, True)

    def test_AND_1(self):
        ''' Instruction AND_1
            Groups:
            0x806c452:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806c000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0806c452] = '\x81'
        mem[0x0806c453] = 'e'
        mem[0x0806c454] = '\x00'
        mem[0x0806c455] = '\xff'
        mem[0x0806c456] = '\x00'
        mem[0x0806c457] = '\x00'
        mem[0x0806c458] = '\x00'
        cpu.EIP = 0x806c452
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x806c452], '\x81')
        self.assertEqual(mem[0x806c453], 'e')
        self.assertEqual(mem[0x806c454], '\x00')
        self.assertEqual(mem[0x806c455], '\xff')
        self.assertEqual(mem[0x806c456], '\x00')
        self.assertEqual(mem[0x806c457], '\x00')
        self.assertEqual(mem[0x806c458], '\x00')
        self.assertEqual(cpu.EIP, 134661209)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_10(self):
        ''' Instruction AND_10
            Groups:
            0xf7fe88dd:	and	edx, 3
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe8000, 0x1000, 'rwx')
        mem[0xf7fe88dd] = '\x83'
        mem[0xf7fe88de] = '\xe2'
        mem[0xf7fe88df] = '\x03'
        cpu.EIP = 0xf7fe88dd
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.PF = True
        cpu.EDX = 0x21
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe88dd], '\x83')
        self.assertEqual(mem[0xf7fe88de], '\xe2')
        self.assertEqual(mem[0xf7fe88df], '\x03')
        self.assertEqual(cpu.EIP, 4160653536)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.SF, False)

    def test_AND_11(self):
        ''' Instruction AND_11
            Groups:
            0xf7ff3eed:	and	edx, 0x1010100
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3eed] = '\x81'
        mem[0xf7ff3eee] = '\xe2'
        mem[0xf7ff3eef] = '\x00'
        mem[0xf7ff3ef0] = '\x01'
        mem[0xf7ff3ef1] = '\x01'
        mem[0xf7ff3ef2] = '\x01'
        cpu.EIP = 0xf7ff3eed
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.PF = False
        cpu.EDX = 0xfefcfef8
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7ff3eed], '\x81')
        self.assertEqual(mem[0xf7ff3eee], '\xe2')
        self.assertEqual(mem[0xf7ff3eef], '\x00')
        self.assertEqual(mem[0xf7ff3ef0], '\x01')
        self.assertEqual(mem[0xf7ff3ef1], '\x01')
        self.assertEqual(mem[0xf7ff3ef2], '\x01')
        self.assertEqual(cpu.EIP, 4160700147)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.SF, False)

    def test_AND_12(self):
        ''' Instruction AND_12
            Groups:
            0x804a3e4:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804a000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0804a3e4] = '\x81'
        mem[0x0804a3e5] = 'e'
        mem[0x0804a3e6] = '\x00'
        mem[0x0804a3e7] = '\xff'
        mem[0x0804a3e8] = '\x00'
        mem[0x0804a3e9] = '\x00'
        mem[0x0804a3ea] = '\x00'
        cpu.EIP = 0x804a3e4
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x804a3e4], '\x81')
        self.assertEqual(mem[0x804a3e5], 'e')
        self.assertEqual(mem[0x804a3e6], '\x00')
        self.assertEqual(mem[0x804a3e7], '\xff')
        self.assertEqual(mem[0x804a3e8], '\x00')
        self.assertEqual(mem[0x804a3e9], '\x00')
        self.assertEqual(mem[0x804a3ea], '\x00')
        self.assertEqual(cpu.EIP, 134521835)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_13(self):
        ''' Instruction AND_13
            Groups:
            0x8069701:	and	edx, 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08069000, 0x1000, 'rwx')
        mem[0x08069701] = '\x81'
        mem[0x08069702] = '\xe2'
        mem[0x08069703] = '\xff'
        mem[0x08069704] = '\x00'
        mem[0x08069705] = '\x00'
        mem[0x08069706] = '\x00'
        cpu.EIP = 0x8069701
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.PF = True
        cpu.EDX = 0x0
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x8069701], '\x81')
        self.assertEqual(mem[0x8069702], '\xe2')
        self.assertEqual(mem[0x8069703], '\xff')
        self.assertEqual(mem[0x8069704], '\x00')
        self.assertEqual(mem[0x8069705], '\x00')
        self.assertEqual(mem[0x8069706], '\x00')
        self.assertEqual(cpu.EIP, 134649607)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.SF, False)

    def test_AND_14(self):
        ''' Instruction AND_14
            Groups:
            0x8065b70:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08065000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x10'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08065b70] = '\x81'
        mem[0x08065b71] = 'e'
        mem[0x08065b72] = '\x00'
        mem[0x08065b73] = '\xff'
        mem[0x08065b74] = '\x00'
        mem[0x08065b75] = '\x00'
        mem[0x08065b76] = '\x00'
        cpu.EIP = 0x8065b70
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x10')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8065b70], '\x81')
        self.assertEqual(mem[0x8065b71], 'e')
        self.assertEqual(mem[0x8065b72], '\x00')
        self.assertEqual(mem[0x8065b73], '\xff')
        self.assertEqual(mem[0x8065b74], '\x00')
        self.assertEqual(mem[0x8065b75], '\x00')
        self.assertEqual(mem[0x8065b76], '\x00')
        self.assertEqual(cpu.EIP, 134634359)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_15(self):
        ''' Instruction AND_15
            Groups:
            0x8064eb1:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08064000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x10'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08064eb1] = '\x81'
        mem[0x08064eb2] = 'e'
        mem[0x08064eb3] = '\x00'
        mem[0x08064eb4] = '\xff'
        mem[0x08064eb5] = '\x00'
        mem[0x08064eb6] = '\x00'
        mem[0x08064eb7] = '\x00'
        cpu.EIP = 0x8064eb1
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x10')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8064eb1], '\x81')
        self.assertEqual(mem[0x8064eb2], 'e')
        self.assertEqual(mem[0x8064eb3], '\x00')
        self.assertEqual(mem[0x8064eb4], '\xff')
        self.assertEqual(mem[0x8064eb5], '\x00')
        self.assertEqual(mem[0x8064eb6], '\x00')
        self.assertEqual(mem[0x8064eb7], '\x00')
        self.assertEqual(cpu.EIP, 134631096)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_16(self):
        ''' Instruction AND_16
            Groups:
            0x806b598:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806b000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0806b598] = '\x81'
        mem[0x0806b599] = 'e'
        mem[0x0806b59a] = '\x00'
        mem[0x0806b59b] = '\xff'
        mem[0x0806b59c] = '\x00'
        mem[0x0806b59d] = '\x00'
        mem[0x0806b59e] = '\x00'
        cpu.EIP = 0x806b598
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x806b598], '\x81')
        self.assertEqual(mem[0x806b599], 'e')
        self.assertEqual(mem[0x806b59a], '\x00')
        self.assertEqual(mem[0x806b59b], '\xff')
        self.assertEqual(mem[0x806b59c], '\x00')
        self.assertEqual(mem[0x806b59d], '\x00')
        self.assertEqual(mem[0x806b59e], '\x00')
        self.assertEqual(cpu.EIP, 134657439)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_17(self):
        ''' Instruction AND_17
            Groups:
            0x805b447:	and	eax, 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805b448] = '\xff'
        mem[0x0805b449] = '\x00'
        mem[0x0805b44a] = '\x00'
        mem[0x0805b44b] = '\x00'
        mem[0x0805b447] = '%'
        cpu.EIP = 0x805b447
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EAX = 0xeb
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x805b448], '\xff')
        self.assertEqual(mem[0x805b449], '\x00')
        self.assertEqual(mem[0x805b44a], '\x00')
        self.assertEqual(mem[0x805b44b], '\x00')
        self.assertEqual(mem[0x805b447], '%')
        self.assertEqual(cpu.EIP, 134591564)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EAX, 235)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AND_18(self):
        ''' Instruction AND_18
            Groups:
            0x805a902:	and	eax, 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805a000, 0x1000, 'rwx')
        mem[0x0805a902] = '%'
        mem[0x0805a903] = '\xff'
        mem[0x0805a904] = '\x00'
        mem[0x0805a905] = '\x00'
        mem[0x0805a906] = '\x00'
        cpu.EIP = 0x805a902
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EAX = 0xeb
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x805a902], '%')
        self.assertEqual(mem[0x805a903], '\xff')
        self.assertEqual(mem[0x805a904], '\x00')
        self.assertEqual(mem[0x805a905], '\x00')
        self.assertEqual(mem[0x805a906], '\x00')
        self.assertEqual(cpu.EIP, 134588679)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EAX, 235)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AND_19(self):
        ''' Instruction AND_19
            Groups:
            0x806aae2:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806a000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0806aae2] = '\x81'
        mem[0x0806aae3] = 'e'
        mem[0x0806aae4] = '\x00'
        mem[0x0806aae5] = '\xff'
        mem[0x0806aae6] = '\x00'
        mem[0x0806aae7] = '\x00'
        mem[0x0806aae8] = '\x00'
        cpu.EIP = 0x806aae2
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x806aae2], '\x81')
        self.assertEqual(mem[0x806aae3], 'e')
        self.assertEqual(mem[0x806aae4], '\x00')
        self.assertEqual(mem[0x806aae5], '\xff')
        self.assertEqual(mem[0x806aae6], '\x00')
        self.assertEqual(mem[0x806aae7], '\x00')
        self.assertEqual(mem[0x806aae8], '\x00')
        self.assertEqual(cpu.EIP, 134654697)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_2(self):
        ''' Instruction AND_2
            Groups:
            0x805dc21:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0805dc21] = '\x81'
        mem[0x0805dc22] = 'e'
        mem[0x0805dc23] = '\x00'
        mem[0x0805dc24] = '\xff'
        mem[0x0805dc25] = '\x00'
        mem[0x0805dc26] = '\x00'
        mem[0x0805dc27] = '\x00'
        cpu.EIP = 0x805dc21
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x805dc21], '\x81')
        self.assertEqual(mem[0x805dc22], 'e')
        self.assertEqual(mem[0x805dc23], '\x00')
        self.assertEqual(mem[0x805dc24], '\xff')
        self.assertEqual(mem[0x805dc25], '\x00')
        self.assertEqual(mem[0x805dc26], '\x00')
        self.assertEqual(mem[0x805dc27], '\x00')
        self.assertEqual(cpu.EIP, 134601768)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_20(self):
        ''' Instruction AND_20
            Groups:
            0x805a4fc:	and	eax, 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805a000, 0x1000, 'rwx')
        mem[0x0805a500] = '\x00'
        mem[0x0805a4fc] = '%'
        mem[0x0805a4fd] = '\xff'
        mem[0x0805a4fe] = '\x00'
        mem[0x0805a4ff] = '\x00'
        cpu.EIP = 0x805a4fc
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EAX = 0xeb
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x805a500], '\x00')
        self.assertEqual(mem[0x805a4fc], '%')
        self.assertEqual(mem[0x805a4fd], '\xff')
        self.assertEqual(mem[0x805a4fe], '\x00')
        self.assertEqual(mem[0x805a4ff], '\x00')
        self.assertEqual(cpu.EIP, 134587649)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.EAX, 235)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_AND_21(self):
        ''' Instruction AND_21
            Groups:
            0x8060799:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08060000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08060799] = '\x81'
        mem[0x0806079a] = 'e'
        mem[0x0806079b] = '\x00'
        mem[0x0806079c] = '\xff'
        mem[0x0806079d] = '\x00'
        mem[0x0806079e] = '\x00'
        mem[0x0806079f] = '\x00'
        cpu.EIP = 0x8060799
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8060799], '\x81')
        self.assertEqual(mem[0x806079a], 'e')
        self.assertEqual(mem[0x806079b], '\x00')
        self.assertEqual(mem[0x806079c], '\xff')
        self.assertEqual(mem[0x806079d], '\x00')
        self.assertEqual(mem[0x806079e], '\x00')
        self.assertEqual(mem[0x806079f], '\x00')
        self.assertEqual(cpu.EIP, 134612896)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_3(self):
        ''' Instruction AND_3
            Groups:
            0x806e0cf:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806e000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0806e0cf] = '\x81'
        mem[0x0806e0d0] = 'e'
        mem[0x0806e0d1] = '\x00'
        mem[0x0806e0d2] = '\xff'
        mem[0x0806e0d3] = '\x00'
        mem[0x0806e0d4] = '\x00'
        mem[0x0806e0d5] = '\x00'
        cpu.EIP = 0x806e0cf
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = True
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x806e0cf], '\x81')
        self.assertEqual(mem[0x806e0d0], 'e')
        self.assertEqual(mem[0x806e0d1], '\x00')
        self.assertEqual(mem[0x806e0d2], '\xff')
        self.assertEqual(mem[0x806e0d3], '\x00')
        self.assertEqual(mem[0x806e0d4], '\x00')
        self.assertEqual(mem[0x806e0d5], '\x00')
        self.assertEqual(cpu.EIP, 134668502)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_4(self):
        ''' Instruction AND_4
            Groups:
            0x806cf9f:	and	edx, 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806c000, 0x1000, 'rwx')
        mem[0x0806cfa0] = '\xe2'
        mem[0x0806cfa1] = '\xff'
        mem[0x0806cfa2] = '\x00'
        mem[0x0806cfa3] = '\x00'
        mem[0x0806cfa4] = '\x00'
        mem[0x0806cf9f] = '\x81'
        cpu.EIP = 0x806cf9f
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.PF = True
        cpu.EDX = 0xfa
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x806cfa0], '\xe2')
        self.assertEqual(mem[0x806cfa1], '\xff')
        self.assertEqual(mem[0x806cfa2], '\x00')
        self.assertEqual(mem[0x806cfa3], '\x00')
        self.assertEqual(mem[0x806cfa4], '\x00')
        self.assertEqual(mem[0x806cf9f], '\x81')
        self.assertEqual(cpu.EIP, 134664101)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 250)
        self.assertEqual(cpu.SF, False)

    def test_AND_5(self):
        ''' Instruction AND_5
            Groups:
            0x8062394:	and	dword ptr [ebp], 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08062000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x10'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08062394] = '\x81'
        mem[0x08062395] = 'e'
        mem[0x08062396] = '\x00'
        mem[0x08062397] = '\xff'
        mem[0x08062398] = '\x00'
        mem[0x08062399] = '\x00'
        mem[0x0806239a] = '\x00'
        cpu.EIP = 0x8062394
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.EBP = 0xffffb600
        cpu.PF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x10')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8062394], '\x81')
        self.assertEqual(mem[0x8062395], 'e')
        self.assertEqual(mem[0x8062396], '\x00')
        self.assertEqual(mem[0x8062397], '\xff')
        self.assertEqual(mem[0x8062398], '\x00')
        self.assertEqual(mem[0x8062399], '\x00')
        self.assertEqual(mem[0x806239a], '\x00')
        self.assertEqual(cpu.EIP, 134620059)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.SF, False)

    def test_AND_6(self):
        ''' Instruction AND_6
            Groups:
            0xf7fe212b:	and	ecx, 7
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe2000, 0x1000, 'rwx')
        mem[0xf7fe212b] = '\x83'
        mem[0xf7fe212c] = '\xe1'
        mem[0xf7fe212d] = '\x07'
        cpu.EIP = 0xf7fe212b
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.PF = True
        cpu.SF = False
        cpu.ECX = 0x6
        cpu.execute()

        self.assertEqual(mem[0xf7fe212b], '\x83')
        self.assertEqual(mem[0xf7fe212c], '\xe1')
        self.assertEqual(mem[0xf7fe212d], '\x07')
        self.assertEqual(cpu.EIP, 4160626990)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.ECX, 6)

    def test_AND_7(self):
        ''' Instruction AND_7
            Groups:
            0x804bf30:	and	edx, 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804b000, 0x1000, 'rwx')
        mem[0x0804bf30] = '\x81'
        mem[0x0804bf31] = '\xe2'
        mem[0x0804bf32] = '\xff'
        mem[0x0804bf33] = '\x00'
        mem[0x0804bf34] = '\x00'
        mem[0x0804bf35] = '\x00'
        cpu.EIP = 0x804bf30
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.PF = True
        cpu.EDX = 0xf0
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x804bf30], '\x81')
        self.assertEqual(mem[0x804bf31], '\xe2')
        self.assertEqual(mem[0x804bf32], '\xff')
        self.assertEqual(mem[0x804bf33], '\x00')
        self.assertEqual(mem[0x804bf34], '\x00')
        self.assertEqual(mem[0x804bf35], '\x00')
        self.assertEqual(cpu.EIP, 134528822)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 240)
        self.assertEqual(cpu.SF, False)

    def test_AND_8(self):
        ''' Instruction AND_8
            Groups:
            0xf7fec3da:	and	edx, 0x7fff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec3da] = '\x81'
        mem[0xf7fec3db] = '\xe2'
        mem[0xf7fec3dc] = '\xff'
        mem[0xf7fec3dd] = '\x7f'
        mem[0xf7fec3de] = '\x00'
        mem[0xf7fec3df] = '\x00'
        cpu.EIP = 0xf7fec3da
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.PF = True
        cpu.EDX = 0x19
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fec3da], '\x81')
        self.assertEqual(mem[0xf7fec3db], '\xe2')
        self.assertEqual(mem[0xf7fec3dc], '\xff')
        self.assertEqual(mem[0xf7fec3dd], '\x7f')
        self.assertEqual(mem[0xf7fec3de], '\x00')
        self.assertEqual(mem[0xf7fec3df], '\x00')
        self.assertEqual(cpu.EIP, 4160668640)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.EDX, 25)
        self.assertEqual(cpu.SF, False)

    def test_AND_9(self):
        ''' Instruction AND_9
            Groups:
            0x80494c9:	and	edx, 0xff
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08049000, 0x1000, 'rwx')
        mem[0x080494c9] = '\x81'
        mem[0x080494ca] = '\xe2'
        mem[0x080494cb] = '\xff'
        mem[0x080494cc] = '\x00'
        mem[0x080494cd] = '\x00'
        mem[0x080494ce] = '\x00'
        cpu.EIP = 0x80494c9
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.PF = True
        cpu.EDX = 0xf0
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x80494c9], '\x81')
        self.assertEqual(mem[0x80494ca], '\xe2')
        self.assertEqual(mem[0x80494cb], '\xff')
        self.assertEqual(mem[0x80494cc], '\x00')
        self.assertEqual(mem[0x80494cd], '\x00')
        self.assertEqual(mem[0x80494ce], '\x00')
        self.assertEqual(cpu.EIP, 134517967)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 240)
        self.assertEqual(cpu.SF, False)

    def test_BSF_1(self):
        ''' Instruction BSF_1
            Groups:
            0x806b25c:	bsf	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806b000, 0x1000, 'rwx')
        mem[0x0806b25c] = 'f'
        mem[0x0806b25d] = '\x0f'
        mem[0x0806b25e] = '\xbc'
        mem[0x0806b25f] = '\xca'
        cpu.EIP = 0x806b25c
        cpu.ZF = True
        cpu.CX = 0x746e
        cpu.DX = 0xfa
        cpu.execute()

        self.assertEqual(mem[0x806b25c], 'f')
        self.assertEqual(mem[0x806b25d], '\x0f')
        self.assertEqual(mem[0x806b25e], '\xbc')
        self.assertEqual(mem[0x806b25f], '\xca')
        self.assertEqual(cpu.EIP, 134656608)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CX, 1)
        self.assertEqual(cpu.DX, 250)

    def test_BSF_2(self):
        ''' Instruction BSF_2
            Groups:
            0x806b294:	bsf	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806b000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0x0806b294] = 'f'
        mem[0x0806b295] = '\x0f'
        mem[0x0806b296] = '\xbc'
        mem[0x0806b297] = 'M'
        mem[0x0806b298] = '\x00'
        cpu.EIP = 0x806b294
        cpu.ZF = True
        cpu.CX = 0x1
        cpu.EBP = 0xffffb600
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x806b294], 'f')
        self.assertEqual(mem[0x806b295], '\x0f')
        self.assertEqual(mem[0x806b296], '\xbc')
        self.assertEqual(mem[0x806b297], 'M')
        self.assertEqual(mem[0x806b298], '\x00')
        self.assertEqual(cpu.EIP, 134656665)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CX, 1)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_BSF_3(self):
        ''' Instruction BSF_3
            Groups:
            0x806b335:	bsf	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806b000, 0x1000, 'rwx')
        mem[0x0806b335] = '\x0f'
        mem[0x0806b336] = '\xbc'
        mem[0x0806b337] = '\xca'
        cpu.EIP = 0x806b335
        cpu.ZF = True
        cpu.EDX = 0xfa
        cpu.ECX = 0x6c650001
        cpu.execute()

        self.assertEqual(mem[0x806b335], '\x0f')
        self.assertEqual(mem[0x806b336], '\xbc')
        self.assertEqual(mem[0x806b337], '\xca')
        self.assertEqual(cpu.EIP, 134656824)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDX, 250)
        self.assertEqual(cpu.ECX, 1)

    def test_BSF_4(self):
        ''' Instruction BSF_4
            Groups:
            0x806b36c:	bsf	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0806b000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0806b36c] = '\x0f'
        mem[0x0806b36d] = '\xbc'
        mem[0x0806b36e] = 'M'
        mem[0x0806b36f] = '\x00'
        cpu.EIP = 0x806b36c
        cpu.ZF = True
        cpu.EBP = 0xffffb600
        cpu.ECX = 0x1
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x806b36c], '\x0f')
        self.assertEqual(mem[0x806b36d], '\xbc')
        self.assertEqual(mem[0x806b36e], 'M')
        self.assertEqual(mem[0x806b36f], '\x00')
        self.assertEqual(cpu.EIP, 134656880)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 1)

    def test_BSR_1(self):
        ''' Instruction BSR_1
            Groups:
            0x80661a3:	bsr	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08066000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0x080661a3] = 'f'
        mem[0x080661a4] = '\x0f'
        mem[0x080661a5] = '\xbd'
        mem[0x080661a6] = 'M'
        mem[0x080661a7] = '\x00'
        cpu.EIP = 0x80661a3
        cpu.ZF = True
        cpu.CX = 0xfc00
        cpu.EBP = 0xffffb600
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x80661a3], 'f')
        self.assertEqual(mem[0x80661a4], '\x0f')
        self.assertEqual(mem[0x80661a5], '\xbd')
        self.assertEqual(mem[0x80661a6], 'M')
        self.assertEqual(mem[0x80661a7], '\x00')
        self.assertEqual(cpu.EIP, 134635944)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CX, 64512)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_BSR_2(self):
        ''' Instruction BSR_2
            Groups:
            0xf7e2e8e8:	bsr	ecx, dword ptr [esp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7e2e000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd600] = '\x1f'
        mem[0xffffd601] = '\x00'
        mem[0xffffd602] = '\x00'
        mem[0xffffd603] = '\x00'
        mem[0xf7e2e8e8] = '\x0f'
        mem[0xf7e2e8e9] = '\xbd'
        mem[0xf7e2e8ea] = '\x0c'
        mem[0xf7e2e8eb] = '$'
        cpu.EIP = 0xf7e2e8e8
        cpu.ZF = True
        cpu.ECX = 0x200
        cpu.ESP = 0xffffd600
        cpu.execute()

        self.assertEqual(mem[0xffffd600], '\x1f')
        self.assertEqual(mem[0xffffd601], '\x00')
        self.assertEqual(mem[0xffffd602], '\x00')
        self.assertEqual(mem[0xffffd603], '\x00')
        self.assertEqual(mem[0xf7e2e8e8], '\x0f')
        self.assertEqual(mem[0xf7e2e8e9], '\xbd')
        self.assertEqual(mem[0xf7e2e8ea], '\x0c')
        self.assertEqual(mem[0xf7e2e8eb], '$')
        self.assertEqual(cpu.EIP, 4158843116)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ESP, 4294956544)
        self.assertEqual(cpu.ECX, 4)

    def test_BSR_3(self):
        ''' Instruction BSR_3
            Groups:
            0x806627b:	bsr	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08066000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0806627b] = '\x0f'
        mem[0x0806627c] = '\xbd'
        mem[0x0806627d] = 'M'
        mem[0x0806627e] = '\x00'
        cpu.EIP = 0x806627b
        cpu.ZF = True
        cpu.EBP = 0xffffb600
        cpu.ECX = 0x80f1fc00
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x806627b], '\x0f')
        self.assertEqual(mem[0x806627c], '\xbd')
        self.assertEqual(mem[0x806627d], 'M')
        self.assertEqual(mem[0x806627e], '\x00')
        self.assertEqual(cpu.EIP, 134636159)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 2163342336)

    def test_BSR_4(self):
        ''' Instruction BSR_4
            Groups:
            0x8066244:	bsr	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08066000, 0x1000, 'rwx')
        mem[0x08066244] = '\x0f'
        mem[0x08066245] = '\xbd'
        mem[0x08066246] = '\xca'
        cpu.EIP = 0x8066244
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.ECX = 0x80f1fc00
        cpu.execute()

        self.assertEqual(mem[0x8066244], '\x0f')
        self.assertEqual(mem[0x8066245], '\xbd')
        self.assertEqual(mem[0x8066246], '\xca')
        self.assertEqual(cpu.EIP, 134636103)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.ECX, 2163342336)

    def test_BSR_5(self):
        ''' Instruction BSR_5
            Groups:
            0x806616b:	bsr	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08066000, 0x1000, 'rwx')
        mem[0x0806616b] = 'f'
        mem[0x0806616c] = '\x0f'
        mem[0x0806616d] = '\xbd'
        mem[0x0806616e] = '\xca'
        cpu.EIP = 0x806616b
        cpu.ZF = True
        cpu.CX = 0xfc00
        cpu.DX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x806616b], 'f')
        self.assertEqual(mem[0x806616c], '\x0f')
        self.assertEqual(mem[0x806616d], '\xbd')
        self.assertEqual(mem[0x806616e], '\xca')
        self.assertEqual(cpu.EIP, 134635887)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CX, 64512)
        self.assertEqual(cpu.DX, 0)

    def test_BSWAP_1(self):
        ''' Instruction BSWAP_1
            Groups:
            0x807937c:	bswap	ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x0807937c] = '\x0f'
        mem[0x0807937d] = '\xc9'
        cpu.EIP = 0x807937c
        cpu.ECX = 0x80008001
        cpu.execute()

        self.assertEqual(mem[0x807937c], '\x0f')
        self.assertEqual(mem[0x807937d], '\xc9')
        self.assertEqual(cpu.EIP, 134714238)
        self.assertEqual(cpu.ECX, 25165952)

    def test_BTC_1(self):
        ''' Instruction BTC_1
            Groups:
            0x8061077:	btc	ecx, 4
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08061000, 0x1000, 'rwx')
        mem[0x08061078] = '\xba'
        mem[0x08061079] = '\xf9'
        mem[0x0806107a] = '\x04'
        mem[0x08061077] = '\x0f'
        cpu.EIP = 0x8061077
        cpu.CF = False
        cpu.ECX = 0xffffffef
        cpu.execute()

        self.assertEqual(mem[0x8061078], '\xba')
        self.assertEqual(mem[0x8061079], '\xf9')
        self.assertEqual(mem[0x806107a], '\x04')
        self.assertEqual(mem[0x8061077], '\x0f')
        self.assertEqual(cpu.EIP, 134615163)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ECX, 4294967295)

    def test_BTC_2(self):
        ''' Instruction BTC_2
            Groups:
            0x8060f33:	btc	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08060000, 0x1000, 'rwx')
        mem[0x08060f33] = 'f'
        mem[0x08060f34] = '\x0f'
        mem[0x08060f35] = '\xbb'
        mem[0x08060f36] = '\xd1'
        cpu.EIP = 0x8060f33
        cpu.CX = 0xffff
        cpu.CF = False
        cpu.DX = 0xec
        cpu.execute()

        self.assertEqual(mem[0x8060f33], 'f')
        self.assertEqual(mem[0x8060f34], '\x0f')
        self.assertEqual(mem[0x8060f35], '\xbb')
        self.assertEqual(mem[0x8060f36], '\xd1')
        self.assertEqual(cpu.EIP, 134614839)
        self.assertEqual(cpu.CX, 61439)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.DX, 236)

    def test_BTC_3(self):
        ''' Instruction BTC_3
            Groups:
            0x80610a2:	btc	ecx, -1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08061000, 0x1000, 'rwx')
        mem[0x080610a2] = '\x0f'
        mem[0x080610a3] = '\xba'
        mem[0x080610a4] = '\xf9'
        mem[0x080610a5] = '\xff'
        cpu.EIP = 0x80610a2
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0x80610a2], '\x0f')
        self.assertEqual(mem[0x80610a3], '\xba')
        self.assertEqual(mem[0x80610a4], '\xf9')
        self.assertEqual(mem[0x80610a5], '\xff')
        self.assertEqual(cpu.EIP, 134615206)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.ECX, 2147483647)

    def test_BTC_4(self):
        ''' Instruction BTC_4
            Groups:
            0x8060fac:	btc	cx, 4
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08060000, 0x1000, 'rwx')
        mem[0x08060fb0] = '\x04'
        mem[0x08060fac] = 'f'
        mem[0x08060fad] = '\x0f'
        mem[0x08060fae] = '\xba'
        mem[0x08060faf] = '\xf9'
        cpu.EIP = 0x8060fac
        cpu.CX = 0xefff
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0x8060fb0], '\x04')
        self.assertEqual(mem[0x8060fac], 'f')
        self.assertEqual(mem[0x8060fad], '\x0f')
        self.assertEqual(mem[0x8060fae], '\xba')
        self.assertEqual(mem[0x8060faf], '\xf9')
        self.assertEqual(cpu.EIP, 134614961)
        self.assertEqual(cpu.CX, 61423)
        self.assertEqual(cpu.CF, True)

    def test_BTC_5(self):
        ''' Instruction BTC_5
            Groups:
            0x806100c:	btc	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08061000, 0x1000, 'rwx')
        mem[0x0806100c] = '\x0f'
        mem[0x0806100d] = '\xbb'
        mem[0x0806100e] = '\xd1'
        cpu.EIP = 0x806100c
        cpu.EDX = 0xec
        cpu.CF = False
        cpu.ECX = 0xffffefef
        cpu.execute()

        self.assertEqual(mem[0x806100c], '\x0f')
        self.assertEqual(mem[0x806100d], '\xbb')
        self.assertEqual(mem[0x806100e], '\xd1')
        self.assertEqual(cpu.EIP, 134615055)
        self.assertEqual(cpu.EDX, 236)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ECX, 4294967279)

    def test_BTR_1(self):
        ''' Instruction BTR_1
            Groups:
            0x805beed:	btr	ecx, -1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bef0] = '\xff'
        mem[0x0805beed] = '\x0f'
        mem[0x0805beee] = '\xba'
        mem[0x0805beef] = '\xf1'
        cpu.EIP = 0x805beed
        cpu.CF = False
        cpu.ECX = 0x80000000
        cpu.execute()

        self.assertEqual(mem[0x805bef0], '\xff')
        self.assertEqual(mem[0x805beed], '\x0f')
        self.assertEqual(mem[0x805beee], '\xba')
        self.assertEqual(mem[0x805beef], '\xf1')
        self.assertEqual(cpu.EIP, 134594289)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.ECX, 0)

    def test_BTR_2(self):
        ''' Instruction BTR_2
            Groups:
            0x805bec2:	btr	ecx, 4
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bec2] = '\x0f'
        mem[0x0805bec3] = '\xba'
        mem[0x0805bec4] = '\xf1'
        mem[0x0805bec5] = '\x04'
        cpu.EIP = 0x805bec2
        cpu.CF = False
        cpu.ECX = 0x80000000
        cpu.execute()

        self.assertEqual(mem[0x805bec2], '\x0f')
        self.assertEqual(mem[0x805bec3], '\xba')
        self.assertEqual(mem[0x805bec4], '\xf1')
        self.assertEqual(mem[0x805bec5], '\x04')
        self.assertEqual(cpu.EIP, 134594246)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ECX, 2147483648)

    def test_BTR_3(self):
        ''' Instruction BTR_3
            Groups:
            0x805bdf7:	btr	cx, 4
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bdf8] = '\x0f'
        mem[0x0805bdf9] = '\xba'
        mem[0x0805bdfa] = '\xf1'
        mem[0x0805bdfb] = '\x04'
        mem[0x0805bdf7] = 'f'
        cpu.EIP = 0x805bdf7
        cpu.CX = 0x10
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0x805bdf8], '\x0f')
        self.assertEqual(mem[0x805bdf9], '\xba')
        self.assertEqual(mem[0x805bdfa], '\xf1')
        self.assertEqual(mem[0x805bdfb], '\x04')
        self.assertEqual(mem[0x805bdf7], 'f')
        self.assertEqual(cpu.EIP, 134594044)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.CF, True)

    def test_BTR_4(self):
        ''' Instruction BTR_4
            Groups:
            0x805be57:	btr	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805be58] = '\xb3'
        mem[0x0805be59] = '\xd1'
        mem[0x0805be57] = '\x0f'
        cpu.EIP = 0x805be57
        cpu.EDX = 0xec
        cpu.CF = False
        cpu.ECX = 0x80000000
        cpu.execute()

        self.assertEqual(mem[0x805be58], '\xb3')
        self.assertEqual(mem[0x805be59], '\xd1')
        self.assertEqual(mem[0x805be57], '\x0f')
        self.assertEqual(cpu.EIP, 134594138)
        self.assertEqual(cpu.EDX, 236)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ECX, 2147483648)

    def test_BTR_5(self):
        ''' Instruction BTR_5
            Groups:
            0x805bd7e:	btr	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bd80] = '\xb3'
        mem[0x0805bd81] = '\xd1'
        mem[0x0805bd7e] = 'f'
        mem[0x0805bd7f] = '\x0f'
        cpu.EIP = 0x805bd7e
        cpu.CX = 0x1010
        cpu.CF = False
        cpu.DX = 0xec
        cpu.execute()

        self.assertEqual(mem[0x805bd80], '\xb3')
        self.assertEqual(mem[0x805bd81], '\xd1')
        self.assertEqual(mem[0x805bd7e], 'f')
        self.assertEqual(mem[0x805bd7f], '\x0f')
        self.assertEqual(cpu.EIP, 134593922)
        self.assertEqual(cpu.CX, 16)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.DX, 236)

    def test_BTS_1(self):
        ''' Instruction BTS_1
            Groups:
            0x805bbab:	bts	ecx, 4
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bbab] = '\x0f'
        mem[0x0805bbac] = '\xba'
        mem[0x0805bbad] = '\xe9'
        mem[0x0805bbae] = '\x04'
        cpu.EIP = 0x805bbab
        cpu.CF = True
        cpu.ECX = 0x1010
        cpu.execute()

        self.assertEqual(mem[0x805bbab], '\x0f')
        self.assertEqual(mem[0x805bbac], '\xba')
        self.assertEqual(mem[0x805bbad], '\xe9')
        self.assertEqual(mem[0x805bbae], '\x04')
        self.assertEqual(cpu.EIP, 134593455)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.ECX, 4112)

    def test_BTS_2(self):
        ''' Instruction BTS_2
            Groups:
            0x805bba8:	bts	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bba8] = '\x0f'
        mem[0x0805bba9] = '\xab'
        mem[0x0805bbaa] = '\xd1'
        cpu.EIP = 0x805bba8
        cpu.EDX = 0x3ec
        cpu.CF = False
        cpu.ECX = 0x1010
        cpu.execute()

        self.assertEqual(mem[0x805bba8], '\x0f')
        self.assertEqual(mem[0x805bba9], '\xab')
        self.assertEqual(mem[0x805bbaa], '\xd1')
        self.assertEqual(cpu.EIP, 134593451)
        self.assertEqual(cpu.EDX, 1004)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.ECX, 4112)

    def test_BTS_3(self):
        ''' Instruction BTS_3
            Groups:
            0x805bba3:	bts	cx, 4
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bba3] = 'f'
        mem[0x0805bba4] = '\x0f'
        mem[0x0805bba5] = '\xba'
        mem[0x0805bba6] = '\xe9'
        mem[0x0805bba7] = '\x04'
        cpu.EIP = 0x805bba3
        cpu.CX = 0x1000
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0x805bba3], 'f')
        self.assertEqual(mem[0x805bba4], '\x0f')
        self.assertEqual(mem[0x805bba5], '\xba')
        self.assertEqual(mem[0x805bba6], '\xe9')
        self.assertEqual(mem[0x805bba7], '\x04')
        self.assertEqual(cpu.EIP, 134593448)
        self.assertEqual(cpu.CX, 4112)
        self.assertEqual(cpu.CF, False)

    def test_BTS_4(self):
        ''' Instruction BTS_4
            Groups:
            0x805bb9f:	bts	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bba0] = '\x0f'
        mem[0x0805bba1] = '\xab'
        mem[0x0805bba2] = '\xd1'
        mem[0x0805bb9f] = 'f'
        cpu.EIP = 0x805bb9f
        cpu.CX = 0x0
        cpu.CF = False
        cpu.DX = 0x3ec
        cpu.execute()

        self.assertEqual(mem[0x805bba0], '\x0f')
        self.assertEqual(mem[0x805bba1], '\xab')
        self.assertEqual(mem[0x805bba2], '\xd1')
        self.assertEqual(mem[0x805bb9f], 'f')
        self.assertEqual(cpu.EIP, 134593443)
        self.assertEqual(cpu.CX, 4096)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.DX, 1004)

    def test_BTS_5(self):
        ''' Instruction BTS_5
            Groups:
            0x805bbaf:	bts	ecx, -1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0805b000, 0x1000, 'rwx')
        mem[0x0805bbb0] = '\xba'
        mem[0x0805bbb1] = '\xe9'
        mem[0x0805bbb2] = '\xff'
        mem[0x0805bbaf] = '\x0f'
        cpu.EIP = 0x805bbaf
        cpu.CF = True
        cpu.ECX = 0x1010
        cpu.execute()

        self.assertEqual(mem[0x805bbb0], '\xba')
        self.assertEqual(mem[0x805bbb1], '\xe9')
        self.assertEqual(mem[0x805bbb2], '\xff')
        self.assertEqual(mem[0x805bbaf], '\x0f')
        self.assertEqual(cpu.EIP, 134593459)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ECX, 2147487760)

    def test_BT_1(self):
        ''' Instruction BT_1
            Groups:
            0x80486c3:	bt	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08048000, 0x1000, 'rwx')
        mem[0x080486c3] = '\x0f'
        mem[0x080486c4] = '\xa3'
        mem[0x080486c5] = '\xd1'
        cpu.EIP = 0x80486c3
        cpu.EDX = 0xf0
        cpu.CF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x80486c3], '\x0f')
        self.assertEqual(mem[0x80486c4], '\xa3')
        self.assertEqual(mem[0x80486c5], '\xd1')
        self.assertEqual(cpu.EIP, 134514374)
        self.assertEqual(cpu.EDX, 240)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ECX, 0)

    def test_BT_10(self):
        ''' Instruction BT_10
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_11(self):
        ''' Instruction BT_11
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x2
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 2)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_12(self):
        ''' Instruction BT_12
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_13(self):
        ''' Instruction BT_13
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_14(self):
        ''' Instruction BT_14
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_15(self):
        ''' Instruction BT_15
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_16(self):
        ''' Instruction BT_16
            Groups:
            0x80485ea:	bt	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08048000, 0x1000, 'rwx')
        mem[0x080485ea] = 'f'
        mem[0x080485eb] = '\x0f'
        mem[0x080485ec] = '\xa3'
        mem[0x080485ed] = '\xd1'
        cpu.EIP = 0x80485ea
        cpu.CX = 0x0
        cpu.CF = False
        cpu.DX = 0xf0
        cpu.execute()

        self.assertEqual(mem[0x80485ea], 'f')
        self.assertEqual(mem[0x80485eb], '\x0f')
        self.assertEqual(mem[0x80485ec], '\xa3')
        self.assertEqual(mem[0x80485ed], '\xd1')
        self.assertEqual(cpu.EIP, 134514158)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.DX, 240)

    def test_BT_17(self):
        ''' Instruction BT_17
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_18(self):
        ''' Instruction BT_18
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_19(self):
        ''' Instruction BT_19
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_2(self):
        ''' Instruction BT_2
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_20(self):
        ''' Instruction BT_20
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_21(self):
        ''' Instruction BT_21
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_3(self):
        ''' Instruction BT_3
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_4(self):
        ''' Instruction BT_4
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_5(self):
        ''' Instruction BT_5
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_6(self):
        ''' Instruction BT_6
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_7(self):
        ''' Instruction BT_7
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_BT_8(self):
        ''' Instruction BT_8
            Groups:
            0x8048759:	bt	ecx, -1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08048000, 0x1000, 'rwx')
        mem[0x08048759] = '\x0f'
        mem[0x0804875a] = '\xba'
        mem[0x0804875b] = '\xe1'
        mem[0x0804875c] = '\xff'
        cpu.EIP = 0x8048759
        cpu.CF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x8048759], '\x0f')
        self.assertEqual(mem[0x804875a], '\xba')
        self.assertEqual(mem[0x804875b], '\xe1')
        self.assertEqual(mem[0x804875c], '\xff')
        self.assertEqual(cpu.EIP, 134514525)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ECX, 0)

    def test_BT_9(self):
        ''' Instruction BT_9
            Groups:
            0xf7fe4cc0:	bt	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4cc0] = '\x0f'
        mem[0xf7fe4cc1] = '\xa3'
        mem[0xf7fe4cc2] = '\xd0'
        cpu.EIP = 0xf7fe4cc0
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.EAX = 0x467
        cpu.execute()

        self.assertEqual(mem[0xf7fe4cc0], '\x0f')
        self.assertEqual(mem[0xf7fe4cc1], '\xa3')
        self.assertEqual(mem[0xf7fe4cc2], '\xd0')
        self.assertEqual(cpu.EIP, 4160638147)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.EAX, 1127)

    def test_CALL_1(self):
        ''' Instruction CALL_1
            Groups: call, not64bitmode
            0xf7fec303:	call	0xf7fdc820
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd400] = '\x03'
        mem[0xffffd401] = '\x00'
        mem[0xffffd402] = '\x00'
        mem[0xf7fec303] = '\xe8'
        mem[0xf7fec304] = '\x18'
        mem[0xf7fec305] = '\x05'
        mem[0xf7fec306] = '\xff'
        mem[0xf7fec307] = '\xff'
        mem[0xffffd403] = '\x00'
        mem[0xffffd404] = '\x10'
        mem[0xffffd3fc] = '\xc1'
        mem[0xffffd3fd] = '\xc1'
        mem[0xffffd3fe] = '\xfe'
        mem[0xffffd3ff] = '\xf7'
        cpu.EIP = 0xf7fec303
        cpu.EBP = 0xffffd488
        cpu.ESP = 0xffffd400
        cpu.execute()

        self.assertEqual(mem[0xffffd400], '\x03')
        self.assertEqual(mem[0xffffd401], '\x00')
        self.assertEqual(mem[0xffffd402], '\x00')
        self.assertEqual(mem[0xf7fec303], '\xe8')
        self.assertEqual(mem[0xf7fec304], '\x18')
        self.assertEqual(mem[0xf7fec305], '\x05')
        self.assertEqual(mem[0xf7fec306], '\xff')
        self.assertEqual(mem[0xf7fec307], '\xff')
        self.assertEqual(mem[0xffffd403], '\x00')
        self.assertEqual(mem[0xffffd404], '\x10')
        self.assertEqual(mem[0xffffd3fc], '\x08')
        self.assertEqual(mem[0xffffd3fd], '\xc3')
        self.assertEqual(mem[0xffffd3fe], '\xfe')
        self.assertEqual(mem[0xffffd3ff], '\xf7')
        self.assertEqual(cpu.EIP, 4160604192)
        self.assertEqual(cpu.EBP, 4294956168)
        self.assertEqual(cpu.ESP, 4294956028)

    def test_CALL_10(self):
        ''' Instruction CALL_10
            Groups: call, not64bitmode
            0xf7ff0819:	call	0xf7ff0590
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff0000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7ff0819] = '\xe8'
        mem[0xf7ff081a] = 'r'
        mem[0xf7ff081b] = '\xfd'
        mem[0xffffd01c] = '\x1e'
        mem[0xffffd01d] = '\x08'
        mem[0xffffd01e] = '\xff'
        mem[0xffffd01f] = '\xf7'
        mem[0xffffd020] = '\xcd'
        mem[0xffffd021] = '^'
        mem[0xffffd022] = '\xff'
        mem[0xffffd023] = '\xf7'
        mem[0xffffd024] = '\x00'
        mem[0xf7ff081c] = '\xff'
        mem[0xf7ff081d] = '\xff'
        cpu.EIP = 0xf7ff0819
        cpu.EBP = 0x306
        cpu.ESP = 0xffffd020
        cpu.execute()

        self.assertEqual(mem[0xf7ff0819], '\xe8')
        self.assertEqual(mem[0xf7ff081a], 'r')
        self.assertEqual(mem[0xf7ff081b], '\xfd')
        self.assertEqual(mem[0xf7ff081c], '\xff')
        self.assertEqual(mem[0xf7ff081d], '\xff')
        self.assertEqual(mem[0xffffd01e], '\xff')
        self.assertEqual(mem[0xffffd01f], '\xf7')
        self.assertEqual(mem[0xffffd020], '\xcd')
        self.assertEqual(mem[0xffffd021], '^')
        self.assertEqual(mem[0xffffd022], '\xff')
        self.assertEqual(mem[0xffffd023], '\xf7')
        self.assertEqual(mem[0xffffd024], '\x00')
        self.assertEqual(mem[0xffffd01c], '\x1e')
        self.assertEqual(mem[0xffffd01d], '\x08')
        self.assertEqual(cpu.EIP, 4160685456)
        self.assertEqual(cpu.EBP, 774)
        self.assertEqual(cpu.ESP, 4294955036)

    def test_CALL_11(self):
        ''' Instruction CALL_11
            Groups: call, not64bitmode
            0xf7fe54ef:	call	0xf7fe4c80
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd2f3] = '\xf7'
        mem[0xffffd2ef] = '\xf7'
        mem[0xf7fe54f0] = '\x8c'
        mem[0xf7fe54f1] = '\xf7'
        mem[0xffffd2ec] = '4'
        mem[0xffffd2ed] = 'N'
        mem[0xffffd2ee] = '\xfe'
        mem[0xf7fe54ef] = '\xe8'
        mem[0xffffd2f0] = '\xc4'
        mem[0xffffd2f1] = '\xb1'
        mem[0xf7fe54f2] = '\xff'
        mem[0xf7fe54f3] = '\xff'
        mem[0xffffd2f4] = '\xdc'
        mem[0xffffd2f2] = '\xfd'
        cpu.EIP = 0xf7fe54ef
        cpu.EBP = 0xf7fdab18
        cpu.ESP = 0xffffd2f0
        cpu.execute()

        self.assertEqual(mem[0xffffd2f3], '\xf7')
        self.assertEqual(mem[0xffffd2ef], '\xf7')
        self.assertEqual(mem[0xffffd2f0], '\xc4')
        self.assertEqual(mem[0xffffd2f1], '\xb1')
        self.assertEqual(mem[0xffffd2ec], '\xf4')
        self.assertEqual(mem[0xffffd2ed], 'T')
        self.assertEqual(mem[0xffffd2ee], '\xfe')
        self.assertEqual(mem[0xf7fe54ef], '\xe8')
        self.assertEqual(mem[0xf7fe54f0], '\x8c')
        self.assertEqual(mem[0xf7fe54f1], '\xf7')
        self.assertEqual(mem[0xf7fe54f2], '\xff')
        self.assertEqual(mem[0xf7fe54f3], '\xff')
        self.assertEqual(mem[0xffffd2f4], '\xdc')
        self.assertEqual(mem[0xffffd2f2], '\xfd')
        self.assertEqual(cpu.EIP, 4160638080)
        self.assertEqual(cpu.EBP, 4160596760)
        self.assertEqual(cpu.ESP, 4294955756)

    def test_CALL_12(self):
        ''' Instruction CALL_12
            Groups: call, not64bitmode
            0xf7fe72f3:	call	0xf7fe5670
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd440] = '\x10'
        mem[0xffffd441] = '\xaa'
        mem[0xffffd442] = '\xfd'
        mem[0xffffd443] = '\xf7'
        mem[0xffffd444] = '\xa8'
        mem[0xf7fe72f3] = '\xe8'
        mem[0xf7fe72f4] = 'x'
        mem[0xf7fe72f5] = '\xe3'
        mem[0xf7fe72f6] = '\xff'
        mem[0xf7fe72f7] = '\xff'
        mem[0xffffd43c] = '\xf8'
        mem[0xffffd43d] = 'r'
        mem[0xffffd43e] = '\xfe'
        mem[0xffffd43f] = '\xf7'
        cpu.EIP = 0xf7fe72f3
        cpu.EBP = 0xffffd4f8
        cpu.ESP = 0xffffd440
        cpu.execute()

        self.assertEqual(mem[0xffffd440], '\x10')
        self.assertEqual(mem[0xffffd441], '\xaa')
        self.assertEqual(mem[0xffffd442], '\xfd')
        self.assertEqual(mem[0xffffd443], '\xf7')
        self.assertEqual(mem[0xffffd444], '\xa8')
        self.assertEqual(mem[0xf7fe72f3], '\xe8')
        self.assertEqual(mem[0xf7fe72f4], 'x')
        self.assertEqual(mem[0xf7fe72f5], '\xe3')
        self.assertEqual(mem[0xf7fe72f6], '\xff')
        self.assertEqual(mem[0xf7fe72f7], '\xff')
        self.assertEqual(mem[0xffffd43c], '\xf8')
        self.assertEqual(mem[0xffffd43d], 'r')
        self.assertEqual(mem[0xffffd43e], '\xfe')
        self.assertEqual(mem[0xffffd43f], '\xf7')
        self.assertEqual(cpu.EIP, 4160640624)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.ESP, 4294956092)

    def test_CALL_13(self):
        ''' Instruction CALL_13
            Groups: call, not64bitmode
            0xf7fe8bc3:	call	0xf7ff45f0
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe8000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7fe8bc3] = '\xe8'
        mem[0xf7fe8bc4] = '('
        mem[0xf7fe8bc5] = '\xba'
        mem[0xf7fe8bc6] = '\x00'
        mem[0xf7fe8bc7] = '\x00'
        mem[0xffffd34c] = '\x9d'
        mem[0xffffd34d] = '\x8b'
        mem[0xffffd34e] = '\xfe'
        mem[0xffffd34f] = '\xf7'
        mem[0xffffd350] = '\xf4'
        mem[0xffffd351] = '\xaa'
        mem[0xffffd352] = '\xfd'
        mem[0xffffd353] = '\xf7'
        mem[0xffffd354] = '\x80'
        cpu.EIP = 0xf7fe8bc3
        cpu.EBP = 0xffffd4f8
        cpu.ESP = 0xffffd350
        cpu.execute()

        self.assertEqual(mem[0xf7fe8bc3], '\xe8')
        self.assertEqual(mem[0xf7fe8bc4], '(')
        self.assertEqual(mem[0xf7fe8bc5], '\xba')
        self.assertEqual(mem[0xf7fe8bc6], '\x00')
        self.assertEqual(mem[0xf7fe8bc7], '\x00')
        self.assertEqual(mem[0xffffd34c], '\xc8')
        self.assertEqual(mem[0xffffd34d], '\x8b')
        self.assertEqual(mem[0xffffd34e], '\xfe')
        self.assertEqual(mem[0xffffd34f], '\xf7')
        self.assertEqual(mem[0xffffd350], '\xf4')
        self.assertEqual(mem[0xffffd351], '\xaa')
        self.assertEqual(mem[0xffffd352], '\xfd')
        self.assertEqual(mem[0xffffd353], '\xf7')
        self.assertEqual(mem[0xffffd354], '\x80')
        self.assertEqual(cpu.EIP, 4160701936)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.ESP, 4294955852)

    def test_CALL_14(self):
        ''' Instruction CALL_14
            Groups: call, not64bitmode
            0xf7eaa007:	call	0xf7f3b7db
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7eaa000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd580] = '\x00'
        mem[0xffffd581] = '\x00'
        mem[0xffffd582] = '\x00'
        mem[0xffffd583] = '\x00'
        mem[0xffffd584] = '\x00'
        mem[0xf7eaa007] = '\xe8'
        mem[0xf7eaa008] = '\xcf'
        mem[0xf7eaa009] = '\x17'
        mem[0xf7eaa00a] = '\t'
        mem[0xf7eaa00b] = '\x00'
        mem[0xffffd57c] = '\x0c'
        mem[0xffffd57d] = '\xa0'
        mem[0xffffd57e] = '\xea'
        mem[0xffffd57f] = '\xf7'
        cpu.EIP = 0xf7eaa007
        cpu.EBP = 0xc2
        cpu.ESP = 0xffffd580
        cpu.execute()

        self.assertEqual(mem[0xffffd580], '\x00')
        self.assertEqual(mem[0xffffd581], '\x00')
        self.assertEqual(mem[0xffffd582], '\x00')
        self.assertEqual(mem[0xffffd583], '\x00')
        self.assertEqual(mem[0xffffd584], '\x00')
        self.assertEqual(mem[0xf7eaa007], '\xe8')
        self.assertEqual(mem[0xf7eaa008], '\xcf')
        self.assertEqual(mem[0xf7eaa009], '\x17')
        self.assertEqual(mem[0xf7eaa00a], '\t')
        self.assertEqual(mem[0xf7eaa00b], '\x00')
        self.assertEqual(mem[0xffffd57c], '\x0c')
        self.assertEqual(mem[0xffffd57d], '\xa0')
        self.assertEqual(mem[0xffffd57e], '\xea')
        self.assertEqual(mem[0xffffd57f], '\xf7')
        self.assertEqual(cpu.EIP, 4159944667)
        self.assertEqual(cpu.EBP, 194)
        self.assertEqual(cpu.ESP, 4294956412)

    def test_CALL_15(self):
        ''' Instruction CALL_15
            Groups: call, not64bitmode
            0xf7feabc3:	call	dword ptr [ebx + 0x558]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fea000, 0x1000, 'rwx')
        mem.mmap(0xf7ffd000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd340] = '\x00'
        mem[0xffffd341] = '\x00'
        mem[0xffffd342] = '\x00'
        mem[0xf7feabc3] = '\xff'
        mem[0xf7feabc4] = '\x93'
        mem[0xf7feabc5] = 'X'
        mem[0xf7feabc6] = '\x05'
        mem[0xf7feabc7] = '\x00'
        mem[0xf7feabc8] = '\x00'
        mem[0xffffd344] = '\x00'
        mem[0xffffd343] = '\x00'
        mem[0xf7ffd558] = ' '
        mem[0xf7ffd559] = '\xd1'
        mem[0xf7ffd55a] = '\xfd'
        mem[0xf7ffd55b] = '\xf7'
        mem[0xffffd33c] = '\x00'
        mem[0xffffd33d] = '\x00'
        mem[0xffffd33e] = '\x00'
        mem[0xffffd33f] = '\x00'
        cpu.EIP = 0xf7feabc3
        cpu.EBP = 0xffffd4f8
        cpu.EBX = 0xf7ffd000
        cpu.ESP = 0xffffd340
        cpu.execute()

        self.assertEqual(mem[0xffffd340], '\x00')
        self.assertEqual(mem[0xffffd341], '\x00')
        self.assertEqual(mem[0xffffd342], '\x00')
        self.assertEqual(mem[0xf7feabc3], '\xff')
        self.assertEqual(mem[0xf7feabc4], '\x93')
        self.assertEqual(mem[0xf7feabc5], 'X')
        self.assertEqual(mem[0xf7feabc6], '\x05')
        self.assertEqual(mem[0xf7feabc7], '\x00')
        self.assertEqual(mem[0xf7feabc8], '\x00')
        self.assertEqual(mem[0xffffd344], '\x00')
        self.assertEqual(mem[0xffffd343], '\x00')
        self.assertEqual(mem[0xf7ffd558], ' ')
        self.assertEqual(mem[0xf7ffd559], '\xd1')
        self.assertEqual(mem[0xf7ffd55a], '\xfd')
        self.assertEqual(mem[0xf7ffd55b], '\xf7')
        self.assertEqual(mem[0xffffd33c], '\xc9')
        self.assertEqual(mem[0xffffd33d], '\xab')
        self.assertEqual(mem[0xffffd33e], '\xfe')
        self.assertEqual(mem[0xffffd33f], '\xf7')
        self.assertEqual(cpu.EIP, 4160606496)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.EBX, 4160737280)
        self.assertEqual(cpu.ESP, 4294955836)

    def test_CALL_16(self):
        ''' Instruction CALL_16
            Groups: call, not64bitmode
            0xf7fe72f3:	call	0xf7fe5670
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd440] = '\x10'
        mem[0xffffd441] = '\xaa'
        mem[0xffffd442] = '\xfd'
        mem[0xffffd443] = '\xf7'
        mem[0xffffd444] = '\xa8'
        mem[0xf7fe72f3] = '\xe8'
        mem[0xf7fe72f4] = 'x'
        mem[0xf7fe72f5] = '\xe3'
        mem[0xf7fe72f6] = '\xff'
        mem[0xf7fe72f7] = '\xff'
        mem[0xffffd43c] = '\xf8'
        mem[0xffffd43d] = 'r'
        mem[0xffffd43e] = '\xfe'
        mem[0xffffd43f] = '\xf7'
        cpu.EIP = 0xf7fe72f3
        cpu.EBP = 0xffffd4f8
        cpu.ESP = 0xffffd440
        cpu.execute()

        self.assertEqual(mem[0xffffd440], '\x10')
        self.assertEqual(mem[0xffffd441], '\xaa')
        self.assertEqual(mem[0xffffd442], '\xfd')
        self.assertEqual(mem[0xffffd443], '\xf7')
        self.assertEqual(mem[0xffffd444], '\xa8')
        self.assertEqual(mem[0xf7fe72f3], '\xe8')
        self.assertEqual(mem[0xf7fe72f4], 'x')
        self.assertEqual(mem[0xf7fe72f5], '\xe3')
        self.assertEqual(mem[0xf7fe72f6], '\xff')
        self.assertEqual(mem[0xf7fe72f7], '\xff')
        self.assertEqual(mem[0xffffd43c], '\xf8')
        self.assertEqual(mem[0xffffd43d], 'r')
        self.assertEqual(mem[0xffffd43e], '\xfe')
        self.assertEqual(mem[0xffffd43f], '\xf7')
        self.assertEqual(cpu.EIP, 4160640624)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.ESP, 4294956092)

    def test_CALL_17(self):
        ''' Instruction CALL_17
            Groups: call, not64bitmode
            0xf7fe568c:	call	0xf7ff4768
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd380] = '\xe8'
        mem[0xffffd381] = '\xd3'
        mem[0xffffd382] = '\xff'
        mem[0xffffd383] = '\xff'
        mem[0xffffd384] = '\xd4'
        mem[0xf7fe568c] = '\xe8'
        mem[0xf7fe568d] = '\xd7'
        mem[0xf7fe568e] = '\xf0'
        mem[0xf7fe568f] = '\x00'
        mem[0xf7fe5690] = '\x00'
        mem[0xffffd37c] = 'z'
        mem[0xffffd37d] = 'W'
        mem[0xffffd37e] = '\xfe'
        mem[0xffffd37f] = '\xf7'
        cpu.EIP = 0xf7fe568c
        cpu.EBP = 0xffffd438
        cpu.ESP = 0xffffd380
        cpu.execute()

        self.assertEqual(mem[0xffffd380], '\xe8')
        self.assertEqual(mem[0xffffd381], '\xd3')
        self.assertEqual(mem[0xffffd382], '\xff')
        self.assertEqual(mem[0xffffd383], '\xff')
        self.assertEqual(mem[0xffffd384], '\xd4')
        self.assertEqual(mem[0xf7fe568c], '\xe8')
        self.assertEqual(mem[0xf7fe568d], '\xd7')
        self.assertEqual(mem[0xf7fe568e], '\xf0')
        self.assertEqual(mem[0xf7fe568f], '\x00')
        self.assertEqual(mem[0xf7fe5690], '\x00')
        self.assertEqual(mem[0xffffd37c], '\x91')
        self.assertEqual(mem[0xffffd37d], 'V')
        self.assertEqual(mem[0xffffd37e], '\xfe')
        self.assertEqual(mem[0xffffd37f], '\xf7')
        self.assertEqual(cpu.EIP, 4160702312)
        self.assertEqual(cpu.EBP, 4294956088)
        self.assertEqual(cpu.ESP, 4294955900)

    def test_CALL_18(self):
        ''' Instruction CALL_18
            Groups: call, not64bitmode
            0xf7ff0a62:	call	0xf7ff0590
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff0000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd022] = '\xff'
        mem[0xffffd023] = '\xf7'
        mem[0xffffd024] = '\x00'
        mem[0xffffd01c] = '\x1e'
        mem[0xffffd01d] = '\x08'
        mem[0xffffd01e] = '\xff'
        mem[0xffffd01f] = '\xf7'
        mem[0xffffd020] = '\xcd'
        mem[0xffffd021] = '^'
        mem[0xf7ff0a62] = '\xe8'
        mem[0xf7ff0a63] = ')'
        mem[0xf7ff0a64] = '\xfb'
        mem[0xf7ff0a65] = '\xff'
        mem[0xf7ff0a66] = '\xff'
        cpu.EIP = 0xf7ff0a62
        cpu.EBP = 0x340
        cpu.ESP = 0xffffd020
        cpu.execute()

        self.assertEqual(mem[0xffffd022], '\xff')
        self.assertEqual(mem[0xffffd023], '\xf7')
        self.assertEqual(mem[0xffffd024], '\x00')
        self.assertEqual(mem[0xffffd01c], 'g')
        self.assertEqual(mem[0xffffd01d], '\n')
        self.assertEqual(mem[0xffffd01e], '\xff')
        self.assertEqual(mem[0xffffd01f], '\xf7')
        self.assertEqual(mem[0xffffd020], '\xcd')
        self.assertEqual(mem[0xffffd021], '^')
        self.assertEqual(mem[0xf7ff0a62], '\xe8')
        self.assertEqual(mem[0xf7ff0a63], ')')
        self.assertEqual(mem[0xf7ff0a64], '\xfb')
        self.assertEqual(mem[0xf7ff0a65], '\xff')
        self.assertEqual(mem[0xf7ff0a66], '\xff')
        self.assertEqual(cpu.EIP, 4160685456)
        self.assertEqual(cpu.EBP, 832)
        self.assertEqual(cpu.ESP, 4294955036)

    def test_CALL_19(self):
        ''' Instruction CALL_19
            Groups: call, not64bitmode
            0xf7fe4d98:	call	0xf7ff3e60
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7fe4d98] = '\xe8'
        mem[0xf7fe4d99] = '\xc3'
        mem[0xf7fe4d9a] = '\xf0'
        mem[0xf7fe4d9b] = '\x00'
        mem[0xf7fe4d9c] = '\x00'
        mem[0xffffd2ac] = '\x97'
        mem[0xffffd2ad] = 'L'
        mem[0xffffd2ae] = '\xfe'
        mem[0xffffd2af] = '\xf7'
        mem[0xffffd2b0] = 'a'
        mem[0xffffd2b1] = '\x80'
        mem[0xffffd2b2] = '\xe2'
        mem[0xffffd2b3] = '\xf7'
        mem[0xffffd2b4] = 'a'
        cpu.EIP = 0xf7fe4d98
        cpu.EBP = 0xf7fdaba8
        cpu.ESP = 0xffffd2b0
        cpu.execute()

        self.assertEqual(mem[0xf7fe4d98], '\xe8')
        self.assertEqual(mem[0xf7fe4d99], '\xc3')
        self.assertEqual(mem[0xf7fe4d9a], '\xf0')
        self.assertEqual(mem[0xf7fe4d9b], '\x00')
        self.assertEqual(mem[0xf7fe4d9c], '\x00')
        self.assertEqual(mem[0xffffd2ac], '\x9d')
        self.assertEqual(mem[0xffffd2ad], 'M')
        self.assertEqual(mem[0xffffd2ae], '\xfe')
        self.assertEqual(mem[0xffffd2af], '\xf7')
        self.assertEqual(mem[0xffffd2b0], 'a')
        self.assertEqual(mem[0xffffd2b1], '\x80')
        self.assertEqual(mem[0xffffd2b2], '\xe2')
        self.assertEqual(mem[0xffffd2b3], '\xf7')
        self.assertEqual(mem[0xffffd2b4], 'a')
        self.assertEqual(cpu.EIP, 4160700000)
        self.assertEqual(cpu.EBP, 4160596904)
        self.assertEqual(cpu.ESP, 4294955692)

    def test_CALL_2(self):
        ''' Instruction CALL_2
            Groups: call, not64bitmode
            0xf7eaa8b1:	call	0xf7f3b7db
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7eaa000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd439] = '\xd0'
        mem[0xf7eaa8b1] = '\xe8'
        mem[0xf7eaa8b2] = '%'
        mem[0xf7eaa8b3] = '\x0f'
        mem[0xf7eaa8b4] = '\t'
        mem[0xf7eaa8b5] = '\x00'
        mem[0xffffd436] = '\xe9'
        mem[0xffffd437] = '\xf7'
        mem[0xffffd438] = '\x00'
        mem[0xffffd434] = 'v'
        mem[0xffffd43a] = '\xff'
        mem[0xffffd43b] = '\xf7'
        mem[0xffffd43c] = '\x8c'
        mem[0xffffd435] = 'x'
        cpu.EIP = 0xf7eaa8b1
        cpu.EBP = 0xffffd4f8
        cpu.ESP = 0xffffd438
        cpu.execute()

        self.assertEqual(mem[0xffffd439], '\xd0')
        self.assertEqual(mem[0xf7eaa8b1], '\xe8')
        self.assertEqual(mem[0xf7eaa8b2], '%')
        self.assertEqual(mem[0xf7eaa8b3], '\x0f')
        self.assertEqual(mem[0xf7eaa8b4], '\t')
        self.assertEqual(mem[0xf7eaa8b5], '\x00')
        self.assertEqual(mem[0xffffd436], '\xea')
        self.assertEqual(mem[0xffffd437], '\xf7')
        self.assertEqual(mem[0xffffd438], '\x00')
        self.assertEqual(mem[0xffffd434], '\xb6')
        self.assertEqual(mem[0xffffd43a], '\xff')
        self.assertEqual(mem[0xffffd43b], '\xf7')
        self.assertEqual(mem[0xffffd43c], '\x8c')
        self.assertEqual(mem[0xffffd435], '\xa8')
        self.assertEqual(cpu.EIP, 4159944667)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.ESP, 4294956084)

    def test_CALL_20(self):
        ''' Instruction CALL_20
            Groups: call, not64bitmode
            0xf7fe9d3c:	call	0xf7fdc810
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7fe9d40] = '\xff'
        mem[0xffffd3ec] = '\x1b'
        mem[0xffffd3ed] = '\x9c'
        mem[0xffffd3ee] = '\xfe'
        mem[0xffffd3ef] = '\xf7'
        mem[0xffffd3f0] = '\xb8'
        mem[0xffffd3f1] = '\x00'
        mem[0xffffd3f2] = '\x00'
        mem[0xffffd3f3] = '\x00'
        mem[0xffffd3f4] = '\x00'
        mem[0xf7fe9d3c] = '\xe8'
        mem[0xf7fe9d3d] = '\xcf'
        mem[0xf7fe9d3e] = '*'
        mem[0xf7fe9d3f] = '\xff'
        cpu.EIP = 0xf7fe9d3c
        cpu.EBP = 0xffffd498
        cpu.ESP = 0xffffd3f0
        cpu.execute()

        self.assertEqual(mem[0xf7fe9d40], '\xff')
        self.assertEqual(mem[0xffffd3ec], 'A')
        self.assertEqual(mem[0xffffd3ed], '\x9d')
        self.assertEqual(mem[0xffffd3ee], '\xfe')
        self.assertEqual(mem[0xffffd3ef], '\xf7')
        self.assertEqual(mem[0xffffd3f0], '\xb8')
        self.assertEqual(mem[0xffffd3f1], '\x00')
        self.assertEqual(mem[0xffffd3f2], '\x00')
        self.assertEqual(mem[0xffffd3f3], '\x00')
        self.assertEqual(mem[0xffffd3f4], '\x00')
        self.assertEqual(mem[0xf7fe9d3c], '\xe8')
        self.assertEqual(mem[0xf7fe9d3d], '\xcf')
        self.assertEqual(mem[0xf7fe9d3e], '*')
        self.assertEqual(mem[0xf7fe9d3f], '\xff')
        self.assertEqual(cpu.EIP, 4160604176)
        self.assertEqual(cpu.EBP, 4294956184)
        self.assertEqual(cpu.ESP, 4294956012)

    def test_CALL_21(self):
        ''' Instruction CALL_21
            Groups: call, not64bitmode
            0xf7fe3b46:	call	0xf7fdc810
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe3000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7fe3b46] = '\xe8'
        mem[0xf7fe3b47] = '\xc5'
        mem[0xf7fe3b48] = '\x8c'
        mem[0xf7fe3b49] = '\xff'
        mem[0xf7fe3b4a] = '\xff'
        mem[0xffffd49c] = '6'
        mem[0xffffd49d] = ';'
        mem[0xffffd49e] = '\xfe'
        mem[0xffffd49f] = '\xf7'
        mem[0xffffd4a0] = '\x14'
        mem[0xffffd4a1] = '\x00'
        mem[0xffffd4a2] = '\x00'
        mem[0xffffd4a3] = '\x00'
        mem[0xffffd4a4] = '\x00'
        cpu.EIP = 0xf7fe3b46
        cpu.EBP = 0xffffd4f8
        cpu.ESP = 0xffffd4a0
        cpu.execute()

        self.assertEqual(mem[0xf7fe3b46], '\xe8')
        self.assertEqual(mem[0xf7fe3b47], '\xc5')
        self.assertEqual(mem[0xf7fe3b48], '\x8c')
        self.assertEqual(mem[0xf7fe3b49], '\xff')
        self.assertEqual(mem[0xf7fe3b4a], '\xff')
        self.assertEqual(mem[0xffffd49c], 'K')
        self.assertEqual(mem[0xffffd49d], ';')
        self.assertEqual(mem[0xffffd49e], '\xfe')
        self.assertEqual(mem[0xffffd49f], '\xf7')
        self.assertEqual(mem[0xffffd4a0], '\x14')
        self.assertEqual(mem[0xffffd4a1], '\x00')
        self.assertEqual(mem[0xffffd4a2], '\x00')
        self.assertEqual(mem[0xffffd4a3], '\x00')
        self.assertEqual(mem[0xffffd4a4], '\x00')
        self.assertEqual(cpu.EIP, 4160604176)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.ESP, 4294956188)

    def test_CALL_3(self):
        ''' Instruction CALL_3
            Groups: call, not64bitmode
            0xf7fe4d98:	call	0xf7ff3e60
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7fe4d98] = '\xe8'
        mem[0xf7fe4d99] = '\xc3'
        mem[0xf7fe4d9a] = '\xf0'
        mem[0xf7fe4d9b] = '\x00'
        mem[0xf7fe4d9c] = '\x00'
        mem[0xffffd2ac] = '\xe2'
        mem[0xffffd2ad] = 'L'
        mem[0xffffd2ae] = '\xfe'
        mem[0xffffd2af] = '\xf7'
        mem[0xffffd2b0] = '4'
        mem[0xffffd2b1] = '\xc6'
        mem[0xffffd2b2] = '\xfd'
        mem[0xffffd2b3] = '\xf7'
        mem[0xffffd2b4] = '\xac'
        cpu.EIP = 0xf7fe4d98
        cpu.EBP = 0xf7fdadb8
        cpu.ESP = 0xffffd2b0
        cpu.execute()

        self.assertEqual(mem[0xf7fe4d98], '\xe8')
        self.assertEqual(mem[0xf7fe4d99], '\xc3')
        self.assertEqual(mem[0xf7fe4d9a], '\xf0')
        self.assertEqual(mem[0xf7fe4d9b], '\x00')
        self.assertEqual(mem[0xf7fe4d9c], '\x00')
        self.assertEqual(mem[0xffffd2ac], '\x9d')
        self.assertEqual(mem[0xffffd2ad], 'M')
        self.assertEqual(mem[0xffffd2ae], '\xfe')
        self.assertEqual(mem[0xffffd2af], '\xf7')
        self.assertEqual(mem[0xffffd2b0], '4')
        self.assertEqual(mem[0xffffd2b1], '\xc6')
        self.assertEqual(mem[0xffffd2b2], '\xfd')
        self.assertEqual(mem[0xffffd2b3], '\xf7')
        self.assertEqual(mem[0xffffd2b4], '\xac')
        self.assertEqual(cpu.EIP, 4160700000)
        self.assertEqual(cpu.EBP, 4160597432)
        self.assertEqual(cpu.ESP, 4294955692)

    def test_CALL_4(self):
        ''' Instruction CALL_4
            Groups: call, not64bitmode
            0xf7fe54ef:	call	0xf7fe4c80
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd2f3] = '\xf7'
        mem[0xffffd2ef] = '\xf7'
        mem[0xf7fe54f0] = '\x8c'
        mem[0xf7fe54f1] = '\xf7'
        mem[0xffffd2ec] = '4'
        mem[0xffffd2ed] = 'N'
        mem[0xffffd2ee] = '\xfe'
        mem[0xf7fe54ef] = '\xe8'
        mem[0xffffd2f0] = '\xc4'
        mem[0xffffd2f1] = '\xb1'
        mem[0xf7fe54f2] = '\xff'
        mem[0xf7fe54f3] = '\xff'
        mem[0xffffd2f4] = '\xdc'
        mem[0xffffd2f2] = '\xfd'
        cpu.EIP = 0xf7fe54ef
        cpu.EBP = 0xf7fdab18
        cpu.ESP = 0xffffd2f0
        cpu.execute()

        self.assertEqual(mem[0xffffd2f3], '\xf7')
        self.assertEqual(mem[0xffffd2ef], '\xf7')
        self.assertEqual(mem[0xffffd2f0], '\xc4')
        self.assertEqual(mem[0xffffd2f1], '\xb1')
        self.assertEqual(mem[0xffffd2ec], '\xf4')
        self.assertEqual(mem[0xffffd2ed], 'T')
        self.assertEqual(mem[0xffffd2ee], '\xfe')
        self.assertEqual(mem[0xf7fe54ef], '\xe8')
        self.assertEqual(mem[0xf7fe54f0], '\x8c')
        self.assertEqual(mem[0xf7fe54f1], '\xf7')
        self.assertEqual(mem[0xf7fe54f2], '\xff')
        self.assertEqual(mem[0xf7fe54f3], '\xff')
        self.assertEqual(mem[0xffffd2f4], '\xdc')
        self.assertEqual(mem[0xffffd2f2], '\xfd')
        self.assertEqual(cpu.EIP, 4160638080)
        self.assertEqual(cpu.EBP, 4160596760)
        self.assertEqual(cpu.ESP, 4294955756)

    def test_CALL_5(self):
        ''' Instruction CALL_5
            Groups: call, not64bitmode
            0xf7ff41d2:	call	0xf7ff4768
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xf7ff41d2] = '\xe8'
        mem[0xf7ff41d3] = '\x91'
        mem[0xf7ff41d4] = '\x05'
        mem[0xf7ff41d5] = '\x00'
        mem[0xf7ff41d6] = '\x00'
        mem[0xffffd030] = '\xd7'
        mem[0xffffd031] = 'A'
        mem[0xffffd032] = '\xff'
        mem[0xffffd033] = '\xf7'
        mem[0xffffd034] = 'D'
        mem[0xffffd035] = '\x00'
        mem[0xffffd036] = '\x00'
        mem[0xffffd037] = '\x00'
        mem[0xffffd038] = '\x00'
        cpu.EIP = 0xf7ff41d2
        cpu.EBP = 0xffffd088
        cpu.ESP = 0xffffd034
        cpu.execute()

        self.assertEqual(mem[0xf7ff41d2], '\xe8')
        self.assertEqual(mem[0xf7ff41d3], '\x91')
        self.assertEqual(mem[0xf7ff41d4], '\x05')
        self.assertEqual(mem[0xf7ff41d5], '\x00')
        self.assertEqual(mem[0xf7ff41d6], '\x00')
        self.assertEqual(mem[0xffffd030], '\xd7')
        self.assertEqual(mem[0xffffd031], 'A')
        self.assertEqual(mem[0xffffd032], '\xff')
        self.assertEqual(mem[0xffffd033], '\xf7')
        self.assertEqual(mem[0xffffd034], 'D')
        self.assertEqual(mem[0xffffd035], '\x00')
        self.assertEqual(mem[0xffffd036], '\x00')
        self.assertEqual(mem[0xffffd037], '\x00')
        self.assertEqual(mem[0xffffd038], '\x00')
        self.assertEqual(cpu.EIP, 4160702312)
        self.assertEqual(cpu.EBP, 4294955144)
        self.assertEqual(cpu.ESP, 4294955056)

    def test_CALL_6(self):
        ''' Instruction CALL_6
            Groups: call, not64bitmode
            0xf7fe568c:	call	0xf7ff4768
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd380] = '\xe8'
        mem[0xffffd381] = '\xd3'
        mem[0xffffd382] = '\xff'
        mem[0xffffd383] = '\xff'
        mem[0xffffd384] = '\xb8'
        mem[0xf7fe568c] = '\xe8'
        mem[0xf7fe568d] = '\xd7'
        mem[0xf7fe568e] = '\xf0'
        mem[0xf7fe568f] = '\x00'
        mem[0xf7fe5690] = '\x00'
        mem[0xffffd37c] = 'z'
        mem[0xffffd37d] = 'W'
        mem[0xffffd37e] = '\xfe'
        mem[0xffffd37f] = '\xf7'
        cpu.EIP = 0xf7fe568c
        cpu.EBP = 0xffffd438
        cpu.ESP = 0xffffd380
        cpu.execute()

        self.assertEqual(mem[0xffffd380], '\xe8')
        self.assertEqual(mem[0xffffd381], '\xd3')
        self.assertEqual(mem[0xffffd382], '\xff')
        self.assertEqual(mem[0xffffd383], '\xff')
        self.assertEqual(mem[0xffffd384], '\xb8')
        self.assertEqual(mem[0xf7fe568c], '\xe8')
        self.assertEqual(mem[0xf7fe568d], '\xd7')
        self.assertEqual(mem[0xf7fe568e], '\xf0')
        self.assertEqual(mem[0xf7fe568f], '\x00')
        self.assertEqual(mem[0xf7fe5690], '\x00')
        self.assertEqual(mem[0xffffd37c], '\x91')
        self.assertEqual(mem[0xffffd37d], 'V')
        self.assertEqual(mem[0xffffd37e], '\xfe')
        self.assertEqual(mem[0xffffd37f], '\xf7')
        self.assertEqual(cpu.EIP, 4160702312)
        self.assertEqual(cpu.EBP, 4294956088)
        self.assertEqual(cpu.ESP, 4294955900)

    def test_CALL_7(self):
        ''' Instruction CALL_7
            Groups: call, not64bitmode
            0xf7fe72f3:	call	0xf7fe5670
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd440] = '\x10'
        mem[0xffffd441] = '\xaa'
        mem[0xffffd442] = '\xfd'
        mem[0xffffd443] = '\xf7'
        mem[0xffffd444] = '\xa8'
        mem[0xf7fe72f3] = '\xe8'
        mem[0xf7fe72f4] = 'x'
        mem[0xf7fe72f5] = '\xe3'
        mem[0xf7fe72f6] = '\xff'
        mem[0xf7fe72f7] = '\xff'
        mem[0xffffd43c] = '\xf8'
        mem[0xffffd43d] = 'r'
        mem[0xffffd43e] = '\xfe'
        mem[0xffffd43f] = '\xf7'
        cpu.EIP = 0xf7fe72f3
        cpu.EBP = 0xffffd4f8
        cpu.ESP = 0xffffd440
        cpu.execute()

        self.assertEqual(mem[0xffffd440], '\x10')
        self.assertEqual(mem[0xffffd441], '\xaa')
        self.assertEqual(mem[0xffffd442], '\xfd')
        self.assertEqual(mem[0xffffd443], '\xf7')
        self.assertEqual(mem[0xffffd444], '\xa8')
        self.assertEqual(mem[0xf7fe72f3], '\xe8')
        self.assertEqual(mem[0xf7fe72f4], 'x')
        self.assertEqual(mem[0xf7fe72f5], '\xe3')
        self.assertEqual(mem[0xf7fe72f6], '\xff')
        self.assertEqual(mem[0xf7fe72f7], '\xff')
        self.assertEqual(mem[0xffffd43c], '\xf8')
        self.assertEqual(mem[0xffffd43d], 'r')
        self.assertEqual(mem[0xffffd43e], '\xfe')
        self.assertEqual(mem[0xffffd43f], '\xf7')
        self.assertEqual(cpu.EIP, 4160640624)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.ESP, 4294956092)

    def test_CALL_8(self):
        ''' Instruction CALL_8
            Groups: call, not64bitmode
            0xf7fe5775:	call	0xf7fe4e10
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd380] = '\xe8'
        mem[0xffffd381] = '\xd3'
        mem[0xffffd382] = '\xff'
        mem[0xffffd383] = '\xff'
        mem[0xffffd384] = 'D'
        mem[0xf7fe5775] = '\xe8'
        mem[0xf7fe5776] = '\x96'
        mem[0xf7fe5777] = '\xf6'
        mem[0xf7fe5778] = '\xff'
        mem[0xf7fe5779] = '\xff'
        mem[0xffffd37c] = '\x91'
        mem[0xffffd37d] = 'V'
        mem[0xffffd37e] = '\xfe'
        mem[0xffffd37f] = '\xf7'
        cpu.EIP = 0xf7fe5775
        cpu.EBP = 0xffffd438
        cpu.ESP = 0xffffd380
        cpu.execute()

        self.assertEqual(mem[0xffffd380], '\xe8')
        self.assertEqual(mem[0xffffd381], '\xd3')
        self.assertEqual(mem[0xffffd382], '\xff')
        self.assertEqual(mem[0xffffd383], '\xff')
        self.assertEqual(mem[0xffffd384], 'D')
        self.assertEqual(mem[0xf7fe5775], '\xe8')
        self.assertEqual(mem[0xf7fe5776], '\x96')
        self.assertEqual(mem[0xf7fe5777], '\xf6')
        self.assertEqual(mem[0xf7fe5778], '\xff')
        self.assertEqual(mem[0xf7fe5779], '\xff')
        self.assertEqual(mem[0xffffd37c], 'z')
        self.assertEqual(mem[0xffffd37d], 'W')
        self.assertEqual(mem[0xffffd37e], '\xfe')
        self.assertEqual(mem[0xffffd37f], '\xf7')
        self.assertEqual(cpu.EIP, 4160638480)
        self.assertEqual(cpu.EBP, 4294956088)
        self.assertEqual(cpu.ESP, 4294955900)

    def test_CALL_9(self):
        ''' Instruction CALL_9
            Groups: call, not64bitmode
            0xf7fe72f3:	call	0xf7fe5670
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd440] = '\x10'
        mem[0xffffd441] = '\xaa'
        mem[0xffffd442] = '\xfd'
        mem[0xffffd443] = '\xf7'
        mem[0xffffd444] = '\xa8'
        mem[0xf7fe72f3] = '\xe8'
        mem[0xf7fe72f4] = 'x'
        mem[0xf7fe72f5] = '\xe3'
        mem[0xf7fe72f6] = '\xff'
        mem[0xf7fe72f7] = '\xff'
        mem[0xffffd43c] = '\xf8'
        mem[0xffffd43d] = 'r'
        mem[0xffffd43e] = '\xfe'
        mem[0xffffd43f] = '\xf7'
        cpu.EIP = 0xf7fe72f3
        cpu.EBP = 0xffffd4f8
        cpu.ESP = 0xffffd440
        cpu.execute()

        self.assertEqual(mem[0xffffd440], '\x10')
        self.assertEqual(mem[0xffffd441], '\xaa')
        self.assertEqual(mem[0xffffd442], '\xfd')
        self.assertEqual(mem[0xffffd443], '\xf7')
        self.assertEqual(mem[0xffffd444], '\xa8')
        self.assertEqual(mem[0xf7fe72f3], '\xe8')
        self.assertEqual(mem[0xf7fe72f4], 'x')
        self.assertEqual(mem[0xf7fe72f5], '\xe3')
        self.assertEqual(mem[0xf7fe72f6], '\xff')
        self.assertEqual(mem[0xf7fe72f7], '\xff')
        self.assertEqual(mem[0xffffd43c], '\xf8')
        self.assertEqual(mem[0xffffd43d], 'r')
        self.assertEqual(mem[0xffffd43e], '\xfe')
        self.assertEqual(mem[0xffffd43f], '\xf7')
        self.assertEqual(cpu.EIP, 4160640624)
        self.assertEqual(cpu.EBP, 4294956280)
        self.assertEqual(cpu.ESP, 4294956092)

    def test_CBW_1(self):
        ''' Instruction CBW_1
            Groups:
            0x8060d84:	cbw
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08060000, 0x1000, 'rwx')
        mem[0x08060d84] = 'f'
        mem[0x08060d85] = '\x98'
        cpu.EIP = 0x8060d84
        cpu.AX = 0xeb
        cpu.execute()

        self.assertEqual(mem[0x8060d84], 'f')
        self.assertEqual(mem[0x8060d85], '\x98')
        self.assertEqual(cpu.EIP, 134614406)
        self.assertEqual(cpu.AX, 65515)

    def test_CDQ_1(self):
        ''' Instruction CDQ_1
            Groups:
            0x804d63b:	cdq
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d63b] = '\x99'
        cpu.EIP = 0x804d63b
        cpu.EDX = 0xf0
        cpu.EAX = 0xeb6eb6eb
        cpu.execute()

        self.assertEqual(mem[0x804d63b], '\x99')
        self.assertEqual(cpu.EIP, 134534716)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.EAX, 3949901547)

    def test_CDQ_2(self):
        ''' Instruction CDQ_2
            Groups:
            0x80702fa:	cdq
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x080702fa] = '\x99'
        cpu.EIP = 0x80702fa
        cpu.EDX = 0xfa
        cpu.EAX = 0xffffecf8
        cpu.execute()

        self.assertEqual(mem[0x80702fa], '\x99')
        self.assertEqual(cpu.EIP, 134677243)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.EAX, 4294962424)

    def test_CLC_1(self):
        ''' Instruction CLC_1
            Groups:
            0x80701bc:	clc
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x080701bc] = '\xf8'
        cpu.EIP = 0x80701bc
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0x80701bc], '\xf8')
        self.assertEqual(cpu.EIP, 134676925)
        self.assertEqual(cpu.CF, False)

    def test_CLD_1(self):
        ''' Instruction CLD_1
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_10(self):
        ''' Instruction CLD_10
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_11(self):
        ''' Instruction CLD_11
            Groups:
            0xf7ff4607:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4607] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4607
        cpu.execute()

        self.assertEqual(mem[0xf7ff4607], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701960)

    def test_CLD_12(self):
        ''' Instruction CLD_12
            Groups:
            0xf7ff4607:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4607] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4607
        cpu.execute()

        self.assertEqual(mem[0xf7ff4607], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701960)

    def test_CLD_13(self):
        ''' Instruction CLD_13
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_14(self):
        ''' Instruction CLD_14
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_15(self):
        ''' Instruction CLD_15
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_16(self):
        ''' Instruction CLD_16
            Groups:
            0xf7ff4607:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4607] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4607
        cpu.execute()

        self.assertEqual(mem[0xf7ff4607], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701960)

    def test_CLD_17(self):
        ''' Instruction CLD_17
            Groups:
            0xf7ff4607:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4607] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4607
        cpu.execute()

        self.assertEqual(mem[0xf7ff4607], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701960)

    def test_CLD_18(self):
        ''' Instruction CLD_18
            Groups:
            0xf7ff44e0:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff44e0] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff44e0
        cpu.execute()

        self.assertEqual(mem[0xf7ff44e0], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701665)

    def test_CLD_19(self):
        ''' Instruction CLD_19
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_2(self):
        ''' Instruction CLD_2
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_20(self):
        ''' Instruction CLD_20
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_21(self):
        ''' Instruction CLD_21
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_3(self):
        ''' Instruction CLD_3
            Groups:
            0xf7ff44e0:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff44e0] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff44e0
        cpu.execute()

        self.assertEqual(mem[0xf7ff44e0], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701665)

    def test_CLD_4(self):
        ''' Instruction CLD_4
            Groups:
            0xf7ff4540:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4540] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4540
        cpu.execute()

        self.assertEqual(mem[0xf7ff4540], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701761)

    def test_CLD_5(self):
        ''' Instruction CLD_5
            Groups:
            0xf7ff4607:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4607] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4607
        cpu.execute()

        self.assertEqual(mem[0xf7ff4607], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701960)

    def test_CLD_6(self):
        ''' Instruction CLD_6
            Groups:
            0xf7ff44e0:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff44e0] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff44e0
        cpu.execute()

        self.assertEqual(mem[0xf7ff44e0], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701665)

    def test_CLD_7(self):
        ''' Instruction CLD_7
            Groups:
            0xf7ff4607:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4607] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4607
        cpu.execute()

        self.assertEqual(mem[0xf7ff4607], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701960)

    def test_CLD_8(self):
        ''' Instruction CLD_8
            Groups:
            0x807019f:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x0807019f] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0x807019f
        cpu.execute()

        self.assertEqual(mem[0x807019f], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 134676896)

    def test_CLD_9(self):
        ''' Instruction CLD_9
            Groups:
            0xf7ff4607:	cld
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff4607] = '\xfc'
        cpu.DF = False
        cpu.EIP = 0xf7ff4607
        cpu.execute()

        self.assertEqual(mem[0xf7ff4607], '\xfc')
        self.assertEqual(cpu.DF, False)
        self.assertEqual(cpu.EIP, 4160701960)

    def test_CMOVAE_1(self):
        ''' Instruction CMOVAE_1
            Groups: cmov
            0xf7fec1d5:	cmovae	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec1d5] = '\x0f'
        mem[0xf7fec1d6] = 'C'
        mem[0xf7fec1d7] = '\xc1'
        cpu.EIP = 0xf7fec1d5
        cpu.EAX = 0x2
        cpu.CF = True
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fec1d5], '\x0f')
        self.assertEqual(mem[0xf7fec1d6], 'C')
        self.assertEqual(mem[0xf7fec1d7], '\xc1')
        self.assertEqual(cpu.EIP, 4160668120)
        self.assertEqual(cpu.ECX, 0)
        self.assertEqual(cpu.EAX, 2)

    def test_CMOVAE_10(self):
        ''' Instruction CMOVAE_10
            Groups: cmov
            0xf7fec1d5:	cmovae	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec1d5] = '\x0f'
        mem[0xf7fec1d6] = 'C'
        mem[0xf7fec1d7] = '\xc1'
        cpu.EIP = 0xf7fec1d5
        cpu.EAX = 0x23
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec1d5], '\x0f')
        self.assertEqual(mem[0xf7fec1d6], 'C')
        self.assertEqual(mem[0xf7fec1d7], '\xc1')
        self.assertEqual(cpu.EIP, 4160668120)
        self.assertEqual(cpu.ECX, 36)
        self.assertEqual(cpu.EAX, 36)

    def test_CMOVAE_11(self):
        ''' Instruction CMOVAE_11
            Groups: cmov
            0xf7fec2ae:	cmovae	edx, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2b0] = '\xd1'
        mem[0xf7fec2ae] = '\x0f'
        mem[0xf7fec2af] = 'C'
        cpu.EIP = 0xf7fec2ae
        cpu.EDX = 0x1
        cpu.CF = True
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fec2b0], '\xd1')
        self.assertEqual(mem[0xf7fec2ae], '\x0f')
        self.assertEqual(mem[0xf7fec2af], 'C')
        self.assertEqual(cpu.EIP, 4160668337)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVAE_12(self):
        ''' Instruction CMOVAE_12
            Groups: cmov
            0x8048431:	cmovae	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08048000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0x08048431] = 'f'
        mem[0x08048432] = '\x0f'
        mem[0x08048433] = 'C'
        mem[0x08048434] = 'M'
        mem[0x08048435] = '\x00'
        cpu.EIP = 0x8048431
        cpu.CX = 0x6ff0
        cpu.EBP = 0xffffb600
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x8048431], 'f')
        self.assertEqual(mem[0x8048432], '\x0f')
        self.assertEqual(mem[0x8048433], 'C')
        self.assertEqual(mem[0x8048434], 'M')
        self.assertEqual(mem[0x8048435], '\x00')
        self.assertEqual(cpu.EIP, 134513718)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVAE_2(self):
        ''' Instruction CMOVAE_2
            Groups: cmov
            0x8048439:	cmovae	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08048000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08048439] = '\x0f'
        mem[0x0804843a] = 'C'
        mem[0x0804843b] = 'M'
        mem[0x0804843c] = '\x00'
        cpu.EIP = 0x8048439
        cpu.EBP = 0xffffb600
        cpu.CF = False
        cpu.ECX = 0xe6fe6ff0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8048439], '\x0f')
        self.assertEqual(mem[0x804843a], 'C')
        self.assertEqual(mem[0x804843b], 'M')
        self.assertEqual(mem[0x804843c], '\x00')
        self.assertEqual(cpu.EIP, 134513725)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVAE_3(self):
        ''' Instruction CMOVAE_3
            Groups: cmov
            0xf7fec1d5:	cmovae	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec1d5] = '\x0f'
        mem[0xf7fec1d6] = 'C'
        mem[0xf7fec1d7] = '\xc1'
        cpu.EIP = 0xf7fec1d5
        cpu.EAX = 0x22
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec1d5], '\x0f')
        self.assertEqual(mem[0xf7fec1d6], 'C')
        self.assertEqual(mem[0xf7fec1d7], '\xc1')
        self.assertEqual(cpu.EIP, 4160668120)
        self.assertEqual(cpu.ECX, 36)
        self.assertEqual(cpu.EAX, 36)

    def test_CMOVAE_4(self):
        ''' Instruction CMOVAE_4
            Groups: cmov
            0xf7fec2ae:	cmovae	edx, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2b0] = '\xd1'
        mem[0xf7fec2ae] = '\x0f'
        mem[0xf7fec2af] = 'C'
        cpu.EIP = 0xf7fec2ae
        cpu.EDX = 0x1
        cpu.CF = True
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fec2b0], '\xd1')
        self.assertEqual(mem[0xf7fec2ae], '\x0f')
        self.assertEqual(mem[0xf7fec2af], 'C')
        self.assertEqual(cpu.EIP, 4160668337)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVAE_5(self):
        ''' Instruction CMOVAE_5
            Groups: cmov
            0xf7fec1d5:	cmovae	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec1d5] = '\x0f'
        mem[0xf7fec1d6] = 'C'
        mem[0xf7fec1d7] = '\xc1'
        cpu.EIP = 0xf7fec1d5
        cpu.EAX = 0x24
        cpu.CF = True
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fec1d5], '\x0f')
        self.assertEqual(mem[0xf7fec1d6], 'C')
        self.assertEqual(mem[0xf7fec1d7], '\xc1')
        self.assertEqual(cpu.EIP, 4160668120)
        self.assertEqual(cpu.ECX, 0)
        self.assertEqual(cpu.EAX, 36)

    def test_CMOVAE_6(self):
        ''' Instruction CMOVAE_6
            Groups: cmov
            0xf7fed76a:	cmovae	edx, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fed000, 0x1000, 'rwx')
        mem[0xf7fed76a] = '\x0f'
        mem[0xf7fed76b] = 'C'
        mem[0xf7fed76c] = '\xd1'
        cpu.EIP = 0xf7fed76a
        cpu.EDX = 0x1
        cpu.CF = True
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fed76a], '\x0f')
        self.assertEqual(mem[0xf7fed76b], 'C')
        self.assertEqual(mem[0xf7fed76c], '\xd1')
        self.assertEqual(cpu.EIP, 4160673645)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVAE_7(self):
        ''' Instruction CMOVAE_7
            Groups: cmov
            0x804842d:	cmovae	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08048000, 0x1000, 'rwx')
        mem[0x08048430] = '\xca'
        mem[0x0804842d] = 'f'
        mem[0x0804842e] = '\x0f'
        mem[0x0804842f] = 'C'
        cpu.EIP = 0x804842d
        cpu.CX = 0x0
        cpu.CF = False
        cpu.DX = 0x6ff0
        cpu.execute()

        self.assertEqual(mem[0x8048430], '\xca')
        self.assertEqual(mem[0x804842d], 'f')
        self.assertEqual(mem[0x804842e], '\x0f')
        self.assertEqual(mem[0x804842f], 'C')
        self.assertEqual(cpu.EIP, 134513713)
        self.assertEqual(cpu.CX, 28656)
        self.assertEqual(cpu.DX, 28656)

    def test_CMOVAE_8(self):
        ''' Instruction CMOVAE_8
            Groups: cmov
            0xf7fec2ae:	cmovae	edx, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2b0] = '\xd1'
        mem[0xf7fec2ae] = '\x0f'
        mem[0xf7fec2af] = 'C'
        cpu.EIP = 0xf7fec2ae
        cpu.EDX = 0x1
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2b0], '\xd1')
        self.assertEqual(mem[0xf7fec2ae], '\x0f')
        self.assertEqual(mem[0xf7fec2af], 'C')
        self.assertEqual(cpu.EIP, 4160668337)
        self.assertEqual(cpu.EDX, 36)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVAE_9(self):
        ''' Instruction CMOVAE_9
            Groups: cmov
            0x8048436:	cmovae	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08048000, 0x1000, 'rwx')
        mem[0x08048438] = '\xca'
        mem[0x08048436] = '\x0f'
        mem[0x08048437] = 'C'
        cpu.EIP = 0x8048436
        cpu.EDX = 0xe6fe6ff0
        cpu.CF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x8048438], '\xca')
        self.assertEqual(mem[0x8048436], '\x0f')
        self.assertEqual(mem[0x8048437], 'C')
        self.assertEqual(cpu.EIP, 134513721)
        self.assertEqual(cpu.EDX, 3875434480)
        self.assertEqual(cpu.ECX, 3875434480)

    def test_CMOVA_1(self):
        ''' Instruction CMOVA_1
            Groups: cmov
            0xf7fe231d:	cmova	edx, dword ptr [ebp - 0x9c]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe2000, 0x1000, 'rwx')
        mem.mmap(0xffffc000, 0x1000, 'rwx')
        mem[0xf7fe231d] = '\x0f'
        mem[0xf7fe231e] = 'G'
        mem[0xf7fe231f] = '\x95'
        mem[0xf7fe2320] = 'd'
        mem[0xf7fe2321] = '\xff'
        mem[0xf7fe2322] = '\xff'
        mem[0xf7fe2323] = '\xff'
        mem[0xffffcfec] = '|'
        mem[0xffffcfed] = ':'
        mem[0xffffcfee] = '\xfc'
        mem[0xffffcfef] = '\xf7'
        cpu.EIP = 0xf7fe231d
        cpu.ZF = False
        cpu.EBP = 0xffffd088
        cpu.CF = True
        cpu.EDX = 0xf7fc1000
        cpu.execute()

        self.assertEqual(mem[0xf7fe231d], '\x0f')
        self.assertEqual(mem[0xf7fe231e], 'G')
        self.assertEqual(mem[0xf7fe231f], '\x95')
        self.assertEqual(mem[0xf7fe2320], 'd')
        self.assertEqual(mem[0xf7fe2321], '\xff')
        self.assertEqual(mem[0xf7fe2322], '\xff')
        self.assertEqual(mem[0xf7fe2323], '\xff')
        self.assertEqual(mem[0xffffcfec], '|')
        self.assertEqual(mem[0xffffcfed], ':')
        self.assertEqual(mem[0xffffcfee], '\xfc')
        self.assertEqual(mem[0xffffcfef], '\xf7')
        self.assertEqual(cpu.EIP, 4160627492)
        self.assertEqual(cpu.EDX, 4160491520)
        self.assertEqual(cpu.EBP, 4294955144)

    def test_CMOVA_2(self):
        ''' Instruction CMOVA_2
            Groups: cmov
            0x804d67b:	cmova	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d67b] = 'f'
        mem[0x0804d67c] = '\x0f'
        mem[0x0804d67d] = 'G'
        mem[0x0804d67e] = '\xca'
        cpu.EIP = 0x804d67b
        cpu.ZF = True
        cpu.CX = 0x0
        cpu.CF = False
        cpu.DX = 0xffff
        cpu.execute()

        self.assertEqual(mem[0x804d67b], 'f')
        self.assertEqual(mem[0x804d67c], '\x0f')
        self.assertEqual(mem[0x804d67d], 'G')
        self.assertEqual(mem[0x804d67e], '\xca')
        self.assertEqual(cpu.EIP, 134534783)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.DX, 65535)

    def test_CMOVA_3(self):
        ''' Instruction CMOVA_3
            Groups: cmov
            0x804d67f:	cmova	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0x0804d680] = '\x0f'
        mem[0x0804d681] = 'G'
        mem[0x0804d682] = 'M'
        mem[0x0804d683] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb600] = '\x00'
        mem[0x0804d67f] = 'f'
        cpu.EIP = 0x804d67f
        cpu.ZF = True
        cpu.CX = 0x0
        cpu.EBP = 0xffffb600
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0x804d680], '\x0f')
        self.assertEqual(mem[0x804d681], 'G')
        self.assertEqual(mem[0x804d682], 'M')
        self.assertEqual(mem[0x804d683], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0x804d67f], 'f')
        self.assertEqual(cpu.EIP, 134534788)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVA_4(self):
        ''' Instruction CMOVA_4
            Groups: cmov
            0x804d684:	cmova	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d684] = '\x0f'
        mem[0x0804d685] = 'G'
        mem[0x0804d686] = '\xca'
        cpu.EIP = 0x804d684
        cpu.ZF = True
        cpu.CF = False
        cpu.EDX = 0xffffffff
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x804d684], '\x0f')
        self.assertEqual(mem[0x804d685], 'G')
        self.assertEqual(mem[0x804d686], '\xca')
        self.assertEqual(cpu.EIP, 134534791)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVA_5(self):
        ''' Instruction CMOVA_5
            Groups: cmov
            0x804d687:	cmova	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0804d687] = '\x0f'
        mem[0x0804d688] = 'G'
        mem[0x0804d689] = 'M'
        mem[0x0804d68a] = '\x00'
        cpu.EIP = 0x804d687
        cpu.ZF = True
        cpu.EBP = 0xffffb600
        cpu.CF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x804d687], '\x0f')
        self.assertEqual(mem[0x804d688], 'G')
        self.assertEqual(mem[0x804d689], 'M')
        self.assertEqual(mem[0x804d68a], '\x00')
        self.assertEqual(cpu.EIP, 134534795)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVBE_1(self):
        ''' Instruction CMOVBE_1
            Groups: cmov
            0x805988d:	cmovbe	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08059000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\xf4'
        mem[0xffffb601] = '\xc9'
        mem[0x0805988d] = 'f'
        mem[0x0805988e] = '\x0f'
        mem[0x0805988f] = 'F'
        mem[0x08059890] = 'M'
        mem[0x08059891] = '\x00'
        cpu.EIP = 0x805988d
        cpu.ZF = False
        cpu.CX = 0xc703
        cpu.EBP = 0xffffb600
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\xf4')
        self.assertEqual(mem[0xffffb601], '\xc9')
        self.assertEqual(mem[0x805988d], 'f')
        self.assertEqual(mem[0x805988e], '\x0f')
        self.assertEqual(mem[0x805988f], 'F')
        self.assertEqual(mem[0x8059890], 'M')
        self.assertEqual(mem[0x8059891], '\x00')
        self.assertEqual(cpu.EIP, 134584466)
        self.assertEqual(cpu.CX, 50947)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVBE_2(self):
        ''' Instruction CMOVBE_2
            Groups: cmov
            0x8059889:	cmovbe	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08059000, 0x1000, 'rwx')
        mem[0x08059889] = 'f'
        mem[0x0805988a] = '\x0f'
        mem[0x0805988b] = 'F'
        mem[0x0805988c] = '\xca'
        cpu.EIP = 0x8059889
        cpu.ZF = False
        cpu.CX = 0xc703
        cpu.CF = False
        cpu.DX = 0xc8f8
        cpu.execute()

        self.assertEqual(mem[0x8059889], 'f')
        self.assertEqual(mem[0x805988a], '\x0f')
        self.assertEqual(mem[0x805988b], 'F')
        self.assertEqual(mem[0x805988c], '\xca')
        self.assertEqual(cpu.EIP, 134584461)
        self.assertEqual(cpu.CX, 50947)
        self.assertEqual(cpu.DX, 51448)

    def test_CMOVBE_3(self):
        ''' Instruction CMOVBE_3
            Groups: cmov
            0x8059892:	cmovbe	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08059000, 0x1000, 'rwx')
        mem[0x08059892] = '\x0f'
        mem[0x08059893] = 'F'
        mem[0x08059894] = '\xca'
        cpu.EIP = 0x8059892
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xc8f8
        cpu.ECX = 0xffffc703
        cpu.execute()

        self.assertEqual(mem[0x8059892], '\x0f')
        self.assertEqual(mem[0x8059893], 'F')
        self.assertEqual(mem[0x8059894], '\xca')
        self.assertEqual(cpu.EIP, 134584469)
        self.assertEqual(cpu.EDX, 51448)
        self.assertEqual(cpu.ECX, 4294952707)

    def test_CMOVBE_4(self):
        ''' Instruction CMOVBE_4
            Groups: cmov
            0xf7fe6d28:	cmovbe	edx, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe6000, 0x1000, 'rwx')
        mem[0xf7fe6d28] = '\x0f'
        mem[0xf7fe6d29] = 'F'
        mem[0xf7fe6d2a] = '\xd1'
        cpu.EIP = 0xf7fe6d28
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0x4e5
        cpu.ECX = 0x542
        cpu.execute()

        self.assertEqual(mem[0xf7fe6d28], '\x0f')
        self.assertEqual(mem[0xf7fe6d29], 'F')
        self.assertEqual(mem[0xf7fe6d2a], '\xd1')
        self.assertEqual(cpu.EIP, 4160646443)
        self.assertEqual(cpu.EDX, 1253)
        self.assertEqual(cpu.ECX, 1346)

    def test_CMOVBE_5(self):
        ''' Instruction CMOVBE_5
            Groups: cmov
            0xf7fe6d28:	cmovbe	edx, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe6000, 0x1000, 'rwx')
        mem[0xf7fe6d28] = '\x0f'
        mem[0xf7fe6d29] = 'F'
        mem[0xf7fe6d2a] = '\xd1'
        cpu.EIP = 0xf7fe6d28
        cpu.ZF = False
        cpu.CF = False
        cpu.EDX = 0xb
        cpu.ECX = 0xe
        cpu.execute()

        self.assertEqual(mem[0xf7fe6d28], '\x0f')
        self.assertEqual(mem[0xf7fe6d29], 'F')
        self.assertEqual(mem[0xf7fe6d2a], '\xd1')
        self.assertEqual(cpu.EIP, 4160646443)
        self.assertEqual(cpu.EDX, 11)
        self.assertEqual(cpu.ECX, 14)

    def test_CMOVBE_6(self):
        ''' Instruction CMOVBE_6
            Groups: cmov
            0xf7fe0a66:	cmovbe	eax, esi
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe0000, 0x1000, 'rwx')
        mem[0xf7fe0a68] = '\xc6'
        mem[0xf7fe0a66] = '\x0f'
        mem[0xf7fe0a67] = 'F'
        cpu.EIP = 0xf7fe0a66
        cpu.ZF = False
        cpu.CF = False
        cpu.ESI = 0xe
        cpu.EAX = 0xb
        cpu.execute()

        self.assertEqual(mem[0xf7fe0a68], '\xc6')
        self.assertEqual(mem[0xf7fe0a66], '\x0f')
        self.assertEqual(mem[0xf7fe0a67], 'F')
        self.assertEqual(cpu.EIP, 4160621161)
        self.assertEqual(cpu.ESI, 14)
        self.assertEqual(cpu.EAX, 11)

    def test_CMOVBE_7(self):
        ''' Instruction CMOVBE_7
            Groups: cmov
            0x8059895:	cmovbe	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08059000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\xf4'
        mem[0xffffb601] = '\xc9'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08059895] = '\x0f'
        mem[0x08059896] = 'F'
        mem[0x08059897] = 'M'
        mem[0x08059898] = '\x00'
        cpu.EIP = 0x8059895
        cpu.ZF = False
        cpu.EBP = 0xffffb600
        cpu.CF = False
        cpu.ECX = 0xffffc703
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\xf4')
        self.assertEqual(mem[0xffffb601], '\xc9')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8059895], '\x0f')
        self.assertEqual(mem[0x8059896], 'F')
        self.assertEqual(mem[0x8059897], 'M')
        self.assertEqual(mem[0x8059898], '\x00')
        self.assertEqual(cpu.EIP, 134584473)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 4294952707)

    def test_CMOVB_1(self):
        ''' Instruction CMOVB_1
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_10(self):
        ''' Instruction CMOVB_10
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_11(self):
        ''' Instruction CMOVB_11
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = True
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 4294967295)

    def test_CMOVB_12(self):
        ''' Instruction CMOVB_12
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_13(self):
        ''' Instruction CMOVB_13
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x9
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 9)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVB_14(self):
        ''' Instruction CMOVB_14
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_15(self):
        ''' Instruction CMOVB_15
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_16(self):
        ''' Instruction CMOVB_16
            Groups: cmov
            0x804d68f:	cmovb	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0x0804d68f] = 'f'
        mem[0x0804d690] = '\x0f'
        mem[0x0804d691] = 'B'
        mem[0x0804d692] = 'M'
        mem[0x0804d693] = '\x00'
        cpu.EIP = 0x804d68f
        cpu.CX = 0x0
        cpu.EBP = 0xffffb600
        cpu.CF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x804d68f], 'f')
        self.assertEqual(mem[0x804d690], '\x0f')
        self.assertEqual(mem[0x804d691], 'B')
        self.assertEqual(mem[0x804d692], 'M')
        self.assertEqual(mem[0x804d693], '\x00')
        self.assertEqual(cpu.EIP, 134534804)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVB_17(self):
        ''' Instruction CMOVB_17
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0xc
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 12)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVB_18(self):
        ''' Instruction CMOVB_18
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x12
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 18)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVB_19(self):
        ''' Instruction CMOVB_19
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x4
        cpu.CF = True
        cpu.ECX = 0x3
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 4)
        self.assertEqual(cpu.ECX, 4)

    def test_CMOVB_2(self):
        ''' Instruction CMOVB_2
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x1e
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 30)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVB_20(self):
        ''' Instruction CMOVB_20
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_21(self):
        ''' Instruction CMOVB_21
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x2
        cpu.CF = True
        cpu.ECX = 0x1
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 2)
        self.assertEqual(cpu.ECX, 2)

    def test_CMOVB_3(self):
        ''' Instruction CMOVB_3
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = True
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 4294967295)

    def test_CMOVB_4(self):
        ''' Instruction CMOVB_4
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_5(self):
        ''' Instruction CMOVB_5
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x20
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 32)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVB_6(self):
        ''' Instruction CMOVB_6
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x8
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 8)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVB_7(self):
        ''' Instruction CMOVB_7
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_8(self):
        ''' Instruction CMOVB_8
            Groups: cmov
            0xf7ff3e81:	cmovb	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e81] = '\x0f'
        mem[0xf7ff3e82] = 'B'
        mem[0xf7ff3e83] = '\xc1'
        cpu.EIP = 0xf7ff3e81
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e81], '\x0f')
        self.assertEqual(mem[0xf7ff3e82], 'B')
        self.assertEqual(mem[0xf7ff3e83], '\xc1')
        self.assertEqual(cpu.EIP, 4160700036)
        self.assertEqual(cpu.ECX, 4294967295)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVB_9(self):
        ''' Instruction CMOVB_9
            Groups: cmov
            0xf7fec2ce:	cmovb	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fec000, 0x1000, 'rwx')
        mem[0xf7fec2d0] = '\xca'
        mem[0xf7fec2ce] = '\x0f'
        mem[0xf7fec2cf] = 'B'
        cpu.EIP = 0xf7fec2ce
        cpu.EDX = 0x1b
        cpu.CF = False
        cpu.ECX = 0x24
        cpu.execute()

        self.assertEqual(mem[0xf7fec2d0], '\xca')
        self.assertEqual(mem[0xf7fec2ce], '\x0f')
        self.assertEqual(mem[0xf7fec2cf], 'B')
        self.assertEqual(cpu.EIP, 4160668369)
        self.assertEqual(cpu.EDX, 27)
        self.assertEqual(cpu.ECX, 36)

    def test_CMOVE_1(self):
        ''' Instruction CMOVE_1
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_10(self):
        ''' Instruction CMOVE_10
            Groups: cmov
            0x804d62b:	cmove	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d62b] = 'f'
        mem[0x0804d62c] = '\x0f'
        mem[0x0804d62d] = 'D'
        mem[0x0804d62e] = '\xca'
        cpu.EIP = 0x804d62b
        cpu.ZF = True
        cpu.CX = 0x0
        cpu.DX = 0xf0
        cpu.execute()

        self.assertEqual(mem[0x804d62b], 'f')
        self.assertEqual(mem[0x804d62c], '\x0f')
        self.assertEqual(mem[0x804d62d], 'D')
        self.assertEqual(mem[0x804d62e], '\xca')
        self.assertEqual(cpu.EIP, 134534703)
        self.assertEqual(cpu.CX, 240)
        self.assertEqual(cpu.DX, 240)

    def test_CMOVE_11(self):
        ''' Instruction CMOVE_11
            Groups: cmov
            0x804d637:	cmove	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0804d637] = '\x0f'
        mem[0x0804d638] = 'D'
        mem[0x0804d639] = 'M'
        mem[0x0804d63a] = '\x00'
        cpu.EIP = 0x804d637
        cpu.ZF = True
        cpu.EBP = 0xffffb600
        cpu.ECX = 0xf0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x804d637], '\x0f')
        self.assertEqual(mem[0x804d638], 'D')
        self.assertEqual(mem[0x804d639], 'M')
        self.assertEqual(mem[0x804d63a], '\x00')
        self.assertEqual(cpu.EIP, 134534715)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVE_12(self):
        ''' Instruction CMOVE_12
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdabf8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596984)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_13(self):
        ''' Instruction CMOVE_13
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdadb8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160597432)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_14(self):
        ''' Instruction CMOVE_14
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_15(self):
        ''' Instruction CMOVE_15
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdabb8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596920)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_16(self):
        ''' Instruction CMOVE_16
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_17(self):
        ''' Instruction CMOVE_17
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdadf8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160597496)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_18(self):
        ''' Instruction CMOVE_18
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_19(self):
        ''' Instruction CMOVE_19
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdabb8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596920)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_2(self):
        ''' Instruction CMOVE_2
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_20(self):
        ''' Instruction CMOVE_20
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdadf8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160597496)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_21(self):
        ''' Instruction CMOVE_21
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_3(self):
        ''' Instruction CMOVE_3
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_4(self):
        ''' Instruction CMOVE_4
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_5(self):
        ''' Instruction CMOVE_5
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdae38
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160597560)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_6(self):
        ''' Instruction CMOVE_6
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_7(self):
        ''' Instruction CMOVE_7
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdaba8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596904)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_8(self):
        ''' Instruction CMOVE_8
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdabb8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596920)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVE_9(self):
        ''' Instruction CMOVE_9
            Groups: cmov
            0xf7fe72be:	cmove	edx, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe72c0] = '\xd0'
        mem[0xf7fe72be] = '\x0f'
        mem[0xf7fe72bf] = 'D'
        cpu.EIP = 0xf7fe72be
        cpu.ZF = False
        cpu.EDX = 0xf7fdabf8
        cpu.EAX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe72c0], '\xd0')
        self.assertEqual(mem[0xf7fe72be], '\x0f')
        self.assertEqual(mem[0xf7fe72bf], 'D')
        self.assertEqual(cpu.EIP, 4160647873)
        self.assertEqual(cpu.EDX, 4160596984)
        self.assertEqual(cpu.EAX, 0)

    def test_CMOVGE_1(self):
        ''' Instruction CMOVGE_1
            Groups: cmov
            0x8079470:	cmovge	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x08079470] = '\x0f'
        mem[0x08079471] = 'M'
        mem[0x08079472] = '\xca'
        cpu.EIP = 0x8079470
        cpu.EDX = 0x0
        cpu.SF = True
        cpu.OF = False
        cpu.ECX = 0xfe8f0085
        cpu.execute()

        self.assertEqual(mem[0x8079470], '\x0f')
        self.assertEqual(mem[0x8079471], 'M')
        self.assertEqual(mem[0x8079472], '\xca')
        self.assertEqual(cpu.EIP, 134714483)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.ECX, 4270784645)

    def test_CMOVGE_2(self):
        ''' Instruction CMOVGE_2
            Groups: cmov
            0x8079473:	cmovge	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08079474] = 'M'
        mem[0x08079473] = '\x0f'
        mem[0x08079476] = '\x00'
        mem[0x08079475] = 'M'
        cpu.EIP = 0x8079473
        cpu.EBP = 0xffffb600
        cpu.SF = True
        cpu.OF = False
        cpu.ECX = 0xfe8f0085
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8079474], 'M')
        self.assertEqual(mem[0x8079473], '\x0f')
        self.assertEqual(mem[0x8079476], '\x00')
        self.assertEqual(mem[0x8079475], 'M')
        self.assertEqual(cpu.EIP, 134714487)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 4270784645)

    def test_CMOVGE_3(self):
        ''' Instruction CMOVGE_3
            Groups: cmov
            0x807946b:	cmovge	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0x0807946b] = 'f'
        mem[0x0807946c] = '\x0f'
        mem[0x0807946d] = 'M'
        mem[0x0807946e] = 'M'
        mem[0x0807946f] = '\x00'
        cpu.EIP = 0x807946b
        cpu.CX = 0x85
        cpu.EBP = 0xffffb600
        cpu.SF = True
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x807946b], 'f')
        self.assertEqual(mem[0x807946c], '\x0f')
        self.assertEqual(mem[0x807946d], 'M')
        self.assertEqual(mem[0x807946e], 'M')
        self.assertEqual(mem[0x807946f], '\x00')
        self.assertEqual(cpu.EIP, 134714480)
        self.assertEqual(cpu.CX, 133)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVGE_4(self):
        ''' Instruction CMOVGE_4
            Groups: cmov
            0x8079467:	cmovge	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x08079468] = '\x0f'
        mem[0x08079469] = 'M'
        mem[0x0807946a] = '\xca'
        mem[0x08079467] = 'f'
        cpu.EIP = 0x8079467
        cpu.CX = 0x85
        cpu.SF = True
        cpu.DX = 0x0
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0x8079468], '\x0f')
        self.assertEqual(mem[0x8079469], 'M')
        self.assertEqual(mem[0x807946a], '\xca')
        self.assertEqual(mem[0x8079467], 'f')
        self.assertEqual(cpu.EIP, 134714475)
        self.assertEqual(cpu.CX, 133)
        self.assertEqual(cpu.DX, 0)

    def test_CMOVG_1(self):
        ''' Instruction CMOVG_1
            Groups: cmov
            0x804d69b:	cmovg	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d69b] = 'f'
        mem[0x0804d69c] = '\x0f'
        mem[0x0804d69d] = 'O'
        mem[0x0804d69e] = '\xca'
        cpu.EIP = 0x804d69b
        cpu.OF = False
        cpu.ZF = True
        cpu.CX = 0x0
        cpu.DX = 0xffff
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x804d69b], 'f')
        self.assertEqual(mem[0x804d69c], '\x0f')
        self.assertEqual(mem[0x804d69d], 'O')
        self.assertEqual(mem[0x804d69e], '\xca')
        self.assertEqual(cpu.EIP, 134534815)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.DX, 65535)

    def test_CMOVG_2(self):
        ''' Instruction CMOVG_2
            Groups: cmov
            0x804d6a7:	cmovg	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0804d6a7] = '\x0f'
        mem[0x0804d6a8] = 'O'
        mem[0x0804d6a9] = 'M'
        mem[0x0804d6aa] = '\x00'
        cpu.EIP = 0x804d6a7
        cpu.OF = False
        cpu.ZF = True
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x804d6a7], '\x0f')
        self.assertEqual(mem[0x804d6a8], 'O')
        self.assertEqual(mem[0x804d6a9], 'M')
        self.assertEqual(mem[0x804d6aa], '\x00')
        self.assertEqual(cpu.EIP, 134534827)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVG_3(self):
        ''' Instruction CMOVG_3
            Groups: cmov
            0x804d6a4:	cmovg	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d6a4] = '\x0f'
        mem[0x0804d6a5] = 'O'
        mem[0x0804d6a6] = '\xca'
        cpu.EIP = 0x804d6a4
        cpu.OF = False
        cpu.ZF = True
        cpu.EDX = 0xffffffff
        cpu.SF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x804d6a4], '\x0f')
        self.assertEqual(mem[0x804d6a5], 'O')
        self.assertEqual(mem[0x804d6a6], '\xca')
        self.assertEqual(cpu.EIP, 134534823)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVG_4(self):
        ''' Instruction CMOVG_4
            Groups: cmov
            0x804d69f:	cmovg	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0x0804d6a0] = '\x0f'
        mem[0x0804d6a1] = 'O'
        mem[0x0804d6a2] = 'M'
        mem[0x0804d6a3] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb600] = '\x00'
        mem[0x0804d69f] = 'f'
        cpu.EIP = 0x804d69f
        cpu.OF = False
        cpu.ZF = True
        cpu.CX = 0x0
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x804d6a0], '\x0f')
        self.assertEqual(mem[0x804d6a1], 'O')
        self.assertEqual(mem[0x804d6a2], 'M')
        self.assertEqual(mem[0x804d6a3], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0x804d69f], 'f')
        self.assertEqual(cpu.EIP, 134534820)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVLE_1(self):
        ''' Instruction CMOVLE_1
            Groups: cmov
            0x80702ea:	cmovle	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x080702ea] = 'f'
        mem[0x080702eb] = '\x0f'
        mem[0x080702ec] = 'N'
        mem[0x080702ed] = '\xca'
        cpu.EIP = 0x80702ea
        cpu.OF = False
        cpu.ZF = True
        cpu.CX = 0xb600
        cpu.DX = 0xfa
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x80702ea], 'f')
        self.assertEqual(mem[0x80702eb], '\x0f')
        self.assertEqual(mem[0x80702ec], 'N')
        self.assertEqual(mem[0x80702ed], '\xca')
        self.assertEqual(cpu.EIP, 134677230)
        self.assertEqual(cpu.CX, 250)
        self.assertEqual(cpu.DX, 250)

    def test_CMOVLE_2(self):
        ''' Instruction CMOVLE_2
            Groups: cmov
            0x80702f6:	cmovle	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x85'
        mem[0xffffb602] = '\xe1'
        mem[0xffffb603] = '\x01'
        mem[0x080702f6] = '\x0f'
        mem[0x080702f7] = 'N'
        mem[0x080702f8] = 'M'
        mem[0x080702f9] = '\x00'
        cpu.EIP = 0x80702f6
        cpu.OF = False
        cpu.ZF = True
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.ECX = 0xfa
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x85')
        self.assertEqual(mem[0xffffb602], '\xe1')
        self.assertEqual(mem[0xffffb603], '\x01')
        self.assertEqual(mem[0x80702f6], '\x0f')
        self.assertEqual(mem[0x80702f7], 'N')
        self.assertEqual(mem[0x80702f8], 'M')
        self.assertEqual(mem[0x80702f9], '\x00')
        self.assertEqual(cpu.EIP, 134677242)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 31556864)

    def test_CMOVLE_3(self):
        ''' Instruction CMOVLE_3
            Groups: cmov
            0x80702ee:	cmovle	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x85'
        mem[0x080702ee] = 'f'
        mem[0x080702ef] = '\x0f'
        mem[0x080702f0] = 'N'
        mem[0x080702f1] = 'M'
        mem[0x080702f2] = '\x00'
        cpu.EIP = 0x80702ee
        cpu.OF = False
        cpu.ZF = True
        cpu.CX = 0xfa
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x85')
        self.assertEqual(mem[0x80702ee], 'f')
        self.assertEqual(mem[0x80702ef], '\x0f')
        self.assertEqual(mem[0x80702f0], 'N')
        self.assertEqual(mem[0x80702f1], 'M')
        self.assertEqual(mem[0x80702f2], '\x00')
        self.assertEqual(cpu.EIP, 134677235)
        self.assertEqual(cpu.CX, 34048)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVLE_4(self):
        ''' Instruction CMOVLE_4
            Groups: cmov
            0x80702f3:	cmovle	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x080702f3] = '\x0f'
        mem[0x080702f4] = 'N'
        mem[0x080702f5] = '\xca'
        cpu.EIP = 0x80702f3
        cpu.OF = False
        cpu.ZF = True
        cpu.EDX = 0xfa
        cpu.SF = False
        cpu.ECX = 0xffff8500
        cpu.execute()

        self.assertEqual(mem[0x80702f3], '\x0f')
        self.assertEqual(mem[0x80702f4], 'N')
        self.assertEqual(mem[0x80702f5], '\xca')
        self.assertEqual(cpu.EIP, 134677238)
        self.assertEqual(cpu.EDX, 250)
        self.assertEqual(cpu.ECX, 250)

    def test_CMOVL_1(self):
        ''' Instruction CMOVL_1
            Groups: cmov
            0x804d64d:	cmovl	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d650] = '\xca'
        mem[0x0804d64d] = 'f'
        mem[0x0804d64e] = '\x0f'
        mem[0x0804d64f] = 'L'
        cpu.EIP = 0x804d64d
        cpu.CX = 0x0
        cpu.SF = False
        cpu.DX = 0xffff
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0x804d650], '\xca')
        self.assertEqual(mem[0x804d64d], 'f')
        self.assertEqual(mem[0x804d64e], '\x0f')
        self.assertEqual(mem[0x804d64f], 'L')
        self.assertEqual(cpu.EIP, 134534737)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.DX, 65535)

    def test_CMOVL_2(self):
        ''' Instruction CMOVL_2
            Groups: cmov
            0x804d656:	cmovl	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d658] = '\xca'
        mem[0x0804d656] = '\x0f'
        mem[0x0804d657] = 'L'
        cpu.EIP = 0x804d656
        cpu.EDX = 0xffffffff
        cpu.SF = False
        cpu.OF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x804d658], '\xca')
        self.assertEqual(mem[0x804d656], '\x0f')
        self.assertEqual(mem[0x804d657], 'L')
        self.assertEqual(cpu.EIP, 134534745)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVL_3(self):
        ''' Instruction CMOVL_3
            Groups: cmov
            0x804d659:	cmovl	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0804d659] = '\x0f'
        mem[0x0804d65a] = 'L'
        mem[0x0804d65b] = 'M'
        mem[0x0804d65c] = '\x00'
        cpu.EIP = 0x804d659
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.OF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x804d659], '\x0f')
        self.assertEqual(mem[0x804d65a], 'L')
        self.assertEqual(mem[0x804d65b], 'M')
        self.assertEqual(mem[0x804d65c], '\x00')
        self.assertEqual(cpu.EIP, 134534749)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVL_4(self):
        ''' Instruction CMOVL_4
            Groups: cmov
            0x804d651:	cmovl	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0x0804d651] = 'f'
        mem[0x0804d652] = '\x0f'
        mem[0x0804d653] = 'L'
        mem[0x0804d654] = 'M'
        mem[0x0804d655] = '\x00'
        cpu.EIP = 0x804d651
        cpu.CX = 0x0
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x804d651], 'f')
        self.assertEqual(mem[0x804d652], '\x0f')
        self.assertEqual(mem[0x804d653], 'L')
        self.assertEqual(mem[0x804d654], 'M')
        self.assertEqual(mem[0x804d655], '\x00')
        self.assertEqual(cpu.EIP, 134534742)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVNE_1(self):
        ''' Instruction CMOVNE_1
            Groups: cmov
            0xf7fe211a:	cmovne	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe2000, 0x1000, 'rwx')
        mem[0xf7fe211a] = '\x0f'
        mem[0xf7fe211b] = 'E'
        mem[0xf7fe211c] = '\xca'
        cpu.EIP = 0xf7fe211a
        cpu.ZF = False
        cpu.EDX = 0x1
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xf7fe211a], '\x0f')
        self.assertEqual(mem[0xf7fe211b], 'E')
        self.assertEqual(mem[0xf7fe211c], '\xca')
        self.assertEqual(cpu.EIP, 4160626973)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.ECX, 1)

    def test_CMOVNE_10(self):
        ''' Instruction CMOVNE_10
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x4008000
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 67141632)

    def test_CMOVNE_11(self):
        ''' Instruction CMOVNE_11
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x8010
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 32784)

    def test_CMOVNE_12(self):
        ''' Instruction CMOVNE_12
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x20
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 32)

    def test_CMOVNE_13(self):
        ''' Instruction CMOVNE_13
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x1002000
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 16785408)

    def test_CMOVNE_14(self):
        ''' Instruction CMOVNE_14
            Groups: cmov
            0xf7fe686d:	cmovne	ebp, eax
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe6000, 0x1000, 'rwx')
        mem[0xf7fe686d] = '\x0f'
        mem[0xf7fe686e] = 'E'
        mem[0xf7fe686f] = '\xe8'
        cpu.EIP = 0xf7fe686d
        cpu.ZF = False
        cpu.EBP = 0x0
        cpu.EAX = 0x10
        cpu.execute()

        self.assertEqual(mem[0xf7fe686d], '\x0f')
        self.assertEqual(mem[0xf7fe686e], 'E')
        self.assertEqual(mem[0xf7fe686f], '\xe8')
        self.assertEqual(cpu.EIP, 4160645232)
        self.assertEqual(cpu.EBP, 16)
        self.assertEqual(cpu.EAX, 16)

    def test_CMOVNE_15(self):
        ''' Instruction CMOVNE_15
            Groups: cmov
            0xf7fe66d5:	cmovne	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe6000, 0x1000, 'rwx')
        mem[0xf7fe66d5] = '\x0f'
        mem[0xf7fe66d6] = 'E'
        mem[0xf7fe66d7] = '\xc1'
        cpu.EIP = 0xf7fe66d5
        cpu.ZF = False
        cpu.EAX = 0xf7fdaacd
        cpu.ECX = 0xf7fda838
        cpu.execute()

        self.assertEqual(mem[0xf7fe66d5], '\x0f')
        self.assertEqual(mem[0xf7fe66d6], 'E')
        self.assertEqual(mem[0xf7fe66d7], '\xc1')
        self.assertEqual(cpu.EIP, 4160644824)
        self.assertEqual(cpu.ECX, 4160596024)
        self.assertEqual(cpu.EAX, 4160596024)

    def test_CMOVNE_16(self):
        ''' Instruction CMOVNE_16
            Groups: cmov
            0xf7fe66d5:	cmovne	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe6000, 0x1000, 'rwx')
        mem[0xf7fe66d5] = '\x0f'
        mem[0xf7fe66d6] = 'E'
        mem[0xf7fe66d7] = '\xc1'
        cpu.EIP = 0xf7fe66d5
        cpu.ZF = True
        cpu.EAX = 0xf7ffdc24
        cpu.ECX = 0xf7ff5844
        cpu.execute()

        self.assertEqual(mem[0xf7fe66d5], '\x0f')
        self.assertEqual(mem[0xf7fe66d6], 'E')
        self.assertEqual(mem[0xf7fe66d7], '\xc1')
        self.assertEqual(cpu.EIP, 4160644824)
        self.assertEqual(cpu.ECX, 4160706628)
        self.assertEqual(cpu.EAX, 4160740388)

    def test_CMOVNE_17(self):
        ''' Instruction CMOVNE_17
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x40080
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 262272)

    def test_CMOVNE_18(self):
        ''' Instruction CMOVNE_18
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x801
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 2049)

    def test_CMOVNE_19(self):
        ''' Instruction CMOVNE_19
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x4
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 4)

    def test_CMOVNE_2(self):
        ''' Instruction CMOVNE_2
            Groups: cmov
            0x80794b9:	cmovne	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0xffffb601] = '\x03'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x080794b9] = '\x0f'
        mem[0x080794ba] = 'E'
        mem[0x080794bb] = 'M'
        mem[0x080794bc] = '\x00'
        cpu.EIP = 0x80794b9
        cpu.ZF = False
        cpu.EBP = 0xffffb600
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0xffffb601], '\x03')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x80794b9], '\x0f')
        self.assertEqual(mem[0x80794ba], 'E')
        self.assertEqual(mem[0x80794bb], 'M')
        self.assertEqual(mem[0x80794bc], '\x00')
        self.assertEqual(cpu.EIP, 134714557)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 769)

    def test_CMOVNE_20(self):
        ''' Instruction CMOVNE_20
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x2004000
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 33570816)

    def test_CMOVNE_21(self):
        ''' Instruction CMOVNE_21
            Groups: cmov
            0x80794ad:	cmovne	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x080794b0] = '\xca'
        mem[0x080794ad] = 'f'
        mem[0x080794ae] = '\x0f'
        mem[0x080794af] = 'E'
        cpu.EIP = 0x80794ad
        cpu.ZF = False
        cpu.CX = 0x1
        cpu.DX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x80794b0], '\xca')
        self.assertEqual(mem[0x80794ad], 'f')
        self.assertEqual(mem[0x80794ae], '\x0f')
        self.assertEqual(mem[0x80794af], 'E')
        self.assertEqual(cpu.EIP, 134714545)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.DX, 0)

    def test_CMOVNE_3(self):
        ''' Instruction CMOVNE_3
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x10
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 16)

    def test_CMOVNE_4(self):
        ''' Instruction CMOVNE_4
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x40
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 64)

    def test_CMOVNE_5(self):
        ''' Instruction CMOVNE_5
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x1
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 1)

    def test_CMOVNE_6(self):
        ''' Instruction CMOVNE_6
            Groups: cmov
            0xf7fe66d5:	cmovne	eax, ecx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe6000, 0x1000, 'rwx')
        mem[0xf7fe66d5] = '\x0f'
        mem[0xf7fe66d6] = 'E'
        mem[0xf7fe66d7] = '\xc1'
        cpu.EIP = 0xf7fe66d5
        cpu.ZF = True
        cpu.EAX = 0xf7ffde94
        cpu.ECX = 0xf7ff5844
        cpu.execute()

        self.assertEqual(mem[0xf7fe66d5], '\x0f')
        self.assertEqual(mem[0xf7fe66d6], 'E')
        self.assertEqual(mem[0xf7fe66d7], '\xc1')
        self.assertEqual(cpu.EIP, 4160644824)
        self.assertEqual(cpu.ECX, 4160706628)
        self.assertEqual(cpu.EAX, 4160741012)

    def test_CMOVNE_7(self):
        ''' Instruction CMOVNE_7
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x1002
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 4098)

    def test_CMOVNE_8(self):
        ''' Instruction CMOVNE_8
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x8
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 8)

    def test_CMOVNE_9(self):
        ''' Instruction CMOVNE_9
            Groups: cmov
            0xf7fe99a0:	cmovne	eax, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe9000, 0x1000, 'rwx')
        mem[0xf7fe99a0] = '\x0f'
        mem[0xf7fe99a1] = 'E'
        mem[0xf7fe99a2] = '\xc2'
        cpu.EIP = 0xf7fe99a0
        cpu.ZF = True
        cpu.EDX = 0x0
        cpu.EAX = 0x80
        cpu.execute()

        self.assertEqual(mem[0xf7fe99a0], '\x0f')
        self.assertEqual(mem[0xf7fe99a1], 'E')
        self.assertEqual(mem[0xf7fe99a2], '\xc2')
        self.assertEqual(cpu.EIP, 4160657827)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.EAX, 128)

    def test_CMOVNO_1(self):
        ''' Instruction CMOVNO_1
            Groups: cmov
            0x80794e1:	cmovno	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0x080794e1] = 'f'
        mem[0x080794e2] = '\x0f'
        mem[0x080794e3] = 'A'
        mem[0x080794e4] = 'M'
        mem[0x080794e5] = '\x00'
        mem[0xffffb601] = '\x03'
        cpu.EIP = 0x80794e1
        cpu.CX = 0x0
        cpu.EBP = 0xffffb600
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0x80794e1], 'f')
        self.assertEqual(mem[0x80794e2], '\x0f')
        self.assertEqual(mem[0x80794e3], 'A')
        self.assertEqual(mem[0x80794e4], 'M')
        self.assertEqual(mem[0x80794e5], '\x00')
        self.assertEqual(mem[0xffffb601], '\x03')
        self.assertEqual(cpu.EIP, 134714598)
        self.assertEqual(cpu.CX, 769)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVNO_2(self):
        ''' Instruction CMOVNO_2
            Groups: cmov
            0x80794e6:	cmovno	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x080794e8] = '\xca'
        mem[0x080794e6] = '\x0f'
        mem[0x080794e7] = 'A'
        cpu.EIP = 0x80794e6
        cpu.EDX = 0x0
        cpu.OF = False
        cpu.ECX = 0x301
        cpu.execute()

        self.assertEqual(mem[0x80794e8], '\xca')
        self.assertEqual(mem[0x80794e6], '\x0f')
        self.assertEqual(mem[0x80794e7], 'A')
        self.assertEqual(cpu.EIP, 134714601)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVNO_3(self):
        ''' Instruction CMOVNO_3
            Groups: cmov
            0x80794dd:	cmovno	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x080794e0] = '\xca'
        mem[0x080794dd] = 'f'
        mem[0x080794de] = '\x0f'
        mem[0x080794df] = 'A'
        cpu.EIP = 0x80794dd
        cpu.CX = 0x301
        cpu.DX = 0x0
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0x80794e0], '\xca')
        self.assertEqual(mem[0x80794dd], 'f')
        self.assertEqual(mem[0x80794de], '\x0f')
        self.assertEqual(mem[0x80794df], 'A')
        self.assertEqual(cpu.EIP, 134714593)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.DX, 0)

    def test_CMOVNO_4(self):
        ''' Instruction CMOVNO_4
            Groups: cmov
            0x80794e9:	cmovno	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0xffffb601] = '\x03'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x080794e9] = '\x0f'
        mem[0x080794ea] = 'A'
        mem[0x080794eb] = 'M'
        mem[0x080794ec] = '\x00'
        cpu.EIP = 0x80794e9
        cpu.EBP = 0xffffb600
        cpu.OF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0xffffb601], '\x03')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x80794e9], '\x0f')
        self.assertEqual(mem[0x80794ea], 'A')
        self.assertEqual(mem[0x80794eb], 'M')
        self.assertEqual(mem[0x80794ec], '\x00')
        self.assertEqual(cpu.EIP, 134714605)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 769)

    def test_CMOVNP_1(self):
        ''' Instruction CMOVNP_1
            Groups: cmov
            0x80794d1:	cmovnp	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0xffffb601] = '\x03'
        mem[0x080794d1] = 'f'
        mem[0x080794d2] = '\x0f'
        mem[0x080794d3] = 'K'
        mem[0x080794d4] = 'M'
        mem[0x080794d5] = '\x00'
        cpu.EIP = 0x80794d1
        cpu.CX = 0x301
        cpu.PF = True
        cpu.EBP = 0xffffb600
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0xffffb601], '\x03')
        self.assertEqual(mem[0x80794d1], 'f')
        self.assertEqual(mem[0x80794d2], '\x0f')
        self.assertEqual(mem[0x80794d3], 'K')
        self.assertEqual(mem[0x80794d4], 'M')
        self.assertEqual(mem[0x80794d5], '\x00')
        self.assertEqual(cpu.EIP, 134714582)
        self.assertEqual(cpu.CX, 769)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVNP_2(self):
        ''' Instruction CMOVNP_2
            Groups: cmov
            0x80794cd:	cmovnp	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x080794d0] = '\xca'
        mem[0x080794cd] = 'f'
        mem[0x080794ce] = '\x0f'
        mem[0x080794cf] = 'K'
        cpu.EIP = 0x80794cd
        cpu.CX = 0x301
        cpu.PF = True
        cpu.DX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x80794d0], '\xca')
        self.assertEqual(mem[0x80794cd], 'f')
        self.assertEqual(mem[0x80794ce], '\x0f')
        self.assertEqual(mem[0x80794cf], 'K')
        self.assertEqual(cpu.EIP, 134714577)
        self.assertEqual(cpu.CX, 769)
        self.assertEqual(cpu.DX, 0)

    def test_CMOVNP_3(self):
        ''' Instruction CMOVNP_3
            Groups: cmov
            0x80794d6:	cmovnp	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x080794d8] = '\xca'
        mem[0x080794d6] = '\x0f'
        mem[0x080794d7] = 'K'
        cpu.EIP = 0x80794d6
        cpu.EDX = 0x0
        cpu.PF = True
        cpu.ECX = 0x301
        cpu.execute()

        self.assertEqual(mem[0x80794d8], '\xca')
        self.assertEqual(mem[0x80794d6], '\x0f')
        self.assertEqual(mem[0x80794d7], 'K')
        self.assertEqual(cpu.EIP, 134714585)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.ECX, 769)

    def test_CMOVNP_4(self):
        ''' Instruction CMOVNP_4
            Groups: cmov
            0x80794d9:	cmovnp	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0xffffb601] = '\x03'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x080794d9] = '\x0f'
        mem[0x080794da] = 'K'
        mem[0x080794db] = 'M'
        mem[0x080794dc] = '\x00'
        cpu.EIP = 0x80794d9
        cpu.PF = True
        cpu.EBP = 0xffffb600
        cpu.ECX = 0x301
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0xffffb601], '\x03')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x80794d9], '\x0f')
        self.assertEqual(mem[0x80794da], 'K')
        self.assertEqual(mem[0x80794db], 'M')
        self.assertEqual(mem[0x80794dc], '\x00')
        self.assertEqual(cpu.EIP, 134714589)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 769)

    def test_CMOVNS_1(self):
        ''' Instruction CMOVNS_1
            Groups: cmov
            0x80794c1:	cmovns	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0x080794c1] = 'f'
        mem[0x080794c2] = '\x0f'
        mem[0x080794c3] = 'I'
        mem[0x080794c4] = 'M'
        mem[0x080794c5] = '\x00'
        mem[0xffffb601] = '\x03'
        cpu.EIP = 0x80794c1
        cpu.CX = 0x301
        cpu.EBP = 0xffffb600
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0x80794c1], 'f')
        self.assertEqual(mem[0x80794c2], '\x0f')
        self.assertEqual(mem[0x80794c3], 'I')
        self.assertEqual(mem[0x80794c4], 'M')
        self.assertEqual(mem[0x80794c5], '\x00')
        self.assertEqual(mem[0xffffb601], '\x03')
        self.assertEqual(cpu.EIP, 134714566)
        self.assertEqual(cpu.CX, 769)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVNS_2(self):
        ''' Instruction CMOVNS_2
            Groups: cmov
            0x80794c9:	cmovns	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0xffffb601] = '\x03'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x080794c9] = '\x0f'
        mem[0x080794ca] = 'I'
        mem[0x080794cb] = 'M'
        mem[0x080794cc] = '\x00'
        cpu.EIP = 0x80794c9
        cpu.EBP = 0xffffb600
        cpu.SF = True
        cpu.ECX = 0x301
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0xffffb601], '\x03')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x80794c9], '\x0f')
        self.assertEqual(mem[0x80794ca], 'I')
        self.assertEqual(mem[0x80794cb], 'M')
        self.assertEqual(mem[0x80794cc], '\x00')
        self.assertEqual(cpu.EIP, 134714573)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 769)

    def test_CMOVNS_3(self):
        ''' Instruction CMOVNS_3
            Groups: cmov
            0x80794bd:	cmovns	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x080794c0] = '\xca'
        mem[0x080794bd] = 'f'
        mem[0x080794be] = '\x0f'
        mem[0x080794bf] = 'I'
        cpu.EIP = 0x80794bd
        cpu.CX = 0x301
        cpu.SF = True
        cpu.DX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x80794c0], '\xca')
        self.assertEqual(mem[0x80794bd], 'f')
        self.assertEqual(mem[0x80794be], '\x0f')
        self.assertEqual(mem[0x80794bf], 'I')
        self.assertEqual(cpu.EIP, 134714561)
        self.assertEqual(cpu.CX, 769)
        self.assertEqual(cpu.DX, 0)

    def test_CMOVNS_4(self):
        ''' Instruction CMOVNS_4
            Groups: cmov
            0x80794c6:	cmovns	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x080794c8] = '\xca'
        mem[0x080794c6] = '\x0f'
        mem[0x080794c7] = 'I'
        cpu.EIP = 0x80794c6
        cpu.EDX = 0x0
        cpu.SF = True
        cpu.ECX = 0x301
        cpu.execute()

        self.assertEqual(mem[0x80794c8], '\xca')
        self.assertEqual(mem[0x80794c6], '\x0f')
        self.assertEqual(mem[0x80794c7], 'I')
        self.assertEqual(cpu.EIP, 134714569)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.ECX, 769)

    def test_CMOVO_1(self):
        ''' Instruction CMOVO_1
            Groups: cmov
            0x804d677:	cmovo	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0804d677] = '\x0f'
        mem[0x0804d678] = '@'
        mem[0x0804d679] = 'M'
        mem[0x0804d67a] = '\x00'
        cpu.EIP = 0x804d677
        cpu.EBP = 0xffffb600
        cpu.OF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x804d677], '\x0f')
        self.assertEqual(mem[0x804d678], '@')
        self.assertEqual(mem[0x804d679], 'M')
        self.assertEqual(mem[0x804d67a], '\x00')
        self.assertEqual(cpu.EIP, 134534779)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVO_2(self):
        ''' Instruction CMOVO_2
            Groups: cmov
            0x804d674:	cmovo	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d674] = '\x0f'
        mem[0x0804d675] = '@'
        mem[0x0804d676] = '\xca'
        cpu.EIP = 0x804d674
        cpu.EDX = 0xffffffff
        cpu.OF = False
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x804d674], '\x0f')
        self.assertEqual(mem[0x804d675], '@')
        self.assertEqual(mem[0x804d676], '\xca')
        self.assertEqual(cpu.EIP, 134534775)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVO_3(self):
        ''' Instruction CMOVO_3
            Groups: cmov
            0x804d66b:	cmovo	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d66b] = 'f'
        mem[0x0804d66c] = '\x0f'
        mem[0x0804d66d] = '@'
        mem[0x0804d66e] = '\xca'
        cpu.EIP = 0x804d66b
        cpu.CX = 0x0
        cpu.DX = 0xffff
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0x804d66b], 'f')
        self.assertEqual(mem[0x804d66c], '\x0f')
        self.assertEqual(mem[0x804d66d], '@')
        self.assertEqual(mem[0x804d66e], '\xca')
        self.assertEqual(cpu.EIP, 134534767)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.DX, 65535)

    def test_CMOVO_4(self):
        ''' Instruction CMOVO_4
            Groups: cmov
            0x804d66f:	cmovo	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0x0804d66f] = 'f'
        mem[0x0804d670] = '\x0f'
        mem[0x0804d671] = '@'
        mem[0x0804d672] = 'M'
        mem[0x0804d673] = '\x00'
        cpu.EIP = 0x804d66f
        cpu.CX = 0x0
        cpu.EBP = 0xffffb600
        cpu.OF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x804d66f], 'f')
        self.assertEqual(mem[0x804d670], '\x0f')
        self.assertEqual(mem[0x804d671], '@')
        self.assertEqual(mem[0x804d672], 'M')
        self.assertEqual(mem[0x804d673], '\x00')
        self.assertEqual(cpu.EIP, 134534772)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVP_1(self):
        ''' Instruction CMOVP_1
            Groups: cmov
            0x804d63c:	cmovp	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d63c] = 'f'
        mem[0x0804d63d] = '\x0f'
        mem[0x0804d63e] = 'J'
        mem[0x0804d63f] = '\xca'
        cpu.EIP = 0x804d63c
        cpu.CX = 0x0
        cpu.PF = True
        cpu.DX = 0xffff
        cpu.execute()

        self.assertEqual(mem[0x804d63c], 'f')
        self.assertEqual(mem[0x804d63d], '\x0f')
        self.assertEqual(mem[0x804d63e], 'J')
        self.assertEqual(mem[0x804d63f], '\xca')
        self.assertEqual(cpu.EIP, 134534720)
        self.assertEqual(cpu.CX, 65535)
        self.assertEqual(cpu.DX, 65535)

    def test_CMOVP_2(self):
        ''' Instruction CMOVP_2
            Groups: cmov
            0x804d648:	cmovp	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x0804d648] = '\x0f'
        mem[0x0804d649] = 'J'
        mem[0x0804d64a] = 'M'
        mem[0x0804d64b] = '\x00'
        cpu.EIP = 0x804d648
        cpu.PF = True
        cpu.EBP = 0xffffb600
        cpu.ECX = 0xffffffff
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x804d648], '\x0f')
        self.assertEqual(mem[0x804d649], 'J')
        self.assertEqual(mem[0x804d64a], 'M')
        self.assertEqual(mem[0x804d64b], '\x00')
        self.assertEqual(cpu.EIP, 134534732)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 0)

    def test_CMOVP_3(self):
        ''' Instruction CMOVP_3
            Groups: cmov
            0x804d640:	cmovp	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0x0804d640] = 'f'
        mem[0x0804d641] = '\x0f'
        mem[0x0804d642] = 'J'
        mem[0x0804d643] = 'M'
        mem[0x0804d644] = '\x00'
        mem[0xffffb601] = '\x00'
        mem[0xffffb600] = '\x00'
        cpu.EIP = 0x804d640
        cpu.CX = 0xffff
        cpu.PF = True
        cpu.EBP = 0xffffb600
        cpu.execute()

        self.assertEqual(mem[0x804d640], 'f')
        self.assertEqual(mem[0x804d641], '\x0f')
        self.assertEqual(mem[0x804d642], 'J')
        self.assertEqual(mem[0x804d643], 'M')
        self.assertEqual(mem[0x804d644], '\x00')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb600], '\x00')
        self.assertEqual(cpu.EIP, 134534725)
        self.assertEqual(cpu.CX, 0)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVP_4(self):
        ''' Instruction CMOVP_4
            Groups: cmov
            0x804d645:	cmovp	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x0804d000, 0x1000, 'rwx')
        mem[0x0804d645] = '\x0f'
        mem[0x0804d646] = 'J'
        mem[0x0804d647] = '\xca'
        cpu.EIP = 0x804d645
        cpu.EDX = 0xffffffff
        cpu.PF = True
        cpu.ECX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x804d645], '\x0f')
        self.assertEqual(mem[0x804d646], 'J')
        self.assertEqual(mem[0x804d647], '\xca')
        self.assertEqual(cpu.EIP, 134534728)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.ECX, 4294967295)

    def test_CMOVS_1(self):
        ''' Instruction CMOVS_1
            Groups: cmov
            0x8079391:	cmovs	ecx, edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x08079391] = '\x0f'
        mem[0x08079392] = 'H'
        mem[0x08079393] = '\xca'
        cpu.EIP = 0x8079391
        cpu.EDX = 0x0
        cpu.SF = False
        cpu.ECX = 0x1800080
        cpu.execute()

        self.assertEqual(mem[0x8079391], '\x0f')
        self.assertEqual(mem[0x8079392], 'H')
        self.assertEqual(mem[0x8079393], '\xca')
        self.assertEqual(cpu.EIP, 134714260)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.ECX, 25165952)

    def test_CMOVS_2(self):
        ''' Instruction CMOVS_2
            Groups: cmov
            0x8079394:	cmovs	ecx, dword ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0xffffb601] = '\x00'
        mem[0xffffb602] = '\x00'
        mem[0xffffb603] = '\x00'
        mem[0x08079394] = '\x0f'
        mem[0x08079395] = 'H'
        mem[0x08079396] = 'M'
        mem[0x08079397] = '\x00'
        cpu.EIP = 0x8079394
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.ECX = 0x1800080
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0xffffb602], '\x00')
        self.assertEqual(mem[0xffffb603], '\x00')
        self.assertEqual(mem[0x8079394], '\x0f')
        self.assertEqual(mem[0x8079395], 'H')
        self.assertEqual(mem[0x8079396], 'M')
        self.assertEqual(mem[0x8079397], '\x00')
        self.assertEqual(cpu.EIP, 134714264)
        self.assertEqual(cpu.EBP, 4294948352)
        self.assertEqual(cpu.ECX, 25165952)

    def test_CMOVS_3(self):
        ''' Instruction CMOVS_3
            Groups: cmov
            0x807938c:	cmovs	cx, word ptr [ebp]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem.mmap(0xffffb000, 0x1000, 'rwx')
        mem[0xffffb600] = '\x01'
        mem[0xffffb601] = '\x00'
        mem[0x0807938c] = 'f'
        mem[0x0807938d] = '\x0f'
        mem[0x0807938e] = 'H'
        mem[0x0807938f] = 'M'
        mem[0x08079390] = '\x00'
        cpu.EIP = 0x807938c
        cpu.CX = 0x80
        cpu.EBP = 0xffffb600
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffb600], '\x01')
        self.assertEqual(mem[0xffffb601], '\x00')
        self.assertEqual(mem[0x807938c], 'f')
        self.assertEqual(mem[0x807938d], '\x0f')
        self.assertEqual(mem[0x807938e], 'H')
        self.assertEqual(mem[0x807938f], 'M')
        self.assertEqual(mem[0x8079390], '\x00')
        self.assertEqual(cpu.EIP, 134714257)
        self.assertEqual(cpu.CX, 128)
        self.assertEqual(cpu.EBP, 4294948352)

    def test_CMOVS_4(self):
        ''' Instruction CMOVS_4
            Groups: cmov
            0x8079388:	cmovs	cx, dx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x08079388] = 'f'
        mem[0x08079389] = '\x0f'
        mem[0x0807938a] = 'H'
        mem[0x0807938b] = '\xca'
        cpu.EIP = 0x8079388
        cpu.CX = 0x80
        cpu.SF = False
        cpu.DX = 0x0
        cpu.execute()

        self.assertEqual(mem[0x8079388], 'f')
        self.assertEqual(mem[0x8079389], '\x0f')
        self.assertEqual(mem[0x807938a], 'H')
        self.assertEqual(mem[0x807938b], '\xca')
        self.assertEqual(cpu.EIP, 134714252)
        self.assertEqual(cpu.CX, 128)
        self.assertEqual(cpu.DX, 0)

    def test_CMPSB_1(self):
        ''' Instruction CMPSB_1
            Groups:
            0x8056678:	cmpsb	byte ptr [esi], byte ptr es:[edi]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08056000, 0x1000, 'rwx')
        mem.mmap(0x0807e000, 0x2000, 'rwx')
        mem[0x08056678] = '\xa6'
        mem[0x0807e037] = '\xe5'
        mem[0x0807f037] = '\xed'
        cpu.EIP = 0x8056678
        cpu.PF = True
        cpu.AF = False
        cpu.DF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0x807f037
        cpu.CF = False
        cpu.ESI = 0x807e037
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0x8056678], '\xa6')
        self.assertEqual(mem[0x807f037], '\xed')
        self.assertEqual(mem[0x807e037], '\xe5')
        self.assertEqual(cpu.EIP, 134571641)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 134737976)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.ESI, 134733880)
        self.assertEqual(cpu.SF, True)

    def test_CMPSD_1(self):
        ''' Instruction CMPSD_1
            Groups:
            0x805667b:	cmpsd	dword ptr [esi], dword ptr es:[edi]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08056000, 0x1000, 'rwx')
        mem.mmap(0x0807e000, 0x2000, 'rwx')
        mem[0x0807e03b] = '\xe5'
        mem[0x0807f03b] = '\xed'
        mem[0x0807e03a] = '\x1e'
        mem[0x0807e03c] = '\xe5'
        mem[0x0807f03a] = '\x1e'
        mem[0x0805667b] = '\xa7'
        mem[0x0807f03c] = '\xed'
        mem[0x0807f03d] = '\xd1'
        mem[0x0807e03d] = 'Q'
        cpu.EIP = 0x805667b
        cpu.PF = False
        cpu.AF = True
        cpu.DF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0x807f03a
        cpu.CF = True
        cpu.ESI = 0x807e03a
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0x807e03b], '\xe5')
        self.assertEqual(mem[0x807f03a], '\x1e')
        self.assertEqual(mem[0x805667b], '\xa7')
        self.assertEqual(mem[0x807e03a], '\x1e')
        self.assertEqual(mem[0x807f03b], '\xed')
        self.assertEqual(mem[0x807e03c], '\xe5')
        self.assertEqual(mem[0x807e03d], 'Q')
        self.assertEqual(mem[0x807f03d], '\xd1')
        self.assertEqual(mem[0x807f03c], '\xed')
        self.assertEqual(cpu.EIP, 134571644)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 134737982)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.ESI, 134733886)
        self.assertEqual(cpu.SF, False)

    def test_CMPSW_1(self):
        ''' Instruction CMPSW_1
            Groups:
            0x8056679:	cmpsw	word ptr [esi], word ptr es:[edi]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08056000, 0x1000, 'rwx')
        mem.mmap(0x0807e000, 0x2000, 'rwx')
        mem[0x0807e038] = '\xe5'
        mem[0x0807f039] = '\xd1'
        mem[0x08056679] = 'f'
        mem[0x0807f038] = '\xed'
        mem[0x0807e039] = 'Q'
        mem[0x0805667a] = '\xa7'
        cpu.EIP = 0x8056679
        cpu.PF = False
        cpu.AF = True
        cpu.DF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0x807f038
        cpu.CF = True
        cpu.ESI = 0x807e038
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0x807f038], '\xed')
        self.assertEqual(mem[0x807e039], 'Q')
        self.assertEqual(mem[0x8056679], 'f')
        self.assertEqual(mem[0x807e038], '\xe5')
        self.assertEqual(mem[0x807f039], '\xd1')
        self.assertEqual(mem[0x805667a], '\xa7')
        self.assertEqual(cpu.EIP, 134571643)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 134737978)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.ESI, 134733882)
        self.assertEqual(cpu.SF, False)

    def test_CMP_1(self):
        ''' Instruction CMP_1
            Groups:
            0xf7fe0b35:	cmp	edi, 0x23
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe0000, 0x1000, 'rwx')
        mem[0xf7fe0b35] = '\x83'
        mem[0xf7fe0b36] = '\xff'
        mem[0xf7fe0b37] = '#'
        cpu.EIP = 0xf7fe0b35
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.EDI = 0x1
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe0b35], '\x83')
        self.assertEqual(mem[0xf7fe0b36], '\xff')
        self.assertEqual(mem[0xf7fe0b37], '#')
        self.assertEqual(cpu.EIP, 4160621368)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.SF, True)

    def test_CMP_10(self):
        ''' Instruction CMP_10
            Groups:
            0xf7fe4caa:	cmp	word ptr [edi + 0xe], 0
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7e20000, 0x1000, 'rwx')
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4caa] = 'f'
        mem[0xf7fe4cab] = '\x83'
        mem[0xf7fe4cac] = '\x7f'
        mem[0xf7fe4cad] = '\x0e'
        mem[0xf7fe4cae] = '\x00'
        mem[0xf7e20892] = ' '
        mem[0xf7e20893] = '\x00'
        cpu.EIP = 0xf7fe4caa
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.EDI = 0xf7e20884
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe4caa], 'f')
        self.assertEqual(mem[0xf7fe4cab], '\x83')
        self.assertEqual(mem[0xf7fe4cac], '\x7f')
        self.assertEqual(mem[0xf7fe4cad], '\x0e')
        self.assertEqual(mem[0xf7fe4cae], '\x00')
        self.assertEqual(mem[0xf7e20892], ' ')
        self.assertEqual(mem[0xf7e20893], '\x00')
        self.assertEqual(cpu.EIP, 4160638127)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDI, 4158785668)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_CMP_11(self):
        ''' Instruction CMP_11
            Groups:
            0xf7ff41ad:	cmp	ecx, 1
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff4000, 0x1000, 'rwx')
        mem[0xf7ff41ad] = '\x83'
        mem[0xf7ff41ae] = '\xf9'
        mem[0xf7ff41af] = '\x01'
        cpu.EIP = 0xf7ff41ad
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.ECX = 0x14
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7ff41ad], '\x83')
        self.assertEqual(mem[0xf7ff41ae], '\xf9')
        self.assertEqual(mem[0xf7ff41af], '\x01')
        self.assertEqual(cpu.EIP, 4160700848)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 20)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_CMP_12(self):
        ''' Instruction CMP_12
            Groups:
            0xf7ff3e6a:	cmp	al, byte ptr [edx]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fdc000, 0x1000, 'rwx')
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e6a] = ':'
        mem[0xf7ff3e6b] = '\x02'
        mem[0xf7fdc4fe] = '_'
        cpu.SF = False
        cpu.EIP = 0xf7ff3e6a
        cpu.EDX = 0xf7fdc4fe
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.AL = 0x5f
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e6a], ':')
        self.assertEqual(mem[0xf7ff3e6b], '\x02')
        self.assertEqual(mem[0xf7fdc4fe], '_')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.EIP, 4160700012)
        self.assertEqual(cpu.EDX, 4160603390)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.AL, 95)

    def test_CMP_13(self):
        ''' Instruction CMP_13
            Groups:
            0xf7fe71ac:	cmp	byte ptr [esi + 4], 8
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7e2a000, 0x1000, 'rwx')
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7e2af60] = '\x08'
        mem[0xf7fe71ac] = '\x80'
        mem[0xf7fe71ad] = '~'
        mem[0xf7fe71ae] = '\x04'
        mem[0xf7fe71af] = '\x08'
        cpu.EIP = 0xf7fe71ac
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.ESI = 0xf7e2af5c
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7e2af60], '\x08')
        self.assertEqual(mem[0xf7fe71ac], '\x80')
        self.assertEqual(mem[0xf7fe71ad], '~')
        self.assertEqual(mem[0xf7fe71ae], '\x04')
        self.assertEqual(mem[0xf7fe71af], '\x08')
        self.assertEqual(cpu.EIP, 4160647600)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4158828380)
        self.assertEqual(cpu.SF, False)

    def test_CMP_14(self):
        ''' Instruction CMP_14
            Groups:
            0xf7ff3e6a:	cmp	al, byte ptr [edx]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7e28000, 0x1000, 'rwx')
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e6a] = ':'
        mem[0xf7ff3e6b] = '\x02'
        mem[0xf7e28067] = '2'
        cpu.SF = False
        cpu.EIP = 0xf7ff3e6a
        cpu.EDX = 0xf7e28067
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.AL = 0x32
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e6a], ':')
        self.assertEqual(mem[0xf7ff3e6b], '\x02')
        self.assertEqual(mem[0xf7e28067], '2')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.EIP, 4160700012)
        self.assertEqual(cpu.EDX, 4158816359)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.AL, 50)

    def test_CMP_15(self):
        ''' Instruction CMP_15
            Groups:
            0xf7fe71bb:	cmp	ecx, esi
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71bb] = '9'
        mem[0xf7fe71bc] = '\xf1'
        cpu.EIP = 0xf7fe71bb
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.ECX = 0xf7e2c06c
        cpu.CF = False
        cpu.ESI = 0xf7e29f8c
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe71bb], '9')
        self.assertEqual(mem[0xf7fe71bc], '\xf1')
        self.assertEqual(cpu.EIP, 4160647613)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 4158832748)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4158824332)
        self.assertEqual(cpu.SF, False)

    def test_CMP_16(self):
        ''' Instruction CMP_16
            Groups:
            0xf7fe71bb:	cmp	ecx, esi
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71bb] = '9'
        mem[0xf7fe71bc] = '\xf1'
        cpu.EIP = 0xf7fe71bb
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.ECX = 0xf7e2c06c
        cpu.CF = False
        cpu.ESI = 0xf7e29f44
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe71bb], '9')
        self.assertEqual(mem[0xf7fe71bc], '\xf1')
        self.assertEqual(cpu.EIP, 4160647613)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 4158832748)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4158824260)
        self.assertEqual(cpu.SF, False)

    def test_CMP_17(self):
        ''' Instruction CMP_17
            Groups:
            0xf7fe71bb:	cmp	ecx, esi
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71bb] = '9'
        mem[0xf7fe71bc] = '\xf1'
        cpu.EIP = 0xf7fe71bb
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.ECX = 0xf7e2c06c
        cpu.CF = False
        cpu.ESI = 0xf7e2bac4
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe71bb], '9')
        self.assertEqual(mem[0xf7fe71bc], '\xf1')
        self.assertEqual(cpu.EIP, 4160647613)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 4158832748)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4158831300)
        self.assertEqual(cpu.SF, False)

    def test_CMP_18(self):
        ''' Instruction CMP_18
            Groups:
            0xf7fe4fa7:	cmp	dl, 2
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem[0xf7fe4fa8] = '\xfa'
        mem[0xf7fe4fa9] = '\x02'
        mem[0xf7fe4fa7] = '\x80'
        cpu.EIP = 0xf7fe4fa7
        cpu.DL = 0x2
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe4fa8], '\xfa')
        self.assertEqual(mem[0xf7fe4fa9], '\x02')
        self.assertEqual(mem[0xf7fe4fa7], '\x80')
        self.assertEqual(cpu.EIP, 4160638890)
        self.assertEqual(cpu.DL, 2)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_CMP_19(self):
        ''' Instruction CMP_19
            Groups:
            0xf7ff3e6a:	cmp	al, byte ptr [edx]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fda000, 0x1000, 'rwx')
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e6a] = ':'
        mem[0xf7ff3e6b] = '\x02'
        mem[0xf7fdaac5] = 'i'
        cpu.SF = False
        cpu.EIP = 0xf7ff3e6a
        cpu.EDX = 0xf7fdaac5
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.AL = 0x64
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e6a], ':')
        self.assertEqual(mem[0xf7ff3e6b], '\x02')
        self.assertEqual(mem[0xf7fdaac5], 'i')
        self.assertEqual(cpu.SF, True)
        self.assertEqual(cpu.EIP, 4160700012)
        self.assertEqual(cpu.EDX, 4160596677)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.AL, 100)

    def test_CMP_2(self):
        ''' Instruction CMP_2
            Groups:
            0xf7fe71bb:	cmp	ecx, esi
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71bb] = '9'
        mem[0xf7fe71bc] = '\xf1'
        cpu.EIP = 0xf7fe71bb
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.ECX = 0xf7e2c06c
        cpu.CF = False
        cpu.ESI = 0xf7e2b12c
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe71bb], '9')
        self.assertEqual(mem[0xf7fe71bc], '\xf1')
        self.assertEqual(cpu.EIP, 4160647613)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 4158832748)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4158828844)
        self.assertEqual(cpu.SF, False)

    def test_CMP_20(self):
        ''' Instruction CMP_20
            Groups:
            0xf7ff3e6a:	cmp	al, byte ptr [edx]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fdc000, 0x1000, 'rwx')
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3e6a] = ':'
        mem[0xf7ff3e6b] = '\x02'
        mem[0xf7fdc626] = '2'
        cpu.SF = False
        cpu.EIP = 0xf7ff3e6a
        cpu.EDX = 0xf7fdc626
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.AL = 0x32
        cpu.execute()

        self.assertEqual(mem[0xf7ff3e6a], ':')
        self.assertEqual(mem[0xf7ff3e6b], '\x02')
        self.assertEqual(mem[0xf7fdc626], '2')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.EIP, 4160700012)
        self.assertEqual(cpu.EDX, 4160603686)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.AL, 50)

    def test_CMP_21(self):
        ''' Instruction CMP_21
            Groups:
            0xf7fe71bb:	cmp	ecx, esi
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe71bb] = '9'
        mem[0xf7fe71bc] = '\xf1'
        cpu.EIP = 0xf7fe71bb
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.ECX = 0xf7e2c06c
        cpu.CF = False
        cpu.ESI = 0xf7e2b944
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fe71bb], '9')
        self.assertEqual(mem[0xf7fe71bc], '\xf1')
        self.assertEqual(cpu.EIP, 4160647613)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 4158832748)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4158830916)
        self.assertEqual(cpu.SF, False)

    def test_CMP_3(self):
        ''' Instruction CMP_3
            Groups:
            0xf7ff0681:	cmp	cl, dl
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff0000, 0x1000, 'rwx')
        mem[0xf7ff0681] = '8'
        mem[0xf7ff0682] = '\xd1'
        cpu.EIP = 0xf7ff0681
        cpu.DL = 0x62
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.CL = 0x62
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7ff0681], '8')
        self.assertEqual(mem[0xf7ff0682], '\xd1')
        self.assertEqual(cpu.EIP, 4160685699)
        self.assertEqual(cpu.DL, 98)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CL, 98)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_CMP_4(self):
        ''' Instruction CMP_4
            Groups:
            0xf7fe4ea2:	cmp	esi, dword ptr [esp + 0xac]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe4000, 0x1000, 'rwx')
        mem.mmap(0xffffd000, 0x1000, 'rwx')
        mem[0xffffd39c] = '\x00'
        mem[0xffffd39d] = '\x00'
        mem[0xffffd39e] = '\x00'
        mem[0xffffd39f] = '\x00'
        mem[0xf7fe4ea2] = ';'
        mem[0xf7fe4ea3] = '\xb4'
        mem[0xf7fe4ea4] = '$'
        mem[0xf7fe4ea5] = '\xac'
        mem[0xf7fe4ea6] = '\x00'
        mem[0xf7fe4ea7] = '\x00'
        mem[0xf7fe4ea8] = '\x00'
        cpu.EIP = 0xf7fe4ea2
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.ESP = 0xffffd2f0
        cpu.CF = False
        cpu.ESI = 0xf7fda858
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xffffd39c], '\x00')
        self.assertEqual(mem[0xffffd39d], '\x00')
        self.assertEqual(mem[0xffffd39e], '\x00')
        self.assertEqual(mem[0xffffd39f], '\x00')
        self.assertEqual(mem[0xf7fe4ea2], ';')
        self.assertEqual(mem[0xf7fe4ea3], '\xb4')
        self.assertEqual(mem[0xf7fe4ea4], '$')
        self.assertEqual(mem[0xf7fe4ea5], '\xac')
        self.assertEqual(mem[0xf7fe4ea6], '\x00')
        self.assertEqual(mem[0xf7fe4ea7], '\x00')
        self.assertEqual(mem[0xf7fe4ea8], '\x00')
        self.assertEqual(cpu.EIP, 4160638633)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ESP, 4294955760)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.ESI, 4160596056)
        self.assertEqual(cpu.SF, True)

    def test_CMP_5(self):
        ''' Instruction CMP_5
            Groups:
            0xf7ff3e6a:	cmp	al, byte ptr [edx]
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7e28000, 0x1000, 'rwx')
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7e28099] = 'G'
        mem[0xf7ff3e6a] = ':'
        mem[0xf7ff3e6b] = '\x02'
        cpu.SF = False
        cpu.EIP = 0xf7ff3e6a
        cpu.EDX = 0xf7e28099
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.AL = 0x47
        cpu.execute()

        self.assertEqual(mem[0xf7e28099], 'G')
        self.assertEqual(mem[0xf7ff3e6a], ':')
        self.assertEqual(mem[0xf7ff3e6b], '\x02')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.EIP, 4160700012)
        self.assertEqual(cpu.EDX, 4158816409)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.AL, 71)

    def test_CMP_6(self):
        ''' Instruction CMP_6
            Groups:
            0xf7ff0681:	cmp	cl, dl
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff0000, 0x1000, 'rwx')
        mem[0xf7ff0681] = '8'
        mem[0xf7ff0682] = '\xd1'
        cpu.EIP = 0xf7ff0681
        cpu.DL = 0x63
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.CL = 0x63
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7ff0681], '8')
        self.assertEqual(mem[0xf7ff0682], '\xd1')
        self.assertEqual(cpu.EIP, 4160685699)
        self.assertEqual(cpu.DL, 99)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CL, 99)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_CMP_7(self):
        ''' Instruction CMP_7
            Groups:
            0xf7fe7f28:	cmp	eax, 2
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe7000, 0x1000, 'rwx')
        mem[0xf7fe7f28] = '\x83'
        mem[0xf7fe7f29] = '\xf8'
        mem[0xf7fe7f2a] = '\x02'
        cpu.EIP = 0xf7fe7f28
        cpu.EAX = 0xffffffde
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe7f28], '\x83')
        self.assertEqual(mem[0xf7fe7f29], '\xf8')
        self.assertEqual(mem[0xf7fe7f2a], '\x02')
        self.assertEqual(cpu.EIP, 4160651051)
        self.assertEqual(cpu.EAX, 4294967262)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, True)

    def test_CMP_8(self):
        ''' Instruction CMP_8
            Groups:
            0xf7fe579d:	cmp	dl, 3
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fe5000, 0x1000, 'rwx')
        mem[0xf7fe579d] = '\x80'
        mem[0xf7fe579e] = '\xfa'
        mem[0xf7fe579f] = '\x03'
        cpu.EIP = 0xf7fe579d
        cpu.DL = 0x0
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7fe579d], '\x80')
        self.assertEqual(mem[0xf7fe579e], '\xfa')
        self.assertEqual(mem[0xf7fe579f], '\x03')
        self.assertEqual(cpu.EIP, 4160640928)
        self.assertEqual(cpu.DL, 0)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.SF, True)

    def test_CMP_9(self):
        ''' Instruction CMP_9
            Groups:
            0xf7fe0abc:	cmp	byte ptr [eax + 4], 8
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7fdc000, 0x1000, 'rwx')
        mem.mmap(0xf7fe0000, 0x1000, 'rwx')
        mem[0xf7fdc780] = '\x08'
        mem[0xf7fe0abc] = '\x80'
        mem[0xf7fe0abd] = 'x'
        mem[0xf7fe0abe] = '\x04'
        mem[0xf7fe0abf] = '\x08'
        cpu.EIP = 0xf7fe0abc
        cpu.EAX = 0xf7fdc77c
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7fdc780], '\x08')
        self.assertEqual(mem[0xf7fe0abc], '\x80')
        self.assertEqual(mem[0xf7fe0abd], 'x')
        self.assertEqual(mem[0xf7fe0abe], '\x04')
        self.assertEqual(mem[0xf7fe0abf], '\x08')
        self.assertEqual(cpu.EIP, 4160621248)
        self.assertEqual(cpu.EAX, 4160604028)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.SF, False)

    def test_CWDE_1(self):
        ''' Instruction CWDE_1
            Groups:
            0x807934a:	cwde
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08079000, 0x1000, 'rwx')
        mem[0x0807934a] = '\x98'
        cpu.EIP = 0x807934a
        cpu.EAX = 0x137
        cpu.execute()

        self.assertEqual(mem[0x807934a], '\x98')
        self.assertEqual(cpu.EIP, 134714187)
        self.assertEqual(cpu.EAX, 311)

    def test_CWDE_2(self):
        ''' Instruction CWDE_2
            Groups:
            0x807028c:	cwde
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08070000, 0x1000, 'rwx')
        mem[0x0807028c] = '\x98'
        cpu.EIP = 0x807028c
        cpu.EAX = 0xb594ecf8
        cpu.execute()

        self.assertEqual(mem[0x807028c], '\x98')
        self.assertEqual(cpu.EIP, 134677133)
        self.assertEqual(cpu.EAX, 4294962424)

    def test_DEC_1(self):
        ''' Instruction DEC_1
            Groups: not64bitmode
            0xf7ff3ee8:	dec	edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3ee8] = 'J'
        cpu.EIP = 0xf7ff3ee8
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.PF = True
        cpu.EDX = 0xa0ffc9d2
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7ff3ee8], 'J')
        self.assertEqual(cpu.EIP, 4160700137)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 2701117905)
        self.assertEqual(cpu.SF, True)

    def test_DEC_10(self):
        ''' Instruction DEC_10
            Groups: not64bitmode
            0xf7ff3ee8:	dec	edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3ee8] = 'J'
        cpu.EIP = 0xf7ff3ee8
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.PF = True
        cpu.EDX = 0xc7cc96d1
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7ff3ee8], 'J')
        self.assertEqual(cpu.EIP, 4160700137)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.EDX, 3352073936)
        self.assertEqual(cpu.SF, True)

    def test_DEC_11(self):
        ''' Instruction DEC_11
            Groups: not64bitmode
            0xf7ff3f1c:	dec	edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3f1c] = 'J'
        cpu.EIP = 0xf7ff3f1c
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.PF = False
        cpu.EDX = 0x8a9198d3
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7ff3f1c], 'J')
        self.assertEqual(cpu.EIP, 4160700189)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 2324797650)
        self.assertEqual(cpu.SF, True)

    def test_DEC_12(self):
        ''' Instruction DEC_12
            Groups: not64bitmode
            0x8059862:	dec	cx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0x08059000, 0x1000, 'rwx')
        mem[0x08059862] = 'f'
        mem[0x08059863] = 'I'
        cpu.EIP = 0x8059862
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.CX = 0xff
        cpu.PF = True
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0x8059862], 'f')
        self.assertEqual(mem[0x8059863], 'I')
        self.assertEqual(cpu.EIP, 134584420)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CX, 254)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)

    def test_DEC_13(self):
        ''' Instruction DEC_13
            Groups: not64bitmode
            0xf7ff3ee8:	dec	edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3ee8] = 'J'
        cpu.EIP = 0xf7ff3ee8
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.PF = True
        cpu.EDX = 0xffffff99
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7ff3ee8], 'J')
        self.assertEqual(cpu.EIP, 4160700137)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.EDX, 4294967192)
        self.assertEqual(cpu.SF, True)

    def test_DEC_14(self):
        ''' Instruction DEC_14
            Groups: not64bitmode
            0xf7ff3ee8:	dec	edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3ee8] = 'J'
        cpu.EIP = 0xf7ff3ee8
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.PF = True
        cpu.EDX = 0x0
        cpu.SF = True
        cpu.execute()

        self.assertEqual(mem[0xf7ff3ee8], 'J')
        self.assertEqual(cpu.EIP, 4160700137)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 4294967295)
        self.assertEqual(cpu.SF, True)

    def test_DEC_15(self):
        ''' Instruction DEC_15
            Groups: not64bitmode
            0xf7ff3ee8:	dec	edx
        '''
        mem = Memory32()
        cpu = I386Cpu(mem)
        mem.mmap(0xf7ff3000, 0x1000, 'rwx')
        mem[0xf7ff3ee8] = 'J'
        cpu.EIP = 0xf7ff3ee8
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.PF = False
        cpu.EDX = 0x908cd19d
        cpu.SF = False
        cpu.execute()

        self.assertEqual(mem[0xf7ff3ee8], 'J')
        self.assertEqual(cpu.EIP, 4160700137)
        self.assertEqual(cpu.AF, False)
