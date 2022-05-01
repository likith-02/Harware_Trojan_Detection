import random
import shutil
import os

INF=10**6
print('Name of the textfile:')
inp=input()
fp=open(inp,'r')

inputs=[]
primary_outputs=[]
output_input_cnt={}
logic_gates=[]
for i in range(6):
    fp.readline()
while 1:
    line=fp.readline()
    if line=='':
        break
    elif "INPUT" in line:
        i=0
        num=''
        while line[i]!='(':
            i+=1
        i+=1
        while line[i]!=')':
            num+=line[i]
            i+=1
        inputs.append(num)
    elif "DFF" in line or "NOT" in line:
        i=0
        out=""
        while line[i]!=' ':
            out+=line[i]
            i+=1
        i+=3
        if "NOT" in line:
            output_input_cnt.update({out:1})
            logic_gates.append('NOT')
        gate_type=""
        while line[i]!='(':
            gate_type+=line[i]
            i+=1
        while i<len(line):
            if (line[i]=='g' or line[i]=='I' or line[i]=='z' or line[i]=='n' or line[i]=='P') and i!=0:
                num=""
                while line[i]!=')':
                    num+=line[i]
                    i+=1
                inputs.append(num)
                break
            i+=1
    elif ("AND" in line) or ("OR" in line) or ("NAND" in line) or ("NOR" in line):
        i=0
        out=""
        while line[i]!=' ':
            out+=line[i]
            i+=1
        i+=3
        gate_type=""
        while line[i]!='(':
            gate_type+=line[i]
            i+=1
        while i<len(line):
            if (line[i]=='g' or line[i]=='I'or line[i]=='z' or line[i]=='n' or line[i]=='P') and i!=0:
                num=""
                while line[i]!=')' and line[i]!=',':
                    num+=line[i]
                    i+=1
                inputs.append(num)
            i+=1
        output_input_cnt.update({out:len(inputs)})
        logic_gates.append(gate_type)
        gate=gate_type+"("
        for i in range(len(inputs)-1):
            gate+=inputs[i]
            gate+=','
        gate+=inputs[-1]
        gate+=')'
    elif "OUTPUT" in line:
        i=0
        while i<len(line):
            if line[i]=='(':
                num=""
                i+=1
                while line[i]!=')':
                    num+=line[i]
                    i+=1
                primary_outputs.append(num)
            i+=1
            
inputs=list(set(inputs))
#print(output_input_cnt)
overall=inputs+primary_outputs
N,I=[],[]
for gate in overall:
    if gate[0]=='n':
        i=1
        num=''
        while gate[i]!='g':
            num+=gate[i]
            i+=1
        N.append(int(num))
    else:
        I.append(int(gate[1:]))
N_left,I_left=[],[]
for i in range(max(N)):
    if i not in N:
        N_left.append(i)
for i in range(max(I)):
    if i not in I:
        I_left.append(i)

def select_output(N_left,I_left):
    out_types=['N','I']
    out_type=random.choice(out_types)
    output=-1
    if out_type=='N':
        output=random.choice(N_left)
    else:
        output=random.choice(I_left)
    if out_type=='N':
        return ('n'+str(output)+'gat')
    else:
        return ('I'+str(output))

def select_input(N,I,logic_gates):
    inp_gates=list(set(logic_gates))
    inp_gate=random.choice(inp_gates)
    select_inputs=[]
    if inp_gate=='NOT':
        inp_types=['N','I']
        inp_type=random.choice(inp_types)
        if inp_type=='N':
            select_inputs.append('n'+str(random.choice(N))+'gat')
        else:
            select_inputs.append('I'+str(random.choice(I)))
                                
    else:
        inp_nos=[2,3,4]
        inp_no=random.choice(inp_nos)
        for i in range(inp_no):
            inp_types=['N','I']
            inp_type=random.choice(inp_types)
            if inp_type=='N':
                select_inputs.append('n'+str(random.choice(N))+'gat')
            else:
                select_inputs.append('I'+str(random.choice(I)))
    return inp_gate,select_inputs

def sep_new_comp(N,I,N_left,I_left,logic_gates):
    output=select_output(N_left,I_left)
    gate,inputs=select_input(N,I,logic_gates)
    comp=output+' = '+gate+'('
    inps=''
    for i in range(len(inputs)-1):
        inps+=inputs[i]+', '
    inps+=inputs[-1]
    comp+=inps+')'
    return comp

def insert_single(comps,k,destination,logic_gates):
    gate=''
    if 'NOR' in comps[k]:
        gate='NOR'
    elif 'NOT' in comps[k]:
        gate='NOT'
    elif 'OR' in comps[k]:
        gate='OR'
    elif 'AND' in comps[k]:
        gate='AND'
    elif 'NAND' in comps[k]:
        gate='NAND'
    with open(destination, "r") as f:
        contents = f.readlines()
    start,stop=0,0
    for i in range(7,len(contents)):
        if gate in contents[i]:
            start=i
            while contents[i]!='' and (gate in contents[i]):
                i+=1
            stop=i
            break
    output=''
    for i in range(len(comps[k])):
        if comps[k][i]==' ':
            output=comps[k][:i]
            break
    contents.insert(random.choice(range(start,stop+1)), comps[k]+'\n')
    logic_gates=list(set(logic_gates))
    logic_gates.remove('NOT')
    inp_gates=logic_gates
    inp_gate=random.choice(inp_gates)
    start,stop=0,0
    for i in range(7,len(contents)):
        if inp_gate in contents[i]:
            start=i
            while contents[i]!='' and (gate in contents[i]):
                i+=1
            stop=i
            break
    index=random.choice(range(start,stop+1))
    contents[index]=contents[index][:-2]+', '+output+')'+'\n'
    with open(destination, "w") as f:
        contents = "".join(contents)
        f.write(contents)

for fil in range(1,101):
    num_comps=[1,2]
    num_comp=random.choice(num_comps)
    comps=[]
    for i in range(num_comp):
        comps.append(sep_new_comp(N,I,N_left,I_left,logic_gates))
    print('trojans added in file no-'+str(fil)+':') 
    print(comps)
    destination=inp[:-6]+'_trojan'+str(fil)+'.bench'
    src = open(inp,'r')
    dst = open(destination,'w+')
    shutil.copyfile(inp,destination)
            
    if num_comp==1:
        insert_single(comps,0,destination,logic_gates)
    else:
        if 'NOT' not in comps[1]:
            types=['single','join']
            typ=random.choice(types)
        else:
            typ='single'
        if typ=='single':
            insert_single(comps,0,destination,logic_gates)
            insert_single(comps,1,destination,logic_gates)
        else:
            output=''
            for i in range(len(comps[0])):
                if comps[0][i]==' ':
                    output=comps[0][:i]
                    break
            comps[1]=comps[1][:-2]+', '+output+')'
            insert_single(comps,0,destination,logic_gates)
            insert_single(comps,1,destination,logic_gates)
