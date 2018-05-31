from builtins import *
import unittest
from manticore.core.cpu.x86 import *
from manticore.core.smtlib import *
from manticore.core.memory import *

class CPUTest(unittest.TestCase):
    _multiprocess_can_split_ = True
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



    def test_ADD_1(self):
        ''' Instruction ADD_1
            Groups:
            0x7ffff7de438b:	add	rcx, 1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de438b] = 'H'
        mem[0x7ffff7de438c] = '\x83'
        mem[0x7ffff7de438d] = '\xc1'
        mem[0x7ffff7de438e] = '\x01'
        cpu.PF = True
        cpu.RCX = 0x7ffff7ba0aba
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de438b
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de438b], b'H')
        self.assertEqual(mem[0x7ffff7de438c], b'\x83')
        self.assertEqual(mem[0x7ffff7de438d], b'\xc1')
        self.assertEqual(mem[0x7ffff7de438e], b'\x01')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RCX, 140737349552827)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926671)
        self.assertEqual(cpu.SF, False)

    def test_ADD_2(self):
        ''' Instruction ADD_2
            Groups:
            0x7ffff7de4396:	add	rax, rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4398] = '\xd0'
        mem[0x7ffff7de4396] = 'H'
        mem[0x7ffff7de4397] = '\x01'
        cpu.SF = False
        cpu.PF = True
        cpu.RAX = 0x310ef63c39
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4396
        cpu.RDX = 0x65
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4398], b'\xd0')
        self.assertEqual(mem[0x7ffff7de4396], b'H')
        self.assertEqual(mem[0x7ffff7de4397], b'\x01')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.RAX, 210704415902)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926681)
        self.assertEqual(cpu.RDX, 101)

    def test_ADD_3(self):
        ''' Instruction ADD_3
            Groups:
            0x7ffff7de6128:	add	rdx, 0x18
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6128] = 'H'
        mem[0x7ffff7de6129] = '\x83'
        mem[0x7ffff7de612a] = '\xc2'
        mem[0x7ffff7de612b] = '\x18'
        cpu.SF = False
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6128
        cpu.RDX = 0x7ffff7a4c978
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6128], b'H')
        self.assertEqual(mem[0x7ffff7de6129], b'\x83')
        self.assertEqual(mem[0x7ffff7de612a], b'\xc2')
        self.assertEqual(mem[0x7ffff7de612b], b'\x18')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351934252)
        self.assertEqual(cpu.RDX, 140737348159888)

    def test_ADD_4(self):
        ''' Instruction ADD_4
            Groups:
            0x7ffff7de3960:	add	r12, 1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3960] = 'I'
        mem[0x7ffff7de3961] = '\x83'
        mem[0x7ffff7de3962] = '\xc4'
        mem[0x7ffff7de3963] = '\x01'
        cpu.PF = True
        cpu.R12 = 0x0
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3960
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3960], b'I')
        self.assertEqual(mem[0x7ffff7de3961], b'\x83')
        self.assertEqual(mem[0x7ffff7de3962], b'\xc4')
        self.assertEqual(mem[0x7ffff7de3963], b'\x01')
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.R12, 1)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351924068)
        self.assertEqual(cpu.SF, False)

    def test_ADD_5(self):
        ''' Instruction ADD_5
            Groups:
            0x7ffff7de6124:	add	rax, qword ptr [rdx + 0x10]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a49000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7a490d0] = '%'
        mem[0x7ffff7a490d1] = '['
        mem[0x7ffff7a490d2] = '\x17'
        mem[0x7ffff7a490d3] = '\x00'
        mem[0x7ffff7a490d4] = '\x00'
        mem[0x7ffff7a490d5] = '\x00'
        mem[0x7ffff7a490d6] = '\x00'
        mem[0x7ffff7a490d7] = '\x00'
        mem[0x7ffff7de6124] = 'H'
        mem[0x7ffff7de6125] = '\x03'
        mem[0x7ffff7de6126] = 'B'
        mem[0x7ffff7de6127] = '\x10'
        cpu.SF = False
        cpu.PF = True
        cpu.RAX = 0x7ffff7a2e000
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6124
        cpu.RDX = 0x7ffff7a490c0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a490d0], b'%')
        self.assertEqual(mem[0x7ffff7a490d1], b'[')
        self.assertEqual(mem[0x7ffff7a490d2], b'\x17')
        self.assertEqual(mem[0x7ffff7a490d3], b'\x00')
        self.assertEqual(mem[0x7ffff7a490d4], b'\x00')
        self.assertEqual(mem[0x7ffff7a490d5], b'\x00')
        self.assertEqual(mem[0x7ffff7a490d6], b'\x00')
        self.assertEqual(mem[0x7ffff7a490d7], b'\x00')
        self.assertEqual(mem[0x7ffff7de6124], b'H')
        self.assertEqual(mem[0x7ffff7de6125], b'\x03')
        self.assertEqual(mem[0x7ffff7de6126], b'B')
        self.assertEqual(mem[0x7ffff7de6127], b'\x10')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.RAX, 140737349565221)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351934248)
        self.assertEqual(cpu.RDX, 140737348145344)

    def test_ADD_6(self):
        ''' Instruction ADD_6
            Groups:
            0x7ffff7de6124:	add	rax, qword ptr [rdx + 0x10]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4b000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7a4bcc8] = '\xc0'
        mem[0x7ffff7a4bcc9] = '\x88'
        mem[0x7ffff7a4bcca] = '\x07'
        mem[0x7ffff7a4bccb] = '\x00'
        mem[0x7ffff7a4bccc] = '\x00'
        mem[0x7ffff7a4bccd] = '\x00'
        mem[0x7ffff7a4bcce] = '\x00'
        mem[0x7ffff7a4bccf] = '\x00'
        mem[0x7ffff7de6124] = 'H'
        mem[0x7ffff7de6125] = '\x03'
        mem[0x7ffff7de6126] = 'B'
        mem[0x7ffff7de6127] = '\x10'
        cpu.SF = False
        cpu.PF = True
        cpu.RAX = 0x7ffff7a2e000
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6124
        cpu.RDX = 0x7ffff7a4bcb8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4bcc8], b'\xc0')
        self.assertEqual(mem[0x7ffff7a4bcc9], b'\x88')
        self.assertEqual(mem[0x7ffff7a4bcca], b'\x07')
        self.assertEqual(mem[0x7ffff7a4bccb], b'\x00')
        self.assertEqual(mem[0x7ffff7a4bccc], b'\x00')
        self.assertEqual(mem[0x7ffff7a4bccd], b'\x00')
        self.assertEqual(mem[0x7ffff7a4bcce], b'\x00')
        self.assertEqual(mem[0x7ffff7a4bccf], b'\x00')
        self.assertEqual(mem[0x7ffff7de6124], b'H')
        self.assertEqual(mem[0x7ffff7de6125], b'\x03')
        self.assertEqual(mem[0x7ffff7de6126], b'B')
        self.assertEqual(mem[0x7ffff7de6127], b'\x10')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 140737348528320)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351934248)
        self.assertEqual(cpu.RDX, 140737348156600)

    def test_AND_1(self):
        ''' Instruction AND_1
            Groups:
            0x7ffff7b58f2f:	and	r9d, 0xf
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f30] = '\x83'
        mem[0x7ffff7b58f31] = '\xe1'
        mem[0x7ffff7b58f32] = '\x0f'
        mem[0x7ffff7b58f2f] = 'A'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7b58f2f
        cpu.SF = False
        cpu.PF = False
        cpu.R9D = 0x12
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f30], b'\x83')
        self.assertEqual(mem[0x7ffff7b58f31], b'\xe1')
        self.assertEqual(mem[0x7ffff7b58f32], b'\x0f')
        self.assertEqual(mem[0x7ffff7b58f2f], b'A')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737349259059)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.R9D, 2)
        self.assertEqual(cpu.SF, False)

    def test_AND_2(self):
        ''' Instruction AND_2
            Groups:
            0x7ffff7aa7bd0:	and	edx, 0x808
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa7000, 0x1000, 'rwx')
        mem[0x7ffff7aa7bd0] = '\x81'
        mem[0x7ffff7aa7bd1] = '\xe2'
        mem[0x7ffff7aa7bd2] = '\x08'
        mem[0x7ffff7aa7bd3] = '\x08'
        mem[0x7ffff7aa7bd4] = '\x00'
        mem[0x7ffff7aa7bd5] = '\x00'
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7aa7bd0
        cpu.PF = True
        cpu.EDX = 0xfbad2807
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7aa7bd0], b'\x81')
        self.assertEqual(mem[0x7ffff7aa7bd1], b'\xe2')
        self.assertEqual(mem[0x7ffff7aa7bd2], b'\x08')
        self.assertEqual(mem[0x7ffff7aa7bd3], b'\x08')
        self.assertEqual(mem[0x7ffff7aa7bd4], b'\x00')
        self.assertEqual(mem[0x7ffff7aa7bd5], b'\x00')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737348533206)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 2048)
        self.assertEqual(cpu.SF, False)

    def test_AND_3(self):
        ''' Instruction AND_3
            Groups:
            0x7ffff7b58f2f:	and	r9d, 0xf
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f30] = '\x83'
        mem[0x7ffff7b58f31] = '\xe1'
        mem[0x7ffff7b58f32] = '\x0f'
        mem[0x7ffff7b58f2f] = 'A'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7b58f2f
        cpu.SF = False
        cpu.PF = False
        cpu.R9D = 0x12
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f30], b'\x83')
        self.assertEqual(mem[0x7ffff7b58f31], b'\xe1')
        self.assertEqual(mem[0x7ffff7b58f32], b'\x0f')
        self.assertEqual(mem[0x7ffff7b58f2f], b'A')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737349259059)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.R9D, 2)
        self.assertEqual(cpu.SF, False)

    def test_AND_4(self):
        ''' Instruction AND_4
            Groups:
            0x7ffff7de3930:	and	rax, rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3930] = 'H'
        mem[0x7ffff7de3931] = '!'
        mem[0x7ffff7de3932] = '\xf0'
        cpu.PF = True
        cpu.RSI = 0x13
        cpu.OF = False
        cpu.ZF = False
        cpu.RAX = 0x9
        cpu.CF = True
        cpu.RIP = 0x7ffff7de3930
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3930], b'H')
        self.assertEqual(mem[0x7ffff7de3931], b'!')
        self.assertEqual(mem[0x7ffff7de3932], b'\xf0')
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.RSI, 19)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RAX, 1)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351924019)
        self.assertEqual(cpu.SF, False)

    def test_AND_5(self):
        ''' Instruction AND_5
            Groups:
            0x7ffff7b58f2f:	and	r9d, 0xf
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f30] = '\x83'
        mem[0x7ffff7b58f31] = '\xe1'
        mem[0x7ffff7b58f32] = '\x0f'
        mem[0x7ffff7b58f2f] = 'A'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7b58f2f
        cpu.SF = False
        cpu.PF = False
        cpu.R9D = 0x12
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f30], b'\x83')
        self.assertEqual(mem[0x7ffff7b58f31], b'\xe1')
        self.assertEqual(mem[0x7ffff7b58f32], b'\x0f')
        self.assertEqual(mem[0x7ffff7b58f2f], b'A')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737349259059)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.R9D, 2)
        self.assertEqual(cpu.SF, False)

    def test_AND_6(self):
        ''' Instruction AND_6
            Groups:
            0x7ffff7de3909:	and	ecx, dword ptr [rbx + 0x2f0]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ff7000, 0x1000, 'rwx')
        mem[0x7ffff7de390b] = '\xf0'
        mem[0x7ffff7ff794a] = '\x00'
        mem[0x7ffff7ff7949] = '\x00'
        mem[0x7ffff7ff7948] = '\xff'
        mem[0x7ffff7de3909] = '#'
        mem[0x7ffff7de390a] = '\x8b'
        mem[0x7ffff7ff794b] = '\x00'
        mem[0x7ffff7de390c] = '\x02'
        mem[0x7ffff7de390d] = '\x00'
        mem[0x7ffff7de390e] = '\x00'
        cpu.PF = True
        cpu.RBX = 0x7ffff7ff7658
        cpu.OF = False
        cpu.ZF = False
        cpu.ECX = 0x1c5e843
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3909
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ff794b], b'\x00')
        self.assertEqual(mem[0x7ffff7ff794a], b'\x00')
        self.assertEqual(mem[0x7ffff7ff7949], b'\x00')
        self.assertEqual(mem[0x7ffff7ff7948], b'\xff')
        self.assertEqual(mem[0x7ffff7de3909], b'#')
        self.assertEqual(mem[0x7ffff7de390a], b'\x8b')
        self.assertEqual(mem[0x7ffff7de390b], b'\xf0')
        self.assertEqual(mem[0x7ffff7de390c], b'\x02')
        self.assertEqual(mem[0x7ffff7de390d], b'\x00')
        self.assertEqual(mem[0x7ffff7de390e], b'\x00')
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.RBX, 140737354102360)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ECX, 67)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351923983)
        self.assertEqual(cpu.SF, False)

    def test_BSF_1(self):
        ''' Instruction BSF_1
            Groups:
            0x4184cd:	bsf	eax, edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004184cd] = '\x0f'
        mem[0x004184ce] = '\xbc'
        mem[0x004184cf] = '\xc2'
        cpu.EAX = 0x495045
        cpu.ZF = False
        cpu.EDX = 0x80
        cpu.RIP = 0x4184cd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4184cd], b'\x0f')
        self.assertEqual(mem[0x4184ce], b'\xbc')
        self.assertEqual(mem[0x4184cf], b'\xc2')
        self.assertEqual(cpu.EAX, 7)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDX, 128)
        self.assertEqual(cpu.RIP, 4293840)

    def test_BSF_2(self):
        ''' Instruction BSF_2
            Groups:
            0x4183ed:	bsf	eax, edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004183ed] = '\x0f'
        mem[0x004183ee] = '\xbc'
        mem[0x004183ef] = '\xc2'
        cpu.EAX = 0x4a5301
        cpu.ZF = False
        cpu.EDX = 0x5
        cpu.RIP = 0x4183ed
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4183ed], b'\x0f')
        self.assertEqual(mem[0x4183ee], b'\xbc')
        self.assertEqual(mem[0x4183ef], b'\xc2')
        self.assertEqual(cpu.EAX, 0)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDX, 5)
        self.assertEqual(cpu.RIP, 4293616)

    def test_BSF_3(self):
        ''' Instruction BSF_3
            Groups:
            0x4184bd:	bsf	eax, edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004184bd] = '\x0f'
        mem[0x004184be] = '\xbc'
        mem[0x004184bf] = '\xc2'
        cpu.EAX = 0x495085
        cpu.ZF = False
        cpu.EDX = 0x80
        cpu.RIP = 0x4184bd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4184bd], b'\x0f')
        self.assertEqual(mem[0x4184be], b'\xbc')
        self.assertEqual(mem[0x4184bf], b'\xc2')
        self.assertEqual(cpu.EAX, 7)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDX, 128)
        self.assertEqual(cpu.RIP, 4293824)

    def test_BSF_4(self):
        ''' Instruction BSF_4
            Groups:
            0x41850a:	bsf	rax, rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x0041850a] = 'H'
        mem[0x0041850b] = '\x0f'
        mem[0x0041850c] = '\xbc'
        mem[0x0041850d] = '\xc2'
        cpu.ZF = False
        cpu.RIP = 0x41850a
        cpu.RAX = 0x495100
        cpu.RDX = 0x800200020000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41850a], b'H')
        self.assertEqual(mem[0x41850b], b'\x0f')
        self.assertEqual(mem[0x41850c], b'\xbc')
        self.assertEqual(mem[0x41850d], b'\xc2')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RAX, 17)
        self.assertEqual(cpu.RIP, 4293902)
        self.assertEqual(cpu.RDX, 140746078420992)

    def test_BSF_5(self):
        ''' Instruction BSF_5
            Groups:
            0x7ffff7ab5d0a:	bsf	rax, rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab5000, 0x1000, 'rwx')
        mem[0x7ffff7ab5d0a] = 'H'
        mem[0x7ffff7ab5d0b] = '\x0f'
        mem[0x7ffff7ab5d0c] = '\xbc'
        mem[0x7ffff7ab5d0d] = '\xc2'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7ab5d0a
        cpu.RAX = 0x5555555549c0
        cpu.RDX = 0xe0e0e0e0ee080000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab5d0a], b'H')
        self.assertEqual(mem[0x7ffff7ab5d0b], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab5d0c], b'\xbc')
        self.assertEqual(mem[0x7ffff7ab5d0d], b'\xc2')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RAX, 19)
        self.assertEqual(cpu.RIP, 140737348590862)
        self.assertEqual(cpu.RDX, 16204198715949842432)

    def test_BSF_6(self):
        ''' Instruction BSF_6
            Groups:
            0x4183ed:	bsf	eax, edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004183ed] = '\x0f'
        mem[0x004183ee] = '\xbc'
        mem[0x004183ef] = '\xc2'
        cpu.EAX = 0x494d05
        cpu.ZF = False
        cpu.EDX = 0x80
        cpu.RIP = 0x4183ed
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4183ed], b'\x0f')
        self.assertEqual(mem[0x4183ee], b'\xbc')
        self.assertEqual(mem[0x4183ef], b'\xc2')
        self.assertEqual(cpu.EAX, 7)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.EDX, 128)
        self.assertEqual(cpu.RIP, 4293616)

    def test_BSR_1(self):
        ''' Instruction BSR_1
            Groups:
            0x4008b7:	bsr	esi, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x004008b8] = '\xbd'
        mem[0x004008b9] = '\xf6'
        mem[0x004008b7] = '\x0f'
        cpu.ZF = True
        cpu.RIP = 0x4008b7
        cpu.ESI = 0xf
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4008b8], b'\xbd')
        self.assertEqual(mem[0x4008b9], b'\xf6')
        self.assertEqual(mem[0x4008b7], b'\x0f')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ESI, 3)
        self.assertEqual(cpu.RIP, 4196538)

    def test_BSR_2(self):
        ''' Instruction BSR_2
            Groups:
            0x400907:	bsr	esi, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400908] = '\xbd'
        mem[0x00400909] = '\xf6'
        mem[0x00400907] = '\x0f'
        cpu.ZF = True
        cpu.RIP = 0x400907
        cpu.ESI = 0xf
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400908], b'\xbd')
        self.assertEqual(mem[0x400909], b'\xf6')
        self.assertEqual(mem[0x400907], b'\x0f')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ESI, 3)
        self.assertEqual(cpu.RIP, 4196618)

    def test_BSR_3(self):
        ''' Instruction BSR_3
            Groups:
            0x457ac8:	bsr	rsi, rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457ac8] = 'H'
        mem[0x00457ac9] = '\x0f'
        mem[0x00457aca] = '\xbd'
        mem[0x00457acb] = '\xf6'
        cpu.ZF = False
        cpu.RSI = 0x4100800
        cpu.RIP = 0x457ac8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457ac8], b'H')
        self.assertEqual(mem[0x457ac9], b'\x0f')
        self.assertEqual(mem[0x457aca], b'\xbd')
        self.assertEqual(mem[0x457acb], b'\xf6')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSI, 26)
        self.assertEqual(cpu.RIP, 4553420)

    def test_BSR_4(self):
        ''' Instruction BSR_4
            Groups:
            0x400847:	bsr	esi, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400848] = '\xbd'
        mem[0x00400849] = '\xf6'
        mem[0x00400847] = '\x0f'
        cpu.ZF = True
        cpu.RIP = 0x400847
        cpu.ESI = 0xf
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400848], b'\xbd')
        self.assertEqual(mem[0x400849], b'\xf6')
        self.assertEqual(mem[0x400847], b'\x0f')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.ESI, 3)
        self.assertEqual(cpu.RIP, 4196426)

    def test_BSR_5(self):
        ''' Instruction BSR_5
            Groups:
            0x457c18:	bsr	rsi, rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457c18] = 'H'
        mem[0x00457c19] = '\x0f'
        mem[0x00457c1a] = '\xbd'
        mem[0x00457c1b] = '\xf6'
        cpu.ZF = False
        cpu.RSI = 0x41008000
        cpu.RIP = 0x457c18
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457c18], b'H')
        self.assertEqual(mem[0x457c19], b'\x0f')
        self.assertEqual(mem[0x457c1a], b'\xbd')
        self.assertEqual(mem[0x457c1b], b'\xf6')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSI, 30)
        self.assertEqual(cpu.RIP, 4553756)

    def test_BSR_6(self):
        ''' Instruction BSR_6
            Groups:
            0x457db8:	bsr	rsi, rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457db8] = 'H'
        mem[0x00457db9] = '\x0f'
        mem[0x00457dba] = '\xbd'
        mem[0x00457dbb] = '\xf6'
        cpu.ZF = False
        cpu.RSI = 0x4100800
        cpu.RIP = 0x457db8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457db8], b'H')
        self.assertEqual(mem[0x457db9], b'\x0f')
        self.assertEqual(mem[0x457dba], b'\xbd')
        self.assertEqual(mem[0x457dbb], b'\xf6')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSI, 26)
        self.assertEqual(cpu.RIP, 4554172)

    def test_BT_1(self):
        ''' Instruction BT_1
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = 0x467
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de36b8], b'\xc0')
        self.assertEqual(mem[0x7ffff7de36b5], b'A')
        self.assertEqual(mem[0x7ffff7de36b6], b'\x0f')
        self.assertEqual(mem[0x7ffff7de36b7], b'\xa3')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351923385)
        self.assertEqual(cpu.R8D, 1127)

    def test_BT_2(self):
        ''' Instruction BT_2
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = 0x2
        cpu.CF = False
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = 0x467
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de36b8], b'\xc0')
        self.assertEqual(mem[0x7ffff7de36b5], b'A')
        self.assertEqual(mem[0x7ffff7de36b6], b'\x0f')
        self.assertEqual(mem[0x7ffff7de36b7], b'\xa3')
        self.assertEqual(cpu.EAX, 2)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351923385)
        self.assertEqual(cpu.R8D, 1127)

    def test_BT_3(self):
        ''' Instruction BT_3
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = 0x2
        cpu.CF = False
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = 0x467
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de36b8], b'\xc0')
        self.assertEqual(mem[0x7ffff7de36b5], b'A')
        self.assertEqual(mem[0x7ffff7de36b6], b'\x0f')
        self.assertEqual(mem[0x7ffff7de36b7], b'\xa3')
        self.assertEqual(cpu.EAX, 2)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351923385)
        self.assertEqual(cpu.R8D, 1127)

    def test_BT_4(self):
        ''' Instruction BT_4
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = 0x467
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de36b8], b'\xc0')
        self.assertEqual(mem[0x7ffff7de36b5], b'A')
        self.assertEqual(mem[0x7ffff7de36b6], b'\x0f')
        self.assertEqual(mem[0x7ffff7de36b7], b'\xa3')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351923385)
        self.assertEqual(cpu.R8D, 1127)

    def test_BT_5(self):
        ''' Instruction BT_5
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = 0x467
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de36b8], b'\xc0')
        self.assertEqual(mem[0x7ffff7de36b5], b'A')
        self.assertEqual(mem[0x7ffff7de36b6], b'\x0f')
        self.assertEqual(mem[0x7ffff7de36b7], b'\xa3')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351923385)
        self.assertEqual(cpu.R8D, 1127)

    def test_BT_6(self):
        ''' Instruction BT_6
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = 0x2
        cpu.CF = False
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = 0x467
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de36b8], b'\xc0')
        self.assertEqual(mem[0x7ffff7de36b5], b'A')
        self.assertEqual(mem[0x7ffff7de36b6], b'\x0f')
        self.assertEqual(mem[0x7ffff7de36b7], b'\xa3')
        self.assertEqual(cpu.EAX, 2)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351923385)
        self.assertEqual(cpu.R8D, 1127)

    def test_CALL_1(self):
        ''' Instruction CALL_1
            Groups: call, mode64
            0x7ffff7de447a:	call	0x7ffff7de3800
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd880] = '\x00'
        mem[0x7fffffffd881] = '\x00'
        mem[0x7fffffffd882] = '\x00'
        mem[0x7fffffffd883] = '\x00'
        mem[0x7fffffffd884] = '\x00'
        mem[0x7fffffffd885] = '\x00'
        mem[0x7fffffffd886] = '\x00'
        mem[0x7fffffffd887] = '\x00'
        mem[0x7fffffffd888] = 'H'
        mem[0x7ffff7de447a] = '\xe8'
        mem[0x7ffff7de447b] = '\x81'
        mem[0x7ffff7de447c] = '\xf3'
        mem[0x7ffff7de447d] = '\xff'
        mem[0x7ffff7de447e] = '\xff'
        mem[0x7fffffffd878] = '\x7f'
        mem[0x7fffffffd879] = 'D'
        mem[0x7fffffffd87a] = '\xde'
        mem[0x7fffffffd87b] = '\xf7'
        mem[0x7fffffffd87c] = '\xff'
        mem[0x7fffffffd87d] = '\x7f'
        mem[0x7fffffffd87e] = '\x00'
        mem[0x7fffffffd87f] = '\x00'
        cpu.RSP = 0x7fffffffd880
        cpu.RIP = 0x7ffff7de447a
        cpu.RBP = 0x7fffffffd9a0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd880], b'\x00')
        self.assertEqual(mem[0x7fffffffd881], b'\x00')
        self.assertEqual(mem[0x7fffffffd882], b'\x00')
        self.assertEqual(mem[0x7fffffffd883], b'\x00')
        self.assertEqual(mem[0x7fffffffd884], b'\x00')
        self.assertEqual(mem[0x7fffffffd885], b'\x00')
        self.assertEqual(mem[0x7fffffffd886], b'\x00')
        self.assertEqual(mem[0x7fffffffd887], b'\x00')
        self.assertEqual(mem[0x7fffffffd888], b'H')
        self.assertEqual(mem[0x7fffffffd87a], b'\xde')
        self.assertEqual(mem[0x7fffffffd87b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd87c], b'\xff')
        self.assertEqual(mem[0x7fffffffd87d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd87e], b'\x00')
        self.assertEqual(mem[0x7fffffffd878], b'\x7f')
        self.assertEqual(mem[0x7fffffffd879], b'D')
        self.assertEqual(mem[0x7ffff7de447a], b'\xe8')
        self.assertEqual(mem[0x7ffff7de447b], b'\x81')
        self.assertEqual(mem[0x7ffff7de447c], b'\xf3')
        self.assertEqual(mem[0x7ffff7de447d], b'\xff')
        self.assertEqual(mem[0x7ffff7de447e], b'\xff')
        self.assertEqual(mem[0x7fffffffd87f], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345208)
        self.assertEqual(cpu.RIP, 140737351923712)
        self.assertEqual(cpu.RBP, 140737488345504)

    def test_CALL_2(self):
        ''' Instruction CALL_2
            Groups: call, mode64
            0x7ffff7a780e1:	call	qword ptr [r8 + 0x38]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd2000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffb000, 0x1000, 'rwx')
        mem[0x7fffffffbdb8] = '\xa2'
        mem[0x7fffffffbdb9] = '\x80'
        mem[0x7fffffffbdba] = '\xa7'
        mem[0x7fffffffbdbb] = '\xf7'
        mem[0x7fffffffbdbc] = '\xff'
        mem[0x7fffffffbdbd] = '\x7f'
        mem[0x7fffffffbdbe] = '\x00'
        mem[0x7fffffffbdbf] = '\x00'
        mem[0x7fffffffbdc0] = '\x00'
        mem[0x7fffffffbdc1] = '\x00'
        mem[0x7fffffffbdc2] = '\x00'
        mem[0x7fffffffbdc3] = '\x00'
        mem[0x7fffffffbdc4] = '\x00'
        mem[0x7fffffffbdc5] = '\x00'
        mem[0x7fffffffbdc6] = '\x00'
        mem[0x7fffffffbdc7] = '\x00'
        mem[0x7fffffffbdc8] = '\x00'
        mem[0x7ffff7a780e1] = 'A'
        mem[0x7ffff7a780e2] = '\xff'
        mem[0x7ffff7a780e3] = 'P'
        mem[0x7ffff7a780e4] = '8'
        mem[0x7ffff7dd2578] = '`'
        mem[0x7ffff7dd2579] = '\x96'
        mem[0x7ffff7dd257a] = '\xaa'
        mem[0x7ffff7dd257b] = '\xf7'
        mem[0x7ffff7dd257c] = '\xff'
        mem[0x7ffff7dd257d] = '\x7f'
        mem[0x7ffff7dd257e] = '\x00'
        mem[0x7ffff7dd257f] = '\x00'
        cpu.RSP = 0x7fffffffbdc0
        cpu.R8 = 0x7ffff7dd2540
        cpu.RIP = 0x7ffff7a780e1
        cpu.RBP = 0x7fffffffc330
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffbdb8], b'\xe5')
        self.assertEqual(mem[0x7fffffffbdb9], b'\x80')
        self.assertEqual(mem[0x7fffffffbdba], b'\xa7')
        self.assertEqual(mem[0x7fffffffbdbb], b'\xf7')
        self.assertEqual(mem[0x7fffffffbdbc], b'\xff')
        self.assertEqual(mem[0x7fffffffbdbd], b'\x7f')
        self.assertEqual(mem[0x7fffffffbdbe], b'\x00')
        self.assertEqual(mem[0x7fffffffbdbf], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc0], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc1], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc2], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc3], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc4], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc5], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc6], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc7], b'\x00')
        self.assertEqual(mem[0x7fffffffbdc8], b'\x00')
        self.assertEqual(mem[0x7ffff7a780e1], b'A')
        self.assertEqual(mem[0x7ffff7a780e2], b'\xff')
        self.assertEqual(mem[0x7ffff7a780e3], b'P')
        self.assertEqual(mem[0x7ffff7a780e4], b'8')
        self.assertEqual(mem[0x7ffff7dd2578], b'`')
        self.assertEqual(mem[0x7ffff7dd2579], b'\x96')
        self.assertEqual(mem[0x7ffff7dd257a], b'\xaa')
        self.assertEqual(mem[0x7ffff7dd257b], b'\xf7')
        self.assertEqual(mem[0x7ffff7dd257c], b'\xff')
        self.assertEqual(mem[0x7ffff7dd257d], b'\x7f')
        self.assertEqual(mem[0x7ffff7dd257e], b'\x00')
        self.assertEqual(mem[0x7ffff7dd257f], b'\x00')
        self.assertEqual(cpu.R8, 140737351853376)
        self.assertEqual(cpu.RSP, 140737488338360)
        self.assertEqual(cpu.RIP, 140737348540000)
        self.assertEqual(cpu.RBP, 140737488339760)

    def test_CALL_3(self):
        ''' Instruction CALL_3
            Groups: call, mode64
            0x4554b0:	call	0x45c7a0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00455000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda18] = '\xda'
        mem[0x7fffffffda19] = 'S'
        mem[0x7fffffffda1a] = 'E'
        mem[0x7fffffffda1b] = '\x00'
        mem[0x7fffffffda1c] = '\x00'
        mem[0x7fffffffda1d] = '\x00'
        mem[0x7fffffffda1e] = '\x00'
        mem[0x7fffffffda1f] = '\x00'
        mem[0x7fffffffda20] = '\x06'
        mem[0x7fffffffda21] = '\x00'
        mem[0x7fffffffda22] = '\x00'
        mem[0x7fffffffda23] = '\x00'
        mem[0x7fffffffda24] = '\x00'
        mem[0x7fffffffda25] = '\x00'
        mem[0x7fffffffda26] = '\x00'
        mem[0x7fffffffda27] = '\x00'
        mem[0x7fffffffda28] = '\x04'
        mem[0x004554b0] = '\xe8'
        mem[0x004554b1] = '\xeb'
        mem[0x004554b2] = 'r'
        mem[0x004554b3] = '\x00'
        mem[0x004554b4] = '\x00'
        cpu.RSP = 0x7fffffffda20
        cpu.RIP = 0x4554b0
        cpu.RBP = 0x7fffffffdad0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda18], b'\xb5')
        self.assertEqual(mem[0x7fffffffda19], b'T')
        self.assertEqual(mem[0x7fffffffda1a], b'E')
        self.assertEqual(mem[0x7fffffffda1b], b'\x00')
        self.assertEqual(mem[0x7fffffffda1c], b'\x00')
        self.assertEqual(mem[0x7fffffffda1d], b'\x00')
        self.assertEqual(mem[0x7fffffffda1e], b'\x00')
        self.assertEqual(mem[0x7fffffffda1f], b'\x00')
        self.assertEqual(mem[0x7fffffffda20], b'\x06')
        self.assertEqual(mem[0x7fffffffda21], b'\x00')
        self.assertEqual(mem[0x7fffffffda22], b'\x00')
        self.assertEqual(mem[0x7fffffffda23], b'\x00')
        self.assertEqual(mem[0x7fffffffda24], b'\x00')
        self.assertEqual(mem[0x7fffffffda25], b'\x00')
        self.assertEqual(mem[0x7fffffffda26], b'\x00')
        self.assertEqual(mem[0x7fffffffda27], b'\x00')
        self.assertEqual(mem[0x7fffffffda28], b'\x04')
        self.assertEqual(mem[0x4554b0], b'\xe8')
        self.assertEqual(mem[0x4554b1], b'\xeb')
        self.assertEqual(mem[0x4554b2], b'r')
        self.assertEqual(mem[0x4554b3], b'\x00')
        self.assertEqual(mem[0x4554b4], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345624)
        self.assertEqual(cpu.RIP, 4573088)
        self.assertEqual(cpu.RBP, 140737488345808)

    def test_CALL_4(self):
        ''' Instruction CALL_4
            Groups: call, mode64
            0x7ffff7de447a:	call	0x7ffff7de3800
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd880] = '\x00'
        mem[0x7fffffffd881] = '\x00'
        mem[0x7fffffffd882] = '\x00'
        mem[0x7fffffffd883] = '\x00'
        mem[0x7fffffffd884] = '\x00'
        mem[0x7fffffffd885] = '\x00'
        mem[0x7fffffffd886] = '\x00'
        mem[0x7fffffffd887] = '\x00'
        mem[0x7fffffffd888] = 'H'
        mem[0x7ffff7de447a] = '\xe8'
        mem[0x7ffff7de447b] = '\x81'
        mem[0x7ffff7de447c] = '\xf3'
        mem[0x7ffff7de447d] = '\xff'
        mem[0x7ffff7de447e] = '\xff'
        mem[0x7fffffffd878] = '\x7f'
        mem[0x7fffffffd879] = 'D'
        mem[0x7fffffffd87a] = '\xde'
        mem[0x7fffffffd87b] = '\xf7'
        mem[0x7fffffffd87c] = '\xff'
        mem[0x7fffffffd87d] = '\x7f'
        mem[0x7fffffffd87e] = '\x00'
        mem[0x7fffffffd87f] = '\x00'
        cpu.RSP = 0x7fffffffd880
        cpu.RIP = 0x7ffff7de447a
        cpu.RBP = 0x7fffffffd9a0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd880], b'\x00')
        self.assertEqual(mem[0x7fffffffd881], b'\x00')
        self.assertEqual(mem[0x7fffffffd882], b'\x00')
        self.assertEqual(mem[0x7fffffffd883], b'\x00')
        self.assertEqual(mem[0x7fffffffd884], b'\x00')
        self.assertEqual(mem[0x7fffffffd885], b'\x00')
        self.assertEqual(mem[0x7fffffffd886], b'\x00')
        self.assertEqual(mem[0x7fffffffd887], b'\x00')
        self.assertEqual(mem[0x7fffffffd888], b'H')
        self.assertEqual(mem[0x7fffffffd87a], b'\xde')
        self.assertEqual(mem[0x7fffffffd87b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd87c], b'\xff')
        self.assertEqual(mem[0x7fffffffd87d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd87e], b'\x00')
        self.assertEqual(mem[0x7fffffffd878], b'\x7f')
        self.assertEqual(mem[0x7fffffffd879], b'D')
        self.assertEqual(mem[0x7ffff7de447a], b'\xe8')
        self.assertEqual(mem[0x7ffff7de447b], b'\x81')
        self.assertEqual(mem[0x7ffff7de447c], b'\xf3')
        self.assertEqual(mem[0x7ffff7de447d], b'\xff')
        self.assertEqual(mem[0x7ffff7de447e], b'\xff')
        self.assertEqual(mem[0x7fffffffd87f], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345208)
        self.assertEqual(cpu.RIP, 140737351923712)
        self.assertEqual(cpu.RBP, 140737488345504)

    def test_CALL_5(self):
        ''' Instruction CALL_5
            Groups: call, mode64
            0x7ffff7de40a6:	call	0x7ffff7de3660
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd808] = '\xab'
        mem[0x7fffffffd809] = '@'
        mem[0x7fffffffd80a] = '\xde'
        mem[0x7fffffffd80b] = '\xf7'
        mem[0x7fffffffd80c] = '\xff'
        mem[0x7fffffffd80d] = '\x7f'
        mem[0x7fffffffd80e] = '\x00'
        mem[0x7fffffffd80f] = '\x00'
        mem[0x7fffffffd810] = '\xec'
        mem[0x7fffffffd811] = '\x04'
        mem[0x7fffffffd812] = '\x00'
        mem[0x7fffffffd813] = '\x00'
        mem[0x7fffffffd814] = '\x00'
        mem[0x7fffffffd815] = '\x00'
        mem[0x7fffffffd816] = '\x00'
        mem[0x7fffffffd817] = '\x00'
        mem[0x7fffffffd818] = '\xd8'
        mem[0x7ffff7de40a6] = '\xe8'
        mem[0x7ffff7de40a7] = '\xb5'
        mem[0x7ffff7de40a8] = '\xf5'
        mem[0x7ffff7de40a9] = '\xff'
        mem[0x7ffff7de40aa] = '\xff'
        cpu.RSP = 0x7fffffffd810
        cpu.RIP = 0x7ffff7de40a6
        cpu.RBP = 0x7fffffffd900
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd808], b'\xab')
        self.assertEqual(mem[0x7fffffffd809], b'@')
        self.assertEqual(mem[0x7fffffffd80a], b'\xde')
        self.assertEqual(mem[0x7fffffffd80b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd80c], b'\xff')
        self.assertEqual(mem[0x7fffffffd80d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd80e], b'\x00')
        self.assertEqual(mem[0x7fffffffd80f], b'\x00')
        self.assertEqual(mem[0x7fffffffd810], b'\xec')
        self.assertEqual(mem[0x7fffffffd811], b'\x04')
        self.assertEqual(mem[0x7fffffffd812], b'\x00')
        self.assertEqual(mem[0x7fffffffd813], b'\x00')
        self.assertEqual(mem[0x7fffffffd814], b'\x00')
        self.assertEqual(mem[0x7fffffffd815], b'\x00')
        self.assertEqual(mem[0x7fffffffd816], b'\x00')
        self.assertEqual(mem[0x7fffffffd817], b'\x00')
        self.assertEqual(mem[0x7fffffffd818], b'\xd8')
        self.assertEqual(mem[0x7ffff7de40a6], b'\xe8')
        self.assertEqual(mem[0x7ffff7de40a7], b'\xb5')
        self.assertEqual(mem[0x7ffff7de40a8], b'\xf5')
        self.assertEqual(mem[0x7ffff7de40a9], b'\xff')
        self.assertEqual(mem[0x7ffff7de40aa], b'\xff')
        self.assertEqual(cpu.RSP, 140737488345096)
        self.assertEqual(cpu.RIP, 140737351923296)
        self.assertEqual(cpu.RBP, 140737488345344)

    def test_CALL_6(self):
        ''' Instruction CALL_6
            Groups: call, mode64
            0x45f878:	call	0x413490
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0045f000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdb00] = '\x01'
        mem[0x7fffffffdb01] = 'S'
        mem[0x7fffffffdb02] = 'J'
        mem[0x7fffffffdb03] = '\x00'
        mem[0x7fffffffdb04] = '\x00'
        mem[0x7fffffffdb05] = '\x00'
        mem[0x7fffffffdb06] = '\x00'
        mem[0x7fffffffdb07] = '\x00'
        mem[0x7fffffffdb08] = '\xf4'
        mem[0x0045f878] = '\xe8'
        mem[0x0045f879] = '\x13'
        mem[0x0045f87a] = '<'
        mem[0x0045f87b] = '\xfb'
        mem[0x0045f87c] = '\xff'
        mem[0x7fffffffdaf8] = '9'
        mem[0x7fffffffdaf9] = '\xf8'
        mem[0x7fffffffdafa] = 'E'
        mem[0x7fffffffdafb] = '\x00'
        mem[0x7fffffffdafc] = '\x00'
        mem[0x7fffffffdafd] = '\x00'
        mem[0x7fffffffdafe] = '\x00'
        mem[0x7fffffffdaff] = '\x00'
        cpu.RSP = 0x7fffffffdb00
        cpu.RIP = 0x45f878
        cpu.RBP = 0x7fffffffdb20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdb00], b'\x01')
        self.assertEqual(mem[0x7fffffffdb01], b'S')
        self.assertEqual(mem[0x7fffffffdb02], b'J')
        self.assertEqual(mem[0x7fffffffdb03], b'\x00')
        self.assertEqual(mem[0x7fffffffdb04], b'\x00')
        self.assertEqual(mem[0x7fffffffdb05], b'\x00')
        self.assertEqual(mem[0x7fffffffdb06], b'\x00')
        self.assertEqual(mem[0x7fffffffdb07], b'\x00')
        self.assertEqual(mem[0x7fffffffdb08], b'\xf4')
        self.assertEqual(mem[0x7fffffffdaf8], b'}')
        self.assertEqual(mem[0x7fffffffdaf9], b'\xf8')
        self.assertEqual(mem[0x7fffffffdafa], b'E')
        self.assertEqual(mem[0x7fffffffdafb], b'\x00')
        self.assertEqual(mem[0x7fffffffdafc], b'\x00')
        self.assertEqual(mem[0x45f878], b'\xe8')
        self.assertEqual(mem[0x45f879], b'\x13')
        self.assertEqual(mem[0x45f87a], b'<')
        self.assertEqual(mem[0x45f87b], b'\xfb')
        self.assertEqual(mem[0x45f87c], b'\xff')
        self.assertEqual(mem[0x7fffffffdafd], b'\x00')
        self.assertEqual(mem[0x7fffffffdafe], b'\x00')
        self.assertEqual(mem[0x7fffffffdaff], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345848)
        self.assertEqual(cpu.RIP, 4273296)
        self.assertEqual(cpu.RBP, 140737488345888)

    def test_CDQE_1(self):
        ''' Instruction CDQE_1
            Groups:
            0x400aa0:	cdqe
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400aa0] = 'H'
        mem[0x00400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = 0x92
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400aa0], b'H')
        self.assertEqual(mem[0x400aa1], b'\x98')
        self.assertEqual(cpu.RAX, 146)
        self.assertEqual(cpu.RIP, 4197026)

    def test_CDQE_2(self):
        ''' Instruction CDQE_2
            Groups:
            0x400aa0:	cdqe
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400aa0] = 'H'
        mem[0x00400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = 0x5a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400aa0], b'H')
        self.assertEqual(mem[0x400aa1], b'\x98')
        self.assertEqual(cpu.RAX, 90)
        self.assertEqual(cpu.RIP, 4197026)

    def test_CDQE_3(self):
        ''' Instruction CDQE_3
            Groups:
            0x400aa0:	cdqe
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400aa0] = 'H'
        mem[0x00400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = 0x80
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400aa0], b'H')
        self.assertEqual(mem[0x400aa1], b'\x98')
        self.assertEqual(cpu.RAX, 128)
        self.assertEqual(cpu.RIP, 4197026)

    def test_CDQE_4(self):
        ''' Instruction CDQE_4
            Groups:
            0x400acf:	cdqe
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400ad0] = '\x98'
        mem[0x00400acf] = 'H'
        cpu.RIP = 0x400acf
        cpu.RAX = 0x98
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400ad0], b'\x98')
        self.assertEqual(mem[0x400acf], b'H')
        self.assertEqual(cpu.RAX, 152)
        self.assertEqual(cpu.RIP, 4197073)

    def test_CDQE_5(self):
        ''' Instruction CDQE_5
            Groups:
            0x400aa0:	cdqe
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400aa0] = 'H'
        mem[0x00400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = 0x73
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400aa0], b'H')
        self.assertEqual(mem[0x400aa1], b'\x98')
        self.assertEqual(cpu.RAX, 115)
        self.assertEqual(cpu.RIP, 4197026)

    def test_CDQE_6(self):
        ''' Instruction CDQE_6
            Groups:
            0x400b07:	cdqe
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400b08] = '\x98'
        mem[0x00400b07] = 'H'
        cpu.RIP = 0x400b07
        cpu.RAX = 0xc6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400b08], b'\x98')
        self.assertEqual(mem[0x400b07], b'H')
        self.assertEqual(cpu.RAX, 198)
        self.assertEqual(cpu.RIP, 4197129)

    def test_CLC_1(self):
        ''' Instruction CLC_1
            Groups:
            0x46a9fc:	clc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0046a000, 0x1000, 'rwx')
        mem[0x0046a9fc] = '\xf8'
        cpu.CF = True
        cpu.RIP = 0x46a9fc
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x46a9fc], b'\xf8')
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4631037)

    def test_CLC_2(self):
        ''' Instruction CLC_2
            Groups:
            0x7542c8:	clc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00754000, 0x1000, 'rwx')
        mem[0x007542c8] = '\xf8'
        cpu.CF = True
        cpu.RIP = 0x7542c8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7542c8], b'\xf8')
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 7684809)

    def test_CLC_3(self):
        ''' Instruction CLC_3
            Groups:
            0x4b473c:	clc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004b4000, 0x1000, 'rwx')
        mem[0x004b473c] = '\xf8'
        cpu.CF = True
        cpu.RIP = 0x4b473c
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4b473c], b'\xf8')
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4933437)

    def test_CLC_4(self):
        ''' Instruction CLC_4
            Groups:
            0x49d4dd:	clc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0049d000, 0x1000, 'rwx')
        mem[0x0049d4dd] = '\xf8'
        cpu.CF = True
        cpu.RIP = 0x49d4dd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x49d4dd], b'\xf8')
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4838622)

    def test_CLC_5(self):
        ''' Instruction CLC_5
            Groups:
            0x4fd621:	clc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004fd000, 0x1000, 'rwx')
        mem[0x004fd621] = '\xf8'
        cpu.CF = True
        cpu.RIP = 0x4fd621
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4fd621], b'\xf8')
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 5232162)

    def test_CLC_6(self):
        ''' Instruction CLC_6
            Groups:
            0x4fadef:	clc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004fa000, 0x1000, 'rwx')
        mem[0x004fadef] = '\xf8'
        cpu.CF = True
        cpu.RIP = 0x4fadef
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4fadef], b'\xf8')
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 5221872)

    def test_CMOVAE_1(self):
        ''' Instruction CMOVAE_1
            Groups: cmov
            0x4117e8:	cmovae	rax, r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x004117e8] = 'I'
        mem[0x004117e9] = '\x0f'
        mem[0x004117ea] = 'C'
        mem[0x004117eb] = '\xc2'
        cpu.RIP = 0x4117e8
        cpu.CF = False
        cpu.RAX = 0x20
        cpu.R10 = 0x20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4117e8], b'I')
        self.assertEqual(mem[0x4117e9], b'\x0f')
        self.assertEqual(mem[0x4117ea], b'C')
        self.assertEqual(mem[0x4117eb], b'\xc2')
        self.assertEqual(cpu.RAX, 32)
        self.assertEqual(cpu.RIP, 4265964)
        self.assertEqual(cpu.R10, 32)

    def test_CMOVAE_2(self):
        ''' Instruction CMOVAE_2
            Groups: cmov
            0x414318:	cmovae	rax, r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x00414318] = 'I'
        mem[0x00414319] = '\x0f'
        mem[0x0041431a] = 'C'
        mem[0x0041431b] = '\xc2'
        cpu.RIP = 0x414318
        cpu.CF = False
        cpu.RAX = 0x20
        cpu.R10 = 0x20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x414318], b'I')
        self.assertEqual(mem[0x414319], b'\x0f')
        self.assertEqual(mem[0x41431a], b'C')
        self.assertEqual(mem[0x41431b], b'\xc2')
        self.assertEqual(cpu.RAX, 32)
        self.assertEqual(cpu.RIP, 4277020)
        self.assertEqual(cpu.R10, 32)

    def test_CMOVAE_3(self):
        ''' Instruction CMOVAE_3
            Groups: cmov
            0x5555555662c8:	cmovae	rdx, rbx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555566000, 0x1000, 'rwx')
        mem[0x5555555662c8] = 'H'
        mem[0x5555555662c9] = '\x0f'
        mem[0x5555555662ca] = 'C'
        mem[0x5555555662cb] = '\xd3'
        cpu.RDX = 0xffffffffffffffff
        cpu.CF = False
        cpu.RIP = 0x5555555662c8
        cpu.RBX = 0x7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5555555662c8], b'H')
        self.assertEqual(mem[0x5555555662c9], b'\x0f')
        self.assertEqual(mem[0x5555555662ca], b'C')
        self.assertEqual(mem[0x5555555662cb], b'\xd3')
        self.assertEqual(cpu.RDX, 7)
        self.assertEqual(cpu.RIP, 93824992305868)
        self.assertEqual(cpu.RBX, 7)

    def test_CMOVAE_4(self):
        ''' Instruction CMOVAE_4
            Groups: cmov
            0x411778:	cmovae	rax, r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x00411778] = 'I'
        mem[0x00411779] = '\x0f'
        mem[0x0041177a] = 'C'
        mem[0x0041177b] = '\xc2'
        cpu.RIP = 0x411778
        cpu.CF = False
        cpu.RAX = 0x20
        cpu.R10 = 0x4a0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x411778], b'I')
        self.assertEqual(mem[0x411779], b'\x0f')
        self.assertEqual(mem[0x41177a], b'C')
        self.assertEqual(mem[0x41177b], b'\xc2')
        self.assertEqual(cpu.RAX, 1184)
        self.assertEqual(cpu.RIP, 4265852)
        self.assertEqual(cpu.R10, 1184)

    def test_CMOVAE_5(self):
        ''' Instruction CMOVAE_5
            Groups: cmov
            0x411778:	cmovae	rax, r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x00411778] = 'I'
        mem[0x00411779] = '\x0f'
        mem[0x0041177a] = 'C'
        mem[0x0041177b] = '\xc2'
        cpu.RIP = 0x411778
        cpu.CF = False
        cpu.RAX = 0x20
        cpu.R10 = 0x20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x411778], b'I')
        self.assertEqual(mem[0x411779], b'\x0f')
        self.assertEqual(mem[0x41177a], b'C')
        self.assertEqual(mem[0x41177b], b'\xc2')
        self.assertEqual(cpu.RAX, 32)
        self.assertEqual(cpu.RIP, 4265852)
        self.assertEqual(cpu.R10, 32)

    def test_CMOVAE_6(self):
        ''' Instruction CMOVAE_6
            Groups: cmov
            0x411b58:	cmovae	rax, r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x00411b58] = 'I'
        mem[0x00411b59] = '\x0f'
        mem[0x00411b5a] = 'C'
        mem[0x00411b5b] = '\xc2'
        cpu.RIP = 0x411b58
        cpu.CF = False
        cpu.RAX = 0x20
        cpu.R10 = 0x50
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x411b58], b'I')
        self.assertEqual(mem[0x411b59], b'\x0f')
        self.assertEqual(mem[0x411b5a], b'C')
        self.assertEqual(mem[0x411b5b], b'\xc2')
        self.assertEqual(cpu.RAX, 80)
        self.assertEqual(cpu.RIP, 4266844)
        self.assertEqual(cpu.R10, 80)

    def test_CMOVA_1(self):
        ''' Instruction CMOVA_1
            Groups: cmov
            0x7ffff7de0ab0:	cmova	rax, r8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de0000, 0x1000, 'rwx')
        mem[0x7ffff7de0ab0] = 'I'
        mem[0x7ffff7de0ab1] = '\x0f'
        mem[0x7ffff7de0ab2] = 'G'
        mem[0x7ffff7de0ab3] = '\xc0'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de0ab0
        cpu.R8 = 0x7ffff7dd9398
        cpu.CF = True
        cpu.RAX = 0x7ffff7dd5000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de0ab0], b'I')
        self.assertEqual(mem[0x7ffff7de0ab1], b'\x0f')
        self.assertEqual(mem[0x7ffff7de0ab2], b'G')
        self.assertEqual(mem[0x7ffff7de0ab3], b'\xc0')
        self.assertEqual(cpu.R8, 140737351881624)
        self.assertEqual(cpu.RAX, 140737351864320)
        self.assertEqual(cpu.RIP, 140737351912116)

    def test_CMOVA_2(self):
        ''' Instruction CMOVA_2
            Groups: cmov
            0x7ffff7a9d404:	cmova	rbx, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a9d000, 0x1000, 'rwx')
        mem[0x7ffff7a9d404] = 'H'
        mem[0x7ffff7a9d405] = '\x0f'
        mem[0x7ffff7a9d406] = 'G'
        mem[0x7ffff7a9d407] = '\xd8'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7a9d404
        cpu.CF = True
        cpu.RAX = 0x7fffffff
        cpu.RBX = 0x14
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a9d404], b'H')
        self.assertEqual(mem[0x7ffff7a9d405], b'\x0f')
        self.assertEqual(mem[0x7ffff7a9d406], b'G')
        self.assertEqual(mem[0x7ffff7a9d407], b'\xd8')
        self.assertEqual(cpu.RAX, 2147483647)
        self.assertEqual(cpu.RIP, 140737348490248)
        self.assertEqual(cpu.RBX, 20)

    def test_CMOVA_3(self):
        ''' Instruction CMOVA_3
            Groups: cmov
            0x4082a4:	cmova	rbx, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00408000, 0x1000, 'rwx')
        mem[0x004082a4] = 'H'
        mem[0x004082a5] = '\x0f'
        mem[0x004082a6] = 'G'
        mem[0x004082a7] = '\xd8'
        cpu.ZF = False
        cpu.RIP = 0x4082a4
        cpu.CF = True
        cpu.RAX = 0x7fffffff
        cpu.RBX = 0xb
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4082a4], b'H')
        self.assertEqual(mem[0x4082a5], b'\x0f')
        self.assertEqual(mem[0x4082a6], b'G')
        self.assertEqual(mem[0x4082a7], b'\xd8')
        self.assertEqual(cpu.RAX, 2147483647)
        self.assertEqual(cpu.RIP, 4227752)
        self.assertEqual(cpu.RBX, 11)

    def test_CMOVA_4(self):
        ''' Instruction CMOVA_4
            Groups: cmov
            0x41462a:	cmova	rdx, r13
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x0041462a] = 'I'
        mem[0x0041462b] = '\x0f'
        mem[0x0041462c] = 'G'
        mem[0x0041462d] = '\xd5'
        cpu.RDX = 0x4a0
        cpu.ZF = False
        cpu.R13 = 0x21df0
        cpu.RIP = 0x41462a
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41462a], b'I')
        self.assertEqual(mem[0x41462b], b'\x0f')
        self.assertEqual(mem[0x41462c], b'G')
        self.assertEqual(mem[0x41462d], b'\xd5')
        self.assertEqual(cpu.RDX, 1184)
        self.assertEqual(cpu.RIP, 4277806)
        self.assertEqual(cpu.R13, 138736)

    def test_CMOVA_5(self):
        ''' Instruction CMOVA_5
            Groups: cmov
            0x41424a:	cmova	rdx, r13
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x0041424a] = 'I'
        mem[0x0041424b] = '\x0f'
        mem[0x0041424c] = 'G'
        mem[0x0041424d] = '\xd5'
        cpu.RDX = 0x4a0
        cpu.ZF = False
        cpu.R13 = 0x21df0
        cpu.RIP = 0x41424a
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41424a], b'I')
        self.assertEqual(mem[0x41424b], b'\x0f')
        self.assertEqual(mem[0x41424c], b'G')
        self.assertEqual(mem[0x41424d], b'\xd5')
        self.assertEqual(cpu.RDX, 1184)
        self.assertEqual(cpu.RIP, 4276814)
        self.assertEqual(cpu.R13, 138736)

    def test_CMOVA_6(self):
        ''' Instruction CMOVA_6
            Groups: cmov
            0x4142ba:	cmova	rdx, r13
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x004142ba] = 'I'
        mem[0x004142bb] = '\x0f'
        mem[0x004142bc] = 'G'
        mem[0x004142bd] = '\xd5'
        cpu.RDX = 0x4a0
        cpu.ZF = False
        cpu.R13 = 0x21df0
        cpu.RIP = 0x4142ba
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4142ba], b'I')
        self.assertEqual(mem[0x4142bb], b'\x0f')
        self.assertEqual(mem[0x4142bc], b'G')
        self.assertEqual(mem[0x4142bd], b'\xd5')
        self.assertEqual(cpu.RDX, 1184)
        self.assertEqual(cpu.RIP, 4276926)
        self.assertEqual(cpu.R13, 138736)

    def test_CMOVBE_1(self):
        ''' Instruction CMOVBE_1
            Groups: cmov
            0x40d233:	cmovbe	rbx, r14
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040d000, 0x1000, 'rwx')
        mem[0x0040d233] = 'I'
        mem[0x0040d234] = '\x0f'
        mem[0x0040d235] = 'F'
        mem[0x0040d236] = '\xde'
        cpu.ZF = False
        cpu.RBX = 0x1000
        cpu.R14 = 0x20
        cpu.RIP = 0x40d233
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40d233], b'I')
        self.assertEqual(mem[0x40d234], b'\x0f')
        self.assertEqual(mem[0x40d235], b'F')
        self.assertEqual(mem[0x40d236], b'\xde')
        self.assertEqual(cpu.R14, 32)
        self.assertEqual(cpu.RIP, 4248119)
        self.assertEqual(cpu.RBX, 32)

    def test_CMOVBE_2(self):
        ''' Instruction CMOVBE_2
            Groups: cmov
            0x7ffff7aa96b3:	cmovbe	rbx, r14
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa9000, 0x1000, 'rwx')
        mem[0x7ffff7aa96b3] = 'I'
        mem[0x7ffff7aa96b4] = '\x0f'
        mem[0x7ffff7aa96b5] = 'F'
        mem[0x7ffff7aa96b6] = '\xde'
        cpu.ZF = False
        cpu.RBX = 0x2000
        cpu.R14 = 0x4
        cpu.RIP = 0x7ffff7aa96b3
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7aa96b3], b'I')
        self.assertEqual(mem[0x7ffff7aa96b4], b'\x0f')
        self.assertEqual(mem[0x7ffff7aa96b5], b'F')
        self.assertEqual(mem[0x7ffff7aa96b6], b'\xde')
        self.assertEqual(cpu.R14, 4)
        self.assertEqual(cpu.RIP, 140737348540087)
        self.assertEqual(cpu.RBX, 4)

    def test_CMOVBE_3(self):
        ''' Instruction CMOVBE_3
            Groups: cmov
            0x7ffff7aa96b3:	cmovbe	rbx, r14
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa9000, 0x1000, 'rwx')
        mem[0x7ffff7aa96b3] = 'I'
        mem[0x7ffff7aa96b4] = '\x0f'
        mem[0x7ffff7aa96b5] = 'F'
        mem[0x7ffff7aa96b6] = '\xde'
        cpu.ZF = False
        cpu.RBX = 0x1000
        cpu.R14 = 0x13
        cpu.RIP = 0x7ffff7aa96b3
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7aa96b3], b'I')
        self.assertEqual(mem[0x7ffff7aa96b4], b'\x0f')
        self.assertEqual(mem[0x7ffff7aa96b5], b'F')
        self.assertEqual(mem[0x7ffff7aa96b6], b'\xde')
        self.assertEqual(cpu.R14, 19)
        self.assertEqual(cpu.RIP, 140737348540087)
        self.assertEqual(cpu.RBX, 19)

    def test_CMOVBE_4(self):
        ''' Instruction CMOVBE_4
            Groups: cmov
            0x40d263:	cmovbe	rbx, r14
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040d000, 0x1000, 'rwx')
        mem[0x0040d263] = 'I'
        mem[0x0040d264] = '\x0f'
        mem[0x0040d265] = 'F'
        mem[0x0040d266] = '\xde'
        cpu.ZF = False
        cpu.RBX = 0x1000
        cpu.R14 = 0x13
        cpu.RIP = 0x40d263
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40d263], b'I')
        self.assertEqual(mem[0x40d264], b'\x0f')
        self.assertEqual(mem[0x40d265], b'F')
        self.assertEqual(mem[0x40d266], b'\xde')
        self.assertEqual(cpu.R14, 19)
        self.assertEqual(cpu.RIP, 4248167)
        self.assertEqual(cpu.RBX, 19)

    def test_CMOVBE_5(self):
        ''' Instruction CMOVBE_5
            Groups: cmov
            0x7ffff7aa96b3:	cmovbe	rbx, r14
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa9000, 0x1000, 'rwx')
        mem[0x7ffff7aa96b3] = 'I'
        mem[0x7ffff7aa96b4] = '\x0f'
        mem[0x7ffff7aa96b5] = 'F'
        mem[0x7ffff7aa96b6] = '\xde'
        cpu.ZF = False
        cpu.RBX = 0x1000
        cpu.R14 = 0x13
        cpu.RIP = 0x7ffff7aa96b3
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7aa96b3], b'I')
        self.assertEqual(mem[0x7ffff7aa96b4], b'\x0f')
        self.assertEqual(mem[0x7ffff7aa96b5], b'F')
        self.assertEqual(mem[0x7ffff7aa96b6], b'\xde')
        self.assertEqual(cpu.R14, 19)
        self.assertEqual(cpu.RIP, 140737348540087)
        self.assertEqual(cpu.RBX, 19)

    def test_CMOVBE_6(self):
        ''' Instruction CMOVBE_6
            Groups: cmov
            0x40fde3:	cmovbe	rbx, r14
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040f000, 0x1000, 'rwx')
        mem[0x0040fde3] = 'I'
        mem[0x0040fde4] = '\x0f'
        mem[0x0040fde5] = 'F'
        mem[0x0040fde6] = '\xde'
        cpu.ZF = False
        cpu.RBX = 0x1000
        cpu.R14 = 0x240
        cpu.RIP = 0x40fde3
        cpu.CF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40fde3], b'I')
        self.assertEqual(mem[0x40fde4], b'\x0f')
        self.assertEqual(mem[0x40fde5], b'F')
        self.assertEqual(mem[0x40fde6], b'\xde')
        self.assertEqual(cpu.R14, 576)
        self.assertEqual(cpu.RIP, 4259303)
        self.assertEqual(cpu.RBX, 576)

    def test_CMOVB_1(self):
        ''' Instruction CMOVB_1
            Groups: cmov
            0x7ffff7deb97f:	cmovb	r12d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7deb000, 0x1000, 'rwx')
        mem[0x7ffff7deb980] = '\x0f'
        mem[0x7ffff7deb981] = 'B'
        mem[0x7ffff7deb982] = '\xe0'
        mem[0x7ffff7deb97f] = 'D'
        cpu.EAX = 0xa
        cpu.CF = False
        cpu.RIP = 0x7ffff7deb97f
        cpu.R12D = 0x1a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7deb980], b'\x0f')
        self.assertEqual(mem[0x7ffff7deb981], b'B')
        self.assertEqual(mem[0x7ffff7deb982], b'\xe0')
        self.assertEqual(mem[0x7ffff7deb97f], b'D')
        self.assertEqual(cpu.EAX, 10)
        self.assertEqual(cpu.R12D, 26)
        self.assertEqual(cpu.RIP, 140737351956867)

    def test_CMOVB_2(self):
        ''' Instruction CMOVB_2
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = 0x1
        cpu.CF = True
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = 0xffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df45ad], b'\x0f')
        self.assertEqual(mem[0x7ffff7df45ae], b'B')
        self.assertEqual(mem[0x7ffff7df45af], b'\xc1')
        self.assertEqual(cpu.EAX, 4294967295)
        self.assertEqual(cpu.RIP, 140737351992752)
        self.assertEqual(cpu.ECX, 4294967295)

    def test_CMOVB_3(self):
        ''' Instruction CMOVB_3
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = 0xffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df45ad], b'\x0f')
        self.assertEqual(mem[0x7ffff7df45ae], b'B')
        self.assertEqual(mem[0x7ffff7df45af], b'\xc1')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.RIP, 140737351992752)
        self.assertEqual(cpu.ECX, 4294967295)

    def test_CMOVB_4(self):
        ''' Instruction CMOVB_4
            Groups: cmov
            0x7ffff7deb97f:	cmovb	r12d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7deb000, 0x1000, 'rwx')
        mem[0x7ffff7deb980] = '\x0f'
        mem[0x7ffff7deb981] = 'B'
        mem[0x7ffff7deb982] = '\xe0'
        mem[0x7ffff7deb97f] = 'D'
        cpu.EAX = 0x12
        cpu.CF = False
        cpu.RIP = 0x7ffff7deb97f
        cpu.R12D = 0x1a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7deb980], b'\x0f')
        self.assertEqual(mem[0x7ffff7deb981], b'B')
        self.assertEqual(mem[0x7ffff7deb982], b'\xe0')
        self.assertEqual(mem[0x7ffff7deb97f], b'D')
        self.assertEqual(cpu.EAX, 18)
        self.assertEqual(cpu.R12D, 26)
        self.assertEqual(cpu.RIP, 140737351956867)

    def test_CMOVB_5(self):
        ''' Instruction CMOVB_5
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = 0xffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df45ad], b'\x0f')
        self.assertEqual(mem[0x7ffff7df45ae], b'B')
        self.assertEqual(mem[0x7ffff7df45af], b'\xc1')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.RIP, 140737351992752)
        self.assertEqual(cpu.ECX, 4294967295)

    def test_CMOVB_6(self):
        ''' Instruction CMOVB_6
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = 0x1
        cpu.CF = False
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = 0xffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df45ad], b'\x0f')
        self.assertEqual(mem[0x7ffff7df45ae], b'B')
        self.assertEqual(mem[0x7ffff7df45af], b'\xc1')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.RIP, 140737351992752)
        self.assertEqual(cpu.ECX, 4294967295)

    def test_CMOVE_1(self):
        ''' Instruction CMOVE_1
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = False
        cpu.R8 = 0x7ffff7ff7c48
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6260], b'D')
        self.assertEqual(mem[0x7ffff7de6261], b'\xc0')
        self.assertEqual(mem[0x7ffff7de625e], b'L')
        self.assertEqual(mem[0x7ffff7de625f], b'\x0f')
        self.assertEqual(cpu.R8, 140737354103880)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 140737351934562)

    def test_CMOVE_2(self):
        ''' Instruction CMOVE_2
            Groups: cmov
            0x415f05:	cmove	rax, rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00415000, 0x1000, 'rwx')
        mem[0x00415f08] = '\xc2'
        mem[0x00415f05] = 'H'
        mem[0x00415f06] = '\x0f'
        mem[0x00415f07] = 'D'
        cpu.ZF = False
        cpu.RIP = 0x415f05
        cpu.RAX = 0x6e01c0
        cpu.RDX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x415f08], b'\xc2')
        self.assertEqual(mem[0x415f05], b'H')
        self.assertEqual(mem[0x415f06], b'\x0f')
        self.assertEqual(mem[0x415f07], b'D')
        self.assertEqual(cpu.RAX, 7209408)
        self.assertEqual(cpu.RIP, 4284169)
        self.assertEqual(cpu.RDX, 0)

    def test_CMOVE_3(self):
        ''' Instruction CMOVE_3
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = False
        cpu.R8 = 0x7ffff7ff7c48
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6260], b'D')
        self.assertEqual(mem[0x7ffff7de6261], b'\xc0')
        self.assertEqual(mem[0x7ffff7de625e], b'L')
        self.assertEqual(mem[0x7ffff7de625f], b'\x0f')
        self.assertEqual(cpu.R8, 140737354103880)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 140737351934562)

    def test_CMOVE_4(self):
        ''' Instruction CMOVE_4
            Groups: cmov
            0x7ffff7df2822:	cmove	rdi, qword ptr [rip + 0x20b886]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df2000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ffe000, 0x1000, 'rwx')
        mem[0x7ffff7df2822] = 'H'
        mem[0x7ffff7df2823] = '\x0f'
        mem[0x7ffff7df2824] = 'D'
        mem[0x7ffff7df2825] = '='
        mem[0x7ffff7df2826] = '\x86'
        mem[0x7ffff7df2827] = '\xb8'
        mem[0x7ffff7df2828] = ' '
        mem[0x7ffff7df2829] = '\x00'
        mem[0x7ffff7ffe0b0] = '0'
        mem[0x7ffff7ffe0b1] = '\x7f'
        mem[0x7ffff7ffe0b2] = '\xff'
        mem[0x7ffff7ffe0b3] = '\xf7'
        mem[0x7ffff7ffe0b4] = '\xff'
        mem[0x7ffff7ffe0b5] = '\x7f'
        mem[0x7ffff7ffe0b6] = '\x00'
        mem[0x7ffff7ffe0b7] = '\x00'
        cpu.ZF = False
        cpu.RDI = 0x7ffff7fd8000
        cpu.RIP = 0x7ffff7df2822
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df2822], b'H')
        self.assertEqual(mem[0x7ffff7df2823], b'\x0f')
        self.assertEqual(mem[0x7ffff7df2824], b'D')
        self.assertEqual(mem[0x7ffff7df2825], b'=')
        self.assertEqual(mem[0x7ffff7df2826], b'\x86')
        self.assertEqual(mem[0x7ffff7df2827], b'\xb8')
        self.assertEqual(mem[0x7ffff7df2828], b' ')
        self.assertEqual(mem[0x7ffff7df2829], b'\x00')
        self.assertEqual(mem[0x7ffff7ffe0b0], b'0')
        self.assertEqual(mem[0x7ffff7ffe0b1], b'\x7f')
        self.assertEqual(mem[0x7ffff7ffe0b2], b'\xff')
        self.assertEqual(mem[0x7ffff7ffe0b3], b'\xf7')
        self.assertEqual(mem[0x7ffff7ffe0b4], b'\xff')
        self.assertEqual(mem[0x7ffff7ffe0b5], b'\x7f')
        self.assertEqual(mem[0x7ffff7ffe0b6], b'\x00')
        self.assertEqual(mem[0x7ffff7ffe0b7], b'\x00')
        self.assertEqual(cpu.RDI, 140737353973760)
        self.assertEqual(cpu.RIP, 140737351985194)

    def test_CMOVE_5(self):
        ''' Instruction CMOVE_5
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = False
        cpu.R8 = 0x7ffff7ff7c48
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6260], b'D')
        self.assertEqual(mem[0x7ffff7de6261], b'\xc0')
        self.assertEqual(mem[0x7ffff7de625e], b'L')
        self.assertEqual(mem[0x7ffff7de625f], b'\x0f')
        self.assertEqual(cpu.R8, 140737354103880)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 140737351934562)

    def test_CMOVE_6(self):
        ''' Instruction CMOVE_6
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = False
        cpu.R8 = 0x7ffff7ff7c48
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6260], b'D')
        self.assertEqual(mem[0x7ffff7de6261], b'\xc0')
        self.assertEqual(mem[0x7ffff7de625e], b'L')
        self.assertEqual(mem[0x7ffff7de625f], b'\x0f')
        self.assertEqual(cpu.R8, 140737354103880)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 140737351934562)

    def test_CMOVNE_1(self):
        ''' Instruction CMOVNE_1
            Groups: cmov
            0x462435:	cmovne	rbx, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00462000, 0x1000, 'rwx')
        mem[0x00462438] = '\xd8'
        mem[0x00462435] = 'H'
        mem[0x00462436] = '\x0f'
        mem[0x00462437] = 'E'
        cpu.ZF = True
        cpu.RIP = 0x462435
        cpu.RAX = 0x4a5441
        cpu.RBX = 0x6bf6b0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x462438], b'\xd8')
        self.assertEqual(mem[0x462435], b'H')
        self.assertEqual(mem[0x462436], b'\x0f')
        self.assertEqual(mem[0x462437], b'E')
        self.assertEqual(cpu.RAX, 4871233)
        self.assertEqual(cpu.RIP, 4596793)
        self.assertEqual(cpu.RBX, 7075504)

    def test_CMOVNE_2(self):
        ''' Instruction CMOVNE_2
            Groups: cmov
            0x7ffff7de5776:	cmovne	r14d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5778] = 'E'
        mem[0x7ffff7de5779] = '\xf0'
        mem[0x7ffff7de5776] = 'D'
        mem[0x7ffff7de5777] = '\x0f'
        cpu.EAX = 0x10
        cpu.ZF = True
        cpu.R14D = 0x0
        cpu.RIP = 0x7ffff7de5776
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5778], b'E')
        self.assertEqual(mem[0x7ffff7de5779], b'\xf0')
        self.assertEqual(mem[0x7ffff7de5776], b'D')
        self.assertEqual(mem[0x7ffff7de5777], b'\x0f')
        self.assertEqual(cpu.EAX, 16)
        self.assertEqual(cpu.R14D, 0)
        self.assertEqual(cpu.RIP, 140737351931770)

    def test_CMOVNE_3(self):
        ''' Instruction CMOVNE_3
            Groups: cmov
            0x7ffff7de57f6:	cmovne	rbx, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de57f8] = 'E'
        mem[0x7ffff7de57f9] = '\xd8'
        mem[0x7ffff7de57f6] = 'H'
        mem[0x7ffff7de57f7] = '\x0f'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de57f6
        cpu.RAX = 0x7ffff7ff7640
        cpu.RBX = 0x7ffff7ff7af1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de57f8], b'E')
        self.assertEqual(mem[0x7ffff7de57f9], b'\xd8')
        self.assertEqual(mem[0x7ffff7de57f6], b'H')
        self.assertEqual(mem[0x7ffff7de57f7], b'\x0f')
        self.assertEqual(cpu.RAX, 140737354102336)
        self.assertEqual(cpu.RIP, 140737351931898)
        self.assertEqual(cpu.RBX, 140737354102336)

    def test_CMOVNE_4(self):
        ''' Instruction CMOVNE_4
            Groups: cmov
            0x457ba4:	cmovne	rsi, rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457ba4] = 'H'
        mem[0x00457ba5] = '\x0f'
        mem[0x00457ba6] = 'E'
        mem[0x00457ba7] = '\xf2'
        cpu.ZF = False
        cpu.RSI = 0x8201000080201021
        cpu.RIP = 0x457ba4
        cpu.RDX = 0x41008000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457ba4], b'H')
        self.assertEqual(mem[0x457ba5], b'\x0f')
        self.assertEqual(mem[0x457ba6], b'E')
        self.assertEqual(mem[0x457ba7], b'\xf2')
        self.assertEqual(cpu.RSI, 1090551808)
        self.assertEqual(cpu.RIP, 4553640)
        self.assertEqual(cpu.RDX, 1090551808)

    def test_CMOVNE_5(self):
        ''' Instruction CMOVNE_5
            Groups: cmov
            0x7ffff7de0910:	cmovne	esi, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de0000, 0x1000, 'rwx')
        mem[0x7ffff7de0910] = '\x0f'
        mem[0x7ffff7de0911] = 'E'
        mem[0x7ffff7de0912] = '\xf0'
        cpu.EAX = 0x1
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de0910
        cpu.ESI = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de0910], b'\x0f')
        self.assertEqual(mem[0x7ffff7de0911], b'E')
        self.assertEqual(mem[0x7ffff7de0912], b'\xf0')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.ESI, 1)
        self.assertEqual(cpu.RIP, 140737351911699)

    def test_CMOVNE_6(self):
        ''' Instruction CMOVNE_6
            Groups: cmov
            0x457db0:	cmovne	rcx, rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457db0] = 'H'
        mem[0x00457db1] = '\x0f'
        mem[0x00457db2] = 'E'
        mem[0x00457db3] = '\xcf'
        cpu.RCX = 0x7fffffffe01b
        cpu.ZF = False
        cpu.RDI = 0x7fffffffe040
        cpu.RIP = 0x457db0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457db0], b'H')
        self.assertEqual(mem[0x457db1], b'\x0f')
        self.assertEqual(mem[0x457db2], b'E')
        self.assertEqual(mem[0x457db3], b'\xcf')
        self.assertEqual(cpu.RDI, 140737488347200)
        self.assertEqual(cpu.RCX, 140737488347200)
        self.assertEqual(cpu.RIP, 4554164)

    def test_CMOVNS_1(self):
        ''' Instruction CMOVNS_1
            Groups: cmov
            0x448555:	cmovns	rax, r11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00448000, 0x1000, 'rwx')
        mem[0x00448558] = '\xc3'
        mem[0x00448555] = 'I'
        mem[0x00448556] = '\x0f'
        mem[0x00448557] = 'I'
        cpu.RIP = 0x448555
        cpu.SF = False
        cpu.RAX = 0x0
        cpu.R11 = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x448558], b'\xc3')
        self.assertEqual(mem[0x448555], b'I')
        self.assertEqual(mem[0x448556], b'\x0f')
        self.assertEqual(mem[0x448557], b'I')
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 4490585)
        self.assertEqual(cpu.R11, 0)

    def test_CMOVNS_2(self):
        ''' Instruction CMOVNS_2
            Groups: cmov
            0x448555:	cmovns	rax, r11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00448000, 0x1000, 'rwx')
        mem[0x00448558] = '\xc3'
        mem[0x00448555] = 'I'
        mem[0x00448556] = '\x0f'
        mem[0x00448557] = 'I'
        cpu.RIP = 0x448555
        cpu.SF = False
        cpu.RAX = 0x0
        cpu.R11 = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x448558], b'\xc3')
        self.assertEqual(mem[0x448555], b'I')
        self.assertEqual(mem[0x448556], b'\x0f')
        self.assertEqual(mem[0x448557], b'I')
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 4490585)
        self.assertEqual(cpu.R11, 0)

    def test_CMPSB_1(self):
        ''' Instruction CMPSB_1
            Groups:
            0x40065b:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda80] = 'Z'
        mem[0x7fffffffda81] = '\xed'
        mem[0x7fffffffda82] = '\xcf'
        mem[0x7fffffffda83] = '\xc2'
        mem[0x00491604] = 'Z'
        mem[0x00491605] = 'A'
        mem[0x00491606] = 'R'
        mem[0x00491607] = 'A'
        mem[0x00491608] = 'Z'
        mem[0x00491609] = 'A'
        mem[0x0049160a] = '\x00'
        mem[0x0049160b] = 'M'
        mem[0x7fffffffda87] = '\xff'
        mem[0x7fffffffda86] = '\x94'
        mem[0x7fffffffda84] = '\xc0'
        mem[0x0040065b] = '\xf3'
        mem[0x0040065c] = '\xa6'
        mem[0x7fffffffda85] = '\xe0'
        cpu.RDI = 0x491604
        cpu.RCX = 0x7
        cpu.RSI = 0x7fffffffda80
        cpu.RIP = 0x40065b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda80], b'Z')
        self.assertEqual(mem[0x7fffffffda81], b'\xed')
        self.assertEqual(mem[0x7fffffffda82], b'\xcf')
        self.assertEqual(mem[0x7fffffffda83], b'\xc2')
        self.assertEqual(mem[0x491604], b'Z')
        self.assertEqual(mem[0x491605], b'A')
        self.assertEqual(mem[0x491606], b'R')
        self.assertEqual(mem[0x491607], b'A')
        self.assertEqual(mem[0x491608], b'Z')
        self.assertEqual(mem[0x491609], b'A')
        self.assertEqual(mem[0x49160a], b'\x00')
        self.assertEqual(mem[0x49160b], b'M')
        self.assertEqual(mem[0x7fffffffda87], b'\xff')
        self.assertEqual(mem[0x7fffffffda86], b'\x94')
        self.assertEqual(mem[0x7fffffffda84], b'\xc0')
        self.assertEqual(mem[0x40065b], b'\xf3')
        self.assertEqual(mem[0x40065c], b'\xa6')
        self.assertEqual(mem[0x7fffffffda85], b'\xe0')
        self.assertEqual(cpu.RCX, 6)
        self.assertEqual(cpu.RDI, 4789765)
        self.assertEqual(cpu.RSI, 140737488345729)
        self.assertEqual(cpu.RIP, 4195931)

    def test_CMPSB_2(self):
        ''' Instruction CMPSB_2
            Groups:
            0x400657:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        mem[0x00400658] = '\xa6'
        mem[0x7fffffffe06a] = 'a'
        mem[0x7fffffffe06b] = 'r'
        mem[0x7fffffffe06c] = 'g'
        mem[0x7fffffffe06d] = '1'
        mem[0x7fffffffe06e] = '\x00'
        mem[0x7fffffffe06f] = 'a'
        mem[0x7fffffffe070] = 'r'
        mem[0x7fffffffe071] = 'g'
        mem[0x00400657] = '\xf3'
        mem[0x00491818] = '-'
        mem[0x00491819] = 'd'
        mem[0x0049181a] = 'o'
        mem[0x0049181b] = 's'
        mem[0x0049181c] = 't'
        mem[0x0049181d] = 'u'
        mem[0x0049181e] = 'f'
        mem[0x00491817] = '-'
        cpu.RDI = 0x491817
        cpu.RCX = 0xa
        cpu.RSI = 0x7fffffffe06a
        cpu.RIP = 0x400657
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffe06b], b'r')
        self.assertEqual(mem[0x7fffffffe071], b'g')
        self.assertEqual(mem[0x7fffffffe06a], b'a')
        self.assertEqual(mem[0x400657], b'\xf3')
        self.assertEqual(mem[0x7fffffffe06c], b'g')
        self.assertEqual(mem[0x7fffffffe06d], b'1')
        self.assertEqual(mem[0x7fffffffe06e], b'\x00')
        self.assertEqual(mem[0x7fffffffe06f], b'a')
        self.assertEqual(mem[0x7fffffffe070], b'r')
        self.assertEqual(mem[0x491818], b'-')
        self.assertEqual(mem[0x491817], b'-')
        self.assertEqual(mem[0x400658], b'\xa6')
        self.assertEqual(mem[0x491819], b'd')
        self.assertEqual(mem[0x49181a], b'o')
        self.assertEqual(mem[0x49181b], b's')
        self.assertEqual(mem[0x49181c], b't')
        self.assertEqual(mem[0x49181d], b'u')
        self.assertEqual(mem[0x49181e], b'f')
        self.assertEqual(cpu.RCX, 9)
        self.assertEqual(cpu.RDI, 4790296)
        self.assertEqual(cpu.RSI, 140737488347243)
        self.assertEqual(cpu.RIP, 4195929)

    def test_CMPSB_3(self):
        ''' Instruction CMPSB_3
            Groups:
            0x40065b:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda81] = '\xed'
        mem[0x7fffffffda82] = '\xcf'
        mem[0x7fffffffda83] = '\xc2'
        mem[0x7fffffffda84] = '\xc0'
        mem[0x00491605] = 'A'
        mem[0x00491606] = 'R'
        mem[0x00491607] = 'A'
        mem[0x00491608] = 'Z'
        mem[0x00491609] = 'A'
        mem[0x0049160a] = '\x00'
        mem[0x0049160b] = 'M'
        mem[0x0049160c] = 'e'
        mem[0x7fffffffda86] = '\x94'
        mem[0x7fffffffda88] = '\xea'
        mem[0x7fffffffda87] = '\xff'
        mem[0x0040065b] = '\xf3'
        mem[0x0040065c] = '\xa6'
        mem[0x7fffffffda85] = '\xe0'
        cpu.RDI = 0x491605
        cpu.RCX = 0x6
        cpu.RSI = 0x7fffffffda81
        cpu.RIP = 0x40065b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda81], b'\xed')
        self.assertEqual(mem[0x7fffffffda82], b'\xcf')
        self.assertEqual(mem[0x7fffffffda83], b'\xc2')
        self.assertEqual(mem[0x7fffffffda84], b'\xc0')
        self.assertEqual(mem[0x491605], b'A')
        self.assertEqual(mem[0x491606], b'R')
        self.assertEqual(mem[0x491607], b'A')
        self.assertEqual(mem[0x491608], b'Z')
        self.assertEqual(mem[0x491609], b'A')
        self.assertEqual(mem[0x49160a], b'\x00')
        self.assertEqual(mem[0x49160b], b'M')
        self.assertEqual(mem[0x49160c], b'e')
        self.assertEqual(mem[0x7fffffffda86], b'\x94')
        self.assertEqual(mem[0x7fffffffda88], b'\xea')
        self.assertEqual(mem[0x7fffffffda87], b'\xff')
        self.assertEqual(mem[0x40065b], b'\xf3')
        self.assertEqual(mem[0x40065c], b'\xa6')
        self.assertEqual(mem[0x7fffffffda85], b'\xe0')
        self.assertEqual(cpu.RCX, 5)
        self.assertEqual(cpu.RDI, 4789766)
        self.assertEqual(cpu.RSI, 140737488345730)
        self.assertEqual(cpu.RIP, 4195933)

    def test_CMPSB_4(self):
        ''' Instruction CMPSB_4
            Groups:
            0x400657:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        mem[0x7fffffffe065] = 'a'
        mem[0x7fffffffe066] = 'r'
        mem[0x7fffffffe067] = 'g'
        mem[0x7fffffffe068] = '1'
        mem[0x7fffffffe069] = '\x00'
        mem[0x7fffffffe06a] = 'a'
        mem[0x7fffffffe06b] = 'r'
        mem[0x7fffffffe06c] = 'g'
        mem[0x00400658] = '\xa6'
        mem[0x00400657] = '\xf3'
        mem[0x00491818] = '-'
        mem[0x00491819] = 'd'
        mem[0x0049181a] = 'o'
        mem[0x0049181b] = 's'
        mem[0x0049181c] = 't'
        mem[0x0049181d] = 'u'
        mem[0x0049181e] = 'f'
        mem[0x00491817] = '-'
        cpu.RDI = 0x491817
        cpu.RCX = 0xa
        cpu.RSI = 0x7fffffffe065
        cpu.RIP = 0x400657
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffe06b], b'r')
        self.assertEqual(mem[0x7fffffffe065], b'a')
        self.assertEqual(mem[0x7fffffffe066], b'r')
        self.assertEqual(mem[0x7fffffffe067], b'g')
        self.assertEqual(mem[0x7fffffffe068], b'1')
        self.assertEqual(mem[0x7fffffffe069], b'\x00')
        self.assertEqual(mem[0x7fffffffe06a], b'a')
        self.assertEqual(mem[0x400657], b'\xf3')
        self.assertEqual(mem[0x7fffffffe06c], b'g')
        self.assertEqual(mem[0x491818], b'-')
        self.assertEqual(mem[0x491817], b'-')
        self.assertEqual(mem[0x400658], b'\xa6')
        self.assertEqual(mem[0x491819], b'd')
        self.assertEqual(mem[0x49181a], b'o')
        self.assertEqual(mem[0x49181b], b's')
        self.assertEqual(mem[0x49181c], b't')
        self.assertEqual(mem[0x49181d], b'u')
        self.assertEqual(mem[0x49181e], b'f')
        self.assertEqual(cpu.RCX, 9)
        self.assertEqual(cpu.RDI, 4790296)
        self.assertEqual(cpu.RSI, 140737488347238)
        self.assertEqual(cpu.RIP, 4195929)

    def test_CMPSB_5(self):
        ''' Instruction CMPSB_5
            Groups:
            0x55555555478b:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda80] = '\xc6'
        mem[0x7fffffffda81] = '\xd9'
        mem[0x7fffffffda82] = 'P'
        mem[0x7fffffffda83] = '%'
        mem[0x7fffffffda84] = '\xc1'
        mem[0x7fffffffda85] = '\xe2'
        mem[0x7fffffffda86] = '\xc9'
        mem[0x7fffffffda87] = '\x7f'
        mem[0x55555555478b] = '\xf3'
        mem[0x55555555478c] = '\xa6'
        mem[0x555555554998] = 'Z'
        mem[0x555555554999] = 'A'
        mem[0x55555555499a] = 'R'
        mem[0x55555555499b] = 'A'
        mem[0x55555555499c] = 'Z'
        mem[0x55555555499d] = 'A'
        mem[0x55555555499e] = '\x00'
        mem[0x55555555499f] = 'M'
        cpu.RDI = 0x555555554998
        cpu.RCX = 0x7
        cpu.RSI = 0x7fffffffda80
        cpu.RIP = 0x55555555478b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda80], b'\xc6')
        self.assertEqual(mem[0x7fffffffda81], b'\xd9')
        self.assertEqual(mem[0x7fffffffda82], b'P')
        self.assertEqual(mem[0x7fffffffda83], b'%')
        self.assertEqual(mem[0x7fffffffda84], b'\xc1')
        self.assertEqual(mem[0x7fffffffda85], b'\xe2')
        self.assertEqual(mem[0x7fffffffda86], b'\xc9')
        self.assertEqual(mem[0x7fffffffda87], b'\x7f')
        self.assertEqual(mem[0x55555555478b], b'\xf3')
        self.assertEqual(mem[0x55555555478c], b'\xa6')
        self.assertEqual(mem[0x555555554998], b'Z')
        self.assertEqual(mem[0x555555554999], b'A')
        self.assertEqual(mem[0x55555555499a], b'R')
        self.assertEqual(mem[0x55555555499b], b'A')
        self.assertEqual(mem[0x55555555499c], b'Z')
        self.assertEqual(mem[0x55555555499d], b'A')
        self.assertEqual(mem[0x55555555499e], b'\x00')
        self.assertEqual(mem[0x55555555499f], b'M')
        self.assertEqual(cpu.RCX, 6)
        self.assertEqual(cpu.RDI, 93824992233881)
        self.assertEqual(cpu.RSI, 140737488345729)
        self.assertEqual(cpu.RIP, 93824992233357)

    def test_CMPSB_6(self):
        ''' Instruction CMPSB_6
            Groups:
            0x5555555548c0:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x5555555548c0] = '\xf3'
        mem[0x5555555548c1] = '\xa6'
        mem[0x7fffffffda82] = '\xd2'
        mem[0x7fffffffda83] = '\xd0'
        mem[0x7fffffffda84] = '\x1f'
        mem[0x7fffffffda85] = '\x1c'
        mem[0x7fffffffda86] = '('
        mem[0x7fffffffda81] = '\x04'
        mem[0x5555555549a8] = 'Z'
        mem[0x5555555549a9] = 'A'
        mem[0x5555555549aa] = 'R'
        mem[0x5555555549ab] = 'A'
        mem[0x5555555549ac] = 'Z'
        mem[0x5555555549ad] = 'A'
        mem[0x5555555549ae] = '\x00'
        mem[0x5555555549af] = 'M'
        mem[0x7fffffffda87] = 'P'
        mem[0x7fffffffda80] = '\x91'
        cpu.RDI = 0x5555555549a8
        cpu.RCX = 0x7
        cpu.RSI = 0x7fffffffda80
        cpu.RIP = 0x5555555548c0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5555555548c0], b'\xf3')
        self.assertEqual(mem[0x5555555548c1], b'\xa6')
        self.assertEqual(mem[0x7fffffffda82], b'\xd2')
        self.assertEqual(mem[0x7fffffffda83], b'\xd0')
        self.assertEqual(mem[0x7fffffffda84], b'\x1f')
        self.assertEqual(mem[0x7fffffffda85], b'\x1c')
        self.assertEqual(mem[0x7fffffffda86], b'(')
        self.assertEqual(mem[0x7fffffffda81], b'\x04')
        self.assertEqual(mem[0x5555555549a8], b'Z')
        self.assertEqual(mem[0x5555555549a9], b'A')
        self.assertEqual(mem[0x5555555549aa], b'R')
        self.assertEqual(mem[0x7fffffffda87], b'P')
        self.assertEqual(mem[0x5555555549ac], b'Z')
        self.assertEqual(mem[0x5555555549ad], b'A')
        self.assertEqual(mem[0x5555555549ae], b'\x00')
        self.assertEqual(mem[0x5555555549af], b'M')
        self.assertEqual(mem[0x7fffffffda80], b'\x91')
        self.assertEqual(mem[0x5555555549ab], b'A')
        self.assertEqual(cpu.RCX, 6)
        self.assertEqual(cpu.RDI, 93824992233897)
        self.assertEqual(cpu.RSI, 140737488345729)
        self.assertEqual(cpu.RIP, 93824992233666)

    def test_CMPXCHG8B_1(self):
        ''' Instruction CMPXCHG8B_1
            Groups:
            0x5c68cb:	lock cmpxchg8b	qword ptr [rsp + 4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x005c6000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x005c68cb] = '\xf0'
        mem[0x005c68cc] = '\x0f'
        mem[0x005c68cd] = '\xc7'
        mem[0x005c68ce] = 'L'
        mem[0x005c68cf] = '$'
        mem[0x005c68d0] = '\x04'
        mem[0x7fffffffccb4] = '\x80'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = '\x01'
        mem[0x7fffffffccb9] = '\x80'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        cpu.EBX = 0x80000001
        cpu.RIP = 0x5c68cb
        cpu.EAX = 0x80000001
        cpu.EDX = 0x8001
        cpu.RSP = 0x7fffffffccb0
        cpu.ECX = 0x80
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5c68cb], b'\xf0')
        self.assertEqual(mem[0x5c68cc], b'\x0f')
        self.assertEqual(mem[0x5c68cd], b'\xc7')
        self.assertEqual(mem[0x5c68ce], b'L')
        self.assertEqual(mem[0x5c68cf], b'$')
        self.assertEqual(mem[0x5c68d0], b'\x04')
        self.assertEqual(mem[0x7fffffffccb4], b'\x80')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'\x01')
        self.assertEqual(mem[0x7fffffffccb9], b'\x80')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 6056145)
        self.assertEqual(cpu.EAX, 128)
        self.assertEqual(cpu.EDX, 32769)
        self.assertEqual(cpu.EBX, 2147483649)
        self.assertEqual(cpu.ECX, 128)

    def test_CMPXCHG8B_2(self):
        ''' Instruction CMPXCHG8B_2
            Groups:
            0x5861a9:	lock cmpxchg8b	qword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00586000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x005861a9] = '\xf0'
        mem[0x005861aa] = '\x0f'
        mem[0x005861ab] = '\xc7'
        mem[0x005861ac] = '\x0c'
        mem[0x005861ad] = '$'
        mem[0x7fffffffccb0] = '\x00'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x80'
        mem[0x7fffffffccb4] = '\x00'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x80'
        cpu.EBX = 0x80000000
        cpu.RIP = 0x5861a9
        cpu.EAX = 0x80000000
        cpu.EDX = 0xffffffff
        cpu.RSP = 0x7fffffffccb0
        cpu.ECX = 0x80000000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5861a9], b'\xf0')
        self.assertEqual(mem[0x5861aa], b'\x0f')
        self.assertEqual(mem[0x5861ab], b'\xc7')
        self.assertEqual(mem[0x5861ac], b'\x0c')
        self.assertEqual(mem[0x5861ad], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'\x00')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x80')
        self.assertEqual(mem[0x7fffffffccb4], b'\x00')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x80')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5792174)
        self.assertEqual(cpu.EAX, 2147483648)
        self.assertEqual(cpu.EDX, 2147483648)
        self.assertEqual(cpu.EBX, 2147483648)
        self.assertEqual(cpu.ECX, 2147483648)

    def test_CMPXCHG8B_3(self):
        ''' Instruction CMPXCHG8B_3
            Groups:
            0x58de05:	lock cmpxchg8b	qword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0058d000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x0058de05] = '\xf0'
        mem[0x0058de06] = '\x0f'
        mem[0x0058de07] = '\xc7'
        mem[0x0058de08] = '\x0c'
        mem[0x0058de09] = '$'
        mem[0x7fffffffccb0] = '\x01'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x80'
        mem[0x7fffffffccb4] = '@'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        cpu.EBX = 0x80000001
        cpu.RIP = 0x58de05
        cpu.EAX = 0x80000001
        cpu.EDX = 0x21
        cpu.RSP = 0x7fffffffccb0
        cpu.ECX = 0x40
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x58de05], b'\xf0')
        self.assertEqual(mem[0x58de06], b'\x0f')
        self.assertEqual(mem[0x58de07], b'\xc7')
        self.assertEqual(mem[0x58de08], b'\x0c')
        self.assertEqual(mem[0x58de09], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'\x01')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x80')
        self.assertEqual(mem[0x7fffffffccb4], b'@')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5824010)
        self.assertEqual(cpu.EAX, 2147483649)
        self.assertEqual(cpu.EDX, 64)
        self.assertEqual(cpu.EBX, 2147483649)
        self.assertEqual(cpu.ECX, 64)

    def test_CMPXCHG8B_4(self):
        ''' Instruction CMPXCHG8B_4
            Groups:
            0x59b473:	lock cmpxchg8b	qword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0059b000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x0059b476] = '\x0c'
        mem[0x0059b477] = '$'
        mem[0x0059b473] = '\xf0'
        mem[0x7fffffffccb0] = '\xff'
        mem[0x7fffffffccb1] = '\xff'
        mem[0x7fffffffccb2] = '\xff'
        mem[0x7fffffffccb3] = '\xff'
        mem[0x0059b474] = '\x0f'
        mem[0x0059b475] = '\xc7'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb4] = '\x80'
        mem[0x7fffffffccb5] = '\x00'
        cpu.EBX = 0xffffffff
        cpu.RIP = 0x59b473
        cpu.EAX = 0xffffffff
        cpu.EDX = 0x80
        cpu.RSP = 0x7fffffffccb0
        cpu.ECX = 0x80
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\xff')
        self.assertEqual(mem[0x7fffffffccb0], b'\xff')
        self.assertEqual(mem[0x7fffffffccb1], b'\xff')
        self.assertEqual(mem[0x7fffffffccb2], b'\xff')
        self.assertEqual(mem[0x59b473], b'\xf0')
        self.assertEqual(mem[0x59b474], b'\x0f')
        self.assertEqual(mem[0x59b475], b'\xc7')
        self.assertEqual(mem[0x59b476], b'\x0c')
        self.assertEqual(mem[0x59b477], b'$')
        self.assertEqual(mem[0x7fffffffccb4], b'\x80')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5878904)
        self.assertEqual(cpu.EAX, 4294967295)
        self.assertEqual(cpu.EDX, 128)
        self.assertEqual(cpu.EBX, 4294967295)
        self.assertEqual(cpu.ECX, 128)

    def test_CMPXCHG8B_5(self):
        ''' Instruction CMPXCHG8B_5
            Groups:
            0x624e14:	lock cmpxchg8b	qword ptr [rsp + 8]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00624000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x00624e14] = '\xf0'
        mem[0x00624e15] = '\x0f'
        mem[0x00624e16] = '\xc7'
        mem[0x00624e17] = 'L'
        mem[0x00624e18] = '$'
        mem[0x00624e19] = '\x08'
        mem[0x7fffffffccb8] = '\x00'
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x80'
        mem[0x7fffffffccbc] = '@'
        mem[0x7fffffffccbd] = '\x00'
        mem[0x7fffffffccbe] = '\x00'
        mem[0x7fffffffccbf] = '\x00'
        cpu.EBX = 0x40
        cpu.RIP = 0x624e14
        cpu.EAX = 0x40
        cpu.EDX = 0x80000000
        cpu.RSP = 0x7fffffffccb0
        cpu.ECX = 0x8001
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x624e14], b'\xf0')
        self.assertEqual(mem[0x624e15], b'\x0f')
        self.assertEqual(mem[0x624e16], b'\xc7')
        self.assertEqual(mem[0x624e17], b'L')
        self.assertEqual(mem[0x624e18], b'$')
        self.assertEqual(mem[0x624e19], b'\x08')
        self.assertEqual(mem[0x7fffffffccb8], b'\x00')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x80')
        self.assertEqual(mem[0x7fffffffccbc], b'@')
        self.assertEqual(mem[0x7fffffffccbd], b'\x00')
        self.assertEqual(mem[0x7fffffffccbe], b'\x00')
        self.assertEqual(mem[0x7fffffffccbf], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 6442522)
        self.assertEqual(cpu.EAX, 2147483648)
        self.assertEqual(cpu.EDX, 64)
        self.assertEqual(cpu.EBX, 64)
        self.assertEqual(cpu.ECX, 32769)

    def test_CMPXCHG8B_6(self):
        ''' Instruction CMPXCHG8B_6
            Groups:
            0x5bfa73:	lock cmpxchg8b	qword ptr [rsp + 4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x005bf000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffccb4] = '\x01'
        mem[0x005bfa76] = 'L'
        mem[0x005bfa77] = '$'
        mem[0x7fffffffccb8] = '\x7f'
        mem[0x005bfa73] = '\xf0'
        mem[0x005bfa74] = '\x0f'
        mem[0x005bfa75] = '\xc7'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x005bfa78] = '\x04'
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        mem[0x7fffffffccb5] = '\x80'
        cpu.EBX = 0x80000000
        cpu.RIP = 0x5bfa73
        cpu.EAX = 0x80000000
        cpu.EDX = 0x7f
        cpu.RSP = 0x7fffffffccb0
        cpu.ECX = 0x8001
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x5bfa78], b'\x04')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x5bfa73], b'\xf0')
        self.assertEqual(mem[0x7fffffffccb4], b'\x01')
        self.assertEqual(mem[0x5bfa75], b'\xc7')
        self.assertEqual(mem[0x5bfa76], b'L')
        self.assertEqual(mem[0x5bfa77], b'$')
        self.assertEqual(mem[0x7fffffffccb8], b'\x7f')
        self.assertEqual(mem[0x5bfa74], b'\x0f')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(mem[0x7fffffffccb5], b'\x80')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 6027897)
        self.assertEqual(cpu.EAX, 32769)
        self.assertEqual(cpu.EDX, 127)
        self.assertEqual(cpu.EBX, 2147483648)
        self.assertEqual(cpu.ECX, 32769)

    def test_CMPXCHG_1(self):
        ''' Instruction CMPXCHG_1
            Groups:
            0x7ffff7a65367:	cmpxchg	dword ptr [rip + 0x36fde2], esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a65000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd5000, 0x1000, 'rwx')
        mem[0x7ffff7dd5150] = '\x00'
        mem[0x7ffff7dd5151] = '\x00'
        mem[0x7ffff7dd5152] = '\x00'
        mem[0x7ffff7dd5153] = '\x00'
        mem[0x7ffff7a65367] = '\x0f'
        mem[0x7ffff7a65368] = '\xb1'
        mem[0x7ffff7a65369] = '5'
        mem[0x7ffff7a6536a] = '\xe2'
        mem[0x7ffff7a6536b] = '\xfd'
        mem[0x7ffff7a6536c] = '6'
        mem[0x7ffff7a6536d] = '\x00'
        cpu.PF = True
        cpu.ESI = 0x1
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RAX = 0x0
        cpu.CF = False
        cpu.RIP = 0x7ffff7a65367
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7dd5150], b'\x01')
        self.assertEqual(mem[0x7ffff7dd5151], b'\x00')
        self.assertEqual(mem[0x7ffff7dd5152], b'\x00')
        self.assertEqual(mem[0x7ffff7dd5153], b'\x00')
        self.assertEqual(mem[0x7ffff7a65367], b'\x0f')
        self.assertEqual(mem[0x7ffff7a65368], b'\xb1')
        self.assertEqual(mem[0x7ffff7a65369], b'5')
        self.assertEqual(mem[0x7ffff7a6536a], b'\xe2')
        self.assertEqual(mem[0x7ffff7a6536b], b'\xfd')
        self.assertEqual(mem[0x7ffff7a6536c], b'6')
        self.assertEqual(mem[0x7ffff7a6536d], b'\x00')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.ESI, 1)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737348260718)
        self.assertEqual(cpu.SF, False)

    def test_CMPXCHG_2(self):
        ''' Instruction CMPXCHG_2
            Groups:
            0x40abbf:	cmpxchg	dword ptr [rdx], esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040a000, 0x1000, 'rwx')
        mem.mmap(0x006be000, 0x1000, 'rwx')
        mem[0x0040abc0] = '\xb1'
        mem[0x0040abc1] = '2'
        mem[0x006be762] = '\x00'
        mem[0x006be763] = '\x00'
        mem[0x006be761] = '\x00'
        mem[0x006be760] = '\x00'
        mem[0x0040abbf] = '\x0f'
        cpu.SF = False
        cpu.PF = True
        cpu.ESI = 0x1
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RAX = 0x0
        cpu.CF = False
        cpu.RIP = 0x40abbf
        cpu.RDX = 0x6be760
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40abc0], b'\xb1')
        self.assertEqual(mem[0x40abc1], b'2')
        self.assertEqual(mem[0x6be762], b'\x00')
        self.assertEqual(mem[0x6be763], b'\x00')
        self.assertEqual(mem[0x6be761], b'\x00')
        self.assertEqual(mem[0x40abbf], b'\x0f')
        self.assertEqual(mem[0x6be760], b'\x01')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.ESI, 1)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4238274)
        self.assertEqual(cpu.RDX, 7071584)

    def test_CMPXCHG_3(self):
        ''' Instruction CMPXCHG_3
            Groups:
            0x413646:	cmpxchg	dword ptr [rbx], esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00413000, 0x1000, 'rwx')
        mem.mmap(0x006b9000, 0x1000, 'rwx')
        mem[0x006b9840] = '\x00'
        mem[0x006b9841] = '\x00'
        mem[0x006b9842] = '\x00'
        mem[0x006b9843] = '\x00'
        mem[0x00413646] = '\x0f'
        mem[0x00413647] = '\xb1'
        mem[0x00413648] = '3'
        cpu.PF = True
        cpu.ESI = 0x1
        cpu.RAX = 0x0
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RBX = 0x6b9840
        cpu.CF = False
        cpu.RIP = 0x413646
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x6b9840], b'\x01')
        self.assertEqual(mem[0x6b9841], b'\x00')
        self.assertEqual(mem[0x6b9842], b'\x00')
        self.assertEqual(mem[0x6b9843], b'\x00')
        self.assertEqual(mem[0x413646], b'\x0f')
        self.assertEqual(mem[0x413647], b'\xb1')
        self.assertEqual(mem[0x413648], b'3')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.ESI, 1)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.RBX, 7051328)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4273737)
        self.assertEqual(cpu.SF, False)

    def test_CMPXCHG_4(self):
        ''' Instruction CMPXCHG_4
            Groups:
            0x435a25:	cmpxchg	qword ptr [rdx], rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00435000, 0x1000, 'rwx')
        mem.mmap(0x006bd000, 0x1000, 'rwx')
        mem[0x006bd380] = '\x00'
        mem[0x006bd381] = '\x00'
        mem[0x006bd382] = '\x00'
        mem[0x006bd383] = '\x00'
        mem[0x006bd384] = '\x00'
        mem[0x006bd385] = '\x00'
        mem[0x006bd386] = '\x00'
        mem[0x006bd387] = '\x00'
        mem[0x00435a25] = 'H'
        mem[0x00435a26] = '\x0f'
        mem[0x00435a27] = '\xb1'
        mem[0x00435a28] = ':'
        cpu.SF = False
        cpu.PF = True
        cpu.RAX = 0x0
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RDI = 0x6bb7c0
        cpu.CF = False
        cpu.RIP = 0x435a25
        cpu.RDX = 0x6bd380
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x6bd380], b'\xc0')
        self.assertEqual(mem[0x6bd381], b'\xb7')
        self.assertEqual(mem[0x6bd382], b'k')
        self.assertEqual(mem[0x6bd383], b'\x00')
        self.assertEqual(mem[0x6bd384], b'\x00')
        self.assertEqual(mem[0x6bd385], b'\x00')
        self.assertEqual(mem[0x6bd386], b'\x00')
        self.assertEqual(mem[0x6bd387], b'\x00')
        self.assertEqual(mem[0x435a25], b'H')
        self.assertEqual(mem[0x435a26], b'\x0f')
        self.assertEqual(mem[0x435a27], b'\xb1')
        self.assertEqual(mem[0x435a28], b':')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.RDI, 7059392)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4413993)
        self.assertEqual(cpu.RDX, 7066496)

    def test_CMPXCHG_5(self):
        ''' Instruction CMPXCHG_5
            Groups:
            0x41086e:	cmpxchg	dword ptr [rdx], ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00410000, 0x1000, 'rwx')
        mem.mmap(0x006be000, 0x1000, 'rwx')
        mem[0x006be760] = '\x00'
        mem[0x006be761] = '\x00'
        mem[0x006be762] = '\x00'
        mem[0x006be763] = '\x00'
        mem[0x0041086e] = '\x0f'
        mem[0x0041086f] = '\xb1'
        mem[0x00410870] = '\n'
        cpu.SF = False
        cpu.PF = True
        cpu.RAX = 0x0
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.ECX = 0x1
        cpu.CF = False
        cpu.RIP = 0x41086e
        cpu.RDX = 0x6be760
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x6be760], b'\x01')
        self.assertEqual(mem[0x6be761], b'\x00')
        self.assertEqual(mem[0x6be762], b'\x00')
        self.assertEqual(mem[0x6be763], b'\x00')
        self.assertEqual(mem[0x41086e], b'\x0f')
        self.assertEqual(mem[0x41086f], b'\xb1')
        self.assertEqual(mem[0x410870], b'\n')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.ECX, 1)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4262001)
        self.assertEqual(cpu.RDX, 7071584)

    def test_CMPXCHG_6(self):
        ''' Instruction CMPXCHG_6
            Groups:
            0x7ffff7aafa06:	cmpxchg	dword ptr [rbx], esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aaf000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd3000, 0x1000, 'rwx')
        mem[0x7ffff7dd3b80] = '\x00'
        mem[0x7ffff7dd3b81] = '\x00'
        mem[0x7ffff7dd3b82] = '\x00'
        mem[0x7ffff7dd3b83] = '\x00'
        mem[0x7ffff7aafa06] = '\x0f'
        mem[0x7ffff7aafa07] = '\xb1'
        mem[0x7ffff7aafa08] = '3'
        cpu.PF = True
        cpu.ESI = 0x1
        cpu.RAX = 0x0
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RBX = 0x7ffff7dd3b80
        cpu.CF = False
        cpu.RIP = 0x7ffff7aafa06
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7dd3b80], b'\x01')
        self.assertEqual(mem[0x7ffff7dd3b81], b'\x00')
        self.assertEqual(mem[0x7ffff7dd3b82], b'\x00')
        self.assertEqual(mem[0x7ffff7dd3b83], b'\x00')
        self.assertEqual(mem[0x7ffff7aafa06], b'\x0f')
        self.assertEqual(mem[0x7ffff7aafa07], b'\xb1')
        self.assertEqual(mem[0x7ffff7aafa08], b'3')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.ESI, 1)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.RBX, 140737351859072)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737348565513)
        self.assertEqual(cpu.SF, False)

    def test_CMP_1(self):
        ''' Instruction CMP_1
            Groups:
            0x7ffff7b58f43:	cmp	r12, r9
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f43] = 'M'
        mem[0x7ffff7b58f44] = '9'
        mem[0x7ffff7b58f45] = '\xcc'
        cpu.SF = False
        cpu.PF = True
        cpu.R12 = 0x7ffff7ab0f80
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7b58f43
        cpu.R9 = 0x7ffff7b23c00
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f43], b'M')
        self.assertEqual(mem[0x7ffff7b58f44], b'9')
        self.assertEqual(mem[0x7ffff7b58f45], b'\xcc')
        self.assertEqual(cpu.SF, True)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.R12, 140737348571008)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737349259078)
        self.assertEqual(cpu.R9, 140737349041152)

    def test_CMP_2(self):
        ''' Instruction CMP_2
            Groups:
            0x406e1d:	cmp	r14w, word ptr [rbx]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        mem[0x00406e20] = '3'
        mem[0x7fffffffee69] = 'W'
        mem[0x7fffffffee6a] = 'I'
        mem[0x00406e1d] = 'f'
        mem[0x00406e1e] = 'D'
        mem[0x00406e1f] = ';'
        cpu.R14W = 0x444c
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RBX = 0x7fffffffee69
        cpu.CF = False
        cpu.RIP = 0x406e1d
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x406e20], b'3')
        self.assertEqual(mem[0x7fffffffee69], b'W')
        self.assertEqual(mem[0x7fffffffee6a], b'I')
        self.assertEqual(mem[0x406e1d], b'f')
        self.assertEqual(mem[0x406e1e], b'D')
        self.assertEqual(mem[0x406e1f], b';')
        self.assertEqual(cpu.R14W, 17484)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RBX, 140737488350825)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4222497)
        self.assertEqual(cpu.SF, True)

    def test_CMP_3(self):
        ''' Instruction CMP_3
            Groups:
            0x40d167:	cmp	eax, 0xff
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040d000, 0x1000, 'rwx')
        mem[0x0040d168] = '\xf8'
        mem[0x0040d169] = '\xff'
        mem[0x0040d167] = '\x83'
        cpu.EAX = 0x1
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x40d167
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40d168], b'\xf8')
        self.assertEqual(mem[0x40d169], b'\xff')
        self.assertEqual(mem[0x40d167], b'\x83')
        self.assertEqual(cpu.EAX, 1)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4247914)
        self.assertEqual(cpu.SF, False)

    def test_CMP_4(self):
        ''' Instruction CMP_4
            Groups:
            0x7ffff7de4488:	cmp	qword ptr [rbp - 0x90], 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd9a0] = '\xe0'
        mem[0x7fffffffd9a1] = 'M'
        mem[0x7fffffffd9a2] = '\xa3'
        mem[0x7fffffffd9a3] = '\xf7'
        mem[0x7fffffffd9a4] = '\xff'
        mem[0x7fffffffd9a5] = '\x7f'
        mem[0x7fffffffd9a6] = '\x00'
        mem[0x7fffffffd9a7] = '\x00'
        mem[0x7ffff7de4488] = 'H'
        mem[0x7ffff7de4489] = '\x83'
        mem[0x7ffff7de448a] = '\xbd'
        mem[0x7ffff7de448b] = 'p'
        mem[0x7ffff7de448c] = '\xff'
        mem[0x7ffff7de448d] = '\xff'
        mem[0x7ffff7de448e] = '\xff'
        mem[0x7ffff7de448f] = '\x00'
        cpu.SF = False
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4488
        cpu.RBP = 0x7fffffffda30
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd9a0], b'\xe0')
        self.assertEqual(mem[0x7fffffffd9a1], b'M')
        self.assertEqual(mem[0x7fffffffd9a2], b'\xa3')
        self.assertEqual(mem[0x7fffffffd9a3], b'\xf7')
        self.assertEqual(mem[0x7fffffffd9a4], b'\xff')
        self.assertEqual(mem[0x7fffffffd9a5], b'\x7f')
        self.assertEqual(mem[0x7fffffffd9a6], b'\x00')
        self.assertEqual(mem[0x7fffffffd9a7], b'\x00')
        self.assertEqual(mem[0x7ffff7de4488], b'H')
        self.assertEqual(mem[0x7ffff7de4489], b'\x83')
        self.assertEqual(mem[0x7ffff7de448a], b'\xbd')
        self.assertEqual(mem[0x7ffff7de448b], b'p')
        self.assertEqual(mem[0x7ffff7de448c], b'\xff')
        self.assertEqual(mem[0x7ffff7de448d], b'\xff')
        self.assertEqual(mem[0x7ffff7de448e], b'\xff')
        self.assertEqual(mem[0x7ffff7de448f], b'\x00')
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926928)
        self.assertEqual(cpu.RBP, 140737488345648)

    def test_CMP_5(self):
        ''' Instruction CMP_5
            Groups:
            0x7ffff7de6111:	cmp	rax, 0x26
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6111] = 'H'
        mem[0x7ffff7de6112] = '\x83'
        mem[0x7ffff7de6113] = '\xf8'
        mem[0x7ffff7de6114] = '&'
        cpu.PF = True
        cpu.RAX = 0x8
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6111
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6111], b'H')
        self.assertEqual(mem[0x7ffff7de6112], b'\x83')
        self.assertEqual(mem[0x7ffff7de6113], b'\xf8')
        self.assertEqual(mem[0x7ffff7de6114], b'&')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 8)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351934229)
        self.assertEqual(cpu.SF, True)

    def test_CMP_6(self):
        ''' Instruction CMP_6
            Groups:
            0x7ffff7de620b:	cmp	r12, 0x24
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de620b] = 'I'
        mem[0x7ffff7de620c] = '\x83'
        mem[0x7ffff7de620d] = '\xfc'
        mem[0x7ffff7de620e] = '$'
        cpu.PF = False
        cpu.R12 = 0x6
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de620b
        cpu.SF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de620b], b'I')
        self.assertEqual(mem[0x7ffff7de620c], b'\x83')
        self.assertEqual(mem[0x7ffff7de620d], b'\xfc')
        self.assertEqual(mem[0x7ffff7de620e], b'$')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.R12, 6)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351934479)
        self.assertEqual(cpu.SF, True)

    def test_CQO_1(self):
        ''' Instruction CQO_1
            Groups:
            0x400794:	cqo
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400794] = 'H'
        mem[0x00400795] = '\x99'
        cpu.RIP = 0x400794
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400794], b'H')
        self.assertEqual(mem[0x400795], b'\x99')
        self.assertEqual(cpu.RAX, 6291456)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4196246)

    def test_CQO_2(self):
        ''' Instruction CQO_2
            Groups:
            0x4006d4:	cqo
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x004006d4] = 'H'
        mem[0x004006d5] = '\x99'
        cpu.RIP = 0x4006d4
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4006d4], b'H')
        self.assertEqual(mem[0x4006d5], b'\x99')
        self.assertEqual(cpu.RAX, 6291456)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4196054)

    def test_CQO_3(self):
        ''' Instruction CQO_3
            Groups:
            0x7ffff7a4e234:	cqo
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e234] = 'H'
        mem[0x7ffff7a4e235] = '\x99'
        cpu.RIP = 0x7ffff7a4e234
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4e234], b'H')
        self.assertEqual(mem[0x7ffff7a4e235], b'\x99')
        self.assertEqual(cpu.RAX, 6291456)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348166198)

    def test_CQO_4(self):
        ''' Instruction CQO_4
            Groups:
            0x7ffff7a4e234:	cqo
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e234] = 'H'
        mem[0x7ffff7a4e235] = '\x99'
        cpu.RIP = 0x7ffff7a4e234
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4e234], b'H')
        self.assertEqual(mem[0x7ffff7a4e235], b'\x99')
        self.assertEqual(cpu.RAX, 6291456)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348166198)

    def test_CQO_5(self):
        ''' Instruction CQO_5
            Groups:
            0x4006d4:	cqo
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x004006d4] = 'H'
        mem[0x004006d5] = '\x99'
        cpu.RIP = 0x4006d4
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4006d4], b'H')
        self.assertEqual(mem[0x4006d5], b'\x99')
        self.assertEqual(cpu.RAX, 6291456)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4196054)

    def test_CQO_6(self):
        ''' Instruction CQO_6
            Groups:
            0x7ffff7a4e234:	cqo
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e234] = 'H'
        mem[0x7ffff7a4e235] = '\x99'
        cpu.RIP = 0x7ffff7a4e234
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4e234], b'H')
        self.assertEqual(mem[0x7ffff7a4e235], b'\x99')
        self.assertEqual(cpu.RAX, 6291456)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348166198)

    def test_DEC_1(self):
        ''' Instruction DEC_1
            Groups: mode64
            0x41e10a:	dec	ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0041e000, 0x1000, 'rwx')
        mem[0x0041e10a] = '\xff'
        mem[0x0041e10b] = '\xc9'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x41e10a
        cpu.PF = False
        cpu.SF = False
        cpu.ECX = 0xd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41e10a], b'\xff')
        self.assertEqual(mem[0x41e10b], b'\xc9')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 4317452)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.ECX, 12)

    def test_DEC_2(self):
        ''' Instruction DEC_2
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = True
        cpu.SF = False
        cpu.ECX = 0x4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df462c], b'\xff')
        self.assertEqual(mem[0x7ffff7df462d], b'\xc9')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992878)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.ECX, 3)

    def test_DEC_3(self):
        ''' Instruction DEC_3
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = False
        cpu.SF = False
        cpu.ECX = 0x2
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df462c], b'\xff')
        self.assertEqual(mem[0x7ffff7df462d], b'\xc9')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992878)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.ECX, 1)

    def test_DEC_4(self):
        ''' Instruction DEC_4
            Groups: mode64
            0x7ffff7a65448:	dec	dword ptr [rip + 0x36fd02]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a65000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd5000, 0x1000, 'rwx')
        mem[0x7ffff7dd5150] = '\x01'
        mem[0x7ffff7dd5151] = '\x00'
        mem[0x7ffff7dd5152] = '\x00'
        mem[0x7ffff7dd5153] = '\x00'
        mem[0x7ffff7a65448] = '\xff'
        mem[0x7ffff7a65449] = '\r'
        mem[0x7ffff7a6544a] = '\x02'
        mem[0x7ffff7a6544b] = '\xfd'
        mem[0x7ffff7a6544c] = '6'
        mem[0x7ffff7a6544d] = '\x00'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RIP = 0x7ffff7a65448
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7dd5150], b'\x00')
        self.assertEqual(mem[0x7ffff7dd5151], b'\x00')
        self.assertEqual(mem[0x7ffff7dd5152], b'\x00')
        self.assertEqual(mem[0x7ffff7dd5153], b'\x00')
        self.assertEqual(mem[0x7ffff7a65448], b'\xff')
        self.assertEqual(mem[0x7ffff7a65449], b'\r')
        self.assertEqual(mem[0x7ffff7a6544a], b'\x02')
        self.assertEqual(mem[0x7ffff7a6544b], b'\xfd')
        self.assertEqual(mem[0x7ffff7a6544c], b'6')
        self.assertEqual(mem[0x7ffff7a6544d], b'\x00')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.RIP, 140737348260942)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_DEC_5(self):
        ''' Instruction DEC_5
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = True
        cpu.SF = False
        cpu.ECX = 0x4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df462c], b'\xff')
        self.assertEqual(mem[0x7ffff7df462d], b'\xc9')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992878)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.ECX, 3)

    def test_DEC_6(self):
        ''' Instruction DEC_6
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = False
        cpu.SF = False
        cpu.ECX = 0x1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df462c], b'\xff')
        self.assertEqual(mem[0x7ffff7df462d], b'\xc9')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.RIP, 140737351992878)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.ECX, 0)

    def test_DIV_1(self):
        ''' Instruction DIV_1
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = 0x3f3
        cpu.RDX = 0x0
        cpu.RAX = 0x3de00ec7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3ff8], b'H')
        self.assertEqual(mem[0x7ffff7de3ff9], b'\xf7')
        self.assertEqual(mem[0x7ffff7de3ffa], b'\xf1')
        self.assertEqual(cpu.RAX, 1026799)
        self.assertEqual(cpu.RCX, 1011)
        self.assertEqual(cpu.RDX, 234)
        self.assertEqual(cpu.RIP, 140737351925755)

    def test_DIV_2(self):
        ''' Instruction DIV_2
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = 0x3f3
        cpu.RDX = 0x0
        cpu.RAX = 0x3de00ec7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3ff8], b'H')
        self.assertEqual(mem[0x7ffff7de3ff9], b'\xf7')
        self.assertEqual(mem[0x7ffff7de3ffa], b'\xf1')
        self.assertEqual(cpu.RAX, 1026799)
        self.assertEqual(cpu.RCX, 1011)
        self.assertEqual(cpu.RDX, 234)
        self.assertEqual(cpu.RIP, 140737351925755)

    def test_DIV_3(self):
        ''' Instruction DIV_3
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = 0x3f3
        cpu.RDX = 0x0
        cpu.RAX = 0x9e7650bc
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3ff8], b'H')
        self.assertEqual(mem[0x7ffff7de3ff9], b'\xf7')
        self.assertEqual(mem[0x7ffff7de3ffa], b'\xf1')
        self.assertEqual(cpu.RAX, 2629628)
        self.assertEqual(cpu.RCX, 1011)
        self.assertEqual(cpu.RDX, 136)
        self.assertEqual(cpu.RIP, 140737351925755)

    def test_DIV_4(self):
        ''' Instruction DIV_4
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = 0x3f3
        cpu.RDX = 0x0
        cpu.RAX = 0x10a8b550
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3ff8], b'H')
        self.assertEqual(mem[0x7ffff7de3ff9], b'\xf7')
        self.assertEqual(mem[0x7ffff7de3ffa], b'\xf1')
        self.assertEqual(cpu.RAX, 276450)
        self.assertEqual(cpu.RCX, 1011)
        self.assertEqual(cpu.RDX, 970)
        self.assertEqual(cpu.RIP, 140737351925755)

    def test_DIV_5(self):
        ''' Instruction DIV_5
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = 0x32
        cpu.RDX = 0x0
        cpu.RAX = 0x3cbc6423
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3ff8], b'H')
        self.assertEqual(mem[0x7ffff7de3ff9], b'\xf7')
        self.assertEqual(mem[0x7ffff7de3ffa], b'\xf1')
        self.assertEqual(cpu.RAX, 20379587)
        self.assertEqual(cpu.RCX, 50)
        self.assertEqual(cpu.RDX, 13)
        self.assertEqual(cpu.RIP, 140737351925755)

    def test_DIV_6(self):
        ''' Instruction DIV_6
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = 0x3f3
        cpu.RDX = 0x0
        cpu.RAX = 0x2e8912d8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3ff8], b'H')
        self.assertEqual(mem[0x7ffff7de3ff9], b'\xf7')
        self.assertEqual(mem[0x7ffff7de3ffa], b'\xf1')
        self.assertEqual(cpu.RAX, 772240)
        self.assertEqual(cpu.RCX, 1011)
        self.assertEqual(cpu.RDX, 552)
        self.assertEqual(cpu.RIP, 140737351925755)

    def test_IDIV_1(self):
        ''' Instruction IDIV_1
            Groups:
            0x7ffff7a4e236:	idiv	r8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e238] = '\xf8'
        mem[0x7ffff7a4e236] = 'I'
        mem[0x7ffff7a4e237] = '\xf7'
        cpu.RIP = 0x7ffff7a4e236
        cpu.R8 = 0x8
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4e238], b'\xf8')
        self.assertEqual(mem[0x7ffff7a4e236], b'I')
        self.assertEqual(mem[0x7ffff7a4e237], b'\xf7')
        self.assertEqual(cpu.RAX, 786432)
        self.assertEqual(cpu.R8, 8)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348166201)

    def test_IDIV_2(self):
        ''' Instruction IDIV_2
            Groups:
            0x4006d6:	idiv	r8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x004006d8] = '\xf8'
        mem[0x004006d6] = 'I'
        mem[0x004006d7] = '\xf7'
        cpu.RIP = 0x4006d6
        cpu.R8 = 0x8
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4006d8], b'\xf8')
        self.assertEqual(mem[0x4006d6], b'I')
        self.assertEqual(mem[0x4006d7], b'\xf7')
        self.assertEqual(cpu.RAX, 786432)
        self.assertEqual(cpu.R8, 8)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4196057)

    def test_IDIV_3(self):
        ''' Instruction IDIV_3
            Groups:
            0x7ffff7a4e236:	idiv	r8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e238] = '\xf8'
        mem[0x7ffff7a4e236] = 'I'
        mem[0x7ffff7a4e237] = '\xf7'
        cpu.RIP = 0x7ffff7a4e236
        cpu.R8 = 0x8
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4e238], b'\xf8')
        self.assertEqual(mem[0x7ffff7a4e236], b'I')
        self.assertEqual(mem[0x7ffff7a4e237], b'\xf7')
        self.assertEqual(cpu.RAX, 786432)
        self.assertEqual(cpu.R8, 8)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348166201)

    def test_IDIV_4(self):
        ''' Instruction IDIV_4
            Groups:
            0x4006d6:	idiv	r8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x004006d8] = '\xf8'
        mem[0x004006d6] = 'I'
        mem[0x004006d7] = '\xf7'
        cpu.RIP = 0x4006d6
        cpu.R8 = 0x8
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4006d8], b'\xf8')
        self.assertEqual(mem[0x4006d6], b'I')
        self.assertEqual(mem[0x4006d7], b'\xf7')
        self.assertEqual(cpu.RAX, 786432)
        self.assertEqual(cpu.R8, 8)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4196057)

    def test_IDIV_5(self):
        ''' Instruction IDIV_5
            Groups:
            0x4006d6:	idiv	r8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x004006d8] = '\xf8'
        mem[0x004006d6] = 'I'
        mem[0x004006d7] = '\xf7'
        cpu.RIP = 0x4006d6
        cpu.R8 = 0x8
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4006d8], b'\xf8')
        self.assertEqual(mem[0x4006d6], b'I')
        self.assertEqual(mem[0x4006d7], b'\xf7')
        self.assertEqual(cpu.RAX, 786432)
        self.assertEqual(cpu.R8, 8)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4196057)

    def test_IDIV_6(self):
        ''' Instruction IDIV_6
            Groups:
            0x7ffff7a4e236:	idiv	r8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e238] = '\xf8'
        mem[0x7ffff7a4e236] = 'I'
        mem[0x7ffff7a4e237] = '\xf7'
        cpu.RIP = 0x7ffff7a4e236
        cpu.R8 = 0x8
        cpu.RDX = 0x0
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4e238], b'\xf8')
        self.assertEqual(mem[0x7ffff7a4e236], b'I')
        self.assertEqual(mem[0x7ffff7a4e237], b'\xf7')
        self.assertEqual(cpu.RAX, 786432)
        self.assertEqual(cpu.R8, 8)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348166201)

    def test_IMUL_1(self):
        ''' Instruction IMUL_1
            Groups:
            0x7ffff7acfec4:	imul	eax, edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7acf000, 0x1000, 'rwx')
        mem[0x7ffff7acfec4] = '\x0f'
        mem[0x7ffff7acfec5] = '\xaf'
        mem[0x7ffff7acfec6] = '\xc2'
        cpu.OF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7acfec4
        cpu.RDX = 0x1
        cpu.EAX = 0x600000
        cpu.EDX = 0x1
        cpu.RAX = 0x600000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7acfec4], b'\x0f')
        self.assertEqual(mem[0x7ffff7acfec5], b'\xaf')
        self.assertEqual(mem[0x7ffff7acfec6], b'\xc2')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737348697799)
        self.assertEqual(cpu.RDX, 1)
        self.assertEqual(cpu.EAX, 6291456)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.RAX, 6291456)

    def test_IMUL_2(self):
        ''' Instruction IMUL_2
            Groups:
            0x7ffff7acfeb3:	imul	eax, edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7acf000, 0x1000, 'rwx')
        mem[0x7ffff7acfeb3] = '\x0f'
        mem[0x7ffff7acfeb4] = '\xaf'
        mem[0x7ffff7acfeb5] = '\xc2'
        cpu.OF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7acfeb3
        cpu.RDX = 0x8
        cpu.EAX = 0x40
        cpu.EDX = 0x8
        cpu.RAX = 0x40
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7acfeb3], b'\x0f')
        self.assertEqual(mem[0x7ffff7acfeb4], b'\xaf')
        self.assertEqual(mem[0x7ffff7acfeb5], b'\xc2')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737348697782)
        self.assertEqual(cpu.RDX, 8)
        self.assertEqual(cpu.EAX, 512)
        self.assertEqual(cpu.EDX, 8)
        self.assertEqual(cpu.RAX, 512)

    def test_IMUL_3(self):
        ''' Instruction IMUL_3
            Groups:
            0x43230c:	imul	edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x0043230c] = '\xf7'
        mem[0x0043230d] = '\xea'
        cpu.OF = False
        cpu.CF = False
        cpu.RIP = 0x43230c
        cpu.RDX = 0x55555556
        cpu.EDX = 0x55555556
        cpu.RAX = 0x3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x43230c], b'\xf7')
        self.assertEqual(mem[0x43230d], b'\xea')
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4399886)
        self.assertEqual(cpu.RDX, 1)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.RAX, 2)

    def test_IMUL_4(self):
        ''' Instruction IMUL_4
            Groups:
            0x43230c:	imul	edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x0043230c] = '\xf7'
        mem[0x0043230d] = '\xea'
        cpu.OF = False
        cpu.CF = False
        cpu.RIP = 0x43230c
        cpu.RDX = 0x55555556
        cpu.EDX = 0x55555556
        cpu.RAX = 0x3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x43230c], b'\xf7')
        self.assertEqual(mem[0x43230d], b'\xea')
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4399886)
        self.assertEqual(cpu.RDX, 1)
        self.assertEqual(cpu.EDX, 1)
        self.assertEqual(cpu.RAX, 2)

    def test_IMUL_5(self):
        ''' Instruction IMUL_5
            Groups:
            0x41403c:	imul	r12, rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x0041403c] = 'L'
        mem[0x0041403d] = '\x0f'
        mem[0x0041403e] = '\xaf'
        mem[0x0041403f] = '\xe6'
        cpu.R12 = 0x491
        cpu.RSI = 0x1
        cpu.OF = False
        cpu.RDX = 0x491
        cpu.RIP = 0x41403c
        cpu.CF = False
        cpu.RAX = 0xffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41403c], b'L')
        self.assertEqual(mem[0x41403d], b'\x0f')
        self.assertEqual(mem[0x41403e], b'\xaf')
        self.assertEqual(mem[0x41403f], b'\xe6')
        self.assertEqual(cpu.R12, 1169)
        self.assertEqual(cpu.RSI, 1)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4276288)
        self.assertEqual(cpu.RDX, 1169)
        self.assertEqual(cpu.RAX, 4294967295)

    def test_IMUL_6(self):
        ''' Instruction IMUL_6
            Groups:
            0x413fdc:	imul	r12, rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00413000, 0x1000, 'rwx')
        mem[0x00413fdc] = 'L'
        mem[0x00413fdd] = '\x0f'
        mem[0x00413fde] = '\xaf'
        mem[0x00413fdf] = '\xe6'
        cpu.R12 = 0x491
        cpu.RSI = 0x1
        cpu.OF = False
        cpu.RDX = 0x491
        cpu.RIP = 0x413fdc
        cpu.CF = False
        cpu.RAX = 0xffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x413fdc], b'L')
        self.assertEqual(mem[0x413fdd], b'\x0f')
        self.assertEqual(mem[0x413fde], b'\xaf')
        self.assertEqual(mem[0x413fdf], b'\xe6')
        self.assertEqual(cpu.R12, 1169)
        self.assertEqual(cpu.RSI, 1)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4276192)
        self.assertEqual(cpu.RDX, 1169)
        self.assertEqual(cpu.RAX, 4294967295)

    def test_INC_1(self):
        ''' Instruction INC_1
            Groups:
            0x7ffff7df4596:	inc	rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4598] = '\xc7'
        mem[0x7ffff7df4596] = 'H'
        mem[0x7ffff7df4597] = '\xff'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RIP = 0x7ffff7df4596
        cpu.PF = True
        cpu.RDI = 0x7ffff7a44729
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4598], b'\xc7')
        self.assertEqual(mem[0x7ffff7df4596], b'H')
        self.assertEqual(mem[0x7ffff7df4597], b'\xff')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992729)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.RDI, 140737348126506)
        self.assertEqual(cpu.SF, False)

    def test_INC_2(self):
        ''' Instruction INC_2
            Groups:
            0x7ffff7df4596:	inc	rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4598] = '\xc7'
        mem[0x7ffff7df4596] = 'H'
        mem[0x7ffff7df4597] = '\xff'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RIP = 0x7ffff7df4596
        cpu.PF = True
        cpu.RDI = 0x7ffff7dda5ec
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4598], b'\xc7')
        self.assertEqual(mem[0x7ffff7df4596], b'H')
        self.assertEqual(mem[0x7ffff7df4597], b'\xff')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992729)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RDI, 140737351886317)
        self.assertEqual(cpu.SF, False)

    def test_INC_3(self):
        ''' Instruction INC_3
            Groups:
            0x7ffff7df4599:	inc	rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4599] = 'H'
        mem[0x7ffff7df459a] = '\xff'
        mem[0x7ffff7df459b] = '\xc6'
        cpu.RSI = 0x7ffff7a4472a
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df4599
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4599], b'H')
        self.assertEqual(mem[0x7ffff7df459a], b'\xff')
        self.assertEqual(mem[0x7ffff7df459b], b'\xc6')
        self.assertEqual(cpu.RSI, 140737348126507)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992732)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_INC_4(self):
        ''' Instruction INC_4
            Groups:
            0x7ffff7df4596:	inc	rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4598] = '\xc7'
        mem[0x7ffff7df4596] = 'H'
        mem[0x7ffff7df4597] = '\xff'
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RIP = 0x7ffff7df4596
        cpu.PF = True
        cpu.RDI = 0x7ffff7a4472e
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4598], b'\xc7')
        self.assertEqual(mem[0x7ffff7df4596], b'H')
        self.assertEqual(mem[0x7ffff7df4597], b'\xff')
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992729)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.RDI, 140737348126511)
        self.assertEqual(cpu.SF, False)

    def test_INC_5(self):
        ''' Instruction INC_5
            Groups:
            0x7ffff7df4599:	inc	rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4599] = 'H'
        mem[0x7ffff7df459a] = '\xff'
        mem[0x7ffff7df459b] = '\xc6'
        cpu.RSI = 0x555555554cbb
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df4599
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4599], b'H')
        self.assertEqual(mem[0x7ffff7df459a], b'\xff')
        self.assertEqual(mem[0x7ffff7df459b], b'\xc6')
        self.assertEqual(cpu.RSI, 93824992234684)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992732)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)

    def test_INC_6(self):
        ''' Instruction INC_6
            Groups:
            0x7ffff7df4599:	inc	rsi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4599] = 'H'
        mem[0x7ffff7df459a] = '\xff'
        mem[0x7ffff7df459b] = '\xc6'
        cpu.RSI = 0x7ffff7a44726
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df4599
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4599], b'H')
        self.assertEqual(mem[0x7ffff7df459a], b'\xff')
        self.assertEqual(mem[0x7ffff7df459b], b'\xc6')
        self.assertEqual(cpu.RSI, 140737348126503)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RIP, 140737351992732)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_JAE_1(self):
        ''' Instruction JAE_1
            Groups: jump
            0x7ffff7aa96ab:	jae	0x7ffff7aa96e8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa9000, 0x1000, 'rwx')
        mem[0x7ffff7aa96ab] = 's'
        mem[0x7ffff7aa96ac] = ';'
        cpu.CF = True
        cpu.RIP = 0x7ffff7aa96ab
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7aa96ab], b's')
        self.assertEqual(mem[0x7ffff7aa96ac], b';')
        self.assertEqual(cpu.RIP, 140737348540077)

    def test_JAE_2(self):
        ''' Instruction JAE_2
            Groups: jump
            0x400c11:	jae	0x400c69
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400c11] = 's'
        mem[0x00400c12] = 'V'
        cpu.CF = False
        cpu.RIP = 0x400c11
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400c11], b's')
        self.assertEqual(mem[0x400c12], b'V')
        self.assertEqual(cpu.RIP, 4197481)

    def test_JAE_3(self):
        ''' Instruction JAE_3
            Groups: jump
            0x432400:	jae	0x432440
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432400] = 's'
        mem[0x00432401] = '>'
        cpu.CF = True
        cpu.RIP = 0x432400
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432400], b's')
        self.assertEqual(mem[0x432401], b'>')
        self.assertEqual(cpu.RIP, 4400130)

    def test_JAE_4(self):
        ''' Instruction JAE_4
            Groups: jump
            0x411d5b:	jae	0x412155
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x00411d60] = '\x00'
        mem[0x00411d5b] = '\x0f'
        mem[0x00411d5c] = '\x83'
        mem[0x00411d5d] = '\xf4'
        mem[0x00411d5e] = '\x03'
        mem[0x00411d5f] = '\x00'
        cpu.CF = False
        cpu.RIP = 0x411d5b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x411d60], b'\x00')
        self.assertEqual(mem[0x411d5b], b'\x0f')
        self.assertEqual(mem[0x411d5c], b'\x83')
        self.assertEqual(mem[0x411d5d], b'\xf4')
        self.assertEqual(mem[0x411d5e], b'\x03')
        self.assertEqual(mem[0x411d5f], b'\x00')
        self.assertEqual(cpu.RIP, 4268373)

    def test_JAE_5(self):
        ''' Instruction JAE_5
            Groups: jump
            0x7ffff7b58f5d:	jae	0x7ffff7b58f00
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f5d] = 's'
        mem[0x7ffff7b58f5e] = '\xa1'
        cpu.CF = False
        cpu.RIP = 0x7ffff7b58f5d
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f5d], b's')
        self.assertEqual(mem[0x7ffff7b58f5e], b'\xa1')
        self.assertEqual(cpu.RIP, 140737349259008)

    def test_JAE_6(self):
        ''' Instruction JAE_6
            Groups: jump
            0x400b82:	jae	0x400b9f
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400b82] = 's'
        mem[0x00400b83] = '\x1b'
        cpu.CF = True
        cpu.RIP = 0x400b82
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400b82], b's')
        self.assertEqual(mem[0x400b83], b'\x1b')
        self.assertEqual(cpu.RIP, 4197252)

    def test_JA_1(self):
        ''' Instruction JA_1
            Groups: jump
            0x7ffff7de6132:	ja	0x7ffff7de6108
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6132] = 'w'
        mem[0x7ffff7de6133] = '\xd4'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6132
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6132], b'w')
        self.assertEqual(mem[0x7ffff7de6133], b'\xd4')
        self.assertEqual(cpu.RIP, 140737351934216)

    def test_JA_2(self):
        ''' Instruction JA_2
            Groups: jump
            0x7ffff7ddf066:	ja	0x7ffff7ddf0b2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddf000, 0x1000, 'rwx')
        mem[0x7ffff7ddf066] = 'w'
        mem[0x7ffff7ddf067] = 'J'
        cpu.ZF = False
        cpu.CF = True
        cpu.RIP = 0x7ffff7ddf066
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddf066], b'w')
        self.assertEqual(mem[0x7ffff7ddf067], b'J')
        self.assertEqual(cpu.RIP, 140737351905384)

    def test_JA_3(self):
        ''' Instruction JA_3
            Groups: jump
            0x7ffff7de6132:	ja	0x7ffff7de6108
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6132] = 'w'
        mem[0x7ffff7de6133] = '\xd4'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6132
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6132], b'w')
        self.assertEqual(mem[0x7ffff7de6133], b'\xd4')
        self.assertEqual(cpu.RIP, 140737351934216)

    def test_JA_4(self):
        ''' Instruction JA_4
            Groups: jump
            0x7ffff7de6132:	ja	0x7ffff7de6108
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6132] = 'w'
        mem[0x7ffff7de6133] = '\xd4'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6132
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6132], b'w')
        self.assertEqual(mem[0x7ffff7de6133], b'\xd4')
        self.assertEqual(cpu.RIP, 140737351934216)

    def test_JA_5(self):
        ''' Instruction JA_5
            Groups: jump
            0x7ffff7de6132:	ja	0x7ffff7de6108
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6132] = 'w'
        mem[0x7ffff7de6133] = '\xd4'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6132
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6132], b'w')
        self.assertEqual(mem[0x7ffff7de6133], b'\xd4')
        self.assertEqual(cpu.RIP, 140737351934216)

    def test_JA_6(self):
        ''' Instruction JA_6
            Groups: jump
            0x7ffff7de6132:	ja	0x7ffff7de6108
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6132] = 'w'
        mem[0x7ffff7de6133] = '\xd4'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6132
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6132], b'w')
        self.assertEqual(mem[0x7ffff7de6133], b'\xd4')
        self.assertEqual(cpu.RIP, 140737351934216)

    def test_JBE_1(self):
        ''' Instruction JBE_1
            Groups: jump
            0x41188d:	jbe	0x411ec0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x0041188d] = '\x0f'
        mem[0x0041188e] = '\x86'
        mem[0x0041188f] = '-'
        mem[0x00411890] = '\x06'
        mem[0x00411891] = '\x00'
        mem[0x00411892] = '\x00'
        cpu.ZF = False
        cpu.CF = True
        cpu.RIP = 0x41188d
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41188d], b'\x0f')
        self.assertEqual(mem[0x41188e], b'\x86')
        self.assertEqual(mem[0x41188f], b'-')
        self.assertEqual(mem[0x411890], b'\x06')
        self.assertEqual(mem[0x411891], b'\x00')
        self.assertEqual(mem[0x411892], b'\x00')
        self.assertEqual(cpu.RIP, 4267712)

    def test_JBE_2(self):
        ''' Instruction JBE_2
            Groups: jump
            0x4325e3:	jbe	0x4326cf
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004325e3] = '\x0f'
        mem[0x004325e4] = '\x86'
        mem[0x004325e5] = '\xe6'
        mem[0x004325e6] = '\x00'
        mem[0x004325e7] = '\x00'
        mem[0x004325e8] = '\x00'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x4325e3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4325e3], b'\x0f')
        self.assertEqual(mem[0x4325e4], b'\x86')
        self.assertEqual(mem[0x4325e5], b'\xe6')
        self.assertEqual(mem[0x4325e6], b'\x00')
        self.assertEqual(mem[0x4325e7], b'\x00')
        self.assertEqual(mem[0x4325e8], b'\x00')
        self.assertEqual(cpu.RIP, 4400617)

    def test_JBE_3(self):
        ''' Instruction JBE_3
            Groups: jump
            0x432388:	jbe	0x4323aa
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432388] = 'v'
        mem[0x00432389] = ' '
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x432388
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432388], b'v')
        self.assertEqual(mem[0x432389], b' ')
        self.assertEqual(cpu.RIP, 4400010)

    def test_JBE_4(self):
        ''' Instruction JBE_4
            Groups: jump
            0x4325e3:	jbe	0x4326cf
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004325e3] = '\x0f'
        mem[0x004325e4] = '\x86'
        mem[0x004325e5] = '\xe6'
        mem[0x004325e6] = '\x00'
        mem[0x004325e7] = '\x00'
        mem[0x004325e8] = '\x00'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x4325e3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4325e3], b'\x0f')
        self.assertEqual(mem[0x4325e4], b'\x86')
        self.assertEqual(mem[0x4325e5], b'\xe6')
        self.assertEqual(mem[0x4325e6], b'\x00')
        self.assertEqual(mem[0x4325e7], b'\x00')
        self.assertEqual(mem[0x4325e8], b'\x00')
        self.assertEqual(cpu.RIP, 4400617)

    def test_JBE_5(self):
        ''' Instruction JBE_5
            Groups: jump
            0x7ffff7df1269:	jbe	0x7ffff7df1289
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1269] = 'v'
        mem[0x7ffff7df126a] = '\x1e'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7df1269
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1269], b'v')
        self.assertEqual(mem[0x7ffff7df126a], b'\x1e')
        self.assertEqual(cpu.RIP, 140737351979627)

    def test_JBE_6(self):
        ''' Instruction JBE_6
            Groups: jump
            0x7ffff7acff53:	jbe	0x7ffff7ad003f
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7acf000, 0x1000, 'rwx')
        mem[0x7ffff7acff53] = '\x0f'
        mem[0x7ffff7acff54] = '\x86'
        mem[0x7ffff7acff55] = '\xe6'
        mem[0x7ffff7acff56] = '\x00'
        mem[0x7ffff7acff57] = '\x00'
        mem[0x7ffff7acff58] = '\x00'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7acff53
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7acff53], b'\x0f')
        self.assertEqual(mem[0x7ffff7acff54], b'\x86')
        self.assertEqual(mem[0x7ffff7acff55], b'\xe6')
        self.assertEqual(mem[0x7ffff7acff56], b'\x00')
        self.assertEqual(mem[0x7ffff7acff57], b'\x00')
        self.assertEqual(mem[0x7ffff7acff58], b'\x00')
        self.assertEqual(cpu.RIP, 140737348697945)

    def test_JB_1(self):
        ''' Instruction JB_1
            Groups: jump
            0x7ffff7b58f46:	jb	0x7ffff7b58f00
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f46] = 'r'
        mem[0x7ffff7b58f47] = '\xb8'
        cpu.CF = True
        cpu.RIP = 0x7ffff7b58f46
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f46], b'r')
        self.assertEqual(mem[0x7ffff7b58f47], b'\xb8')
        self.assertEqual(cpu.RIP, 140737349259008)

    def test_JB_2(self):
        ''' Instruction JB_2
            Groups: jump
            0x7ffff7b58f46:	jb	0x7ffff7b58f00
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f46] = 'r'
        mem[0x7ffff7b58f47] = '\xb8'
        cpu.CF = False
        cpu.RIP = 0x7ffff7b58f46
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f46], b'r')
        self.assertEqual(mem[0x7ffff7b58f47], b'\xb8')
        self.assertEqual(cpu.RIP, 140737349259080)

    def test_JB_3(self):
        ''' Instruction JB_3
            Groups: jump
            0x400bab:	jb	0x400ab4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400bab] = '\x0f'
        mem[0x00400bac] = '\x82'
        mem[0x00400bad] = '\x03'
        mem[0x00400bae] = '\xff'
        mem[0x00400baf] = '\xff'
        mem[0x00400bb0] = '\xff'
        cpu.CF = True
        cpu.RIP = 0x400bab
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400bab], b'\x0f')
        self.assertEqual(mem[0x400bac], b'\x82')
        self.assertEqual(mem[0x400bad], b'\x03')
        self.assertEqual(mem[0x400bae], b'\xff')
        self.assertEqual(mem[0x400baf], b'\xff')
        self.assertEqual(mem[0x400bb0], b'\xff')
        self.assertEqual(cpu.RIP, 4197044)

    def test_JB_4(self):
        ''' Instruction JB_4
            Groups: jump
            0x7ffff7b58f46:	jb	0x7ffff7b58f00
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f46] = 'r'
        mem[0x7ffff7b58f47] = '\xb8'
        cpu.CF = True
        cpu.RIP = 0x7ffff7b58f46
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f46], b'r')
        self.assertEqual(mem[0x7ffff7b58f47], b'\xb8')
        self.assertEqual(cpu.RIP, 140737349259008)

    def test_JB_5(self):
        ''' Instruction JB_5
            Groups: jump
            0x7ffff7ddeff1:	jb	0x7ffff7ddefd0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7dde000, 0x1000, 'rwx')
        mem[0x7ffff7ddeff1] = 'r'
        mem[0x7ffff7ddeff2] = '\xdd'
        cpu.CF = True
        cpu.RIP = 0x7ffff7ddeff1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddeff1], b'r')
        self.assertEqual(mem[0x7ffff7ddeff2], b'\xdd')
        self.assertEqual(cpu.RIP, 140737351905232)

    def test_JB_6(self):
        ''' Instruction JB_6
            Groups: jump
            0x7ffff7b58f46:	jb	0x7ffff7b58f00
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f46] = 'r'
        mem[0x7ffff7b58f47] = '\xb8'
        cpu.CF = True
        cpu.RIP = 0x7ffff7b58f46
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f46], b'r')
        self.assertEqual(mem[0x7ffff7b58f47], b'\xb8')
        self.assertEqual(cpu.RIP, 140737349259008)

    def test_JE_1(self):
        ''' Instruction JE_1
            Groups: jump
            0x7ffff7de3a9d:	je	0x7ffff7de3ed1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3aa0] = '\x04'
        mem[0x7ffff7de3aa1] = '\x00'
        mem[0x7ffff7de3aa2] = '\x00'
        mem[0x7ffff7de3a9d] = '\x0f'
        mem[0x7ffff7de3a9e] = '\x84'
        mem[0x7ffff7de3a9f] = '.'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de3a9d
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3aa0], b'\x04')
        self.assertEqual(mem[0x7ffff7de3aa1], b'\x00')
        self.assertEqual(mem[0x7ffff7de3aa2], b'\x00')
        self.assertEqual(mem[0x7ffff7de3a9d], b'\x0f')
        self.assertEqual(mem[0x7ffff7de3a9e], b'\x84')
        self.assertEqual(mem[0x7ffff7de3a9f], b'.')
        self.assertEqual(cpu.RIP, 140737351924387)

    def test_JE_2(self):
        ''' Instruction JE_2
            Groups: jump
            0x7ffff7de61be:	je	0x7ffff7de65b8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de61c0] = '\xf4'
        mem[0x7ffff7de61c1] = '\x03'
        mem[0x7ffff7de61c2] = '\x00'
        mem[0x7ffff7de61c3] = '\x00'
        mem[0x7ffff7de61be] = '\x0f'
        mem[0x7ffff7de61bf] = '\x84'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de61be
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de61c0], b'\xf4')
        self.assertEqual(mem[0x7ffff7de61c1], b'\x03')
        self.assertEqual(mem[0x7ffff7de61c2], b'\x00')
        self.assertEqual(mem[0x7ffff7de61c3], b'\x00')
        self.assertEqual(mem[0x7ffff7de61be], b'\x0f')
        self.assertEqual(mem[0x7ffff7de61bf], b'\x84')
        self.assertEqual(cpu.RIP, 140737351934404)

    def test_JE_3(self):
        ''' Instruction JE_3
            Groups: jump
            0x7ffff7de38c6:	je	0x7ffff7de3960
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de38c6] = '\x0f'
        mem[0x7ffff7de38c7] = '\x84'
        mem[0x7ffff7de38c8] = '\x94'
        mem[0x7ffff7de38c9] = '\x00'
        mem[0x7ffff7de38ca] = '\x00'
        mem[0x7ffff7de38cb] = '\x00'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de38c6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de38c6], b'\x0f')
        self.assertEqual(mem[0x7ffff7de38c7], b'\x84')
        self.assertEqual(mem[0x7ffff7de38c8], b'\x94')
        self.assertEqual(mem[0x7ffff7de38c9], b'\x00')
        self.assertEqual(mem[0x7ffff7de38ca], b'\x00')
        self.assertEqual(mem[0x7ffff7de38cb], b'\x00')
        self.assertEqual(cpu.RIP, 140737351923916)

    def test_JE_4(self):
        ''' Instruction JE_4
            Groups: jump
            0x7ffff7de440b:	je	0x7ffff7de4644
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de440b] = '\x0f'
        mem[0x7ffff7de440c] = '\x84'
        mem[0x7ffff7de440d] = '3'
        mem[0x7ffff7de440e] = '\x02'
        mem[0x7ffff7de440f] = '\x00'
        mem[0x7ffff7de4410] = '\x00'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de440b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de440b], b'\x0f')
        self.assertEqual(mem[0x7ffff7de440c], b'\x84')
        self.assertEqual(mem[0x7ffff7de440d], b'3')
        self.assertEqual(mem[0x7ffff7de440e], b'\x02')
        self.assertEqual(mem[0x7ffff7de440f], b'\x00')
        self.assertEqual(mem[0x7ffff7de4410], b'\x00')
        self.assertEqual(cpu.RIP, 140737351926801)

    def test_JE_5(self):
        ''' Instruction JE_5
            Groups: jump
            0x7ffff7de6115:	je	0x7ffff7de6121
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6115] = 't'
        mem[0x7ffff7de6116] = '\n'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de6115
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6115], b't')
        self.assertEqual(mem[0x7ffff7de6116], b'\n')
        self.assertEqual(cpu.RIP, 140737351934231)

    def test_JE_6(self):
        ''' Instruction JE_6
            Groups: jump
            0x406e0b:	je	0x406dc6
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem[0x00406e0b] = 't'
        mem[0x00406e0c] = '\xb9'
        cpu.ZF = False
        cpu.RIP = 0x406e0b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x406e0b], b't')
        self.assertEqual(mem[0x406e0c], b'\xb9')
        self.assertEqual(cpu.RIP, 4222477)

    def test_JGE_1(self):
        ''' Instruction JGE_1
            Groups: jump
            0x7ffff7ab5b02:	jge	0x7ffff7ab5be0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab5000, 0x1000, 'rwx')
        mem[0x7ffff7ab5b02] = '\x0f'
        mem[0x7ffff7ab5b03] = '\x8d'
        mem[0x7ffff7ab5b04] = '\xd8'
        mem[0x7ffff7ab5b05] = '\x00'
        mem[0x7ffff7ab5b06] = '\x00'
        mem[0x7ffff7ab5b07] = '\x00'
        cpu.OF = False
        cpu.SF = True
        cpu.RIP = 0x7ffff7ab5b02
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab5b02], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab5b03], b'\x8d')
        self.assertEqual(mem[0x7ffff7ab5b04], b'\xd8')
        self.assertEqual(mem[0x7ffff7ab5b05], b'\x00')
        self.assertEqual(mem[0x7ffff7ab5b06], b'\x00')
        self.assertEqual(mem[0x7ffff7ab5b07], b'\x00')
        self.assertEqual(cpu.RIP, 140737348590344)

    def test_JGE_2(self):
        ''' Instruction JGE_2
            Groups: jump
            0x7ffff7b09879:	jge	0x7ffff7b0987f
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b09000, 0x1000, 'rwx')
        mem[0x7ffff7b09879] = '}'
        mem[0x7ffff7b0987a] = '\x04'
        cpu.OF = False
        cpu.SF = False
        cpu.RIP = 0x7ffff7b09879
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b09879], b'}')
        self.assertEqual(mem[0x7ffff7b0987a], b'\x04')
        self.assertEqual(cpu.RIP, 140737348933759)

    def test_JGE_3(self):
        ''' Instruction JGE_3
            Groups: jump
            0x7ffff7ab5b02:	jge	0x7ffff7ab5be0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab5000, 0x1000, 'rwx')
        mem[0x7ffff7ab5b02] = '\x0f'
        mem[0x7ffff7ab5b03] = '\x8d'
        mem[0x7ffff7ab5b04] = '\xd8'
        mem[0x7ffff7ab5b05] = '\x00'
        mem[0x7ffff7ab5b06] = '\x00'
        mem[0x7ffff7ab5b07] = '\x00'
        cpu.OF = False
        cpu.SF = True
        cpu.RIP = 0x7ffff7ab5b02
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab5b02], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab5b03], b'\x8d')
        self.assertEqual(mem[0x7ffff7ab5b04], b'\xd8')
        self.assertEqual(mem[0x7ffff7ab5b05], b'\x00')
        self.assertEqual(mem[0x7ffff7ab5b06], b'\x00')
        self.assertEqual(mem[0x7ffff7ab5b07], b'\x00')
        self.assertEqual(cpu.RIP, 140737348590344)

    def test_JG_1(self):
        ''' Instruction JG_1
            Groups: jump
            0x403684:	jg	0x40361a
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00403000, 0x1000, 'rwx')
        mem[0x00403684] = '\x7f'
        mem[0x00403685] = '\x94'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x403684
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x403684], b'\x7f')
        self.assertEqual(mem[0x403685], b'\x94')
        self.assertEqual(cpu.RIP, 4208154)

    def test_JG_2(self):
        ''' Instruction JG_2
            Groups: jump
            0x40c120:	jg	0x40c3f0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040c000, 0x1000, 'rwx')
        mem[0x0040c120] = '\x0f'
        mem[0x0040c121] = '\x8f'
        mem[0x0040c122] = '\xca'
        mem[0x0040c123] = '\x02'
        mem[0x0040c124] = '\x00'
        mem[0x0040c125] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = True
        cpu.RIP = 0x40c120
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40c120], b'\x0f')
        self.assertEqual(mem[0x40c121], b'\x8f')
        self.assertEqual(mem[0x40c122], b'\xca')
        self.assertEqual(mem[0x40c123], b'\x02')
        self.assertEqual(mem[0x40c124], b'\x00')
        self.assertEqual(mem[0x40c125], b'\x00')
        self.assertEqual(cpu.RIP, 4243750)

    def test_JG_3(self):
        ''' Instruction JG_3
            Groups: jump
            0x7ffff7df1357:	jg	0x7ffff7df13a0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1358] = 'G'
        mem[0x7ffff7df1357] = '\x7f'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = True
        cpu.RIP = 0x7ffff7df1357
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1358], b'G')
        self.assertEqual(mem[0x7ffff7df1357], b'\x7f')
        self.assertEqual(cpu.RIP, 140737351979865)

    def test_JG_4(self):
        ''' Instruction JG_4
            Groups: jump
            0x7ffff7ddc9fb:	jg	0x7ffff7ddce16
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddc000, 0x1000, 'rwx')
        mem[0x7ffff7ddca00] = '\x00'
        mem[0x7ffff7ddc9fb] = '\x0f'
        mem[0x7ffff7ddc9fc] = '\x8f'
        mem[0x7ffff7ddc9fd] = '\x15'
        mem[0x7ffff7ddc9fe] = '\x04'
        mem[0x7ffff7ddc9ff] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x7ffff7ddc9fb
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddca00], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc9fb], b'\x0f')
        self.assertEqual(mem[0x7ffff7ddc9fc], b'\x8f')
        self.assertEqual(mem[0x7ffff7ddc9fd], b'\x15')
        self.assertEqual(mem[0x7ffff7ddc9fe], b'\x04')
        self.assertEqual(mem[0x7ffff7ddc9ff], b'\x00')
        self.assertEqual(cpu.RIP, 140737351896598)

    def test_JG_5(self):
        ''' Instruction JG_5
            Groups: jump
            0x7ffff7ddc9fb:	jg	0x7ffff7ddce16
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddc000, 0x1000, 'rwx')
        mem[0x7ffff7ddca00] = '\x00'
        mem[0x7ffff7ddc9fb] = '\x0f'
        mem[0x7ffff7ddc9fc] = '\x8f'
        mem[0x7ffff7ddc9fd] = '\x15'
        mem[0x7ffff7ddc9fe] = '\x04'
        mem[0x7ffff7ddc9ff] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x7ffff7ddc9fb
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddca00], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc9fb], b'\x0f')
        self.assertEqual(mem[0x7ffff7ddc9fc], b'\x8f')
        self.assertEqual(mem[0x7ffff7ddc9fd], b'\x15')
        self.assertEqual(mem[0x7ffff7ddc9fe], b'\x04')
        self.assertEqual(mem[0x7ffff7ddc9ff], b'\x00')
        self.assertEqual(cpu.RIP, 140737351896598)

    def test_JG_6(self):
        ''' Instruction JG_6
            Groups: jump
            0x40c2e4:	jg	0x40c250
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040c000, 0x1000, 'rwx')
        mem[0x0040c2e4] = '\x0f'
        mem[0x0040c2e5] = '\x8f'
        mem[0x0040c2e6] = 'f'
        mem[0x0040c2e7] = '\xff'
        mem[0x0040c2e8] = '\xff'
        mem[0x0040c2e9] = '\xff'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = True
        cpu.RIP = 0x40c2e4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40c2e4], b'\x0f')
        self.assertEqual(mem[0x40c2e5], b'\x8f')
        self.assertEqual(mem[0x40c2e6], b'f')
        self.assertEqual(mem[0x40c2e7], b'\xff')
        self.assertEqual(mem[0x40c2e8], b'\xff')
        self.assertEqual(mem[0x40c2e9], b'\xff')
        self.assertEqual(cpu.RIP, 4244202)

    def test_JLE_1(self):
        ''' Instruction JLE_1
            Groups: jump
            0x400b2b:	jle	0x400b01
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400b2b] = '~'
        mem[0x00400b2c] = '\xd4'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = True
        cpu.RIP = 0x400b2b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400b2b], b'~')
        self.assertEqual(mem[0x400b2c], b'\xd4')
        self.assertEqual(cpu.RIP, 4197121)

    def test_JLE_2(self):
        ''' Instruction JLE_2
            Groups: jump
            0x7ffff7a4e1cb:	jle	0x7ffff7a4e429
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e1cb] = '\x0f'
        mem[0x7ffff7a4e1cc] = '\x8e'
        mem[0x7ffff7a4e1cd] = 'X'
        mem[0x7ffff7a4e1ce] = '\x02'
        mem[0x7ffff7a4e1cf] = '\x00'
        mem[0x7ffff7a4e1d0] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x7ffff7a4e1cb
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4e1cb], b'\x0f')
        self.assertEqual(mem[0x7ffff7a4e1cc], b'\x8e')
        self.assertEqual(mem[0x7ffff7a4e1cd], b'X')
        self.assertEqual(mem[0x7ffff7a4e1ce], b'\x02')
        self.assertEqual(mem[0x7ffff7a4e1cf], b'\x00')
        self.assertEqual(mem[0x7ffff7a4e1d0], b'\x00')
        self.assertEqual(cpu.RIP, 140737348166097)

    def test_JLE_3(self):
        ''' Instruction JLE_3
            Groups: jump
            0x437c08:	jle	0x437c1f
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00437000, 0x1000, 'rwx')
        mem[0x00437c08] = '~'
        mem[0x00437c09] = '\x15'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x437c08
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x437c08], b'~')
        self.assertEqual(mem[0x437c09], b'\x15')
        self.assertEqual(cpu.RIP, 4422666)

    def test_JLE_4(self):
        ''' Instruction JLE_4
            Groups: jump
            0x7ffff7de4486:	jle	0x7ffff7de4430
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4486] = '~'
        mem[0x7ffff7de4487] = '\xa8'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x7ffff7de4486
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4486], b'~')
        self.assertEqual(mem[0x7ffff7de4487], b'\xa8')
        self.assertEqual(cpu.RIP, 140737351926920)

    def test_JLE_5(self):
        ''' Instruction JLE_5
            Groups: jump
            0x7ffff7de4486:	jle	0x7ffff7de4430
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4486] = '~'
        mem[0x7ffff7de4487] = '\xa8'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x7ffff7de4486
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4486], b'~')
        self.assertEqual(mem[0x7ffff7de4487], b'\xa8')
        self.assertEqual(cpu.RIP, 140737351926920)

    def test_JLE_6(self):
        ''' Instruction JLE_6
            Groups: jump
            0x7ffff7de4486:	jle	0x7ffff7de4430
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4486] = '~'
        mem[0x7ffff7de4487] = '\xa8'
        cpu.OF = False
        cpu.ZF = False
        cpu.SF = False
        cpu.RIP = 0x7ffff7de4486
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4486], b'~')
        self.assertEqual(mem[0x7ffff7de4487], b'\xa8')
        self.assertEqual(cpu.RIP, 140737351926920)

    def test_JL_1(self):
        ''' Instruction JL_1
            Groups: jump
            0x555555556f00:	jl	0x555555556ee2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem[0x555555556f00] = '|'
        mem[0x555555556f01] = '\xe0'
        cpu.OF = False
        cpu.SF = True
        cpu.RIP = 0x555555556f00
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555556f00], b'|')
        self.assertEqual(mem[0x555555556f01], b'\xe0')
        self.assertEqual(cpu.RIP, 93824992243426)

    def test_JL_2(self):
        ''' Instruction JL_2
            Groups: jump
            0x555555556f00:	jl	0x555555556ee2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem[0x555555556f00] = '|'
        mem[0x555555556f01] = '\xe0'
        cpu.OF = False
        cpu.SF = False
        cpu.RIP = 0x555555556f00
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555556f00], b'|')
        self.assertEqual(mem[0x555555556f01], b'\xe0')
        self.assertEqual(cpu.RIP, 93824992243458)

    def test_JL_3(self):
        ''' Instruction JL_3
            Groups: jump
            0x555555556f00:	jl	0x555555556ee2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem[0x555555556f00] = '|'
        mem[0x555555556f01] = '\xe0'
        cpu.OF = False
        cpu.SF = True
        cpu.RIP = 0x555555556f00
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555556f00], b'|')
        self.assertEqual(mem[0x555555556f01], b'\xe0')
        self.assertEqual(cpu.RIP, 93824992243426)

    def test_JMP_1(self):
        ''' Instruction JMP_1
            Groups: jump
            0x7ffff7de4279:	jmp	0x7ffff7de3a98
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4279] = '\xe9'
        mem[0x7ffff7de427a] = '\x1a'
        mem[0x7ffff7de427b] = '\xf8'
        mem[0x7ffff7de427c] = '\xff'
        mem[0x7ffff7de427d] = '\xff'
        cpu.RIP = 0x7ffff7de4279
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4279], b'\xe9')
        self.assertEqual(mem[0x7ffff7de427a], b'\x1a')
        self.assertEqual(mem[0x7ffff7de427b], b'\xf8')
        self.assertEqual(mem[0x7ffff7de427c], b'\xff')
        self.assertEqual(mem[0x7ffff7de427d], b'\xff')
        self.assertEqual(cpu.RIP, 140737351924376)

    def test_JMP_2(self):
        ''' Instruction JMP_2
            Groups: jump
            0x7ffff7b58ee7:	jmp	0x7ffff7b58f10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58ee8] = "'"
        mem[0x7ffff7b58ee7] = '\xeb'
        cpu.RIP = 0x7ffff7b58ee7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58ee8], b"'")
        self.assertEqual(mem[0x7ffff7b58ee7], b'\xeb')
        self.assertEqual(cpu.RIP, 140737349259024)

    def test_JMP_3(self):
        ''' Instruction JMP_3
            Groups: jump
            0x7ffff7df28e1:	jmp	0x7ffff7ddaa00
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df2000, 0x1000, 'rwx')
        mem[0x7ffff7df28e1] = '\xe9'
        mem[0x7ffff7df28e2] = '\x1a'
        mem[0x7ffff7df28e3] = '\x81'
        mem[0x7ffff7df28e4] = '\xfe'
        mem[0x7ffff7df28e5] = '\xff'
        cpu.RIP = 0x7ffff7df28e1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df28e1], b'\xe9')
        self.assertEqual(mem[0x7ffff7df28e2], b'\x1a')
        self.assertEqual(mem[0x7ffff7df28e3], b'\x81')
        self.assertEqual(mem[0x7ffff7df28e4], b'\xfe')
        self.assertEqual(mem[0x7ffff7df28e5], b'\xff')
        self.assertEqual(cpu.RIP, 140737351887360)

    def test_JMP_4(self):
        ''' Instruction JMP_4
            Groups: mode64, jump
            0x7ffff7de62ee:	jmp	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de62ee] = '\xff'
        mem[0x7ffff7de62ef] = '\xe2'
        cpu.RDX = 0x7ffff7de63b8
        cpu.RIP = 0x7ffff7de62ee
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de62ee], b'\xff')
        self.assertEqual(mem[0x7ffff7de62ef], b'\xe2')
        self.assertEqual(cpu.RDX, 140737351934904)
        self.assertEqual(cpu.RIP, 140737351934904)

    def test_JMP_5(self):
        ''' Instruction JMP_5
            Groups: jump
            0x7ffff7de4042:	jmp	0x7ffff7de4054
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4042] = '\xeb'
        mem[0x7ffff7de4043] = '\x10'
        cpu.RIP = 0x7ffff7de4042
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4042], b'\xeb')
        self.assertEqual(mem[0x7ffff7de4043], b'\x10')
        self.assertEqual(cpu.RIP, 140737351925844)

    def test_JMP_6(self):
        ''' Instruction JMP_6
            Groups: jump
            0x7ffff7b58ee7:	jmp	0x7ffff7b58f10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58ee8] = "'"
        mem[0x7ffff7b58ee7] = '\xeb'
        cpu.RIP = 0x7ffff7b58ee7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58ee8], b"'")
        self.assertEqual(mem[0x7ffff7b58ee7], b'\xeb')
        self.assertEqual(cpu.RIP, 140737349259024)

    def test_JNE_1(self):
        ''' Instruction JNE_1
            Groups: jump
            0x7ffff7df459e:	jne	0x7ffff7df4590
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df459e] = 'u'
        mem[0x7ffff7df459f] = '\xf0'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df459e
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df459e], b'u')
        self.assertEqual(mem[0x7ffff7df459f], b'\xf0')
        self.assertEqual(cpu.RIP, 140737351992720)

    def test_JNE_2(self):
        ''' Instruction JNE_2
            Groups: jump
            0x7ffff7de5a4b:	jne	0x7ffff7de5a40
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5a4b] = 'u'
        mem[0x7ffff7de5a4c] = '\xf3'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de5a4b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5a4b], b'u')
        self.assertEqual(mem[0x7ffff7de5a4c], b'\xf3')
        self.assertEqual(cpu.RIP, 140737351932480)

    def test_JNE_3(self):
        ''' Instruction JNE_3
            Groups: jump
            0x7ffff7de611b:	jne	0x7ffff7de73ad
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6120] = '\x00'
        mem[0x7ffff7de611b] = '\x0f'
        mem[0x7ffff7de611c] = '\x85'
        mem[0x7ffff7de611d] = '\x8c'
        mem[0x7ffff7de611e] = '\x12'
        mem[0x7ffff7de611f] = '\x00'
        cpu.ZF = True
        cpu.RIP = 0x7ffff7de611b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6120], b'\x00')
        self.assertEqual(mem[0x7ffff7de611b], b'\x0f')
        self.assertEqual(mem[0x7ffff7de611c], b'\x85')
        self.assertEqual(mem[0x7ffff7de611d], b'\x8c')
        self.assertEqual(mem[0x7ffff7de611e], b'\x12')
        self.assertEqual(mem[0x7ffff7de611f], b'\x00')
        self.assertEqual(cpu.RIP, 140737351934241)

    def test_JNE_4(self):
        ''' Instruction JNE_4
            Groups: jump
            0x7ffff7aab197:	jne	0x7ffff7aab188
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aab000, 0x1000, 'rwx')
        mem[0x7ffff7aab198] = '\xef'
        mem[0x7ffff7aab197] = 'u'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7aab197
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7aab198], b'\xef')
        self.assertEqual(mem[0x7ffff7aab197], b'u')
        self.assertEqual(cpu.RIP, 140737348546952)

    def test_JNE_5(self):
        ''' Instruction JNE_5
            Groups: jump
            0x7ffff7df4594:	jne	0x7ffff7df45a3
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4594] = 'u'
        mem[0x7ffff7df4595] = '\r'
        cpu.ZF = True
        cpu.RIP = 0x7ffff7df4594
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4594], b'u')
        self.assertEqual(mem[0x7ffff7df4595], b'\r')
        self.assertEqual(cpu.RIP, 140737351992726)

    def test_JNE_6(self):
        ''' Instruction JNE_6
            Groups: jump
            0x7ffff7df459e:	jne	0x7ffff7df4590
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df459e] = 'u'
        mem[0x7ffff7df459f] = '\xf0'
        cpu.ZF = False
        cpu.RIP = 0x7ffff7df459e
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df459e], b'u')
        self.assertEqual(mem[0x7ffff7df459f], b'\xf0')
        self.assertEqual(cpu.RIP, 140737351992720)

    def test_JNS_1(self):
        ''' Instruction JNS_1
            Groups: jump
            0x7ffff7df138f:	jns	0x7ffff7df1350
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1390] = '\xbf'
        mem[0x7ffff7df138f] = 'y'
        cpu.SF = True
        cpu.RIP = 0x7ffff7df138f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1390], b'\xbf')
        self.assertEqual(mem[0x7ffff7df138f], b'y')
        self.assertEqual(cpu.RIP, 140737351979921)

    def test_JNS_2(self):
        ''' Instruction JNS_2
            Groups: jump
            0x555555565fb2:	jns	0x5555555659ec
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555565000, 0x1000, 'rwx')
        mem[0x555555565fb2] = '\x0f'
        mem[0x555555565fb3] = '\x89'
        mem[0x555555565fb4] = '4'
        mem[0x555555565fb5] = '\xfa'
        mem[0x555555565fb6] = '\xff'
        mem[0x555555565fb7] = '\xff'
        cpu.SF = False
        cpu.RIP = 0x555555565fb2
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555565fb2], b'\x0f')
        self.assertEqual(mem[0x555555565fb3], b'\x89')
        self.assertEqual(mem[0x555555565fb4], b'4')
        self.assertEqual(mem[0x555555565fb5], b'\xfa')
        self.assertEqual(mem[0x555555565fb6], b'\xff')
        self.assertEqual(mem[0x555555565fb7], b'\xff')
        self.assertEqual(cpu.RIP, 93824992303596)

    def test_JNS_3(self):
        ''' Instruction JNS_3
            Groups: jump
            0x7ffff7df138f:	jns	0x7ffff7df1350
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1390] = '\xbf'
        mem[0x7ffff7df138f] = 'y'
        cpu.SF = True
        cpu.RIP = 0x7ffff7df138f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1390], b'\xbf')
        self.assertEqual(mem[0x7ffff7df138f], b'y')
        self.assertEqual(cpu.RIP, 140737351979921)

    def test_JNS_4(self):
        ''' Instruction JNS_4
            Groups: jump
            0x7ffff7df138f:	jns	0x7ffff7df1350
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1390] = '\xbf'
        mem[0x7ffff7df138f] = 'y'
        cpu.SF = False
        cpu.RIP = 0x7ffff7df138f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1390], b'\xbf')
        self.assertEqual(mem[0x7ffff7df138f], b'y')
        self.assertEqual(cpu.RIP, 140737351979856)

    def test_JNS_5(self):
        ''' Instruction JNS_5
            Groups: jump
            0x7ffff7df138f:	jns	0x7ffff7df1350
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1390] = '\xbf'
        mem[0x7ffff7df138f] = 'y'
        cpu.SF = True
        cpu.RIP = 0x7ffff7df138f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1390], b'\xbf')
        self.assertEqual(mem[0x7ffff7df138f], b'y')
        self.assertEqual(cpu.RIP, 140737351979921)

    def test_JNS_6(self):
        ''' Instruction JNS_6
            Groups: jump
            0x7ffff7df138f:	jns	0x7ffff7df1350
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1390] = '\xbf'
        mem[0x7ffff7df138f] = 'y'
        cpu.SF = False
        cpu.RIP = 0x7ffff7df138f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1390], b'\xbf')
        self.assertEqual(mem[0x7ffff7df138f], b'y')
        self.assertEqual(cpu.RIP, 140737351979856)

    def test_JS_1(self):
        ''' Instruction JS_1
            Groups: jump
            0x4326b2:	js	0x4328fb
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004326b2] = '\x0f'
        mem[0x004326b3] = '\x88'
        mem[0x004326b4] = 'C'
        mem[0x004326b5] = '\x02'
        mem[0x004326b6] = '\x00'
        mem[0x004326b7] = '\x00'
        cpu.SF = False
        cpu.RIP = 0x4326b2
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4326b2], b'\x0f')
        self.assertEqual(mem[0x4326b3], b'\x88')
        self.assertEqual(mem[0x4326b4], b'C')
        self.assertEqual(mem[0x4326b5], b'\x02')
        self.assertEqual(mem[0x4326b6], b'\x00')
        self.assertEqual(mem[0x4326b7], b'\x00')
        self.assertEqual(cpu.RIP, 4400824)

    def test_JS_2(self):
        ''' Instruction JS_2
            Groups: jump
            0x4322d2:	js	0x43251b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004322d2] = '\x0f'
        mem[0x004322d3] = '\x88'
        mem[0x004322d4] = 'C'
        mem[0x004322d5] = '\x02'
        mem[0x004322d6] = '\x00'
        mem[0x004322d7] = '\x00'
        cpu.SF = False
        cpu.RIP = 0x4322d2
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4322d2], b'\x0f')
        self.assertEqual(mem[0x4322d3], b'\x88')
        self.assertEqual(mem[0x4322d4], b'C')
        self.assertEqual(mem[0x4322d5], b'\x02')
        self.assertEqual(mem[0x4322d6], b'\x00')
        self.assertEqual(mem[0x4322d7], b'\x00')
        self.assertEqual(cpu.RIP, 4399832)

    def test_JS_3(self):
        ''' Instruction JS_3
            Groups: jump
            0x555555565075:	js	0x555555566260
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555565000, 0x1000, 'rwx')
        mem[0x555555565075] = '\x0f'
        mem[0x555555565076] = '\x88'
        mem[0x555555565077] = '\xe5'
        mem[0x555555565078] = '\x11'
        mem[0x555555565079] = '\x00'
        mem[0x55555556507a] = '\x00'
        cpu.SF = False
        cpu.RIP = 0x555555565075
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555565075], b'\x0f')
        self.assertEqual(mem[0x555555565076], b'\x88')
        self.assertEqual(mem[0x555555565077], b'\xe5')
        self.assertEqual(mem[0x555555565078], b'\x11')
        self.assertEqual(mem[0x555555565079], b'\x00')
        self.assertEqual(mem[0x55555556507a], b'\x00')
        self.assertEqual(cpu.RIP, 93824992301179)

    def test_JS_4(self):
        ''' Instruction JS_4
            Groups: jump
            0x40dd40:	js	0x40dd4c
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040d000, 0x1000, 'rwx')
        mem[0x0040dd40] = 'x'
        mem[0x0040dd41] = '\n'
        cpu.SF = True
        cpu.RIP = 0x40dd40
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40dd40], b'x')
        self.assertEqual(mem[0x40dd41], b'\n')
        self.assertEqual(cpu.RIP, 4250956)

    def test_JS_5(self):
        ''' Instruction JS_5
            Groups: jump
            0x555555559cb6:	js	0x555555559ccf
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555559000, 0x1000, 'rwx')
        mem[0x555555559cb6] = 'x'
        mem[0x555555559cb7] = '\x17'
        cpu.SF = True
        cpu.RIP = 0x555555559cb6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555559cb6], b'x')
        self.assertEqual(mem[0x555555559cb7], b'\x17')
        self.assertEqual(cpu.RIP, 93824992255183)

    def test_JS_6(self):
        ''' Instruction JS_6
            Groups: jump
            0x5555555673d5:	js	0x555555567450
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555567000, 0x1000, 'rwx')
        mem[0x5555555673d5] = 'x'
        mem[0x5555555673d6] = 'y'
        cpu.SF = False
        cpu.RIP = 0x5555555673d5
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5555555673d5], b'x')
        self.assertEqual(mem[0x5555555673d6], b'y')
        self.assertEqual(cpu.RIP, 93824992310231)

    def test_LEAVE_1(self):
        ''' Instruction LEAVE_1
            Groups: mode64
            0x7ffff7b30c15:	leave
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b30000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7ffff7b30c15] = '\xc9'
        mem[0x7fffffffda98] = '\xd0'
        mem[0x7fffffffda99] = '\xda'
        mem[0x7fffffffda9a] = '\xff'
        mem[0x7fffffffda9b] = '\xff'
        mem[0x7fffffffda9c] = '\xff'
        mem[0x7fffffffda9d] = '\x7f'
        mem[0x7fffffffda9e] = '\x00'
        mem[0x7fffffffda9f] = '\x00'
        mem[0x7fffffffdaa0] = '\xf0'
        mem[0x7fffffffdaa1] = '\xda'
        mem[0x7fffffffdaa2] = '\xff'
        mem[0x7fffffffdaa3] = '\xff'
        mem[0x7fffffffdaa4] = '\xff'
        mem[0x7fffffffdaa5] = '\x7f'
        mem[0x7fffffffdaa6] = '\x00'
        mem[0x7fffffffdaa7] = '\x00'
        mem[0x7fffffffdaa8] = 'H'
        mem[0x7fffffffdaa9] = '\xe1'
        mem[0x7fffffffdaaa] = '\xff'
        mem[0x7fffffffdaab] = '\xf7'
        mem[0x7fffffffdaac] = '\xff'
        mem[0x7fffffffdaad] = '\x7f'
        mem[0x7fffffffdaae] = '\x00'
        mem[0x7fffffffdaaf] = '\x00'
        mem[0x7fffffffdab0] = '\xc0'
        mem[0x7fffffffdab1] = '\xda'
        mem[0x7fffffffdab2] = '\xff'
        mem[0x7fffffffdab3] = '\xff'
        mem[0x7fffffffdab4] = '\xff'
        mem[0x7fffffffdab5] = '\x7f'
        mem[0x7fffffffdab6] = '\x00'
        mem[0x7fffffffdab7] = '\x00'
        mem[0x7fffffffdab8] = '\xb3'
        cpu.RSP = 0x7fffffffdaa0
        cpu.RIP = 0x7ffff7b30c15
        cpu.RBP = 0x7fffffffdab0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b30c15], b'\xc9')
        self.assertEqual(mem[0x7fffffffda98], b'\xd0')
        self.assertEqual(mem[0x7fffffffda99], b'\xda')
        self.assertEqual(mem[0x7fffffffda9a], b'\xff')
        self.assertEqual(mem[0x7fffffffda9b], b'\xff')
        self.assertEqual(mem[0x7fffffffda9c], b'\xff')
        self.assertEqual(mem[0x7fffffffda9d], b'\x7f')
        self.assertEqual(mem[0x7fffffffda9e], b'\x00')
        self.assertEqual(mem[0x7fffffffda9f], b'\x00')
        self.assertEqual(mem[0x7fffffffdaa0], b'\xf0')
        self.assertEqual(mem[0x7fffffffdaa1], b'\xda')
        self.assertEqual(mem[0x7fffffffdaa2], b'\xff')
        self.assertEqual(mem[0x7fffffffdaa3], b'\xff')
        self.assertEqual(mem[0x7fffffffdaa4], b'\xff')
        self.assertEqual(mem[0x7fffffffdaa5], b'\x7f')
        self.assertEqual(mem[0x7fffffffdaa6], b'\x00')
        self.assertEqual(mem[0x7fffffffdaa7], b'\x00')
        self.assertEqual(mem[0x7fffffffdaa8], b'H')
        self.assertEqual(mem[0x7fffffffdaa9], b'\xe1')
        self.assertEqual(mem[0x7fffffffdaaa], b'\xff')
        self.assertEqual(mem[0x7fffffffdaab], b'\xf7')
        self.assertEqual(mem[0x7fffffffdaac], b'\xff')
        self.assertEqual(mem[0x7fffffffdaad], b'\x7f')
        self.assertEqual(mem[0x7fffffffdaae], b'\x00')
        self.assertEqual(mem[0x7fffffffdaaf], b'\x00')
        self.assertEqual(mem[0x7fffffffdab0], b'\xc0')
        self.assertEqual(mem[0x7fffffffdab1], b'\xda')
        self.assertEqual(mem[0x7fffffffdab2], b'\xff')
        self.assertEqual(mem[0x7fffffffdab3], b'\xff')
        self.assertEqual(mem[0x7fffffffdab4], b'\xff')
        self.assertEqual(mem[0x7fffffffdab5], b'\x7f')
        self.assertEqual(mem[0x7fffffffdab6], b'\x00')
        self.assertEqual(mem[0x7fffffffdab7], b'\x00')
        self.assertEqual(mem[0x7fffffffdab8], b'\xb3')
        self.assertEqual(cpu.RSP, 140737488345784)
        self.assertEqual(cpu.RIP, 140737349094422)
        self.assertEqual(cpu.RBP, 140737488345792)

    def test_LEAVE_2(self):
        ''' Instruction LEAVE_2
            Groups: mode64
            0x4176f4:	leave
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00417000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcad8] = '\xf0'
        mem[0x7fffffffcad9] = 'v'
        mem[0x7fffffffcada] = 'A'
        mem[0x7fffffffcadb] = '\x00'
        mem[0x7fffffffcadc] = '\x00'
        mem[0x7fffffffcadd] = '\x00'
        mem[0x7fffffffcade] = '\x00'
        mem[0x7fffffffcadf] = '\x00'
        mem[0x7fffffffcae0] = '@'
        mem[0x7fffffffcae1] = '\x00'
        mem[0x7fffffffcae2] = '\x00'
        mem[0x7fffffffcae3] = '\x00'
        mem[0x7fffffffcae4] = '\x00'
        mem[0x7fffffffcae5] = '\x00'
        mem[0x7fffffffcae6] = '\x00'
        mem[0x7fffffffcae7] = '\x00'
        mem[0x7fffffffcae8] = 'A'
        mem[0x7fffffffcae9] = '\x00'
        mem[0x7fffffffcaea] = '\x00'
        mem[0x7fffffffcaeb] = '\x00'
        mem[0x7fffffffcaec] = '\x00'
        mem[0x7fffffffcaed] = '\x00'
        mem[0x7fffffffcaee] = '\x00'
        mem[0x7fffffffcaef] = '\x00'
        mem[0x7fffffffcaf0] = ' '
        mem[0x7fffffffcaf1] = '\xdb'
        mem[0x7fffffffcaf2] = '\xff'
        mem[0x7fffffffcaf3] = '\xff'
        mem[0x7fffffffcaf4] = '\xff'
        mem[0x7fffffffcaf5] = '\x7f'
        mem[0x7fffffffcaf6] = '\x00'
        mem[0x7fffffffcaf7] = '\x00'
        mem[0x7fffffffcaf8] = '+'
        mem[0x004176f4] = '\xc9'
        cpu.RSP = 0x7fffffffcae0
        cpu.RIP = 0x4176f4
        cpu.RBP = 0x7fffffffcaf0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcad8], b'\xf0')
        self.assertEqual(mem[0x7fffffffcad9], b'v')
        self.assertEqual(mem[0x7fffffffcada], b'A')
        self.assertEqual(mem[0x7fffffffcadb], b'\x00')
        self.assertEqual(mem[0x7fffffffcadc], b'\x00')
        self.assertEqual(mem[0x7fffffffcadd], b'\x00')
        self.assertEqual(mem[0x7fffffffcade], b'\x00')
        self.assertEqual(mem[0x7fffffffcadf], b'\x00')
        self.assertEqual(mem[0x7fffffffcae0], b'@')
        self.assertEqual(mem[0x7fffffffcae1], b'\x00')
        self.assertEqual(mem[0x7fffffffcae2], b'\x00')
        self.assertEqual(mem[0x7fffffffcae3], b'\x00')
        self.assertEqual(mem[0x7fffffffcae4], b'\x00')
        self.assertEqual(mem[0x7fffffffcae5], b'\x00')
        self.assertEqual(mem[0x7fffffffcae6], b'\x00')
        self.assertEqual(mem[0x7fffffffcae7], b'\x00')
        self.assertEqual(mem[0x7fffffffcae8], b'A')
        self.assertEqual(mem[0x7fffffffcae9], b'\x00')
        self.assertEqual(mem[0x7fffffffcaea], b'\x00')
        self.assertEqual(mem[0x7fffffffcaeb], b'\x00')
        self.assertEqual(mem[0x7fffffffcaec], b'\x00')
        self.assertEqual(mem[0x7fffffffcaed], b'\x00')
        self.assertEqual(mem[0x7fffffffcaee], b'\x00')
        self.assertEqual(mem[0x7fffffffcaef], b'\x00')
        self.assertEqual(mem[0x7fffffffcaf0], b' ')
        self.assertEqual(mem[0x7fffffffcaf1], b'\xdb')
        self.assertEqual(mem[0x7fffffffcaf2], b'\xff')
        self.assertEqual(mem[0x7fffffffcaf3], b'\xff')
        self.assertEqual(mem[0x4176f4], b'\xc9')
        self.assertEqual(mem[0x7fffffffcaf5], b'\x7f')
        self.assertEqual(mem[0x7fffffffcaf6], b'\x00')
        self.assertEqual(mem[0x7fffffffcaf7], b'\x00')
        self.assertEqual(mem[0x7fffffffcaf8], b'+')
        self.assertEqual(mem[0x7fffffffcaf4], b'\xff')
        self.assertEqual(cpu.RSP, 140737488341752)
        self.assertEqual(cpu.RIP, 4290293)
        self.assertEqual(cpu.RBP, 140737488345888)

    def test_LEAVE_3(self):
        ''' Instruction LEAVE_3
            Groups: mode64
            0x7ffff7b59b18:	leave
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b59000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda08] = '\xd0'
        mem[0x7fffffffda09] = '\xd4'
        mem[0x7fffffffda0a] = '\xa4'
        mem[0x7fffffffda0b] = '\xf7'
        mem[0x7fffffffda0c] = '\xff'
        mem[0x7fffffffda0d] = '\x7f'
        mem[0x7fffffffda0e] = '\x00'
        mem[0x7fffffffda0f] = '\x00'
        mem[0x7fffffffda10] = '@'
        mem[0x7fffffffda11] = '\xda'
        mem[0x7fffffffda12] = '\xff'
        mem[0x7fffffffda13] = '\xff'
        mem[0x7fffffffda14] = '\xff'
        mem[0x7fffffffda15] = '\x7f'
        mem[0x7fffffffda16] = '\x00'
        mem[0x7fffffffda17] = '\x00'
        mem[0x7ffff7b59b18] = '\xc9'
        mem[0x7fffffffd9d9] = '\x00'
        mem[0x7fffffffd9da] = '\x00'
        mem[0x7fffffffd9db] = '\x00'
        mem[0x7fffffffd9dc] = '\x00'
        mem[0x7fffffffd9dd] = '\x00'
        mem[0x7fffffffd9de] = '\x00'
        mem[0x7fffffffd9df] = '\x00'
        mem[0x7fffffffd9e0] = '\x00'
        mem[0x7fffffffd9e1] = '\x00'
        mem[0x7fffffffd9e2] = '\x00'
        mem[0x7fffffffd9e3] = '\x00'
        mem[0x7fffffffd9d8] = '\x00'
        mem[0x7fffffffd9e5] = '\x00'
        mem[0x7fffffffda18] = "'"
        mem[0x7fffffffd9e7] = '\x00'
        mem[0x7fffffffd9e8] = '\xf0'
        mem[0x7fffffffd9e6] = '\x00'
        mem[0x7fffffffd9e4] = '\x00'
        cpu.RSP = 0x7fffffffd9e0
        cpu.RIP = 0x7ffff7b59b18
        cpu.RBP = 0x7fffffffda10
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda08], b'\xd0')
        self.assertEqual(mem[0x7fffffffda09], b'\xd4')
        self.assertEqual(mem[0x7fffffffda0a], b'\xa4')
        self.assertEqual(mem[0x7fffffffda0b], b'\xf7')
        self.assertEqual(mem[0x7fffffffda0c], b'\xff')
        self.assertEqual(mem[0x7fffffffda0d], b'\x7f')
        self.assertEqual(mem[0x7fffffffda0e], b'\x00')
        self.assertEqual(mem[0x7fffffffda0f], b'\x00')
        self.assertEqual(mem[0x7fffffffda10], b'@')
        self.assertEqual(mem[0x7fffffffda11], b'\xda')
        self.assertEqual(mem[0x7fffffffda12], b'\xff')
        self.assertEqual(mem[0x7fffffffda13], b'\xff')
        self.assertEqual(mem[0x7fffffffda14], b'\xff')
        self.assertEqual(mem[0x7fffffffda15], b'\x7f')
        self.assertEqual(mem[0x7fffffffda16], b'\x00')
        self.assertEqual(mem[0x7fffffffda17], b'\x00')
        self.assertEqual(mem[0x7ffff7b59b18], b'\xc9')
        self.assertEqual(mem[0x7fffffffd9d9], b'\x00')
        self.assertEqual(mem[0x7fffffffd9da], b'\x00')
        self.assertEqual(mem[0x7fffffffd9db], b'\x00')
        self.assertEqual(mem[0x7fffffffd9dc], b'\x00')
        self.assertEqual(mem[0x7fffffffd9dd], b'\x00')
        self.assertEqual(mem[0x7fffffffd9de], b'\x00')
        self.assertEqual(mem[0x7fffffffd9df], b'\x00')
        self.assertEqual(mem[0x7fffffffd9e0], b'\x00')
        self.assertEqual(mem[0x7fffffffd9e1], b'\x00')
        self.assertEqual(mem[0x7fffffffd9e2], b'\x00')
        self.assertEqual(mem[0x7fffffffd9e3], b'\x00')
        self.assertEqual(mem[0x7fffffffd9d8], b'\x00')
        self.assertEqual(mem[0x7fffffffd9e5], b'\x00')
        self.assertEqual(mem[0x7fffffffda18], b"'")
        self.assertEqual(mem[0x7fffffffd9e7], b'\x00')
        self.assertEqual(mem[0x7fffffffd9e8], b'\xf0')
        self.assertEqual(mem[0x7fffffffd9e6], b'\x00')
        self.assertEqual(mem[0x7fffffffd9e4], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345624)
        self.assertEqual(cpu.RIP, 140737349262105)
        self.assertEqual(cpu.RBP, 140737488345664)

    def test_LEAVE_4(self):
        ''' Instruction LEAVE_4
            Groups: mode64
            0x7ffff7b59b18:	leave
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b59000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdb98] = '\x00'
        mem[0x7fffffffdb71] = '\xdc'
        mem[0x7ffff7b59b18] = '\xc9'
        mem[0x7fffffffdb99] = '\x00'
        mem[0x7fffffffdb9a] = '\x00'
        mem[0x7fffffffdb9b] = '\x00'
        mem[0x7fffffffdb9c] = '\x00'
        mem[0x7fffffffdb9d] = '\x00'
        mem[0x7fffffffdb9e] = '\x00'
        mem[0x7fffffffdb9f] = '\x00'
        mem[0x7fffffffdba0] = '\xf0'
        mem[0x7fffffffdba1] = '\xdb'
        mem[0x7fffffffdba2] = '\xff'
        mem[0x7fffffffdba3] = '\xff'
        mem[0x7fffffffdba4] = '\xff'
        mem[0x7fffffffdba5] = '\x7f'
        mem[0x7fffffffdba6] = '\x00'
        mem[0x7fffffffdba7] = '\x00'
        mem[0x7fffffffdba8] = ':'
        mem[0x7fffffffdb69] = '\x00'
        mem[0x7fffffffdb6a] = '\x00'
        mem[0x7fffffffdb6b] = '\x00'
        mem[0x7fffffffdb6c] = '\x00'
        mem[0x7fffffffdb6d] = '\x00'
        mem[0x7fffffffdb6e] = '\x00'
        mem[0x7fffffffdb6f] = '\x00'
        mem[0x7fffffffdb70] = '\xb8'
        mem[0x7fffffffdb68] = '\x00'
        mem[0x7fffffffdb72] = '\xff'
        mem[0x7fffffffdb73] = '\xff'
        mem[0x7fffffffdb74] = '\xff'
        mem[0x7fffffffdb75] = '\x7f'
        mem[0x7fffffffdb76] = '\x00'
        mem[0x7fffffffdb77] = '\x00'
        mem[0x7fffffffdb78] = 'P'
        cpu.RSP = 0x7fffffffdb70
        cpu.RIP = 0x7ffff7b59b18
        cpu.RBP = 0x7fffffffdba0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b59b18], b'\xc9')
        self.assertEqual(mem[0x7fffffffdb71], b'\xdc')
        self.assertEqual(mem[0x7fffffffdb98], b'\x00')
        self.assertEqual(mem[0x7fffffffdb99], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9a], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9b], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9f], b'\x00')
        self.assertEqual(mem[0x7fffffffdba0], b'\xf0')
        self.assertEqual(mem[0x7fffffffdba1], b'\xdb')
        self.assertEqual(mem[0x7fffffffdba2], b'\xff')
        self.assertEqual(mem[0x7fffffffdba3], b'\xff')
        self.assertEqual(mem[0x7fffffffdba4], b'\xff')
        self.assertEqual(mem[0x7fffffffdba5], b'\x7f')
        self.assertEqual(mem[0x7fffffffdba6], b'\x00')
        self.assertEqual(mem[0x7fffffffdba7], b'\x00')
        self.assertEqual(mem[0x7fffffffdba8], b':')
        self.assertEqual(mem[0x7fffffffdb69], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6a], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6b], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6f], b'\x00')
        self.assertEqual(mem[0x7fffffffdb70], b'\xb8')
        self.assertEqual(mem[0x7fffffffdb68], b'\x00')
        self.assertEqual(mem[0x7fffffffdb72], b'\xff')
        self.assertEqual(mem[0x7fffffffdb73], b'\xff')
        self.assertEqual(mem[0x7fffffffdb74], b'\xff')
        self.assertEqual(mem[0x7fffffffdb75], b'\x7f')
        self.assertEqual(mem[0x7fffffffdb76], b'\x00')
        self.assertEqual(mem[0x7fffffffdb77], b'\x00')
        self.assertEqual(mem[0x7fffffffdb78], b'P')
        self.assertEqual(cpu.RSP, 140737488346024)
        self.assertEqual(cpu.RIP, 140737349262105)
        self.assertEqual(cpu.RBP, 140737488346096)

    def test_LEAVE_5(self):
        ''' Instruction LEAVE_5
            Groups: mode64
            0x7ffff7ae0541:	leave
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ae0000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7ffff7ae0541] = '\xc9'
        mem[0x7fffffffd988] = '7'
        mem[0x7fffffffd989] = '\x05'
        mem[0x7fffffffd98a] = '\xae'
        mem[0x7fffffffd98b] = '\xf7'
        mem[0x7fffffffd98c] = '\xff'
        mem[0x7fffffffd98d] = '\x7f'
        mem[0x7fffffffd98e] = '\x00'
        mem[0x7fffffffd98f] = '\x00'
        mem[0x7fffffffd990] = '\xa8'
        mem[0x7fffffffd991] = '\n'
        mem[0x7fffffffd992] = '\xba'
        mem[0x7fffffffd993] = '\xf7'
        mem[0x7fffffffd994] = '\xff'
        mem[0x7fffffffd995] = '\x7f'
        mem[0x7fffffffd996] = '\x00'
        mem[0x7fffffffd997] = '\x00'
        mem[0x7fffffffd998] = '\xf6'
        mem[0x7fffffffd9a8] = '\xe0'
        mem[0x7fffffffd9a9] = '\xda'
        mem[0x7fffffffd9aa] = '\xff'
        mem[0x7fffffffd9ab] = '\xff'
        mem[0x7fffffffd9ac] = '\xff'
        mem[0x7fffffffd9ad] = '\x7f'
        mem[0x7fffffffd9ae] = '\x00'
        mem[0x7fffffffd9af] = '\x00'
        mem[0x7fffffffd9b0] = '\xe0'
        mem[0x7fffffffd9b1] = '\xda'
        mem[0x7fffffffd9b2] = '\xff'
        mem[0x7fffffffd9b3] = '\xff'
        mem[0x7fffffffd9b4] = '\xff'
        mem[0x7fffffffd9b5] = '\x7f'
        mem[0x7fffffffd9b6] = '\x00'
        mem[0x7fffffffd9b7] = '\x00'
        mem[0x7fffffffd9b8] = '\xf8'
        cpu.RSP = 0x7fffffffd990
        cpu.RIP = 0x7ffff7ae0541
        cpu.RBP = 0x7fffffffd9b0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ae0541], b'\xc9')
        self.assertEqual(mem[0x7fffffffd988], b'7')
        self.assertEqual(mem[0x7fffffffd989], b'\x05')
        self.assertEqual(mem[0x7fffffffd98a], b'\xae')
        self.assertEqual(mem[0x7fffffffd98b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd98c], b'\xff')
        self.assertEqual(mem[0x7fffffffd98d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd98e], b'\x00')
        self.assertEqual(mem[0x7fffffffd98f], b'\x00')
        self.assertEqual(mem[0x7fffffffd990], b'\xa8')
        self.assertEqual(mem[0x7fffffffd991], b'\n')
        self.assertEqual(mem[0x7fffffffd992], b'\xba')
        self.assertEqual(mem[0x7fffffffd993], b'\xf7')
        self.assertEqual(mem[0x7fffffffd994], b'\xff')
        self.assertEqual(mem[0x7fffffffd995], b'\x7f')
        self.assertEqual(mem[0x7fffffffd996], b'\x00')
        self.assertEqual(mem[0x7fffffffd997], b'\x00')
        self.assertEqual(mem[0x7fffffffd998], b'\xf6')
        self.assertEqual(mem[0x7fffffffd9a8], b'\xe0')
        self.assertEqual(mem[0x7fffffffd9a9], b'\xda')
        self.assertEqual(mem[0x7fffffffd9aa], b'\xff')
        self.assertEqual(mem[0x7fffffffd9ab], b'\xff')
        self.assertEqual(mem[0x7fffffffd9ac], b'\xff')
        self.assertEqual(mem[0x7fffffffd9ad], b'\x7f')
        self.assertEqual(mem[0x7fffffffd9ae], b'\x00')
        self.assertEqual(mem[0x7fffffffd9af], b'\x00')
        self.assertEqual(mem[0x7fffffffd9b0], b'\xe0')
        self.assertEqual(mem[0x7fffffffd9b1], b'\xda')
        self.assertEqual(mem[0x7fffffffd9b2], b'\xff')
        self.assertEqual(mem[0x7fffffffd9b3], b'\xff')
        self.assertEqual(mem[0x7fffffffd9b4], b'\xff')
        self.assertEqual(mem[0x7fffffffd9b5], b'\x7f')
        self.assertEqual(mem[0x7fffffffd9b6], b'\x00')
        self.assertEqual(mem[0x7fffffffd9b7], b'\x00')
        self.assertEqual(mem[0x7fffffffd9b8], b'\xf8')
        self.assertEqual(cpu.RSP, 140737488345528)
        self.assertEqual(cpu.RIP, 140737348764994)
        self.assertEqual(cpu.RBP, 140737488345824)

    def test_LEAVE_6(self):
        ''' Instruction LEAVE_6
            Groups: mode64
            0x7ffff7a626cd:	leave
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a62000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda6c] = '\x00'
        mem[0x7fffffffda6b] = '\x00'
        mem[0x7fffffffda68] = '\x00'
        mem[0x7ffff7a626cd] = '\xc9'
        mem[0x7fffffffda6d] = '\x00'
        mem[0x7fffffffda6e] = '\x00'
        mem[0x7fffffffda6f] = '\x00'
        mem[0x7fffffffda60] = '\x00'
        mem[0x7fffffffda61] = '\x00'
        mem[0x7fffffffda62] = '\x00'
        mem[0x7fffffffda63] = '\x00'
        mem[0x7fffffffda64] = '\x00'
        mem[0x7fffffffda65] = '\x00'
        mem[0x7fffffffda66] = '\x00'
        mem[0x7fffffffda67] = '\x00'
        mem[0x7fffffffdb28] = '\x00'
        mem[0x7fffffffdb29] = '\x00'
        mem[0x7fffffffdb2a] = '\x00'
        mem[0x7fffffffdb2b] = '\x00'
        mem[0x7fffffffdb2c] = '\x00'
        mem[0x7fffffffdb2d] = '\x00'
        mem[0x7fffffffdb2e] = '\x00'
        mem[0x7fffffffdb2f] = '\x00'
        mem[0x7fffffffdb30] = '0'
        mem[0x7fffffffdb31] = '\xdc'
        mem[0x7fffffffdb32] = '\xff'
        mem[0x7fffffffdb33] = '\xff'
        mem[0x7fffffffdb34] = '\xff'
        mem[0x7fffffffdb35] = '\x7f'
        mem[0x7fffffffdb36] = '\x00'
        mem[0x7fffffffdb37] = '\x00'
        mem[0x7fffffffdb38] = 'x'
        mem[0x7fffffffda70] = '\x00'
        mem[0x7fffffffda69] = '\x00'
        mem[0x7fffffffda6a] = '\x00'
        cpu.RSP = 0x7fffffffda68
        cpu.RIP = 0x7ffff7a626cd
        cpu.RBP = 0x7fffffffdb30
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda6c], b'\x00')
        self.assertEqual(mem[0x7fffffffda6b], b'\x00')
        self.assertEqual(mem[0x7fffffffda68], b'\x00')
        self.assertEqual(mem[0x7ffff7a626cd], b'\xc9')
        self.assertEqual(mem[0x7fffffffda6d], b'\x00')
        self.assertEqual(mem[0x7fffffffda6e], b'\x00')
        self.assertEqual(mem[0x7fffffffda6f], b'\x00')
        self.assertEqual(mem[0x7fffffffda60], b'\x00')
        self.assertEqual(mem[0x7fffffffda61], b'\x00')
        self.assertEqual(mem[0x7fffffffda62], b'\x00')
        self.assertEqual(mem[0x7fffffffda63], b'\x00')
        self.assertEqual(mem[0x7fffffffda64], b'\x00')
        self.assertEqual(mem[0x7fffffffda65], b'\x00')
        self.assertEqual(mem[0x7fffffffda66], b'\x00')
        self.assertEqual(mem[0x7fffffffda67], b'\x00')
        self.assertEqual(mem[0x7fffffffdb28], b'\x00')
        self.assertEqual(mem[0x7fffffffdb29], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2a], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2b], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2f], b'\x00')
        self.assertEqual(mem[0x7fffffffdb30], b'0')
        self.assertEqual(mem[0x7fffffffdb31], b'\xdc')
        self.assertEqual(mem[0x7fffffffdb32], b'\xff')
        self.assertEqual(mem[0x7fffffffdb33], b'\xff')
        self.assertEqual(mem[0x7fffffffdb34], b'\xff')
        self.assertEqual(mem[0x7fffffffdb35], b'\x7f')
        self.assertEqual(mem[0x7fffffffdb36], b'\x00')
        self.assertEqual(mem[0x7fffffffdb37], b'\x00')
        self.assertEqual(mem[0x7fffffffdb38], b'x')
        self.assertEqual(mem[0x7fffffffda70], b'\x00')
        self.assertEqual(mem[0x7fffffffda69], b'\x00')
        self.assertEqual(mem[0x7fffffffda6a], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345912)
        self.assertEqual(cpu.RIP, 140737348249294)
        self.assertEqual(cpu.RBP, 140737488346160)

    def test_LEA_1(self):
        ''' Instruction LEA_1
            Groups:
            0x7ffff7de44f3:	lea	rsp, qword ptr [rbp - 0x28]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7ffff7de44f3] = 'H'
        mem[0x7ffff7de44f4] = '\x8d'
        mem[0x7ffff7de44f5] = 'e'
        mem[0x7ffff7de44f6] = '\xd8'
        mem[0x7fffffffd978] = '\xc8'
        mem[0x7fffffffd979] = '\xcd'
        mem[0x7fffffffd97a] = '\xa4'
        mem[0x7fffffffd97b] = '\xf7'
        mem[0x7fffffffd97c] = '\xff'
        mem[0x7fffffffd97d] = '\x7f'
        mem[0x7fffffffd97e] = '\x00'
        mem[0x7fffffffd97f] = '\x00'
        cpu.RSP = 0x7fffffffd8b0
        cpu.RIP = 0x7ffff7de44f3
        cpu.RBP = 0x7fffffffd9a0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de44f3], b'H')
        self.assertEqual(mem[0x7ffff7de44f4], b'\x8d')
        self.assertEqual(mem[0x7ffff7de44f5], b'e')
        self.assertEqual(mem[0x7ffff7de44f6], b'\xd8')
        self.assertEqual(mem[0x7fffffffd978], b'\xc8')
        self.assertEqual(mem[0x7fffffffd979], b'\xcd')
        self.assertEqual(mem[0x7fffffffd97a], b'\xa4')
        self.assertEqual(mem[0x7fffffffd97b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd97c], b'\xff')
        self.assertEqual(mem[0x7fffffffd97d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd97e], b'\x00')
        self.assertEqual(mem[0x7fffffffd97f], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345464)
        self.assertEqual(cpu.RIP, 140737351927031)
        self.assertEqual(cpu.RBP, 140737488345504)

    def test_LEA_2(self):
        ''' Instruction LEA_2
            Groups:
            0x7ffff7b58ee3:	lea	r8, qword ptr [r8 + rdx*4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a2f000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7a2fde3] = '\xb2'
        mem[0x7ffff7a2fde4] = '4'
        mem[0x7ffff7a2fde5] = '\xd5'
        mem[0x7ffff7a2fde0] = 'x'
        mem[0x7ffff7a2fde1] = ')'
        mem[0x7ffff7a2fde2] = '\xce'
        mem[0x7ffff7b58ee3] = 'M'
        mem[0x7ffff7b58ee4] = '\x8d'
        mem[0x7ffff7b58ee5] = '\x04'
        mem[0x7ffff7b58ee6] = '\x90'
        mem[0x7ffff7a2fde7] = 'P'
        mem[0x7ffff7a2fde6] = '\x92'
        cpu.R8 = 0x7ffff7a2fa7c
        cpu.RDX = 0xd9
        cpu.RIP = 0x7ffff7b58ee3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a2fde3], b'\xb2')
        self.assertEqual(mem[0x7ffff7a2fde4], b'4')
        self.assertEqual(mem[0x7ffff7a2fde5], b'\xd5')
        self.assertEqual(mem[0x7ffff7a2fde0], b'x')
        self.assertEqual(mem[0x7ffff7a2fde1], b')')
        self.assertEqual(mem[0x7ffff7a2fde2], b'\xce')
        self.assertEqual(mem[0x7ffff7b58ee3], b'M')
        self.assertEqual(mem[0x7ffff7b58ee4], b'\x8d')
        self.assertEqual(mem[0x7ffff7b58ee5], b'\x04')
        self.assertEqual(mem[0x7ffff7b58ee6], b'\x90')
        self.assertEqual(mem[0x7ffff7a2fde7], b'P')
        self.assertEqual(mem[0x7ffff7a2fde6], b'\x92')
        self.assertEqual(cpu.R8, 140737348042208)
        self.assertEqual(cpu.RDX, 217)
        self.assertEqual(cpu.RIP, 140737349258983)

    def test_LEA_3(self):
        ''' Instruction LEA_3
            Groups:
            0x7ffff7de3841:	lea	rsi, qword ptr [rbp - 0x3c]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7ffff7de3841] = 'H'
        mem[0x7ffff7de3842] = '\x8d'
        mem[0x7ffff7de3843] = 'u'
        mem[0x7ffff7de3844] = '\xc4'
        mem[0x7fffffffd8c5] = '\x00'
        mem[0x7fffffffd8c6] = '\x00'
        mem[0x7fffffffd8c7] = '\x00'
        mem[0x7fffffffd8c8] = '\x00'
        mem[0x7fffffffd8c9] = '\x00'
        mem[0x7fffffffd8ca] = '\x00'
        mem[0x7fffffffd8cb] = '\x00'
        mem[0x7fffffffd8c4] = '\x00'
        cpu.RSI = 0xbdd69f1b
        cpu.RIP = 0x7ffff7de3841
        cpu.RBP = 0x7fffffffd900
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3841], b'H')
        self.assertEqual(mem[0x7ffff7de3842], b'\x8d')
        self.assertEqual(mem[0x7ffff7de3843], b'u')
        self.assertEqual(mem[0x7ffff7de3844], b'\xc4')
        self.assertEqual(mem[0x7fffffffd8c5], b'\x00')
        self.assertEqual(mem[0x7fffffffd8c6], b'\x00')
        self.assertEqual(mem[0x7fffffffd8c7], b'\x00')
        self.assertEqual(mem[0x7fffffffd8c8], b'\x00')
        self.assertEqual(mem[0x7fffffffd8c9], b'\x00')
        self.assertEqual(mem[0x7fffffffd8ca], b'\x00')
        self.assertEqual(mem[0x7fffffffd8cb], b'\x00')
        self.assertEqual(mem[0x7fffffffd8c4], b'\x00')
        self.assertEqual(cpu.RSI, 140737488345284)
        self.assertEqual(cpu.RIP, 140737351923781)
        self.assertEqual(cpu.RBP, 140737488345344)

    def test_LEA_4(self):
        ''' Instruction LEA_4
            Groups:
            0x7ffff7b58f14:	lea	rdx, qword ptr [rbx + rdx*8]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a34000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f14] = 'H'
        mem[0x7ffff7b58f15] = '\x8d'
        mem[0x7ffff7b58f16] = '\x14'
        mem[0x7ffff7b58f17] = '\xd3'
        mem[0x7ffff7a34270] = '\xb5'
        mem[0x7ffff7a34271] = '*'
        mem[0x7ffff7a34272] = '\x00'
        mem[0x7ffff7a34273] = '\x00'
        mem[0x7ffff7a34274] = '\x1a'
        mem[0x7ffff7a34275] = '\x00'
        mem[0x7ffff7a34276] = '\x0b'
        mem[0x7ffff7a34277] = '\x00'
        cpu.RDX = 0x4a1
        cpu.RIP = 0x7ffff7b58f14
        cpu.RBX = 0x7ffff7a31d68
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f14], b'H')
        self.assertEqual(mem[0x7ffff7b58f15], b'\x8d')
        self.assertEqual(mem[0x7ffff7b58f16], b'\x14')
        self.assertEqual(mem[0x7ffff7b58f17], b'\xd3')
        self.assertEqual(mem[0x7ffff7a34270], b'\xb5')
        self.assertEqual(mem[0x7ffff7a34271], b'*')
        self.assertEqual(mem[0x7ffff7a34272], b'\x00')
        self.assertEqual(mem[0x7ffff7a34273], b'\x00')
        self.assertEqual(mem[0x7ffff7a34274], b'\x1a')
        self.assertEqual(mem[0x7ffff7a34275], b'\x00')
        self.assertEqual(mem[0x7ffff7a34276], b'\x0b')
        self.assertEqual(mem[0x7ffff7a34277], b'\x00')
        self.assertEqual(cpu.RDX, 140737348059760)
        self.assertEqual(cpu.RIP, 140737349259032)
        self.assertEqual(cpu.RBX, 140737348050280)

    def test_LEA_5(self):
        ''' Instruction LEA_5
            Groups:
            0x7ffff7a652b7:	lea	rsi, qword ptr [rip + 0x36e35a]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a65000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd3000, 0x1000, 'rwx')
        mem[0x7ffff7dd3618] = '@'
        mem[0x7ffff7dd3619] = 'M'
        mem[0x7ffff7dd361a] = '\xdd'
        mem[0x7ffff7dd361b] = '\xf7'
        mem[0x7ffff7dd361c] = '\xff'
        mem[0x7ffff7dd361d] = '\x7f'
        mem[0x7ffff7dd361e] = '\x00'
        mem[0x7ffff7dd361f] = '\x00'
        mem[0x7ffff7a652b7] = 'H'
        mem[0x7ffff7a652b8] = '\x8d'
        mem[0x7ffff7a652b9] = '5'
        mem[0x7ffff7a652ba] = 'Z'
        mem[0x7ffff7a652bb] = '\xe3'
        mem[0x7ffff7a652bc] = '6'
        mem[0x7ffff7a652bd] = '\x00'
        cpu.RSI = 0x555555554a00
        cpu.RIP = 0x7ffff7a652b7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7dd3618], b'@')
        self.assertEqual(mem[0x7ffff7dd3619], b'M')
        self.assertEqual(mem[0x7ffff7dd361a], b'\xdd')
        self.assertEqual(mem[0x7ffff7dd361b], b'\xf7')
        self.assertEqual(mem[0x7ffff7dd361c], b'\xff')
        self.assertEqual(mem[0x7ffff7dd361d], b'\x7f')
        self.assertEqual(mem[0x7ffff7dd361e], b'\x00')
        self.assertEqual(mem[0x7ffff7dd361f], b'\x00')
        self.assertEqual(mem[0x7ffff7a652b7], b'H')
        self.assertEqual(mem[0x7ffff7a652b8], b'\x8d')
        self.assertEqual(mem[0x7ffff7a652b9], b'5')
        self.assertEqual(mem[0x7ffff7a652ba], b'Z')
        self.assertEqual(mem[0x7ffff7a652bb], b'\xe3')
        self.assertEqual(mem[0x7ffff7a652bc], b'6')
        self.assertEqual(mem[0x7ffff7a652bd], b'\x00')
        self.assertEqual(cpu.RSI, 140737351857688)
        self.assertEqual(cpu.RIP, 140737348260542)

    def test_LEA_6(self):
        ''' Instruction LEA_6
            Groups:
            0x7ffff7de4418:	lea	rdi, qword ptr [rbp - 0xa0]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd910] = '\xff'
        mem[0x7fffffffd911] = '\xff'
        mem[0x7fffffffd912] = '\xff'
        mem[0x7fffffffd913] = '\xff'
        mem[0x7fffffffd914] = '\x00'
        mem[0x7fffffffd915] = '\x00'
        mem[0x7fffffffd916] = '\x00'
        mem[0x7fffffffd917] = '\x00'
        mem[0x7ffff7de4418] = 'H'
        mem[0x7ffff7de4419] = '\x8d'
        mem[0x7ffff7de441a] = '\xbd'
        mem[0x7ffff7de441b] = '`'
        mem[0x7ffff7de441c] = '\xff'
        mem[0x7ffff7de441d] = '\xff'
        mem[0x7ffff7de441e] = '\xff'
        cpu.RDI = 0x555555554548
        cpu.RIP = 0x7ffff7de4418
        cpu.RBP = 0x7fffffffd9b0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd910], b'\xff')
        self.assertEqual(mem[0x7fffffffd911], b'\xff')
        self.assertEqual(mem[0x7fffffffd912], b'\xff')
        self.assertEqual(mem[0x7fffffffd913], b'\xff')
        self.assertEqual(mem[0x7fffffffd914], b'\x00')
        self.assertEqual(mem[0x7fffffffd915], b'\x00')
        self.assertEqual(mem[0x7fffffffd916], b'\x00')
        self.assertEqual(mem[0x7fffffffd917], b'\x00')
        self.assertEqual(mem[0x7ffff7de4418], b'H')
        self.assertEqual(mem[0x7ffff7de4419], b'\x8d')
        self.assertEqual(mem[0x7ffff7de441a], b'\xbd')
        self.assertEqual(mem[0x7ffff7de441b], b'`')
        self.assertEqual(mem[0x7ffff7de441c], b'\xff')
        self.assertEqual(mem[0x7ffff7de441d], b'\xff')
        self.assertEqual(mem[0x7ffff7de441e], b'\xff')
        self.assertEqual(cpu.RDI, 140737488345360)
        self.assertEqual(cpu.RIP, 140737351926815)
        self.assertEqual(cpu.RBP, 140737488345520)

    def test_MOVABS_1(self):
        ''' Instruction MOVABS_1
            Groups:
            0x7ffff7ddc5df:	movabs	r8, 0x37ffff1a0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddc000, 0x1000, 'rwx')
        mem[0x7ffff7ddc5e0] = '\xb8'
        mem[0x7ffff7ddc5e1] = '\xa0'
        mem[0x7ffff7ddc5e2] = '\xf1'
        mem[0x7ffff7ddc5e3] = '\xff'
        mem[0x7ffff7ddc5e4] = '\x7f'
        mem[0x7ffff7ddc5e5] = '\x03'
        mem[0x7ffff7ddc5e6] = '\x00'
        mem[0x7ffff7ddc5e7] = '\x00'
        mem[0x7ffff7ddc5e8] = '\x00'
        mem[0x7ffff7ddc5df] = 'I'
        cpu.R8 = 0x0
        cpu.RIP = 0x7ffff7ddc5df
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddc5e0], b'\xb8')
        self.assertEqual(mem[0x7ffff7ddc5e1], b'\xa0')
        self.assertEqual(mem[0x7ffff7ddc5e2], b'\xf1')
        self.assertEqual(mem[0x7ffff7ddc5e3], b'\xff')
        self.assertEqual(mem[0x7ffff7ddc5e4], b'\x7f')
        self.assertEqual(mem[0x7ffff7ddc5e5], b'\x03')
        self.assertEqual(mem[0x7ffff7ddc5e6], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5e7], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5e8], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5df], b'I')
        self.assertEqual(cpu.R8, 15032381856)
        self.assertEqual(cpu.RIP, 140737351894505)

    def test_MOVABS_2(self):
        ''' Instruction MOVABS_2
            Groups:
            0x7ffff7ddc5df:	movabs	r8, 0x37ffff1a0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddc000, 0x1000, 'rwx')
        mem[0x7ffff7ddc5e0] = '\xb8'
        mem[0x7ffff7ddc5e1] = '\xa0'
        mem[0x7ffff7ddc5e2] = '\xf1'
        mem[0x7ffff7ddc5e3] = '\xff'
        mem[0x7ffff7ddc5e4] = '\x7f'
        mem[0x7ffff7ddc5e5] = '\x03'
        mem[0x7ffff7ddc5e6] = '\x00'
        mem[0x7ffff7ddc5e7] = '\x00'
        mem[0x7ffff7ddc5e8] = '\x00'
        mem[0x7ffff7ddc5df] = 'I'
        cpu.R8 = 0x0
        cpu.RIP = 0x7ffff7ddc5df
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddc5e0], b'\xb8')
        self.assertEqual(mem[0x7ffff7ddc5e1], b'\xa0')
        self.assertEqual(mem[0x7ffff7ddc5e2], b'\xf1')
        self.assertEqual(mem[0x7ffff7ddc5e3], b'\xff')
        self.assertEqual(mem[0x7ffff7ddc5e4], b'\x7f')
        self.assertEqual(mem[0x7ffff7ddc5e5], b'\x03')
        self.assertEqual(mem[0x7ffff7ddc5e6], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5e7], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5e8], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5df], b'I')
        self.assertEqual(cpu.R8, 15032381856)
        self.assertEqual(cpu.RIP, 140737351894505)

    def test_MOVABS_3(self):
        ''' Instruction MOVABS_3
            Groups:
            0x7ffff7df1435:	movabs	rcx, -0x8000000000000000
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1435] = 'H'
        mem[0x7ffff7df1436] = '\xb9'
        mem[0x7ffff7df1437] = '\x00'
        mem[0x7ffff7df1438] = '\x00'
        mem[0x7ffff7df1439] = '\x00'
        mem[0x7ffff7df143a] = '\x00'
        mem[0x7ffff7df143b] = '\x00'
        mem[0x7ffff7df143c] = '\x00'
        mem[0x7ffff7df143d] = '\x00'
        mem[0x7ffff7df143e] = '\x80'
        cpu.RCX = 0x31
        cpu.RIP = 0x7ffff7df1435
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1435], b'H')
        self.assertEqual(mem[0x7ffff7df1436], b'\xb9')
        self.assertEqual(mem[0x7ffff7df1437], b'\x00')
        self.assertEqual(mem[0x7ffff7df1438], b'\x00')
        self.assertEqual(mem[0x7ffff7df1439], b'\x00')
        self.assertEqual(mem[0x7ffff7df143a], b'\x00')
        self.assertEqual(mem[0x7ffff7df143b], b'\x00')
        self.assertEqual(mem[0x7ffff7df143c], b'\x00')
        self.assertEqual(mem[0x7ffff7df143d], b'\x00')
        self.assertEqual(mem[0x7ffff7df143e], b'\x80')
        self.assertEqual(cpu.RCX, 9223372036854775808)
        self.assertEqual(cpu.RIP, 140737351980095)

    def test_MOVABS_4(self):
        ''' Instruction MOVABS_4
            Groups:
            0x45f853:	movabs	rdx, -0x3333333333333333
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0045f000, 0x1000, 'rwx')
        mem[0x0045f853] = 'H'
        mem[0x0045f854] = '\xba'
        mem[0x0045f855] = '\xcd'
        mem[0x0045f856] = '\xcc'
        mem[0x0045f857] = '\xcc'
        mem[0x0045f858] = '\xcc'
        mem[0x0045f859] = '\xcc'
        mem[0x0045f85a] = '\xcc'
        mem[0x0045f85b] = '\xcc'
        mem[0x0045f85c] = '\xcc'
        cpu.RDX = 0x6bf710
        cpu.RIP = 0x45f853
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x45f853], b'H')
        self.assertEqual(mem[0x45f854], b'\xba')
        self.assertEqual(mem[0x45f855], b'\xcd')
        self.assertEqual(mem[0x45f856], b'\xcc')
        self.assertEqual(mem[0x45f857], b'\xcc')
        self.assertEqual(mem[0x45f858], b'\xcc')
        self.assertEqual(mem[0x45f859], b'\xcc')
        self.assertEqual(mem[0x45f85a], b'\xcc')
        self.assertEqual(mem[0x45f85b], b'\xcc')
        self.assertEqual(mem[0x45f85c], b'\xcc')
        self.assertEqual(cpu.RDX, 14757395258967641293)
        self.assertEqual(cpu.RIP, 4585565)

    def test_MOVABS_5(self):
        ''' Instruction MOVABS_5
            Groups:
            0x7ffff7df4630:	movabs	r8, -0x101010101010101
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4630] = 'I'
        mem[0x7ffff7df4631] = '\xb8'
        mem[0x7ffff7df4632] = '\xff'
        mem[0x7ffff7df4633] = '\xfe'
        mem[0x7ffff7df4634] = '\xfe'
        mem[0x7ffff7df4635] = '\xfe'
        mem[0x7ffff7df4636] = '\xfe'
        mem[0x7ffff7df4637] = '\xfe'
        mem[0x7ffff7df4638] = '\xfe'
        mem[0x7ffff7df4639] = '\xfe'
        cpu.R8 = 0x7ffff7fdd5a0
        cpu.RIP = 0x7ffff7df4630
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4630], b'I')
        self.assertEqual(mem[0x7ffff7df4631], b'\xb8')
        self.assertEqual(mem[0x7ffff7df4632], b'\xff')
        self.assertEqual(mem[0x7ffff7df4633], b'\xfe')
        self.assertEqual(mem[0x7ffff7df4634], b'\xfe')
        self.assertEqual(mem[0x7ffff7df4635], b'\xfe')
        self.assertEqual(mem[0x7ffff7df4636], b'\xfe')
        self.assertEqual(mem[0x7ffff7df4637], b'\xfe')
        self.assertEqual(mem[0x7ffff7df4638], b'\xfe')
        self.assertEqual(mem[0x7ffff7df4639], b'\xfe')
        self.assertEqual(cpu.R8, 18374403900871474943)
        self.assertEqual(cpu.RIP, 140737351992890)

    def test_MOVABS_6(self):
        ''' Instruction MOVABS_6
            Groups:
            0x7ffff7ddc5df:	movabs	r8, 0x37ffff1a0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddc000, 0x1000, 'rwx')
        mem[0x7ffff7ddc5e0] = '\xb8'
        mem[0x7ffff7ddc5e1] = '\xa0'
        mem[0x7ffff7ddc5e2] = '\xf1'
        mem[0x7ffff7ddc5e3] = '\xff'
        mem[0x7ffff7ddc5e4] = '\x7f'
        mem[0x7ffff7ddc5e5] = '\x03'
        mem[0x7ffff7ddc5e6] = '\x00'
        mem[0x7ffff7ddc5e7] = '\x00'
        mem[0x7ffff7ddc5e8] = '\x00'
        mem[0x7ffff7ddc5df] = 'I'
        cpu.R8 = 0x0
        cpu.RIP = 0x7ffff7ddc5df
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddc5e0], b'\xb8')
        self.assertEqual(mem[0x7ffff7ddc5e1], b'\xa0')
        self.assertEqual(mem[0x7ffff7ddc5e2], b'\xf1')
        self.assertEqual(mem[0x7ffff7ddc5e3], b'\xff')
        self.assertEqual(mem[0x7ffff7ddc5e4], b'\x7f')
        self.assertEqual(mem[0x7ffff7ddc5e5], b'\x03')
        self.assertEqual(mem[0x7ffff7ddc5e6], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5e7], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5e8], b'\x00')
        self.assertEqual(mem[0x7ffff7ddc5df], b'I')
        self.assertEqual(cpu.R8, 15032381856)
        self.assertEqual(cpu.RIP, 140737351894505)

    def test_MOVDQA_1(self):
        ''' Instruction MOVDQA_1
            Groups: sse2
            0x7ffff7ac0b0b:	movdqa	xmm4, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0b0b] = 'f'
        mem[0x7ffff7ac0b0c] = '\x0f'
        mem[0x7ffff7ac0b0d] = 'o'
        mem[0x7ffff7ac0b0e] = '\xe0'
        cpu.XMM0 = 0x616572635f706374746e6c63000a7325
        cpu.RIP = 0x7ffff7ac0b0b
        cpu.XMM4 = 0xff0000000000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0b0b], b'f')
        self.assertEqual(mem[0x7ffff7ac0b0c], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0b0d], b'o')
        self.assertEqual(mem[0x7ffff7ac0b0e], b'\xe0')
        self.assertEqual(cpu.XMM0, 129461857641668707752067115693843837733)
        self.assertEqual(cpu.XMM4, 129461857641668707752067115693843837733)
        self.assertEqual(cpu.RIP, 140737348635407)

    def test_MOVDQA_2(self):
        ''' Instruction MOVDQA_2
            Groups: sse2
            0x457d38:	movdqa	xmm0, xmm2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457d38] = 'f'
        mem[0x00457d39] = '\x0f'
        mem[0x00457d3a] = 'o'
        mem[0x00457d3b] = '\xc2'
        cpu.XMM2 = 0x414d00323d524e54565f474458003267
        cpu.XMM0 = 0xff0000
        cpu.RIP = 0x457d38
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457d38], b'f')
        self.assertEqual(mem[0x457d39], b'\x0f')
        self.assertEqual(mem[0x457d3a], b'o')
        self.assertEqual(mem[0x457d3b], b'\xc2')
        self.assertEqual(cpu.XMM2, 86799630564512926596007573190145487463)
        self.assertEqual(cpu.XMM0, 86799630564512926596007573190145487463)
        self.assertEqual(cpu.RIP, 4554044)

    def test_MOVDQA_3(self):
        ''' Instruction MOVDQA_3
            Groups: sse2
            0x457aaf:	movdqa	xmm5, xmm3
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457ab0] = '\x0f'
        mem[0x00457ab1] = 'o'
        mem[0x00457ab2] = '\xeb'
        mem[0x00457aaf] = 'f'
        cpu.XMM3 = 0x726f74756365784563696c6f626d7953
        cpu.RIP = 0x457aaf
        cpu.XMM5 = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457ab0], b'\x0f')
        self.assertEqual(mem[0x457ab1], b'o')
        self.assertEqual(mem[0x457ab2], b'\xeb')
        self.assertEqual(mem[0x457aaf], b'f')
        self.assertEqual(cpu.XMM3, 152110698530748498584558466992035428691)
        self.assertEqual(cpu.RIP, 4553395)
        self.assertEqual(cpu.XMM5, 152110698530748498584558466992035428691)

    def test_MOVDQA_4(self):
        ''' Instruction MOVDQA_4
            Groups: sse2
            0x457a08:	movdqa	xmm2, xmmword ptr [rdi + 0x30]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        mem[0x00457a08] = 'f'
        mem[0x00457a09] = '\x0f'
        mem[0x00457a0a] = 'o'
        mem[0x00457a0b] = 'W'
        mem[0x00457a0c] = '0'
        mem[0x7fffffffe070] = 'D'
        mem[0x7fffffffe071] = 'G'
        mem[0x7fffffffe072] = '_'
        mem[0x7fffffffe073] = 'V'
        mem[0x7fffffffe074] = 'T'
        mem[0x7fffffffe075] = 'N'
        mem[0x7fffffffe076] = 'R'
        mem[0x7fffffffe077] = '='
        mem[0x7fffffffe078] = '2'
        mem[0x7fffffffe079] = '\x00'
        mem[0x7fffffffe07a] = 'M'
        mem[0x7fffffffe07b] = 'A'
        mem[0x7fffffffe07c] = 'N'
        mem[0x7fffffffe07d] = 'P'
        mem[0x7fffffffe07e] = 'A'
        mem[0x7fffffffe07f] = 'T'
        cpu.XMM2 = 0x0
        cpu.RDI = 0x7fffffffe040
        cpu.RIP = 0x457a08
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457a08], b'f')
        self.assertEqual(mem[0x457a09], b'\x0f')
        self.assertEqual(mem[0x457a0a], b'o')
        self.assertEqual(mem[0x457a0b], b'W')
        self.assertEqual(mem[0x457a0c], b'0')
        self.assertEqual(mem[0x7fffffffe070], b'D')
        self.assertEqual(mem[0x7fffffffe071], b'G')
        self.assertEqual(mem[0x7fffffffe072], b'_')
        self.assertEqual(mem[0x7fffffffe073], b'V')
        self.assertEqual(mem[0x7fffffffe074], b'T')
        self.assertEqual(mem[0x7fffffffe075], b'N')
        self.assertEqual(mem[0x7fffffffe076], b'R')
        self.assertEqual(mem[0x7fffffffe077], b'=')
        self.assertEqual(mem[0x7fffffffe078], b'2')
        self.assertEqual(mem[0x7fffffffe079], b'\x00')
        self.assertEqual(mem[0x7fffffffe07a], b'M')
        self.assertEqual(mem[0x7fffffffe07b], b'A')
        self.assertEqual(mem[0x7fffffffe07c], b'N')
        self.assertEqual(mem[0x7fffffffe07d], b'P')
        self.assertEqual(mem[0x7fffffffe07e], b'A')
        self.assertEqual(mem[0x7fffffffe07f], b'T')
        self.assertEqual(cpu.XMM2, 111994279734512279219280163309057165124)
        self.assertEqual(cpu.RDI, 140737488347200)
        self.assertEqual(cpu.RIP, 4553229)

    def test_MOVDQA_5(self):
        ''' Instruction MOVDQA_5
            Groups: sse2
            0x457b38:	movdqa	xmm0, xmm2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457b38] = 'f'
        mem[0x00457b39] = '\x0f'
        mem[0x00457b3a] = 'o'
        mem[0x00457b3b] = '\xc2'
        cpu.XMM2 = 0x504e414d00323d524e54565f47445800
        cpu.XMM0 = 0x0
        cpu.RIP = 0x457b38
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457b38], b'f')
        self.assertEqual(mem[0x457b39], b'\x0f')
        self.assertEqual(mem[0x457b3a], b'o')
        self.assertEqual(mem[0x457b3b], b'\xc2')
        self.assertEqual(cpu.XMM2, 106744563275012473217874926561820694528)
        self.assertEqual(cpu.XMM0, 106744563275012473217874926561820694528)
        self.assertEqual(cpu.RIP, 4553532)

    def test_MOVDQA_6(self):
        ''' Instruction MOVDQA_6
            Groups: sse2
            0x7ffff7ac0b0b:	movdqa	xmm4, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0b0b] = 'f'
        mem[0x7ffff7ac0b0c] = '\x0f'
        mem[0x7ffff7ac0b0d] = 'o'
        mem[0x7ffff7ac0b0e] = '\xe0'
        cpu.XMM0 = 0xcd202730fa0892a58d0000007fffff00
        cpu.RIP = 0x7ffff7ac0b0b
        cpu.XMM4 = 0xffffff000000ff0000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0b0b], b'f')
        self.assertEqual(mem[0x7ffff7ac0b0c], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0b0d], b'o')
        self.assertEqual(mem[0x7ffff7ac0b0e], b'\xe0')
        self.assertEqual(cpu.XMM0, 272658687529688827910500737779280903936)
        self.assertEqual(cpu.XMM4, 272658687529688827910500737779280903936)
        self.assertEqual(cpu.RIP, 140737348635407)

    def test_MOVDQU_1(self):
        ''' Instruction MOVDQU_1
            Groups: sse2
            0x6a74d4:	movdqu	xmm0, xmmword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x006a7000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb4] = '!'
        mem[0x006a74d6] = 'o'
        mem[0x7fffffffccb8] = '\x01'
        mem[0x006a74d7] = '\x04'
        mem[0x7fffffffccb0] = '\xff'
        mem[0x7fffffffccb1] = '\x7f'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x006a74d4] = '\xf3'
        mem[0x006a74d5] = '\x0f'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x006a74d8] = '$'
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x80'
        mem[0x7fffffffccbc] = '\xff'
        mem[0x7fffffffccbd] = '\x7f'
        mem[0x7fffffffccbe] = '\x00'
        mem[0x7fffffffccbf] = '\x00'
        cpu.XMM0 = 0x7fff800000000000002100007fff
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x6a74d4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffccbb], b'\x80')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccbf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'\xff')
        self.assertEqual(mem[0x7fffffffccb1], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x6a74d4], b'\xf3')
        self.assertEqual(mem[0x6a74d5], b'\x0f')
        self.assertEqual(mem[0x6a74d6], b'o')
        self.assertEqual(mem[0x6a74d7], b'\x04')
        self.assertEqual(mem[0x6a74d8], b'$')
        self.assertEqual(mem[0x7fffffffccb4], b'!')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'\x01')
        self.assertEqual(mem[0x7fffffffccbc], b'\xff')
        self.assertEqual(mem[0x7fffffffccbd], b'\x7f')
        self.assertEqual(mem[0x7fffffffccbe], b'\x00')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(cpu.XMM0, 2596108815186175128840666836140031)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 6976729)

    def test_MOVDQU_2(self):
        ''' Instruction MOVDQU_2
            Groups: sse2
            0x568fac:	movdqu	xmm0, xmmword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00568000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x00568fb0] = '$'
        mem[0x00568fac] = '\xf3'
        mem[0x00568fad] = '\x0f'
        mem[0x00568fae] = 'o'
        mem[0x00568faf] = '\x04'
        mem[0x7fffffffccb0] = 'x'
        mem[0x7fffffffccb1] = 'V'
        mem[0x7fffffffccb2] = '4'
        mem[0x7fffffffccb3] = '\x12'
        mem[0x7fffffffccb4] = '\xff'
        mem[0x7fffffffccb5] = '\x7f'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = '\x01'
        mem[0x7fffffffccb9] = '\x80'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        mem[0x7fffffffccbc] = 'x'
        mem[0x7fffffffccbd] = 'V'
        mem[0x7fffffffccbe] = '4'
        mem[0x7fffffffccbf] = '\x12'
        cpu.XMM0 = 0x1234567800007fff00007fff12345678
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x568fac
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffccb0], b'x')
        self.assertEqual(mem[0x568fac], b'\xf3')
        self.assertEqual(mem[0x568fad], b'\x0f')
        self.assertEqual(mem[0x568fae], b'o')
        self.assertEqual(mem[0x568faf], b'\x04')
        self.assertEqual(mem[0x568fb0], b'$')
        self.assertEqual(mem[0x7fffffffccb1], b'V')
        self.assertEqual(mem[0x7fffffffccb2], b'4')
        self.assertEqual(mem[0x7fffffffccb3], b'\x12')
        self.assertEqual(mem[0x7fffffffccb4], b'\xff')
        self.assertEqual(mem[0x7fffffffccb5], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'\x01')
        self.assertEqual(mem[0x7fffffffccb9], b'\x80')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(mem[0x7fffffffccbc], b'x')
        self.assertEqual(mem[0x7fffffffccbd], b'V')
        self.assertEqual(mem[0x7fffffffccbe], b'4')
        self.assertEqual(mem[0x7fffffffccbf], b'\x12')
        self.assertEqual(cpu.XMM0, 24197857155378316985685775704845997688)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5672881)

    def test_MOVDQU_3(self):
        ''' Instruction MOVDQU_3
            Groups: sse2
            0x6f4c12:	movdqu	xmm1, xmmword ptr [rsp + 4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x006f4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x006f4c12] = '\xf3'
        mem[0x006f4c13] = '\x0f'
        mem[0x006f4c14] = 'o'
        mem[0x006f4c15] = 'L'
        mem[0x006f4c16] = '$'
        mem[0x006f4c17] = '\x04'
        mem[0x7fffffffccb4] = '\xff'
        mem[0x7fffffffccb5] = '\x7f'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = ' '
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        mem[0x7fffffffccbc] = '!'
        mem[0x7fffffffccbd] = '\x00'
        mem[0x7fffffffccbe] = '\x00'
        mem[0x7fffffffccbf] = '\x00'
        mem[0x7fffffffccc0] = '\xff'
        mem[0x7fffffffccc1] = '\x7f'
        mem[0x7fffffffccc2] = '\x00'
        mem[0x7fffffffccc3] = '\x00'
        cpu.XMM1 = 0x7fff000000210000002100007fff
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x6f4c12
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x6f4c12], b'\xf3')
        self.assertEqual(mem[0x6f4c13], b'\x0f')
        self.assertEqual(mem[0x6f4c14], b'o')
        self.assertEqual(mem[0x6f4c15], b'L')
        self.assertEqual(mem[0x6f4c16], b'$')
        self.assertEqual(mem[0x6f4c17], b'\x04')
        self.assertEqual(mem[0x7fffffffccb4], b'\xff')
        self.assertEqual(mem[0x7fffffffccb5], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b' ')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(mem[0x7fffffffccbc], b'!')
        self.assertEqual(mem[0x7fffffffccbd], b'\x00')
        self.assertEqual(mem[0x7fffffffccbe], b'\x00')
        self.assertEqual(mem[0x7fffffffccbf], b'\x00')
        self.assertEqual(mem[0x7fffffffccc0], b'\xff')
        self.assertEqual(mem[0x7fffffffccc1], b'\x7f')
        self.assertEqual(mem[0x7fffffffccc2], b'\x00')
        self.assertEqual(mem[0x7fffffffccc3], b'\x00')
        self.assertEqual(cpu.XMM1, 2596069201105508292482224474849279)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 7293976)

    def test_MOVDQU_4(self):
        ''' Instruction MOVDQU_4
            Groups: sse2
            0x56fa50:	movdqu	xmm1, xmmword ptr [rsp + 4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0056f000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffccb4] = ' '
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = '!'
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        mem[0x7fffffffccbc] = '!'
        mem[0x7fffffffccbd] = 'C'
        mem[0x7fffffffccbe] = 'e'
        mem[0x7fffffffccbf] = '\x87'
        mem[0x7fffffffccc0] = ' '
        mem[0x7fffffffccc1] = '\x00'
        mem[0x7fffffffccc2] = '\x00'
        mem[0x7fffffffccc3] = '\x00'
        mem[0x0056fa50] = '\xf3'
        mem[0x0056fa51] = '\x0f'
        mem[0x0056fa52] = 'o'
        mem[0x0056fa53] = 'L'
        mem[0x0056fa54] = '$'
        mem[0x0056fa55] = '\x04'
        cpu.XMM1 = 0x20876543218765432100000020
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x56fa50
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffccb4], b' ')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'!')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(mem[0x7fffffffccbc], b'!')
        self.assertEqual(mem[0x7fffffffccbd], b'C')
        self.assertEqual(mem[0x7fffffffccbe], b'e')
        self.assertEqual(mem[0x7fffffffccbf], b'\x87')
        self.assertEqual(mem[0x7fffffffccc0], b' ')
        self.assertEqual(mem[0x7fffffffccc1], b'\x00')
        self.assertEqual(mem[0x7fffffffccc2], b'\x00')
        self.assertEqual(mem[0x7fffffffccc3], b'\x00')
        self.assertEqual(mem[0x56fa50], b'\xf3')
        self.assertEqual(mem[0x56fa51], b'\x0f')
        self.assertEqual(mem[0x56fa52], b'o')
        self.assertEqual(mem[0x56fa53], b'L')
        self.assertEqual(mem[0x56fa54], b'$')
        self.assertEqual(mem[0x56fa55], b'\x04')
        self.assertEqual(cpu.XMM1, 2577204095297418371658275618848)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5700182)

    def test_MOVDQU_5(self):
        ''' Instruction MOVDQU_5
            Groups: sse2
            0x606649:	movdqu	xmm1, xmmword ptr [rsp + 4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00606000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffccb4] = '\xff'
        mem[0x7fffffffccb5] = '\xff'
        mem[0x7fffffffccb6] = '\xff'
        mem[0x7fffffffccb7] = '\xff'
        mem[0x7fffffffccb8] = '\x01'
        mem[0x7fffffffccb9] = '\x80'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        mem[0x7fffffffccbc] = '\x01'
        mem[0x7fffffffccbd] = '\x80'
        mem[0x7fffffffccbe] = '\x00'
        mem[0x7fffffffccbf] = '\x00'
        mem[0x7fffffffccc0] = '\xff'
        mem[0x7fffffffccc1] = '\xff'
        mem[0x7fffffffccc2] = '\xff'
        mem[0x7fffffffccc3] = '\xff'
        mem[0x00606649] = '\xf3'
        mem[0x0060664a] = '\x0f'
        mem[0x0060664b] = 'o'
        mem[0x0060664c] = 'L'
        mem[0x0060664d] = '$'
        mem[0x0060664e] = '\x04'
        cpu.XMM1 = 0xffffffff0000800100007fffffffffff
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x606649
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffccb4], b'\xff')
        self.assertEqual(mem[0x7fffffffccb5], b'\xff')
        self.assertEqual(mem[0x7fffffffccb6], b'\xff')
        self.assertEqual(mem[0x7fffffffccb7], b'\xff')
        self.assertEqual(mem[0x7fffffffccb8], b'\x01')
        self.assertEqual(mem[0x7fffffffccb9], b'\x80')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(mem[0x7fffffffccbc], b'\x01')
        self.assertEqual(mem[0x7fffffffccbd], b'\x80')
        self.assertEqual(mem[0x7fffffffccbe], b'\x00')
        self.assertEqual(mem[0x7fffffffccbf], b'\x00')
        self.assertEqual(mem[0x7fffffffccc0], b'\xff')
        self.assertEqual(mem[0x7fffffffccc1], b'\xff')
        self.assertEqual(mem[0x7fffffffccc2], b'\xff')
        self.assertEqual(mem[0x7fffffffccc3], b'\xff')
        self.assertEqual(mem[0x606649], b'\xf3')
        self.assertEqual(mem[0x60664a], b'\x0f')
        self.assertEqual(mem[0x60664b], b'o')
        self.assertEqual(mem[0x60664c], b'L')
        self.assertEqual(mem[0x60664d], b'$')
        self.assertEqual(mem[0x60664e], b'\x04')
        self.assertEqual(cpu.XMM1, 340282366841710905430466961972599455743)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 6317647)

    def test_MOVDQU_6(self):
        ''' Instruction MOVDQU_6
            Groups: sse2
            0x6fc91e:	movdqu	xmm0, xmmword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x006fc000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x006fc920] = 'o'
        mem[0x006fc921] = '\x04'
        mem[0x006fc922] = '$'
        mem[0x006fc91f] = '\x0f'
        mem[0x006fc91e] = '\xf3'
        mem[0x7fffffffccb0] = '@'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x7fffffffccb4] = '\x01'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x80'
        mem[0x7fffffffccb8] = '\x01'
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x80'
        mem[0x7fffffffccbc] = '@'
        mem[0x7fffffffccbd] = '\x00'
        mem[0x7fffffffccbe] = '\x00'
        mem[0x7fffffffccbf] = '\x00'
        cpu.XMM0 = 0x40800000008000000100000040
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x6fc91e
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x6fc920], b'o')
        self.assertEqual(mem[0x6fc921], b'\x04')
        self.assertEqual(mem[0x6fc922], b'$')
        self.assertEqual(mem[0x7fffffffccbf], b'\x00')
        self.assertEqual(mem[0x7fffffffccbe], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'@')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x7fffffffccb4], b'\x01')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x80')
        self.assertEqual(mem[0x7fffffffccb8], b'\x01')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x80')
        self.assertEqual(mem[0x7fffffffccbc], b'@')
        self.assertEqual(mem[0x7fffffffccbd], b'\x00')
        self.assertEqual(mem[0x6fc91e], b'\xf3')
        self.assertEqual(mem[0x6fc91f], b'\x0f')
        self.assertEqual(cpu.XMM0, 5110216482197719890898444091456)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 7325987)

    def test_MOVD_1(self):
        ''' Instruction MOVD_1
            Groups: sse2
            0x7ffff7df4370:	movd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4370] = 'f'
        mem[0x7ffff7df4371] = '\x0f'
        mem[0x7ffff7df4372] = 'n'
        mem[0x7ffff7df4373] = '\xce'
        cpu.XMM1 = 0x24242424242424242424242424242424
        cpu.RIP = 0x7ffff7df4370
        cpu.ESI = 0x2f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4370], b'f')
        self.assertEqual(mem[0x7ffff7df4371], b'\x0f')
        self.assertEqual(mem[0x7ffff7df4372], b'n')
        self.assertEqual(mem[0x7ffff7df4373], b'\xce')
        self.assertEqual(cpu.XMM1, 47)
        self.assertEqual(cpu.ESI, 47)
        self.assertEqual(cpu.RIP, 140737351992180)

    def test_MOVD_2(self):
        ''' Instruction MOVD_2
            Groups: sse2
            0x7ffff7ab7980:	movd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab7000, 0x1000, 'rwx')
        mem[0x7ffff7ab7980] = 'f'
        mem[0x7ffff7ab7981] = '\x0f'
        mem[0x7ffff7ab7982] = 'n'
        mem[0x7ffff7ab7983] = '\xce'
        cpu.XMM1 = 0x24242424242424242424242424242424
        cpu.RIP = 0x7ffff7ab7980
        cpu.ESI = 0x2f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab7980], b'f')
        self.assertEqual(mem[0x7ffff7ab7981], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab7982], b'n')
        self.assertEqual(mem[0x7ffff7ab7983], b'\xce')
        self.assertEqual(cpu.XMM1, 47)
        self.assertEqual(cpu.ESI, 47)
        self.assertEqual(cpu.RIP, 140737348598148)

    def test_MOVD_3(self):
        ''' Instruction MOVD_3
            Groups: sse2
            0x4578e0:	movd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x004578e0] = 'f'
        mem[0x004578e1] = '\x0f'
        mem[0x004578e2] = 'n'
        mem[0x004578e3] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x4578e0
        cpu.ESI = 0x2f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4578e0], b'f')
        self.assertEqual(mem[0x4578e1], b'\x0f')
        self.assertEqual(mem[0x4578e2], b'n')
        self.assertEqual(mem[0x4578e3], b'\xce')
        self.assertEqual(cpu.XMM1, 47)
        self.assertEqual(cpu.ESI, 47)
        self.assertEqual(cpu.RIP, 4552932)

    def test_MOVD_4(self):
        ''' Instruction MOVD_4
            Groups: sse2
            0x421b10:	movd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00421000, 0x1000, 'rwx')
        mem[0x00421b10] = 'f'
        mem[0x00421b11] = '\x0f'
        mem[0x00421b12] = 'n'
        mem[0x00421b13] = '\xce'
        cpu.XMM1 = 0x25252525252525252525252525252525
        cpu.RIP = 0x421b10
        cpu.ESI = 0x25
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x421b10], b'f')
        self.assertEqual(mem[0x421b11], b'\x0f')
        self.assertEqual(mem[0x421b12], b'n')
        self.assertEqual(mem[0x421b13], b'\xce')
        self.assertEqual(cpu.XMM1, 37)
        self.assertEqual(cpu.ESI, 37)
        self.assertEqual(cpu.RIP, 4332308)

    def test_MOVD_5(self):
        ''' Instruction MOVD_5
            Groups: sse2
            0x457da0:	movd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457da0] = 'f'
        mem[0x00457da1] = '\x0f'
        mem[0x00457da2] = 'n'
        mem[0x00457da3] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x457da0
        cpu.ESI = 0x2f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457da0], b'f')
        self.assertEqual(mem[0x457da1], b'\x0f')
        self.assertEqual(mem[0x457da2], b'n')
        self.assertEqual(mem[0x457da3], b'\xce')
        self.assertEqual(cpu.XMM1, 47)
        self.assertEqual(cpu.ESI, 47)
        self.assertEqual(cpu.RIP, 4554148)

    def test_MOVD_6(self):
        ''' Instruction MOVD_6
            Groups: sse2
            0x7ffff7ac0ae0:	movd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0ae0] = 'f'
        mem[0x7ffff7ac0ae1] = '\x0f'
        mem[0x7ffff7ac0ae2] = 'n'
        mem[0x7ffff7ac0ae3] = '\xce'
        cpu.XMM1 = 0x25252525252525252525252525252525
        cpu.RIP = 0x7ffff7ac0ae0
        cpu.ESI = 0x25
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0ae0], b'f')
        self.assertEqual(mem[0x7ffff7ac0ae1], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0ae2], b'n')
        self.assertEqual(mem[0x7ffff7ac0ae3], b'\xce')
        self.assertEqual(cpu.XMM1, 37)
        self.assertEqual(cpu.ESI, 37)
        self.assertEqual(cpu.RIP, 140737348635364)

    def test_MOVLPD_1(self):
        ''' Instruction MOVLPD_1
            Groups: sse2
            0x50f61f:	movlpd	xmm1, qword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0050f000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x0050f61f] = 'f'
        mem[0x0050f620] = '\x0f'
        mem[0x0050f621] = '\x12'
        mem[0x0050f622] = '\x0c'
        mem[0x0050f623] = '$'
        mem[0x7fffffffccb0] = '@'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x7fffffffccb4] = '\x80'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        cpu.XMM1 = 0x80000000400000008000000040
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x50f61f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x50f61f], b'f')
        self.assertEqual(mem[0x50f620], b'\x0f')
        self.assertEqual(mem[0x50f621], b'\x12')
        self.assertEqual(mem[0x50f622], b'\x0c')
        self.assertEqual(mem[0x50f623], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'@')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x7fffffffccb4], b'\x80')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(cpu.XMM1, 10141204803006426833240792760384)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5305892)

    def test_MOVLPD_2(self):
        ''' Instruction MOVLPD_2
            Groups: sse2
            0x4aa891:	movlpd	qword ptr [rsp], xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004aa000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x004aa891] = 'f'
        mem[0x004aa892] = '\x0f'
        mem[0x004aa893] = '\x13'
        mem[0x004aa894] = '\x0c'
        mem[0x004aa895] = '$'
        mem[0x7fffffffccb0] = '!'
        mem[0x7fffffffccb1] = 'C'
        mem[0x7fffffffccb2] = 'e'
        mem[0x7fffffffccb3] = '\x87'
        mem[0x7fffffffccb4] = '@'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        cpu.XMM1 = 0x87654321800000000000004087654321
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x4aa891
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4aa891], b'f')
        self.assertEqual(mem[0x4aa892], b'\x0f')
        self.assertEqual(mem[0x4aa893], b'\x13')
        self.assertEqual(mem[0x4aa894], b'\x0c')
        self.assertEqual(mem[0x4aa895], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'!')
        self.assertEqual(mem[0x7fffffffccb1], b'C')
        self.assertEqual(mem[0x7fffffffccb2], b'e')
        self.assertEqual(mem[0x7fffffffccb3], b'\x87')
        self.assertEqual(mem[0x7fffffffccb4], b'@')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(cpu.XMM1, 179971562989262549322269247393805714209)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 4892822)

    def test_MOVLPD_3(self):
        ''' Instruction MOVLPD_3
            Groups: sse2
            0x4adf87:	movlpd	qword ptr [rsp], xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004ad000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x004adf87] = 'f'
        mem[0x004adf88] = '\x0f'
        mem[0x004adf89] = '\x13'
        mem[0x004adf8a] = '\x0c'
        mem[0x004adf8b] = '$'
        mem[0x7fffffffccb0] = '\xfe'
        mem[0x7fffffffccb1] = '\xff'
        mem[0x7fffffffccb2] = '\xff'
        mem[0x7fffffffccb3] = '\xff'
        mem[0x7fffffffccb4] = '\x01'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x80'
        cpu.XMM1 = 0xfffffffe8000000180000001fffffffe
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x4adf87
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4adf87], b'f')
        self.assertEqual(mem[0x4adf88], b'\x0f')
        self.assertEqual(mem[0x4adf89], b'\x13')
        self.assertEqual(mem[0x4adf8a], b'\x0c')
        self.assertEqual(mem[0x4adf8b], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'\xfe')
        self.assertEqual(mem[0x7fffffffccb1], b'\xff')
        self.assertEqual(mem[0x7fffffffccb2], b'\xff')
        self.assertEqual(mem[0x7fffffffccb3], b'\xff')
        self.assertEqual(mem[0x7fffffffccb4], b'\x01')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x80')
        self.assertEqual(cpu.XMM1, 340282366802096219719648217160606547966)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 4906892)

    def test_MOVLPD_4(self):
        ''' Instruction MOVLPD_4
            Groups: sse2
            0x4acf88:	movlpd	qword ptr [rsp], xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004ac000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x004acf88] = 'f'
        mem[0x004acf89] = '\x0f'
        mem[0x004acf8a] = '\x13'
        mem[0x004acf8b] = '\x0c'
        mem[0x004acf8c] = '$'
        mem[0x7fffffffccb0] = '\xff'
        mem[0x7fffffffccb1] = '\x7f'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x7fffffffccb4] = '\x01'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x80'
        cpu.XMM1 = 0x7fff800000018000000100007fff
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x4acf88
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4acf88], b'f')
        self.assertEqual(mem[0x4acf89], b'\x0f')
        self.assertEqual(mem[0x4acf8a], b'\x13')
        self.assertEqual(mem[0x4acf8b], b'\x0c')
        self.assertEqual(mem[0x4acf8c], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'\xff')
        self.assertEqual(mem[0x7fffffffccb1], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x7fffffffccb4], b'\x01')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x80')
        self.assertEqual(cpu.XMM1, 2596108815186184352212566251962367)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 4902797)

    def test_MOVLPD_5(self):
        ''' Instruction MOVLPD_5
            Groups: sse2
            0x50a2c7:	movlpd	xmm1, qword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0050a000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x0050a2c7] = 'f'
        mem[0x0050a2c8] = '\x0f'
        mem[0x0050a2c9] = '\x12'
        mem[0x0050a2ca] = '\x0c'
        mem[0x0050a2cb] = '$'
        mem[0x7fffffffccb0] = ' '
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x7fffffffccb4] = '!'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        cpu.XMM1 = 0x21000000200000004000000021
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x50a2c7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x50a2c7], b'f')
        self.assertEqual(mem[0x50a2c8], b'\x0f')
        self.assertEqual(mem[0x50a2c9], b'\x12')
        self.assertEqual(mem[0x50a2ca], b'\x0c')
        self.assertEqual(mem[0x50a2cb], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b' ')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x7fffffffccb4], b'!')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(cpu.XMM1, 2614529363561018951087389933600)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5284556)

    def test_MOVLPD_6(self):
        ''' Instruction MOVLPD_6
            Groups: sse2
            0x4d851b:	movlpd	qword ptr [rsp], xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004d8000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x004d851b] = 'f'
        mem[0x004d851c] = '\x0f'
        mem[0x004d851d] = '\x13'
        mem[0x004d851e] = '\x0c'
        mem[0x004d851f] = '$'
        mem[0x7fffffffccb0] = '\xff'
        mem[0x7fffffffccb1] = '\x7f'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x7fffffffccb4] = '\xff'
        mem[0x7fffffffccb5] = '\x7f'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        cpu.XMM1 = 0x7fff0000008000007fff00007fff
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x4d851b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4d851b], b'f')
        self.assertEqual(mem[0x4d851c], b'\x0f')
        self.assertEqual(mem[0x4d851d], b'\x13')
        self.assertEqual(mem[0x4d851e], b'\x0c')
        self.assertEqual(mem[0x4d851f], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'\xff')
        self.assertEqual(mem[0x7fffffffccb1], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x7fffffffccb4], b'\xff')
        self.assertEqual(mem[0x7fffffffccb5], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(cpu.XMM1, 2596069201107260733309822636687359)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5080352)

    def test_MOVSD_1(self):
        ''' Instruction MOVSD_1
            Groups:
            0x555555556e3b:	rep movsd	dword ptr [rdi], dword ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem.mmap(0x55555576e000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdba0] = '\x10'
        mem[0x7fffffffdba1] = '\xdb'
        mem[0x7fffffffdba2] = '\xff'
        mem[0x7fffffffdba3] = '\xff'
        mem[0x7fffffffdba4] = '\xff'
        mem[0x7fffffffdba5] = '\x7f'
        mem[0x7fffffffdba6] = '\x00'
        mem[0x7fffffffdba7] = '\x00'
        mem[0x555555556e3c] = '\xa5'
        mem[0x55555576e63b] = '\x00'
        mem[0x55555576e638] = '\x00'
        mem[0x55555576e639] = '\x00'
        mem[0x55555576e63a] = '\x00'
        mem[0x555555556e3b] = '\xf3'
        mem[0x55555576e63c] = '\x00'
        mem[0x55555576e63d] = '\x00'
        mem[0x55555576e63e] = '\x00'
        mem[0x55555576e63f] = '\x00'
        cpu.RDI = 0x7fffffffdba0
        cpu.RCX = 0x12
        cpu.RSI = 0x55555576e638
        cpu.RIP = 0x555555556e3b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdba0], b'\x00')
        self.assertEqual(mem[0x7fffffffdba1], b'\x00')
        self.assertEqual(mem[0x7fffffffdba2], b'\x00')
        self.assertEqual(mem[0x7fffffffdba3], b'\x00')
        self.assertEqual(mem[0x7fffffffdba4], b'\xff')
        self.assertEqual(mem[0x7fffffffdba5], b'\x7f')
        self.assertEqual(mem[0x7fffffffdba6], b'\x00')
        self.assertEqual(mem[0x7fffffffdba7], b'\x00')
        self.assertEqual(mem[0x55555576e63c], b'\x00')
        self.assertEqual(mem[0x555555556e3b], b'\xf3')
        self.assertEqual(mem[0x55555576e638], b'\x00')
        self.assertEqual(mem[0x55555576e639], b'\x00')
        self.assertEqual(mem[0x55555576e63a], b'\x00')
        self.assertEqual(mem[0x55555576e63b], b'\x00')
        self.assertEqual(mem[0x555555556e3c], b'\xa5')
        self.assertEqual(mem[0x55555576e63d], b'\x00')
        self.assertEqual(mem[0x55555576e63e], b'\x00')
        self.assertEqual(mem[0x55555576e63f], b'\x00')
        self.assertEqual(cpu.RCX, 17)
        self.assertEqual(cpu.RDI, 140737488346020)
        self.assertEqual(cpu.RSI, 93824994436668)
        self.assertEqual(cpu.RIP, 93824992243259)

    def test_MOVSD_2(self):
        ''' Instruction MOVSD_2
            Groups:
            0x555555556e3b:	rep movsd	dword ptr [rdi], dword ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem.mmap(0x55555576e000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x55555576e620] = '\x00'
        mem[0x55555576e621] = '\x00'
        mem[0x55555576e622] = '\x00'
        mem[0x55555576e623] = '\x00'
        mem[0x7fffffffdb84] = 'U'
        mem[0x7fffffffdb85] = 'U'
        mem[0x7fffffffdb86] = '\x00'
        mem[0x7fffffffdb87] = '\x00'
        mem[0x7fffffffdb88] = '\x00'
        mem[0x7fffffffdb89] = '\x00'
        mem[0x7fffffffdb8a] = '\x00'
        mem[0x7fffffffdb8b] = '\x00'
        mem[0x55555576e61c] = '\x00'
        mem[0x555555556e3b] = '\xf3'
        mem[0x555555556e3c] = '\xa5'
        mem[0x55555576e61d] = '\x00'
        mem[0x55555576e61e] = '\x00'
        mem[0x55555576e61f] = '\x00'
        cpu.RDI = 0x7fffffffdb84
        cpu.RCX = 0x19
        cpu.RSI = 0x55555576e61c
        cpu.RIP = 0x555555556e3b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x55555576e620], b'\x00')
        self.assertEqual(mem[0x55555576e621], b'\x00')
        self.assertEqual(mem[0x55555576e622], b'\x00')
        self.assertEqual(mem[0x55555576e623], b'\x00')
        self.assertEqual(mem[0x7fffffffdb84], b'\x00')
        self.assertEqual(mem[0x7fffffffdb85], b'\x00')
        self.assertEqual(mem[0x7fffffffdb86], b'\x00')
        self.assertEqual(mem[0x7fffffffdb87], b'\x00')
        self.assertEqual(mem[0x7fffffffdb88], b'\x00')
        self.assertEqual(mem[0x7fffffffdb89], b'\x00')
        self.assertEqual(mem[0x7fffffffdb8a], b'\x00')
        self.assertEqual(mem[0x7fffffffdb8b], b'\x00')
        self.assertEqual(mem[0x555555556e3c], b'\xa5')
        self.assertEqual(mem[0x555555556e3b], b'\xf3')
        self.assertEqual(mem[0x55555576e61c], b'\x00')
        self.assertEqual(mem[0x55555576e61d], b'\x00')
        self.assertEqual(mem[0x55555576e61e], b'\x00')
        self.assertEqual(mem[0x55555576e61f], b'\x00')
        self.assertEqual(cpu.RCX, 24)
        self.assertEqual(cpu.RDI, 140737488345992)
        self.assertEqual(cpu.RSI, 93824994436640)
        self.assertEqual(cpu.RIP, 93824992243259)

    def test_MOVSD_3(self):
        ''' Instruction MOVSD_3
            Groups:
            0x555555556e3b:	rep movsd	dword ptr [rdi], dword ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem.mmap(0x55555576e000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x555555556e3b] = '\xf3'
        mem[0x55555576e64c] = '\x00'
        mem[0x55555576e64d] = '\x00'
        mem[0x55555576e64e] = '\x00'
        mem[0x55555576e64f] = '\x00'
        mem[0x55555576e650] = '\x00'
        mem[0x55555576e651] = '\x00'
        mem[0x55555576e652] = '\x00'
        mem[0x55555576e653] = '\x00'
        mem[0x7fffffffdbb4] = '\xff'
        mem[0x7fffffffdbb5] = '\x7f'
        mem[0x7fffffffdbb6] = '\x00'
        mem[0x7fffffffdbb7] = '\x00'
        mem[0x7fffffffdbb8] = '\x00'
        mem[0x7fffffffdbb9] = '\x00'
        mem[0x7fffffffdbba] = '\x00'
        mem[0x7fffffffdbbb] = '\x00'
        mem[0x555555556e3c] = '\xa5'
        cpu.RDI = 0x7fffffffdbb4
        cpu.RCX = 0xd
        cpu.RSI = 0x55555576e64c
        cpu.RIP = 0x555555556e3b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdbbb], b'\x00')
        self.assertEqual(mem[0x55555576e64c], b'\x00')
        self.assertEqual(mem[0x55555576e64d], b'\x00')
        self.assertEqual(mem[0x55555576e64e], b'\x00')
        self.assertEqual(mem[0x55555576e64f], b'\x00')
        self.assertEqual(mem[0x55555576e650], b'\x00')
        self.assertEqual(mem[0x55555576e651], b'\x00')
        self.assertEqual(mem[0x55555576e652], b'\x00')
        self.assertEqual(mem[0x55555576e653], b'\x00')
        self.assertEqual(mem[0x7fffffffdbb4], b'\x00')
        self.assertEqual(mem[0x7fffffffdbb5], b'\x00')
        self.assertEqual(mem[0x7fffffffdbb6], b'\x00')
        self.assertEqual(mem[0x7fffffffdbb7], b'\x00')
        self.assertEqual(mem[0x7fffffffdbb8], b'\x00')
        self.assertEqual(mem[0x7fffffffdbb9], b'\x00')
        self.assertEqual(mem[0x7fffffffdbba], b'\x00')
        self.assertEqual(mem[0x555555556e3b], b'\xf3')
        self.assertEqual(mem[0x555555556e3c], b'\xa5')
        self.assertEqual(cpu.RCX, 12)
        self.assertEqual(cpu.RDI, 140737488346040)
        self.assertEqual(cpu.RSI, 93824994436688)
        self.assertEqual(cpu.RIP, 93824992243259)

    def test_MOVSD_4(self):
        ''' Instruction MOVSD_4
            Groups:
            0x555555556e3b:	rep movsd	dword ptr [rdi], dword ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem.mmap(0x55555576e000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x55555576e640] = '\x00'
        mem[0x55555576e641] = '\x00'
        mem[0x55555576e642] = '\x00'
        mem[0x55555576e643] = '\x00'
        mem[0x55555576e644] = '\x00'
        mem[0x55555576e645] = '\x00'
        mem[0x55555576e646] = '\x00'
        mem[0x55555576e647] = '\x00'
        mem[0x7fffffffdba8] = 'g'
        mem[0x7fffffffdba9] = '\xa8'
        mem[0x7fffffffdbaa] = '\xb0'
        mem[0x7fffffffdbab] = '\xf7'
        mem[0x7fffffffdbac] = '\xff'
        mem[0x7fffffffdbad] = '\x7f'
        mem[0x7fffffffdbae] = '\x00'
        mem[0x7fffffffdbaf] = '\x00'
        mem[0x555555556e3b] = '\xf3'
        mem[0x555555556e3c] = '\xa5'
        cpu.RDI = 0x7fffffffdba8
        cpu.RCX = 0x10
        cpu.RSI = 0x55555576e640
        cpu.RIP = 0x555555556e3b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x55555576e640], b'\x00')
        self.assertEqual(mem[0x55555576e641], b'\x00')
        self.assertEqual(mem[0x55555576e642], b'\x00')
        self.assertEqual(mem[0x55555576e643], b'\x00')
        self.assertEqual(mem[0x55555576e644], b'\x00')
        self.assertEqual(mem[0x55555576e645], b'\x00')
        self.assertEqual(mem[0x55555576e646], b'\x00')
        self.assertEqual(mem[0x55555576e647], b'\x00')
        self.assertEqual(mem[0x7fffffffdba8], b'\x00')
        self.assertEqual(mem[0x7fffffffdba9], b'\x00')
        self.assertEqual(mem[0x7fffffffdbaa], b'\x00')
        self.assertEqual(mem[0x7fffffffdbab], b'\x00')
        self.assertEqual(mem[0x7fffffffdbac], b'\xff')
        self.assertEqual(mem[0x7fffffffdbad], b'\x7f')
        self.assertEqual(mem[0x7fffffffdbae], b'\x00')
        self.assertEqual(mem[0x7fffffffdbaf], b'\x00')
        self.assertEqual(mem[0x555555556e3b], b'\xf3')
        self.assertEqual(mem[0x555555556e3c], b'\xa5')
        self.assertEqual(cpu.RCX, 15)
        self.assertEqual(cpu.RDI, 140737488346028)
        self.assertEqual(cpu.RSI, 93824994436676)
        self.assertEqual(cpu.RIP, 93824992243259)

    def test_MOVSD_5(self):
        ''' Instruction MOVSD_5
            Groups:
            0x555555556e3b:	rep movsd	dword ptr [rdi], dword ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem.mmap(0x55555576e000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdba0] = '\x10'
        mem[0x7fffffffdba1] = '\xdb'
        mem[0x7fffffffdba2] = '\xff'
        mem[0x7fffffffdba3] = '\xff'
        mem[0x7fffffffdb9c] = '\x00'
        mem[0x555555556e3b] = '\xf3'
        mem[0x55555576e634] = '\x00'
        mem[0x55555576e635] = '\x00'
        mem[0x55555576e636] = '\x00'
        mem[0x55555576e637] = '\x00'
        mem[0x55555576e638] = '\x00'
        mem[0x55555576e639] = '\x00'
        mem[0x55555576e63a] = '\x00'
        mem[0x55555576e63b] = '\x00'
        mem[0x555555556e3c] = '\xa5'
        mem[0x7fffffffdb9d] = '\x00'
        mem[0x7fffffffdb9e] = '\x00'
        mem[0x7fffffffdb9f] = '\x00'
        cpu.RDI = 0x7fffffffdb9c
        cpu.RCX = 0x13
        cpu.RSI = 0x55555576e634
        cpu.RIP = 0x555555556e3b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdba0], b'\x10')
        self.assertEqual(mem[0x7fffffffdba1], b'\xdb')
        self.assertEqual(mem[0x7fffffffdba2], b'\xff')
        self.assertEqual(mem[0x7fffffffdba3], b'\xff')
        self.assertEqual(mem[0x55555576e63b], b'\x00')
        self.assertEqual(mem[0x555555556e3c], b'\xa5')
        self.assertEqual(mem[0x55555576e634], b'\x00')
        self.assertEqual(mem[0x55555576e635], b'\x00')
        self.assertEqual(mem[0x55555576e636], b'\x00')
        self.assertEqual(mem[0x55555576e637], b'\x00')
        self.assertEqual(mem[0x55555576e638], b'\x00')
        self.assertEqual(mem[0x55555576e639], b'\x00')
        self.assertEqual(mem[0x55555576e63a], b'\x00')
        self.assertEqual(mem[0x555555556e3b], b'\xf3')
        self.assertEqual(mem[0x7fffffffdb9c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb9f], b'\x00')
        self.assertEqual(cpu.RCX, 18)
        self.assertEqual(cpu.RDI, 140737488346016)
        self.assertEqual(cpu.RSI, 93824994436664)
        self.assertEqual(cpu.RIP, 93824992243259)

    def test_MOVSD_6(self):
        ''' Instruction MOVSD_6
            Groups:
            0x555555556e3b:	rep movsd	dword ptr [rdi], dword ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555556000, 0x1000, 'rwx')
        mem.mmap(0x55555576e000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x55555576e604] = '\x00'
        mem[0x55555576e605] = '\x00'
        mem[0x55555576e606] = '\x00'
        mem[0x55555576e607] = '\x00'
        mem[0x55555576e608] = '\x00'
        mem[0x55555576e609] = '\x00'
        mem[0x55555576e60a] = '\x00'
        mem[0x55555576e60b] = '\x00'
        mem[0x7fffffffdb6c] = '\x00'
        mem[0x7fffffffdb6d] = '\x00'
        mem[0x7fffffffdb6e] = '\x00'
        mem[0x7fffffffdb6f] = '\x00'
        mem[0x7fffffffdb70] = '\xe0'
        mem[0x7fffffffdb71] = '\xdb'
        mem[0x7fffffffdb72] = '\xff'
        mem[0x7fffffffdb73] = '\xff'
        mem[0x555555556e3b] = '\xf3'
        mem[0x555555556e3c] = '\xa5'
        cpu.RDI = 0x7fffffffdb6c
        cpu.RCX = 0x1f
        cpu.RSI = 0x55555576e604
        cpu.RIP = 0x555555556e3b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x55555576e604], b'\x00')
        self.assertEqual(mem[0x55555576e605], b'\x00')
        self.assertEqual(mem[0x55555576e606], b'\x00')
        self.assertEqual(mem[0x55555576e607], b'\x00')
        self.assertEqual(mem[0x55555576e608], b'\x00')
        self.assertEqual(mem[0x55555576e609], b'\x00')
        self.assertEqual(mem[0x55555576e60a], b'\x00')
        self.assertEqual(mem[0x55555576e60b], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb6f], b'\x00')
        self.assertEqual(mem[0x7fffffffdb70], b'\xe0')
        self.assertEqual(mem[0x7fffffffdb71], b'\xdb')
        self.assertEqual(mem[0x7fffffffdb72], b'\xff')
        self.assertEqual(mem[0x7fffffffdb73], b'\xff')
        self.assertEqual(mem[0x555555556e3b], b'\xf3')
        self.assertEqual(mem[0x555555556e3c], b'\xa5')
        self.assertEqual(cpu.RCX, 30)
        self.assertEqual(cpu.RDI, 140737488345968)
        self.assertEqual(cpu.RSI, 93824994436616)
        self.assertEqual(cpu.RIP, 93824992243259)

    def test_MOVSXD_1(self):
        ''' Instruction MOVSXD_1
            Groups:
            0x466083:	movsxd	rdi, edi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00466000, 0x1000, 'rwx')
        mem[0x00466083] = 'H'
        mem[0x00466084] = 'c'
        mem[0x00466085] = '\xff'
        cpu.EDI = 0x41
        cpu.RDI = 0x41
        cpu.RIP = 0x466083
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x466083], b'H')
        self.assertEqual(mem[0x466084], b'c')
        self.assertEqual(mem[0x466085], b'\xff')
        self.assertEqual(cpu.EDI, 65)
        self.assertEqual(cpu.RDI, 65)
        self.assertEqual(cpu.RIP, 4612230)

    def test_MOVSXD_2(self):
        ''' Instruction MOVSXD_2
            Groups:
            0x7ffff7ddf068:	movsxd	rdx, dword ptr [r8 + rbx*4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddf000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7df5000, 0x1000, 'rwx')
        mem[0x7ffff7ddf068] = 'I'
        mem[0x7ffff7ddf069] = 'c'
        mem[0x7ffff7ddf06a] = '\x14'
        mem[0x7ffff7ddf06b] = '\x98'
        mem[0x7ffff7df5f1c] = '\x8f'
        mem[0x7ffff7df5f1d] = '\x91'
        mem[0x7ffff7df5f1e] = '\xfe'
        mem[0x7ffff7df5f1f] = '\xff'
        cpu.R8 = 0x7ffff7df5f1c
        cpu.RDX = 0x2
        cpu.RIP = 0x7ffff7ddf068
        cpu.RBX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddf068], b'I')
        self.assertEqual(mem[0x7ffff7ddf069], b'c')
        self.assertEqual(mem[0x7ffff7ddf06a], b'\x14')
        self.assertEqual(mem[0x7ffff7ddf06b], b'\x98')
        self.assertEqual(mem[0x7ffff7df5f1c], b'\x8f')
        self.assertEqual(mem[0x7ffff7df5f1d], b'\x91')
        self.assertEqual(mem[0x7ffff7df5f1e], b'\xfe')
        self.assertEqual(mem[0x7ffff7df5f1f], b'\xff')
        self.assertEqual(cpu.R8, 140737351999260)
        self.assertEqual(cpu.RDX, 18446744073709457807)
        self.assertEqual(cpu.RIP, 140737351905388)
        self.assertEqual(cpu.RBX, 0)

    def test_MOVSXD_3(self):
        ''' Instruction MOVSXD_3
            Groups:
            0x436902:	movsxd	rax, dword ptr [rdx + rax*4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00436000, 0x1000, 'rwx')
        mem.mmap(0x00494000, 0x1000, 'rwx')
        mem[0x00494cf0] = '\xa0'
        mem[0x00494cf1] = '\x1c'
        mem[0x00436902] = 'H'
        mem[0x00436903] = 'c'
        mem[0x00436904] = '\x04'
        mem[0x00436905] = '\x82'
        mem[0x00494cf3] = '\xff'
        mem[0x00494cf2] = '\xfa'
        cpu.RIP = 0x436902
        cpu.RAX = 0x1c
        cpu.RDX = 0x494c80
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x494cf0], b'\xa0')
        self.assertEqual(mem[0x494cf1], b'\x1c')
        self.assertEqual(mem[0x436902], b'H')
        self.assertEqual(mem[0x436903], b'c')
        self.assertEqual(mem[0x436904], b'\x04')
        self.assertEqual(mem[0x436905], b'\x82')
        self.assertEqual(mem[0x494cf3], b'\xff')
        self.assertEqual(mem[0x494cf2], b'\xfa')
        self.assertEqual(cpu.RAX, 18446744073709165728)
        self.assertEqual(cpu.RIP, 4417798)
        self.assertEqual(cpu.RDX, 4803712)

    def test_MOVSXD_4(self):
        ''' Instruction MOVSXD_4
            Groups:
            0x7ffff7df214a:	movsxd	rax, dword ptr [rcx + rax*4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df2000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7df6000, 0x1000, 'rwx')
        mem[0x7ffff7df674f] = '\xff'
        mem[0x7ffff7df674c] = '0'
        mem[0x7ffff7df214a] = 'H'
        mem[0x7ffff7df214b] = 'c'
        mem[0x7ffff7df214c] = '\x04'
        mem[0x7ffff7df214d] = '\x81'
        mem[0x7ffff7df674e] = '\xff'
        mem[0x7ffff7df674d] = '\xbb'
        cpu.RCX = 0x7ffff7df6740
        cpu.RIP = 0x7ffff7df214a
        cpu.RAX = 0x3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df674f], b'\xff')
        self.assertEqual(mem[0x7ffff7df214c], b'\x04')
        self.assertEqual(mem[0x7ffff7df214a], b'H')
        self.assertEqual(mem[0x7ffff7df214b], b'c')
        self.assertEqual(mem[0x7ffff7df674c], b'0')
        self.assertEqual(mem[0x7ffff7df214d], b'\x81')
        self.assertEqual(mem[0x7ffff7df674e], b'\xff')
        self.assertEqual(mem[0x7ffff7df674d], b'\xbb')
        self.assertEqual(cpu.RCX, 140737352001344)
        self.assertEqual(cpu.RAX, 18446744073709534000)
        self.assertEqual(cpu.RIP, 140737351983438)

    def test_MOVSXD_5(self):
        ''' Instruction MOVSXD_5
            Groups:
            0x436b12:	movsxd	rax, dword ptr [rdx + rax*4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00436000, 0x1000, 'rwx')
        mem.mmap(0x00494000, 0x1000, 'rwx')
        mem[0x00494ea0] = '\x10'
        mem[0x00494ea1] = '\x1d'
        mem[0x00494ea2] = '\xfa'
        mem[0x00494ea3] = '\xff'
        mem[0x00436b14] = '\x04'
        mem[0x00436b15] = '\x82'
        mem[0x00436b13] = 'c'
        mem[0x00436b12] = 'H'
        cpu.RIP = 0x436b12
        cpu.RAX = 0x8
        cpu.RDX = 0x494e80
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x494ea0], b'\x10')
        self.assertEqual(mem[0x494ea1], b'\x1d')
        self.assertEqual(mem[0x494ea2], b'\xfa')
        self.assertEqual(mem[0x494ea3], b'\xff')
        self.assertEqual(mem[0x436b14], b'\x04')
        self.assertEqual(mem[0x436b15], b'\x82')
        self.assertEqual(mem[0x436b13], b'c')
        self.assertEqual(mem[0x436b12], b'H')
        self.assertEqual(cpu.RAX, 18446744073709165840)
        self.assertEqual(cpu.RIP, 4418326)
        self.assertEqual(cpu.RDX, 4804224)

    def test_MOVSXD_6(self):
        ''' Instruction MOVSXD_6
            Groups:
            0x7ffff7de62e7:	movsxd	rdx, dword ptr [rax + r12*4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7df6000, 0x1000, 'rwx')
        mem[0x7ffff7df6458] = 'x'
        mem[0x7ffff7df6459] = '\xff'
        mem[0x7ffff7de62e7] = 'J'
        mem[0x7ffff7de62e8] = 'c'
        mem[0x7ffff7de62e9] = '\x14'
        mem[0x7ffff7de62ea] = '\xa0'
        mem[0x7ffff7df645b] = '\xff'
        mem[0x7ffff7df645a] = '\xfe'
        cpu.RIP = 0x7ffff7de62e7
        cpu.R12 = 0x6
        cpu.RDX = 0x7ffff7a32fe0
        cpu.RAX = 0x7ffff7df6440
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df6458], b'x')
        self.assertEqual(mem[0x7ffff7df6459], b'\xff')
        self.assertEqual(mem[0x7ffff7de62e7], b'J')
        self.assertEqual(mem[0x7ffff7de62e8], b'c')
        self.assertEqual(mem[0x7ffff7de62e9], b'\x14')
        self.assertEqual(mem[0x7ffff7de62ea], b'\xa0')
        self.assertEqual(mem[0x7ffff7df645b], b'\xff')
        self.assertEqual(mem[0x7ffff7df645a], b'\xfe')
        self.assertEqual(cpu.RAX, 140737352000576)
        self.assertEqual(cpu.R12, 6)
        self.assertEqual(cpu.RDX, 18446744073709485944)
        self.assertEqual(cpu.RIP, 140737351934699)

    def test_MOVSX_1(self):
        ''' Instruction MOVSX_1
            Groups:
            0x7ffff7df1273:	movsx	edx, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1273] = '\x0f'
        mem[0x7ffff7df1274] = '\xbe'
        mem[0x7ffff7df1275] = '\x17'
        mem[0x555555554435] = '.'
        cpu.EDX = 0x63
        cpu.RDI = 0x555555554435
        cpu.RIP = 0x7ffff7df1273
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1273], b'\x0f')
        self.assertEqual(mem[0x7ffff7df1274], b'\xbe')
        self.assertEqual(mem[0x7ffff7df1275], b'\x17')
        self.assertEqual(mem[0x555555554435], b'.')
        self.assertEqual(cpu.EDX, 46)
        self.assertEqual(cpu.RDI, 93824992232501)
        self.assertEqual(cpu.RIP, 140737351979638)

    def test_MOVSX_2(self):
        ''' Instruction MOVSX_2
            Groups:
            0x7ffff7df1273:	movsx	edx, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1273] = '\x0f'
        mem[0x7ffff7df1274] = '\xbe'
        mem[0x7ffff7df1275] = '\x17'
        mem[0x55555555444d] = '.'
        cpu.EDX = 0x63
        cpu.RDI = 0x55555555444d
        cpu.RIP = 0x7ffff7df1273
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1273], b'\x0f')
        self.assertEqual(mem[0x7ffff7df1274], b'\xbe')
        self.assertEqual(mem[0x7ffff7df1275], b'\x17')
        self.assertEqual(mem[0x55555555444d], b'.')
        self.assertEqual(cpu.EDX, 46)
        self.assertEqual(cpu.RDI, 93824992232525)
        self.assertEqual(cpu.RIP, 140737351979638)

    def test_MOVSX_3(self):
        ''' Instruction MOVSX_3
            Groups:
            0x7ffff7df1260:	movsx	eax, byte ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ff2000, 0x1000, 'rwx')
        mem[0x7ffff7df1260] = '\x0f'
        mem[0x7ffff7df1261] = '\xbe'
        mem[0x7ffff7df1262] = '\x06'
        mem[0x7ffff7ff23b6] = 'l'
        cpu.EAX = 0x3c
        cpu.RSI = 0x7ffff7ff23b6
        cpu.RIP = 0x7ffff7df1260
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1260], b'\x0f')
        self.assertEqual(mem[0x7ffff7df1261], b'\xbe')
        self.assertEqual(mem[0x7ffff7df1262], b'\x06')
        self.assertEqual(mem[0x7ffff7ff23b6], b'l')
        self.assertEqual(cpu.EAX, 108)
        self.assertEqual(cpu.RSI, 140737354081206)
        self.assertEqual(cpu.RIP, 140737351979619)

    def test_MOVSX_4(self):
        ''' Instruction MOVSX_4
            Groups:
            0x7ffff7df1260:	movsx	eax, byte ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7fed000, 0x1000, 'rwx')
        mem[0x7ffff7df1260] = '\x0f'
        mem[0x7ffff7df1261] = '\xbe'
        mem[0x7ffff7df1262] = '\x06'
        mem[0x7ffff7fede8e] = 'i'
        cpu.EAX = 0x39
        cpu.RSI = 0x7ffff7fede8e
        cpu.RIP = 0x7ffff7df1260
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1260], b'\x0f')
        self.assertEqual(mem[0x7ffff7df1261], b'\xbe')
        self.assertEqual(mem[0x7ffff7df1262], b'\x06')
        self.assertEqual(mem[0x7ffff7fede8e], b'i')
        self.assertEqual(cpu.EAX, 105)
        self.assertEqual(cpu.RSI, 140737354063502)
        self.assertEqual(cpu.RIP, 140737351979619)

    def test_MOVSX_5(self):
        ''' Instruction MOVSX_5
            Groups:
            0x7ffff7df1260:	movsx	eax, byte ptr [rsi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7fed000, 0x1000, 'rwx')
        mem[0x7ffff7df1260] = '\x0f'
        mem[0x7ffff7df1261] = '\xbe'
        mem[0x7ffff7df1262] = '\x06'
        mem[0x7ffff7fede8f] = 'b'
        cpu.EAX = 0x32
        cpu.RSI = 0x7ffff7fede8f
        cpu.RIP = 0x7ffff7df1260
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df1260], b'\x0f')
        self.assertEqual(mem[0x7ffff7df1261], b'\xbe')
        self.assertEqual(mem[0x7ffff7df1262], b'\x06')
        self.assertEqual(mem[0x7ffff7fede8f], b'b')
        self.assertEqual(cpu.EAX, 98)
        self.assertEqual(cpu.RSI, 140737354063503)
        self.assertEqual(cpu.RIP, 140737351979619)

    def test_MOVSX_6(self):
        ''' Instruction MOVSX_6
            Groups:
            0x7ffff7df1273:	movsx	edx, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df1274] = '\xbe'
        mem[0x7ffff7df1273] = '\x0f'
        mem[0x555555554434] = 'c'
        mem[0x7ffff7df1275] = '\x17'
        cpu.EDX = 0x62
        cpu.RDI = 0x555555554434
        cpu.RIP = 0x7ffff7df1273
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555554434], b'c')
        self.assertEqual(mem[0x7ffff7df1273], b'\x0f')
        self.assertEqual(mem[0x7ffff7df1274], b'\xbe')
        self.assertEqual(mem[0x7ffff7df1275], b'\x17')
        self.assertEqual(cpu.EDX, 99)
        self.assertEqual(cpu.RDI, 93824992232500)
        self.assertEqual(cpu.RIP, 140737351979638)

    def test_MOVZX_1(self):
        ''' Instruction MOVZX_1
            Groups:
            0x7ffff7de3aa3:	movzx	edx, byte ptr [rcx + 4]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a32000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3aa4] = '\xb6'
        mem[0x7ffff7de3aa3] = '\x0f'
        mem[0x7ffff7a324bc] = '\x11'
        mem[0x7ffff7de3aa5] = 'Q'
        mem[0x7ffff7de3aa6] = '\x04'
        cpu.EDX = 0x6
        cpu.RCX = 0x7ffff7a324b8
        cpu.RIP = 0x7ffff7de3aa3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a324bc], b'\x11')
        self.assertEqual(mem[0x7ffff7de3aa3], b'\x0f')
        self.assertEqual(mem[0x7ffff7de3aa4], b'\xb6')
        self.assertEqual(mem[0x7ffff7de3aa5], b'Q')
        self.assertEqual(mem[0x7ffff7de3aa6], b'\x04')
        self.assertEqual(cpu.EDX, 17)
        self.assertEqual(cpu.RCX, 140737348052152)
        self.assertEqual(cpu.RIP, 140737351924391)

    def test_MOVZX_2(self):
        ''' Instruction MOVZX_2
            Groups:
            0x7ffff7de4399:	movzx	edx, byte ptr [rcx]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4399] = '\x0f'
        mem[0x7ffff7de439a] = '\xb6'
        mem[0x7ffff7de439b] = '\x11'
        mem[0x555555554e44] = '_'
        cpu.EDX = 0x6c
        cpu.RCX = 0x555555554e44
        cpu.RIP = 0x7ffff7de4399
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4399], b'\x0f')
        self.assertEqual(mem[0x7ffff7de439a], b'\xb6')
        self.assertEqual(mem[0x7ffff7de439b], b'\x11')
        self.assertEqual(mem[0x555555554e44], b'_')
        self.assertEqual(cpu.EDX, 95)
        self.assertEqual(cpu.RCX, 93824992235076)
        self.assertEqual(cpu.RIP, 140737351926684)

    def test_MOVZX_3(self):
        ''' Instruction MOVZX_3
            Groups:
            0x400aaa:	movzx	eax, al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x00400aaa] = '\x0f'
        mem[0x00400aab] = '\xb6'
        mem[0x00400aac] = '\xc0'
        cpu.EAX = 0x79
        cpu.AL = 0x79
        cpu.RIP = 0x400aaa
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x400aaa], b'\x0f')
        self.assertEqual(mem[0x400aab], b'\xb6')
        self.assertEqual(mem[0x400aac], b'\xc0')
        self.assertEqual(cpu.EAX, 121)
        self.assertEqual(cpu.AL, 121)
        self.assertEqual(cpu.RIP, 4197037)

    def test_MOVZX_4(self):
        ''' Instruction MOVZX_4
            Groups:
            0x7ffff7b58f18:	movzx	r10d, word ptr [rdx + 6]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a35000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f18] = 'D'
        mem[0x7ffff7b58f19] = '\x0f'
        mem[0x7ffff7b58f1a] = '\xb7'
        mem[0x7ffff7b58f1b] = 'R'
        mem[0x7ffff7b58f1c] = '\x06'
        mem[0x7ffff7a3575e] = '\x0b'
        mem[0x7ffff7a3575f] = '\x00'
        cpu.RDX = 0x7ffff7a35758
        cpu.RIP = 0x7ffff7b58f18
        cpu.R10D = 0x24
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f18], b'D')
        self.assertEqual(mem[0x7ffff7b58f19], b'\x0f')
        self.assertEqual(mem[0x7ffff7b58f1a], b'\xb7')
        self.assertEqual(mem[0x7ffff7b58f1b], b'R')
        self.assertEqual(mem[0x7ffff7b58f1c], b'\x06')
        self.assertEqual(mem[0x7ffff7a3575e], b'\x0b')
        self.assertEqual(mem[0x7ffff7a3575f], b'\x00')
        self.assertEqual(cpu.RDX, 140737348065112)
        self.assertEqual(cpu.RIP, 140737349259037)
        self.assertEqual(cpu.R10D, 11)

    def test_MOVZX_5(self):
        ''' Instruction MOVZX_5
            Groups:
            0x7ffff7de6219:	movzx	r9d, r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6219] = 'E'
        mem[0x7ffff7de621a] = '\x0f'
        mem[0x7ffff7de621b] = '\xb6'
        mem[0x7ffff7de621c] = '\xc9'
        cpu.R9D = 0xffffff00
        cpu.R9B = 0x0
        cpu.RIP = 0x7ffff7de6219
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6219], b'E')
        self.assertEqual(mem[0x7ffff7de621a], b'\x0f')
        self.assertEqual(mem[0x7ffff7de621b], b'\xb6')
        self.assertEqual(mem[0x7ffff7de621c], b'\xc9')
        self.assertEqual(cpu.R9D, 0)
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 140737351934493)

    def test_MOVZX_6(self):
        ''' Instruction MOVZX_6
            Groups:
            0x7ffff7de3929:	movzx	ecx, byte ptr [rbp - 0x78]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd808] = '8'
        mem[0x7ffff7de3929] = '\x0f'
        mem[0x7ffff7de392a] = '\xb6'
        mem[0x7ffff7de392b] = 'M'
        mem[0x7ffff7de392c] = '\x88'
        cpu.ECX = 0x2917737
        cpu.RIP = 0x7ffff7de3929
        cpu.RBP = 0x7fffffffd880
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd808], b'8')
        self.assertEqual(mem[0x7ffff7de3929], b'\x0f')
        self.assertEqual(mem[0x7ffff7de392a], b'\xb6')
        self.assertEqual(mem[0x7ffff7de392b], b'M')
        self.assertEqual(mem[0x7ffff7de392c], b'\x88')
        self.assertEqual(cpu.RBP, 140737488345216)
        self.assertEqual(cpu.RIP, 140737351924013)
        self.assertEqual(cpu.ECX, 56)

    def test_MOV_1(self):
        ''' Instruction MOV_1
            Groups:
            0x737287:	mov	ebx, 0x40
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00737000, 0x1000, 'rwx')
        mem[0x00737288] = '@'
        mem[0x00737289] = '\x00'
        mem[0x0073728a] = '\x00'
        mem[0x0073728b] = '\x00'
        mem[0x00737287] = '\xbb'
        cpu.EBX = 0x40
        cpu.RIP = 0x737287
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x737288], b'@')
        self.assertEqual(mem[0x737289], b'\x00')
        self.assertEqual(mem[0x73728a], b'\x00')
        self.assertEqual(mem[0x73728b], b'\x00')
        self.assertEqual(mem[0x737287], b'\xbb')
        self.assertEqual(cpu.EBX, 64)
        self.assertEqual(cpu.RIP, 7565964)

    def test_MOV_2(self):
        ''' Instruction MOV_2
            Groups:
            0x7ffff7de6121:	mov	rax, r13
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6121] = 'L'
        mem[0x7ffff7de6122] = '\x89'
        mem[0x7ffff7de6123] = '\xe8'
        cpu.RIP = 0x7ffff7de6121
        cpu.RAX = 0x8
        cpu.R13 = 0x7ffff7a2e000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6121], b'L')
        self.assertEqual(mem[0x7ffff7de6122], b'\x89')
        self.assertEqual(mem[0x7ffff7de6123], b'\xe8')
        self.assertEqual(cpu.RAX, 140737348034560)
        self.assertEqual(cpu.RIP, 140737351934244)
        self.assertEqual(cpu.R13, 140737348034560)

    def test_MOV_3(self):
        ''' Instruction MOV_3
            Groups:
            0x74dced:	mov	dword ptr [rsp], 0x7fff
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0074d000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x0074dced] = '\xc7'
        mem[0x0074dcf0] = '\xff'
        mem[0x0074dcf1] = '\x7f'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x0074dcee] = '\x04'
        mem[0x0074dcef] = '$'
        mem[0x7fffffffccb0] = '\xff'
        mem[0x7fffffffccb1] = '\x7f'
        mem[0x0074dcf2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x0074dcf3] = '\x00'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x74dced
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x74dced], b'\xc7')
        self.assertEqual(mem[0x7fffffffccb0], b'\xff')
        self.assertEqual(mem[0x7fffffffccb1], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x74dcee], b'\x04')
        self.assertEqual(mem[0x74dcef], b'$')
        self.assertEqual(mem[0x74dcf0], b'\xff')
        self.assertEqual(mem[0x74dcf1], b'\x7f')
        self.assertEqual(mem[0x74dcf2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x74dcf3], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 7658740)

    def test_MOV_4(self):
        ''' Instruction MOV_4
            Groups:
            0x4b00dc:	mov	dword ptr [rsp + 4], 0x80
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004b0000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x004b00dc] = '\xc7'
        mem[0x004b00dd] = 'D'
        mem[0x004b00de] = '$'
        mem[0x004b00df] = '\x04'
        mem[0x004b00e0] = '\x80'
        mem[0x004b00e1] = '\x00'
        mem[0x004b00e2] = '\x00'
        mem[0x004b00e3] = '\x00'
        mem[0x7fffffffccb4] = '\xff'
        mem[0x7fffffffccb5] = '\xff'
        mem[0x7fffffffccb6] = '\xff'
        mem[0x7fffffffccb7] = '\xff'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x4b00dc
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4b00dc], b'\xc7')
        self.assertEqual(mem[0x4b00dd], b'D')
        self.assertEqual(mem[0x4b00de], b'$')
        self.assertEqual(mem[0x4b00df], b'\x04')
        self.assertEqual(mem[0x4b00e0], b'\x80')
        self.assertEqual(mem[0x4b00e1], b'\x00')
        self.assertEqual(mem[0x4b00e2], b'\x00')
        self.assertEqual(mem[0x4b00e3], b'\x00')
        self.assertEqual(mem[0x7fffffffccb4], b'\x80')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 4915428)

    def test_MOV_5(self):
        ''' Instruction MOV_5
            Groups:
            0x7776d9:	mov	dword ptr [rsp + 8], 0x80000000
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00777000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x007776d9] = '\xc7'
        mem[0x007776da] = 'D'
        mem[0x007776db] = '$'
        mem[0x007776dc] = '\x08'
        mem[0x007776dd] = '\x00'
        mem[0x007776de] = '\x00'
        mem[0x007776df] = '\x00'
        mem[0x007776e0] = '\x80'
        mem[0x7fffffffccb8] = '\x7f'
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x7776d9
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7776d9], b'\xc7')
        self.assertEqual(mem[0x7776da], b'D')
        self.assertEqual(mem[0x7776db], b'$')
        self.assertEqual(mem[0x7776dc], b'\x08')
        self.assertEqual(mem[0x7776dd], b'\x00')
        self.assertEqual(mem[0x7776de], b'\x00')
        self.assertEqual(mem[0x7776df], b'\x00')
        self.assertEqual(mem[0x7776e0], b'\x80')
        self.assertEqual(mem[0x7fffffffccb8], b'\x00')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x80')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 7829217)

    def test_MOV_6(self):
        ''' Instruction MOV_6
            Groups:
            0x4c3b88:	mov	dword ptr [rsp + 0xc], 0x12345678
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004c3000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x004c3b88] = '\xc7'
        mem[0x004c3b89] = 'D'
        mem[0x004c3b8a] = '$'
        mem[0x004c3b8b] = '\x0c'
        mem[0x004c3b8c] = 'x'
        mem[0x004c3b8d] = 'V'
        mem[0x004c3b8e] = '4'
        mem[0x004c3b8f] = '\x12'
        mem[0x7fffffffccbc] = 'x'
        mem[0x7fffffffccbd] = 'V'
        mem[0x7fffffffccbe] = '4'
        mem[0x7fffffffccbf] = '\x12'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x4c3b88
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4c3b88], b'\xc7')
        self.assertEqual(mem[0x4c3b89], b'D')
        self.assertEqual(mem[0x4c3b8a], b'$')
        self.assertEqual(mem[0x4c3b8b], b'\x0c')
        self.assertEqual(mem[0x4c3b8c], b'x')
        self.assertEqual(mem[0x4c3b8d], b'V')
        self.assertEqual(mem[0x4c3b8e], b'4')
        self.assertEqual(mem[0x4c3b8f], b'\x12')
        self.assertEqual(mem[0x7fffffffccbc], b'x')
        self.assertEqual(mem[0x7fffffffccbd], b'V')
        self.assertEqual(mem[0x7fffffffccbe], b'4')
        self.assertEqual(mem[0x7fffffffccbf], b'\x12')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 4995984)

    def test_MUL_1(self):
        ''' Instruction MUL_1
            Groups:
            0x7ffff7de253f:	mul	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de2000, 0x1000, 'rwx')
        mem[0x7ffff7de2540] = '\xf7'
        mem[0x7ffff7de2541] = '\xe2'
        mem[0x7ffff7de253f] = 'H'
        cpu.OF = False
        cpu.RIP = 0x7ffff7de253f
        cpu.CF = False
        cpu.RAX = 0x5f
        cpu.RDX = 0xcccccccccccccccd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de2540], b'\xf7')
        self.assertEqual(mem[0x7ffff7de2541], b'\xe2')
        self.assertEqual(mem[0x7ffff7de253f], b'H')
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.RAX, 19)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351918914)
        self.assertEqual(cpu.RDX, 76)

    def test_MUL_2(self):
        ''' Instruction MUL_2
            Groups:
            0x7ffff7de253f:	mul	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de2000, 0x1000, 'rwx')
        mem[0x7ffff7de2540] = '\xf7'
        mem[0x7ffff7de2541] = '\xe2'
        mem[0x7ffff7de253f] = 'H'
        cpu.OF = False
        cpu.RIP = 0x7ffff7de253f
        cpu.CF = False
        cpu.RAX = 0x5f
        cpu.RDX = 0xcccccccccccccccd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de2540], b'\xf7')
        self.assertEqual(mem[0x7ffff7de2541], b'\xe2')
        self.assertEqual(mem[0x7ffff7de253f], b'H')
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.RAX, 19)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351918914)
        self.assertEqual(cpu.RDX, 76)

    def test_MUL_3(self):
        ''' Instruction MUL_3
            Groups:
            0x7ffff7de253f:	mul	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de2000, 0x1000, 'rwx')
        mem[0x7ffff7de2540] = '\xf7'
        mem[0x7ffff7de2541] = '\xe2'
        mem[0x7ffff7de253f] = 'H'
        cpu.OF = False
        cpu.RIP = 0x7ffff7de253f
        cpu.CF = False
        cpu.RAX = 0x5f
        cpu.RDX = 0xcccccccccccccccd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de2540], b'\xf7')
        self.assertEqual(mem[0x7ffff7de2541], b'\xe2')
        self.assertEqual(mem[0x7ffff7de253f], b'H')
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.RAX, 19)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351918914)
        self.assertEqual(cpu.RDX, 76)

    def test_MUL_4(self):
        ''' Instruction MUL_4
            Groups:
            0x45f865:	mul	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0045f000, 0x1000, 'rwx')
        mem[0x0045f865] = 'H'
        mem[0x0045f866] = '\xf7'
        mem[0x0045f867] = '\xe2'
        cpu.OF = False
        cpu.RIP = 0x45f865
        cpu.CF = False
        cpu.RAX = 0x57
        cpu.RDX = 0xcccccccccccccccd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x45f865], b'H')
        self.assertEqual(mem[0x45f866], b'\xf7')
        self.assertEqual(mem[0x45f867], b'\xe2')
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.RAX, 11068046444225730987)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4585576)
        self.assertEqual(cpu.RDX, 69)

    def test_MUL_5(self):
        ''' Instruction MUL_5
            Groups:
            0x4624e5:	mul	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00462000, 0x1000, 'rwx')
        mem[0x004624e5] = 'H'
        mem[0x004624e6] = '\xf7'
        mem[0x004624e7] = '\xe2'
        cpu.OF = False
        cpu.RIP = 0x4624e5
        cpu.CF = False
        cpu.RAX = 0x57
        cpu.RDX = 0xcccccccccccccccd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4624e5], b'H')
        self.assertEqual(mem[0x4624e6], b'\xf7')
        self.assertEqual(mem[0x4624e7], b'\xe2')
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.RAX, 11068046444225730987)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4596968)
        self.assertEqual(cpu.RDX, 69)

    def test_MUL_6(self):
        ''' Instruction MUL_6
            Groups:
            0x443dc7:	mul	r9
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00443000, 0x1000, 'rwx')
        mem[0x00443dc8] = '\xf7'
        mem[0x00443dc9] = '\xe1'
        mem[0x00443dc7] = 'I'
        cpu.OF = False
        cpu.R9 = 0xcccccccccccccccd
        cpu.RIP = 0x443dc7
        cpu.RDX = 0xa
        cpu.CF = False
        cpu.RAX = 0x3
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x443dc8], b'\xf7')
        self.assertEqual(mem[0x443dc9], b'\xe1')
        self.assertEqual(mem[0x443dc7], b'I')
        self.assertEqual(cpu.RDX, 2)
        self.assertEqual(cpu.OF, True)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4472266)
        self.assertEqual(cpu.R9, 14757395258967641293)
        self.assertEqual(cpu.RAX, 7378697629483820647)

    def test_NEG_1(self):
        ''' Instruction NEG_1
            Groups:
            0x7ffff7df27cf:	neg	rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df2000, 0x1000, 'rwx')
        mem[0x7ffff7df27d0] = '\xf7'
        mem[0x7ffff7df27d1] = '\xd8'
        mem[0x7ffff7df27cf] = 'H'
        cpu.PF = True
        cpu.RAX = 0x7ffff7ffeb78
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = True
        cpu.RIP = 0x7ffff7df27cf
        cpu.SF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df27d0], b'\xf7')
        self.assertEqual(mem[0x7ffff7df27d1], b'\xd8')
        self.assertEqual(mem[0x7ffff7df27cf], b'H')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 18446603336355419272)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351985106)
        self.assertEqual(cpu.SF, True)

    def test_NEG_2(self):
        ''' Instruction NEG_2
            Groups:
            0x7ffff7de5c54:	neg	rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5c54] = 'H'
        mem[0x7ffff7de5c55] = '\xf7'
        mem[0x7ffff7de5c56] = '\xd8'
        cpu.PF = True
        cpu.RAX = 0x1000
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de5c54
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5c54], b'H')
        self.assertEqual(mem[0x7ffff7de5c55], b'\xf7')
        self.assertEqual(mem[0x7ffff7de5c56], b'\xd8')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RAX, 18446744073709547520)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351933015)
        self.assertEqual(cpu.SF, True)

    def test_NEG_3(self):
        ''' Instruction NEG_3
            Groups:
            0x40baad:	neg	eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040b000, 0x1000, 'rwx')
        mem[0x0040baad] = '\xf7'
        mem[0x0040baae] = '\xd8'
        cpu.EAX = 0x0
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x40baad
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40baad], b'\xf7')
        self.assertEqual(mem[0x40baae], b'\xd8')
        self.assertEqual(cpu.EAX, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4242095)
        self.assertEqual(cpu.SF, False)

    def test_NEG_4(self):
        ''' Instruction NEG_4
            Groups:
            0x7ffff7df27b6:	neg	rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df2000, 0x1000, 'rwx')
        mem[0x7ffff7df27b8] = '\xdf'
        mem[0x7ffff7df27b6] = 'H'
        mem[0x7ffff7df27b7] = '\xf7'
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RDI = 0x8
        cpu.CF = False
        cpu.RIP = 0x7ffff7df27b6
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df27b8], b'\xdf')
        self.assertEqual(mem[0x7ffff7df27b6], b'H')
        self.assertEqual(mem[0x7ffff7df27b7], b'\xf7')
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RDI, 18446744073709551608)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351985081)
        self.assertEqual(cpu.SF, True)

    def test_NEG_5(self):
        ''' Instruction NEG_5
            Groups:
            0x411176:	neg	r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x00411178] = '\xda'
        mem[0x00411176] = 'I'
        mem[0x00411177] = '\xf7'
        cpu.PF = True
        cpu.R10 = 0x1000
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x411176
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x411178], b'\xda')
        self.assertEqual(mem[0x411176], b'I')
        self.assertEqual(mem[0x411177], b'\xf7')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.R10, 18446744073709547520)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4264313)
        self.assertEqual(cpu.SF, True)

    def test_NEG_6(self):
        ''' Instruction NEG_6
            Groups:
            0x7ffff7df27b6:	neg	rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df2000, 0x1000, 'rwx')
        mem[0x7ffff7df27b8] = '\xdf'
        mem[0x7ffff7df27b6] = 'H'
        mem[0x7ffff7df27b7] = '\xf7'
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RDI = 0x8
        cpu.CF = False
        cpu.RIP = 0x7ffff7df27b6
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df27b8], b'\xdf')
        self.assertEqual(mem[0x7ffff7df27b6], b'H')
        self.assertEqual(mem[0x7ffff7df27b7], b'\xf7')
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RDI, 18446744073709551608)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351985081)
        self.assertEqual(cpu.SF, True)

    def test_NOT_1(self):
        ''' Instruction NOT_1
            Groups:
            0x7ffff7df144a:	not	rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df1000, 0x1000, 'rwx')
        mem[0x7ffff7df144a] = 'H'
        mem[0x7ffff7df144b] = '\xf7'
        mem[0x7ffff7df144c] = '\xd0'
        cpu.RIP = 0x7ffff7df144a
        cpu.RAX = 0x8000000000000000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df144a], b'H')
        self.assertEqual(mem[0x7ffff7df144b], b'\xf7')
        self.assertEqual(mem[0x7ffff7df144c], b'\xd0')
        self.assertEqual(cpu.RAX, 9223372036854775807)
        self.assertEqual(cpu.RIP, 140737351980109)

    def test_NOT_2(self):
        ''' Instruction NOT_2
            Groups:
            0x4008f7:	not	esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x004008f8] = '\xd6'
        mem[0x004008f7] = '\xf7'
        cpu.RIP = 0x4008f7
        cpu.ESI = 0xfffffff0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4008f8], b'\xd6')
        self.assertEqual(mem[0x4008f7], b'\xf7')
        self.assertEqual(cpu.ESI, 15)
        self.assertEqual(cpu.RIP, 4196601)

    def test_NOT_3(self):
        ''' Instruction NOT_3
            Groups:
            0x7ffff7a78242:	not	rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem[0x7ffff7a78242] = 'H'
        mem[0x7ffff7a78243] = '\xf7'
        mem[0x7ffff7a78244] = '\xd0'
        cpu.RIP = 0x7ffff7a78242
        cpu.RAX = 0xfffffffffffffffc
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a78242], b'H')
        self.assertEqual(mem[0x7ffff7a78243], b'\xf7')
        self.assertEqual(mem[0x7ffff7a78244], b'\xd0')
        self.assertEqual(cpu.RAX, 3)
        self.assertEqual(cpu.RIP, 140737348338245)

    def test_NOT_4(self):
        ''' Instruction NOT_4
            Groups:
            0x7ffff7de5765:	not	r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5765] = 'I'
        mem[0x7ffff7de5766] = '\xf7'
        mem[0x7ffff7de5767] = '\xd2'
        cpu.RIP = 0x7ffff7de5765
        cpu.R10 = 0xffffffffffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5765], b'I')
        self.assertEqual(mem[0x7ffff7de5766], b'\xf7')
        self.assertEqual(mem[0x7ffff7de5767], b'\xd2')
        self.assertEqual(cpu.R10, 0)
        self.assertEqual(cpu.RIP, 140737351931752)

    def test_NOT_5(self):
        ''' Instruction NOT_5
            Groups:
            0x7ffff7de5765:	not	r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5765] = 'I'
        mem[0x7ffff7de5766] = '\xf7'
        mem[0x7ffff7de5767] = '\xd2'
        cpu.RIP = 0x7ffff7de5765
        cpu.R10 = 0xffffffffffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5765], b'I')
        self.assertEqual(mem[0x7ffff7de5766], b'\xf7')
        self.assertEqual(mem[0x7ffff7de5767], b'\xd2')
        self.assertEqual(cpu.R10, 0)
        self.assertEqual(cpu.RIP, 140737351931752)

    def test_NOT_6(self):
        ''' Instruction NOT_6
            Groups:
            0x7ffff7de5765:	not	r10
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5765] = 'I'
        mem[0x7ffff7de5766] = '\xf7'
        mem[0x7ffff7de5767] = '\xd2'
        cpu.RIP = 0x7ffff7de5765
        cpu.R10 = 0xffffffffffffffff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5765], b'I')
        self.assertEqual(mem[0x7ffff7de5766], b'\xf7')
        self.assertEqual(mem[0x7ffff7de5767], b'\xd2')
        self.assertEqual(cpu.R10, 0)
        self.assertEqual(cpu.RIP, 140737351931752)

    def test_OR_1(self):
        ''' Instruction OR_1
            Groups:
            0x7ffff7de6235:	or	r9d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6235] = 'A'
        mem[0x7ffff7de6236] = '\t'
        mem[0x7ffff7de6237] = '\xc1'
        cpu.EAX = 0x0
        cpu.PF = False
        cpu.SF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6235
        cpu.R9D = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6235], b'A')
        self.assertEqual(mem[0x7ffff7de6236], b'\t')
        self.assertEqual(mem[0x7ffff7de6237], b'\xc1')
        self.assertEqual(cpu.EAX, 0)
        self.assertEqual(cpu.R9D, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351934520)
        self.assertEqual(cpu.SF, False)

    def test_OR_2(self):
        ''' Instruction OR_2
            Groups:
            0x7ffff7de4344:	or	qword ptr [rsp], 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7ffff7de4344] = 'H'
        mem[0x7ffff7de4345] = '\x83'
        mem[0x7ffff7de4346] = '\x0c'
        mem[0x7ffff7de4347] = '$'
        mem[0x7ffff7de4348] = '\x00'
        mem[0x7fffffffc920] = '\x00'
        mem[0x7fffffffc921] = '\x00'
        mem[0x7fffffffc922] = '\x00'
        mem[0x7fffffffc923] = '\x00'
        mem[0x7fffffffc924] = '\x00'
        mem[0x7fffffffc925] = '\x00'
        mem[0x7fffffffc926] = '\x00'
        mem[0x7fffffffc927] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4344
        cpu.PF = False
        cpu.RSP = 0x7fffffffc920
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4344], b'H')
        self.assertEqual(mem[0x7ffff7de4345], b'\x83')
        self.assertEqual(mem[0x7ffff7de4346], b'\x0c')
        self.assertEqual(mem[0x7ffff7de4347], b'$')
        self.assertEqual(mem[0x7ffff7de4348], b'\x00')
        self.assertEqual(mem[0x7fffffffc920], b'\x00')
        self.assertEqual(mem[0x7fffffffc921], b'\x00')
        self.assertEqual(mem[0x7fffffffc922], b'\x00')
        self.assertEqual(mem[0x7fffffffc923], b'\x00')
        self.assertEqual(mem[0x7fffffffc924], b'\x00')
        self.assertEqual(mem[0x7fffffffc925], b'\x00')
        self.assertEqual(mem[0x7fffffffc926], b'\x00')
        self.assertEqual(mem[0x7fffffffc927], b'\x00')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926601)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RSP, 140737488341280)
        self.assertEqual(cpu.SF, False)

    def test_OR_3(self):
        ''' Instruction OR_3
            Groups:
            0x7ffff7de3814:	or	qword ptr [rsp], 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7ffff7de3816] = '\x0c'
        mem[0x7ffff7de3817] = '$'
        mem[0x7fffffffc790] = '\x00'
        mem[0x7fffffffc791] = '\x00'
        mem[0x7fffffffc792] = '\x00'
        mem[0x7fffffffc793] = '\x00'
        mem[0x7ffff7de3814] = 'H'
        mem[0x7ffff7de3815] = '\x83'
        mem[0x7fffffffc796] = '\x00'
        mem[0x7fffffffc797] = '\x00'
        mem[0x7ffff7de3818] = '\x00'
        mem[0x7fffffffc794] = '\x00'
        mem[0x7fffffffc795] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3814
        cpu.PF = True
        cpu.RSP = 0x7fffffffc790
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffc796], b'\x00')
        self.assertEqual(mem[0x7fffffffc797], b'\x00')
        self.assertEqual(mem[0x7fffffffc790], b'\x00')
        self.assertEqual(mem[0x7fffffffc791], b'\x00')
        self.assertEqual(mem[0x7fffffffc792], b'\x00')
        self.assertEqual(mem[0x7fffffffc793], b'\x00')
        self.assertEqual(mem[0x7ffff7de3814], b'H')
        self.assertEqual(mem[0x7ffff7de3815], b'\x83')
        self.assertEqual(mem[0x7ffff7de3816], b'\x0c')
        self.assertEqual(mem[0x7ffff7de3817], b'$')
        self.assertEqual(mem[0x7ffff7de3818], b'\x00')
        self.assertEqual(mem[0x7fffffffc794], b'\x00')
        self.assertEqual(mem[0x7fffffffc795], b'\x00')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351923737)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RSP, 140737488340880)
        self.assertEqual(cpu.SF, False)

    def test_OR_4(self):
        ''' Instruction OR_4
            Groups:
            0x7ffff7de3814:	or	qword ptr [rsp], 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7ffff7de3816] = '\x0c'
        mem[0x7ffff7de3817] = '$'
        mem[0x7fffffffc790] = '\x00'
        mem[0x7fffffffc791] = '\x00'
        mem[0x7fffffffc792] = '\x00'
        mem[0x7fffffffc793] = '\x00'
        mem[0x7ffff7de3814] = 'H'
        mem[0x7ffff7de3815] = '\x83'
        mem[0x7fffffffc796] = '\x00'
        mem[0x7fffffffc797] = '\x00'
        mem[0x7ffff7de3818] = '\x00'
        mem[0x7fffffffc794] = '\x00'
        mem[0x7fffffffc795] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3814
        cpu.PF = True
        cpu.RSP = 0x7fffffffc790
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffc796], b'\x00')
        self.assertEqual(mem[0x7fffffffc797], b'\x00')
        self.assertEqual(mem[0x7fffffffc790], b'\x00')
        self.assertEqual(mem[0x7fffffffc791], b'\x00')
        self.assertEqual(mem[0x7fffffffc792], b'\x00')
        self.assertEqual(mem[0x7fffffffc793], b'\x00')
        self.assertEqual(mem[0x7ffff7de3814], b'H')
        self.assertEqual(mem[0x7ffff7de3815], b'\x83')
        self.assertEqual(mem[0x7ffff7de3816], b'\x0c')
        self.assertEqual(mem[0x7ffff7de3817], b'$')
        self.assertEqual(mem[0x7ffff7de3818], b'\x00')
        self.assertEqual(mem[0x7fffffffc794], b'\x00')
        self.assertEqual(mem[0x7fffffffc795], b'\x00')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351923737)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RSP, 140737488340880)
        self.assertEqual(cpu.SF, False)

    def test_OR_5(self):
        ''' Instruction OR_5
            Groups:
            0x40a38c:	or	qword ptr [rsp], 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040a000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcb00] = '/'
        mem[0x7fffffffcb01] = 'h'
        mem[0x7fffffffcb02] = 'o'
        mem[0x7fffffffcb03] = 'm'
        mem[0x7fffffffcb04] = 'e'
        mem[0x7fffffffcb05] = '/'
        mem[0x7fffffffcb06] = 'f'
        mem[0x7fffffffcb07] = 'e'
        mem[0x0040a38c] = 'H'
        mem[0x0040a38d] = '\x83'
        mem[0x0040a38e] = '\x0c'
        mem[0x0040a38f] = '$'
        mem[0x0040a390] = '\x00'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x40a38c
        cpu.PF = True
        cpu.RSP = 0x7fffffffcb00
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcb00], b'/')
        self.assertEqual(mem[0x7fffffffcb01], b'h')
        self.assertEqual(mem[0x7fffffffcb02], b'o')
        self.assertEqual(mem[0x7fffffffcb03], b'm')
        self.assertEqual(mem[0x7fffffffcb04], b'e')
        self.assertEqual(mem[0x7fffffffcb05], b'/')
        self.assertEqual(mem[0x7fffffffcb06], b'f')
        self.assertEqual(mem[0x7fffffffcb07], b'e')
        self.assertEqual(mem[0x40a38c], b'H')
        self.assertEqual(mem[0x40a38d], b'\x83')
        self.assertEqual(mem[0x40a38e], b'\x0c')
        self.assertEqual(mem[0x40a38f], b'$')
        self.assertEqual(mem[0x40a390], b'\x00')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4236177)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.RSP, 140737488341760)
        self.assertEqual(cpu.SF, False)

    def test_OR_6(self):
        ''' Instruction OR_6
            Groups:
            0x7ffff7de6212:	or	r9d, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6212] = 'A'
        mem[0x7ffff7de6213] = '\t'
        mem[0x7ffff7de6214] = '\xc1'
        cpu.EAX = 0xffffff00
        cpu.PF = True
        cpu.SF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = True
        cpu.RIP = 0x7ffff7de6212
        cpu.R9D = 0xf7ff7600
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6212], b'A')
        self.assertEqual(mem[0x7ffff7de6213], b'\t')
        self.assertEqual(mem[0x7ffff7de6214], b'\xc1')
        self.assertEqual(cpu.EAX, 4294967040)
        self.assertEqual(cpu.R9D, 4294967040)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351934485)
        self.assertEqual(cpu.SF, True)

    def test_PCMPEQB_1(self):
        ''' Instruction PCMPEQB_1
            Groups: sse2
            0x457e12:	pcmpeqb	xmm5, xmm2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457e12] = 'f'
        mem[0x00457e13] = '\x0f'
        mem[0x00457e14] = 't'
        mem[0x00457e15] = '\xea'
        cpu.XMM2 = 0x0
        cpu.RIP = 0x457e12
        cpu.XMM5 = 0x2f65726f6369746e614d2f737463656a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457e12], b'f')
        self.assertEqual(mem[0x457e13], b'\x0f')
        self.assertEqual(mem[0x457e14], b't')
        self.assertEqual(mem[0x457e15], b'\xea')
        self.assertEqual(cpu.XMM2, 0)
        self.assertEqual(cpu.RIP, 4554262)
        self.assertEqual(cpu.XMM5, 0)

    def test_PCMPEQB_2(self):
        ''' Instruction PCMPEQB_2
            Groups: sse2
            0x4184bf:	pcmpeqb	xmm12, xmm8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004184c0] = 'E'
        mem[0x004184c1] = '\x0f'
        mem[0x004184c2] = 't'
        mem[0x004184c3] = '\xe0'
        mem[0x004184bf] = 'f'
        cpu.XMM12 = 0x6e696874796e61206f642074276e6f44
        cpu.XMM8 = 0x0
        cpu.RIP = 0x4184bf
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4184c0], b'E')
        self.assertEqual(mem[0x4184c1], b'\x0f')
        self.assertEqual(mem[0x4184c2], b't')
        self.assertEqual(mem[0x4184c3], b'\xe0')
        self.assertEqual(mem[0x4184bf], b'f')
        self.assertEqual(cpu.XMM12, 0)
        self.assertEqual(cpu.XMM8, 0)
        self.assertEqual(cpu.RIP, 4293828)

    def test_PCMPEQB_3(self):
        ''' Instruction PCMPEQB_3
            Groups: sse2
            0x457a26:	pcmpeqb	xmm0, xmm7
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457a28] = 't'
        mem[0x00457a29] = '\xc7'
        mem[0x00457a26] = 'f'
        mem[0x00457a27] = '\x0f'
        cpu.XMM0 = 0x5400324e2f2f00313d524e00455f4744
        cpu.XMM7 = 0x0
        cpu.RIP = 0x457a26
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457a28], b't')
        self.assertEqual(mem[0x457a29], b'\xc7')
        self.assertEqual(mem[0x457a26], b'f')
        self.assertEqual(mem[0x457a27], b'\x0f')
        self.assertEqual(cpu.XMM0, 1324035698927585248728409418697277440)
        self.assertEqual(cpu.XMM7, 0)
        self.assertEqual(cpu.RIP, 4553258)

    def test_PCMPEQB_4(self):
        ''' Instruction PCMPEQB_4
            Groups: sse2
            0x4579e8:	pcmpeqb	xmm0, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x004579e8] = 'f'
        mem[0x004579e9] = '\x0f'
        mem[0x004579ea] = 't'
        mem[0x004579eb] = '\xc1'
        cpu.XMM0 = 0x2f78756e696c2f73656c706d6178652f
        cpu.XMM1 = 0x2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f
        cpu.RIP = 0x4579e8
        cpu.execute()
        self.assertEqual(mem[0x4579e8], b'f')
        self.assertEqual(mem[0x4579e9], b'\x0f')
        self.assertEqual(mem[0x4579ea], b't')
        self.assertEqual(mem[0x4579eb], b'\xc1')
        self.assertEqual(cpu.XMM0, 338953138925154751793923932131017359615)
        self.assertEqual(cpu.XMM1, 62718710765820030520700417840365121327)
        self.assertEqual(cpu.RIP, 4553196)

    def test_PCMPEQB_5(self):
        ''' Instruction PCMPEQB_5
            Groups: sse2
            0x7ffff7ab7ac6:	pcmpeqb	xmm0, xmm7
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab7000, 0x1000, 'rwx')
        mem[0x7ffff7ab7ac8] = 't'
        mem[0x7ffff7ab7ac9] = '\xc7'
        mem[0x7ffff7ab7ac6] = 'f'
        mem[0x7ffff7ab7ac7] = '\x0f'
        cpu.XMM0 = 0x322f2f4d00313d522f00565f474458
        cpu.XMM7 = 0x0
        cpu.RIP = 0x7ffff7ab7ac6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab7ac8], b't')
        self.assertEqual(mem[0x7ffff7ab7ac9], b'\xc7')
        self.assertEqual(mem[0x7ffff7ab7ac6], b'f')
        self.assertEqual(mem[0x7ffff7ab7ac7], b'\x0f')
        self.assertEqual(cpu.XMM0, 338953138925461823674472811186503024640)
        self.assertEqual(cpu.XMM7, 0)
        self.assertEqual(cpu.RIP, 140737348598474)

    def test_PCMPEQB_6(self):
        ''' Instruction PCMPEQB_6
            Groups: sse2
            0x7ffff7ab79b1:	pcmpeqb	xmm0, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab7000, 0x1000, 'rwx')
        mem[0x7ffff7ab79b1] = 'f'
        mem[0x7ffff7ab79b2] = '\x0f'
        mem[0x7ffff7ab79b3] = 't'
        mem[0x7ffff7ab79b4] = '\xc1'
        cpu.XMM0 = 0x6f72502f6570696c65662f656d6f682f
        cpu.XMM1 = 0x2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f
        cpu.RIP = 0x7ffff7ab79b1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab79b1], b'f')
        self.assertEqual(mem[0x7ffff7ab79b2], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab79b3], b't')
        self.assertEqual(mem[0x7ffff7ab79b4], b'\xc1')
        self.assertEqual(cpu.XMM0, 20203181441137406366729172418815)
        self.assertEqual(cpu.XMM1, 62718710765820030520700417840365121327)
        self.assertEqual(cpu.RIP, 140737348598197)

    def test_PMINUB_1(self):
        ''' Instruction PMINUB_1
            Groups: sse2
            0x41b15f:	pminub	xmm8, xmmword ptr [rax + 0x10]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0041b000, 0x1000, 'rwx')
        mem.mmap(0x00494000, 0x1000, 'rwx')
        mem[0x00494290] = ' '
        mem[0x00494291] = ' '
        mem[0x00494292] = ' '
        mem[0x00494293] = ' '
        mem[0x00494294] = ' '
        mem[0x00494295] = ' '
        mem[0x00494296] = ' '
        mem[0x00494297] = ' '
        mem[0x00494298] = ' '
        mem[0x00494299] = ' '
        mem[0x0049429a] = ' '
        mem[0x0049429b] = ' '
        mem[0x0049429c] = ' '
        mem[0x0049429d] = ' '
        mem[0x0049429e] = ' '
        mem[0x0049429f] = ' '
        mem[0x0041b15f] = 'f'
        mem[0x0041b160] = 'D'
        mem[0x0041b161] = '\x0f'
        mem[0x0041b162] = '\xda'
        mem[0x0041b163] = '@'
        mem[0x0041b164] = '\x10'
        cpu.XMM8 = 0x5f5f5f5f5f200a2e646574726f706572
        cpu.RIP = 0x41b15f
        cpu.RAX = 0x494280
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x494290], b' ')
        self.assertEqual(mem[0x494291], b' ')
        self.assertEqual(mem[0x494292], b' ')
        self.assertEqual(mem[0x494293], b' ')
        self.assertEqual(mem[0x494294], b' ')
        self.assertEqual(mem[0x494295], b' ')
        self.assertEqual(mem[0x494296], b' ')
        self.assertEqual(mem[0x494297], b' ')
        self.assertEqual(mem[0x494298], b' ')
        self.assertEqual(mem[0x494299], b' ')
        self.assertEqual(mem[0x49429a], b' ')
        self.assertEqual(mem[0x49429b], b' ')
        self.assertEqual(mem[0x49429c], b' ')
        self.assertEqual(mem[0x49429d], b' ')
        self.assertEqual(mem[0x49429e], b' ')
        self.assertEqual(mem[0x49429f], b' ')
        self.assertEqual(mem[0x41b15f], b'f')
        self.assertEqual(mem[0x41b160], b'D')
        self.assertEqual(mem[0x41b161], b'\x0f')
        self.assertEqual(mem[0x41b162], b'\xda')
        self.assertEqual(mem[0x41b163], b'@')
        self.assertEqual(mem[0x41b164], b'\x10')
        self.assertEqual(cpu.XMM8, 42702100946941193483733406035713466400)
        self.assertEqual(cpu.RAX, 4801152)
        self.assertEqual(cpu.RIP, 4305253)

    def test_PMINUB_2(self):
        ''' Instruction PMINUB_2
            Groups: sse2
            0x41b142:	pminub	xmm8, xmmword ptr [rax + 0x70]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0041b000, 0x1000, 'rwx')
        mem.mmap(0x00494000, 0x1000, 'rwx')
        mem[0x0041b142] = 'f'
        mem[0x0041b143] = 'D'
        mem[0x0041b144] = '\x0f'
        mem[0x0041b145] = '\xda'
        mem[0x0041b146] = '@'
        mem[0x0041b147] = 'p'
        mem[0x004942f0] = '_'
        mem[0x004942f1] = '_'
        mem[0x004942f2] = '_'
        mem[0x004942f3] = ' '
        mem[0x004942f4] = '_'
        mem[0x004942f5] = '_'
        mem[0x004942f6] = '_'
        mem[0x004942f7] = '_'
        mem[0x004942f8] = '_'
        mem[0x004942f9] = ' '
        mem[0x004942fa] = ' '
        mem[0x004942fb] = ' '
        mem[0x004942fc] = ' '
        mem[0x004942fd] = ' '
        mem[0x004942fe] = ' '
        mem[0x004942ff] = '_'
        cpu.XMM8 = 0x2020202020202020202020200a202020
        cpu.RIP = 0x41b142
        cpu.RAX = 0x494280
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41b142], b'f')
        self.assertEqual(mem[0x41b143], b'D')
        self.assertEqual(mem[0x41b144], b'\x0f')
        self.assertEqual(mem[0x41b145], b'\xda')
        self.assertEqual(mem[0x41b146], b'@')
        self.assertEqual(mem[0x41b147], b'p')
        self.assertEqual(mem[0x4942f0], b'_')
        self.assertEqual(mem[0x4942f1], b'_')
        self.assertEqual(mem[0x4942f2], b'_')
        self.assertEqual(mem[0x4942f3], b' ')
        self.assertEqual(mem[0x4942f4], b'_')
        self.assertEqual(mem[0x4942f5], b'_')
        self.assertEqual(mem[0x4942f6], b'_')
        self.assertEqual(mem[0x4942f7], b'_')
        self.assertEqual(mem[0x4942f8], b'_')
        self.assertEqual(mem[0x4942f9], b' ')
        self.assertEqual(mem[0x4942fa], b' ')
        self.assertEqual(mem[0x4942fb], b' ')
        self.assertEqual(mem[0x4942fc], b' ')
        self.assertEqual(mem[0x4942fd], b' ')
        self.assertEqual(mem[0x4942fe], b' ')
        self.assertEqual(mem[0x4942ff], b'_')
        self.assertEqual(cpu.XMM8, 42702100946941297375796029167539068960)
        self.assertEqual(cpu.RAX, 4801152)
        self.assertEqual(cpu.RIP, 4305224)

    def test_PMINUB_3(self):
        ''' Instruction PMINUB_3
            Groups: sse2
            0x457af6:	pminub	xmm0, xmm2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457af8] = '\xda'
        mem[0x00457af9] = '\xc2'
        mem[0x00457af6] = 'f'
        mem[0x00457af7] = '\x0f'
        cpu.XMM2 = 0x504e414d00323d524e54565f47445800
        cpu.XMM0 = 0x32677261003167726100706d636e7274
        cpu.RIP = 0x457af6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457af8], b'\xda')
        self.assertEqual(mem[0x457af9], b'\xc2')
        self.assertEqual(mem[0x457af6], b'f')
        self.assertEqual(mem[0x457af7], b'\x0f')
        self.assertEqual(cpu.XMM2, 106744563275012473217874926561820694528)
        self.assertEqual(cpu.XMM0, 66867723401463788104917456226191955968)
        self.assertEqual(cpu.RIP, 4553466)

    def test_PMINUB_4(self):
        ''' Instruction PMINUB_4
            Groups: sse2
            0x41b13c:	pminub	xmm8, xmmword ptr [rax + 0x60]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0041b000, 0x1000, 'rwx')
        mem.mmap(0x00494000, 0x1000, 'rwx')
        mem[0x0041b13c] = 'f'
        mem[0x0041b13d] = 'D'
        mem[0x0041b13e] = '\x0f'
        mem[0x0041b13f] = '\xda'
        mem[0x0041b140] = '@'
        mem[0x0041b141] = '`'
        mem[0x004941e0] = 'h'
        mem[0x004941e1] = 'e'
        mem[0x004941e2] = 'c'
        mem[0x004941e3] = 'k'
        mem[0x004941e4] = 'e'
        mem[0x004941e5] = 'd'
        mem[0x004941e6] = ' '
        mem[0x004941e7] = 'b'
        mem[0x004941e8] = 'y'
        mem[0x004941e9] = ' '
        mem[0x004941ea] = 's'
        mem[0x004941eb] = 'y'
        mem[0x004941ec] = 's'
        mem[0x004941ed] = 't'
        mem[0x004941ee] = 'e'
        mem[0x004941ef] = 'm'
        cpu.XMM8 = 0x632067676f6120736720720a646e6120
        cpu.RIP = 0x41b13c
        cpu.RAX = 0x494180
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x41b13c], b'f')
        self.assertEqual(mem[0x41b13d], b'D')
        self.assertEqual(mem[0x41b13e], b'\x0f')
        self.assertEqual(mem[0x41b13f], b'\xda')
        self.assertEqual(mem[0x41b140], b'@')
        self.assertEqual(mem[0x41b141], b'`')
        self.assertEqual(mem[0x4941e0], b'h')
        self.assertEqual(mem[0x4941e1], b'e')
        self.assertEqual(mem[0x4941e2], b'c')
        self.assertEqual(mem[0x4941e3], b'k')
        self.assertEqual(mem[0x4941e4], b'e')
        self.assertEqual(mem[0x4941e5], b'd')
        self.assertEqual(mem[0x4941e6], b' ')
        self.assertEqual(mem[0x4941e7], b'b')
        self.assertEqual(mem[0x4941e8], b'y')
        self.assertEqual(mem[0x4941e9], b' ')
        self.assertEqual(mem[0x4941ea], b's')
        self.assertEqual(mem[0x4941eb], b'y')
        self.assertEqual(mem[0x4941ec], b's')
        self.assertEqual(mem[0x4941ed], b't')
        self.assertEqual(mem[0x4941ee], b'e')
        self.assertEqual(mem[0x4941ef], b'm')
        self.assertEqual(cpu.XMM8, 131761822365339956131716016926609334560)
        self.assertEqual(cpu.RAX, 4800896)
        self.assertEqual(cpu.RIP, 4305218)

    def test_PMINUB_5(self):
        ''' Instruction PMINUB_5
            Groups: sse2
            0x457ee2:	pminub	xmm0, xmm5
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457ee2] = 'f'
        mem[0x00457ee3] = '\x0f'
        mem[0x00457ee4] = '\xda'
        mem[0x00457ee5] = '\xc5'
        cpu.XMM0 = 0x4d00313d524e00565f472f2f00326763
        cpu.RIP = 0x457ee2
        cpu.XMM5 = 0x65784563696c6f626d79532f65726f63
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457ee2], b'f')
        self.assertEqual(mem[0x457ee3], b'\x0f')
        self.assertEqual(mem[0x457ee4], b'\xda')
        self.assertEqual(mem[0x457ee5], b'\xc5')
        self.assertEqual(cpu.XMM0, 102351554371899083128134245349023967075)
        self.assertEqual(cpu.RIP, 4554470)
        self.assertEqual(cpu.XMM5, 134876510559778439374245404375482789731)

    def test_PMINUB_6(self):
        ''' Instruction PMINUB_6
            Groups: sse2
            0x7ffff7ab7abe:	pminub	xmm0, xmm4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab7000, 0x1000, 'rwx')
        mem[0x7ffff7ab7ac0] = '\xda'
        mem[0x7ffff7ab7ac1] = '\xc4'
        mem[0x7ffff7ab7abe] = 'f'
        mem[0x7ffff7ab7abf] = '\x0f'
        cpu.XMM0 = 0x324e414d00313d524e00565f474458
        cpu.RIP = 0x7ffff7ab7abe
        cpu.XMM4 = 0x7274732f78756e696c2f73656c706d61
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab7ac0], b'\xda')
        self.assertEqual(mem[0x7ffff7ab7ac1], b'\xc4')
        self.assertEqual(mem[0x7ffff7ab7abe], b'f')
        self.assertEqual(mem[0x7ffff7ab7abf], b'\x0f')
        self.assertEqual(cpu.XMM0, 261200618430042665518031405314425944)
        self.assertEqual(cpu.XMM4, 152136634193178674532939302896952962401)
        self.assertEqual(cpu.RIP, 140737348598466)

    def test_PMOVMSKB_1(self):
        ''' Instruction PMOVMSKB_1
            Groups: sse2
            0x4184f1:	pmovmskb	ecx, xmm11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004184f1] = 'f'
        mem[0x004184f2] = 'A'
        mem[0x004184f3] = '\x0f'
        mem[0x004184f4] = '\xd7'
        mem[0x004184f5] = '\xcb'
        cpu.XMM11 = 0x0
        cpu.RIP = 0x4184f1
        cpu.ECX = 0x10e
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4184f1], b'f')
        self.assertEqual(mem[0x4184f2], b'A')
        self.assertEqual(mem[0x4184f3], b'\x0f')
        self.assertEqual(mem[0x4184f4], b'\xd7')
        self.assertEqual(mem[0x4184f5], b'\xcb')
        self.assertEqual(cpu.XMM11, 0)
        self.assertEqual(cpu.RIP, 4293878)
        self.assertEqual(cpu.ECX, 0)

    def test_PMOVMSKB_2(self):
        ''' Instruction PMOVMSKB_2
            Groups: sse2
            0x457d6e:	pmovmskb	r10d, xmm3
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457d70] = '\x0f'
        mem[0x00457d71] = '\xd7'
        mem[0x00457d72] = '\xd3'
        mem[0x00457d6e] = 'f'
        mem[0x00457d6f] = 'D'
        cpu.XMM3 = 0xff00000000ff0000000000000000
        cpu.RIP = 0x457d6e
        cpu.R10D = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457d70], b'\x0f')
        self.assertEqual(mem[0x457d71], b'\xd7')
        self.assertEqual(mem[0x457d72], b'\xd3')
        self.assertEqual(mem[0x457d6e], b'f')
        self.assertEqual(mem[0x457d6f], b'D')
        self.assertEqual(cpu.XMM3, 5172014448935879877845345013596160)
        self.assertEqual(cpu.RIP, 4554099)
        self.assertEqual(cpu.R10D, 8448)

    def test_PMOVMSKB_3(self):
        ''' Instruction PMOVMSKB_3
            Groups: sse2
            0x457ddd:	pmovmskb	edx, xmm3
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457de0] = '\xd3'
        mem[0x00457ddd] = 'f'
        mem[0x00457dde] = '\x0f'
        mem[0x00457ddf] = '\xd7'
        cpu.XMM3 = 0x0
        cpu.EDX = 0xffffdcc8
        cpu.RIP = 0x457ddd
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457de0], b'\xd3')
        self.assertEqual(mem[0x457ddd], b'f')
        self.assertEqual(mem[0x457dde], b'\x0f')
        self.assertEqual(mem[0x457ddf], b'\xd7')
        self.assertEqual(cpu.XMM3, 0)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.RIP, 4554209)

    def test_PMOVMSKB_4(self):
        ''' Instruction PMOVMSKB_4
            Groups: sse2
            0x7ffff7ab5ce1:	pmovmskb	ecx, xmm11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab5000, 0x1000, 'rwx')
        mem[0x7ffff7ab5ce1] = 'f'
        mem[0x7ffff7ab5ce2] = 'A'
        mem[0x7ffff7ab5ce3] = '\x0f'
        mem[0x7ffff7ab5ce4] = '\xd7'
        mem[0x7ffff7ab5ce5] = '\xcb'
        cpu.XMM11 = 0xffffff0000000000ffffff0000000000
        cpu.RIP = 0x7ffff7ab5ce1
        cpu.ECX = 0xa00
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab5ce1], b'f')
        self.assertEqual(mem[0x7ffff7ab5ce2], b'A')
        self.assertEqual(mem[0x7ffff7ab5ce3], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab5ce4], b'\xd7')
        self.assertEqual(mem[0x7ffff7ab5ce5], b'\xcb')
        self.assertEqual(cpu.XMM11, 340282346638528859830150926458714849280)
        self.assertEqual(cpu.RIP, 140737348590822)
        self.assertEqual(cpu.ECX, 57568)

    def test_PMOVMSKB_5(self):
        ''' Instruction PMOVMSKB_5
            Groups: sse2
            0x4184e7:	pmovmskb	edx, xmm9
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004184e8] = 'A'
        mem[0x004184e9] = '\x0f'
        mem[0x004184ea] = '\xd7'
        mem[0x004184eb] = '\xd1'
        mem[0x004184e7] = 'f'
        cpu.EDX = 0x0
        cpu.XMM9 = 0xff00000000000000000000000000
        cpu.RIP = 0x4184e7
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4184e8], b'A')
        self.assertEqual(mem[0x4184e9], b'\x0f')
        self.assertEqual(mem[0x4184ea], b'\xd7')
        self.assertEqual(mem[0x4184eb], b'\xd1')
        self.assertEqual(mem[0x4184e7], b'f')
        self.assertEqual(cpu.EDX, 8192)
        self.assertEqual(cpu.XMM9, 5172014448931175958106549077934080)
        self.assertEqual(cpu.RIP, 4293868)

    def test_PMOVMSKB_6(self):
        ''' Instruction PMOVMSKB_6
            Groups: sse2
            0x4184c4:	pmovmskb	edx, xmm12
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004184c8] = '\xd4'
        mem[0x004184c4] = 'f'
        mem[0x004184c5] = 'A'
        mem[0x004184c6] = '\x0f'
        mem[0x004184c7] = '\xd7'
        cpu.EDX = 0x100
        cpu.XMM12 = 0x0
        cpu.RIP = 0x4184c4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4184c8], b'\xd4')
        self.assertEqual(mem[0x4184c4], b'f')
        self.assertEqual(mem[0x4184c5], b'A')
        self.assertEqual(mem[0x4184c6], b'\x0f')
        self.assertEqual(mem[0x4184c7], b'\xd7')
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.XMM12, 0)
        self.assertEqual(cpu.RIP, 4293833)

    def test_POP_1(self):
        ''' Instruction POP_1
            Groups: mode64
            0x7ffff7de3b0b:	pop	rbp
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd880] = '\xb0'
        mem[0x7fffffffd881] = '\xd9'
        mem[0x7fffffffd882] = '\xff'
        mem[0x7fffffffd883] = '\xff'
        mem[0x7fffffffd884] = '\xff'
        mem[0x7fffffffd885] = '\x7f'
        mem[0x7fffffffd886] = '\x00'
        mem[0x7fffffffd887] = '\x00'
        mem[0x7fffffffd888] = '\x7f'
        mem[0x7ffff7de3b0b] = ']'
        mem[0x7fffffffd878] = 'p'
        mem[0x7fffffffd879] = '\xda'
        mem[0x7fffffffd87a] = '\xff'
        mem[0x7fffffffd87b] = '\xff'
        mem[0x7fffffffd87c] = '\xff'
        mem[0x7fffffffd87d] = '\x7f'
        mem[0x7fffffffd87e] = '\x00'
        mem[0x7fffffffd87f] = '\x00'
        cpu.RSP = 0x7fffffffd880
        cpu.RIP = 0x7ffff7de3b0b
        cpu.RBP = 0x7fffffffd880
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd880], b'\xb0')
        self.assertEqual(mem[0x7fffffffd881], b'\xd9')
        self.assertEqual(mem[0x7fffffffd882], b'\xff')
        self.assertEqual(mem[0x7fffffffd883], b'\xff')
        self.assertEqual(mem[0x7fffffffd884], b'\xff')
        self.assertEqual(mem[0x7fffffffd885], b'\x7f')
        self.assertEqual(mem[0x7fffffffd886], b'\x00')
        self.assertEqual(mem[0x7fffffffd887], b'\x00')
        self.assertEqual(mem[0x7fffffffd888], b'\x7f')
        self.assertEqual(mem[0x7ffff7de3b0b], b']')
        self.assertEqual(mem[0x7fffffffd878], b'p')
        self.assertEqual(mem[0x7fffffffd879], b'\xda')
        self.assertEqual(mem[0x7fffffffd87a], b'\xff')
        self.assertEqual(mem[0x7fffffffd87b], b'\xff')
        self.assertEqual(mem[0x7fffffffd87c], b'\xff')
        self.assertEqual(mem[0x7fffffffd87d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd87e], b'\x00')
        self.assertEqual(mem[0x7fffffffd87f], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345224)
        self.assertEqual(cpu.RIP, 140737351924492)
        self.assertEqual(cpu.RBP, 140737488345520)

    def test_POP_2(self):
        ''' Instruction POP_2
            Groups: mode64
            0x7ffff7dea3ad:	pop	r14
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7dea000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda08] = '\x01'
        mem[0x7fffffffda09] = '\x00'
        mem[0x7fffffffda0a] = '\x00'
        mem[0x7fffffffda0b] = '\x00'
        mem[0x7fffffffda0c] = '\x00'
        mem[0x7ffff7dea3ad] = 'A'
        mem[0x7ffff7dea3ae] = '^'
        mem[0x7fffffffda0d] = '\x00'
        mem[0x7fffffffda10] = '0'
        mem[0x7fffffffda11] = '\xda'
        mem[0x7fffffffda12] = '\xff'
        mem[0x7fffffffda13] = '\xff'
        mem[0x7fffffffda14] = '\xff'
        mem[0x7fffffffda0e] = '\x00'
        mem[0x7fffffffda16] = '\x00'
        mem[0x7fffffffda17] = '\x00'
        mem[0x7fffffffda18] = '`'
        mem[0x7fffffffda0f] = '\x00'
        mem[0x7fffffffda15] = '\x7f'
        cpu.R14 = 0x4
        cpu.RSP = 0x7fffffffda10
        cpu.RIP = 0x7ffff7dea3ad
        cpu.RBP = 0x7fffffffda20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7dea3ae], b'^')
        self.assertEqual(mem[0x7fffffffda08], b'\x01')
        self.assertEqual(mem[0x7fffffffda09], b'\x00')
        self.assertEqual(mem[0x7fffffffda0a], b'\x00')
        self.assertEqual(mem[0x7fffffffda0b], b'\x00')
        self.assertEqual(mem[0x7fffffffda0c], b'\x00')
        self.assertEqual(mem[0x7fffffffda0d], b'\x00')
        self.assertEqual(mem[0x7fffffffda0e], b'\x00')
        self.assertEqual(mem[0x7fffffffda0f], b'\x00')
        self.assertEqual(mem[0x7fffffffda10], b'0')
        self.assertEqual(mem[0x7fffffffda11], b'\xda')
        self.assertEqual(mem[0x7fffffffda12], b'\xff')
        self.assertEqual(mem[0x7fffffffda13], b'\xff')
        self.assertEqual(mem[0x7fffffffda14], b'\xff')
        self.assertEqual(mem[0x7fffffffda15], b'\x7f')
        self.assertEqual(mem[0x7fffffffda16], b'\x00')
        self.assertEqual(mem[0x7fffffffda17], b'\x00')
        self.assertEqual(mem[0x7fffffffda18], b'`')
        self.assertEqual(mem[0x7ffff7dea3ad], b'A')
        self.assertEqual(cpu.R14, 140737488345648)
        self.assertEqual(cpu.RSP, 140737488345624)
        self.assertEqual(cpu.RIP, 140737351951279)
        self.assertEqual(cpu.RBP, 140737488345632)

    def test_POP_3(self):
        ''' Instruction POP_3
            Groups: mode64
            0x4624e4:	pop	r12
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00462000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdb00] = 'H'
        mem[0x7fffffffdb01] = '\xd4'
        mem[0x7fffffffdb02] = 'k'
        mem[0x7fffffffdb03] = '\x00'
        mem[0x004624e4] = 'A'
        mem[0x004624e5] = '\\'
        mem[0x7fffffffdb06] = '\x00'
        mem[0x7fffffffdb07] = '\x00'
        mem[0x7fffffffdb08] = '\xb8'
        mem[0x7fffffffdaff] = '\x00'
        mem[0x7fffffffdaf9] = '\x00'
        mem[0x7fffffffdaf8] = '\x03'
        mem[0x7fffffffdb04] = '\x00'
        mem[0x7fffffffdafa] = '\x00'
        mem[0x7fffffffdafb] = '\x00'
        mem[0x7fffffffdafc] = '\x00'
        mem[0x7fffffffdafd] = '\x00'
        mem[0x7fffffffdafe] = '\x00'
        mem[0x7fffffffdb05] = '\x00'
        cpu.RSP = 0x7fffffffdb00
        cpu.R12 = 0x1
        cpu.RIP = 0x4624e4
        cpu.RBP = 0x7fffffffdb20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdb00], b'H')
        self.assertEqual(mem[0x7fffffffdb01], b'\xd4')
        self.assertEqual(mem[0x7fffffffdb02], b'k')
        self.assertEqual(mem[0x7fffffffdb03], b'\x00')
        self.assertEqual(mem[0x7fffffffdb04], b'\x00')
        self.assertEqual(mem[0x7fffffffdb05], b'\x00')
        self.assertEqual(mem[0x7fffffffdb06], b'\x00')
        self.assertEqual(mem[0x7fffffffdb07], b'\x00')
        self.assertEqual(mem[0x7fffffffdb08], b'\xb8')
        self.assertEqual(mem[0x7fffffffdaff], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf9], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf8], b'\x03')
        self.assertEqual(mem[0x4624e4], b'A')
        self.assertEqual(mem[0x7fffffffdafa], b'\x00')
        self.assertEqual(mem[0x7fffffffdafb], b'\x00')
        self.assertEqual(mem[0x7fffffffdafc], b'\x00')
        self.assertEqual(mem[0x7fffffffdafd], b'\x00')
        self.assertEqual(mem[0x7fffffffdafe], b'\x00')
        self.assertEqual(mem[0x4624e5], b'\\')
        self.assertEqual(cpu.R12, 7066696)
        self.assertEqual(cpu.RSP, 140737488345864)
        self.assertEqual(cpu.RIP, 4596966)
        self.assertEqual(cpu.RBP, 140737488345888)

    def test_POP_4(self):
        ''' Instruction POP_4
            Groups: mode64
            0x6ff233:	pop	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x006ff000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcca0] = '\x00'
        mem[0x7fffffffcca1] = '\x00'
        mem[0x7fffffffcca2] = '\x00'
        mem[0x7fffffffcca3] = '\x00'
        mem[0x7fffffffcca4] = '\x00'
        mem[0x7fffffffcca5] = '\x00'
        mem[0x7fffffffcca6] = '\x00'
        mem[0x7fffffffcca7] = '\x00'
        mem[0x7fffffffcca8] = '\x01'
        mem[0x7fffffffcca9] = '\x00'
        mem[0x7fffffffccaa] = '\x00'
        mem[0x7fffffffccab] = '\x00'
        mem[0x7fffffffccac] = '\x00'
        mem[0x7fffffffccad] = '\x00'
        mem[0x7fffffffccae] = '\x00'
        mem[0x7fffffffccaf] = '\x00'
        mem[0x7fffffffccb0] = '@'
        mem[0x006ff233] = 'Z'
        cpu.RSP = 0x7fffffffcca8
        cpu.RDX = 0x80000001
        cpu.RIP = 0x6ff233
        cpu.RBP = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcca0], b'\x00')
        self.assertEqual(mem[0x7fffffffcca1], b'\x00')
        self.assertEqual(mem[0x7fffffffcca2], b'\x00')
        self.assertEqual(mem[0x7fffffffcca3], b'\x00')
        self.assertEqual(mem[0x7fffffffcca4], b'\x00')
        self.assertEqual(mem[0x7fffffffcca5], b'\x00')
        self.assertEqual(mem[0x7fffffffcca6], b'\x00')
        self.assertEqual(mem[0x7fffffffcca7], b'\x00')
        self.assertEqual(mem[0x7fffffffcca8], b'\x01')
        self.assertEqual(mem[0x7fffffffcca9], b'\x00')
        self.assertEqual(mem[0x7fffffffccaa], b'\x00')
        self.assertEqual(mem[0x7fffffffccab], b'\x00')
        self.assertEqual(mem[0x7fffffffccac], b'\x00')
        self.assertEqual(mem[0x7fffffffccad], b'\x00')
        self.assertEqual(mem[0x7fffffffccae], b'\x00')
        self.assertEqual(mem[0x7fffffffccaf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'@')
        self.assertEqual(mem[0x6ff233], b'Z')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RDX, 1)
        self.assertEqual(cpu.RIP, 7336500)
        self.assertEqual(cpu.RBP, 0)

    def test_POP_5(self):
        ''' Instruction POP_5
            Groups: mode64
            0x632f8a:	pop	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00632000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcca0] = '\x00'
        mem[0x7fffffffcca1] = '\x00'
        mem[0x7fffffffcca2] = '\x00'
        mem[0x7fffffffcca3] = '\x00'
        mem[0x7fffffffcca4] = '\x00'
        mem[0x7fffffffcca5] = '\x00'
        mem[0x7fffffffcca6] = '\x00'
        mem[0x7fffffffcca7] = '\x00'
        mem[0x7fffffffcca8] = '\x00'
        mem[0x7fffffffcca9] = '\x00'
        mem[0x00632f8a] = 'Z'
        mem[0x7fffffffccab] = '\x80'
        mem[0x7fffffffccac] = '\x00'
        mem[0x7fffffffccad] = '\x00'
        mem[0x7fffffffccae] = '\x00'
        mem[0x7fffffffccaf] = '\x00'
        mem[0x7fffffffccb0] = '\x00'
        mem[0x7fffffffccaa] = '\x00'
        cpu.RSP = 0x7fffffffcca8
        cpu.RDX = 0x7f
        cpu.RIP = 0x632f8a
        cpu.RBP = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcca0], b'\x00')
        self.assertEqual(mem[0x7fffffffcca1], b'\x00')
        self.assertEqual(mem[0x7fffffffcca2], b'\x00')
        self.assertEqual(mem[0x7fffffffcca3], b'\x00')
        self.assertEqual(mem[0x7fffffffcca4], b'\x00')
        self.assertEqual(mem[0x7fffffffcca5], b'\x00')
        self.assertEqual(mem[0x7fffffffcca6], b'\x00')
        self.assertEqual(mem[0x7fffffffcca7], b'\x00')
        self.assertEqual(mem[0x7fffffffcca8], b'\x00')
        self.assertEqual(mem[0x7fffffffcca9], b'\x00')
        self.assertEqual(mem[0x632f8a], b'Z')
        self.assertEqual(mem[0x7fffffffccab], b'\x80')
        self.assertEqual(mem[0x7fffffffccac], b'\x00')
        self.assertEqual(mem[0x7fffffffccad], b'\x00')
        self.assertEqual(mem[0x7fffffffccae], b'\x00')
        self.assertEqual(mem[0x7fffffffccaf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'\x00')
        self.assertEqual(mem[0x7fffffffccaa], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RDX, 2147483648)
        self.assertEqual(cpu.RIP, 6500235)
        self.assertEqual(cpu.RBP, 0)

    def test_POP_6(self):
        ''' Instruction POP_6
            Groups: mode64
            0x737db3:	pop	rdx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00737000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcca0] = '\x00'
        mem[0x7fffffffcca1] = '\x00'
        mem[0x7fffffffcca2] = '\x00'
        mem[0x7fffffffcca3] = '\x00'
        mem[0x7fffffffcca4] = '\x00'
        mem[0x7fffffffcca5] = '\x00'
        mem[0x7fffffffcca6] = '\x00'
        mem[0x7fffffffcca7] = '\x00'
        mem[0x7fffffffcca8] = '\x00'
        mem[0x7fffffffcca9] = '\xff'
        mem[0x7fffffffccaa] = '\x00'
        mem[0x7fffffffccab] = '\x00'
        mem[0x7fffffffccac] = '\x00'
        mem[0x7fffffffccad] = '\x00'
        mem[0x7fffffffccae] = '\x00'
        mem[0x7fffffffccaf] = '\x00'
        mem[0x7fffffffccb0] = '@'
        mem[0x00737db3] = 'Z'
        cpu.RSP = 0x7fffffffcca8
        cpu.RDX = 0x40
        cpu.RIP = 0x737db3
        cpu.RBP = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcca0], b'\x00')
        self.assertEqual(mem[0x7fffffffcca1], b'\x00')
        self.assertEqual(mem[0x7fffffffcca2], b'\x00')
        self.assertEqual(mem[0x7fffffffcca3], b'\x00')
        self.assertEqual(mem[0x7fffffffcca4], b'\x00')
        self.assertEqual(mem[0x7fffffffcca5], b'\x00')
        self.assertEqual(mem[0x7fffffffcca6], b'\x00')
        self.assertEqual(mem[0x7fffffffcca7], b'\x00')
        self.assertEqual(mem[0x7fffffffcca8], b'\x00')
        self.assertEqual(mem[0x7fffffffcca9], b'\xff')
        self.assertEqual(mem[0x7fffffffccaa], b'\x00')
        self.assertEqual(mem[0x7fffffffccab], b'\x00')
        self.assertEqual(mem[0x7fffffffccac], b'\x00')
        self.assertEqual(mem[0x7fffffffccad], b'\x00')
        self.assertEqual(mem[0x7fffffffccae], b'\x00')
        self.assertEqual(mem[0x7fffffffccaf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'@')
        self.assertEqual(mem[0x737db3], b'Z')
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RDX, 65280)
        self.assertEqual(cpu.RIP, 7568820)
        self.assertEqual(cpu.RBP, 0)

    def test_POR_1(self):
        ''' Instruction POR_1
            Groups: sse2
            0x7ffff7df43a7:	por	xmm0, xmm4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df43a8] = '\x0f'
        mem[0x7ffff7df43a9] = '\xeb'
        mem[0x7ffff7df43aa] = '\xc4'
        mem[0x7ffff7df43a7] = 'f'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x7ffff7df43a7
        cpu.XMM4 = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df43a8], b'\x0f')
        self.assertEqual(mem[0x7ffff7df43a9], b'\xeb')
        self.assertEqual(mem[0x7ffff7df43aa], b'\xc4')
        self.assertEqual(mem[0x7ffff7df43a7], b'f')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM4, 0)
        self.assertEqual(cpu.RIP, 140737351992235)

    def test_POR_2(self):
        ''' Instruction POR_2
            Groups: sse2
            0x7ffff7df43a7:	por	xmm0, xmm4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df43a8] = '\x0f'
        mem[0x7ffff7df43a9] = '\xeb'
        mem[0x7ffff7df43aa] = '\xc4'
        mem[0x7ffff7df43a7] = 'f'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x7ffff7df43a7
        cpu.XMM4 = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df43a8], b'\x0f')
        self.assertEqual(mem[0x7ffff7df43a9], b'\xeb')
        self.assertEqual(mem[0x7ffff7df43aa], b'\xc4')
        self.assertEqual(mem[0x7ffff7df43a7], b'f')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM4, 0)
        self.assertEqual(cpu.RIP, 140737351992235)

    def test_POR_3(self):
        ''' Instruction POR_3
            Groups: sse2
            0x7ffff7df43a7:	por	xmm0, xmm4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df43a8] = '\x0f'
        mem[0x7ffff7df43a9] = '\xeb'
        mem[0x7ffff7df43aa] = '\xc4'
        mem[0x7ffff7df43a7] = 'f'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x7ffff7df43a7
        cpu.XMM4 = 0xff00000000ff000000000000000000
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df43a8], b'\x0f')
        self.assertEqual(mem[0x7ffff7df43a9], b'\xeb')
        self.assertEqual(mem[0x7ffff7df43aa], b'\xc4')
        self.assertEqual(mem[0x7ffff7df43a7], b'f')
        self.assertEqual(cpu.XMM0, 1324035698927585248728408323480616960)
        self.assertEqual(cpu.XMM4, 1324035698927585248728408323480616960)
        self.assertEqual(cpu.RIP, 140737351992235)

    def test_POR_4(self):
        ''' Instruction POR_4
            Groups: sse2
            0x7ffff7df43a7:	por	xmm0, xmm4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df43a8] = '\x0f'
        mem[0x7ffff7df43a9] = '\xeb'
        mem[0x7ffff7df43aa] = '\xc4'
        mem[0x7ffff7df43a7] = 'f'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x7ffff7df43a7
        cpu.XMM4 = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df43a8], b'\x0f')
        self.assertEqual(mem[0x7ffff7df43a9], b'\xeb')
        self.assertEqual(mem[0x7ffff7df43aa], b'\xc4')
        self.assertEqual(mem[0x7ffff7df43a7], b'f')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM4, 0)
        self.assertEqual(cpu.RIP, 140737351992235)

    def test_POR_5(self):
        ''' Instruction POR_5
            Groups: sse2
            0x7ffff7df4412:	por	xmm0, xmm3
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4412] = 'f'
        mem[0x7ffff7df4413] = '\x0f'
        mem[0x7ffff7df4414] = '\xeb'
        mem[0x7ffff7df4415] = '\xc3'
        cpu.XMM3 = 0xff000000000000
        cpu.XMM0 = 0x0
        cpu.RIP = 0x7ffff7df4412
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4412], b'f')
        self.assertEqual(mem[0x7ffff7df4413], b'\x0f')
        self.assertEqual(mem[0x7ffff7df4414], b'\xeb')
        self.assertEqual(mem[0x7ffff7df4415], b'\xc3')
        self.assertEqual(cpu.XMM3, 71776119061217280)
        self.assertEqual(cpu.XMM0, 71776119061217280)
        self.assertEqual(cpu.RIP, 140737351992342)

    def test_POR_6(self):
        ''' Instruction POR_6
            Groups: sse2
            0x7ffff7ac0b17:	por	xmm0, xmm4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0b18] = '\x0f'
        mem[0x7ffff7ac0b19] = '\xeb'
        mem[0x7ffff7ac0b1a] = '\xc4'
        mem[0x7ffff7ac0b17] = 'f'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x7ffff7ac0b17
        cpu.XMM4 = 0xffffff000000ff
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0b18], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0b19], b'\xeb')
        self.assertEqual(mem[0x7ffff7ac0b1a], b'\xc4')
        self.assertEqual(mem[0x7ffff7ac0b17], b'f')
        self.assertEqual(cpu.XMM0, 72057589742960895)
        self.assertEqual(cpu.XMM4, 72057589742960895)
        self.assertEqual(cpu.RIP, 140737348635419)

    def test_PSHUFD_1(self):
        ''' Instruction PSHUFD_1
            Groups: sse2
            0x7ffff7ac0af8:	pshufd	xmm1, xmm1, 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0af8] = 'f'
        mem[0x7ffff7ac0af9] = '\x0f'
        mem[0x7ffff7ac0afa] = 'p'
        mem[0x7ffff7ac0afb] = '\xc9'
        mem[0x7ffff7ac0afc] = '\x00'
        cpu.XMM1 = 0x25252525
        cpu.RIP = 0x7ffff7ac0af8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0af8], b'f')
        self.assertEqual(mem[0x7ffff7ac0af9], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0afa], b'p')
        self.assertEqual(mem[0x7ffff7ac0afb], b'\xc9')
        self.assertEqual(mem[0x7ffff7ac0afc], b'\x00')
        self.assertEqual(cpu.XMM1, 49374304219900875090764158725393818917)
        self.assertEqual(cpu.RIP, 140737348635389)

    def test_PSHUFD_2(self):
        ''' Instruction PSHUFD_2
            Groups: sse2
            0x7ffff7ac0af8:	pshufd	xmm1, xmm1, 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0af8] = 'f'
        mem[0x7ffff7ac0af9] = '\x0f'
        mem[0x7ffff7ac0afa] = 'p'
        mem[0x7ffff7ac0afb] = '\xc9'
        mem[0x7ffff7ac0afc] = '\x00'
        cpu.XMM1 = 0x25252525
        cpu.RIP = 0x7ffff7ac0af8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0af8], b'f')
        self.assertEqual(mem[0x7ffff7ac0af9], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0afa], b'p')
        self.assertEqual(mem[0x7ffff7ac0afb], b'\xc9')
        self.assertEqual(mem[0x7ffff7ac0afc], b'\x00')
        self.assertEqual(cpu.XMM1, 49374304219900875090764158725393818917)
        self.assertEqual(cpu.RIP, 140737348635389)

    def test_PSHUFD_3(self):
        ''' Instruction PSHUFD_3
            Groups: sse2
            0x7ffff7df4388:	pshufd	xmm1, xmm1, 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4388] = 'f'
        mem[0x7ffff7df4389] = '\x0f'
        mem[0x7ffff7df438a] = 'p'
        mem[0x7ffff7df438b] = '\xc9'
        mem[0x7ffff7df438c] = '\x00'
        cpu.XMM1 = 0x24242424
        cpu.RIP = 0x7ffff7df4388
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4388], b'f')
        self.assertEqual(mem[0x7ffff7df4389], b'\x0f')
        self.assertEqual(mem[0x7ffff7df438a], b'p')
        self.assertEqual(mem[0x7ffff7df438b], b'\xc9')
        self.assertEqual(mem[0x7ffff7df438c], b'\x00')
        self.assertEqual(cpu.XMM1, 48039863565308959547770532813896688676)
        self.assertEqual(cpu.RIP, 140737351992205)

    def test_PSHUFD_4(self):
        ''' Instruction PSHUFD_4
            Groups: sse2
            0x7ffff7ab799a:	pshufd	xmm1, xmm1, 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab7000, 0x1000, 'rwx')
        mem[0x7ffff7ab799a] = 'f'
        mem[0x7ffff7ab799b] = '\x0f'
        mem[0x7ffff7ab799c] = 'p'
        mem[0x7ffff7ab799d] = '\xc9'
        mem[0x7ffff7ab799e] = '\x00'
        cpu.XMM1 = 0x2f2f2f2f
        cpu.RIP = 0x7ffff7ab799a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab799a], b'f')
        self.assertEqual(mem[0x7ffff7ab799b], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab799c], b'p')
        self.assertEqual(mem[0x7ffff7ab799d], b'\xc9')
        self.assertEqual(mem[0x7ffff7ab799e], b'\x00')
        self.assertEqual(cpu.XMM1, 62718710765820030520700417840365121327)
        self.assertEqual(cpu.RIP, 140737348598175)

    def test_PSHUFD_5(self):
        ''' Instruction PSHUFD_5
            Groups: sse2
            0x7ffff7df4388:	pshufd	xmm1, xmm1, 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4388] = 'f'
        mem[0x7ffff7df4389] = '\x0f'
        mem[0x7ffff7df438a] = 'p'
        mem[0x7ffff7df438b] = '\xc9'
        mem[0x7ffff7df438c] = '\x00'
        cpu.XMM1 = 0x24242424
        cpu.RIP = 0x7ffff7df4388
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4388], b'f')
        self.assertEqual(mem[0x7ffff7df4389], b'\x0f')
        self.assertEqual(mem[0x7ffff7df438a], b'p')
        self.assertEqual(mem[0x7ffff7df438b], b'\xc9')
        self.assertEqual(mem[0x7ffff7df438c], b'\x00')
        self.assertEqual(cpu.XMM1, 48039863565308959547770532813896688676)
        self.assertEqual(cpu.RIP, 140737351992205)

    def test_PSHUFD_6(self):
        ''' Instruction PSHUFD_6
            Groups: sse2
            0x7ffff7ab799a:	pshufd	xmm1, xmm1, 0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab7000, 0x1000, 'rwx')
        mem[0x7ffff7ab799a] = 'f'
        mem[0x7ffff7ab799b] = '\x0f'
        mem[0x7ffff7ab799c] = 'p'
        mem[0x7ffff7ab799d] = '\xc9'
        mem[0x7ffff7ab799e] = '\x00'
        cpu.XMM1 = 0x2f2f2f2f
        cpu.RIP = 0x7ffff7ab799a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ab799a], b'f')
        self.assertEqual(mem[0x7ffff7ab799b], b'\x0f')
        self.assertEqual(mem[0x7ffff7ab799c], b'p')
        self.assertEqual(mem[0x7ffff7ab799d], b'\xc9')
        self.assertEqual(mem[0x7ffff7ab799e], b'\x00')
        self.assertEqual(cpu.XMM1, 62718710765820030520700417840365121327)
        self.assertEqual(cpu.RIP, 140737348598175)

    def test_PUNPCKLBW_1(self):
        ''' Instruction PUNPCKLBW_1
            Groups: sse2
            0x7ffff7df437b:	punpcklbw	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df437b] = 'f'
        mem[0x7ffff7df437c] = '\x0f'
        mem[0x7ffff7df437d] = '`'
        mem[0x7ffff7df437e] = '\xc9'
        cpu.XMM1 = 0x24
        cpu.RIP = 0x7ffff7df437b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df437b], b'f')
        self.assertEqual(mem[0x7ffff7df437c], b'\x0f')
        self.assertEqual(mem[0x7ffff7df437d], b'`')
        self.assertEqual(mem[0x7ffff7df437e], b'\xc9')
        self.assertEqual(cpu.XMM1, 9252)
        self.assertEqual(cpu.RIP, 140737351992191)

    def test_PUNPCKLBW_2(self):
        ''' Instruction PUNPCKLBW_2
            Groups: sse2
            0x7ffff7ac0aeb:	punpcklbw	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0aeb] = 'f'
        mem[0x7ffff7ac0aec] = '\x0f'
        mem[0x7ffff7ac0aed] = '`'
        mem[0x7ffff7ac0aee] = '\xc9'
        cpu.XMM1 = 0x25
        cpu.RIP = 0x7ffff7ac0aeb
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0aeb], b'f')
        self.assertEqual(mem[0x7ffff7ac0aec], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0aed], b'`')
        self.assertEqual(mem[0x7ffff7ac0aee], b'\xc9')
        self.assertEqual(cpu.XMM1, 9509)
        self.assertEqual(cpu.RIP, 140737348635375)

    def test_PUNPCKLBW_3(self):
        ''' Instruction PUNPCKLBW_3
            Groups: sse2
            0x7ffff7ac0aeb:	punpcklbw	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0aeb] = 'f'
        mem[0x7ffff7ac0aec] = '\x0f'
        mem[0x7ffff7ac0aed] = '`'
        mem[0x7ffff7ac0aee] = '\xc9'
        cpu.XMM1 = 0x25
        cpu.RIP = 0x7ffff7ac0aeb
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0aeb], b'f')
        self.assertEqual(mem[0x7ffff7ac0aec], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0aed], b'`')
        self.assertEqual(mem[0x7ffff7ac0aee], b'\xc9')
        self.assertEqual(cpu.XMM1, 9509)
        self.assertEqual(cpu.RIP, 140737348635375)

    def test_PUNPCKLBW_4(self):
        ''' Instruction PUNPCKLBW_4
            Groups: sse2
            0x4579cc:	punpcklbw	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x004579cc] = 'f'
        mem[0x004579cd] = '\x0f'
        mem[0x004579ce] = '`'
        mem[0x004579cf] = '\xc9'
        cpu.XMM1 = 0x2f
        cpu.RIP = 0x4579cc
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4579cc], b'f')
        self.assertEqual(mem[0x4579cd], b'\x0f')
        self.assertEqual(mem[0x4579ce], b'`')
        self.assertEqual(mem[0x4579cf], b'\xc9')
        self.assertEqual(cpu.XMM1, 12079)
        self.assertEqual(cpu.RIP, 4553168)

    def test_PUNPCKLBW_5(self):
        ''' Instruction PUNPCKLBW_5
            Groups: sse2
            0x45794c:	punpcklbw	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x0045794c] = 'f'
        mem[0x0045794d] = '\x0f'
        mem[0x0045794e] = '`'
        mem[0x0045794f] = '\xc9'
        cpu.XMM1 = 0x2f
        cpu.RIP = 0x45794c
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x45794c], b'f')
        self.assertEqual(mem[0x45794d], b'\x0f')
        self.assertEqual(mem[0x45794e], b'`')
        self.assertEqual(mem[0x45794f], b'\xc9')
        self.assertEqual(cpu.XMM1, 12079)
        self.assertEqual(cpu.RIP, 4553040)

    def test_PUNPCKLBW_6(self):
        ''' Instruction PUNPCKLBW_6
            Groups: sse2
            0x7ffff7df437b:	punpcklbw	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df437b] = 'f'
        mem[0x7ffff7df437c] = '\x0f'
        mem[0x7ffff7df437d] = '`'
        mem[0x7ffff7df437e] = '\xc9'
        cpu.XMM1 = 0x24
        cpu.RIP = 0x7ffff7df437b
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df437b], b'f')
        self.assertEqual(mem[0x7ffff7df437c], b'\x0f')
        self.assertEqual(mem[0x7ffff7df437d], b'`')
        self.assertEqual(mem[0x7ffff7df437e], b'\xc9')
        self.assertEqual(cpu.XMM1, 9252)
        self.assertEqual(cpu.RIP, 140737351992191)

    def test_PUNPCKLWD_1(self):
        ''' Instruction PUNPCKLWD_1
            Groups: sse2
            0x457a46:	punpcklwd	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x00457a48] = 'a'
        mem[0x00457a49] = '\xc9'
        mem[0x00457a46] = 'f'
        mem[0x00457a47] = '\x0f'
        cpu.XMM1 = 0x2f2f
        cpu.RIP = 0x457a46
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x457a48], b'a')
        self.assertEqual(mem[0x457a49], b'\xc9')
        self.assertEqual(mem[0x457a46], b'f')
        self.assertEqual(mem[0x457a47], b'\x0f')
        self.assertEqual(cpu.XMM1, 791621423)
        self.assertEqual(cpu.RIP, 4553290)

    def test_PUNPCKLWD_2(self):
        ''' Instruction PUNPCKLWD_2
            Groups: sse2
            0x421b24:	punpcklwd	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00421000, 0x1000, 'rwx')
        mem[0x00421b24] = 'f'
        mem[0x00421b25] = '\x0f'
        mem[0x00421b26] = 'a'
        mem[0x00421b27] = '\xc9'
        cpu.XMM1 = 0x2525
        cpu.RIP = 0x421b24
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x421b24], b'f')
        self.assertEqual(mem[0x421b25], b'\x0f')
        self.assertEqual(mem[0x421b26], b'a')
        self.assertEqual(mem[0x421b27], b'\xc9')
        self.assertEqual(cpu.XMM1, 623191333)
        self.assertEqual(cpu.RIP, 4332328)

    def test_PUNPCKLWD_3(self):
        ''' Instruction PUNPCKLWD_3
            Groups: sse2
            0x7ffff7df4384:	punpcklwd	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4384] = 'f'
        mem[0x7ffff7df4385] = '\x0f'
        mem[0x7ffff7df4386] = 'a'
        mem[0x7ffff7df4387] = '\xc9'
        cpu.XMM1 = 0x2424
        cpu.RIP = 0x7ffff7df4384
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4384], b'f')
        self.assertEqual(mem[0x7ffff7df4385], b'\x0f')
        self.assertEqual(mem[0x7ffff7df4386], b'a')
        self.assertEqual(mem[0x7ffff7df4387], b'\xc9')
        self.assertEqual(cpu.XMM1, 606348324)
        self.assertEqual(cpu.RIP, 140737351992200)

    def test_PUNPCKLWD_4(self):
        ''' Instruction PUNPCKLWD_4
            Groups: sse2
            0x7ffff7df4384:	punpcklwd	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4384] = 'f'
        mem[0x7ffff7df4385] = '\x0f'
        mem[0x7ffff7df4386] = 'a'
        mem[0x7ffff7df4387] = '\xc9'
        cpu.XMM1 = 0x2424
        cpu.RIP = 0x7ffff7df4384
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4384], b'f')
        self.assertEqual(mem[0x7ffff7df4385], b'\x0f')
        self.assertEqual(mem[0x7ffff7df4386], b'a')
        self.assertEqual(mem[0x7ffff7df4387], b'\xc9')
        self.assertEqual(cpu.XMM1, 606348324)
        self.assertEqual(cpu.RIP, 140737351992200)

    def test_PUNPCKLWD_5(self):
        ''' Instruction PUNPCKLWD_5
            Groups: sse2
            0x45a576:	punpcklwd	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0045a000, 0x1000, 'rwx')
        mem[0x0045a578] = 'a'
        mem[0x0045a579] = '\xc9'
        mem[0x0045a576] = 'f'
        mem[0x0045a577] = '\x0f'
        cpu.XMM1 = 0x2f2f
        cpu.RIP = 0x45a576
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x45a578], b'a')
        self.assertEqual(mem[0x45a579], b'\xc9')
        self.assertEqual(mem[0x45a576], b'f')
        self.assertEqual(mem[0x45a577], b'\x0f')
        self.assertEqual(cpu.XMM1, 791621423)
        self.assertEqual(cpu.RIP, 4564346)

    def test_PUNPCKLWD_6(self):
        ''' Instruction PUNPCKLWD_6
            Groups: sse2
            0x7ffff7ac0af4:	punpcklwd	xmm1, xmm1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ac0000, 0x1000, 'rwx')
        mem[0x7ffff7ac0af4] = 'f'
        mem[0x7ffff7ac0af5] = '\x0f'
        mem[0x7ffff7ac0af6] = 'a'
        mem[0x7ffff7ac0af7] = '\xc9'
        cpu.XMM1 = 0x2525
        cpu.RIP = 0x7ffff7ac0af4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ac0af4], b'f')
        self.assertEqual(mem[0x7ffff7ac0af5], b'\x0f')
        self.assertEqual(mem[0x7ffff7ac0af6], b'a')
        self.assertEqual(mem[0x7ffff7ac0af7], b'\xc9')
        self.assertEqual(cpu.XMM1, 623191333)
        self.assertEqual(cpu.RIP, 140737348635384)

    def test_PUSH_1(self):
        ''' Instruction PUSH_1
            Groups: mode64
            0x7ffff7de407a:	push	r12
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd7a0] = '4'
        mem[0x7ffff7de407b] = 'T'
        mem[0x7fffffffd79a] = '\xff'
        mem[0x7fffffffd790] = 'X'
        mem[0x7fffffffd791] = 'v'
        mem[0x7fffffffd792] = '\xff'
        mem[0x7fffffffd793] = '\xf7'
        mem[0x7fffffffd794] = '\xff'
        mem[0x7fffffffd795] = '\x7f'
        mem[0x7fffffffd796] = '\x00'
        mem[0x7fffffffd797] = '\x00'
        mem[0x7fffffffd798] = '8'
        mem[0x7fffffffd799] = '\xd8'
        mem[0x7ffff7de407a] = 'A'
        mem[0x7fffffffd79b] = '\xff'
        mem[0x7fffffffd79c] = '\xff'
        mem[0x7fffffffd79d] = '\x7f'
        mem[0x7fffffffd79e] = '\x00'
        mem[0x7fffffffd79f] = '\x00'
        cpu.RSP = 0x7fffffffd798
        cpu.R12 = 0x7ffff7ff7658
        cpu.RIP = 0x7ffff7de407a
        cpu.RBP = 0x7fffffffd870
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd7a0], b'4')
        self.assertEqual(mem[0x7ffff7de407b], b'T')
        self.assertEqual(mem[0x7ffff7de407a], b'A')
        self.assertEqual(mem[0x7fffffffd790], b'X')
        self.assertEqual(mem[0x7fffffffd791], b'v')
        self.assertEqual(mem[0x7fffffffd792], b'\xff')
        self.assertEqual(mem[0x7fffffffd793], b'\xf7')
        self.assertEqual(mem[0x7fffffffd794], b'\xff')
        self.assertEqual(mem[0x7fffffffd795], b'\x7f')
        self.assertEqual(mem[0x7fffffffd796], b'\x00')
        self.assertEqual(mem[0x7fffffffd797], b'\x00')
        self.assertEqual(mem[0x7fffffffd798], b'8')
        self.assertEqual(mem[0x7fffffffd799], b'\xd8')
        self.assertEqual(mem[0x7fffffffd79a], b'\xff')
        self.assertEqual(mem[0x7fffffffd79b], b'\xff')
        self.assertEqual(mem[0x7fffffffd79c], b'\xff')
        self.assertEqual(mem[0x7fffffffd79d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd79e], b'\x00')
        self.assertEqual(mem[0x7fffffffd79f], b'\x00')
        self.assertEqual(cpu.R12, 140737354102360)
        self.assertEqual(cpu.RSP, 140737488344976)
        self.assertEqual(cpu.RIP, 140737351925884)
        self.assertEqual(cpu.RBP, 140737488345200)

    def test_PUSH_2(self):
        ''' Instruction PUSH_2
            Groups: mode64
            0x722546:	push	0xff00
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00722000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcca8] = '\x00'
        mem[0x7fffffffcca9] = '\xff'
        mem[0x7fffffffccaa] = '\x00'
        mem[0x7fffffffccab] = '\x00'
        mem[0x7fffffffccac] = '\x00'
        mem[0x7fffffffccad] = '\x00'
        mem[0x7fffffffccae] = '\x00'
        mem[0x7fffffffccaf] = '\x00'
        mem[0x7fffffffccb0] = '\xfe'
        mem[0x7fffffffccb1] = '\xff'
        mem[0x7fffffffccb2] = '\xff'
        mem[0x7fffffffccb3] = '\xff'
        mem[0x7fffffffccb4] = '@'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = '\xfe'
        mem[0x00722546] = 'h'
        mem[0x00722547] = '\x00'
        mem[0x00722548] = '\xff'
        mem[0x00722549] = '\x00'
        mem[0x0072254a] = '\x00'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x722546
        cpu.RBP = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcca8], b'\x00')
        self.assertEqual(mem[0x7fffffffcca9], b'\xff')
        self.assertEqual(mem[0x7fffffffccaa], b'\x00')
        self.assertEqual(mem[0x7fffffffccab], b'\x00')
        self.assertEqual(mem[0x7fffffffccac], b'\x00')
        self.assertEqual(mem[0x7fffffffccad], b'\x00')
        self.assertEqual(mem[0x7fffffffccae], b'\x00')
        self.assertEqual(mem[0x7fffffffccaf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'\xfe')
        self.assertEqual(mem[0x7fffffffccb1], b'\xff')
        self.assertEqual(mem[0x7fffffffccb2], b'\xff')
        self.assertEqual(mem[0x7fffffffccb3], b'\xff')
        self.assertEqual(mem[0x7fffffffccb4], b'@')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'\xfe')
        self.assertEqual(mem[0x722546], b'h')
        self.assertEqual(mem[0x722547], b'\x00')
        self.assertEqual(mem[0x722548], b'\xff')
        self.assertEqual(mem[0x722549], b'\x00')
        self.assertEqual(mem[0x72254a], b'\x00')
        self.assertEqual(cpu.RSP, 140737488342184)
        self.assertEqual(cpu.RIP, 7480651)
        self.assertEqual(cpu.RBP, 0)

    def test_PUSH_3(self):
        ''' Instruction PUSH_3
            Groups: mode64
            0x744c3e:	push	0xf00aabb
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00744000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcca8] = '\xbb'
        mem[0x7fffffffcca9] = '\xaa'
        mem[0x7fffffffccaa] = '\x00'
        mem[0x7fffffffccab] = '\x0f'
        mem[0x7fffffffccac] = '\x00'
        mem[0x7fffffffccad] = '\x00'
        mem[0x7fffffffccae] = '\x00'
        mem[0x7fffffffccaf] = '\x00'
        mem[0x7fffffffccb0] = '\x00'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x80'
        mem[0x7fffffffccb4] = '!'
        mem[0x7fffffffccb5] = 'C'
        mem[0x7fffffffccb6] = 'e'
        mem[0x7fffffffccb7] = '\x87'
        mem[0x7fffffffccb8] = '@'
        mem[0x00744c3e] = 'h'
        mem[0x00744c3f] = '\xbb'
        mem[0x00744c40] = '\xaa'
        mem[0x00744c41] = '\x00'
        mem[0x00744c42] = '\x0f'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x744c3e
        cpu.RBP = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcca8], b'\xbb')
        self.assertEqual(mem[0x7fffffffcca9], b'\xaa')
        self.assertEqual(mem[0x7fffffffccaa], b'\x00')
        self.assertEqual(mem[0x7fffffffccab], b'\x0f')
        self.assertEqual(mem[0x7fffffffccac], b'\x00')
        self.assertEqual(mem[0x7fffffffccad], b'\x00')
        self.assertEqual(mem[0x7fffffffccae], b'\x00')
        self.assertEqual(mem[0x7fffffffccaf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'\x00')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x80')
        self.assertEqual(mem[0x7fffffffccb4], b'!')
        self.assertEqual(mem[0x7fffffffccb5], b'C')
        self.assertEqual(mem[0x7fffffffccb6], b'e')
        self.assertEqual(mem[0x7fffffffccb7], b'\x87')
        self.assertEqual(mem[0x7fffffffccb8], b'@')
        self.assertEqual(mem[0x744c3e], b'h')
        self.assertEqual(mem[0x744c3f], b'\xbb')
        self.assertEqual(mem[0x744c40], b'\xaa')
        self.assertEqual(mem[0x744c41], b'\x00')
        self.assertEqual(mem[0x744c42], b'\x0f')
        self.assertEqual(cpu.RSP, 140737488342184)
        self.assertEqual(cpu.RIP, 7621699)
        self.assertEqual(cpu.RBP, 0)

    def test_PUSH_4(self):
        ''' Instruction PUSH_4
            Groups: mode64
            0x6651fa:	push	rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00665000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcca8] = '\x7f'
        mem[0x7fffffffcca9] = '\x00'
        mem[0x7fffffffccaa] = '\x00'
        mem[0x7fffffffccab] = '\x00'
        mem[0x7fffffffccac] = '\x00'
        mem[0x7fffffffccad] = '\x00'
        mem[0x7fffffffccae] = '\x00'
        mem[0x7fffffffccaf] = '\x00'
        mem[0x7fffffffccb0] = '\x7f'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x00'
        mem[0x7fffffffccb4] = ' '
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = '!'
        mem[0x006651fa] = 'P'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x6651fa
        cpu.RAX = 0x7f
        cpu.RBP = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcca8], b'\x7f')
        self.assertEqual(mem[0x7fffffffcca9], b'\x00')
        self.assertEqual(mem[0x7fffffffccaa], b'\x00')
        self.assertEqual(mem[0x7fffffffccab], b'\x00')
        self.assertEqual(mem[0x7fffffffccac], b'\x00')
        self.assertEqual(mem[0x7fffffffccad], b'\x00')
        self.assertEqual(mem[0x7fffffffccae], b'\x00')
        self.assertEqual(mem[0x7fffffffccaf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x00')
        self.assertEqual(mem[0x7fffffffccb4], b' ')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'!')
        self.assertEqual(mem[0x6651fa], b'P')
        self.assertEqual(cpu.RSP, 140737488342184)
        self.assertEqual(cpu.RAX, 127)
        self.assertEqual(cpu.RIP, 6705659)
        self.assertEqual(cpu.RBP, 0)

    def test_PUSH_5(self):
        ''' Instruction PUSH_5
            Groups: mode64
            0x7ffff7de4330:	push	rbp
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda40] = '\x01'
        mem[0x7ffff7de4330] = 'U'
        mem[0x7fffffffda30] = 'p'
        mem[0x7fffffffda31] = '\xdb'
        mem[0x7fffffffda32] = '\xff'
        mem[0x7fffffffda33] = '\xff'
        mem[0x7fffffffda34] = '\xff'
        mem[0x7fffffffda35] = '\x7f'
        mem[0x7fffffffda36] = '\x00'
        mem[0x7fffffffda37] = '\x00'
        mem[0x7fffffffda38] = '\x94'
        mem[0x7fffffffda39] = 'b'
        mem[0x7fffffffda3a] = '\xde'
        mem[0x7fffffffda3b] = '\xf7'
        mem[0x7fffffffda3c] = '\xff'
        mem[0x7fffffffda3d] = '\x7f'
        mem[0x7fffffffda3e] = '\x00'
        mem[0x7fffffffda3f] = '\x00'
        cpu.RSP = 0x7fffffffda38
        cpu.RIP = 0x7ffff7de4330
        cpu.RBP = 0x7fffffffdb70
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda40], b'\x01')
        self.assertEqual(mem[0x7fffffffda30], b'p')
        self.assertEqual(mem[0x7ffff7de4330], b'U')
        self.assertEqual(mem[0x7fffffffda31], b'\xdb')
        self.assertEqual(mem[0x7fffffffda32], b'\xff')
        self.assertEqual(mem[0x7fffffffda33], b'\xff')
        self.assertEqual(mem[0x7fffffffda34], b'\xff')
        self.assertEqual(mem[0x7fffffffda35], b'\x7f')
        self.assertEqual(mem[0x7fffffffda36], b'\x00')
        self.assertEqual(mem[0x7fffffffda37], b'\x00')
        self.assertEqual(mem[0x7fffffffda38], b'\x94')
        self.assertEqual(mem[0x7fffffffda39], b'b')
        self.assertEqual(mem[0x7fffffffda3a], b'\xde')
        self.assertEqual(mem[0x7fffffffda3b], b'\xf7')
        self.assertEqual(mem[0x7fffffffda3c], b'\xff')
        self.assertEqual(mem[0x7fffffffda3d], b'\x7f')
        self.assertEqual(mem[0x7fffffffda3e], b'\x00')
        self.assertEqual(mem[0x7fffffffda3f], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345648)
        self.assertEqual(cpu.RIP, 140737351926577)
        self.assertEqual(cpu.RBP, 140737488345968)

    def test_PUSH_6(self):
        ''' Instruction PUSH_6
            Groups: mode64
            0x75c167:	push	0xf00aabb
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0075c000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffcca8] = '\xbb'
        mem[0x7fffffffcca9] = '\xaa'
        mem[0x7fffffffccaa] = '\x00'
        mem[0x7fffffffccab] = '\x0f'
        mem[0x7fffffffccac] = '\x00'
        mem[0x7fffffffccad] = '\x00'
        mem[0x7fffffffccae] = '\x00'
        mem[0x7fffffffccaf] = '\x00'
        mem[0x7fffffffccb0] = '\xfe'
        mem[0x7fffffffccb1] = '\xff'
        mem[0x7fffffffccb2] = '\xff'
        mem[0x7fffffffccb3] = '\xff'
        mem[0x7fffffffccb4] = '\x80'
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = 'x'
        mem[0x0075c167] = 'h'
        mem[0x0075c168] = '\xbb'
        mem[0x0075c169] = '\xaa'
        mem[0x0075c16a] = '\x00'
        mem[0x0075c16b] = '\x0f'
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x75c167
        cpu.RBP = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffcca8], b'\xbb')
        self.assertEqual(mem[0x7fffffffcca9], b'\xaa')
        self.assertEqual(mem[0x7fffffffccaa], b'\x00')
        self.assertEqual(mem[0x7fffffffccab], b'\x0f')
        self.assertEqual(mem[0x7fffffffccac], b'\x00')
        self.assertEqual(mem[0x7fffffffccad], b'\x00')
        self.assertEqual(mem[0x7fffffffccae], b'\x00')
        self.assertEqual(mem[0x7fffffffccaf], b'\x00')
        self.assertEqual(mem[0x7fffffffccb0], b'\xfe')
        self.assertEqual(mem[0x7fffffffccb1], b'\xff')
        self.assertEqual(mem[0x7fffffffccb2], b'\xff')
        self.assertEqual(mem[0x7fffffffccb3], b'\xff')
        self.assertEqual(mem[0x7fffffffccb4], b'\x80')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'x')
        self.assertEqual(mem[0x75c167], b'h')
        self.assertEqual(mem[0x75c168], b'\xbb')
        self.assertEqual(mem[0x75c169], b'\xaa')
        self.assertEqual(mem[0x75c16a], b'\x00')
        self.assertEqual(mem[0x75c16b], b'\x0f')
        self.assertEqual(cpu.RSP, 140737488342184)
        self.assertEqual(cpu.RIP, 7717228)
        self.assertEqual(cpu.RBP, 0)

    def test_PXOR_1(self):
        ''' Instruction PXOR_1
            Groups: sse2
            0x418490:	pxor	xmm8, xmm8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x00418490] = 'f'
        mem[0x00418491] = 'E'
        mem[0x00418492] = '\x0f'
        mem[0x00418493] = '\xef'
        mem[0x00418494] = '\xc0'
        cpu.XMM8 = 0x0
        cpu.RIP = 0x418490
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x418490], b'f')
        self.assertEqual(mem[0x418491], b'E')
        self.assertEqual(mem[0x418492], b'\x0f')
        self.assertEqual(mem[0x418493], b'\xef')
        self.assertEqual(mem[0x418494], b'\xc0')
        self.assertEqual(cpu.XMM8, 0)
        self.assertEqual(cpu.RIP, 4293781)

    def test_PXOR_2(self):
        ''' Instruction PXOR_2
            Groups: sse2
            0x41848f:	pxor	xmm11, xmm11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x00418490] = 'E'
        mem[0x00418491] = '\x0f'
        mem[0x00418492] = '\xef'
        mem[0x00418493] = '\xdb'
        mem[0x0041848f] = 'f'
        cpu.XMM11 = 0x0
        cpu.RIP = 0x41848f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x418490], b'E')
        self.assertEqual(mem[0x418491], b'\x0f')
        self.assertEqual(mem[0x418492], b'\xef')
        self.assertEqual(mem[0x418493], b'\xdb')
        self.assertEqual(mem[0x41848f], b'f')
        self.assertEqual(cpu.XMM11, 0)
        self.assertEqual(cpu.RIP, 4293780)

    def test_PXOR_3(self):
        ''' Instruction PXOR_3
            Groups: sse2
            0x4184bf:	pxor	xmm11, xmm11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004184c0] = 'E'
        mem[0x004184c1] = '\x0f'
        mem[0x004184c2] = '\xef'
        mem[0x004184c3] = '\xdb'
        mem[0x004184bf] = 'f'
        cpu.XMM11 = 0x0
        cpu.RIP = 0x4184bf
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4184c0], b'E')
        self.assertEqual(mem[0x4184c1], b'\x0f')
        self.assertEqual(mem[0x4184c2], b'\xef')
        self.assertEqual(mem[0x4184c3], b'\xdb')
        self.assertEqual(mem[0x4184bf], b'f')
        self.assertEqual(cpu.XMM11, 0)
        self.assertEqual(cpu.RIP, 4293828)

    def test_PXOR_4(self):
        ''' Instruction PXOR_4
            Groups: sse2
            0x418480:	pxor	xmm8, xmm8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x00418480] = 'f'
        mem[0x00418481] = 'E'
        mem[0x00418482] = '\x0f'
        mem[0x00418483] = '\xef'
        mem[0x00418484] = '\xc0'
        cpu.XMM8 = 0x0
        cpu.RIP = 0x418480
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x418480], b'f')
        self.assertEqual(mem[0x418481], b'E')
        self.assertEqual(mem[0x418482], b'\x0f')
        self.assertEqual(mem[0x418483], b'\xef')
        self.assertEqual(mem[0x418484], b'\xc0')
        self.assertEqual(cpu.XMM8, 0)
        self.assertEqual(cpu.RIP, 4293765)

    def test_PXOR_5(self):
        ''' Instruction PXOR_5
            Groups: sse2
            0x4183b5:	pxor	xmm9, xmm9
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x004183b8] = '\xef'
        mem[0x004183b9] = '\xc9'
        mem[0x004183b5] = 'f'
        mem[0x004183b6] = 'E'
        mem[0x004183b7] = '\x0f'
        cpu.XMM9 = 0x0
        cpu.RIP = 0x4183b5
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4183b8], b'\xef')
        self.assertEqual(mem[0x4183b9], b'\xc9')
        self.assertEqual(mem[0x4183b5], b'f')
        self.assertEqual(mem[0x4183b6], b'E')
        self.assertEqual(mem[0x4183b7], b'\x0f')
        self.assertEqual(cpu.XMM9, 0)
        self.assertEqual(cpu.RIP, 4293562)

    def test_PXOR_6(self):
        ''' Instruction PXOR_6
            Groups: sse2
            0x418495:	pxor	xmm9, xmm9
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x00418498] = '\xef'
        mem[0x00418499] = '\xc9'
        mem[0x00418495] = 'f'
        mem[0x00418496] = 'E'
        mem[0x00418497] = '\x0f'
        cpu.XMM9 = 0x0
        cpu.RIP = 0x418495
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x418498], b'\xef')
        self.assertEqual(mem[0x418499], b'\xc9')
        self.assertEqual(mem[0x418495], b'f')
        self.assertEqual(mem[0x418496], b'E')
        self.assertEqual(mem[0x418497], b'\x0f')
        self.assertEqual(cpu.XMM9, 0)
        self.assertEqual(cpu.RIP, 4293786)

    def test_RET_1(self):
        ''' Instruction RET_1
            Groups: ret, mode64
            0x7ffff7de3748:	ret
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd780] = ']'
        mem[0x7ffff7de3748] = '\xc3'
        mem[0x7fffffffd770] = 'p'
        mem[0x7fffffffd771] = '\xd8'
        mem[0x7fffffffd772] = '\xff'
        mem[0x7fffffffd773] = '\xff'
        mem[0x7fffffffd774] = '\xff'
        mem[0x7fffffffd775] = '\x7f'
        mem[0x7fffffffd776] = '\x00'
        mem[0x7fffffffd777] = '\x00'
        mem[0x7fffffffd778] = '\xab'
        mem[0x7fffffffd779] = '@'
        mem[0x7fffffffd77a] = '\xde'
        mem[0x7fffffffd77b] = '\xf7'
        mem[0x7fffffffd77c] = '\xff'
        mem[0x7fffffffd77d] = '\x7f'
        mem[0x7fffffffd77e] = '\x00'
        mem[0x7fffffffd77f] = '\x00'
        cpu.RSP = 0x7fffffffd778
        cpu.RIP = 0x7ffff7de3748
        cpu.RBP = 0x7fffffffd870
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd780], b']')
        self.assertEqual(mem[0x7ffff7de3748], b'\xc3')
        self.assertEqual(mem[0x7fffffffd770], b'p')
        self.assertEqual(mem[0x7fffffffd771], b'\xd8')
        self.assertEqual(mem[0x7fffffffd772], b'\xff')
        self.assertEqual(mem[0x7fffffffd773], b'\xff')
        self.assertEqual(mem[0x7fffffffd774], b'\xff')
        self.assertEqual(mem[0x7fffffffd775], b'\x7f')
        self.assertEqual(mem[0x7fffffffd776], b'\x00')
        self.assertEqual(mem[0x7fffffffd777], b'\x00')
        self.assertEqual(mem[0x7fffffffd778], b'\xab')
        self.assertEqual(mem[0x7fffffffd779], b'@')
        self.assertEqual(mem[0x7fffffffd77a], b'\xde')
        self.assertEqual(mem[0x7fffffffd77b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd77c], b'\xff')
        self.assertEqual(mem[0x7fffffffd77d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd77e], b'\x00')
        self.assertEqual(mem[0x7fffffffd77f], b'\x00')
        self.assertEqual(cpu.RSP, 140737488344960)
        self.assertEqual(cpu.RIP, 140737351925931)
        self.assertEqual(cpu.RBP, 140737488345200)

    def test_RET_2(self):
        ''' Instruction RET_2
            Groups: ret, mode64
            0x7ffff7df537f:	ret
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df5000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd840] = '\x00'
        mem[0x7ffff7df537f] = '\xc3'
        mem[0x7fffffffd830] = '\x03'
        mem[0x7fffffffd831] = '\x00'
        mem[0x7fffffffd832] = '\x00'
        mem[0x7fffffffd833] = '\x00'
        mem[0x7fffffffd834] = '\x00'
        mem[0x7fffffffd835] = '\x00'
        mem[0x7fffffffd836] = '\x00'
        mem[0x7fffffffd837] = '\x00'
        mem[0x7fffffffd838] = '\xdb'
        mem[0x7fffffffd839] = '\x7f'
        mem[0x7fffffffd83a] = '\xde'
        mem[0x7fffffffd83b] = '\xf7'
        mem[0x7fffffffd83c] = '\xff'
        mem[0x7fffffffd83d] = '\x7f'
        mem[0x7fffffffd83e] = '\x00'
        mem[0x7fffffffd83f] = '\x00'
        cpu.RSP = 0x7fffffffd838
        cpu.RIP = 0x7ffff7df537f
        cpu.RBP = 0x7fffffffdae0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd840], b'\x00')
        self.assertEqual(mem[0x7fffffffd83f], b'\x00')
        self.assertEqual(mem[0x7fffffffd830], b'\x03')
        self.assertEqual(mem[0x7fffffffd831], b'\x00')
        self.assertEqual(mem[0x7fffffffd832], b'\x00')
        self.assertEqual(mem[0x7fffffffd833], b'\x00')
        self.assertEqual(mem[0x7fffffffd834], b'\x00')
        self.assertEqual(mem[0x7fffffffd835], b'\x00')
        self.assertEqual(mem[0x7fffffffd836], b'\x00')
        self.assertEqual(mem[0x7fffffffd837], b'\x00')
        self.assertEqual(mem[0x7fffffffd838], b'\xdb')
        self.assertEqual(mem[0x7fffffffd839], b'\x7f')
        self.assertEqual(mem[0x7fffffffd83a], b'\xde')
        self.assertEqual(mem[0x7fffffffd83b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd83c], b'\xff')
        self.assertEqual(mem[0x7fffffffd83d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd83e], b'\x00')
        self.assertEqual(mem[0x7ffff7df537f], b'\xc3')
        self.assertEqual(cpu.RSP, 140737488345152)
        self.assertEqual(cpu.RIP, 140737351942107)
        self.assertEqual(cpu.RBP, 140737488345824)

    def test_RET_3(self):
        ''' Instruction RET_3
            Groups: ret, mode64
            0x406e67:	ret
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdb20] = 'p'
        mem[0x7fffffffdb21] = '\xdb'
        mem[0x7fffffffdb22] = '\xff'
        mem[0x7fffffffdb23] = '\xff'
        mem[0x7fffffffdb24] = '\xff'
        mem[0x7fffffffdb25] = '\x7f'
        mem[0x7fffffffdb26] = '\x00'
        mem[0x00406e67] = '\xc3'
        mem[0x7fffffffdb28] = 'N'
        mem[0x7fffffffdb29] = 'o'
        mem[0x7fffffffdb2a] = 'C'
        mem[0x7fffffffdb27] = '\x00'
        mem[0x7fffffffdb2c] = '\x00'
        mem[0x7fffffffdb2d] = '\x00'
        mem[0x7fffffffdb2e] = '\x00'
        mem[0x7fffffffdb2f] = '\x00'
        mem[0x7fffffffdb30] = '@'
        mem[0x7fffffffdb2b] = '\x00'
        cpu.RSP = 0x7fffffffdb28
        cpu.RIP = 0x406e67
        cpu.RBP = 0x7fffffffdb70
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdb20], b'p')
        self.assertEqual(mem[0x7fffffffdb21], b'\xdb')
        self.assertEqual(mem[0x7fffffffdb22], b'\xff')
        self.assertEqual(mem[0x7fffffffdb23], b'\xff')
        self.assertEqual(mem[0x7fffffffdb24], b'\xff')
        self.assertEqual(mem[0x7fffffffdb25], b'\x7f')
        self.assertEqual(mem[0x7fffffffdb26], b'\x00')
        self.assertEqual(mem[0x406e67], b'\xc3')
        self.assertEqual(mem[0x7fffffffdb28], b'N')
        self.assertEqual(mem[0x7fffffffdb29], b'o')
        self.assertEqual(mem[0x7fffffffdb2a], b'C')
        self.assertEqual(mem[0x7fffffffdb2b], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb2f], b'\x00')
        self.assertEqual(mem[0x7fffffffdb30], b'@')
        self.assertEqual(mem[0x7fffffffdb27], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345904)
        self.assertEqual(cpu.RIP, 4419406)
        self.assertEqual(cpu.RBP, 140737488345968)

    def test_RET_4(self):
        ''' Instruction RET_4
            Groups: ret, mode64
            0x7ffff7de2af3:	ret
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de2000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffd700] = ' '
        mem[0x7fffffffd701] = '\xd7'
        mem[0x7fffffffd702] = '\xff'
        mem[0x7fffffffd703] = '\xff'
        mem[0x7fffffffd704] = '\xff'
        mem[0x7fffffffd705] = '\x7f'
        mem[0x7fffffffd706] = '\x00'
        mem[0x7fffffffd707] = '\x00'
        mem[0x7fffffffd708] = ')'
        mem[0x7fffffffd709] = 'u'
        mem[0x7fffffffd70a] = '\xde'
        mem[0x7fffffffd70b] = '\xf7'
        mem[0x7fffffffd70c] = '\xff'
        mem[0x7fffffffd70d] = '\x7f'
        mem[0x7fffffffd70e] = '\x00'
        mem[0x7fffffffd70f] = '\x00'
        mem[0x7fffffffd710] = '\xb0'
        mem[0x7ffff7de2af3] = '\xc3'
        cpu.RSP = 0x7fffffffd708
        cpu.RIP = 0x7ffff7de2af3
        cpu.RBP = 0x7fffffffd720
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffd700], b' ')
        self.assertEqual(mem[0x7fffffffd701], b'\xd7')
        self.assertEqual(mem[0x7fffffffd702], b'\xff')
        self.assertEqual(mem[0x7fffffffd703], b'\xff')
        self.assertEqual(mem[0x7fffffffd704], b'\xff')
        self.assertEqual(mem[0x7fffffffd705], b'\x7f')
        self.assertEqual(mem[0x7fffffffd706], b'\x00')
        self.assertEqual(mem[0x7fffffffd707], b'\x00')
        self.assertEqual(mem[0x7fffffffd708], b')')
        self.assertEqual(mem[0x7fffffffd709], b'u')
        self.assertEqual(mem[0x7fffffffd70a], b'\xde')
        self.assertEqual(mem[0x7fffffffd70b], b'\xf7')
        self.assertEqual(mem[0x7fffffffd70c], b'\xff')
        self.assertEqual(mem[0x7fffffffd70d], b'\x7f')
        self.assertEqual(mem[0x7fffffffd70e], b'\x00')
        self.assertEqual(mem[0x7fffffffd70f], b'\x00')
        self.assertEqual(mem[0x7fffffffd710], b'\xb0')
        self.assertEqual(mem[0x7ffff7de2af3], b'\xc3')
        self.assertEqual(cpu.RSP, 140737488344848)
        self.assertEqual(cpu.RIP, 140737351939369)
        self.assertEqual(cpu.RBP, 140737488344864)

    def test_RET_5(self):
        ''' Instruction RET_5
            Groups: ret, mode64
            0x4118a1:	ret
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdae0] = '\x00'
        mem[0x004118a1] = '\xc3'
        mem[0x7fffffffdae2] = '\xff'
        mem[0x7fffffffdae3] = '\xff'
        mem[0x7fffffffdae4] = '\xff'
        mem[0x7fffffffdae5] = '\x7f'
        mem[0x7fffffffdae6] = '\x00'
        mem[0x7fffffffdae1] = '\xdb'
        mem[0x7fffffffdae8] = '\x1c'
        mem[0x7fffffffdae9] = '6'
        mem[0x7fffffffdaea] = 'A'
        mem[0x7fffffffdae7] = '\x00'
        mem[0x7fffffffdaec] = '\x00'
        mem[0x7fffffffdaed] = '\x00'
        mem[0x7fffffffdaee] = '\x00'
        mem[0x7fffffffdaef] = '\x00'
        mem[0x7fffffffdaf0] = '\x02'
        mem[0x7fffffffdaeb] = '\x00'
        cpu.RSP = 0x7fffffffdae8
        cpu.RIP = 0x4118a1
        cpu.RBP = 0x7fffffffdb00
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdae0], b'\x00')
        self.assertEqual(mem[0x7fffffffdae1], b'\xdb')
        self.assertEqual(mem[0x7fffffffdae2], b'\xff')
        self.assertEqual(mem[0x7fffffffdae3], b'\xff')
        self.assertEqual(mem[0x7fffffffdae4], b'\xff')
        self.assertEqual(mem[0x7fffffffdae5], b'\x7f')
        self.assertEqual(mem[0x7fffffffdae6], b'\x00')
        self.assertEqual(mem[0x4118a1], b'\xc3')
        self.assertEqual(mem[0x7fffffffdae8], b'\x1c')
        self.assertEqual(mem[0x7fffffffdae9], b'6')
        self.assertEqual(mem[0x7fffffffdaea], b'A')
        self.assertEqual(mem[0x7fffffffdae7], b'\x00')
        self.assertEqual(mem[0x7fffffffdaec], b'\x00')
        self.assertEqual(mem[0x7fffffffdaed], b'\x00')
        self.assertEqual(mem[0x7fffffffdaee], b'\x00')
        self.assertEqual(mem[0x7fffffffdaef], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf0], b'\x02')
        self.assertEqual(mem[0x7fffffffdaeb], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345840)
        self.assertEqual(cpu.RIP, 4273692)
        self.assertEqual(cpu.RBP, 140737488345856)

    def test_RET_6(self):
        ''' Instruction RET_6
            Groups: ret, mode64
            0x40fc8d:	ret
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040f000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffda00] = '\x06'
        mem[0x0040fc8d] = '\xc3'
        mem[0x7fffffffd9f0] = '\xb0'
        mem[0x7fffffffd9f1] = '\xda'
        mem[0x7fffffffd9f2] = '\xff'
        mem[0x7fffffffd9f3] = '\xff'
        mem[0x7fffffffd9f4] = '\xff'
        mem[0x7fffffffd9f5] = '\x7f'
        mem[0x7fffffffd9f6] = '\x00'
        mem[0x7fffffffd9f7] = '\x00'
        mem[0x7fffffffd9f8] = '\xee'
        mem[0x7fffffffd9f9] = '}'
        mem[0x7fffffffd9fa] = 'E'
        mem[0x7fffffffd9fb] = '\x00'
        mem[0x7fffffffd9fc] = '\x00'
        mem[0x7fffffffd9fd] = '\x00'
        mem[0x7fffffffd9fe] = '\x00'
        mem[0x7fffffffd9ff] = '\x00'
        cpu.RSP = 0x7fffffffd9f8
        cpu.RIP = 0x40fc8d
        cpu.RBP = 0x7fffffffdab0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda00], b'\x06')
        self.assertEqual(mem[0x40fc8d], b'\xc3')
        self.assertEqual(mem[0x7fffffffd9f0], b'\xb0')
        self.assertEqual(mem[0x7fffffffd9f1], b'\xda')
        self.assertEqual(mem[0x7fffffffd9f2], b'\xff')
        self.assertEqual(mem[0x7fffffffd9f3], b'\xff')
        self.assertEqual(mem[0x7fffffffd9f4], b'\xff')
        self.assertEqual(mem[0x7fffffffd9f5], b'\x7f')
        self.assertEqual(mem[0x7fffffffd9f6], b'\x00')
        self.assertEqual(mem[0x7fffffffd9f7], b'\x00')
        self.assertEqual(mem[0x7fffffffd9f8], b'\xee')
        self.assertEqual(mem[0x7fffffffd9f9], b'}')
        self.assertEqual(mem[0x7fffffffd9fa], b'E')
        self.assertEqual(mem[0x7fffffffd9fb], b'\x00')
        self.assertEqual(mem[0x7fffffffd9fc], b'\x00')
        self.assertEqual(mem[0x7fffffffd9fd], b'\x00')
        self.assertEqual(mem[0x7fffffffd9fe], b'\x00')
        self.assertEqual(mem[0x7fffffffd9ff], b'\x00')
        self.assertEqual(cpu.RSP, 140737488345600)
        self.assertEqual(cpu.RIP, 4554222)
        self.assertEqual(cpu.RBP, 140737488345776)

    def test_ROL_1(self):
        ''' Instruction ROL_1
            Groups:
            0x44272a:	rol	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00442000, 0x1000, 'rwx')
        mem[0x0044272a] = 'H'
        mem[0x0044272b] = '\xc1'
        mem[0x0044272c] = '\xc0'
        mem[0x0044272d] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x44272a
        cpu.CF = False
        cpu.RAX = 0x69fd1b8f25bea73
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x44272a], b'H')
        self.assertEqual(mem[0x44272b], b'\xc1')
        self.assertEqual(mem[0x44272c], b'\xc0')
        self.assertEqual(mem[0x44272d], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 11777445978752552255)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4466478)

    def test_ROL_2(self):
        ''' Instruction ROL_2
            Groups:
            0x7ffff7df408d:	rol	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df4090] = '\x11'
        mem[0x7ffff7df408d] = 'H'
        mem[0x7ffff7df408e] = '\xc1'
        mem[0x7ffff7df408f] = '\xc0'
        cpu.OF = False
        cpu.RIP = 0x7ffff7df408d
        cpu.CF = False
        cpu.RAX = 0x7fffffffd9b0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df4090], b'\x11')
        self.assertEqual(mem[0x7ffff7df408d], b'H')
        self.assertEqual(mem[0x7ffff7df408e], b'\xc1')
        self.assertEqual(mem[0x7ffff7df408f], b'\xc0')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 18446744072423997440)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351991441)

    def test_ROL_3(self):
        ''' Instruction ROL_3
            Groups:
            0x409c7a:	rol	rdi, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00409000, 0x1000, 'rwx')
        mem[0x00409c7a] = 'H'
        mem[0x00409c7b] = '\xc1'
        mem[0x00409c7c] = '\xc7'
        mem[0x00409c7d] = '\x11'
        cpu.OF = False
        cpu.RDI = 0x4fb19f79d00a9c7e
        cpu.CF = False
        cpu.RIP = 0x409c7a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x409c7a], b'H')
        self.assertEqual(mem[0x409c7b], b'\xc1')
        self.assertEqual(mem[0x409c7c], b'\xc7')
        self.assertEqual(mem[0x409c7d], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RDI, 4536145262703058787)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4234366)

    def test_ROL_4(self):
        ''' Instruction ROL_4
            Groups:
            0x40725a:	rol	rdi, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00407000, 0x1000, 'rwx')
        mem[0x0040725a] = 'H'
        mem[0x0040725b] = '\xc1'
        mem[0x0040725c] = '\xc7'
        mem[0x0040725d] = '\x11'
        cpu.OF = False
        cpu.RDI = 0x1d13aa75a9fb0505
        cpu.CF = False
        cpu.RIP = 0x40725a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40725a], b'H')
        self.assertEqual(mem[0x40725b], b'\xc1')
        self.assertEqual(mem[0x40725c], b'\xc7')
        self.assertEqual(mem[0x40725d], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RDI, 6119076834908453415)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4223582)

    def test_ROL_5(self):
        ''' Instruction ROL_5
            Groups:
            0x4452b5:	rol	rdx, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00445000, 0x1000, 'rwx')
        mem[0x004452b8] = '\x11'
        mem[0x004452b5] = 'H'
        mem[0x004452b6] = '\xc1'
        mem[0x004452b7] = '\xc2'
        cpu.OF = False
        cpu.CF = False
        cpu.RIP = 0x4452b5
        cpu.RDX = 0x4fb1e0862fb57b2e
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4452b8], b'\x11')
        self.assertEqual(mem[0x4452b5], b'H')
        self.assertEqual(mem[0x4452b6], b'\xc1')
        self.assertEqual(mem[0x4452b7], b'\xc2')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4477625)
        self.assertEqual(cpu.RDX, 13910598262045056867)

    def test_ROL_6(self):
        ''' Instruction ROL_6
            Groups:
            0x7ffff7a6220a:	rol	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a62000, 0x1000, 'rwx')
        mem[0x7ffff7a6220a] = 'H'
        mem[0x7ffff7a6220b] = '\xc1'
        mem[0x7ffff7a6220c] = '\xc0'
        mem[0x7ffff7a6220d] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x7ffff7a6220a
        cpu.CF = False
        cpu.RAX = 0x4d168f8071dccc80
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a6220a], b'H')
        self.assertEqual(mem[0x7ffff7a6220b], b'\xc1')
        self.assertEqual(mem[0x7ffff7a6220c], b'\xc0')
        self.assertEqual(mem[0x7ffff7a6220d], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 2234035801451174445)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737348248078)

    def test_ROR_1(self):
        ''' Instruction ROR_1
            Groups:
            0x406f53:	ror	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem[0x00406f53] = 'H'
        mem[0x00406f54] = '\xc1'
        mem[0x00406f55] = '\xc8'
        mem[0x00406f56] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x406f53
        cpu.CF = False
        cpu.RAX = 0x9287e74ad78292fc
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x406f53], b'H')
        self.assertEqual(mem[0x406f54], b'\xc1')
        self.assertEqual(mem[0x406f55], b'\xc8')
        self.assertEqual(mem[0x406f56], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 5295750768033622977)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4222807)

    def test_ROR_2(self):
        ''' Instruction ROR_2
            Groups:
            0x7ffff7a65253:	ror	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a65000, 0x1000, 'rwx')
        mem[0x7ffff7a65253] = 'H'
        mem[0x7ffff7a65254] = '\xc1'
        mem[0x7ffff7a65255] = '\xc8'
        mem[0x7ffff7a65256] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x7ffff7a65253
        cpu.CF = False
        cpu.RAX = 0x42002153efdd741e
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a65253], b'H')
        self.assertEqual(mem[0x7ffff7a65254], b'\xc1')
        self.assertEqual(mem[0x7ffff7a65255], b'\xc8')
        self.assertEqual(mem[0x7ffff7a65256], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 13406970899868547054)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737348260439)

    def test_ROR_3(self):
        ''' Instruction ROR_3
            Groups:
            0x406fd3:	ror	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem[0x00406fd3] = 'H'
        mem[0x00406fd4] = '\xc1'
        mem[0x00406fd5] = '\xc8'
        mem[0x00406fd6] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x406fd3
        cpu.CF = False
        cpu.RAX = 0x4a02228a32751a47
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x406fd3], b'H')
        self.assertEqual(mem[0x406fd4], b'\xc1')
        self.assertEqual(mem[0x406fd5], b'\xc8')
        self.assertEqual(mem[0x406fd6], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 10170153807536003386)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4222935)

    def test_ROR_4(self):
        ''' Instruction ROR_4
            Groups:
            0x7ffff7a65253:	ror	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a65000, 0x1000, 'rwx')
        mem[0x7ffff7a65253] = 'H'
        mem[0x7ffff7a65254] = '\xc1'
        mem[0x7ffff7a65255] = '\xc8'
        mem[0x7ffff7a65256] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x7ffff7a65253
        cpu.CF = False
        cpu.RAX = 0x1b65e4b049796683
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a65253], b'H')
        self.assertEqual(mem[0x7ffff7a65254], b'\xc1')
        self.assertEqual(mem[0x7ffff7a65255], b'\xc8')
        self.assertEqual(mem[0x7ffff7a65256], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 12916761005984851132)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737348260439)

    def test_ROR_5(self):
        ''' Instruction ROR_5
            Groups:
            0x406f53:	ror	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem[0x00406f53] = 'H'
        mem[0x00406f54] = '\xc1'
        mem[0x00406f55] = '\xc8'
        mem[0x00406f56] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x406f53
        cpu.CF = False
        cpu.RAX = 0x54eb53f60a0a3a27
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x406f53], b'H')
        self.assertEqual(mem[0x406f54], b'\xc1')
        self.assertEqual(mem[0x406f55], b'\xc8')
        self.assertEqual(mem[0x406f56], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 2095205673997108485)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4222807)

    def test_ROR_6(self):
        ''' Instruction ROR_6
            Groups:
            0x406fc3:	ror	rax, 0x11
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem[0x00406fc3] = 'H'
        mem[0x00406fc4] = '\xc1'
        mem[0x00406fc5] = '\xc8'
        mem[0x00406fc6] = '\x11'
        cpu.OF = False
        cpu.RIP = 0x406fc3
        cpu.CF = False
        cpu.RAX = 0xf69983477b463caa
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x406fc3], b'H')
        self.assertEqual(mem[0x406fc4], b'\xc1')
        self.assertEqual(mem[0x406fc5], b'\xc8')
        self.assertEqual(mem[0x406fc6], b'\x11')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.RAX, 2185788763754708387)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4222919)

    def test_SAR_1(self):
        ''' Instruction SAR_1
            Groups:
            0x7ffff7de4085:	sar	rax, 2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4088] = '\x02'
        mem[0x7ffff7de4085] = 'H'
        mem[0x7ffff7de4086] = '\xc1'
        mem[0x7ffff7de4087] = '\xf8'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4085
        cpu.PF = False
        cpu.SF = False
        cpu.RAX = 0x15c8
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4088], b'\x02')
        self.assertEqual(mem[0x7ffff7de4085], b'H')
        self.assertEqual(mem[0x7ffff7de4086], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4087], b'\xf8')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925897)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.RAX, 1394)

    def test_SAR_2(self):
        ''' Instruction SAR_2
            Groups:
            0x7ffff7acfc78:	sar	r8d, 0x1f
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7acf000, 0x1000, 'rwx')
        mem[0x7ffff7acfc78] = 'A'
        mem[0x7ffff7acfc79] = '\xc1'
        mem[0x7ffff7acfc7a] = '\xf8'
        mem[0x7ffff7acfc7b] = '\x1f'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7acfc78
        cpu.R8D = 0x9
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7acfc78], b'A')
        self.assertEqual(mem[0x7ffff7acfc79], b'\xc1')
        self.assertEqual(mem[0x7ffff7acfc7a], b'\xf8')
        self.assertEqual(mem[0x7ffff7acfc7b], b'\x1f')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737348697212)
        self.assertEqual(cpu.R8D, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_SAR_3(self):
        ''' Instruction SAR_3
            Groups:
            0x7ffff7de4085:	sar	rax, 2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4088] = '\x02'
        mem[0x7ffff7de4085] = 'H'
        mem[0x7ffff7de4086] = '\xc1'
        mem[0x7ffff7de4087] = '\xf8'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4085
        cpu.PF = True
        cpu.SF = False
        cpu.RAX = 0x1290
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4088], b'\x02')
        self.assertEqual(mem[0x7ffff7de4085], b'H')
        self.assertEqual(mem[0x7ffff7de4086], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4087], b'\xf8')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925897)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.RAX, 1188)

    def test_SAR_4(self):
        ''' Instruction SAR_4
            Groups:
            0x7ffff7de4085:	sar	rax, 2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4088] = '\x02'
        mem[0x7ffff7de4085] = 'H'
        mem[0x7ffff7de4086] = '\xc1'
        mem[0x7ffff7de4087] = '\xf8'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4085
        cpu.PF = False
        cpu.SF = False
        cpu.RAX = 0x1450
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4088], b'\x02')
        self.assertEqual(mem[0x7ffff7de4085], b'H')
        self.assertEqual(mem[0x7ffff7de4086], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4087], b'\xf8')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925897)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.RAX, 1300)

    def test_SAR_5(self):
        ''' Instruction SAR_5
            Groups:
            0x7ffff7de4085:	sar	rax, 2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4088] = '\x02'
        mem[0x7ffff7de4085] = 'H'
        mem[0x7ffff7de4086] = '\xc1'
        mem[0x7ffff7de4087] = '\xf8'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4085
        cpu.PF = False
        cpu.SF = False
        cpu.RAX = 0x1420
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4088], b'\x02')
        self.assertEqual(mem[0x7ffff7de4085], b'H')
        self.assertEqual(mem[0x7ffff7de4086], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4087], b'\xf8')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925897)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.RAX, 1288)

    def test_SAR_6(self):
        ''' Instruction SAR_6
            Groups:
            0x7ffff7de4085:	sar	rax, 2
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4088] = '\x02'
        mem[0x7ffff7de4085] = 'H'
        mem[0x7ffff7de4086] = '\xc1'
        mem[0x7ffff7de4087] = '\xf8'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de4085
        cpu.PF = False
        cpu.SF = False
        cpu.RAX = 0x1070
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4088], b'\x02')
        self.assertEqual(mem[0x7ffff7de4085], b'H')
        self.assertEqual(mem[0x7ffff7de4086], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4087], b'\xf8')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925897)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.RAX, 1052)

    def test_SCASB_1(self):
        ''' Instruction SCASB_1
            Groups:
            0x7ffff7a78233:	repne scasb	al, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ba1000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffa000, 0x1000, 'rwx')
        mem[0x7ffff7a78234] = '\xae'
        mem[0x7fffffffa9c8] = 'F'
        mem[0x7fffffffa9c9] = '{'
        mem[0x7fffffffa9ca] = '\xaa'
        mem[0x7fffffffa9cb] = '\xf7'
        mem[0x7fffffffa9cc] = '\xff'
        mem[0x7fffffffa9cd] = '\x7f'
        mem[0x7fffffffa9ce] = '\x00'
        mem[0x7fffffffa9cf] = '\x00'
        mem[0x7ffff7a78233] = '\xf2'
        mem[0x7ffff7ba14b4] = 't'
        mem[0x7ffff7ba14b5] = 'o'
        mem[0x7ffff7ba14b6] = 'r'
        mem[0x7ffff7ba14b7] = 'y'
        mem[0x7ffff7ba14b8] = '\x00'
        mem[0x7ffff7ba14b9] = 'N'
        mem[0x7ffff7ba14ba] = 'o'
        mem[0x7ffff7ba14bb] = ' '
        cpu.RDI = 0x7ffff7ba14b4
        cpu.RCX = 0xffffffffffffffea
        cpu.RSI = 0x7fffffffa9c8
        cpu.RIP = 0x7ffff7a78233
        cpu.AL = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ba14b9], b'N')
        self.assertEqual(mem[0x7fffffffa9c8], b'F')
        self.assertEqual(mem[0x7fffffffa9c9], b'{')
        self.assertEqual(mem[0x7fffffffa9ca], b'\xaa')
        self.assertEqual(mem[0x7fffffffa9cb], b'\xf7')
        self.assertEqual(mem[0x7fffffffa9cc], b'\xff')
        self.assertEqual(mem[0x7fffffffa9cd], b'\x7f')
        self.assertEqual(mem[0x7fffffffa9ce], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cf], b'\x00')
        self.assertEqual(mem[0x7ffff7a78233], b'\xf2')
        self.assertEqual(mem[0x7ffff7a78234], b'\xae')
        self.assertEqual(mem[0x7ffff7ba14b5], b'o')
        self.assertEqual(mem[0x7ffff7ba14b6], b'r')
        self.assertEqual(mem[0x7ffff7ba14b7], b'y')
        self.assertEqual(mem[0x7ffff7ba14b8], b'\x00')
        self.assertEqual(mem[0x7ffff7ba14b4], b't')
        self.assertEqual(mem[0x7ffff7ba14ba], b'o')
        self.assertEqual(mem[0x7ffff7ba14bb], b' ')
        self.assertEqual(cpu.RCX, 18446744073709551593)
        self.assertEqual(cpu.RDI, 140737349555381)
        self.assertEqual(cpu.RSI, 140737488333256)
        self.assertEqual(cpu.RIP, 140737348338227)
        self.assertEqual(cpu.AL, 0)

    def test_SCASB_2(self):
        ''' Instruction SCASB_2
            Groups:
            0x7ffff7a78233:	repne scasb	al, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ba1000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffa000, 0x1000, 'rwx')
        mem[0x7ffff7ba14a1] = ' '
        mem[0x7ffff7ba14a2] = 's'
        mem[0x7ffff7ba14a3] = 'u'
        mem[0x7ffff7ba14a4] = 'c'
        mem[0x7ffff7ba14a5] = 'h'
        mem[0x7ffff7ba14a6] = ' '
        mem[0x7ffff7ba14a7] = 'f'
        mem[0x7ffff7ba14a8] = 'i'
        mem[0x7fffffffa9c9] = '\x00'
        mem[0x7fffffffa9ca] = '\x00'
        mem[0x7fffffffa9cb] = '\x00'
        mem[0x7fffffffa9cc] = '\x00'
        mem[0x7fffffffa9cd] = '\x00'
        mem[0x7fffffffa9ce] = '\x00'
        mem[0x7fffffffa9cf] = '\x00'
        mem[0x7fffffffa9c8] = '\x00'
        mem[0x7ffff7a78233] = '\xf2'
        mem[0x7ffff7a78234] = '\xae'
        cpu.RDI = 0x7ffff7ba14a1
        cpu.RCX = 0xfffffffffffffffd
        cpu.RSI = 0x7fffffffa9c8
        cpu.RIP = 0x7ffff7a78233
        cpu.AL = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ba14a1], b' ')
        self.assertEqual(mem[0x7ffff7ba14a2], b's')
        self.assertEqual(mem[0x7ffff7ba14a3], b'u')
        self.assertEqual(mem[0x7ffff7ba14a4], b'c')
        self.assertEqual(mem[0x7ffff7ba14a5], b'h')
        self.assertEqual(mem[0x7ffff7ba14a6], b' ')
        self.assertEqual(mem[0x7ffff7ba14a7], b'f')
        self.assertEqual(mem[0x7fffffffa9c8], b'\x00')
        self.assertEqual(mem[0x7fffffffa9c9], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ca], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cb], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cc], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cd], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ce], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cf], b'\x00')
        self.assertEqual(mem[0x7ffff7ba14a8], b'i')
        self.assertEqual(mem[0x7ffff7a78233], b'\xf2')
        self.assertEqual(mem[0x7ffff7a78234], b'\xae')
        self.assertEqual(cpu.RCX, 18446744073709551612)
        self.assertEqual(cpu.RDI, 140737349555362)
        self.assertEqual(cpu.RSI, 140737488333256)
        self.assertEqual(cpu.RIP, 140737348338227)
        self.assertEqual(cpu.AL, 0)

    def test_SCASB_3(self):
        ''' Instruction SCASB_3
            Groups:
            0x7ffff7a78233:	repne scasb	al, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ba1000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffa000, 0x1000, 'rwx')
        mem[0x7ffff7a78234] = '\xae'
        mem[0x7fffffffa9c8] = '\x00'
        mem[0x7fffffffa9c9] = '\x00'
        mem[0x7fffffffa9ca] = '\x00'
        mem[0x7fffffffa9cb] = '\x00'
        mem[0x7fffffffa9cc] = '\x00'
        mem[0x7fffffffa9cd] = '\x00'
        mem[0x7fffffffa9ce] = '\x00'
        mem[0x7fffffffa9cf] = '\x00'
        mem[0x7ffff7a78233] = '\xf2'
        mem[0x7ffff7ba14b2] = 'e'
        mem[0x7ffff7ba14b3] = 'c'
        mem[0x7ffff7ba14b4] = 't'
        mem[0x7ffff7ba14b5] = 'o'
        mem[0x7ffff7ba14b6] = 'r'
        mem[0x7ffff7ba14b7] = 'y'
        mem[0x7ffff7ba14b8] = '\x00'
        mem[0x7ffff7ba14b9] = 'N'
        cpu.RDI = 0x7ffff7ba14b2
        cpu.RCX = 0xffffffffffffffec
        cpu.RSI = 0x7fffffffa9c8
        cpu.RIP = 0x7ffff7a78233
        cpu.AL = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ba14b9], b'N')
        self.assertEqual(mem[0x7ffff7ba14b3], b'c')
        self.assertEqual(mem[0x7fffffffa9c8], b'\x00')
        self.assertEqual(mem[0x7fffffffa9c9], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ca], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cb], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cc], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cd], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ce], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cf], b'\x00')
        self.assertEqual(mem[0x7ffff7ba14b2], b'e')
        self.assertEqual(mem[0x7ffff7a78233], b'\xf2')
        self.assertEqual(mem[0x7ffff7a78234], b'\xae')
        self.assertEqual(mem[0x7ffff7ba14b5], b'o')
        self.assertEqual(mem[0x7ffff7ba14b6], b'r')
        self.assertEqual(mem[0x7ffff7ba14b7], b'y')
        self.assertEqual(mem[0x7ffff7ba14b8], b'\x00')
        self.assertEqual(mem[0x7ffff7ba14b4], b't')
        self.assertEqual(cpu.RCX, 18446744073709551595)
        self.assertEqual(cpu.RDI, 140737349555379)
        self.assertEqual(cpu.RSI, 140737488333256)
        self.assertEqual(cpu.RIP, 140737348338227)
        self.assertEqual(cpu.AL, 0)

    def test_SCASB_4(self):
        ''' Instruction SCASB_4
            Groups:
            0x7ffff7a78233:	repne scasb	al, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        mem[0x7fffffffe0a5] = 'g'
        mem[0x7fffffffe0a6] = 'z'
        mem[0x7fffffffe0a7] = 'i'
        mem[0x7fffffffe0a8] = 'p'
        mem[0x7fffffffe0a9] = '\x00'
        mem[0x7fffffffe0aa] = 'a'
        mem[0x7fffffffe0ab] = 'r'
        mem[0x7fffffffe0ac] = 'g'
        mem[0x7ffff7a78233] = '\xf2'
        mem[0x7ffff7a78234] = '\xae'
        mem[0x7fffffffc2f8] = '\x1f'
        mem[0x7fffffffc2f9] = '\xd5'
        mem[0x7fffffffc2fa] = '\xff'
        mem[0x7fffffffc2fb] = '\xff'
        mem[0x7fffffffc2fc] = '\xff'
        mem[0x7fffffffc2fd] = '\x7f'
        mem[0x7fffffffc2fe] = '\x00'
        mem[0x7fffffffc2ff] = '\x00'
        cpu.RDI = 0x7fffffffe0a5
        cpu.RCX = 0xffffffffffffffff
        cpu.RSI = 0x7fffffffc2f8
        cpu.RIP = 0x7ffff7a78233
        cpu.AL = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffe0a5], b'g')
        self.assertEqual(mem[0x7fffffffe0a6], b'z')
        self.assertEqual(mem[0x7fffffffe0a7], b'i')
        self.assertEqual(mem[0x7fffffffe0a8], b'p')
        self.assertEqual(mem[0x7fffffffe0a9], b'\x00')
        self.assertEqual(mem[0x7fffffffe0aa], b'a')
        self.assertEqual(mem[0x7fffffffe0ab], b'r')
        self.assertEqual(mem[0x7fffffffe0ac], b'g')
        self.assertEqual(mem[0x7ffff7a78233], b'\xf2')
        self.assertEqual(mem[0x7ffff7a78234], b'\xae')
        self.assertEqual(mem[0x7fffffffc2f8], b'\x1f')
        self.assertEqual(mem[0x7fffffffc2f9], b'\xd5')
        self.assertEqual(mem[0x7fffffffc2fa], b'\xff')
        self.assertEqual(mem[0x7fffffffc2fb], b'\xff')
        self.assertEqual(mem[0x7fffffffc2fc], b'\xff')
        self.assertEqual(mem[0x7fffffffc2fd], b'\x7f')
        self.assertEqual(mem[0x7fffffffc2fe], b'\x00')
        self.assertEqual(mem[0x7fffffffc2ff], b'\x00')
        self.assertEqual(cpu.RCX, 18446744073709551614)
        self.assertEqual(cpu.RDI, 140737488347302)
        self.assertEqual(cpu.RSI, 140737488339704)
        self.assertEqual(cpu.RIP, 140737348338227)
        self.assertEqual(cpu.AL, 0)

    def test_SCASB_5(self):
        ''' Instruction SCASB_5
            Groups:
            0x7ffff7a78233:	repne scasb	al, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ba1000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffa000, 0x1000, 'rwx')
        mem[0x7ffff7ba14ab] = ' '
        mem[0x7ffff7ba14a5] = 'h'
        mem[0x7ffff7ba14a6] = ' '
        mem[0x7ffff7ba14a7] = 'f'
        mem[0x7ffff7ba14a8] = 'i'
        mem[0x7ffff7ba14a9] = 'l'
        mem[0x7ffff7ba14aa] = 'e'
        mem[0x7fffffffa9cb] = '\x00'
        mem[0x7ffff7ba14ac] = 'o'
        mem[0x7fffffffa9cd] = '\x00'
        mem[0x7fffffffa9ce] = '\x00'
        mem[0x7fffffffa9cf] = '\x00'
        mem[0x7fffffffa9c8] = '\x00'
        mem[0x7ffff7a78233] = '\xf2'
        mem[0x7ffff7a78234] = '\xae'
        mem[0x7fffffffa9c9] = '\x00'
        mem[0x7fffffffa9cc] = '\x00'
        mem[0x7fffffffa9ca] = '\x00'
        cpu.RDI = 0x7ffff7ba14a5
        cpu.RCX = 0xfffffffffffffff9
        cpu.RSI = 0x7fffffffa9c8
        cpu.RIP = 0x7ffff7a78233
        cpu.AL = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ba14ab], b' ')
        self.assertEqual(mem[0x7ffff7ba14a5], b'h')
        self.assertEqual(mem[0x7ffff7ba14a6], b' ')
        self.assertEqual(mem[0x7ffff7ba14a7], b'f')
        self.assertEqual(mem[0x7fffffffa9c8], b'\x00')
        self.assertEqual(mem[0x7fffffffa9c9], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ca], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cb], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cc], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cd], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ce], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cf], b'\x00')
        self.assertEqual(mem[0x7ffff7ba14a8], b'i')
        self.assertEqual(mem[0x7ffff7ba14ac], b'o')
        self.assertEqual(mem[0x7ffff7a78234], b'\xae')
        self.assertEqual(mem[0x7ffff7a78233], b'\xf2')
        self.assertEqual(mem[0x7ffff7ba14a9], b'l')
        self.assertEqual(mem[0x7ffff7ba14aa], b'e')
        self.assertEqual(cpu.RCX, 18446744073709551608)
        self.assertEqual(cpu.RDI, 140737349555366)
        self.assertEqual(cpu.RSI, 140737488333256)
        self.assertEqual(cpu.RIP, 140737348338227)
        self.assertEqual(cpu.AL, 0)

    def test_SCASB_6(self):
        ''' Instruction SCASB_6
            Groups:
            0x7ffff7a78233:	repne scasb	al, byte ptr [rdi]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555771000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffa000, 0x1000, 'rwx')
        mem[0x555555771dc0] = 'a'
        mem[0x555555771dc1] = 'r'
        mem[0x555555771dc2] = 'g'
        mem[0x555555771dc3] = '1'
        mem[0x555555771dc4] = '\x00'
        mem[0x555555771dc5] = '\x00'
        mem[0x555555771dc6] = '\x00'
        mem[0x555555771dc7] = '\x00'
        mem[0x7fffffffa9c8] = '\x00'
        mem[0x7fffffffa9c9] = '\x00'
        mem[0x7fffffffa9ca] = '\x00'
        mem[0x7fffffffa9cb] = '\x00'
        mem[0x7fffffffa9cc] = '\x00'
        mem[0x7fffffffa9cd] = '\x00'
        mem[0x7fffffffa9ce] = '\x00'
        mem[0x7fffffffa9cf] = '\x00'
        mem[0x7ffff7a78233] = '\xf2'
        mem[0x7ffff7a78234] = '\xae'
        cpu.RDI = 0x555555771dc0
        cpu.RCX = 0xffffffffffffffff
        cpu.RSI = 0x7fffffffa9c8
        cpu.RIP = 0x7ffff7a78233
        cpu.AL = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555771dc0], b'a')
        self.assertEqual(mem[0x555555771dc1], b'r')
        self.assertEqual(mem[0x555555771dc2], b'g')
        self.assertEqual(mem[0x555555771dc3], b'1')
        self.assertEqual(mem[0x555555771dc4], b'\x00')
        self.assertEqual(mem[0x555555771dc5], b'\x00')
        self.assertEqual(mem[0x555555771dc6], b'\x00')
        self.assertEqual(mem[0x555555771dc7], b'\x00')
        self.assertEqual(mem[0x7fffffffa9c8], b'\x00')
        self.assertEqual(mem[0x7fffffffa9c9], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ca], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cb], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cc], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cd], b'\x00')
        self.assertEqual(mem[0x7fffffffa9ce], b'\x00')
        self.assertEqual(mem[0x7fffffffa9cf], b'\x00')
        self.assertEqual(mem[0x7ffff7a78233], b'\xf2')
        self.assertEqual(mem[0x7ffff7a78234], b'\xae')
        self.assertEqual(cpu.RCX, 18446744073709551614)
        self.assertEqual(cpu.RDI, 93824994450881)
        self.assertEqual(cpu.RSI, 140737488333256)
        self.assertEqual(cpu.RIP, 140737348338227)
        self.assertEqual(cpu.AL, 0)

    def test_SETA_1(self):
        ''' Instruction SETA_1
            Groups:
            0x5555555548c2:	seta	dl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem[0x5555555548c2] = '\x0f'
        mem[0x5555555548c3] = '\x97'
        mem[0x5555555548c4] = '\xc2'
        cpu.DL = 0x0
        cpu.ZF = False
        cpu.RIP = 0x5555555548c2
        cpu.CF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5555555548c2], b'\x0f')
        self.assertEqual(mem[0x5555555548c3], b'\x97')
        self.assertEqual(mem[0x5555555548c4], b'\xc2')
        self.assertEqual(cpu.DL, 1)
        self.assertEqual(cpu.RIP, 93824992233669)

    def test_SETBE_1(self):
        ''' Instruction SETBE_1
            Groups:
            0x7ffff7de6207:	setbe	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6208] = '\x0f'
        mem[0x7ffff7de6209] = '\x96'
        mem[0x7ffff7de620a] = '\xc1'
        mem[0x7ffff7de6207] = 'A'
        cpu.ZF = False
        cpu.R9B = 0x58
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6207
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6208], b'\x0f')
        self.assertEqual(mem[0x7ffff7de6209], b'\x96')
        self.assertEqual(mem[0x7ffff7de620a], b'\xc1')
        self.assertEqual(mem[0x7ffff7de6207], b'A')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 140737351934475)

    def test_SETBE_2(self):
        ''' Instruction SETBE_2
            Groups:
            0x7ffff7de6207:	setbe	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6208] = '\x0f'
        mem[0x7ffff7de6209] = '\x96'
        mem[0x7ffff7de620a] = '\xc1'
        mem[0x7ffff7de6207] = 'A'
        cpu.ZF = False
        cpu.R9B = 0x58
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6207
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6208], b'\x0f')
        self.assertEqual(mem[0x7ffff7de6209], b'\x96')
        self.assertEqual(mem[0x7ffff7de620a], b'\xc1')
        self.assertEqual(mem[0x7ffff7de6207], b'A')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 140737351934475)

    def test_SETBE_3(self):
        ''' Instruction SETBE_3
            Groups:
            0x7ffff7de6207:	setbe	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6208] = '\x0f'
        mem[0x7ffff7de6209] = '\x96'
        mem[0x7ffff7de620a] = '\xc1'
        mem[0x7ffff7de6207] = 'A'
        cpu.ZF = False
        cpu.R9B = 0x58
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6207
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6208], b'\x0f')
        self.assertEqual(mem[0x7ffff7de6209], b'\x96')
        self.assertEqual(mem[0x7ffff7de620a], b'\xc1')
        self.assertEqual(mem[0x7ffff7de6207], b'A')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 140737351934475)

    def test_SETBE_4(self):
        ''' Instruction SETBE_4
            Groups:
            0x7ffff7de6207:	setbe	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6208] = '\x0f'
        mem[0x7ffff7de6209] = '\x96'
        mem[0x7ffff7de620a] = '\xc1'
        mem[0x7ffff7de6207] = 'A'
        cpu.ZF = False
        cpu.R9B = 0x58
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6207
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6208], b'\x0f')
        self.assertEqual(mem[0x7ffff7de6209], b'\x96')
        self.assertEqual(mem[0x7ffff7de620a], b'\xc1')
        self.assertEqual(mem[0x7ffff7de6207], b'A')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 140737351934475)

    def test_SETBE_5(self):
        ''' Instruction SETBE_5
            Groups:
            0x7ffff7de6207:	setbe	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6208] = '\x0f'
        mem[0x7ffff7de6209] = '\x96'
        mem[0x7ffff7de620a] = '\xc1'
        mem[0x7ffff7de6207] = 'A'
        cpu.ZF = False
        cpu.R9B = 0x58
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6207
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6208], b'\x0f')
        self.assertEqual(mem[0x7ffff7de6209], b'\x96')
        self.assertEqual(mem[0x7ffff7de620a], b'\xc1')
        self.assertEqual(mem[0x7ffff7de6207], b'A')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 140737351934475)

    def test_SETBE_6(self):
        ''' Instruction SETBE_6
            Groups:
            0x7ffff7de6207:	setbe	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6208] = '\x0f'
        mem[0x7ffff7de6209] = '\x96'
        mem[0x7ffff7de620a] = '\xc1'
        mem[0x7ffff7de6207] = 'A'
        cpu.ZF = False
        cpu.R9B = 0x58
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6207
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6208], b'\x0f')
        self.assertEqual(mem[0x7ffff7de6209], b'\x96')
        self.assertEqual(mem[0x7ffff7de620a], b'\xc1')
        self.assertEqual(mem[0x7ffff7de6207], b'A')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 140737351934475)

    def test_SETB_1(self):
        ''' Instruction SETB_1
            Groups:
            0x4342ea:	setb	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x004342ea] = '\x0f'
        mem[0x004342eb] = '\x92'
        mem[0x004342ec] = '\xc0'
        cpu.CF = False
        cpu.RIP = 0x4342ea
        cpu.AL = 0xc0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4342ea], b'\x0f')
        self.assertEqual(mem[0x4342eb], b'\x92')
        self.assertEqual(mem[0x4342ec], b'\xc0')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 4408045)

    def test_SETB_2(self):
        ''' Instruction SETB_2
            Groups:
            0x43426a:	setb	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x0043426a] = '\x0f'
        mem[0x0043426b] = '\x92'
        mem[0x0043426c] = '\xc0'
        cpu.CF = False
        cpu.RIP = 0x43426a
        cpu.AL = 0xc0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x43426a], b'\x0f')
        self.assertEqual(mem[0x43426b], b'\x92')
        self.assertEqual(mem[0x43426c], b'\xc0')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 4407917)

    def test_SETB_3(self):
        ''' Instruction SETB_3
            Groups:
            0x4346ca:	setb	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x004346ca] = '\x0f'
        mem[0x004346cb] = '\x92'
        mem[0x004346cc] = '\xc0'
        cpu.CF = False
        cpu.RIP = 0x4346ca
        cpu.AL = 0xc0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4346ca], b'\x0f')
        self.assertEqual(mem[0x4346cb], b'\x92')
        self.assertEqual(mem[0x4346cc], b'\xc0')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 4409037)

    def test_SETB_4(self):
        ''' Instruction SETB_4
            Groups:
            0x4342ea:	setb	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x004342ea] = '\x0f'
        mem[0x004342eb] = '\x92'
        mem[0x004342ec] = '\xc0'
        cpu.CF = False
        cpu.RIP = 0x4342ea
        cpu.AL = 0xc0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4342ea], b'\x0f')
        self.assertEqual(mem[0x4342eb], b'\x92')
        self.assertEqual(mem[0x4342ec], b'\xc0')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 4408045)

    def test_SETB_5(self):
        ''' Instruction SETB_5
            Groups:
            0x4342ea:	setb	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x004342ea] = '\x0f'
        mem[0x004342eb] = '\x92'
        mem[0x004342ec] = '\xc0'
        cpu.CF = False
        cpu.RIP = 0x4342ea
        cpu.AL = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4342ea], b'\x0f')
        self.assertEqual(mem[0x4342eb], b'\x92')
        self.assertEqual(mem[0x4342ec], b'\xc0')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 4408045)

    def test_SETB_6(self):
        ''' Instruction SETB_6
            Groups:
            0x43430a:	setb	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x0043430a] = '\x0f'
        mem[0x0043430b] = '\x92'
        mem[0x0043430c] = '\xc0'
        cpu.CF = False
        cpu.RIP = 0x43430a
        cpu.AL = 0xc0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x43430a], b'\x0f')
        self.assertEqual(mem[0x43430b], b'\x92')
        self.assertEqual(mem[0x43430c], b'\xc0')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 4408077)

    def test_SETE_1(self):
        ''' Instruction SETE_1
            Groups:
            0x7ffff7de36a2:	sete	r10b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36a2] = 'A'
        mem[0x7ffff7de36a3] = '\x0f'
        mem[0x7ffff7de36a4] = '\x94'
        mem[0x7ffff7de36a5] = '\xc2'
        cpu.R10B = 0x0
        cpu.ZF = False
        cpu.RIP = 0x7ffff7de36a2
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de36a2], b'A')
        self.assertEqual(mem[0x7ffff7de36a3], b'\x0f')
        self.assertEqual(mem[0x7ffff7de36a4], b'\x94')
        self.assertEqual(mem[0x7ffff7de36a5], b'\xc2')
        self.assertEqual(cpu.R10B, 0)
        self.assertEqual(cpu.RIP, 140737351923366)

    def test_SETE_2(self):
        ''' Instruction SETE_2
            Groups:
            0x7ffff7de620f:	sete	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6210] = '\x94'
        mem[0x7ffff7de6211] = '\xc0'
        mem[0x7ffff7de620f] = '\x0f'
        cpu.ZF = False
        cpu.AL = 0xf5
        cpu.RIP = 0x7ffff7de620f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6210], b'\x94')
        self.assertEqual(mem[0x7ffff7de6211], b'\xc0')
        self.assertEqual(mem[0x7ffff7de620f], b'\x0f')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 140737351934482)

    def test_SETE_3(self):
        ''' Instruction SETE_3
            Groups:
            0x7ffff7de6229:	sete	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6229] = '\x0f'
        mem[0x7ffff7de622a] = '\x94'
        mem[0x7ffff7de622b] = '\xc0'
        cpu.ZF = True
        cpu.AL = 0x0
        cpu.RIP = 0x7ffff7de6229
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6229], b'\x0f')
        self.assertEqual(mem[0x7ffff7de622a], b'\x94')
        self.assertEqual(mem[0x7ffff7de622b], b'\xc0')
        self.assertEqual(cpu.AL, 1)
        self.assertEqual(cpu.RIP, 140737351934508)

    def test_SETE_4(self):
        ''' Instruction SETE_4
            Groups:
            0x7ffff7de6229:	sete	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6229] = '\x0f'
        mem[0x7ffff7de622a] = '\x94'
        mem[0x7ffff7de622b] = '\xc0'
        cpu.ZF = True
        cpu.AL = 0x0
        cpu.RIP = 0x7ffff7de6229
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6229], b'\x0f')
        self.assertEqual(mem[0x7ffff7de622a], b'\x94')
        self.assertEqual(mem[0x7ffff7de622b], b'\xc0')
        self.assertEqual(cpu.AL, 1)
        self.assertEqual(cpu.RIP, 140737351934508)

    def test_SETE_5(self):
        ''' Instruction SETE_5
            Groups:
            0x432458:	sete	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432458] = 'A'
        mem[0x00432459] = '\x0f'
        mem[0x0043245a] = '\x94'
        mem[0x0043245b] = '\xc1'
        cpu.ZF = False
        cpu.R9B = 0x30
        cpu.RIP = 0x432458
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432458], b'A')
        self.assertEqual(mem[0x432459], b'\x0f')
        self.assertEqual(mem[0x43245a], b'\x94')
        self.assertEqual(mem[0x43245b], b'\xc1')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 4400220)

    def test_SETE_6(self):
        ''' Instruction SETE_6
            Groups:
            0x7ffff7de620f:	sete	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6210] = '\x94'
        mem[0x7ffff7de6211] = '\xc0'
        mem[0x7ffff7de620f] = '\x0f'
        cpu.ZF = False
        cpu.AL = 0xf5
        cpu.RIP = 0x7ffff7de620f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6210], b'\x94')
        self.assertEqual(mem[0x7ffff7de6211], b'\xc0')
        self.assertEqual(mem[0x7ffff7de620f], b'\x0f')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 140737351934482)

    def test_SETG_1(self):
        ''' Instruction SETG_1
            Groups:
            0x555555567df4:	setg	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555567000, 0x1000, 'rwx')
        mem[0x555555567df4] = 'A'
        mem[0x555555567df5] = '\x0f'
        mem[0x555555567df6] = '\x9f'
        mem[0x555555567df7] = '\xc1'
        cpu.OF = False
        cpu.ZF = False
        cpu.R9B = 0x0
        cpu.SF = True
        cpu.RIP = 0x555555567df4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555567df4], b'A')
        self.assertEqual(mem[0x555555567df5], b'\x0f')
        self.assertEqual(mem[0x555555567df6], b'\x9f')
        self.assertEqual(mem[0x555555567df7], b'\xc1')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 93824992312824)

    def test_SETG_2(self):
        ''' Instruction SETG_2
            Groups:
            0x555555567df4:	setg	r9b
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555567000, 0x1000, 'rwx')
        mem[0x555555567df4] = 'A'
        mem[0x555555567df5] = '\x0f'
        mem[0x555555567df6] = '\x9f'
        mem[0x555555567df7] = '\xc1'
        cpu.OF = False
        cpu.ZF = False
        cpu.R9B = 0x0
        cpu.SF = True
        cpu.RIP = 0x555555567df4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x555555567df4], b'A')
        self.assertEqual(mem[0x555555567df5], b'\x0f')
        self.assertEqual(mem[0x555555567df6], b'\x9f')
        self.assertEqual(mem[0x555555567df7], b'\xc1')
        self.assertEqual(cpu.R9B, 0)
        self.assertEqual(cpu.RIP, 93824992312824)

    def test_SETLE_1(self):
        ''' Instruction SETLE_1
            Groups:
            0x448ae0:	setle	dl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00448000, 0x1000, 'rwx')
        mem[0x00448ae0] = '\x0f'
        mem[0x00448ae1] = '\x9e'
        mem[0x00448ae2] = '\xc2'
        cpu.OF = False
        cpu.ZF = True
        cpu.SF = False
        cpu.RIP = 0x448ae0
        cpu.DL = 0x1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x448ae0], b'\x0f')
        self.assertEqual(mem[0x448ae1], b'\x9e')
        self.assertEqual(mem[0x448ae2], b'\xc2')
        self.assertEqual(cpu.DL, 1)
        self.assertEqual(cpu.RIP, 4492003)

    def test_SETLE_2(self):
        ''' Instruction SETLE_2
            Groups:
            0x448ae0:	setle	dl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00448000, 0x1000, 'rwx')
        mem[0x00448ae0] = '\x0f'
        mem[0x00448ae1] = '\x9e'
        mem[0x00448ae2] = '\xc2'
        cpu.OF = False
        cpu.ZF = True
        cpu.SF = False
        cpu.RIP = 0x448ae0
        cpu.DL = 0x1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x448ae0], b'\x0f')
        self.assertEqual(mem[0x448ae1], b'\x9e')
        self.assertEqual(mem[0x448ae2], b'\xc2')
        self.assertEqual(cpu.DL, 1)
        self.assertEqual(cpu.RIP, 4492003)

    def test_SETNE_1(self):
        ''' Instruction SETNE_1
            Groups:
            0x410ee5:	setne	cl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00410000, 0x1000, 'rwx')
        mem[0x00410ee5] = '\x0f'
        mem[0x00410ee6] = '\x95'
        mem[0x00410ee7] = '\xc1'
        cpu.ZF = True
        cpu.RIP = 0x410ee5
        cpu.CL = 0x6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x410ee5], b'\x0f')
        self.assertEqual(mem[0x410ee6], b'\x95')
        self.assertEqual(mem[0x410ee7], b'\xc1')
        self.assertEqual(cpu.RIP, 4263656)
        self.assertEqual(cpu.CL, 0)

    def test_SETNE_2(self):
        ''' Instruction SETNE_2
            Groups:
            0x436d20:	setne	dl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00436000, 0x1000, 'rwx')
        mem[0x00436d20] = '\x0f'
        mem[0x00436d21] = '\x95'
        mem[0x00436d22] = '\xc2'
        cpu.ZF = True
        cpu.DL = 0x0
        cpu.RIP = 0x436d20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x436d20], b'\x0f')
        self.assertEqual(mem[0x436d21], b'\x95')
        self.assertEqual(mem[0x436d22], b'\xc2')
        self.assertEqual(cpu.DL, 0)
        self.assertEqual(cpu.RIP, 4418851)

    def test_SETNE_3(self):
        ''' Instruction SETNE_3
            Groups:
            0x410f05:	setne	cl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00410000, 0x1000, 'rwx')
        mem[0x00410f05] = '\x0f'
        mem[0x00410f06] = '\x95'
        mem[0x00410f07] = '\xc1'
        cpu.ZF = True
        cpu.RIP = 0x410f05
        cpu.CL = 0x6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x410f05], b'\x0f')
        self.assertEqual(mem[0x410f06], b'\x95')
        self.assertEqual(mem[0x410f07], b'\xc1')
        self.assertEqual(cpu.RIP, 4263688)
        self.assertEqual(cpu.CL, 0)

    def test_SETNE_4(self):
        ''' Instruction SETNE_4
            Groups:
            0x436f20:	setne	dl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00436000, 0x1000, 'rwx')
        mem[0x00436f20] = '\x0f'
        mem[0x00436f21] = '\x95'
        mem[0x00436f22] = '\xc2'
        cpu.ZF = True
        cpu.DL = 0x0
        cpu.RIP = 0x436f20
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x436f20], b'\x0f')
        self.assertEqual(mem[0x436f21], b'\x95')
        self.assertEqual(mem[0x436f22], b'\xc2')
        self.assertEqual(cpu.DL, 0)
        self.assertEqual(cpu.RIP, 4419363)

    def test_SETNE_5(self):
        ''' Instruction SETNE_5
            Groups:
            0x4120f9:	setne	cl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00412000, 0x1000, 'rwx')
        mem[0x004120f9] = '\x0f'
        mem[0x004120fa] = '\x95'
        mem[0x004120fb] = '\xc1'
        cpu.ZF = True
        cpu.RIP = 0x4120f9
        cpu.CL = 0x40
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4120f9], b'\x0f')
        self.assertEqual(mem[0x4120fa], b'\x95')
        self.assertEqual(mem[0x4120fb], b'\xc1')
        self.assertEqual(cpu.RIP, 4268284)
        self.assertEqual(cpu.CL, 0)

    def test_SETNE_6(self):
        ''' Instruction SETNE_6
            Groups:
            0x7ffff7de5de4:	setne	al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5de4] = '\x0f'
        mem[0x7ffff7de5de5] = '\x95'
        mem[0x7ffff7de5de6] = '\xc0'
        cpu.ZF = True
        cpu.AL = 0x0
        cpu.RIP = 0x7ffff7de5de4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5de4], b'\x0f')
        self.assertEqual(mem[0x7ffff7de5de5], b'\x95')
        self.assertEqual(mem[0x7ffff7de5de6], b'\xc0')
        self.assertEqual(cpu.AL, 0)
        self.assertEqual(cpu.RIP, 140737351933415)

    def test_SHLX_1(self):
        ''' Instruction SHLX_1
            Groups: bmi2
            0x55555556594d:	shlx	rax, qword ptr [r14 + 0x50], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555565000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffc800] = '\x00'
        mem[0x7fffffffc801] = '\x00'
        mem[0x7fffffffc802] = '\x00'
        mem[0x7fffffffc803] = '\x00'
        mem[0x7fffffffc804] = '\x00'
        mem[0x7fffffffc805] = '\x00'
        mem[0x7fffffffc806] = '\x00'
        mem[0x7fffffffc807] = '\x00'
        mem[0x55555556594d] = '\xc4'
        mem[0x55555556594e] = '\xc2'
        mem[0x55555556594f] = '\xf9'
        mem[0x555555565950] = '\xf7'
        mem[0x555555565951] = 'F'
        mem[0x555555565952] = 'P'
        cpu.R14 = 0x7fffffffc7b0
        cpu.RIP = 0x55555556594d
        cpu.RAX = 0x5
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffc800], b'\x00')
        self.assertEqual(mem[0x7fffffffc801], b'\x00')
        self.assertEqual(mem[0x7fffffffc802], b'\x00')
        self.assertEqual(mem[0x7fffffffc803], b'\x00')
        self.assertEqual(mem[0x7fffffffc804], b'\x00')
        self.assertEqual(mem[0x7fffffffc805], b'\x00')
        self.assertEqual(mem[0x7fffffffc806], b'\x00')
        self.assertEqual(mem[0x7fffffffc807], b'\x00')
        self.assertEqual(mem[0x55555556594d], b'\xc4')
        self.assertEqual(mem[0x55555556594e], b'\xc2')
        self.assertEqual(mem[0x55555556594f], b'\xf9')
        self.assertEqual(mem[0x555555565950], b'\xf7')
        self.assertEqual(mem[0x555555565951], b'F')
        self.assertEqual(mem[0x555555565952], b'P')
        self.assertEqual(cpu.R14, 140737488340912)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 93824992303443)

    def test_SHLX_2(self):
        ''' Instruction SHLX_2
            Groups: bmi2
            0x55555556544a:	shlx	rax, rdx, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555565000, 0x1000, 'rwx')
        mem[0x55555556544a] = '\xc4'
        mem[0x55555556544b] = '\xe2'
        mem[0x55555556544c] = '\xf9'
        mem[0x55555556544d] = '\xf7'
        mem[0x55555556544e] = '\xc2'
        cpu.RIP = 0x55555556544a
        cpu.RAX = 0x8
        cpu.RDX = 0x1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x55555556544a], b'\xc4')
        self.assertEqual(mem[0x55555556544b], b'\xe2')
        self.assertEqual(mem[0x55555556544c], b'\xf9')
        self.assertEqual(mem[0x55555556544d], b'\xf7')
        self.assertEqual(mem[0x55555556544e], b'\xc2')
        self.assertEqual(cpu.RAX, 256)
        self.assertEqual(cpu.RIP, 93824992302159)
        self.assertEqual(cpu.RDX, 1)

    def test_SHLX_3(self):
        ''' Instruction SHLX_3
            Groups: bmi2
            0x55555556544a:	shlx	rax, rdx, rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555565000, 0x1000, 'rwx')
        mem[0x55555556544a] = '\xc4'
        mem[0x55555556544b] = '\xe2'
        mem[0x55555556544c] = '\xf9'
        mem[0x55555556544d] = '\xf7'
        mem[0x55555556544e] = '\xc2'
        cpu.RIP = 0x55555556544a
        cpu.RAX = 0x8
        cpu.RDX = 0x1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x55555556544a], b'\xc4')
        self.assertEqual(mem[0x55555556544b], b'\xe2')
        self.assertEqual(mem[0x55555556544c], b'\xf9')
        self.assertEqual(mem[0x55555556544d], b'\xf7')
        self.assertEqual(mem[0x55555556544e], b'\xc2')
        self.assertEqual(cpu.RAX, 256)
        self.assertEqual(cpu.RIP, 93824992302159)
        self.assertEqual(cpu.RDX, 1)

    def test_SHLX_4(self):
        ''' Instruction SHLX_4
            Groups: bmi2
            0x55555556594d:	shlx	rax, qword ptr [r14 + 0x50], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555565000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffc800] = '\x00'
        mem[0x7fffffffc801] = '\x00'
        mem[0x7fffffffc802] = '\x00'
        mem[0x7fffffffc803] = '\x00'
        mem[0x7fffffffc804] = '\x00'
        mem[0x7fffffffc805] = '\x00'
        mem[0x7fffffffc806] = '\x00'
        mem[0x7fffffffc807] = '\x00'
        mem[0x55555556594d] = '\xc4'
        mem[0x55555556594e] = '\xc2'
        mem[0x55555556594f] = '\xf9'
        mem[0x555555565950] = '\xf7'
        mem[0x555555565951] = 'F'
        mem[0x555555565952] = 'P'
        cpu.R14 = 0x7fffffffc7b0
        cpu.RIP = 0x55555556594d
        cpu.RAX = 0x5
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffc800], b'\x00')
        self.assertEqual(mem[0x7fffffffc801], b'\x00')
        self.assertEqual(mem[0x7fffffffc802], b'\x00')
        self.assertEqual(mem[0x7fffffffc803], b'\x00')
        self.assertEqual(mem[0x7fffffffc804], b'\x00')
        self.assertEqual(mem[0x7fffffffc805], b'\x00')
        self.assertEqual(mem[0x7fffffffc806], b'\x00')
        self.assertEqual(mem[0x7fffffffc807], b'\x00')
        self.assertEqual(mem[0x55555556594d], b'\xc4')
        self.assertEqual(mem[0x55555556594e], b'\xc2')
        self.assertEqual(mem[0x55555556594f], b'\xf9')
        self.assertEqual(mem[0x555555565950], b'\xf7')
        self.assertEqual(mem[0x555555565951], b'F')
        self.assertEqual(mem[0x555555565952], b'P')
        self.assertEqual(cpu.R14, 140737488340912)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RIP, 93824992303443)

    def test_SHL_1(self):
        ''' Instruction SHL_1
            Groups:
            0x7ffff7de438f:	shl	rsi, 5
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4390] = '\xc1'
        mem[0x7ffff7de4391] = '\xe6'
        mem[0x7ffff7de4392] = '\x05'
        mem[0x7ffff7de438f] = 'H'
        cpu.RSI = 0x597904
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de438f
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4390], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4391], b'\xe6')
        self.assertEqual(mem[0x7ffff7de4392], b'\x05')
        self.assertEqual(mem[0x7ffff7de438f], b'H')
        self.assertEqual(cpu.RSI, 187637888)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926675)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)

    def test_SHL_2(self):
        ''' Instruction SHL_2
            Groups:
            0x7ffff7de438f:	shl	rsi, 5
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4390] = '\xc1'
        mem[0x7ffff7de4391] = '\xe6'
        mem[0x7ffff7de4392] = '\x05'
        mem[0x7ffff7de438f] = 'H'
        cpu.RSI = 0x7144b72823ea49e0
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de438f
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4390], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4391], b'\xe6')
        self.assertEqual(mem[0x7ffff7de4392], b'\x05')
        self.assertEqual(mem[0x7ffff7de438f], b'H')
        self.assertEqual(cpu.RSI, 2924776815468297216)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926675)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_SHL_3(self):
        ''' Instruction SHL_3
            Groups:
            0x7ffff7de438f:	shl	rsi, 5
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4390] = '\xc1'
        mem[0x7ffff7de4391] = '\xe6'
        mem[0x7ffff7de4392] = '\x05'
        mem[0x7ffff7de438f] = 'H'
        cpu.RSI = 0xcc5c406168309853
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de438f
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4390], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4391], b'\xe6')
        self.assertEqual(mem[0x7ffff7de4392], b'\x05')
        self.assertEqual(mem[0x7ffff7de438f], b'H')
        self.assertEqual(cpu.RSI, 10054299555619605088)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351926675)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, True)

    def test_SHL_4(self):
        ''' Instruction SHL_4
            Groups:
            0x7ffff7de438f:	shl	rsi, 5
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4390] = '\xc1'
        mem[0x7ffff7de4391] = '\xe6'
        mem[0x7ffff7de4392] = '\x05'
        mem[0x7ffff7de438f] = 'H'
        cpu.RSI = 0x726f9570cfb9645b
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de438f
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4390], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4391], b'\xe6')
        self.assertEqual(mem[0x7ffff7de4392], b'\x05')
        self.assertEqual(mem[0x7ffff7de438f], b'H')
        self.assertEqual(cpu.RSI, 5616743111828736864)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926675)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_SHL_5(self):
        ''' Instruction SHL_5
            Groups:
            0x7ffff7de438f:	shl	rsi, 5
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4390] = '\xc1'
        mem[0x7ffff7de4391] = '\xe6'
        mem[0x7ffff7de4392] = '\x05'
        mem[0x7ffff7de438f] = 'H'
        cpu.RSI = 0x2b60c
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de438f
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4390], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4391], b'\xe6')
        self.assertEqual(mem[0x7ffff7de4392], b'\x05')
        self.assertEqual(mem[0x7ffff7de438f], b'H')
        self.assertEqual(cpu.RSI, 5685632)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926675)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)

    def test_SHL_6(self):
        ''' Instruction SHL_6
            Groups:
            0x7ffff7de438f:	shl	rsi, 5
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4390] = '\xc1'
        mem[0x7ffff7de4391] = '\xe6'
        mem[0x7ffff7de4392] = '\x05'
        mem[0x7ffff7de438f] = 'H'
        cpu.RSI = 0x377beb912d8eae5
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de438f
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4390], b'\xc1')
        self.assertEqual(mem[0x7ffff7de4391], b'\xe6')
        self.assertEqual(mem[0x7ffff7de4392], b'\x05')
        self.assertEqual(mem[0x7ffff7de438f], b'H')
        self.assertEqual(cpu.RSI, 7996096205977115808)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351926675)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_SHR_1(self):
        ''' Instruction SHR_1
            Groups:
            0x7ffff7de405d:	shr	rdx, 1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de405d] = 'H'
        mem[0x7ffff7de405e] = '\xd1'
        mem[0x7ffff7de405f] = '\xea'
        cpu.ZF = False
        cpu.RDX = 0x144a5ad4
        cpu.RIP = 0x7ffff7de405d
        cpu.CF = False
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de405d], b'H')
        self.assertEqual(mem[0x7ffff7de405e], b'\xd1')
        self.assertEqual(mem[0x7ffff7de405f], b'\xea')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925856)
        self.assertEqual(cpu.RDX, 170208618)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_SHR_2(self):
        ''' Instruction SHR_2
            Groups:
            0x7ffff7de391d:	shr	rsi, cl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de391d] = 'H'
        mem[0x7ffff7de391e] = '\xd3'
        mem[0x7ffff7de391f] = '\xee'
        cpu.RSI = 0x20ce23f6
        cpu.CL = 0x6
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7de391d
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de391d], b'H')
        self.assertEqual(mem[0x7ffff7de391e], b'\xd3')
        self.assertEqual(mem[0x7ffff7de391f], b'\xee')
        self.assertEqual(cpu.RSI, 8599695)
        self.assertEqual(cpu.CL, 6)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351924000)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)

    def test_SHR_3(self):
        ''' Instruction SHR_3
            Groups:
            0x7ffff7de3926:	shr	rsi, cl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3928] = '\xee'
        mem[0x7ffff7de3926] = 'H'
        mem[0x7ffff7de3927] = '\xd3'
        cpu.RSI = 0x800000001204088
        cpu.CL = 0xda
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3926
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3928], b'\xee')
        self.assertEqual(mem[0x7ffff7de3926], b'H')
        self.assertEqual(mem[0x7ffff7de3927], b'\xd3')
        self.assertEqual(cpu.RSI, 8589934592)
        self.assertEqual(cpu.CL, 218)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351924009)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_SHR_4(self):
        ''' Instruction SHR_4
            Groups:
            0x7ffff7de61d2:	shr	al, 4
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de61d2] = '\xc0'
        mem[0x7ffff7de61d3] = '\xe8'
        mem[0x7ffff7de61d4] = '\x04'
        cpu.ZF = False
        cpu.AL = 0x22
        cpu.RIP = 0x7ffff7de61d2
        cpu.CF = False
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de61d2], b'\xc0')
        self.assertEqual(mem[0x7ffff7de61d3], b'\xe8')
        self.assertEqual(mem[0x7ffff7de61d4], b'\x04')
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351934421)
        self.assertEqual(cpu.AL, 2)
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.SF, False)

    def test_SHR_5(self):
        ''' Instruction SHR_5
            Groups:
            0x7ffff7de391d:	shr	rsi, cl
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de391d] = 'H'
        mem[0x7ffff7de391e] = '\xd3'
        mem[0x7ffff7de391f] = '\xee'
        cpu.RSI = 0x7c967e3f
        cpu.CL = 0xe
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de391d
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de391d], b'H')
        self.assertEqual(mem[0x7ffff7de391e], b'\xd3')
        self.assertEqual(mem[0x7ffff7de391f], b'\xee')
        self.assertEqual(cpu.RSI, 127577)
        self.assertEqual(cpu.CL, 14)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 140737351924000)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_SHR_6(self):
        ''' Instruction SHR_6
            Groups:
            0x4322bd:	shr	rax, 1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004322bd] = 'H'
        mem[0x004322be] = '\xd1'
        mem[0x004322bf] = '\xe8'
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x4322bd
        cpu.PF = False
        cpu.SF = False
        cpu.RAX = 0x1
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4322bd], b'H')
        self.assertEqual(mem[0x4322be], b'\xd1')
        self.assertEqual(mem[0x4322bf], b'\xe8')
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4399808)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.RAX, 0)

    def test_STC_1(self):
        ''' Instruction STC_1
            Groups:
            0x5667fa:	stc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00566000, 0x1000, 'rwx')
        mem[0x005667fa] = '\xf9'
        cpu.CF = False
        cpu.RIP = 0x5667fa
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5667fa], b'\xf9')
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 5662715)

    def test_STC_2(self):
        ''' Instruction STC_2
            Groups:
            0x42a889:	stc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0042a000, 0x1000, 'rwx')
        mem[0x0042a889] = '\xf9'
        cpu.CF = False
        cpu.RIP = 0x42a889
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x42a889], b'\xf9')
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 4368522)

    def test_STC_3(self):
        ''' Instruction STC_3
            Groups:
            0x60b5d5:	stc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0060b000, 0x1000, 'rwx')
        mem[0x0060b5d5] = '\xf9'
        cpu.CF = False
        cpu.RIP = 0x60b5d5
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x60b5d5], b'\xf9')
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 6338006)

    def test_STC_4(self):
        ''' Instruction STC_4
            Groups:
            0x52da4d:	stc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0052d000, 0x1000, 'rwx')
        mem[0x0052da4d] = '\xf9'
        cpu.CF = False
        cpu.RIP = 0x52da4d
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x52da4d], b'\xf9')
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 5429838)

    def test_STC_5(self):
        ''' Instruction STC_5
            Groups:
            0x56ba0e:	stc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0056b000, 0x1000, 'rwx')
        mem[0x0056ba0e] = '\xf9'
        cpu.CF = False
        cpu.RIP = 0x56ba0e
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x56ba0e], b'\xf9')
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 5683727)

    def test_STC_6(self):
        ''' Instruction STC_6
            Groups:
            0x61a7d6:	stc
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0061a000, 0x1000, 'rwx')
        mem[0x0061a7d6] = '\xf9'
        cpu.CF = False
        cpu.RIP = 0x61a7d6
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x61a7d6], b'\xf9')
        self.assertEqual(cpu.CF, True)
        self.assertEqual(cpu.RIP, 6399959)

    def test_STOSD_1(self):
        ''' Instruction STOSD_1
            Groups:
            0x5555555547c2:	rep stosd	dword ptr [rdi], eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x5555555547c2] = '\xf3'
        mem[0x5555555547c3] = '\xab'
        mem[0x7fffffffda88] = '\x00'
        mem[0x7fffffffda89] = '\x00'
        mem[0x7fffffffda8a] = '\x00'
        mem[0x7fffffffda8b] = '\x00'
        mem[0x7fffffffda8c] = '\x00'
        mem[0x7fffffffda8d] = '\x00'
        mem[0x7fffffffda8e] = '\x00'
        mem[0x7fffffffda8f] = '\x00'
        mem[0x7fffffffdb70] = '\xa0'
        mem[0x7fffffffdb71] = '\xdb'
        mem[0x7fffffffdb72] = '\xff'
        mem[0x7fffffffdb73] = '\xff'
        mem[0x7fffffffdb74] = '\xff'
        mem[0x7fffffffdb75] = '\x7f'
        mem[0x7fffffffdb76] = '\x00'
        mem[0x7fffffffdb77] = '\x00'
        cpu.RDI = 0x7fffffffdb70
        cpu.RCX = 0x6
        cpu.RSI = 0x7fffffffda88
        cpu.RIP = 0x5555555547c2
        cpu.EAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5555555547c2], b'\xf3')
        self.assertEqual(mem[0x5555555547c3], b'\xab')
        self.assertEqual(mem[0x7fffffffda88], b'\x00')
        self.assertEqual(mem[0x7fffffffda89], b'\x00')
        self.assertEqual(mem[0x7fffffffda8a], b'\x00')
        self.assertEqual(mem[0x7fffffffda8b], b'\x00')
        self.assertEqual(mem[0x7fffffffda8c], b'\x00')
        self.assertEqual(mem[0x7fffffffda8d], b'\x00')
        self.assertEqual(mem[0x7fffffffda8e], b'\x00')
        self.assertEqual(mem[0x7fffffffda8f], b'\x00')
        self.assertEqual(mem[0x7fffffffdb70], b'\x00')
        self.assertEqual(mem[0x7fffffffdb71], b'\x00')
        self.assertEqual(mem[0x7fffffffdb72], b'\x00')
        self.assertEqual(mem[0x7fffffffdb73], b'\x00')
        self.assertEqual(mem[0x7fffffffdb74], b'\xff')
        self.assertEqual(mem[0x7fffffffdb75], b'\x7f')
        self.assertEqual(mem[0x7fffffffdb76], b'\x00')
        self.assertEqual(mem[0x7fffffffdb77], b'\x00')
        self.assertEqual(cpu.RCX, 5)
        self.assertEqual(cpu.RDI, 140737488345972)
        self.assertEqual(cpu.RSI, 140737488345736)
        self.assertEqual(cpu.RIP, 93824992233410)
        self.assertEqual(cpu.EAX, 0)

    def test_STOSD_2(self):
        ''' Instruction STOSD_2
            Groups:
            0x5555555547c2:	rep stosd	dword ptr [rdi], eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdb20] = '\x00'
        mem[0x7fffffffdb21] = '\x00'
        mem[0x5555555547c2] = '\xf3'
        mem[0x5555555547c3] = '\xab'
        mem[0x7fffffffda88] = '\x00'
        mem[0x7fffffffda89] = '\x00'
        mem[0x7fffffffda8a] = '\x00'
        mem[0x7fffffffda8b] = '\x00'
        mem[0x7fffffffda8c] = '\x00'
        mem[0x7fffffffdb22] = '\x00'
        mem[0x7fffffffda8e] = '\x00'
        mem[0x7fffffffda8d] = '\x00'
        mem[0x7fffffffdb23] = '\x00'
        mem[0x7fffffffda8f] = '\x00'
        mem[0x7fffffffdb1c] = '\x00'
        mem[0x7fffffffdb1d] = '\x00'
        mem[0x7fffffffdb1e] = '\x00'
        mem[0x7fffffffdb1f] = '\x00'
        cpu.RDI = 0x7fffffffdb1c
        cpu.RCX = 0x1b
        cpu.RSI = 0x7fffffffda88
        cpu.RIP = 0x5555555547c2
        cpu.EAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdb20], b'\x00')
        self.assertEqual(mem[0x7fffffffdb21], b'\x00')
        self.assertEqual(mem[0x5555555547c2], b'\xf3')
        self.assertEqual(mem[0x5555555547c3], b'\xab')
        self.assertEqual(mem[0x7fffffffda88], b'\x00')
        self.assertEqual(mem[0x7fffffffda89], b'\x00')
        self.assertEqual(mem[0x7fffffffda8a], b'\x00')
        self.assertEqual(mem[0x7fffffffda8b], b'\x00')
        self.assertEqual(mem[0x7fffffffda8c], b'\x00')
        self.assertEqual(mem[0x7fffffffda8d], b'\x00')
        self.assertEqual(mem[0x7fffffffda8e], b'\x00')
        self.assertEqual(mem[0x7fffffffda8f], b'\x00')
        self.assertEqual(mem[0x7fffffffdb23], b'\x00')
        self.assertEqual(mem[0x7fffffffdb22], b'\x00')
        self.assertEqual(mem[0x7fffffffdb1c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb1d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb1e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb1f], b'\x00')
        self.assertEqual(cpu.RCX, 26)
        self.assertEqual(cpu.RDI, 140737488345888)
        self.assertEqual(cpu.RSI, 140737488345736)
        self.assertEqual(cpu.RIP, 93824992233410)
        self.assertEqual(cpu.EAX, 0)

    def test_STOSD_3(self):
        ''' Instruction STOSD_3
            Groups:
            0x5555555547c2:	rep stosd	dword ptr [rdi], eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdaa0] = '&'
        mem[0x7fffffffdaa1] = '\xb0'
        mem[0x5555555547c2] = '\xf3'
        mem[0x5555555547c3] = '\xab'
        mem[0x7fffffffda88] = '\x00'
        mem[0x7fffffffda89] = '\x00'
        mem[0x7fffffffda8a] = '\x00'
        mem[0x7fffffffda8b] = '\x00'
        mem[0x7fffffffda8c] = '\x00'
        mem[0x7fffffffdaa2] = 'b'
        mem[0x7fffffffda8e] = '\x00'
        mem[0x7fffffffda8d] = '\x00'
        mem[0x7fffffffdaa3] = 'e'
        mem[0x7fffffffda8f] = '\x00'
        mem[0x7fffffffda9c] = '\xff'
        mem[0x7fffffffda9d] = '\x7f'
        mem[0x7fffffffda9e] = '\x00'
        mem[0x7fffffffda9f] = '\x00'
        cpu.RDI = 0x7fffffffda9c
        cpu.RCX = 0x3b
        cpu.RSI = 0x7fffffffda88
        cpu.RIP = 0x5555555547c2
        cpu.EAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdaa0], b'&')
        self.assertEqual(mem[0x7fffffffdaa1], b'\xb0')
        self.assertEqual(mem[0x5555555547c2], b'\xf3')
        self.assertEqual(mem[0x5555555547c3], b'\xab')
        self.assertEqual(mem[0x7fffffffda88], b'\x00')
        self.assertEqual(mem[0x7fffffffda89], b'\x00')
        self.assertEqual(mem[0x7fffffffda8a], b'\x00')
        self.assertEqual(mem[0x7fffffffda8b], b'\x00')
        self.assertEqual(mem[0x7fffffffda8c], b'\x00')
        self.assertEqual(mem[0x7fffffffda8d], b'\x00')
        self.assertEqual(mem[0x7fffffffda8e], b'\x00')
        self.assertEqual(mem[0x7fffffffda8f], b'\x00')
        self.assertEqual(mem[0x7fffffffdaa3], b'e')
        self.assertEqual(mem[0x7fffffffdaa2], b'b')
        self.assertEqual(mem[0x7fffffffda9c], b'\x00')
        self.assertEqual(mem[0x7fffffffda9d], b'\x00')
        self.assertEqual(mem[0x7fffffffda9e], b'\x00')
        self.assertEqual(mem[0x7fffffffda9f], b'\x00')
        self.assertEqual(cpu.RCX, 58)
        self.assertEqual(cpu.RDI, 140737488345760)
        self.assertEqual(cpu.RSI, 140737488345736)
        self.assertEqual(cpu.RIP, 93824992233410)
        self.assertEqual(cpu.EAX, 0)

    def test_STOSD_4(self):
        ''' Instruction STOSD_4
            Groups:
            0x5555555547c2:	rep stosd	dword ptr [rdi], eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x5555555547c2] = '\xf3'
        mem[0x5555555547c3] = '\xab'
        mem[0x7fffffffdaec] = '\xff'
        mem[0x7fffffffda88] = '\x00'
        mem[0x7fffffffda89] = '\x00'
        mem[0x7fffffffda8a] = '\x00'
        mem[0x7fffffffda8b] = '\x00'
        mem[0x7fffffffda8c] = '\x00'
        mem[0x7fffffffda8d] = '\x00'
        mem[0x7fffffffdaee] = '\x00'
        mem[0x7fffffffdaed] = '\x7f'
        mem[0x7fffffffdaf0] = '\x00'
        mem[0x7fffffffdaf1] = '\x00'
        mem[0x7fffffffdaf2] = '\x00'
        mem[0x7fffffffdaf3] = '\x00'
        mem[0x7fffffffda8e] = '\x00'
        mem[0x7fffffffdaef] = '\x00'
        mem[0x7fffffffda8f] = '\x00'
        cpu.RDI = 0x7fffffffdaec
        cpu.RCX = 0x27
        cpu.RSI = 0x7fffffffda88
        cpu.RIP = 0x5555555547c2
        cpu.EAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5555555547c2], b'\xf3')
        self.assertEqual(mem[0x5555555547c3], b'\xab')
        self.assertEqual(mem[0x7fffffffdaec], b'\x00')
        self.assertEqual(mem[0x7fffffffdaed], b'\x00')
        self.assertEqual(mem[0x7fffffffda88], b'\x00')
        self.assertEqual(mem[0x7fffffffda89], b'\x00')
        self.assertEqual(mem[0x7fffffffda8a], b'\x00')
        self.assertEqual(mem[0x7fffffffda8b], b'\x00')
        self.assertEqual(mem[0x7fffffffda8c], b'\x00')
        self.assertEqual(mem[0x7fffffffda8d], b'\x00')
        self.assertEqual(mem[0x7fffffffda8e], b'\x00')
        self.assertEqual(mem[0x7fffffffda8f], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf0], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf1], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf2], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf3], b'\x00')
        self.assertEqual(mem[0x7fffffffdaee], b'\x00')
        self.assertEqual(mem[0x7fffffffdaef], b'\x00')
        self.assertEqual(cpu.RCX, 38)
        self.assertEqual(cpu.RDI, 140737488345840)
        self.assertEqual(cpu.RSI, 140737488345736)
        self.assertEqual(cpu.RIP, 93824992233410)
        self.assertEqual(cpu.EAX, 0)

    def test_STOSD_5(self):
        ''' Instruction STOSD_5
            Groups:
            0x5555555547c2:	rep stosd	dword ptr [rdi], eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7fffffffdb80] = 'P'
        mem[0x7fffffffdb81] = 'I'
        mem[0x5555555547c2] = '\xf3'
        mem[0x5555555547c3] = '\xab'
        mem[0x7fffffffda88] = '\x00'
        mem[0x7fffffffda89] = '\x00'
        mem[0x7fffffffda8a] = '\x00'
        mem[0x7fffffffda8b] = '\x00'
        mem[0x7fffffffda8c] = '\x00'
        mem[0x7fffffffdb82] = 'U'
        mem[0x7fffffffda8e] = '\x00'
        mem[0x7fffffffda8d] = '\x00'
        mem[0x7fffffffdb83] = 'U'
        mem[0x7fffffffda8f] = '\x00'
        mem[0x7fffffffdb7c] = '\x00'
        mem[0x7fffffffdb7d] = '\x00'
        mem[0x7fffffffdb7e] = '\x00'
        mem[0x7fffffffdb7f] = '\x00'
        cpu.RDI = 0x7fffffffdb7c
        cpu.RCX = 0x3
        cpu.RSI = 0x7fffffffda88
        cpu.RIP = 0x5555555547c2
        cpu.EAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffdb80], b'P')
        self.assertEqual(mem[0x7fffffffdb81], b'I')
        self.assertEqual(mem[0x5555555547c2], b'\xf3')
        self.assertEqual(mem[0x5555555547c3], b'\xab')
        self.assertEqual(mem[0x7fffffffda88], b'\x00')
        self.assertEqual(mem[0x7fffffffda89], b'\x00')
        self.assertEqual(mem[0x7fffffffda8a], b'\x00')
        self.assertEqual(mem[0x7fffffffda8b], b'\x00')
        self.assertEqual(mem[0x7fffffffda8c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb82], b'U')
        self.assertEqual(mem[0x7fffffffda8e], b'\x00')
        self.assertEqual(mem[0x7fffffffda8d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb83], b'U')
        self.assertEqual(mem[0x7fffffffda8f], b'\x00')
        self.assertEqual(mem[0x7fffffffdb7c], b'\x00')
        self.assertEqual(mem[0x7fffffffdb7d], b'\x00')
        self.assertEqual(mem[0x7fffffffdb7e], b'\x00')
        self.assertEqual(mem[0x7fffffffdb7f], b'\x00')
        self.assertEqual(cpu.RCX, 2)
        self.assertEqual(cpu.RDI, 140737488345984)
        self.assertEqual(cpu.RSI, 140737488345736)
        self.assertEqual(cpu.RIP, 93824992233410)
        self.assertEqual(cpu.EAX, 0)

    def test_STOSD_6(self):
        ''' Instruction STOSD_6
            Groups:
            0x5555555547c2:	rep stosd	dword ptr [rdi], eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x5555555547c2] = '\xf3'
        mem[0x5555555547c3] = '\xab'
        mem[0x7fffffffda88] = '\x00'
        mem[0x7fffffffda89] = '\x00'
        mem[0x7fffffffda8a] = '\x00'
        mem[0x7fffffffda8b] = '\x00'
        mem[0x7fffffffda8c] = '\x00'
        mem[0x7fffffffda8d] = '\x00'
        mem[0x7fffffffda8e] = '\x00'
        mem[0x7fffffffda8f] = '\x00'
        mem[0x7fffffffdaf0] = '\x00'
        mem[0x7fffffffdaf1] = '\x00'
        mem[0x7fffffffdaf2] = '\x00'
        mem[0x7fffffffdaf3] = '\x00'
        mem[0x7fffffffdaf4] = '\x00'
        mem[0x7fffffffdaf5] = '\x00'
        mem[0x7fffffffdaf6] = '\x00'
        mem[0x7fffffffdaf7] = '\x00'
        cpu.RDI = 0x7fffffffdaf0
        cpu.RCX = 0x26
        cpu.RSI = 0x7fffffffda88
        cpu.RIP = 0x5555555547c2
        cpu.EAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x5555555547c2], b'\xf3')
        self.assertEqual(mem[0x5555555547c3], b'\xab')
        self.assertEqual(mem[0x7fffffffda88], b'\x00')
        self.assertEqual(mem[0x7fffffffda89], b'\x00')
        self.assertEqual(mem[0x7fffffffda8a], b'\x00')
        self.assertEqual(mem[0x7fffffffda8b], b'\x00')
        self.assertEqual(mem[0x7fffffffda8c], b'\x00')
        self.assertEqual(mem[0x7fffffffda8d], b'\x00')
        self.assertEqual(mem[0x7fffffffda8e], b'\x00')
        self.assertEqual(mem[0x7fffffffda8f], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf0], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf1], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf2], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf3], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf4], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf5], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf6], b'\x00')
        self.assertEqual(mem[0x7fffffffdaf7], b'\x00')
        self.assertEqual(cpu.RCX, 37)
        self.assertEqual(cpu.RDI, 140737488345844)
        self.assertEqual(cpu.RSI, 140737488345736)
        self.assertEqual(cpu.RIP, 93824992233410)
        self.assertEqual(cpu.EAX, 0)

    def test_STOSQ_1(self):
        ''' Instruction STOSQ_1
            Groups:
            0x7ffff7ded09b:	rep stosq	qword ptr [rdi], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ded000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7fd7000, 0x1000, 'rwx')
        mem[0x7ffff7fd7700] = '\x00'
        mem[0x7ffff7fd7701] = '\x00'
        mem[0x7ffff7fd7702] = '\x00'
        mem[0x7ffff7fd7703] = '\x00'
        mem[0x7ffff7fd7704] = '\x00'
        mem[0x7ffff7fd7705] = '\x00'
        mem[0x7ffff7fd7706] = '\x00'
        mem[0x7ffff7fd7707] = '\x00'
        mem[0x7ffff7ded09c] = 'H'
        mem[0x7ffff7ded09d] = '\xab'
        mem[0x7ffff7ded09b] = '\xf3'
        mem[0x7ffff7fd7f38] = '\x00'
        mem[0x7ffff7fd7f39] = '\x00'
        mem[0x7ffff7fd7f3a] = '\x00'
        mem[0x7ffff7fd7f3b] = '\x00'
        mem[0x7ffff7fd7f3c] = '\x00'
        mem[0x7ffff7fd7f3d] = '\x00'
        mem[0x7ffff7fd7f3e] = '\x00'
        mem[0x7ffff7fd7f3f] = '\x00'
        cpu.RDI = 0x7ffff7fd7f38
        cpu.RIP = 0x7ffff7ded09b
        cpu.RCX = 0x19
        cpu.RSI = 0x7ffff7fd7700
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7fd7700], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7701], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7702], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7703], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7704], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7705], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7706], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7707], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7f3b], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7f3c], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7f3d], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7f38], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7f39], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7f3a], b'\x00')
        self.assertEqual(mem[0x7ffff7ded09b], b'\xf3')
        self.assertEqual(mem[0x7ffff7ded09c], b'H')
        self.assertEqual(mem[0x7ffff7ded09d], b'\xab')
        self.assertEqual(mem[0x7ffff7fd7f3e], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7f3f], b'\x00')
        self.assertEqual(cpu.RCX, 24)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RDI, 140737353973568)
        self.assertEqual(cpu.RSI, 140737353971456)
        self.assertEqual(cpu.RIP, 140737351962779)

    def test_STOSQ_2(self):
        ''' Instruction STOSQ_2
            Groups:
            0x7ffff7ded09b:	rep stosq	qword ptr [rdi], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ded000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7fd7000, 0x1000, 'rwx')
        mem[0x7ffff7fd7700] = '\x00'
        mem[0x7ffff7fd7701] = '\x00'
        mem[0x7ffff7fd7702] = '\x00'
        mem[0x7ffff7fd7703] = '\x00'
        mem[0x7ffff7fd7704] = '\x00'
        mem[0x7ffff7fd7705] = '\x00'
        mem[0x7ffff7fd7706] = '\x00'
        mem[0x7ffff7fd7707] = '\x00'
        mem[0x7ffff7ded09c] = 'H'
        mem[0x7ffff7ded09d] = '\xab'
        mem[0x7ffff7ded09b] = '\xf3'
        mem[0x7ffff7fd7cb8] = '\x00'
        mem[0x7ffff7fd7cb9] = '\x00'
        mem[0x7ffff7fd7cba] = '\x00'
        mem[0x7ffff7fd7cbb] = '\x00'
        mem[0x7ffff7fd7cbc] = '\x00'
        mem[0x7ffff7fd7cbd] = '\x00'
        mem[0x7ffff7fd7cbe] = '\x00'
        mem[0x7ffff7fd7cbf] = '\x00'
        cpu.RDI = 0x7ffff7fd7cb8
        cpu.RIP = 0x7ffff7ded09b
        cpu.RCX = 0x69
        cpu.RSI = 0x7ffff7fd7700
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7fd7700], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7701], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7702], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7703], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7704], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7705], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7706], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7707], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7cbc], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7cbd], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7cbb], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7cb8], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7cb9], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7cba], b'\x00')
        self.assertEqual(mem[0x7ffff7ded09b], b'\xf3')
        self.assertEqual(mem[0x7ffff7ded09c], b'H')
        self.assertEqual(mem[0x7ffff7ded09d], b'\xab')
        self.assertEqual(mem[0x7ffff7fd7cbe], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7cbf], b'\x00')
        self.assertEqual(cpu.RCX, 104)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RDI, 140737353972928)
        self.assertEqual(cpu.RSI, 140737353971456)
        self.assertEqual(cpu.RIP, 140737351962779)

    def test_STOSQ_3(self):
        ''' Instruction STOSQ_3
            Groups:
            0x7ffff7de5ebf:	rep stosq	qword ptr [rdi], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ffe000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x7ffff7de5ec0] = 'H'
        mem[0x7ffff7de5ec1] = '\xab'
        mem[0x7ffff7ffe4a2] = '\xff'
        mem[0x7ffff7ffe4a3] = '\xf7'
        mem[0x7ffff7ffe4a4] = '\xff'
        mem[0x7ffff7ffe4a5] = '\x7f'
        mem[0x7ffff7ffe4a6] = '\x00'
        mem[0x7ffff7ffe4a1] = '\xe4'
        mem[0x7fffffffda88] = '\x90'
        mem[0x7fffffffda89] = 'x'
        mem[0x7fffffffda8a] = '\x00'
        mem[0x7fffffffda8b] = '\x00'
        mem[0x7fffffffda8c] = '\x00'
        mem[0x7fffffffda8d] = '\x00'
        mem[0x7fffffffda8e] = '\x00'
        mem[0x7fffffffda8f] = '\x00'
        mem[0x7ffff7ffe4a0] = '\x00'
        mem[0x7ffff7ffe4a7] = '\x00'
        mem[0x7ffff7de5ebf] = '\xf3'
        cpu.RDI = 0x7fffffffda88
        cpu.RIP = 0x7ffff7de5ebf
        cpu.RCX = 0x7
        cpu.RSI = 0x7ffff7ffe4a0
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de5ec0], b'H')
        self.assertEqual(mem[0x7ffff7de5ec1], b'\xab')
        self.assertEqual(mem[0x7ffff7ffe4a2], b'\xff')
        self.assertEqual(mem[0x7ffff7ffe4a3], b'\xf7')
        self.assertEqual(mem[0x7ffff7ffe4a4], b'\xff')
        self.assertEqual(mem[0x7ffff7ffe4a5], b'\x7f')
        self.assertEqual(mem[0x7ffff7ffe4a6], b'\x00')
        self.assertEqual(mem[0x7ffff7ffe4a1], b'\xe4')
        self.assertEqual(mem[0x7fffffffda88], b'\x00')
        self.assertEqual(mem[0x7fffffffda89], b'\x00')
        self.assertEqual(mem[0x7fffffffda8a], b'\x00')
        self.assertEqual(mem[0x7fffffffda8b], b'\x00')
        self.assertEqual(mem[0x7fffffffda8c], b'\x00')
        self.assertEqual(mem[0x7fffffffda8d], b'\x00')
        self.assertEqual(mem[0x7fffffffda8e], b'\x00')
        self.assertEqual(mem[0x7fffffffda8f], b'\x00')
        self.assertEqual(mem[0x7ffff7ffe4a0], b'\x00')
        self.assertEqual(mem[0x7ffff7ffe4a7], b'\x00')
        self.assertEqual(mem[0x7ffff7de5ebf], b'\xf3')
        self.assertEqual(cpu.RCX, 6)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RDI, 140737488345744)
        self.assertEqual(cpu.RSI, 140737354130592)
        self.assertEqual(cpu.RIP, 140737351933631)

    def test_STOSQ_4(self):
        ''' Instruction STOSQ_4
            Groups:
            0x7ffff7ded09b:	rep stosq	qword ptr [rdi], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ded000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7fd7000, 0x1000, 'rwx')
        mem[0x7ffff7fd7700] = '\x00'
        mem[0x7ffff7fd7701] = '\x00'
        mem[0x7ffff7fd7702] = '\x00'
        mem[0x7ffff7fd7703] = '\x00'
        mem[0x7ffff7fd7704] = '\x00'
        mem[0x7ffff7fd7705] = '\x00'
        mem[0x7ffff7fd7706] = '\x00'
        mem[0x7ffff7fd7707] = '\x00'
        mem[0x7ffff7fd7730] = '\x00'
        mem[0x7ffff7fd7731] = '\x00'
        mem[0x7ffff7fd7732] = '\x00'
        mem[0x7ffff7fd7733] = '\x00'
        mem[0x7ffff7fd7734] = '\x00'
        mem[0x7ffff7fd7735] = '\x00'
        mem[0x7ffff7fd7736] = '\x00'
        mem[0x7ffff7fd7737] = '\x00'
        mem[0x7ffff7ded09b] = '\xf3'
        mem[0x7ffff7ded09c] = 'H'
        mem[0x7ffff7ded09d] = '\xab'
        cpu.RDI = 0x7ffff7fd7730
        cpu.RIP = 0x7ffff7ded09b
        cpu.RCX = 0x11a
        cpu.RSI = 0x7ffff7fd7700
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7fd7700], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7701], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7702], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7703], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7704], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7705], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7706], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7707], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7730], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7731], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7732], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7733], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7734], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7735], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7736], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7737], b'\x00')
        self.assertEqual(mem[0x7ffff7ded09b], b'\xf3')
        self.assertEqual(mem[0x7ffff7ded09c], b'H')
        self.assertEqual(mem[0x7ffff7ded09d], b'\xab')
        self.assertEqual(cpu.RCX, 281)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RDI, 140737353971512)
        self.assertEqual(cpu.RSI, 140737353971456)
        self.assertEqual(cpu.RIP, 140737351962779)

    def test_STOSQ_5(self):
        ''' Instruction STOSQ_5
            Groups:
            0x555555554895:	rep stosq	qword ptr [rdi], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x555555554896] = 'H'
        mem[0x7fffffffda95] = '\x00'
        mem[0x555555554897] = '\xab'
        mem[0x7fffffffda90] = '\x00'
        mem[0x7fffffffda91] = '\x00'
        mem[0x7fffffffda92] = '\x00'
        mem[0x7fffffffda93] = '\x00'
        mem[0x7fffffffda94] = '\x00'
        mem[0x555555554895] = '\xf3'
        mem[0x7fffffffda96] = '\x00'
        mem[0x7fffffffda97] = '\x00'
        mem[0x7fffffffdc98] = '\x1d'
        mem[0x7fffffffdc99] = '\xe0'
        mem[0x7fffffffdc9a] = '\xff'
        mem[0x7fffffffdc9b] = '\xff'
        mem[0x7fffffffdc9c] = '\xff'
        mem[0x7fffffffdc9d] = '\x7f'
        mem[0x7fffffffdc9e] = '\x00'
        mem[0x7fffffffdc9f] = '\x00'
        cpu.RDI = 0x7fffffffda90
        cpu.RIP = 0x555555554895
        cpu.RCX = 0x1e
        cpu.RSI = 0x7fffffffdc98
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffda96], b'\x00')
        self.assertEqual(mem[0x7fffffffda95], b'\x00')
        self.assertEqual(mem[0x7fffffffda97], b'\x00')
        self.assertEqual(mem[0x7fffffffda90], b'\x00')
        self.assertEqual(mem[0x7fffffffda91], b'\x00')
        self.assertEqual(mem[0x7fffffffda92], b'\x00')
        self.assertEqual(mem[0x7fffffffda93], b'\x00')
        self.assertEqual(mem[0x7fffffffda94], b'\x00')
        self.assertEqual(mem[0x555555554895], b'\xf3')
        self.assertEqual(mem[0x555555554896], b'H')
        self.assertEqual(mem[0x555555554897], b'\xab')
        self.assertEqual(mem[0x7fffffffdc98], b'\x1d')
        self.assertEqual(mem[0x7fffffffdc99], b'\xe0')
        self.assertEqual(mem[0x7fffffffdc9a], b'\xff')
        self.assertEqual(mem[0x7fffffffdc9b], b'\xff')
        self.assertEqual(mem[0x7fffffffdc9c], b'\xff')
        self.assertEqual(mem[0x7fffffffdc9d], b'\x7f')
        self.assertEqual(mem[0x7fffffffdc9e], b'\x00')
        self.assertEqual(mem[0x7fffffffdc9f], b'\x00')
        self.assertEqual(cpu.RCX, 29)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RDI, 140737488345752)
        self.assertEqual(cpu.RSI, 140737488346264)
        self.assertEqual(cpu.RIP, 93824992233621)

    def test_STOSQ_6(self):
        ''' Instruction STOSQ_6
            Groups:
            0x7ffff7ded09b:	rep stosq	qword ptr [rdi], rax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ded000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7fd7000, 0x1000, 'rwx')
        mem[0x7ffff7fd7700] = '\x00'
        mem[0x7ffff7fd7701] = '\x00'
        mem[0x7ffff7fd7702] = '\x00'
        mem[0x7ffff7fd7703] = '\x00'
        mem[0x7ffff7fd7704] = '\x00'
        mem[0x7ffff7fd7705] = '\x00'
        mem[0x7ffff7fd7706] = '\x00'
        mem[0x7ffff7fd7707] = '\x00'
        mem[0x7ffff7fd7ef0] = '\x00'
        mem[0x7ffff7fd7ef1] = '\x00'
        mem[0x7ffff7fd7ef2] = '\x00'
        mem[0x7ffff7fd7ef3] = '\x00'
        mem[0x7ffff7fd7ef4] = '\x00'
        mem[0x7ffff7fd7ef5] = '\x00'
        mem[0x7ffff7fd7ef6] = '\x00'
        mem[0x7ffff7fd7ef7] = '\x00'
        mem[0x7ffff7ded09b] = '\xf3'
        mem[0x7ffff7ded09c] = 'H'
        mem[0x7ffff7ded09d] = '\xab'
        cpu.RDI = 0x7ffff7fd7ef0
        cpu.RIP = 0x7ffff7ded09b
        cpu.RCX = 0x22
        cpu.RSI = 0x7ffff7fd7700
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7fd7700], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7701], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7702], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7703], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7704], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7705], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7706], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7707], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef0], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef1], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef2], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef3], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef4], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef5], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef6], b'\x00')
        self.assertEqual(mem[0x7ffff7fd7ef7], b'\x00')
        self.assertEqual(mem[0x7ffff7ded09b], b'\xf3')
        self.assertEqual(mem[0x7ffff7ded09c], b'H')
        self.assertEqual(mem[0x7ffff7ded09d], b'\xab')
        self.assertEqual(cpu.RCX, 33)
        self.assertEqual(cpu.RAX, 0)
        self.assertEqual(cpu.RDI, 140737353973496)
        self.assertEqual(cpu.RSI, 140737353971456)
        self.assertEqual(cpu.RIP, 140737351962779)

    def test_SUB_1(self):
        ''' Instruction SUB_1
            Groups:
            0x4326c3:	sub	rsp, 0x1020
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004326c3] = 'H'
        mem[0x004326c4] = '\x81'
        mem[0x004326c5] = '\xec'
        mem[0x004326c6] = ' '
        mem[0x004326c7] = '\x10'
        mem[0x004326c8] = '\x00'
        mem[0x004326c9] = '\x00'
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RSP = 0x7fffffffdab0
        cpu.CF = False
        cpu.RIP = 0x4326c3
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4326c3], b'H')
        self.assertEqual(mem[0x4326c4], b'\x81')
        self.assertEqual(mem[0x4326c5], b'\xec')
        self.assertEqual(mem[0x4326c6], b' ')
        self.assertEqual(mem[0x4326c7], b'\x10')
        self.assertEqual(mem[0x4326c8], b'\x00')
        self.assertEqual(mem[0x4326c9], b'\x00')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSP, 140737488341648)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4400842)
        self.assertEqual(cpu.SF, False)

    def test_SUB_2(self):
        ''' Instruction SUB_2
            Groups:
            0x40b6dd:	sub	rsp, 0x1028
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040b000, 0x1000, 'rwx')
        mem[0x0040b6e0] = '('
        mem[0x0040b6e1] = '\x10'
        mem[0x0040b6e2] = '\x00'
        mem[0x0040b6e3] = '\x00'
        mem[0x0040b6dd] = 'H'
        mem[0x0040b6de] = '\x81'
        mem[0x0040b6df] = '\xec'
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RSP = 0x7fffffffda18
        cpu.CF = False
        cpu.RIP = 0x40b6dd
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x40b6e0], b'(')
        self.assertEqual(mem[0x40b6e1], b'\x10')
        self.assertEqual(mem[0x40b6e2], b'\x00')
        self.assertEqual(mem[0x40b6e3], b'\x00')
        self.assertEqual(mem[0x40b6dd], b'H')
        self.assertEqual(mem[0x40b6de], b'\x81')
        self.assertEqual(mem[0x40b6df], b'\xec')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSP, 140737488341488)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4241124)
        self.assertEqual(cpu.SF, False)

    def test_SUB_3(self):
        ''' Instruction SUB_3
            Groups:
            0x7ffff7de406d:	sub	rsp, 8
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4070] = '\x08'
        mem[0x7ffff7de406d] = 'H'
        mem[0x7ffff7de406e] = '\x83'
        mem[0x7ffff7de406f] = '\xec'
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.RSP = 0x7fffffffd840
        cpu.CF = False
        cpu.RIP = 0x7ffff7de406d
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de4070], b'\x08')
        self.assertEqual(mem[0x7ffff7de406d], b'H')
        self.assertEqual(mem[0x7ffff7de406e], b'\x83')
        self.assertEqual(mem[0x7ffff7de406f], b'\xec')
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, True)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSP, 140737488345144)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925873)
        self.assertEqual(cpu.SF, False)

    def test_SUB_4(self):
        ''' Instruction SUB_4
            Groups:
            0x7ffff7decc04:	sub	rsp, 0x1020
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7dec000, 0x1000, 'rwx')
        mem[0x7ffff7decc04] = 'H'
        mem[0x7ffff7decc05] = '\x81'
        mem[0x7ffff7decc06] = '\xec'
        mem[0x7ffff7decc07] = ' '
        mem[0x7ffff7decc08] = '\x10'
        mem[0x7ffff7decc09] = '\x00'
        mem[0x7ffff7decc0a] = '\x00'
        cpu.PF = True
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.RSP = 0x7fffffffd0c0
        cpu.CF = False
        cpu.RIP = 0x7ffff7decc04
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7decc04], b'H')
        self.assertEqual(mem[0x7ffff7decc05], b'\x81')
        self.assertEqual(mem[0x7ffff7decc06], b'\xec')
        self.assertEqual(mem[0x7ffff7decc07], b' ')
        self.assertEqual(mem[0x7ffff7decc08], b'\x10')
        self.assertEqual(mem[0x7ffff7decc09], b'\x00')
        self.assertEqual(mem[0x7ffff7decc0a], b'\x00')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSP, 140737488339104)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351961611)
        self.assertEqual(cpu.SF, False)

    def test_SUB_5(self):
        ''' Instruction SUB_5
            Groups:
            0x7ffff7de060d:	sub	rsp, 0x1020
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de0000, 0x1000, 'rwx')
        mem[0x7ffff7de060d] = 'H'
        mem[0x7ffff7de060e] = '\x81'
        mem[0x7ffff7de060f] = '\xec'
        mem[0x7ffff7de0610] = ' '
        mem[0x7ffff7de0611] = '\x10'
        mem[0x7ffff7de0612] = '\x00'
        mem[0x7ffff7de0613] = '\x00'
        cpu.PF = False
        cpu.AF = False
        cpu.OF = False
        cpu.ZF = False
        cpu.RSP = 0x7fffffffd2e0
        cpu.CF = True
        cpu.RIP = 0x7ffff7de060d
        cpu.SF = True
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de060d], b'H')
        self.assertEqual(mem[0x7ffff7de060e], b'\x81')
        self.assertEqual(mem[0x7ffff7de060f], b'\xec')
        self.assertEqual(mem[0x7ffff7de0610], b' ')
        self.assertEqual(mem[0x7ffff7de0611], b'\x10')
        self.assertEqual(mem[0x7ffff7de0612], b'\x00')
        self.assertEqual(mem[0x7ffff7de0613], b'\x00')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSP, 140737488339648)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351910932)
        self.assertEqual(cpu.SF, False)

    def test_SUB_6(self):
        ''' Instruction SUB_6
            Groups:
            0x7ffff7deb22d:	sub	rsp, 0x1078
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7deb000, 0x1000, 'rwx')
        mem[0x7ffff7deb22d] = 'H'
        mem[0x7ffff7deb22e] = '\x81'
        mem[0x7ffff7deb22f] = '\xec'
        mem[0x7ffff7deb230] = 'x'
        mem[0x7ffff7deb231] = '\x10'
        mem[0x7ffff7deb232] = '\x00'
        mem[0x7ffff7deb233] = '\x00'
        cpu.PF = False
        cpu.AF = True
        cpu.OF = False
        cpu.ZF = False
        cpu.RSP = 0x7fffffffd9f8
        cpu.CF = False
        cpu.RIP = 0x7ffff7deb22d
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7deb22d], b'H')
        self.assertEqual(mem[0x7ffff7deb22e], b'\x81')
        self.assertEqual(mem[0x7ffff7deb22f], b'\xec')
        self.assertEqual(mem[0x7ffff7deb230], b'x')
        self.assertEqual(mem[0x7ffff7deb231], b'\x10')
        self.assertEqual(mem[0x7ffff7deb232], b'\x00')
        self.assertEqual(mem[0x7ffff7deb233], b'\x00')
        self.assertEqual(cpu.PF, False)
        self.assertEqual(cpu.AF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.RSP, 140737488341376)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351954996)
        self.assertEqual(cpu.SF, False)

    def test_TEST_1(self):
        ''' Instruction TEST_1
            Groups:
            0x7ffff7df459c:	test	al, al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df459c] = '\x84'
        mem[0x7ffff7df459d] = '\xc0'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7df459c
        cpu.AL = 0x6c
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df459c], b'\x84')
        self.assertEqual(mem[0x7ffff7df459d], b'\xc0')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351992734)
        self.assertEqual(cpu.AL, 108)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_TEST_2(self):
        ''' Instruction TEST_2
            Groups:
            0x7ffff7df459c:	test	al, al
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df459c] = '\x84'
        mem[0x7ffff7df459d] = '\xc0'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7df459c
        cpu.AL = 0x5f
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df459c], b'\x84')
        self.assertEqual(mem[0x7ffff7df459d], b'\xc0')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351992734)
        self.assertEqual(cpu.AL, 95)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_TEST_3(self):
        ''' Instruction TEST_3
            Groups:
            0x7ffff7de3892:	test	r15d, r15d
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3892] = 'E'
        mem[0x7ffff7de3893] = '\x85'
        mem[0x7ffff7de3894] = '\xff'
        cpu.R15D = 0x0
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3892
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3892], b'E')
        self.assertEqual(mem[0x7ffff7de3893], b'\x85')
        self.assertEqual(mem[0x7ffff7de3894], b'\xff')
        self.assertEqual(cpu.R15D, 0)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351923861)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_TEST_4(self):
        ''' Instruction TEST_4
            Groups:
            0x7ffff7b58f07:	test	byte ptr [r8 - 4], 1
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a31000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f07] = 'A'
        mem[0x7ffff7b58f08] = '\xf6'
        mem[0x7ffff7b58f09] = '@'
        mem[0x7ffff7b58f0a] = '\xfc'
        mem[0x7ffff7b58f0b] = '\x01'
        mem[0x7ffff7a3193c] = '\xbc'
        cpu.OF = False
        cpu.ZF = False
        cpu.R8 = 0x7ffff7a31940
        cpu.CF = False
        cpu.RIP = 0x7ffff7b58f07
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7b58f07], b'A')
        self.assertEqual(mem[0x7ffff7b58f08], b'\xf6')
        self.assertEqual(mem[0x7ffff7b58f09], b'@')
        self.assertEqual(mem[0x7ffff7b58f0a], b'\xfc')
        self.assertEqual(mem[0x7ffff7b58f0b], b'\x01')
        self.assertEqual(mem[0x7ffff7a3193c], b'\xbc')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.R8, 140737348049216)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737349259020)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_TEST_5(self):
        ''' Instruction TEST_5
            Groups:
            0x7ffff7ddc6b7:	test	rdi, rdi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ddc000, 0x1000, 'rwx')
        mem[0x7ffff7ddc6b8] = '\x85'
        mem[0x7ffff7ddc6b9] = '\xff'
        mem[0x7ffff7ddc6b7] = 'H'
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7ddc6b7
        cpu.PF = True
        cpu.RDI = 0x7ffff7ffa3a0
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7ddc6b8], b'\x85')
        self.assertEqual(mem[0x7ffff7ddc6b9], b'\xff')
        self.assertEqual(mem[0x7ffff7ddc6b7], b'H')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351894714)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.RDI, 140737354113952)
        self.assertEqual(cpu.SF, False)

    def test_TEST_6(self):
        ''' Instruction TEST_6
            Groups:
            0x406e88:	test	rbx, rbx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem[0x00406e88] = 'H'
        mem[0x00406e89] = '\x85'
        mem[0x00406e8a] = '\xdb'
        cpu.RBX = 0x7fffffffe927
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x406e88
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x406e88], b'H')
        self.assertEqual(mem[0x406e89], b'\x85')
        self.assertEqual(mem[0x406e8a], b'\xdb')
        self.assertEqual(cpu.RBX, 140737488349479)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, False)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 4222603)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_VMOVD_1(self):
        ''' Instruction VMOVD_1
            Groups: avx
            0x432054:	vmovd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432054] = '\xc5'
        mem[0x00432055] = '\xf9'
        mem[0x00432056] = 'n'
        mem[0x00432057] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x432054
        cpu.ESI = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432054], b'\xc5')
        self.assertEqual(mem[0x432055], b'\xf9')
        self.assertEqual(mem[0x432056], b'n')
        self.assertEqual(mem[0x432057], b'\xce')
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.ESI, 0)
        self.assertEqual(cpu.RIP, 4399192)

    def test_VMOVD_2(self):
        ''' Instruction VMOVD_2
            Groups: avx
            0x432154:	vmovd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432154] = '\xc5'
        mem[0x00432155] = '\xf9'
        mem[0x00432156] = 'n'
        mem[0x00432157] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x432154
        cpu.ESI = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432154], b'\xc5')
        self.assertEqual(mem[0x432155], b'\xf9')
        self.assertEqual(mem[0x432156], b'n')
        self.assertEqual(mem[0x432157], b'\xce')
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.ESI, 0)
        self.assertEqual(cpu.RIP, 4399448)

    def test_VMOVD_3(self):
        ''' Instruction VMOVD_3
            Groups: avx
            0x432124:	vmovd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432124] = '\xc5'
        mem[0x00432125] = '\xf9'
        mem[0x00432126] = 'n'
        mem[0x00432127] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x432124
        cpu.ESI = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432124], b'\xc5')
        self.assertEqual(mem[0x432125], b'\xf9')
        self.assertEqual(mem[0x432126], b'n')
        self.assertEqual(mem[0x432127], b'\xce')
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.ESI, 0)
        self.assertEqual(cpu.RIP, 4399400)

    def test_VMOVD_4(self):
        ''' Instruction VMOVD_4
            Groups: avx
            0x434cd4:	vmovd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x00434cd4] = '\xc5'
        mem[0x00434cd5] = '\xf9'
        mem[0x00434cd6] = 'n'
        mem[0x00434cd7] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x434cd4
        cpu.ESI = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x434cd4], b'\xc5')
        self.assertEqual(mem[0x434cd5], b'\xf9')
        self.assertEqual(mem[0x434cd6], b'n')
        self.assertEqual(mem[0x434cd7], b'\xce')
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.ESI, 0)
        self.assertEqual(cpu.RIP, 4410584)

    def test_VMOVD_5(self):
        ''' Instruction VMOVD_5
            Groups: avx
            0x432134:	vmovd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432134] = '\xc5'
        mem[0x00432135] = '\xf9'
        mem[0x00432136] = 'n'
        mem[0x00432137] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x432134
        cpu.ESI = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432134], b'\xc5')
        self.assertEqual(mem[0x432135], b'\xf9')
        self.assertEqual(mem[0x432136], b'n')
        self.assertEqual(mem[0x432137], b'\xce')
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.ESI, 0)
        self.assertEqual(cpu.RIP, 4399416)

    def test_VMOVD_6(self):
        ''' Instruction VMOVD_6
            Groups: avx
            0x432514:	vmovd	xmm1, esi
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432514] = '\xc5'
        mem[0x00432515] = '\xf9'
        mem[0x00432516] = 'n'
        mem[0x00432517] = '\xce'
        cpu.XMM1 = 0x0
        cpu.RIP = 0x432514
        cpu.ESI = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432514], b'\xc5')
        self.assertEqual(mem[0x432515], b'\xf9')
        self.assertEqual(mem[0x432516], b'n')
        self.assertEqual(mem[0x432517], b'\xce')
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.ESI, 0)
        self.assertEqual(cpu.RIP, 4400408)

    def test_VPSHUFB_1(self):
        ''' Instruction VPSHUFB_1
            Groups: avx
            0x4321af:	vpshufb	xmm0, xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004321b0] = '\xe2'
        mem[0x004321b1] = 'q'
        mem[0x004321b2] = '\x00'
        mem[0x004321b3] = '\xc0'
        mem[0x004321af] = '\xc4'
        cpu.XMM0 = 0x0
        cpu.XMM1 = 0x0
        cpu.RIP = 0x4321af
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4321b0], b'\xe2')
        self.assertEqual(mem[0x4321b1], b'q')
        self.assertEqual(mem[0x4321b2], b'\x00')
        self.assertEqual(mem[0x4321b3], b'\xc0')
        self.assertEqual(mem[0x4321af], b'\xc4')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.RIP, 4399540)

    def test_VPSHUFB_2(self):
        ''' Instruction VPSHUFB_2
            Groups: avx
            0x43215f:	vpshufb	xmm0, xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432160] = '\xe2'
        mem[0x00432161] = 'q'
        mem[0x00432162] = '\x00'
        mem[0x00432163] = '\xc0'
        mem[0x0043215f] = '\xc4'
        cpu.XMM0 = 0x0
        cpu.XMM1 = 0x0
        cpu.RIP = 0x43215f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432160], b'\xe2')
        self.assertEqual(mem[0x432161], b'q')
        self.assertEqual(mem[0x432162], b'\x00')
        self.assertEqual(mem[0x432163], b'\xc0')
        self.assertEqual(mem[0x43215f], b'\xc4')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.RIP, 4399460)

    def test_VPSHUFB_3(self):
        ''' Instruction VPSHUFB_3
            Groups: avx
            0x43205f:	vpshufb	xmm0, xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432060] = '\xe2'
        mem[0x00432061] = 'q'
        mem[0x00432062] = '\x00'
        mem[0x00432063] = '\xc0'
        mem[0x0043205f] = '\xc4'
        cpu.XMM0 = 0x0
        cpu.XMM1 = 0x0
        cpu.RIP = 0x43205f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432060], b'\xe2')
        self.assertEqual(mem[0x432061], b'q')
        self.assertEqual(mem[0x432062], b'\x00')
        self.assertEqual(mem[0x432063], b'\xc0')
        self.assertEqual(mem[0x43205f], b'\xc4')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.RIP, 4399204)

    def test_VPSHUFB_4(self):
        ''' Instruction VPSHUFB_4
            Groups: avx
            0x43212f:	vpshufb	xmm0, xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432130] = '\xe2'
        mem[0x00432131] = 'q'
        mem[0x00432132] = '\x00'
        mem[0x00432133] = '\xc0'
        mem[0x0043212f] = '\xc4'
        cpu.XMM0 = 0x0
        cpu.XMM1 = 0x0
        cpu.RIP = 0x43212f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432130], b'\xe2')
        self.assertEqual(mem[0x432131], b'q')
        self.assertEqual(mem[0x432132], b'\x00')
        self.assertEqual(mem[0x432133], b'\xc0')
        self.assertEqual(mem[0x43212f], b'\xc4')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.RIP, 4399412)

    def test_VPSHUFB_5(self):
        ''' Instruction VPSHUFB_5
            Groups: avx
            0x43213f:	vpshufb	xmm0, xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432140] = '\xe2'
        mem[0x00432141] = 'q'
        mem[0x00432142] = '\x00'
        mem[0x00432143] = '\xc0'
        mem[0x0043213f] = '\xc4'
        cpu.XMM0 = 0x0
        cpu.XMM1 = 0x0
        cpu.RIP = 0x43213f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432140], b'\xe2')
        self.assertEqual(mem[0x432141], b'q')
        self.assertEqual(mem[0x432142], b'\x00')
        self.assertEqual(mem[0x432143], b'\xc0')
        self.assertEqual(mem[0x43213f], b'\xc4')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.RIP, 4399428)

    def test_VPSHUFB_6(self):
        ''' Instruction VPSHUFB_6
            Groups: avx
            0x434cdf:	vpshufb	xmm0, xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00434000, 0x1000, 'rwx')
        mem[0x00434ce0] = '\xe2'
        mem[0x00434ce1] = 'q'
        mem[0x00434ce2] = '\x00'
        mem[0x00434ce3] = '\xc0'
        mem[0x00434cdf] = '\xc4'
        cpu.XMM0 = 0x0
        cpu.XMM1 = 0x0
        cpu.RIP = 0x434cdf
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x434ce0], b'\xe2')
        self.assertEqual(mem[0x434ce1], b'q')
        self.assertEqual(mem[0x434ce2], b'\x00')
        self.assertEqual(mem[0x434ce3], b'\xc0')
        self.assertEqual(mem[0x434cdf], b'\xc4')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.XMM1, 0)
        self.assertEqual(cpu.RIP, 4410596)

    def test_VPXOR_1(self):
        ''' Instruction VPXOR_1
            Groups: avx
            0x4321a0:	vpxor	xmm0, xmm0, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004321a0] = '\xc5'
        mem[0x004321a1] = '\xf9'
        mem[0x004321a2] = '\xef'
        mem[0x004321a3] = '\xc0'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x4321a0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4321a0], b'\xc5')
        self.assertEqual(mem[0x4321a1], b'\xf9')
        self.assertEqual(mem[0x4321a2], b'\xef')
        self.assertEqual(mem[0x4321a3], b'\xc0')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RIP, 4399524)

    def test_VPXOR_2(self):
        ''' Instruction VPXOR_2
            Groups: avx
            0x432510:	vpxor	xmm0, xmm0, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432510] = '\xc5'
        mem[0x00432511] = '\xf9'
        mem[0x00432512] = '\xef'
        mem[0x00432513] = '\xc0'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x432510
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432510], b'\xc5')
        self.assertEqual(mem[0x432511], b'\xf9')
        self.assertEqual(mem[0x432512], b'\xef')
        self.assertEqual(mem[0x432513], b'\xc0')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RIP, 4400404)

    def test_VPXOR_3(self):
        ''' Instruction VPXOR_3
            Groups: avx
            0x432050:	vpxor	xmm0, xmm0, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432050] = '\xc5'
        mem[0x00432051] = '\xf9'
        mem[0x00432052] = '\xef'
        mem[0x00432053] = '\xc0'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x432050
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432050], b'\xc5')
        self.assertEqual(mem[0x432051], b'\xf9')
        self.assertEqual(mem[0x432052], b'\xef')
        self.assertEqual(mem[0x432053], b'\xc0')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RIP, 4399188)

    def test_VPXOR_4(self):
        ''' Instruction VPXOR_4
            Groups: avx
            0x432150:	vpxor	xmm0, xmm0, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432150] = '\xc5'
        mem[0x00432151] = '\xf9'
        mem[0x00432152] = '\xef'
        mem[0x00432153] = '\xc0'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x432150
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432150], b'\xc5')
        self.assertEqual(mem[0x432151], b'\xf9')
        self.assertEqual(mem[0x432152], b'\xef')
        self.assertEqual(mem[0x432153], b'\xc0')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RIP, 4399444)

    def test_VPXOR_5(self):
        ''' Instruction VPXOR_5
            Groups: avx
            0x432130:	vpxor	xmm0, xmm0, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432130] = '\xc5'
        mem[0x00432131] = '\xf9'
        mem[0x00432132] = '\xef'
        mem[0x00432133] = '\xc0'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x432130
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432130], b'\xc5')
        self.assertEqual(mem[0x432131], b'\xf9')
        self.assertEqual(mem[0x432132], b'\xef')
        self.assertEqual(mem[0x432133], b'\xc0')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RIP, 4399412)

    def test_VPXOR_6(self):
        ''' Instruction VPXOR_6
            Groups: avx
            0x432130:	vpxor	xmm0, xmm0, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432130] = '\xc5'
        mem[0x00432131] = '\xf9'
        mem[0x00432132] = '\xef'
        mem[0x00432133] = '\xc0'
        cpu.XMM0 = 0x0
        cpu.RIP = 0x432130
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432130], b'\xc5')
        self.assertEqual(mem[0x432131], b'\xf9')
        self.assertEqual(mem[0x432132], b'\xef')
        self.assertEqual(mem[0x432133], b'\xc0')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RIP, 4399412)

    def test_VZEROUPPER_1(self):
        ''' Instruction VZEROUPPER_1
            Groups: avx
            0x4322a9:	vzeroupper
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004322a9] = '\xc5'
        mem[0x004322aa] = '\xf8'
        mem[0x004322ab] = 'w'
        cpu.RIP = 0x4322a9
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4322a9], b'\xc5')
        self.assertEqual(mem[0x4322aa], b'\xf8')
        self.assertEqual(mem[0x4322ab], b'w')
        self.assertEqual(cpu.RIP, 4399788)

    def test_VZEROUPPER_2(self):
        ''' Instruction VZEROUPPER_2
            Groups: avx
            0x432319:	vzeroupper
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432319] = '\xc5'
        mem[0x0043231a] = '\xf8'
        mem[0x0043231b] = 'w'
        cpu.RIP = 0x432319
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432319], b'\xc5')
        self.assertEqual(mem[0x43231a], b'\xf8')
        self.assertEqual(mem[0x43231b], b'w')
        self.assertEqual(cpu.RIP, 4399900)

    def test_VZEROUPPER_3(self):
        ''' Instruction VZEROUPPER_3
            Groups: avx
            0x4322c9:	vzeroupper
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004322c9] = '\xc5'
        mem[0x004322ca] = '\xf8'
        mem[0x004322cb] = 'w'
        cpu.RIP = 0x4322c9
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4322c9], b'\xc5')
        self.assertEqual(mem[0x4322ca], b'\xf8')
        self.assertEqual(mem[0x4322cb], b'w')
        self.assertEqual(cpu.RIP, 4399820)

    def test_VZEROUPPER_4(self):
        ''' Instruction VZEROUPPER_4
            Groups: avx
            0x432229:	vzeroupper
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432229] = '\xc5'
        mem[0x0043222a] = '\xf8'
        mem[0x0043222b] = 'w'
        cpu.RIP = 0x432229
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432229], b'\xc5')
        self.assertEqual(mem[0x43222a], b'\xf8')
        self.assertEqual(mem[0x43222b], b'w')
        self.assertEqual(cpu.RIP, 4399660)

    def test_VZEROUPPER_5(self):
        ''' Instruction VZEROUPPER_5
            Groups: avx
            0x4322a9:	vzeroupper
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x004322a9] = '\xc5'
        mem[0x004322aa] = '\xf8'
        mem[0x004322ab] = 'w'
        cpu.RIP = 0x4322a9
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x4322a9], b'\xc5')
        self.assertEqual(mem[0x4322aa], b'\xf8')
        self.assertEqual(mem[0x4322ab], b'w')
        self.assertEqual(cpu.RIP, 4399788)

    def test_VZEROUPPER_6(self):
        ''' Instruction VZEROUPPER_6
            Groups: avx
            0x432689:	vzeroupper
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00432000, 0x1000, 'rwx')
        mem[0x00432689] = '\xc5'
        mem[0x0043268a] = '\xf8'
        mem[0x0043268b] = 'w'
        cpu.RIP = 0x432689
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x432689], b'\xc5')
        self.assertEqual(mem[0x43268a], b'\xf8')
        self.assertEqual(mem[0x43268b], b'w')
        self.assertEqual(cpu.RIP, 4400780)

    def test_XGETBV_1(self):
        ''' Instruction XGETBV_1
            Groups:
            0x7ffff7a4eb1b:	xgetbv
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4eb1b] = '\x0f'
        mem[0x7ffff7a4eb1c] = '\x01'
        mem[0x7ffff7a4eb1d] = '\xd0'
        cpu.RIP = 0x7ffff7a4eb1b
        cpu.RCX = 0x0
        cpu.RDX = 0x0
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4eb1b], b'\x0f')
        self.assertEqual(mem[0x7ffff7a4eb1c], b'\x01')
        self.assertEqual(mem[0x7ffff7a4eb1d], b'\xd0')
        self.assertEqual(cpu.RAX, 7)
        self.assertEqual(cpu.RCX, 0)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348168478)

    def test_XGETBV_2(self):
        ''' Instruction XGETBV_2
            Groups:
            0x437c0e:	xgetbv
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00437000, 0x1000, 'rwx')
        mem[0x00437c10] = '\xd0'
        mem[0x00437c0e] = '\x0f'
        mem[0x00437c0f] = '\x01'
        cpu.RIP = 0x437c0e
        cpu.RCX = 0x0
        cpu.RDX = 0x0
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x437c10], b'\xd0')
        self.assertEqual(mem[0x437c0e], b'\x0f')
        self.assertEqual(mem[0x437c0f], b'\x01')
        self.assertEqual(cpu.RAX, 7)
        self.assertEqual(cpu.RCX, 0)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4422673)

    def test_XGETBV_3(self):
        ''' Instruction XGETBV_3
            Groups:
            0x7ffff7a4eb1b:	xgetbv
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4eb1b] = '\x0f'
        mem[0x7ffff7a4eb1c] = '\x01'
        mem[0x7ffff7a4eb1d] = '\xd0'
        cpu.RIP = 0x7ffff7a4eb1b
        cpu.RCX = 0x0
        cpu.RDX = 0x0
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7a4eb1b], b'\x0f')
        self.assertEqual(mem[0x7ffff7a4eb1c], b'\x01')
        self.assertEqual(mem[0x7ffff7a4eb1d], b'\xd0')
        self.assertEqual(cpu.RAX, 7)
        self.assertEqual(cpu.RCX, 0)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 140737348168478)

    def test_XGETBV_4(self):
        ''' Instruction XGETBV_4
            Groups:
            0x43a59e:	xgetbv
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0043a000, 0x1000, 'rwx')
        mem[0x0043a5a0] = '\xd0'
        mem[0x0043a59e] = '\x0f'
        mem[0x0043a59f] = '\x01'
        cpu.RIP = 0x43a59e
        cpu.RCX = 0x0
        cpu.RDX = 0x0
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x43a5a0], b'\xd0')
        self.assertEqual(mem[0x43a59e], b'\x0f')
        self.assertEqual(mem[0x43a59f], b'\x01')
        self.assertEqual(cpu.RAX, 7)
        self.assertEqual(cpu.RCX, 0)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4433313)

    def test_XGETBV_5(self):
        ''' Instruction XGETBV_5
            Groups:
            0x43791e:	xgetbv
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00437000, 0x1000, 'rwx')
        mem[0x00437920] = '\xd0'
        mem[0x0043791e] = '\x0f'
        mem[0x0043791f] = '\x01'
        cpu.RIP = 0x43791e
        cpu.RCX = 0x0
        cpu.RDX = 0x0
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x437920], b'\xd0')
        self.assertEqual(mem[0x43791e], b'\x0f')
        self.assertEqual(mem[0x43791f], b'\x01')
        self.assertEqual(cpu.RAX, 7)
        self.assertEqual(cpu.RCX, 0)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4421921)

    def test_XGETBV_6(self):
        ''' Instruction XGETBV_6
            Groups:
            0x437a6e:	xgetbv
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00437000, 0x1000, 'rwx')
        mem[0x00437a70] = '\xd0'
        mem[0x00437a6e] = '\x0f'
        mem[0x00437a6f] = '\x01'
        cpu.RIP = 0x437a6e
        cpu.RCX = 0x0
        cpu.RDX = 0x0
        cpu.RAX = 0x0
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x437a70], b'\xd0')
        self.assertEqual(mem[0x437a6e], b'\x0f')
        self.assertEqual(mem[0x437a6f], b'\x01')
        self.assertEqual(cpu.RAX, 7)
        self.assertEqual(cpu.RCX, 0)
        self.assertEqual(cpu.RDX, 0)
        self.assertEqual(cpu.RIP, 4422257)

    def test_XORPS_1(self):
        ''' Instruction XORPS_1
            Groups: sse1
            0x530d2f:	xorps	xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00530000, 0x1000, 'rwx')
        mem[0x00530d30] = 'W'
        mem[0x00530d31] = '\xc8'
        mem[0x00530d2f] = '\x0f'
        cpu.XMM0 = 0xfffffffe0000002100000040fffffffe
        cpu.XMM1 = 0xffffffbeffffffdf00000061ffffffbe
        cpu.RIP = 0x530d2f
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x530d30], b'W')
        self.assertEqual(mem[0x530d31], b'\xc8')
        self.assertEqual(mem[0x530d2f], b'\x0f')
        self.assertEqual(cpu.XMM0, 340282366762482139043588486956268388350)
        self.assertEqual(cpu.XMM1, 5149830563390288455574671589440)
        self.assertEqual(cpu.RIP, 5442866)

    def test_XORPS_2(self):
        ''' Instruction XORPS_2
            Groups: sse1
            0x530a6c:	xorps	xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00530000, 0x1000, 'rwx')
        mem[0x00530a6c] = '\x0f'
        mem[0x00530a6d] = 'W'
        mem[0x00530a6e] = '\xc8'
        cpu.XMM0 = 0xfffffffe8000000100000040fffffffe
        cpu.XMM1 = 0xffffffbe7fffffff80000041ffffffbe
        cpu.RIP = 0x530a6c
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x530a6c], b'\x0f')
        self.assertEqual(mem[0x530a6d], b'W')
        self.assertEqual(mem[0x530a6e], b'\xc8')
        self.assertEqual(cpu.XMM0, 340282366802096219710424845394334711806)
        self.assertEqual(cpu.XMM1, 5149830563399511827474087411776)
        self.assertEqual(cpu.RIP, 5442159)

    def test_XORPS_3(self):
        ''' Instruction XORPS_3
            Groups: sse1
            0x54f76a:	xorps	xmm0, xmmword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0054f000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x0054f76a] = '\x0f'
        mem[0x0054f76b] = 'W'
        mem[0x0054f76c] = '\x04'
        mem[0x0054f76d] = '$'
        mem[0x7fffffffccb0] = '\x00'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x80'
        mem[0x7fffffffccb4] = '\xff'
        mem[0x7fffffffccb5] = '\x7f'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = '\xff'
        mem[0x7fffffffccb9] = '\x7f'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        mem[0x7fffffffccbc] = '\x00'
        mem[0x7fffffffccbd] = '\x00'
        mem[0x7fffffffccbe] = '\x00'
        mem[0x7fffffffccbf] = '\x80'
        cpu.XMM0 = 0x0
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x54f76a
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x54f76a], b'\x0f')
        self.assertEqual(mem[0x54f76b], b'W')
        self.assertEqual(mem[0x54f76c], b'\x04')
        self.assertEqual(mem[0x54f76d], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'\x00')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x80')
        self.assertEqual(mem[0x7fffffffccb4], b'\xff')
        self.assertEqual(mem[0x7fffffffccb5], b'\x7f')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b'\xff')
        self.assertEqual(mem[0x7fffffffccb9], b'\x7f')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(mem[0x7fffffffccbc], b'\x00')
        self.assertEqual(mem[0x7fffffffccbd], b'\x00')
        self.assertEqual(mem[0x7fffffffccbe], b'\x00')
        self.assertEqual(mem[0x7fffffffccbf], b'\x80')
        self.assertEqual(cpu.XMM0, 170141183460469836176150507692102778880)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5568366)

    def test_XORPS_4(self):
        ''' Instruction XORPS_4
            Groups: sse1
            0x540f22:	xorps	xmm1, xmm0
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00540000, 0x1000, 'rwx')
        mem[0x00540f22] = '\x0f'
        mem[0x00540f23] = 'W'
        mem[0x00540f24] = '\xc8'
        cpu.XMM0 = 0x200000007f0000002100000020
        cpu.XMM1 = 0x21000000200000007f00000021
        cpu.RIP = 0x540f22
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x540f22], b'\x0f')
        self.assertEqual(mem[0x540f23], b'W')
        self.assertEqual(mem[0x540f24], b'\xc8')
        self.assertEqual(cpu.XMM0, 2535301202799195300496253386784)
        self.assertEqual(cpu.XMM1, 79228164266705024999678279681)
        self.assertEqual(cpu.RIP, 5508901)

    def test_XORPS_5(self):
        ''' Instruction XORPS_5
            Groups: sse1
            0x560955:	xorps	xmm0, xmmword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00560000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x7fffffffccb5] = '\x7f'
        mem[0x00560956] = 'W'
        mem[0x7fffffffccb8] = '!'
        mem[0x00560957] = '\x04'
        mem[0x7fffffffccb0] = '\xff'
        mem[0x7fffffffccb1] = '\xff'
        mem[0x7fffffffccb2] = '\xff'
        mem[0x7fffffffccb3] = '\xff'
        mem[0x7fffffffccb4] = '\xff'
        mem[0x00560955] = '\x0f'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x00560958] = '$'
        mem[0x7fffffffccb9] = 'C'
        mem[0x7fffffffccba] = 'e'
        mem[0x7fffffffccbb] = '\x87'
        mem[0x7fffffffccbc] = '\xff'
        mem[0x7fffffffccbd] = '\xff'
        mem[0x7fffffffccbe] = '\xff'
        mem[0x7fffffffccbf] = '\xff'
        cpu.XMM0 = 0xffffffff8765432100007fffffffffff
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x560955
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7fffffffccbb], b'\x87')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccbf], b'\xff')
        self.assertEqual(mem[0x7fffffffccb0], b'\xff')
        self.assertEqual(mem[0x7fffffffccb1], b'\xff')
        self.assertEqual(mem[0x7fffffffccb2], b'\xff')
        self.assertEqual(mem[0x7fffffffccb3], b'\xff')
        self.assertEqual(mem[0x7fffffffccb4], b'\xff')
        self.assertEqual(mem[0x560955], b'\x0f')
        self.assertEqual(mem[0x560956], b'W')
        self.assertEqual(mem[0x560957], b'\x04')
        self.assertEqual(mem[0x560958], b'$')
        self.assertEqual(mem[0x7fffffffccb9], b'C')
        self.assertEqual(mem[0x7fffffffccba], b'e')
        self.assertEqual(mem[0x7fffffffccb8], b'!')
        self.assertEqual(mem[0x7fffffffccbc], b'\xff')
        self.assertEqual(mem[0x7fffffffccbd], b'\xff')
        self.assertEqual(mem[0x7fffffffccbe], b'\xff')
        self.assertEqual(mem[0x7fffffffccb5], b'\x7f')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5638489)

    def test_XORPS_6(self):
        ''' Instruction XORPS_6
            Groups: sse1
            0x551ec4:	xorps	xmm0, xmmword ptr [rsp]
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00551000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x00551ec4] = '\x0f'
        mem[0x00551ec5] = 'W'
        mem[0x00551ec6] = '\x04'
        mem[0x00551ec7] = '$'
        mem[0x7fffffffccb0] = '\x00'
        mem[0x7fffffffccb1] = '\x00'
        mem[0x7fffffffccb2] = '\x00'
        mem[0x7fffffffccb3] = '\x80'
        mem[0x7fffffffccb4] = ' '
        mem[0x7fffffffccb5] = '\x00'
        mem[0x7fffffffccb6] = '\x00'
        mem[0x7fffffffccb7] = '\x00'
        mem[0x7fffffffccb8] = ' '
        mem[0x7fffffffccb9] = '\x00'
        mem[0x7fffffffccba] = '\x00'
        mem[0x7fffffffccbb] = '\x00'
        mem[0x7fffffffccbc] = '\x00'
        mem[0x7fffffffccbd] = '\x00'
        mem[0x7fffffffccbe] = '\x00'
        mem[0x7fffffffccbf] = '\x80'
        cpu.XMM0 = 0x80000000000000200000002080000000
        cpu.RSP = 0x7fffffffccb0
        cpu.RIP = 0x551ec4
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x551ec4], b'\x0f')
        self.assertEqual(mem[0x551ec5], b'W')
        self.assertEqual(mem[0x551ec6], b'\x04')
        self.assertEqual(mem[0x551ec7], b'$')
        self.assertEqual(mem[0x7fffffffccb0], b'\x00')
        self.assertEqual(mem[0x7fffffffccb1], b'\x00')
        self.assertEqual(mem[0x7fffffffccb2], b'\x00')
        self.assertEqual(mem[0x7fffffffccb3], b'\x80')
        self.assertEqual(mem[0x7fffffffccb4], b' ')
        self.assertEqual(mem[0x7fffffffccb5], b'\x00')
        self.assertEqual(mem[0x7fffffffccb6], b'\x00')
        self.assertEqual(mem[0x7fffffffccb7], b'\x00')
        self.assertEqual(mem[0x7fffffffccb8], b' ')
        self.assertEqual(mem[0x7fffffffccb9], b'\x00')
        self.assertEqual(mem[0x7fffffffccba], b'\x00')
        self.assertEqual(mem[0x7fffffffccbb], b'\x00')
        self.assertEqual(mem[0x7fffffffccbc], b'\x00')
        self.assertEqual(mem[0x7fffffffccbd], b'\x00')
        self.assertEqual(mem[0x7fffffffccbe], b'\x00')
        self.assertEqual(mem[0x7fffffffccbf], b'\x80')
        self.assertEqual(cpu.XMM0, 0)
        self.assertEqual(cpu.RSP, 140737488342192)
        self.assertEqual(cpu.RIP, 5578440)

    def test_XOR_1(self):
        ''' Instruction XOR_1
            Groups:
            0x7ffff7de6223:	xor	eax, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6223] = '1'
        mem[0x7ffff7de6224] = '\xc0'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de6223
        cpu.EAX = 0xffffff00
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de6223], b'1')
        self.assertEqual(mem[0x7ffff7de6224], b'\xc0')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351934501)
        self.assertEqual(cpu.EAX, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_XOR_2(self):
        ''' Instruction XOR_2
            Groups:
            0x7ffff7de405a:	xor	rdx, r13
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de405a] = 'L'
        mem[0x7ffff7de405b] = '1'
        mem[0x7ffff7de405c] = '\xea'
        cpu.PF = True
        cpu.R13 = 0x7c96f087
        cpu.SF = False
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7de405a
        cpu.RDX = 0x7c96f087
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de405a], b'L')
        self.assertEqual(mem[0x7ffff7de405b], b'1')
        self.assertEqual(mem[0x7ffff7de405c], b'\xea')
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.R13, 2090266759)
        self.assertEqual(cpu.SF, False)
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925853)
        self.assertEqual(cpu.RDX, 0)

    def test_XOR_3(self):
        ''' Instruction XOR_3
            Groups:
            0x7ffff7df45a0:	xor	eax, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45a0] = '1'
        mem[0x7ffff7df45a1] = '\xc0'
        cpu.OF = False
        cpu.ZF = True
        cpu.CF = False
        cpu.RIP = 0x7ffff7df45a0
        cpu.EAX = 0xf7ff7c00
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df45a0], b'1')
        self.assertEqual(mem[0x7ffff7df45a1], b'\xc0')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351992738)
        self.assertEqual(cpu.EAX, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_XOR_4(self):
        ''' Instruction XOR_4
            Groups:
            0x7ffff7de3ff6:	xor	edx, edx
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff6] = '1'
        mem[0x7ffff7de3ff7] = '\xd2'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3ff6
        cpu.PF = False
        cpu.EDX = 0x3f3
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3ff6], b'1')
        self.assertEqual(mem[0x7ffff7de3ff7], b'\xd2')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351925752)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.EDX, 0)
        self.assertEqual(cpu.SF, False)

    def test_XOR_5(self):
        ''' Instruction XOR_5
            Groups:
            0x7ffff7df40cc:	xor	eax, eax
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df40cc] = '1'
        mem[0x7ffff7df40cd] = '\xc0'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7df40cc
        cpu.EAX = 0x3c340000
        cpu.PF = False
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7df40cc], b'1')
        self.assertEqual(mem[0x7ffff7df40cd], b'\xc0')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351991502)
        self.assertEqual(cpu.EAX, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_XOR_6(self):
        ''' Instruction XOR_6
            Groups:
            0x7ffff7de3699:	xor	r10d, r10d
        '''
        mem = Memory64()
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3699] = 'E'
        mem[0x7ffff7de369a] = '1'
        mem[0x7ffff7de369b] = '\xd2'
        cpu.OF = False
        cpu.ZF = False
        cpu.CF = False
        cpu.RIP = 0x7ffff7de3699
        cpu.R10D = 0xf7a2e000
        cpu.PF = True
        cpu.SF = False
        cpu.execute()
        #cpu.writeback()
        self.assertEqual(mem[0x7ffff7de3699], b'E')
        self.assertEqual(mem[0x7ffff7de369a], b'1')
        self.assertEqual(mem[0x7ffff7de369b], b'\xd2')
        self.assertEqual(cpu.OF, False)
        self.assertEqual(cpu.ZF, True)
        self.assertEqual(cpu.CF, False)
        self.assertEqual(cpu.RIP, 140737351923356)
        self.assertEqual(cpu.R10D, 0)
        self.assertEqual(cpu.PF, True)
        self.assertEqual(cpu.SF, False)

    def test_ADD_1_symbolic(self):
        ''' Instruction ADD_1
            Groups:
            0x7ffff7de438b:	add	rcx, 1
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de438b] = 'H'
        mem[0x7ffff7de438c] = '\x83'
        mem[0x7ffff7de438d] = '\xc1'
        mem[0x7ffff7de438e] = '\x01'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x7ffff7ba0aba)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de438b
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de438b, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de438c, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de438d, 8)== ord('\xc1'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de438e, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RCX == 0x7ffff7ba0abb)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de438f)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_ADD_2_symbolic(self):
        ''' Instruction ADD_2
            Groups:
            0x7ffff7de4396:	add	rax, rdx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem[0x7ffff7de4398] = '\xd0'
        mem[0x7ffff7de4396] = 'H'
        mem[0x7ffff7de4397] = '\x01'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x310ef63c39)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de4396
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x65)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de4398, 8)== ord('\xd0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de4396, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de4397, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.RAX == 0x310ef63c9e)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de4399)
        condition = Operators.AND(condition, cpu.RDX == 0x65)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_ADD_3_symbolic(self):
        ''' Instruction ADD_3
            Groups:
            0x7ffff7de6128:	add	rdx, 0x18
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6128] = 'H'
        mem[0x7ffff7de6129] = '\x83'
        mem[0x7ffff7de612a] = '\xc2'
        mem[0x7ffff7de612b] = '\x18'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de6128
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x7ffff7a4c978)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6128, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6129, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de612a, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de612b, 8)== ord('\x18'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.AF == True)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de612c)
        condition = Operators.AND(condition, cpu.RDX == 0x7ffff7a4c990)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_ADD_4_symbolic(self):
        ''' Instruction ADD_4
            Groups:
            0x7ffff7de3960:	add	r12, 1
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3960] = 'I'
        mem[0x7ffff7de3961] = '\x83'
        mem[0x7ffff7de3962] = '\xc4'
        mem[0x7ffff7de3963] = '\x01'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.R12 = cs.new_bitvec(64)
        cs.add(cpu.R12 == 0x0)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de3960
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3960, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3961, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3962, 8)== ord('\xc4'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3963, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.R12 == 0x1)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3964)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_ADD_5_symbolic(self):
        ''' Instruction ADD_5
            Groups:
            0x7ffff7de6124:	add	rax, qword ptr [rdx + 0x10]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a49000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d0)
        value = cs.new_bitvec(8)
        cs.add(value == 0x25)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d1)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5b)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d2)
        value = cs.new_bitvec(8)
        cs.add(value == 0x17)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d3)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d4)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a490d7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7de6124] = 'H'
        mem[0x7ffff7de6125] = '\x03'
        mem[0x7ffff7de6126] = 'B'
        mem[0x7ffff7de6127] = '\x10'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x7ffff7a2e000)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de6124
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x7ffff7a490c0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d0, 8)== ord('%'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d1, 8)== ord('['))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d2, 8)== ord('\x17'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d3, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d4, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d5, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a490d7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6124, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6125, 8)== ord('\x03'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6126, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6127, 8)== ord('\x10'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.RAX == 0x7ffff7ba3b25)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de6128)
        condition = Operators.AND(condition, cpu.RDX == 0x7ffff7a490c0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_ADD_6_symbolic(self):
        ''' Instruction ADD_6
            Groups:
            0x7ffff7de6124:	add	rax, qword ptr [rdx + 0x10]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4b000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bcc8)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bcc9)
        value = cs.new_bitvec(8)
        cs.add(value == 0x88)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bcca)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bccb)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bccc)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bccd)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bcce)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7a4bccf)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7de6124] = 'H'
        mem[0x7ffff7de6125] = '\x03'
        mem[0x7ffff7de6126] = 'B'
        mem[0x7ffff7de6127] = '\x10'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x7ffff7a2e000)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de6124
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x7ffff7a4bcb8)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bcc8, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bcc9, 8)== ord('\x88'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bcca, 8)== ord('\x07'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bccb, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bccc, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bccd, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bcce, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4bccf, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6124, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6125, 8)== ord('\x03'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6126, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6127, 8)== ord('\x10'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x7ffff7aa68c0)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de6128)
        condition = Operators.AND(condition, cpu.RDX == 0x7ffff7a4bcb8)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_AND_1_symbolic(self):
        ''' Instruction AND_1
            Groups:
            0x7ffff7b58f2f:	and	r9d, 0xf
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f30] = '\x83'
        mem[0x7ffff7b58f31] = '\xe1'
        mem[0x7ffff7b58f32] = '\x0f'
        mem[0x7ffff7b58f2f] = 'A'
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7b58f2f
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.R9D = cs.new_bitvec(32)
        cs.add(cpu.R9D == 0x12)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f30, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f31, 8)== ord('\xe1'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f32, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f2f, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7b58f33)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.R9D == 0x2)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_AND_2_symbolic(self):
        ''' Instruction AND_2
            Groups:
            0x7ffff7aa7bd0:	and	edx, 0x808
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa7000, 0x1000, 'rwx')
        mem[0x7ffff7aa7bd0] = '\x81'
        mem[0x7ffff7aa7bd1] = '\xe2'
        mem[0x7ffff7aa7bd2] = '\x08'
        mem[0x7ffff7aa7bd3] = '\x08'
        mem[0x7ffff7aa7bd4] = '\x00'
        mem[0x7ffff7aa7bd5] = '\x00'
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7aa7bd0
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0xfbad2807)
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa7bd0, 8)== ord('\x81'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa7bd1, 8)== ord('\xe2'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa7bd2, 8)== ord('\x08'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa7bd3, 8)== ord('\x08'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa7bd4, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa7bd5, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7aa7bd6)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.EDX == 0x800)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_AND_3_symbolic(self):
        ''' Instruction AND_3
            Groups:
            0x7ffff7b58f2f:	and	r9d, 0xf
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f30] = '\x83'
        mem[0x7ffff7b58f31] = '\xe1'
        mem[0x7ffff7b58f32] = '\x0f'
        mem[0x7ffff7b58f2f] = 'A'
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7b58f2f
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.R9D = cs.new_bitvec(32)
        cs.add(cpu.R9D == 0x12)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f30, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f31, 8)== ord('\xe1'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f32, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f2f, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7b58f33)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.R9D == 0x2)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_AND_4_symbolic(self):
        ''' Instruction AND_4
            Groups:
            0x7ffff7de3930:	and	rax, rsi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3930] = 'H'
        mem[0x7ffff7de3931] = '!'
        mem[0x7ffff7de3932] = '\xf0'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x13)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x9)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x7ffff7de3930
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3930, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3931, 8)== ord('!'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3932, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.RSI == 0x13)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RAX == 0x1)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3933)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_AND_5_symbolic(self):
        ''' Instruction AND_5
            Groups:
            0x7ffff7b58f2f:	and	r9d, 0xf
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f30] = '\x83'
        mem[0x7ffff7b58f31] = '\xe1'
        mem[0x7ffff7b58f32] = '\x0f'
        mem[0x7ffff7b58f2f] = 'A'
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7b58f2f
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.R9D = cs.new_bitvec(32)
        cs.add(cpu.R9D == 0x12)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f30, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f31, 8)== ord('\xe1'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f32, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f2f, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7b58f33)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.R9D == 0x2)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_AND_6_symbolic(self):
        ''' Instruction AND_6
            Groups:
            0x7ffff7de3909:	and	ecx, dword ptr [rbx + 0x2f0]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ff7000, 0x1000, 'rwx')
        mem[0x7ffff7de390b] = '\xf0'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ff794a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ff7949)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ff7948)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        mem[0x7ffff7de3909] = '#'
        mem[0x7ffff7de390a] = '\x8b'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ff794b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7de390c] = '\x02'
        mem[0x7ffff7de390d] = '\x00'
        mem[0x7ffff7de390e] = '\x00'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x7ffff7ff7658)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x1c5e843)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de3909
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ff794b, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ff794a, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ff7949, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ff7948, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3909, 8)== ord('#'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de390a, 8)== ord('\x8b'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de390b, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de390c, 8)== ord('\x02'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de390d, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de390e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.RBX == 0x7ffff7ff7658)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.ECX == 0x43)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de390f)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSF_1_symbolic(self):
        ''' Instruction BSF_1
            Groups:
            0x4184cd:	bsf	eax, edx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x4184cd] = '\x0f'
        mem[0x4184ce] = '\xbc'
        mem[0x4184cf] = '\xc2'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x495045)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x80)
        cpu.RIP = 0x4184cd

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4184cd, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x4184ce, 8)== ord('\xbc'))
        condition = Operators.AND(condition, cpu.read_int(0x4184cf, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.EAX == 0x7)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.EDX == 0x80)
        condition = Operators.AND(condition, cpu.RIP == 0x4184d0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSF_2_symbolic(self):
        ''' Instruction BSF_2
            Groups:
            0x4183ed:	bsf	eax, edx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x4183ed] = '\x0f'
        mem[0x4183ee] = '\xbc'
        mem[0x4183ef] = '\xc2'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x4a5301)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x5)
        cpu.RIP = 0x4183ed

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4183ed, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x4183ee, 8)== ord('\xbc'))
        condition = Operators.AND(condition, cpu.read_int(0x4183ef, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.EAX == 0x0)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.EDX == 0x5)
        condition = Operators.AND(condition, cpu.RIP == 0x4183f0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSF_3_symbolic(self):
        ''' Instruction BSF_3
            Groups:
            0x4184bd:	bsf	eax, edx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x4184bd] = '\x0f'
        mem[0x4184be] = '\xbc'
        mem[0x4184bf] = '\xc2'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x495085)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x80)
        cpu.RIP = 0x4184bd

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4184bd, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x4184be, 8)== ord('\xbc'))
        condition = Operators.AND(condition, cpu.read_int(0x4184bf, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.EAX == 0x7)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.EDX == 0x80)
        condition = Operators.AND(condition, cpu.RIP == 0x4184c0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSF_4_symbolic(self):
        ''' Instruction BSF_4
            Groups:
            0x41850a:	bsf	rax, rdx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x41850a] = 'H'
        mem[0x41850b] = '\x0f'
        mem[0x41850c] = '\xbc'
        mem[0x41850d] = '\xc2'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x41850a
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x495100)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x800200020000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x41850a, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x41850b, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x41850c, 8)== ord('\xbc'))
        condition = Operators.AND(condition, cpu.read_int(0x41850d, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RAX == 0x11)
        condition = Operators.AND(condition, cpu.RIP == 0x41850e)
        condition = Operators.AND(condition, cpu.RDX == 0x800200020000)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSF_5_symbolic(self):
        ''' Instruction BSF_5
            Groups:
            0x7ffff7ab5d0a:	bsf	rax, rdx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7ab5000, 0x1000, 'rwx')
        mem[0x7ffff7ab5d0a] = 'H'
        mem[0x7ffff7ab5d0b] = '\x0f'
        mem[0x7ffff7ab5d0c] = '\xbc'
        mem[0x7ffff7ab5d0d] = '\xc2'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7ab5d0a
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x5555555549c0)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0xe0e0e0e0ee080000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ab5d0a, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ab5d0b, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ab5d0c, 8)== ord('\xbc'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ab5d0d, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RAX == 0x13)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7ab5d0e)
        condition = Operators.AND(condition, cpu.RDX == 0xe0e0e0e0ee080000)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSF_6_symbolic(self):
        ''' Instruction BSF_6
            Groups:
            0x4183ed:	bsf	eax, edx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00418000, 0x1000, 'rwx')
        mem[0x4183ed] = '\x0f'
        mem[0x4183ee] = '\xbc'
        mem[0x4183ef] = '\xc2'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x494d05)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x80)
        cpu.RIP = 0x4183ed

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4183ed, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x4183ee, 8)== ord('\xbc'))
        condition = Operators.AND(condition, cpu.read_int(0x4183ef, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.EAX == 0x7)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.EDX == 0x80)
        condition = Operators.AND(condition, cpu.RIP == 0x4183f0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSR_1_symbolic(self):
        ''' Instruction BSR_1
            Groups:
            0x4008b7:	bsr	esi, esi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x4008b8] = '\xbd'
        mem[0x4008b9] = '\xf6'
        mem[0x4008b7] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RIP = 0x4008b7
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0xf)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4008b8, 8)== ord('\xbd'))
        condition = Operators.AND(condition, cpu.read_int(0x4008b9, 8)== ord('\xf6'))
        condition = Operators.AND(condition, cpu.read_int(0x4008b7, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.ESI == 0x3)
        condition = Operators.AND(condition, cpu.RIP == 0x4008ba)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSR_2_symbolic(self):
        ''' Instruction BSR_2
            Groups:
            0x400907:	bsr	esi, esi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400908] = '\xbd'
        mem[0x400909] = '\xf6'
        mem[0x400907] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RIP = 0x400907
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0xf)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400908, 8)== ord('\xbd'))
        condition = Operators.AND(condition, cpu.read_int(0x400909, 8)== ord('\xf6'))
        condition = Operators.AND(condition, cpu.read_int(0x400907, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.ESI == 0x3)
        condition = Operators.AND(condition, cpu.RIP == 0x40090a)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSR_3_symbolic(self):
        ''' Instruction BSR_3
            Groups:
            0x457ac8:	bsr	rsi, rsi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x457ac8] = 'H'
        mem[0x457ac9] = '\x0f'
        mem[0x457aca] = '\xbd'
        mem[0x457acb] = '\xf6'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x4100800)
        cpu.RIP = 0x457ac8

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x457ac8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x457ac9, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x457aca, 8)== ord('\xbd'))
        condition = Operators.AND(condition, cpu.read_int(0x457acb, 8)== ord('\xf6'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RSI == 0x1a)
        condition = Operators.AND(condition, cpu.RIP == 0x457acc)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSR_4_symbolic(self):
        ''' Instruction BSR_4
            Groups:
            0x400847:	bsr	esi, esi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400848] = '\xbd'
        mem[0x400849] = '\xf6'
        mem[0x400847] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RIP = 0x400847
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0xf)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400848, 8)== ord('\xbd'))
        condition = Operators.AND(condition, cpu.read_int(0x400849, 8)== ord('\xf6'))
        condition = Operators.AND(condition, cpu.read_int(0x400847, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.ESI == 0x3)
        condition = Operators.AND(condition, cpu.RIP == 0x40084a)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSR_5_symbolic(self):
        ''' Instruction BSR_5
            Groups:
            0x457c18:	bsr	rsi, rsi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x457c18] = 'H'
        mem[0x457c19] = '\x0f'
        mem[0x457c1a] = '\xbd'
        mem[0x457c1b] = '\xf6'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x41008000)
        cpu.RIP = 0x457c18

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x457c18, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x457c19, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x457c1a, 8)== ord('\xbd'))
        condition = Operators.AND(condition, cpu.read_int(0x457c1b, 8)== ord('\xf6'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RSI == 0x1e)
        condition = Operators.AND(condition, cpu.RIP == 0x457c1c)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BSR_6_symbolic(self):
        ''' Instruction BSR_6
            Groups:
            0x457db8:	bsr	rsi, rsi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x457db8] = 'H'
        mem[0x457db9] = '\x0f'
        mem[0x457dba] = '\xbd'
        mem[0x457dbb] = '\xf6'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x4100800)
        cpu.RIP = 0x457db8

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x457db8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x457db9, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x457dba, 8)== ord('\xbd'))
        condition = Operators.AND(condition, cpu.read_int(0x457dbb, 8)== ord('\xf6'))
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RSI == 0x1a)
        condition = Operators.AND(condition, cpu.RIP == 0x457dbc)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BT_1_symbolic(self):
        ''' Instruction BT_1
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = cs.new_bitvec(32)
        cs.add(cpu.R8D == 0x467)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b8, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b5, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b6, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b7, 8)== ord('\xa3'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de36b9)
        condition = Operators.AND(condition, cpu.R8D == 0x467)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BT_2_symbolic(self):
        ''' Instruction BT_2
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x2)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = cs.new_bitvec(32)
        cs.add(cpu.R8D == 0x467)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b8, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b5, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b6, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b7, 8)== ord('\xa3'))
        condition = Operators.AND(condition, cpu.EAX == 0x2)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de36b9)
        condition = Operators.AND(condition, cpu.R8D == 0x467)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BT_3_symbolic(self):
        ''' Instruction BT_3
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x2)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = cs.new_bitvec(32)
        cs.add(cpu.R8D == 0x467)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b8, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b5, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b6, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b7, 8)== ord('\xa3'))
        condition = Operators.AND(condition, cpu.EAX == 0x2)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de36b9)
        condition = Operators.AND(condition, cpu.R8D == 0x467)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BT_4_symbolic(self):
        ''' Instruction BT_4
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = cs.new_bitvec(32)
        cs.add(cpu.R8D == 0x467)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b8, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b5, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b6, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b7, 8)== ord('\xa3'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de36b9)
        condition = Operators.AND(condition, cpu.R8D == 0x467)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BT_5_symbolic(self):
        ''' Instruction BT_5
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = cs.new_bitvec(32)
        cs.add(cpu.R8D == 0x467)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b8, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b5, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b6, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b7, 8)== ord('\xa3'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de36b9)
        condition = Operators.AND(condition, cpu.R8D == 0x467)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_BT_6_symbolic(self):
        ''' Instruction BT_6
            Groups:
            0x7ffff7de36b5:	bt	r8d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de36b8] = '\xc0'
        mem[0x7ffff7de36b5] = 'A'
        mem[0x7ffff7de36b6] = '\x0f'
        mem[0x7ffff7de36b7] = '\xa3'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x2)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de36b5
        cpu.R8D = cs.new_bitvec(32)
        cs.add(cpu.R8D == 0x467)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b8, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b5, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b6, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de36b7, 8)== ord('\xa3'))
        condition = Operators.AND(condition, cpu.EAX == 0x2)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de36b9)
        condition = Operators.AND(condition, cpu.R8D == 0x467)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CALL_1_symbolic(self):
        ''' Instruction CALL_1
            Groups: call, mode64
            0x7ffff7de447a:	call	0x7ffff7de3800
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd880)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd881)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd882)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd883)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd884)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd885)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd886)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd887)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd888)
        value = cs.new_bitvec(8)
        cs.add(value == 0x48)
        mem[addr] = value
        mem[0x7ffff7de447a] = '\xe8'
        mem[0x7ffff7de447b] = '\x81'
        mem[0x7ffff7de447c] = '\xf3'
        mem[0x7ffff7de447d] = '\xff'
        mem[0x7ffff7de447e] = '\xff'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd878)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd879)
        value = cs.new_bitvec(8)
        cs.add(value == 0x44)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87a)
        value = cs.new_bitvec(8)
        cs.add(value == 0xde)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87b)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87c)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87f)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffd880)
        cpu.RIP = 0x7ffff7de447a
        cpu.RBP = cs.new_bitvec(64)
        cs.add(cpu.RBP == 0x7fffffffd9a0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd880, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd881, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd882, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd883, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd884, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd885, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd886, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd887, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd888, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87a, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87b, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87d, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd878, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd879, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447a, 8)== ord('\xe8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447b, 8)== ord('\x81'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447c, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447d, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447e, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87f, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffd878)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3800)
        condition = Operators.AND(condition, cpu.RBP == 0x7fffffffd9a0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CALL_2_symbolic(self):
        ''' Instruction CALL_2
            Groups: call, mode64
            0x7ffff7a780e1:	call	qword ptr [r8 + 0x38]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a78000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd2000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffb000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdb8)
        value = cs.new_bitvec(8)
        cs.add(value == 0xa2)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdb9)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdba)
        value = cs.new_bitvec(8)
        cs.add(value == 0xa7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdbb)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdbc)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdbd)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdbe)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdbf)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc0)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc1)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc2)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc3)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc4)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffbdc8)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7a780e1] = 'A'
        mem[0x7ffff7a780e2] = '\xff'
        mem[0x7ffff7a780e3] = 'P'
        mem[0x7ffff7a780e4] = '8'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd2578)
        value = cs.new_bitvec(8)
        cs.add(value == 0x60)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd2579)
        value = cs.new_bitvec(8)
        cs.add(value == 0x96)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd257a)
        value = cs.new_bitvec(8)
        cs.add(value == 0xaa)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd257b)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd257c)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd257d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd257e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd257f)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffbdc0)
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x7ffff7dd2540)
        cpu.RIP = 0x7ffff7a780e1
        cpu.RBP = cs.new_bitvec(64)
        cs.add(cpu.RBP == 0x7fffffffc330)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdb8, 8)== ord('\xe5'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdb9, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdba, 8)== ord('\xa7'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdbb, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdbc, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdbd, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdbe, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdbf, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc0, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc1, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc2, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc3, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc4, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc5, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffbdc8, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a780e1, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a780e2, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a780e3, 8)== ord('P'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a780e4, 8)== ord('8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd2578, 8)== ord('`'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd2579, 8)== ord('\x96'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd257a, 8)== ord('\xaa'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd257b, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd257c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd257d, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd257e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd257f, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.R8 == 0x7ffff7dd2540)
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffbdb8)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7aa9660)
        condition = Operators.AND(condition, cpu.RBP == 0x7fffffffc330)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CALL_3_symbolic(self):
        ''' Instruction CALL_3
            Groups: call, mode64
            0x4554b0:	call	0x45c7a0
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00455000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda18)
        value = cs.new_bitvec(8)
        cs.add(value == 0xda)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda19)
        value = cs.new_bitvec(8)
        cs.add(value == 0x53)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda1a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x45)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda1b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda1c)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda1d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda1e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda1f)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda20)
        value = cs.new_bitvec(8)
        cs.add(value == 0x6)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda21)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda22)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda23)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda24)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda25)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda26)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda27)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda28)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4)
        mem[addr] = value
        mem[0x4554b0] = '\xe8'
        mem[0x4554b1] = '\xeb'
        mem[0x4554b2] = 'r'
        mem[0x4554b3] = '\x00'
        mem[0x4554b4] = '\x00'
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffda20)
        cpu.RIP = 0x4554b0
        cpu.RBP = cs.new_bitvec(64)
        cs.add(cpu.RBP == 0x7fffffffdad0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda18, 8)== ord('\xb5'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda19, 8)== ord('T'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda1a, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda1b, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda1c, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda1d, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda1e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda1f, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda20, 8)== ord('\x06'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda21, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda22, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda23, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda24, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda25, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda26, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda27, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda28, 8)== ord('\x04'))
        condition = Operators.AND(condition, cpu.read_int(0x4554b0, 8)== ord('\xe8'))
        condition = Operators.AND(condition, cpu.read_int(0x4554b1, 8)== ord('\xeb'))
        condition = Operators.AND(condition, cpu.read_int(0x4554b2, 8)== ord('r'))
        condition = Operators.AND(condition, cpu.read_int(0x4554b3, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x4554b4, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffda18)
        condition = Operators.AND(condition, cpu.RIP == 0x45c7a0)
        condition = Operators.AND(condition, cpu.RBP == 0x7fffffffdad0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CALL_4_symbolic(self):
        ''' Instruction CALL_4
            Groups: call, mode64
            0x7ffff7de447a:	call	0x7ffff7de3800
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd880)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd881)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd882)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd883)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd884)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd885)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd886)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd887)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd888)
        value = cs.new_bitvec(8)
        cs.add(value == 0x48)
        mem[addr] = value
        mem[0x7ffff7de447a] = '\xe8'
        mem[0x7ffff7de447b] = '\x81'
        mem[0x7ffff7de447c] = '\xf3'
        mem[0x7ffff7de447d] = '\xff'
        mem[0x7ffff7de447e] = '\xff'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd878)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd879)
        value = cs.new_bitvec(8)
        cs.add(value == 0x44)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87a)
        value = cs.new_bitvec(8)
        cs.add(value == 0xde)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87b)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87c)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd87f)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffd880)
        cpu.RIP = 0x7ffff7de447a
        cpu.RBP = cs.new_bitvec(64)
        cs.add(cpu.RBP == 0x7fffffffd9a0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd880, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd881, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd882, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd883, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd884, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd885, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd886, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd887, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd888, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87a, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87b, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87d, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd878, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd879, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447a, 8)== ord('\xe8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447b, 8)== ord('\x81'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447c, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447d, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de447e, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd87f, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffd878)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3800)
        condition = Operators.AND(condition, cpu.RBP == 0x7fffffffd9a0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CALL_5_symbolic(self):
        ''' Instruction CALL_5
            Groups: call, mode64
            0x7ffff7de40a6:	call	0x7ffff7de3660
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd808)
        value = cs.new_bitvec(8)
        cs.add(value == 0xab)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd809)
        value = cs.new_bitvec(8)
        cs.add(value == 0x40)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd80a)
        value = cs.new_bitvec(8)
        cs.add(value == 0xde)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd80b)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd80c)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd80d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd80e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd80f)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd810)
        value = cs.new_bitvec(8)
        cs.add(value == 0xec)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd811)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd812)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd813)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd814)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd815)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd816)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd817)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd818)
        value = cs.new_bitvec(8)
        cs.add(value == 0xd8)
        mem[addr] = value
        mem[0x7ffff7de40a6] = '\xe8'
        mem[0x7ffff7de40a7] = '\xb5'
        mem[0x7ffff7de40a8] = '\xf5'
        mem[0x7ffff7de40a9] = '\xff'
        mem[0x7ffff7de40aa] = '\xff'
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffd810)
        cpu.RIP = 0x7ffff7de40a6
        cpu.RBP = cs.new_bitvec(64)
        cs.add(cpu.RBP == 0x7fffffffd900)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd808, 8)== ord('\xab'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd809, 8)== ord('@'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd80a, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd80b, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd80c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd80d, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd80e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd80f, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd810, 8)== ord('\xec'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd811, 8)== ord('\x04'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd812, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd813, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd814, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd815, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd816, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd817, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd818, 8)== ord('\xd8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de40a6, 8)== ord('\xe8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de40a7, 8)== ord('\xb5'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de40a8, 8)== ord('\xf5'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de40a9, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de40aa, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffd808)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3660)
        condition = Operators.AND(condition, cpu.RBP == 0x7fffffffd900)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CALL_6_symbolic(self):
        ''' Instruction CALL_6
            Groups: call, mode64
            0x45f878:	call	0x413490
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0045f000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb00)
        value = cs.new_bitvec(8)
        cs.add(value == 0x1)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb01)
        value = cs.new_bitvec(8)
        cs.add(value == 0x53)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb02)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb03)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb04)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb05)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb06)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb07)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdb08)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf4)
        mem[addr] = value
        mem[0x45f878] = '\xe8'
        mem[0x45f879] = '\x13'
        mem[0x45f87a] = '<'
        mem[0x45f87b] = '\xfb'
        mem[0x45f87c] = '\xff'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdaf8)
        value = cs.new_bitvec(8)
        cs.add(value == 0x39)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdaf9)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf8)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdafa)
        value = cs.new_bitvec(8)
        cs.add(value == 0x45)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdafb)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdafc)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdafd)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdafe)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffdaff)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffdb00)
        cpu.RIP = 0x45f878
        cpu.RBP = cs.new_bitvec(64)
        cs.add(cpu.RBP == 0x7fffffffdb20)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb00, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb01, 8)== ord('S'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb02, 8)== ord('J'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb03, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb04, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb05, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb06, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb07, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdb08, 8)== ord('\xf4'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdaf8, 8)== ord('}'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdaf9, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdafa, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdafb, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdafc, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x45f878, 8)== ord('\xe8'))
        condition = Operators.AND(condition, cpu.read_int(0x45f879, 8)== ord('\x13'))
        condition = Operators.AND(condition, cpu.read_int(0x45f87a, 8)== ord('<'))
        condition = Operators.AND(condition, cpu.read_int(0x45f87b, 8)== ord('\xfb'))
        condition = Operators.AND(condition, cpu.read_int(0x45f87c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdafd, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdafe, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffdaff, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffdaf8)
        condition = Operators.AND(condition, cpu.RIP == 0x413490)
        condition = Operators.AND(condition, cpu.RBP == 0x7fffffffdb20)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CDQE_1_symbolic(self):
        ''' Instruction CDQE_1
            Groups:
            0x400aa0:	cdqe
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400aa0] = 'H'
        mem[0x400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x92)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400aa0, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x400aa1, 8)== ord('\x98'))
        condition = Operators.AND(condition, cpu.RAX == 0x92)
        condition = Operators.AND(condition, cpu.RIP == 0x400aa2)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CDQE_2_symbolic(self):
        ''' Instruction CDQE_2
            Groups:
            0x400aa0:	cdqe
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400aa0] = 'H'
        mem[0x400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x5a)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400aa0, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x400aa1, 8)== ord('\x98'))
        condition = Operators.AND(condition, cpu.RAX == 0x5a)
        condition = Operators.AND(condition, cpu.RIP == 0x400aa2)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CDQE_3_symbolic(self):
        ''' Instruction CDQE_3
            Groups:
            0x400aa0:	cdqe
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400aa0] = 'H'
        mem[0x400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x80)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400aa0, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x400aa1, 8)== ord('\x98'))
        condition = Operators.AND(condition, cpu.RAX == 0x80)
        condition = Operators.AND(condition, cpu.RIP == 0x400aa2)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CDQE_4_symbolic(self):
        ''' Instruction CDQE_4
            Groups:
            0x400acf:	cdqe
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400ad0] = '\x98'
        mem[0x400acf] = 'H'
        cpu.RIP = 0x400acf
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x98)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400ad0, 8)== ord('\x98'))
        condition = Operators.AND(condition, cpu.read_int(0x400acf, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.RAX == 0x98)
        condition = Operators.AND(condition, cpu.RIP == 0x400ad1)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CDQE_5_symbolic(self):
        ''' Instruction CDQE_5
            Groups:
            0x400aa0:	cdqe
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400aa0] = 'H'
        mem[0x400aa1] = '\x98'
        cpu.RIP = 0x400aa0
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x73)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400aa0, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x400aa1, 8)== ord('\x98'))
        condition = Operators.AND(condition, cpu.RAX == 0x73)
        condition = Operators.AND(condition, cpu.RIP == 0x400aa2)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CDQE_6_symbolic(self):
        ''' Instruction CDQE_6
            Groups:
            0x400b07:	cdqe
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400b08] = '\x98'
        mem[0x400b07] = 'H'
        cpu.RIP = 0x400b07
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0xc6)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400b08, 8)== ord('\x98'))
        condition = Operators.AND(condition, cpu.read_int(0x400b07, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.RAX == 0xc6)
        condition = Operators.AND(condition, cpu.RIP == 0x400b09)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CLC_1_symbolic(self):
        ''' Instruction CLC_1
            Groups:
            0x46a9fc:	clc
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0046a000, 0x1000, 'rwx')
        mem[0x46a9fc] = '\xf8'
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x46a9fc

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x46a9fc, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x46a9fd)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CLC_2_symbolic(self):
        ''' Instruction CLC_2
            Groups:
            0x7542c8:	clc
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00754000, 0x1000, 'rwx')
        mem[0x7542c8] = '\xf8'
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x7542c8

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7542c8, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7542c9)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CLC_3_symbolic(self):
        ''' Instruction CLC_3
            Groups:
            0x4b473c:	clc
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004b4000, 0x1000, 'rwx')
        mem[0x4b473c] = '\xf8'
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x4b473c

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4b473c, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x4b473d)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CLC_4_symbolic(self):
        ''' Instruction CLC_4
            Groups:
            0x49d4dd:	clc
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0049d000, 0x1000, 'rwx')
        mem[0x49d4dd] = '\xf8'
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x49d4dd

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x49d4dd, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x49d4de)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CLC_5_symbolic(self):
        ''' Instruction CLC_5
            Groups:
            0x4fd621:	clc
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004fd000, 0x1000, 'rwx')
        mem[0x4fd621] = '\xf8'
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x4fd621

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4fd621, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x4fd622)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CLC_6_symbolic(self):
        ''' Instruction CLC_6
            Groups:
            0x4fadef:	clc
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x004fa000, 0x1000, 'rwx')
        mem[0x4fadef] = '\xf8'
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x4fadef

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4fadef, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x4fadf0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVAE_1_symbolic(self):
        ''' Instruction CMOVAE_1
            Groups: cmov
            0x4117e8:	cmovae	rax, r10
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x4117e8] = 'I'
        mem[0x4117e9] = '\x0f'
        mem[0x4117ea] = 'C'
        mem[0x4117eb] = '\xc2'
        cpu.RIP = 0x4117e8
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x20)
        cpu.R10 = cs.new_bitvec(64)
        cs.add(cpu.R10 == 0x20)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4117e8, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x4117e9, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x4117ea, 8)== ord('C'))
        condition = Operators.AND(condition, cpu.read_int(0x4117eb, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.RAX == 0x20)
        condition = Operators.AND(condition, cpu.RIP == 0x4117ec)
        condition = Operators.AND(condition, cpu.R10 == 0x20)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVAE_2_symbolic(self):
        ''' Instruction CMOVAE_2
            Groups: cmov
            0x414318:	cmovae	rax, r10
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x414318] = 'I'
        mem[0x414319] = '\x0f'
        mem[0x41431a] = 'C'
        mem[0x41431b] = '\xc2'
        cpu.RIP = 0x414318
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x20)
        cpu.R10 = cs.new_bitvec(64)
        cs.add(cpu.R10 == 0x20)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x414318, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x414319, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x41431a, 8)== ord('C'))
        condition = Operators.AND(condition, cpu.read_int(0x41431b, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.RAX == 0x20)
        condition = Operators.AND(condition, cpu.RIP == 0x41431c)
        condition = Operators.AND(condition, cpu.R10 == 0x20)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVAE_3_symbolic(self):
        ''' Instruction CMOVAE_3
            Groups: cmov
            0x5555555662c8:	cmovae	rdx, rbx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555566000, 0x1000, 'rwx')
        mem[0x5555555662c8] = 'H'
        mem[0x5555555662c9] = '\x0f'
        mem[0x5555555662ca] = 'C'
        mem[0x5555555662cb] = '\xd3'
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0xffffffffffffffff)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x5555555662c8
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x7)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x5555555662c8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555662c9, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555662ca, 8)== ord('C'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555662cb, 8)== ord('\xd3'))
        condition = Operators.AND(condition, cpu.RDX == 0x7)
        condition = Operators.AND(condition, cpu.RIP == 0x5555555662cc)
        condition = Operators.AND(condition, cpu.RBX == 0x7)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVAE_4_symbolic(self):
        ''' Instruction CMOVAE_4
            Groups: cmov
            0x411778:	cmovae	rax, r10
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x411778] = 'I'
        mem[0x411779] = '\x0f'
        mem[0x41177a] = 'C'
        mem[0x41177b] = '\xc2'
        cpu.RIP = 0x411778
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x20)
        cpu.R10 = cs.new_bitvec(64)
        cs.add(cpu.R10 == 0x4a0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x411778, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x411779, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x41177a, 8)== ord('C'))
        condition = Operators.AND(condition, cpu.read_int(0x41177b, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.RAX == 0x4a0)
        condition = Operators.AND(condition, cpu.RIP == 0x41177c)
        condition = Operators.AND(condition, cpu.R10 == 0x4a0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVAE_5_symbolic(self):
        ''' Instruction CMOVAE_5
            Groups: cmov
            0x411778:	cmovae	rax, r10
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x411778] = 'I'
        mem[0x411779] = '\x0f'
        mem[0x41177a] = 'C'
        mem[0x41177b] = '\xc2'
        cpu.RIP = 0x411778
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x20)
        cpu.R10 = cs.new_bitvec(64)
        cs.add(cpu.R10 == 0x20)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x411778, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x411779, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x41177a, 8)== ord('C'))
        condition = Operators.AND(condition, cpu.read_int(0x41177b, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.RAX == 0x20)
        condition = Operators.AND(condition, cpu.RIP == 0x41177c)
        condition = Operators.AND(condition, cpu.R10 == 0x20)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVAE_6_symbolic(self):
        ''' Instruction CMOVAE_6
            Groups: cmov
            0x411b58:	cmovae	rax, r10
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00411000, 0x1000, 'rwx')
        mem[0x411b58] = 'I'
        mem[0x411b59] = '\x0f'
        mem[0x411b5a] = 'C'
        mem[0x411b5b] = '\xc2'
        cpu.RIP = 0x411b58
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x20)
        cpu.R10 = cs.new_bitvec(64)
        cs.add(cpu.R10 == 0x50)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x411b58, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x411b59, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x411b5a, 8)== ord('C'))
        condition = Operators.AND(condition, cpu.read_int(0x411b5b, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.RAX == 0x50)
        condition = Operators.AND(condition, cpu.RIP == 0x411b5c)
        condition = Operators.AND(condition, cpu.R10 == 0x50)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVA_1_symbolic(self):
        ''' Instruction CMOVA_1
            Groups: cmov
            0x7ffff7de0ab0:	cmova	rax, r8
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de0000, 0x1000, 'rwx')
        mem[0x7ffff7de0ab0] = 'I'
        mem[0x7ffff7de0ab1] = '\x0f'
        mem[0x7ffff7de0ab2] = 'G'
        mem[0x7ffff7de0ab3] = '\xc0'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7de0ab0
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x7ffff7dd9398)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x7ffff7dd5000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de0ab0, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de0ab1, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de0ab2, 8)== ord('G'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de0ab3, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.R8 == 0x7ffff7dd9398)
        condition = Operators.AND(condition, cpu.RAX == 0x7ffff7dd5000)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de0ab4)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVA_2_symbolic(self):
        ''' Instruction CMOVA_2
            Groups: cmov
            0x7ffff7a9d404:	cmova	rbx, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a9d000, 0x1000, 'rwx')
        mem[0x7ffff7a9d404] = 'H'
        mem[0x7ffff7a9d405] = '\x0f'
        mem[0x7ffff7a9d406] = 'G'
        mem[0x7ffff7a9d407] = '\xd8'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7a9d404
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x7fffffff)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x14)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a9d404, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a9d405, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a9d406, 8)== ord('G'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a9d407, 8)== ord('\xd8'))
        condition = Operators.AND(condition, cpu.RAX == 0x7fffffff)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a9d408)
        condition = Operators.AND(condition, cpu.RBX == 0x14)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVA_3_symbolic(self):
        ''' Instruction CMOVA_3
            Groups: cmov
            0x4082a4:	cmova	rbx, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00408000, 0x1000, 'rwx')
        mem[0x4082a4] = 'H'
        mem[0x4082a5] = '\x0f'
        mem[0x4082a6] = 'G'
        mem[0x4082a7] = '\xd8'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x4082a4
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x7fffffff)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0xb)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4082a4, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x4082a5, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x4082a6, 8)== ord('G'))
        condition = Operators.AND(condition, cpu.read_int(0x4082a7, 8)== ord('\xd8'))
        condition = Operators.AND(condition, cpu.RAX == 0x7fffffff)
        condition = Operators.AND(condition, cpu.RIP == 0x4082a8)
        condition = Operators.AND(condition, cpu.RBX == 0xb)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVA_4_symbolic(self):
        ''' Instruction CMOVA_4
            Groups: cmov
            0x41462a:	cmova	rdx, r13
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x41462a] = 'I'
        mem[0x41462b] = '\x0f'
        mem[0x41462c] = 'G'
        mem[0x41462d] = '\xd5'
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x4a0)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.R13 = cs.new_bitvec(64)
        cs.add(cpu.R13 == 0x21df0)
        cpu.RIP = 0x41462a
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x41462a, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x41462b, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x41462c, 8)== ord('G'))
        condition = Operators.AND(condition, cpu.read_int(0x41462d, 8)== ord('\xd5'))
        condition = Operators.AND(condition, cpu.RDX == 0x4a0)
        condition = Operators.AND(condition, cpu.RIP == 0x41462e)
        condition = Operators.AND(condition, cpu.R13 == 0x21df0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVA_5_symbolic(self):
        ''' Instruction CMOVA_5
            Groups: cmov
            0x41424a:	cmova	rdx, r13
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x41424a] = 'I'
        mem[0x41424b] = '\x0f'
        mem[0x41424c] = 'G'
        mem[0x41424d] = '\xd5'
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x4a0)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.R13 = cs.new_bitvec(64)
        cs.add(cpu.R13 == 0x21df0)
        cpu.RIP = 0x41424a
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x41424a, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x41424b, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x41424c, 8)== ord('G'))
        condition = Operators.AND(condition, cpu.read_int(0x41424d, 8)== ord('\xd5'))
        condition = Operators.AND(condition, cpu.RDX == 0x4a0)
        condition = Operators.AND(condition, cpu.RIP == 0x41424e)
        condition = Operators.AND(condition, cpu.R13 == 0x21df0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVA_6_symbolic(self):
        ''' Instruction CMOVA_6
            Groups: cmov
            0x4142ba:	cmova	rdx, r13
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00414000, 0x1000, 'rwx')
        mem[0x4142ba] = 'I'
        mem[0x4142bb] = '\x0f'
        mem[0x4142bc] = 'G'
        mem[0x4142bd] = '\xd5'
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x4a0)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.R13 = cs.new_bitvec(64)
        cs.add(cpu.R13 == 0x21df0)
        cpu.RIP = 0x4142ba
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4142ba, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x4142bb, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x4142bc, 8)== ord('G'))
        condition = Operators.AND(condition, cpu.read_int(0x4142bd, 8)== ord('\xd5'))
        condition = Operators.AND(condition, cpu.RDX == 0x4a0)
        condition = Operators.AND(condition, cpu.RIP == 0x4142be)
        condition = Operators.AND(condition, cpu.R13 == 0x21df0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVBE_1_symbolic(self):
        ''' Instruction CMOVBE_1
            Groups: cmov
            0x40d233:	cmovbe	rbx, r14
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040d000, 0x1000, 'rwx')
        mem[0x40d233] = 'I'
        mem[0x40d234] = '\x0f'
        mem[0x40d235] = 'F'
        mem[0x40d236] = '\xde'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x1000)
        cpu.R14 = cs.new_bitvec(64)
        cs.add(cpu.R14 == 0x20)
        cpu.RIP = 0x40d233
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x40d233, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x40d234, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x40d235, 8)== ord('F'))
        condition = Operators.AND(condition, cpu.read_int(0x40d236, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.R14 == 0x20)
        condition = Operators.AND(condition, cpu.RIP == 0x40d237)
        condition = Operators.AND(condition, cpu.RBX == 0x20)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVBE_2_symbolic(self):
        ''' Instruction CMOVBE_2
            Groups: cmov
            0x7ffff7aa96b3:	cmovbe	rbx, r14
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa9000, 0x1000, 'rwx')
        mem[0x7ffff7aa96b3] = 'I'
        mem[0x7ffff7aa96b4] = '\x0f'
        mem[0x7ffff7aa96b5] = 'F'
        mem[0x7ffff7aa96b6] = '\xde'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x2000)
        cpu.R14 = cs.new_bitvec(64)
        cs.add(cpu.R14 == 0x4)
        cpu.RIP = 0x7ffff7aa96b3
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b3, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b4, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b5, 8)== ord('F'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b6, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.R14 == 0x4)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7aa96b7)
        condition = Operators.AND(condition, cpu.RBX == 0x4)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVBE_3_symbolic(self):
        ''' Instruction CMOVBE_3
            Groups: cmov
            0x7ffff7aa96b3:	cmovbe	rbx, r14
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa9000, 0x1000, 'rwx')
        mem[0x7ffff7aa96b3] = 'I'
        mem[0x7ffff7aa96b4] = '\x0f'
        mem[0x7ffff7aa96b5] = 'F'
        mem[0x7ffff7aa96b6] = '\xde'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x1000)
        cpu.R14 = cs.new_bitvec(64)
        cs.add(cpu.R14 == 0x13)
        cpu.RIP = 0x7ffff7aa96b3
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b3, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b4, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b5, 8)== ord('F'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b6, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.R14 == 0x13)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7aa96b7)
        condition = Operators.AND(condition, cpu.RBX == 0x13)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVBE_4_symbolic(self):
        ''' Instruction CMOVBE_4
            Groups: cmov
            0x40d263:	cmovbe	rbx, r14
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040d000, 0x1000, 'rwx')
        mem[0x40d263] = 'I'
        mem[0x40d264] = '\x0f'
        mem[0x40d265] = 'F'
        mem[0x40d266] = '\xde'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x1000)
        cpu.R14 = cs.new_bitvec(64)
        cs.add(cpu.R14 == 0x13)
        cpu.RIP = 0x40d263
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x40d263, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x40d264, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x40d265, 8)== ord('F'))
        condition = Operators.AND(condition, cpu.read_int(0x40d266, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.R14 == 0x13)
        condition = Operators.AND(condition, cpu.RIP == 0x40d267)
        condition = Operators.AND(condition, cpu.RBX == 0x13)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVBE_5_symbolic(self):
        ''' Instruction CMOVBE_5
            Groups: cmov
            0x7ffff7aa96b3:	cmovbe	rbx, r14
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aa9000, 0x1000, 'rwx')
        mem[0x7ffff7aa96b3] = 'I'
        mem[0x7ffff7aa96b4] = '\x0f'
        mem[0x7ffff7aa96b5] = 'F'
        mem[0x7ffff7aa96b6] = '\xde'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x1000)
        cpu.R14 = cs.new_bitvec(64)
        cs.add(cpu.R14 == 0x13)
        cpu.RIP = 0x7ffff7aa96b3
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b3, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b4, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b5, 8)== ord('F'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aa96b6, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.R14 == 0x13)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7aa96b7)
        condition = Operators.AND(condition, cpu.RBX == 0x13)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVBE_6_symbolic(self):
        ''' Instruction CMOVBE_6
            Groups: cmov
            0x40fde3:	cmovbe	rbx, r14
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040f000, 0x1000, 'rwx')
        mem[0x40fde3] = 'I'
        mem[0x40fde4] = '\x0f'
        mem[0x40fde5] = 'F'
        mem[0x40fde6] = '\xde'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x1000)
        cpu.R14 = cs.new_bitvec(64)
        cs.add(cpu.R14 == 0x240)
        cpu.RIP = 0x40fde3
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x40fde3, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x40fde4, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x40fde5, 8)== ord('F'))
        condition = Operators.AND(condition, cpu.read_int(0x40fde6, 8)== ord('\xde'))
        condition = Operators.AND(condition, cpu.R14 == 0x240)
        condition = Operators.AND(condition, cpu.RIP == 0x40fde7)
        condition = Operators.AND(condition, cpu.RBX == 0x240)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVB_1_symbolic(self):
        ''' Instruction CMOVB_1
            Groups: cmov
            0x7ffff7deb97f:	cmovb	r12d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7deb000, 0x1000, 'rwx')
        mem[0x7ffff7deb980] = '\x0f'
        mem[0x7ffff7deb981] = 'B'
        mem[0x7ffff7deb982] = '\xe0'
        mem[0x7ffff7deb97f] = 'D'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0xa)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7deb97f
        cpu.R12D = cs.new_bitvec(32)
        cs.add(cpu.R12D == 0x1a)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb980, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb981, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb982, 8)== ord('\xe0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb97f, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.EAX == 0xa)
        condition = Operators.AND(condition, cpu.R12D == 0x1a)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7deb983)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVB_2_symbolic(self):
        ''' Instruction CMOVB_2
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == True)
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0xffffffff)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ad, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ae, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45af, 8)== ord('\xc1'))
        condition = Operators.AND(condition, cpu.EAX == 0xffffffff)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df45b0)
        condition = Operators.AND(condition, cpu.ECX == 0xffffffff)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVB_3_symbolic(self):
        ''' Instruction CMOVB_3
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0xffffffff)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ad, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ae, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45af, 8)== ord('\xc1'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df45b0)
        condition = Operators.AND(condition, cpu.ECX == 0xffffffff)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVB_4_symbolic(self):
        ''' Instruction CMOVB_4
            Groups: cmov
            0x7ffff7deb97f:	cmovb	r12d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7deb000, 0x1000, 'rwx')
        mem[0x7ffff7deb980] = '\x0f'
        mem[0x7ffff7deb981] = 'B'
        mem[0x7ffff7deb982] = '\xe0'
        mem[0x7ffff7deb97f] = 'D'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x12)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7deb97f
        cpu.R12D = cs.new_bitvec(32)
        cs.add(cpu.R12D == 0x1a)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb980, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb981, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb982, 8)== ord('\xe0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7deb97f, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.EAX == 0x12)
        condition = Operators.AND(condition, cpu.R12D == 0x1a)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7deb983)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVB_5_symbolic(self):
        ''' Instruction CMOVB_5
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0xffffffff)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ad, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ae, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45af, 8)== ord('\xc1'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df45b0)
        condition = Operators.AND(condition, cpu.ECX == 0xffffffff)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVB_6_symbolic(self):
        ''' Instruction CMOVB_6
            Groups: cmov
            0x7ffff7df45ad:	cmovb	eax, ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df45ad] = '\x0f'
        mem[0x7ffff7df45ae] = 'B'
        mem[0x7ffff7df45af] = '\xc1'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7df45ad
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0xffffffff)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ad, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45ae, 8)== ord('B'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df45af, 8)== ord('\xc1'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df45b0)
        condition = Operators.AND(condition, cpu.ECX == 0xffffffff)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVE_1_symbolic(self):
        ''' Instruction CMOVE_1
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x7ffff7ff7c48)
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6260, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6261, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625e, 8)== ord('L'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625f, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.R8 == 0x7ffff7ff7c48)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de6262)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVE_2_symbolic(self):
        ''' Instruction CMOVE_2
            Groups: cmov
            0x415f05:	cmove	rax, rdx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00415000, 0x1000, 'rwx')
        mem[0x415f08] = '\xc2'
        mem[0x415f05] = 'H'
        mem[0x415f06] = '\x0f'
        mem[0x415f07] = 'D'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x415f05
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x6e01c0)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x415f08, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.read_int(0x415f05, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x415f06, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x415f07, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.RAX == 0x6e01c0)
        condition = Operators.AND(condition, cpu.RIP == 0x415f09)
        condition = Operators.AND(condition, cpu.RDX == 0x0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVE_3_symbolic(self):
        ''' Instruction CMOVE_3
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x7ffff7ff7c48)
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6260, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6261, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625e, 8)== ord('L'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625f, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.R8 == 0x7ffff7ff7c48)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de6262)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVE_4_symbolic(self):
        ''' Instruction CMOVE_4
            Groups: cmov
            0x7ffff7df2822:	cmove	rdi, qword ptr [rip + 0x20b886]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df2000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7ffe000, 0x1000, 'rwx')
        mem[0x7ffff7df2822] = 'H'
        mem[0x7ffff7df2823] = '\x0f'
        mem[0x7ffff7df2824] = 'D'
        mem[0x7ffff7df2825] = '='
        mem[0x7ffff7df2826] = '\x86'
        mem[0x7ffff7df2827] = '\xb8'
        mem[0x7ffff7df2828] = ' '
        mem[0x7ffff7df2829] = '\x00'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b0)
        value = cs.new_bitvec(8)
        cs.add(value == 0x30)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b1)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b2)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b3)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b4)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7ffe0b7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x7ffff7fd8000)
        cpu.RIP = 0x7ffff7df2822

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2822, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2823, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2824, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2825, 8)== ord('='))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2826, 8)== ord('\x86'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2827, 8)== ord('\xb8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2828, 8)== ord(' '))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df2829, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b0, 8)== ord('0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b1, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b2, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b3, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b4, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b5, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7ffe0b7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RDI == 0x7ffff7fd8000)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df282a)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVE_5_symbolic(self):
        ''' Instruction CMOVE_5
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x7ffff7ff7c48)
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6260, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6261, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625e, 8)== ord('L'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625f, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.R8 == 0x7ffff7ff7c48)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de6262)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVE_6_symbolic(self):
        ''' Instruction CMOVE_6
            Groups: cmov
            0x7ffff7de625e:	cmove	r8, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6260] = 'D'
        mem[0x7ffff7de6261] = '\xc0'
        mem[0x7ffff7de625e] = 'L'
        mem[0x7ffff7de625f] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x7ffff7ff7c48)
        cpu.RIP = 0x7ffff7de625e
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6260, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6261, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625e, 8)== ord('L'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de625f, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.R8 == 0x7ffff7ff7c48)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de6262)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNE_1_symbolic(self):
        ''' Instruction CMOVNE_1
            Groups: cmov
            0x462435:	cmovne	rbx, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00462000, 0x1000, 'rwx')
        mem[0x462438] = '\xd8'
        mem[0x462435] = 'H'
        mem[0x462436] = '\x0f'
        mem[0x462437] = 'E'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RIP = 0x462435
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x4a5441)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x6bf6b0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x462438, 8)== ord('\xd8'))
        condition = Operators.AND(condition, cpu.read_int(0x462435, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x462436, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x462437, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.RAX == 0x4a5441)
        condition = Operators.AND(condition, cpu.RIP == 0x462439)
        condition = Operators.AND(condition, cpu.RBX == 0x6bf6b0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNE_2_symbolic(self):
        ''' Instruction CMOVNE_2
            Groups: cmov
            0x7ffff7de5776:	cmovne	r14d, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de5778] = 'E'
        mem[0x7ffff7de5779] = '\xf0'
        mem[0x7ffff7de5776] = 'D'
        mem[0x7ffff7de5777] = '\x0f'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x10)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.R14D = cs.new_bitvec(32)
        cs.add(cpu.R14D == 0x0)
        cpu.RIP = 0x7ffff7de5776

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de5778, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de5779, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de5776, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de5777, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.EAX == 0x10)
        condition = Operators.AND(condition, cpu.R14D == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de577a)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNE_3_symbolic(self):
        ''' Instruction CMOVNE_3
            Groups: cmov
            0x7ffff7de57f6:	cmovne	rbx, rax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de5000, 0x1000, 'rwx')
        mem[0x7ffff7de57f8] = 'E'
        mem[0x7ffff7de57f9] = '\xd8'
        mem[0x7ffff7de57f6] = 'H'
        mem[0x7ffff7de57f7] = '\x0f'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7de57f6
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x7ffff7ff7640)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x7ffff7ff7af1)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de57f8, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de57f9, 8)== ord('\xd8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de57f6, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de57f7, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.RAX == 0x7ffff7ff7640)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de57fa)
        condition = Operators.AND(condition, cpu.RBX == 0x7ffff7ff7640)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNE_4_symbolic(self):
        ''' Instruction CMOVNE_4
            Groups: cmov
            0x457ba4:	cmovne	rsi, rdx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x457ba4] = 'H'
        mem[0x457ba5] = '\x0f'
        mem[0x457ba6] = 'E'
        mem[0x457ba7] = '\xf2'
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x8201000080201021)
        cpu.RIP = 0x457ba4
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x41008000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x457ba4, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x457ba5, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x457ba6, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.read_int(0x457ba7, 8)== ord('\xf2'))
        condition = Operators.AND(condition, cpu.RSI == 0x41008000)
        condition = Operators.AND(condition, cpu.RIP == 0x457ba8)
        condition = Operators.AND(condition, cpu.RDX == 0x41008000)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNE_5_symbolic(self):
        ''' Instruction CMOVNE_5
            Groups: cmov
            0x7ffff7de0910:	cmovne	esi, eax
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de0000, 0x1000, 'rwx')
        mem[0x7ffff7de0910] = '\x0f'
        mem[0x7ffff7de0911] = 'E'
        mem[0x7ffff7de0912] = '\xf0'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7de0910
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de0910, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de0911, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de0912, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.ESI == 0x1)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de0913)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNE_6_symbolic(self):
        ''' Instruction CMOVNE_6
            Groups: cmov
            0x457db0:	cmovne	rcx, rdi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00457000, 0x1000, 'rwx')
        mem[0x457db0] = 'H'
        mem[0x457db1] = '\x0f'
        mem[0x457db2] = 'E'
        mem[0x457db3] = '\xcf'
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x7fffffffe01b)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x7fffffffe040)
        cpu.RIP = 0x457db0

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x457db0, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x457db1, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x457db2, 8)== ord('E'))
        condition = Operators.AND(condition, cpu.read_int(0x457db3, 8)== ord('\xcf'))
        condition = Operators.AND(condition, cpu.RDI == 0x7fffffffe040)
        condition = Operators.AND(condition, cpu.RCX == 0x7fffffffe040)
        condition = Operators.AND(condition, cpu.RIP == 0x457db4)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNS_1_symbolic(self):
        ''' Instruction CMOVNS_1
            Groups: cmov
            0x448555:	cmovns	rax, r11
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00448000, 0x1000, 'rwx')
        mem[0x448558] = '\xc3'
        mem[0x448555] = 'I'
        mem[0x448556] = '\x0f'
        mem[0x448557] = 'I'
        cpu.RIP = 0x448555
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.R11 = cs.new_bitvec(64)
        cs.add(cpu.R11 == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x448558, 8)== ord('\xc3'))
        condition = Operators.AND(condition, cpu.read_int(0x448555, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x448556, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x448557, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x448559)
        condition = Operators.AND(condition, cpu.R11 == 0x0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMOVNS_2_symbolic(self):
        ''' Instruction CMOVNS_2
            Groups: cmov
            0x448555:	cmovns	rax, r11
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00448000, 0x1000, 'rwx')
        mem[0x448558] = '\xc3'
        mem[0x448555] = 'I'
        mem[0x448556] = '\x0f'
        mem[0x448557] = 'I'
        cpu.RIP = 0x448555
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.R11 = cs.new_bitvec(64)
        cs.add(cpu.R11 == 0x0)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x448558, 8)== ord('\xc3'))
        condition = Operators.AND(condition, cpu.read_int(0x448555, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x448556, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x448557, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x448559)
        condition = Operators.AND(condition, cpu.R11 == 0x0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPSB_1_symbolic(self):
        ''' Instruction CMPSB_1
            Groups:
            0x40065b:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda80)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda81)
        value = cs.new_bitvec(8)
        cs.add(value == 0xed)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda82)
        value = cs.new_bitvec(8)
        cs.add(value == 0xcf)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda83)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc2)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491604)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491605)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491606)
        value = cs.new_bitvec(8)
        cs.add(value == 0x52)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491607)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491608)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491609)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49160a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49160b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4d)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda87)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda86)
        value = cs.new_bitvec(8)
        cs.add(value == 0x94)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda84)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc0)
        mem[addr] = value
        mem[0x40065b] = '\xf3'
        mem[0x40065c] = '\xa6'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda85)
        value = cs.new_bitvec(8)
        cs.add(value == 0xe0)
        mem[addr] = value
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x491604)
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x7)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x7fffffffda80)
        cpu.RIP = 0x40065b

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda80, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda81, 8)== ord('\xed'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda82, 8)== ord('\xcf'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda83, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.read_int(0x491604, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x491605, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x491606, 8)== ord('R'))
        condition = Operators.AND(condition, cpu.read_int(0x491607, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x491608, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x491609, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x49160a, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x49160b, 8)== ord('M'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda87, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda86, 8)== ord('\x94'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda84, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x40065b, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x40065c, 8)== ord('\xa6'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda85, 8)== ord('\xe0'))
        condition = Operators.AND(condition, cpu.RCX == 0x6)
        condition = Operators.AND(condition, cpu.RDI == 0x491605)
        condition = Operators.AND(condition, cpu.RSI == 0x7fffffffda81)
        condition = Operators.AND(condition, cpu.RIP == 0x40065b)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPSB_2_symbolic(self):
        ''' Instruction CMPSB_2
            Groups:
            0x400657:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        mem[0x400658] = '\xa6'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x61)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x72)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06c)
        value = cs.new_bitvec(8)
        cs.add(value == 0x67)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x31)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06f)
        value = cs.new_bitvec(8)
        cs.add(value == 0x61)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe070)
        value = cs.new_bitvec(8)
        cs.add(value == 0x72)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe071)
        value = cs.new_bitvec(8)
        cs.add(value == 0x67)
        mem[addr] = value
        mem[0x400657] = '\xf3'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491818)
        value = cs.new_bitvec(8)
        cs.add(value == 0x2d)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491819)
        value = cs.new_bitvec(8)
        cs.add(value == 0x64)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x6f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x73)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181c)
        value = cs.new_bitvec(8)
        cs.add(value == 0x74)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x75)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x66)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491817)
        value = cs.new_bitvec(8)
        cs.add(value == 0x2d)
        mem[addr] = value
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x491817)
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0xa)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x7fffffffe06a)
        cpu.RIP = 0x400657

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06b, 8)== ord('r'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe071, 8)== ord('g'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06a, 8)== ord('a'))
        condition = Operators.AND(condition, cpu.read_int(0x400657, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06c, 8)== ord('g'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06d, 8)== ord('1'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06f, 8)== ord('a'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe070, 8)== ord('r'))
        condition = Operators.AND(condition, cpu.read_int(0x491818, 8)== ord('-'))
        condition = Operators.AND(condition, cpu.read_int(0x491817, 8)== ord('-'))
        condition = Operators.AND(condition, cpu.read_int(0x400658, 8)== ord('\xa6'))
        condition = Operators.AND(condition, cpu.read_int(0x491819, 8)== ord('d'))
        condition = Operators.AND(condition, cpu.read_int(0x49181a, 8)== ord('o'))
        condition = Operators.AND(condition, cpu.read_int(0x49181b, 8)== ord('s'))
        condition = Operators.AND(condition, cpu.read_int(0x49181c, 8)== ord('t'))
        condition = Operators.AND(condition, cpu.read_int(0x49181d, 8)== ord('u'))
        condition = Operators.AND(condition, cpu.read_int(0x49181e, 8)== ord('f'))
        condition = Operators.AND(condition, cpu.RCX == 0x9)
        condition = Operators.AND(condition, cpu.RDI == 0x491818)
        condition = Operators.AND(condition, cpu.RSI == 0x7fffffffe06b)
        condition = Operators.AND(condition, cpu.RIP == 0x400659)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPSB_3_symbolic(self):
        ''' Instruction CMPSB_3
            Groups:
            0x40065b:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda81)
        value = cs.new_bitvec(8)
        cs.add(value == 0xed)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda82)
        value = cs.new_bitvec(8)
        cs.add(value == 0xcf)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda83)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc2)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda84)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491605)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491606)
        value = cs.new_bitvec(8)
        cs.add(value == 0x52)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491607)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491608)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491609)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49160a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49160b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4d)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49160c)
        value = cs.new_bitvec(8)
        cs.add(value == 0x65)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda86)
        value = cs.new_bitvec(8)
        cs.add(value == 0x94)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda88)
        value = cs.new_bitvec(8)
        cs.add(value == 0xea)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda87)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        mem[0x40065b] = '\xf3'
        mem[0x40065c] = '\xa6'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda85)
        value = cs.new_bitvec(8)
        cs.add(value == 0xe0)
        mem[addr] = value
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x491605)
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x6)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x7fffffffda81)
        cpu.RIP = 0x40065b

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda81, 8)== ord('\xed'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda82, 8)== ord('\xcf'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda83, 8)== ord('\xc2'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda84, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x491605, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x491606, 8)== ord('R'))
        condition = Operators.AND(condition, cpu.read_int(0x491607, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x491608, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x491609, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x49160a, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x49160b, 8)== ord('M'))
        condition = Operators.AND(condition, cpu.read_int(0x49160c, 8)== ord('e'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda86, 8)== ord('\x94'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda88, 8)== ord('\xea'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda87, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x40065b, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x40065c, 8)== ord('\xa6'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda85, 8)== ord('\xe0'))
        condition = Operators.AND(condition, cpu.RCX == 0x5)
        condition = Operators.AND(condition, cpu.RDI == 0x491606)
        condition = Operators.AND(condition, cpu.RSI == 0x7fffffffda82)
        condition = Operators.AND(condition, cpu.RIP == 0x40065d)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPSB_4_symbolic(self):
        ''' Instruction CMPSB_4
            Groups:
            0x400657:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem.mmap(0x00491000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe065)
        value = cs.new_bitvec(8)
        cs.add(value == 0x61)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe066)
        value = cs.new_bitvec(8)
        cs.add(value == 0x72)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe067)
        value = cs.new_bitvec(8)
        cs.add(value == 0x67)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe068)
        value = cs.new_bitvec(8)
        cs.add(value == 0x31)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe069)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x61)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x72)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffe06c)
        value = cs.new_bitvec(8)
        cs.add(value == 0x67)
        mem[addr] = value
        mem[0x400658] = '\xa6'
        mem[0x400657] = '\xf3'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491818)
        value = cs.new_bitvec(8)
        cs.add(value == 0x2d)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491819)
        value = cs.new_bitvec(8)
        cs.add(value == 0x64)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x6f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x73)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181c)
        value = cs.new_bitvec(8)
        cs.add(value == 0x74)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x75)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x49181e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x66)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x491817)
        value = cs.new_bitvec(8)
        cs.add(value == 0x2d)
        mem[addr] = value
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x491817)
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0xa)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x7fffffffe065)
        cpu.RIP = 0x400657

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06b, 8)== ord('r'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe065, 8)== ord('a'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe066, 8)== ord('r'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe067, 8)== ord('g'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe068, 8)== ord('1'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe069, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06a, 8)== ord('a'))
        condition = Operators.AND(condition, cpu.read_int(0x400657, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffe06c, 8)== ord('g'))
        condition = Operators.AND(condition, cpu.read_int(0x491818, 8)== ord('-'))
        condition = Operators.AND(condition, cpu.read_int(0x491817, 8)== ord('-'))
        condition = Operators.AND(condition, cpu.read_int(0x400658, 8)== ord('\xa6'))
        condition = Operators.AND(condition, cpu.read_int(0x491819, 8)== ord('d'))
        condition = Operators.AND(condition, cpu.read_int(0x49181a, 8)== ord('o'))
        condition = Operators.AND(condition, cpu.read_int(0x49181b, 8)== ord('s'))
        condition = Operators.AND(condition, cpu.read_int(0x49181c, 8)== ord('t'))
        condition = Operators.AND(condition, cpu.read_int(0x49181d, 8)== ord('u'))
        condition = Operators.AND(condition, cpu.read_int(0x49181e, 8)== ord('f'))
        condition = Operators.AND(condition, cpu.RCX == 0x9)
        condition = Operators.AND(condition, cpu.RDI == 0x491818)
        condition = Operators.AND(condition, cpu.RSI == 0x7fffffffe066)
        condition = Operators.AND(condition, cpu.RIP == 0x400659)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPSB_5_symbolic(self):
        ''' Instruction CMPSB_5
            Groups:
            0x55555555478b:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda80)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc6)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda81)
        value = cs.new_bitvec(8)
        cs.add(value == 0xd9)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda82)
        value = cs.new_bitvec(8)
        cs.add(value == 0x50)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda83)
        value = cs.new_bitvec(8)
        cs.add(value == 0x25)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda84)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc1)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda85)
        value = cs.new_bitvec(8)
        cs.add(value == 0xe2)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda86)
        value = cs.new_bitvec(8)
        cs.add(value == 0xc9)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda87)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        mem[0x55555555478b] = '\xf3'
        mem[0x55555555478c] = '\xa6'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x555555554998)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x555555554999)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x55555555499a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x52)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x55555555499b)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x55555555499c)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x55555555499d)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x55555555499e)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x55555555499f)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4d)
        mem[addr] = value
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x555555554998)
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x7)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x7fffffffda80)
        cpu.RIP = 0x55555555478b

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda80, 8)== ord('\xc6'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda81, 8)== ord('\xd9'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda82, 8)== ord('P'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda83, 8)== ord('%'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda84, 8)== ord('\xc1'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda85, 8)== ord('\xe2'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda86, 8)== ord('\xc9'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda87, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555478b, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555478c, 8)== ord('\xa6'))
        condition = Operators.AND(condition, cpu.read_int(0x555555554998, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x555555554999, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555499a, 8)== ord('R'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555499b, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555499c, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555499d, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555499e, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x55555555499f, 8)== ord('M'))
        condition = Operators.AND(condition, cpu.RCX == 0x6)
        condition = Operators.AND(condition, cpu.RDI == 0x555555554999)
        condition = Operators.AND(condition, cpu.RSI == 0x7fffffffda81)
        condition = Operators.AND(condition, cpu.RIP == 0x55555555478d)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPSB_6_symbolic(self):
        ''' Instruction CMPSB_6
            Groups:
            0x5555555548c0:	repe cmpsb	byte ptr [rsi], byte ptr [rdi]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x555555554000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        mem[0x5555555548c0] = '\xf3'
        mem[0x5555555548c1] = '\xa6'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda82)
        value = cs.new_bitvec(8)
        cs.add(value == 0xd2)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda83)
        value = cs.new_bitvec(8)
        cs.add(value == 0xd0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda84)
        value = cs.new_bitvec(8)
        cs.add(value == 0x1f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda85)
        value = cs.new_bitvec(8)
        cs.add(value == 0x1c)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda86)
        value = cs.new_bitvec(8)
        cs.add(value == 0x28)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda81)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549a8)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549a9)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549aa)
        value = cs.new_bitvec(8)
        cs.add(value == 0x52)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549ab)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549ac)
        value = cs.new_bitvec(8)
        cs.add(value == 0x5a)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549ad)
        value = cs.new_bitvec(8)
        cs.add(value == 0x41)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549ae)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x5555555549af)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4d)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda87)
        value = cs.new_bitvec(8)
        cs.add(value == 0x50)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffda80)
        value = cs.new_bitvec(8)
        cs.add(value == 0x91)
        mem[addr] = value
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x5555555549a8)
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x7)
        cpu.RSI = cs.new_bitvec(64)
        cs.add(cpu.RSI == 0x7fffffffda80)
        cpu.RIP = 0x5555555548c0

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x5555555548c0, 8)== ord('\xf3'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555548c1, 8)== ord('\xa6'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda82, 8)== ord('\xd2'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda83, 8)== ord('\xd0'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda84, 8)== ord('\x1f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda85, 8)== ord('\x1c'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda86, 8)== ord('('))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda81, 8)== ord('\x04'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549a8, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549a9, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549aa, 8)== ord('R'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda87, 8)== ord('P'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549ac, 8)== ord('Z'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549ad, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549ae, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549af, 8)== ord('M'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffda80, 8)== ord('\x91'))
        condition = Operators.AND(condition, cpu.read_int(0x5555555549ab, 8)== ord('A'))
        condition = Operators.AND(condition, cpu.RCX == 0x6)
        condition = Operators.AND(condition, cpu.RDI == 0x5555555549a9)
        condition = Operators.AND(condition, cpu.RSI == 0x7fffffffda81)
        condition = Operators.AND(condition, cpu.RIP == 0x5555555548c2)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG8B_1_symbolic(self):
        ''' Instruction CMPXCHG8B_1
            Groups:
            0x5c68cb:	lock cmpxchg8b	qword ptr [rsp + 4]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x005c6000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x5c68cb] = '\xf0'
        mem[0x5c68cc] = '\x0f'
        mem[0x5c68cd] = '\xc7'
        mem[0x5c68ce] = 'L'
        mem[0x5c68cf] = '$'
        mem[0x5c68d0] = '\x04'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb4)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb8)
        value = cs.new_bitvec(8)
        cs.add(value == 0x1)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb9)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccba)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccbb)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.EBX = cs.new_bitvec(32)
        cs.add(cpu.EBX == 0x80000001)
        cpu.RIP = 0x5c68cb
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x80000001)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x8001)
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffccb0)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x80)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x5c68cb, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x5c68cc, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x5c68cd, 8)== ord('\xc7'))
        condition = Operators.AND(condition, cpu.read_int(0x5c68ce, 8)== ord('L'))
        condition = Operators.AND(condition, cpu.read_int(0x5c68cf, 8)== ord('$'))
        condition = Operators.AND(condition, cpu.read_int(0x5c68d0, 8)== ord('\x04'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb4, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb5, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb8, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb9, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccba, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccbb, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffccb0)
        condition = Operators.AND(condition, cpu.RIP == 0x5c68d1)
        condition = Operators.AND(condition, cpu.EAX == 0x80)
        condition = Operators.AND(condition, cpu.EDX == 0x8001)
        condition = Operators.AND(condition, cpu.EBX == 0x80000001)
        condition = Operators.AND(condition, cpu.ECX == 0x80)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG8B_2_symbolic(self):
        ''' Instruction CMPXCHG8B_2
            Groups:
            0x5861a9:	lock cmpxchg8b	qword ptr [rsp]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00586000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x5861a9] = '\xf0'
        mem[0x5861aa] = '\x0f'
        mem[0x5861ab] = '\xc7'
        mem[0x5861ac] = '\x0c'
        mem[0x5861ad] = '$'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb0)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb1)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb2)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb3)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb4)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        cpu.EBX = cs.new_bitvec(32)
        cs.add(cpu.EBX == 0x80000000)
        cpu.RIP = 0x5861a9
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x80000000)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0xffffffff)
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffccb0)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x80000000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x5861a9, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x5861aa, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x5861ab, 8)== ord('\xc7'))
        condition = Operators.AND(condition, cpu.read_int(0x5861ac, 8)== ord('\x0c'))
        condition = Operators.AND(condition, cpu.read_int(0x5861ad, 8)== ord('$'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb0, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb1, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb2, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb3, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb4, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb5, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb7, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffccb0)
        condition = Operators.AND(condition, cpu.RIP == 0x5861ae)
        condition = Operators.AND(condition, cpu.EAX == 0x80000000)
        condition = Operators.AND(condition, cpu.EDX == 0x80000000)
        condition = Operators.AND(condition, cpu.EBX == 0x80000000)
        condition = Operators.AND(condition, cpu.ECX == 0x80000000)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG8B_3_symbolic(self):
        ''' Instruction CMPXCHG8B_3
            Groups:
            0x58de05:	lock cmpxchg8b	qword ptr [rsp]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0058d000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x58de05] = '\xf0'
        mem[0x58de06] = '\x0f'
        mem[0x58de07] = '\xc7'
        mem[0x58de08] = '\x0c'
        mem[0x58de09] = '$'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb0)
        value = cs.new_bitvec(8)
        cs.add(value == 0x1)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb1)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb2)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb3)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb4)
        value = cs.new_bitvec(8)
        cs.add(value == 0x40)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.EBX = cs.new_bitvec(32)
        cs.add(cpu.EBX == 0x80000001)
        cpu.RIP = 0x58de05
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x80000001)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x21)
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffccb0)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x40)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x58de05, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x58de06, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x58de07, 8)== ord('\xc7'))
        condition = Operators.AND(condition, cpu.read_int(0x58de08, 8)== ord('\x0c'))
        condition = Operators.AND(condition, cpu.read_int(0x58de09, 8)== ord('$'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb0, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb1, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb2, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb3, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb4, 8)== ord('@'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb5, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffccb0)
        condition = Operators.AND(condition, cpu.RIP == 0x58de0a)
        condition = Operators.AND(condition, cpu.EAX == 0x80000001)
        condition = Operators.AND(condition, cpu.EDX == 0x40)
        condition = Operators.AND(condition, cpu.EBX == 0x80000001)
        condition = Operators.AND(condition, cpu.ECX == 0x40)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG8B_4_symbolic(self):
        ''' Instruction CMPXCHG8B_4
            Groups:
            0x59b473:	lock cmpxchg8b	qword ptr [rsp]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0059b000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x59b476] = '\x0c'
        mem[0x59b477] = '$'
        mem[0x59b473] = '\xf0'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb0)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb1)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb2)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb3)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        mem[0x59b474] = '\x0f'
        mem[0x59b475] = '\xc7'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb4)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.EBX = cs.new_bitvec(32)
        cs.add(cpu.EBX == 0xffffffff)
        cpu.RIP = 0x59b473
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0xffffffff)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x80)
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffccb0)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x80)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb3, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb0, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb1, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb2, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x59b473, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x59b474, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x59b475, 8)== ord('\xc7'))
        condition = Operators.AND(condition, cpu.read_int(0x59b476, 8)== ord('\x0c'))
        condition = Operators.AND(condition, cpu.read_int(0x59b477, 8)== ord('$'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb4, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb5, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffccb0)
        condition = Operators.AND(condition, cpu.RIP == 0x59b478)
        condition = Operators.AND(condition, cpu.EAX == 0xffffffff)
        condition = Operators.AND(condition, cpu.EDX == 0x80)
        condition = Operators.AND(condition, cpu.EBX == 0xffffffff)
        condition = Operators.AND(condition, cpu.ECX == 0x80)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG8B_5_symbolic(self):
        ''' Instruction CMPXCHG8B_5
            Groups:
            0x624e14:	lock cmpxchg8b	qword ptr [rsp + 8]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00624000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        mem[0x624e14] = '\xf0'
        mem[0x624e15] = '\x0f'
        mem[0x624e16] = '\xc7'
        mem[0x624e17] = 'L'
        mem[0x624e18] = '$'
        mem[0x624e19] = '\x08'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb8)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb9)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccba)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccbb)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccbc)
        value = cs.new_bitvec(8)
        cs.add(value == 0x40)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccbd)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccbe)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccbf)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        cpu.EBX = cs.new_bitvec(32)
        cs.add(cpu.EBX == 0x40)
        cpu.RIP = 0x624e14
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x40)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x80000000)
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffccb0)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x8001)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x624e14, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x624e15, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x624e16, 8)== ord('\xc7'))
        condition = Operators.AND(condition, cpu.read_int(0x624e17, 8)== ord('L'))
        condition = Operators.AND(condition, cpu.read_int(0x624e18, 8)== ord('$'))
        condition = Operators.AND(condition, cpu.read_int(0x624e19, 8)== ord('\x08'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb8, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb9, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccba, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccbb, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccbc, 8)== ord('@'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccbd, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccbe, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccbf, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffccb0)
        condition = Operators.AND(condition, cpu.RIP == 0x624e1a)
        condition = Operators.AND(condition, cpu.EAX == 0x80000000)
        condition = Operators.AND(condition, cpu.EDX == 0x40)
        condition = Operators.AND(condition, cpu.EBX == 0x40)
        condition = Operators.AND(condition, cpu.ECX == 0x8001)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG8B_6_symbolic(self):
        ''' Instruction CMPXCHG8B_6
            Groups:
            0x5bfa73:	lock cmpxchg8b	qword ptr [rsp + 4]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x005bf000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffc000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb4)
        value = cs.new_bitvec(8)
        cs.add(value == 0x1)
        mem[addr] = value
        mem[0x5bfa76] = 'L'
        mem[0x5bfa77] = '$'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb8)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        mem[0x5bfa73] = '\xf0'
        mem[0x5bfa74] = '\x0f'
        mem[0x5bfa75] = '\xc7'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x5bfa78] = '\x04'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb9)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccba)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccbb)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffccb5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x80)
        mem[addr] = value
        cpu.EBX = cs.new_bitvec(32)
        cs.add(cpu.EBX == 0x80000000)
        cpu.RIP = 0x5bfa73
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x80000000)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x7f)
        cpu.RSP = cs.new_bitvec(64)
        cs.add(cpu.RSP == 0x7fffffffccb0)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x8001)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x5bfa78, 8)== ord('\x04'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb9, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x5bfa73, 8)== ord('\xf0'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb4, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x5bfa75, 8)== ord('\xc7'))
        condition = Operators.AND(condition, cpu.read_int(0x5bfa76, 8)== ord('L'))
        condition = Operators.AND(condition, cpu.read_int(0x5bfa77, 8)== ord('$'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb8, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x5bfa74, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccba, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccbb, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffccb5, 8)== ord('\x80'))
        condition = Operators.AND(condition, cpu.RSP == 0x7fffffffccb0)
        condition = Operators.AND(condition, cpu.RIP == 0x5bfa79)
        condition = Operators.AND(condition, cpu.EAX == 0x8001)
        condition = Operators.AND(condition, cpu.EDX == 0x7f)
        condition = Operators.AND(condition, cpu.EBX == 0x80000000)
        condition = Operators.AND(condition, cpu.ECX == 0x8001)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG_1_symbolic(self):
        ''' Instruction CMPXCHG_1
            Groups:
            0x7ffff7a65367:	cmpxchg	dword ptr [rip + 0x36fde2], esi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a65000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd5000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5150)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5151)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5152)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5153)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7a65367] = '\x0f'
        mem[0x7ffff7a65368] = '\xb1'
        mem[0x7ffff7a65369] = '5'
        mem[0x7ffff7a6536a] = '\xe2'
        mem[0x7ffff7a6536b] = '\xfd'
        mem[0x7ffff7a6536c] = '6'
        mem[0x7ffff7a6536d] = '\x00'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0x1)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7a65367
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5150, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5151, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5152, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5153, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a65367, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a65368, 8)== ord('\xb1'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a65369, 8)== ord('5'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6536a, 8)== ord('\xe2'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6536b, 8)== ord('\xfd'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6536c, 8)== ord('6'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6536d, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.ESI == 0x1)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a6536e)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG_2_symbolic(self):
        ''' Instruction CMPXCHG_2
            Groups:
            0x40abbf:	cmpxchg	dword ptr [rdx], esi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040a000, 0x1000, 'rwx')
        mem.mmap(0x006be000, 0x1000, 'rwx')
        mem[0x40abc0] = '\xb1'
        mem[0x40abc1] = '2'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be762)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be763)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be761)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be760)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x40abbf] = '\x0f'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0x1)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x40abbf
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x6be760)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x40abc0, 8)== ord('\xb1'))
        condition = Operators.AND(condition, cpu.read_int(0x40abc1, 8)== ord('2'))
        condition = Operators.AND(condition, cpu.read_int(0x6be762, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6be763, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6be761, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x40abbf, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x6be760, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.ESI == 0x1)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x40abc2)
        condition = Operators.AND(condition, cpu.RDX == 0x6be760)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG_3_symbolic(self):
        ''' Instruction CMPXCHG_3
            Groups:
            0x413646:	cmpxchg	dword ptr [rbx], esi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00413000, 0x1000, 'rwx')
        mem.mmap(0x006b9000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6b9840)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6b9841)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6b9842)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6b9843)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x413646] = '\x0f'
        mem[0x413647] = '\xb1'
        mem[0x413648] = '3'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0x1)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x6b9840)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x413646
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x6b9840, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x6b9841, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6b9842, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6b9843, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x413646, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x413647, 8)== ord('\xb1'))
        condition = Operators.AND(condition, cpu.read_int(0x413648, 8)== ord('3'))
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.ESI == 0x1)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.RBX == 0x6b9840)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x413649)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG_4_symbolic(self):
        ''' Instruction CMPXCHG_4
            Groups:
            0x435a25:	cmpxchg	qword ptr [rdx], rdi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00435000, 0x1000, 'rwx')
        mem.mmap(0x006bd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd380)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd381)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd382)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd383)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd384)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd385)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd386)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6bd387)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x435a25] = 'H'
        mem[0x435a26] = '\x0f'
        mem[0x435a27] = '\xb1'
        mem[0x435a28] = ':'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RDI = cs.new_bitvec(64)
        cs.add(cpu.RDI == 0x6bb7c0)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x435a25
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x6bd380)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x6bd380, 8)== ord('\xc0'))
        condition = Operators.AND(condition, cpu.read_int(0x6bd381, 8)== ord('\xb7'))
        condition = Operators.AND(condition, cpu.read_int(0x6bd382, 8)== ord('k'))
        condition = Operators.AND(condition, cpu.read_int(0x6bd383, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6bd384, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6bd385, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6bd386, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6bd387, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x435a25, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x435a26, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x435a27, 8)== ord('\xb1'))
        condition = Operators.AND(condition, cpu.read_int(0x435a28, 8)== ord(':'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.RDI == 0x6bb7c0)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x435a29)
        condition = Operators.AND(condition, cpu.RDX == 0x6bd380)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG_5_symbolic(self):
        ''' Instruction CMPXCHG_5
            Groups:
            0x41086e:	cmpxchg	dword ptr [rdx], ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00410000, 0x1000, 'rwx')
        mem.mmap(0x006be000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be760)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be761)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be762)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x6be763)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x41086e] = '\x0f'
        mem[0x41086f] = '\xb1'
        mem[0x410870] = '\n'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x1)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x41086e
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x6be760)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x6be760, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x6be761, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6be762, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x6be763, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x41086e, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x41086f, 8)== ord('\xb1'))
        condition = Operators.AND(condition, cpu.read_int(0x410870, 8)== ord('\n'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.ECX == 0x1)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x410871)
        condition = Operators.AND(condition, cpu.RDX == 0x6be760)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMPXCHG_6_symbolic(self):
        ''' Instruction CMPXCHG_6
            Groups:
            0x7ffff7aafa06:	cmpxchg	dword ptr [rbx], esi
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7aaf000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd3000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd3b80)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd3b81)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd3b82)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd3b83)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7aafa06] = '\x0f'
        mem[0x7ffff7aafa07] = '\xb1'
        mem[0x7ffff7aafa08] = '3'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.ESI = cs.new_bitvec(32)
        cs.add(cpu.ESI == 0x1)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x0)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x7ffff7dd3b80)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7aafa06
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd3b80, 8)== ord('\x01'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd3b81, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd3b82, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd3b83, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aafa06, 8)== ord('\x0f'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aafa07, 8)== ord('\xb1'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7aafa08, 8)== ord('3'))
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x0)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.ESI == 0x1)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.RBX == 0x7ffff7dd3b80)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7aafa09)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMP_1_symbolic(self):
        ''' Instruction CMP_1
            Groups:
            0x7ffff7b58f43:	cmp	r12, r9
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7b58000, 0x1000, 'rwx')
        mem[0x7ffff7b58f43] = 'M'
        mem[0x7ffff7b58f44] = '9'
        mem[0x7ffff7b58f45] = '\xcc'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.R12 = cs.new_bitvec(64)
        cs.add(cpu.R12 == 0x7ffff7ab0f80)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7b58f43
        cpu.R9 = cs.new_bitvec(64)
        cs.add(cpu.R9 == 0x7ffff7b23c00)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f43, 8)== ord('M'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f44, 8)== ord('9'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7b58f45, 8)== ord('\xcc'))
        condition = Operators.AND(condition, cpu.SF == True)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.R12 == 0x7ffff7ab0f80)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7b58f46)
        condition = Operators.AND(condition, cpu.R9 == 0x7ffff7b23c00)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMP_2_symbolic(self):
        ''' Instruction CMP_2
            Groups:
            0x406e1d:	cmp	r14w, word ptr [rbx]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00406000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffe000, 0x1000, 'rwx')
        mem[0x406e20] = '3'
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffee69)
        value = cs.new_bitvec(8)
        cs.add(value == 0x57)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffee6a)
        value = cs.new_bitvec(8)
        cs.add(value == 0x49)
        mem[addr] = value
        mem[0x406e1d] = 'f'
        mem[0x406e1e] = 'D'
        mem[0x406e1f] = ';'
        cpu.R14W = cs.new_bitvec(16)
        cs.add(cpu.R14W == 0x444c)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RBX = cs.new_bitvec(64)
        cs.add(cpu.RBX == 0x7fffffffee69)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x406e1d
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x406e20, 8)== ord('3'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffee69, 8)== ord('W'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffee6a, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x406e1d, 8)== ord('f'))
        condition = Operators.AND(condition, cpu.read_int(0x406e1e, 8)== ord('D'))
        condition = Operators.AND(condition, cpu.read_int(0x406e1f, 8)== ord(';'))
        condition = Operators.AND(condition, cpu.R14W == 0x444c)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RBX == 0x7fffffffee69)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x406e21)
        condition = Operators.AND(condition, cpu.SF == True)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMP_3_symbolic(self):
        ''' Instruction CMP_3
            Groups:
            0x40d167:	cmp	eax, 0xff
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0040d000, 0x1000, 'rwx')
        mem[0x40d168] = '\xf8'
        mem[0x40d169] = '\xff'
        mem[0x40d167] = '\x83'
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x1)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x40d167
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x40d168, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x40d169, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x40d167, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.EAX == 0x1)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.AF == True)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x40d16a)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMP_4_symbolic(self):
        ''' Instruction CMP_4
            Groups:
            0x7ffff7de4488:	cmp	qword ptr [rbp - 0x90], 0
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de4000, 0x1000, 'rwx')
        mem.mmap(0x7fffffffd000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a0)
        value = cs.new_bitvec(8)
        cs.add(value == 0xe0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a1)
        value = cs.new_bitvec(8)
        cs.add(value == 0x4d)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a2)
        value = cs.new_bitvec(8)
        cs.add(value == 0xa3)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a3)
        value = cs.new_bitvec(8)
        cs.add(value == 0xf7)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a4)
        value = cs.new_bitvec(8)
        cs.add(value == 0xff)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a5)
        value = cs.new_bitvec(8)
        cs.add(value == 0x7f)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a6)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7fffffffd9a7)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7de4488] = 'H'
        mem[0x7ffff7de4489] = '\x83'
        mem[0x7ffff7de448a] = '\xbd'
        mem[0x7ffff7de448b] = 'p'
        mem[0x7ffff7de448c] = '\xff'
        mem[0x7ffff7de448d] = '\xff'
        mem[0x7ffff7de448e] = '\xff'
        mem[0x7ffff7de448f] = '\x00'
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de4488
        cpu.RBP = cs.new_bitvec(64)
        cs.add(cpu.RBP == 0x7fffffffda30)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a0, 8)== ord('\xe0'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a1, 8)== ord('M'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a2, 8)== ord('\xa3'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a3, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a4, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a5, 8)== ord('\x7f'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a6, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7fffffffd9a7, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de4488, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de4489, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de448a, 8)== ord('\xbd'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de448b, 8)== ord('p'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de448c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de448d, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de448e, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de448f, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de4490)
        condition = Operators.AND(condition, cpu.RBP == 0x7fffffffda30)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMP_5_symbolic(self):
        ''' Instruction CMP_5
            Groups:
            0x7ffff7de6111:	cmp	rax, 0x26
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de6111] = 'H'
        mem[0x7ffff7de6112] = '\x83'
        mem[0x7ffff7de6113] = '\xf8'
        mem[0x7ffff7de6114] = '&'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x8)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de6111
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6111, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6112, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6113, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de6114, 8)== ord('&'))
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.RAX == 0x8)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de6115)
        condition = Operators.AND(condition, cpu.SF == True)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CMP_6_symbolic(self):
        ''' Instruction CMP_6
            Groups:
            0x7ffff7de620b:	cmp	r12, 0x24
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de6000, 0x1000, 'rwx')
        mem[0x7ffff7de620b] = 'I'
        mem[0x7ffff7de620c] = '\x83'
        mem[0x7ffff7de620d] = '\xfc'
        mem[0x7ffff7de620e] = '$'
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.R12 = cs.new_bitvec(64)
        cs.add(cpu.R12 == 0x6)
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7de620b
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == True)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de620b, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de620c, 8)== ord('\x83'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de620d, 8)== ord('\xfc'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de620e, 8)== ord('$'))
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.R12 == 0x6)
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.CF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de620f)
        condition = Operators.AND(condition, cpu.SF == True)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CQO_1_symbolic(self):
        ''' Instruction CQO_1
            Groups:
            0x400794:	cqo
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x400794] = 'H'
        mem[0x400795] = '\x99'
        cpu.RIP = 0x400794
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x400794, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x400795, 8)== ord('\x99'))
        condition = Operators.AND(condition, cpu.RAX == 0x600000)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x400796)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CQO_2_symbolic(self):
        ''' Instruction CQO_2
            Groups:
            0x4006d4:	cqo
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x4006d4] = 'H'
        mem[0x4006d5] = '\x99'
        cpu.RIP = 0x4006d4
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4006d4, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d5, 8)== ord('\x99'))
        condition = Operators.AND(condition, cpu.RAX == 0x600000)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x4006d6)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CQO_3_symbolic(self):
        ''' Instruction CQO_3
            Groups:
            0x7ffff7a4e234:	cqo
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e234] = 'H'
        mem[0x7ffff7a4e235] = '\x99'
        cpu.RIP = 0x7ffff7a4e234
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e234, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e235, 8)== ord('\x99'))
        condition = Operators.AND(condition, cpu.RAX == 0x600000)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a4e236)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CQO_4_symbolic(self):
        ''' Instruction CQO_4
            Groups:
            0x7ffff7a4e234:	cqo
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e234] = 'H'
        mem[0x7ffff7a4e235] = '\x99'
        cpu.RIP = 0x7ffff7a4e234
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e234, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e235, 8)== ord('\x99'))
        condition = Operators.AND(condition, cpu.RAX == 0x600000)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a4e236)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CQO_5_symbolic(self):
        ''' Instruction CQO_5
            Groups:
            0x4006d4:	cqo
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x4006d4] = 'H'
        mem[0x4006d5] = '\x99'
        cpu.RIP = 0x4006d4
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4006d4, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d5, 8)== ord('\x99'))
        condition = Operators.AND(condition, cpu.RAX == 0x600000)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x4006d6)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_CQO_6_symbolic(self):
        ''' Instruction CQO_6
            Groups:
            0x7ffff7a4e234:	cqo
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e234] = 'H'
        mem[0x7ffff7a4e235] = '\x99'
        cpu.RIP = 0x7ffff7a4e234
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e234, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e235, 8)== ord('\x99'))
        condition = Operators.AND(condition, cpu.RAX == 0x600000)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a4e236)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DEC_1_symbolic(self):
        ''' Instruction DEC_1
            Groups: mode64
            0x41e10a:	dec	ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x0041e000, 0x1000, 'rwx')
        mem[0x41e10a] = '\xff'
        mem[0x41e10b] = '\xc9'
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x41e10a
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0xd)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x41e10a, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x41e10b, 8)== ord('\xc9'))
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x41e10c)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.ECX == 0xc)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DEC_2_symbolic(self):
        ''' Instruction DEC_2
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x4)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462d, 8)== ord('\xc9'))
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df462e)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.ECX == 0x3)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DEC_3_symbolic(self):
        ''' Instruction DEC_3
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x2)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462d, 8)== ord('\xc9'))
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df462e)
        condition = Operators.AND(condition, cpu.PF == False)
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.ECX == 0x1)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DEC_4_symbolic(self):
        ''' Instruction DEC_4
            Groups: mode64
            0x7ffff7a65448:	dec	dword ptr [rip + 0x36fd02]
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a65000, 0x1000, 'rwx')
        mem.mmap(0x7ffff7dd5000, 0x1000, 'rwx')
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5150)
        value = cs.new_bitvec(8)
        cs.add(value == 0x1)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5151)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5152)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        addr = cs.new_bitvec(64)
        cs.add(addr == 0x7ffff7dd5153)
        value = cs.new_bitvec(8)
        cs.add(value == 0x0)
        mem[addr] = value
        mem[0x7ffff7a65448] = '\xff'
        mem[0x7ffff7a65449] = '\r'
        mem[0x7ffff7a6544a] = '\x02'
        mem[0x7ffff7a6544b] = '\xfd'
        mem[0x7ffff7a6544c] = '6'
        mem[0x7ffff7a6544d] = '\x00'
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == True)
        cpu.RIP = 0x7ffff7a65448
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5150, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5151, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5152, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7dd5153, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a65448, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a65449, 8)== ord('\r'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6544a, 8)== ord('\x02'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6544b, 8)== ord('\xfd'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6544c, 8)== ord('6'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a6544d, 8)== ord('\x00'))
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a6544e)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.SF == False)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DEC_5_symbolic(self):
        ''' Instruction DEC_5
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == True)
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x4)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462d, 8)== ord('\xc9'))
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == False)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df462e)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.ECX == 0x3)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DEC_6_symbolic(self):
        ''' Instruction DEC_6
            Groups: mode64
            0x7ffff7df462c:	dec	ecx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7df4000, 0x1000, 'rwx')
        mem[0x7ffff7df462c] = '\xff'
        mem[0x7ffff7df462d] = '\xc9'
        cpu.AF = cs.new_bool()
        cs.add(cpu.AF == False)
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.ZF = cs.new_bool()
        cs.add(cpu.ZF == False)
        cpu.RIP = 0x7ffff7df462c
        cpu.PF = cs.new_bool()
        cs.add(cpu.PF == False)
        cpu.SF = cs.new_bool()
        cs.add(cpu.SF == False)
        cpu.ECX = cs.new_bitvec(32)
        cs.add(cpu.ECX == 0x1)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462c, 8)== ord('\xff'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7df462d, 8)== ord('\xc9'))
        condition = Operators.AND(condition, cpu.AF == False)
        condition = Operators.AND(condition, cpu.OF == False)
        condition = Operators.AND(condition, cpu.ZF == True)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7df462e)
        condition = Operators.AND(condition, cpu.PF == True)
        condition = Operators.AND(condition, cpu.SF == False)
        condition = Operators.AND(condition, cpu.ECX == 0x0)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DIV_1_symbolic(self):
        ''' Instruction DIV_1
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x3f3)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x3de00ec7)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff9, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ffa, 8)== ord('\xf1'))
        condition = Operators.AND(condition, cpu.RAX == 0xfaaef)
        condition = Operators.AND(condition, cpu.RCX == 0x3f3)
        condition = Operators.AND(condition, cpu.RDX == 0xea)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3ffb)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DIV_2_symbolic(self):
        ''' Instruction DIV_2
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x3f3)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x3de00ec7)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff9, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ffa, 8)== ord('\xf1'))
        condition = Operators.AND(condition, cpu.RAX == 0xfaaef)
        condition = Operators.AND(condition, cpu.RCX == 0x3f3)
        condition = Operators.AND(condition, cpu.RDX == 0xea)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3ffb)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DIV_3_symbolic(self):
        ''' Instruction DIV_3
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x3f3)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x9e7650bc)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff9, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ffa, 8)== ord('\xf1'))
        condition = Operators.AND(condition, cpu.RAX == 0x281ffc)
        condition = Operators.AND(condition, cpu.RCX == 0x3f3)
        condition = Operators.AND(condition, cpu.RDX == 0x88)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3ffb)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DIV_4_symbolic(self):
        ''' Instruction DIV_4
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x3f3)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x10a8b550)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff9, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ffa, 8)== ord('\xf1'))
        condition = Operators.AND(condition, cpu.RAX == 0x437e2)
        condition = Operators.AND(condition, cpu.RCX == 0x3f3)
        condition = Operators.AND(condition, cpu.RDX == 0x3ca)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3ffb)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DIV_5_symbolic(self):
        ''' Instruction DIV_5
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x32)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x3cbc6423)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff9, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ffa, 8)== ord('\xf1'))
        condition = Operators.AND(condition, cpu.RAX == 0x136f7c3)
        condition = Operators.AND(condition, cpu.RCX == 0x32)
        condition = Operators.AND(condition, cpu.RDX == 0xd)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3ffb)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_DIV_6_symbolic(self):
        ''' Instruction DIV_6
            Groups:
            0x7ffff7de3ff8:	div	rcx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7de3000, 0x1000, 'rwx')
        mem[0x7ffff7de3ff8] = 'H'
        mem[0x7ffff7de3ff9] = '\xf7'
        mem[0x7ffff7de3ffa] = '\xf1'
        cpu.RIP = 0x7ffff7de3ff8
        cpu.RCX = cs.new_bitvec(64)
        cs.add(cpu.RCX == 0x3f3)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x2e8912d8)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff8, 8)== ord('H'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ff9, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7de3ffa, 8)== ord('\xf1'))
        condition = Operators.AND(condition, cpu.RAX == 0xbc890)
        condition = Operators.AND(condition, cpu.RCX == 0x3f3)
        condition = Operators.AND(condition, cpu.RDX == 0x228)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7de3ffb)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_IDIV_1_symbolic(self):
        ''' Instruction IDIV_1
            Groups:
            0x7ffff7a4e236:	idiv	r8
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e238] = '\xf8'
        mem[0x7ffff7a4e236] = 'I'
        mem[0x7ffff7a4e237] = '\xf7'
        cpu.RIP = 0x7ffff7a4e236
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x8)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e238, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e236, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e237, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.RAX == 0xc0000)
        condition = Operators.AND(condition, cpu.R8 == 0x8)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a4e239)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_IDIV_2_symbolic(self):
        ''' Instruction IDIV_2
            Groups:
            0x4006d6:	idiv	r8
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x4006d8] = '\xf8'
        mem[0x4006d6] = 'I'
        mem[0x4006d7] = '\xf7'
        cpu.RIP = 0x4006d6
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x8)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4006d8, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d6, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d7, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.RAX == 0xc0000)
        condition = Operators.AND(condition, cpu.R8 == 0x8)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x4006d9)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_IDIV_3_symbolic(self):
        ''' Instruction IDIV_3
            Groups:
            0x7ffff7a4e236:	idiv	r8
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e238] = '\xf8'
        mem[0x7ffff7a4e236] = 'I'
        mem[0x7ffff7a4e237] = '\xf7'
        cpu.RIP = 0x7ffff7a4e236
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x8)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e238, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e236, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e237, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.RAX == 0xc0000)
        condition = Operators.AND(condition, cpu.R8 == 0x8)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a4e239)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_IDIV_4_symbolic(self):
        ''' Instruction IDIV_4
            Groups:
            0x4006d6:	idiv	r8
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x4006d8] = '\xf8'
        mem[0x4006d6] = 'I'
        mem[0x4006d7] = '\xf7'
        cpu.RIP = 0x4006d6
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x8)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4006d8, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d6, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d7, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.RAX == 0xc0000)
        condition = Operators.AND(condition, cpu.R8 == 0x8)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x4006d9)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_IDIV_5_symbolic(self):
        ''' Instruction IDIV_5
            Groups:
            0x4006d6:	idiv	r8
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x00400000, 0x1000, 'rwx')
        mem[0x4006d8] = '\xf8'
        mem[0x4006d6] = 'I'
        mem[0x4006d7] = '\xf7'
        cpu.RIP = 0x4006d6
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x8)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x4006d8, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d6, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x4006d7, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.RAX == 0xc0000)
        condition = Operators.AND(condition, cpu.R8 == 0x8)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x4006d9)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_IDIV_6_symbolic(self):
        ''' Instruction IDIV_6
            Groups:
            0x7ffff7a4e236:	idiv	r8
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7a4e000, 0x1000, 'rwx')
        mem[0x7ffff7a4e238] = '\xf8'
        mem[0x7ffff7a4e236] = 'I'
        mem[0x7ffff7a4e237] = '\xf7'
        cpu.RIP = 0x7ffff7a4e236
        cpu.R8 = cs.new_bitvec(64)
        cs.add(cpu.R8 == 0x8)
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x0)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])

        condition = True
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e238, 8)== ord('\xf8'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e236, 8)== ord('I'))
        condition = Operators.AND(condition, cpu.read_int(0x7ffff7a4e237, 8)== ord('\xf7'))
        condition = Operators.AND(condition, cpu.RAX == 0xc0000)
        condition = Operators.AND(condition, cpu.R8 == 0x8)
        condition = Operators.AND(condition, cpu.RDX == 0x0)
        condition = Operators.AND(condition, cpu.RIP == 0x7ffff7a4e239)

        with cs as temp_cs:
            temp_cs.add(condition)
            self.assertTrue(solver.check(temp_cs))
        with cs as temp_cs:
            temp_cs.add(condition == False)
            self.assertFalse(solver.check(temp_cs))


    def test_IMUL_1_symbolic(self):
        ''' Instruction IMUL_1
            Groups:
            0x7ffff7acfec4:	imul	eax, edx
        '''
        cs = ConstraintSet()
        mem = SMemory64(cs)
        cpu = AMD64Cpu(mem)
        mem.mmap(0x7ffff7acf000, 0x1000, 'rwx')
        mem[0x7ffff7acfec4] = '\x0f'
        mem[0x7ffff7acfec5] = '\xaf'
        mem[0x7ffff7acfec6] = '\xc2'
        cpu.OF = cs.new_bool()
        cs.add(cpu.OF == False)
        cpu.CF = cs.new_bool()
        cs.add(cpu.CF == False)
        cpu.RIP = 0x7ffff7acfec4
        cpu.RDX = cs.new_bitvec(64)
        cs.add(cpu.RDX == 0x1)
        cpu.EAX = cs.new_bitvec(32)
        cs.add(cpu.EAX == 0x600000)
        cpu.EDX = cs.new_bitvec(32)
        cs.add(cpu.EDX == 0x1)
        cpu.RAX = cs.new_bitvec(64)
        cs.add(cpu.RAX == 0x600000)

        done = False
        while not done:
            try:
                cpu.execute()
                #cpu.writeback()
                done = True
            except ConcretizeRegister as e:
                symbol = getattr(cpu, e.reg_name)
                values = solver.get_all_values(cs, symbol)
                self.assertEqual(len(values), 1)
                setattr(cpu, e.reg_name, values[0])
