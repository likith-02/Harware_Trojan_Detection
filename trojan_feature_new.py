from statistics import mean
import queue

# Data processing
# Making a Graph using a dictionary

INF=10**6
for y in range(1,101):
    inp='s5378_trojan'+str(y)+'.txt'
    fp=open(inp,"r")

    # mapp maps the all the outputs from the gates and the primary inputs to its children
    mapp={}
    dff=[]
    primary_outputs=[]
    primary_inputs=[]
    output_input_cnt={}
    nets_LGFi={}
    nets_FFo_dist={}
    nets_FF_dist={}
    nets_FF_vis={}
    nets_PI_dist={}
    nets_PI_vis={}
    nets_po_dist={}
    nets_PO_dist={}
    nets_po_vis={}
    nets_FFi_dist={}
    nets_FFi_vis={}
    cnt_trojan=0
    # Reading the input file to initialize all the visited and distance arrays and to convert the input given to a graph

    for i in range(6):
        fp.readline()
    while 1:
        cnt_trojan+=1
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
            if num not in primary_outputs:
                nets_LGFi.update({num:0})
                nets_FF_vis.update({num:0})
                nets_FFo_dist.update({num:INF})
                nets_FF_dist.update({num:INF})
                nets_PI_vis.update({num:0})
                nets_PI_dist.update({num:INF})
                nets_po_vis.update({num:0})
                nets_PO_dist.update({num:INF})
                nets_po_dist.update({num:INF})
                nets_FFi_vis.update({num:0})
                nets_FFi_dist.update({num:INF})
            primary_inputs.append(num)
        elif "DFF" in line or "NOT" in line:
            i=0
            out=""
            while line[i]!=' ':
                out+=line[i]
                i+=1
            i+=3
            if "NOT" in line:
                output_input_cnt.update({out:1})
            if "DFF" in line:
                dff.append(out)
            if out not in mapp:
                mapp.update({out:[]})
            if out not in primary_outputs:
                nets_LGFi.update({out:0})
                nets_FFo_dist.update({out:INF})
                nets_FF_dist.update({out:INF})
                nets_FF_vis.update({out:0})
                nets_PI_dist.update({out:INF})
                nets_PI_vis.update({out:0})
                nets_PO_dist.update({out:INF})
                nets_po_dist.update({out:INF})
                nets_po_vis.update({out:0})
                nets_FFi_dist.update({out:INF})
                nets_FFi_vis.update({out:0})
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
                    gate=gate_type+"("+num+")"
                    if num in mapp:
                        mapp[num].append([gate,out])
                    else:
                        mapp.update({num:[[gate,out]]})
                    nets_LGFi.update({num:0})
                    nets_FFo_dist.update({num:INF})
                    nets_FF_dist.update({num:INF})
                    nets_FF_vis.update({num:0})
                    nets_PI_dist.update({num:INF})
                    nets_PI_vis.update({num:0})
                    nets_PO_dist.update({num:INF})
                    nets_po_dist.update({num:INF})
                    nets_po_vis.update({num:0})
                    nets_FFi_dist.update({num:INF})
                    nets_FFi_vis.update({num:0})
                    break
                i+=1
        elif ("AND" in line) or ("OR" in line) or ("NAND" in line) or ("NOR" in line):
            i=0
            out=""
            while line[i]!=' ':
                out+=line[i]
                i+=1
            i+=3
            if out not in mapp:
                mapp.update({out:[]})
            if out not in primary_outputs:
                nets_LGFi.update({out:0})
                nets_FFo_dist.update({out:INF})
                nets_FF_dist.update({out:INF})
                nets_FF_vis.update({out:0})
                nets_PI_dist.update({out:INF})
                nets_PI_vis.update({out:0})
                nets_PO_dist.update({out:INF})
                nets_po_dist.update({out:INF})
                nets_po_vis.update({out:0})
                nets_FFi_dist.update({out:INF})
                nets_FFi_vis.update({out:0})
            gate_type=""
            while line[i]!='(':
                gate_type+=line[i]
                i+=1
            inputs=[]
            while i<len(line):
                if (line[i]=='g' or line[i]=='I'or line[i]=='z' or line[i]=='n' or line[i]=='P') and i!=0:
                    num=""
                    while line[i]!=')' and line[i]!=',':
                        num+=line[i]
                        i+=1
                    inputs.append(num)
                i+=1
            output_input_cnt.update({out:len(inputs)})
            gate=gate_type+"("
            for i in range(len(inputs)-1):
                gate+=inputs[i]
                gate+=','
            gate+=inputs[-1]
            gate+=')'
            for i in range(len(inputs)):
                num=inputs[i]
                if inputs[i] in mapp.keys():
                    mapp[inputs[i]].append([gate,out])
                else:
                    mapp.update({inputs[i]:[[gate,out]]})
                nets_LGFi.update({num:0})
                nets_FFo_dist.update({num:INF})
                nets_FF_dist.update({num:INF})
                nets_FF_vis.update({num:0})
                nets_PI_dist.update({num:INF})
                nets_PI_vis.update({num:0})
                nets_PO_dist.update({num:INF})
                nets_po_dist.update({num:INF})
                nets_po_vis.update({num:0})
                nets_FFi_dist.update({num:INF})
                nets_FFi_vis.update({num:0})
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
                    if num not in mapp:
                        mapp.update({num:[]})
                i+=1
    for out in primary_outputs:
        nets_LGFi.update({out:0})
        nets_FFo_dist.update({out:INF})
        nets_FF_dist.update({out:INF})
        nets_FF_vis.update({out:0})
        nets_PI_dist.update({out:INF})
        nets_PI_vis.update({out:0})
        nets_PO_dist.update({out:INF})
        nets_po_dist.update({out:INF})
        nets_po_vis.update({out:0})
        nets_FFi_dist.update({out:INF})
        nets_FFi_vis.update({out:0})

    #print(cnt_trojan)
    total=0
    for i in mapp:
        total+=len(i)
    #print(total)

    #LGFi Implementation

    for out in output_input_cnt:
        for gate in mapp[out]:
            nets_LGFi[gate[1]]+=output_input_cnt[out]

    total=0
    for i in nets_LGFi:
        total+=nets_LGFi[i]

    LGFi_avg=total/len(nets_LGFi)

    # PI implementation
    #using BFS to find the shortest path between net n and primary input

    def BFS_PI(src):
        q=queue.Queue(maxsize=10**6)
        q.put(src)
        nets_PI_vis[src]=1
        nets_PI_dist[src]=0
        while q.empty()==False:
            curr=q.get()
            for gate in mapp[curr]:
                if nets_PI_vis[gate[1]]==0:
                    q.put(gate[1])
                    nets_PI_dist[gate[1]]=min(nets_PI_dist[curr]+1,nets_PI_dist[gate[1]])
                    nets_PI_vis[gate[1]]=1

    for out in primary_inputs:
        for nets in nets_PI_vis:
            nets_PI_vis[nets]=0
        #print(out)
        BFS_PI(out)
        
    # Calculating the average distance of a net from primary input

    total=0

    for i in nets_PI_dist.keys():
        if nets_PI_dist[i]!=INF:
            total+=nets_PI_dist[i]
        else:
            nets_PI_dist[i]=-1
            
    PI_avg=total/len(nets_PI_dist)

    #FFi implementation
    #using BFS to find the nearest flip flop output to the net n

    def BFS_FFi(src):
        q=queue.Queue(maxsize=10**6)
        q.put(src)
        nets_FFi_vis[src]=1
        nets_FFi_dist[src]=0
        while q.empty()==False:
            curr=q.get()
            for gate in mapp[curr]:
                if  nets_FFi_vis[gate[1]]==0:
                    q.put(gate[1])
                    nets_FFi_dist[gate[1]]=min(nets_FFi_dist[curr]+1,nets_FFi_dist[gate[1]])
                    nets_FFi_vis[gate[1]]=1
           
    for out in dff:
        for nets in nets_FFi_vis:
            nets_FFi_vis[nets]=0
        BFS_FFi(out)

    # Calculating the average distance of the nearest flip flop from the net n

    total=0
    for i in nets_FFi_dist:
        if nets_FFi_dist[i]!=INF:
            total+=nets_FFi_dist[i]
        else:
            nets_FFi_dist[i]=-1
            
    FFi_avg=total/len(nets_FFi_dist)

    #FFo im plementation
    #Using BFS to find the nearest flip flop input from net n

    def BFS_FFo(src):
        q=queue.Queue(maxsize=10**6)
        q.put(src)
        end=False
        nets_FF_vis[src]=1
        nets_FF_dist[src]=0
        while q.empty()==False and end==False:
            curr=q.get()
            for gate in mapp[curr]:
                if  nets_FF_vis[gate[1]]==0:
                    q.put(gate[1])
                    nets_FF_dist[gate[1]]=nets_FF_dist[curr]+1
                    nets_FF_vis[gate[1]]=1
                if gate[1] in dff:
                    nets_FFo_dist[src]=nets_FF_dist[curr]
                    end=True

    for src in nets_FF_dist.keys():
        for nets in nets_FF_vis:
            nets_FF_vis[nets]=0
        BFS_FFo(src)
        
    #Calculating the average distance of nearest flipflop input from net n
        
    total=0
    for i in nets_FFo_dist:
        if nets_FFo_dist[i]!=INF:
            total+=nets_FFo_dist[i]
        else:
            nets_FFo_dist[i]=-1
            
    FFo_avg=total/len(nets_FFo_dist)

    #PO implementation
    #Using BFS to find the shortest path from net n to the primary output

    def BFS_PO(src):
        q=queue.Queue(maxsize=10**6)
        q.put(src)
        end=False
        nets_po_vis[src]=1
        nets_po_dist[src]=0
        while q.empty()==False and end==False:
            curr=q.get()
            for gate in mapp[curr]:
                if  nets_po_vis[gate[1]]==0:
                    q.put(gate[1])
                    nets_po_dist[gate[1]]=nets_po_dist[curr]+1
                    nets_po_vis[gate[1]]=1
                if gate[1] in primary_outputs:
                    nets_PO_dist[src]=nets_po_dist[curr]+1
                    end=True
            if len(mapp[curr])==0:
                nets_PO_dist[src]=nets_po_dist[curr]

    for src in nets_po_dist.keys():
        for nets in nets_po_vis:
            nets_po_vis[nets]=0
        BFS_PO(src)

    #Calculating the average of the distance of the net n from primary output
        
    total=0
    for i in nets_PO_dist:
        if nets_PO_dist[i]!=INF:
            total+=nets_PO_dist[i]
        else:
            nets_PO_dist[i]=-1
            
    PO_avg=total/len(nets_PO_dist)

    #Creating a file for storing all the 5 features for each net  
    outp='s5378_trojan'+str(y)+'features.txt'
    fp1=open(outp,"w")
    fp1.write("NOTE:\n")
    fp1.write("FFi=-1 means that there is no Flop input to the target net n\n")
    fp1.write("FFo=-1 means that there is no Flop output from the target net n\n")
    fp1.write("PI=-1 means that there is no primary input reachable to target net n\n\n\n")
    fp1.write("LGFi_avg: "+str(LGFi_avg)+"\n"+"FFi_avg: "+str(FFi_avg)+"\n"+"PI_avg: "+str(PI_avg)+"\n"+"FFo_avg: "+str(FFo_avg)+"\n"+"PO_avg: "+str(PO_avg)+"\n\n\n")
    fp1.write("Net\t"+"LGFi\t"+"FFi\t"+"FFo\t"+"PI\t"+"PO\n")
    for i in nets_FFo_dist:
        fp1.write(i+'\t'+str(nets_LGFi[i])+'\t'+str(nets_FFi_dist[i])+'\t'+str(nets_FFo_dist[i])+"\t"+str(nets_PI_dist[i])+'\t'+str(nets_PO_dist[i])+'\n')

    #Close both input and output file
        
    fp1.close()
    fp.close()
