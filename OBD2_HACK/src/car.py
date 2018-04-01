
import pydevd
import sys

pydevd.settrace("localhost", port=5678,stdoutToServer=True, stderrToServer=True)

sys.path.append('./lib')

import obd
from obd import OBDStatus
from sys import stdout
import time
from operator import itemgetter

h=None
def read_test():
        global h
        if h==None: 
            h=open("Output2.txt","r")
        return h.readline()
        
        

class zeroterm:
    def __init__(self, nrow=4, ncol=50):      # nrow, ncol determines the size of the scrolling (=normal terminal behaviour) part of the screen
        stdout.write("\x1b[2J")                # clear screen
        self.nrow = nrow
        self.ncol = ncol
        self.buf = []

    def write(self, s, x=None, y=None):        # if no x,y specified, normal console behaviour
        if x is not None and y is not None:    # if x,y specified, fixed text position
            self.movepos(x,y)
            print s
        else:
            if len(self.buf) < self.nrow:
                self.buf.append(s)
            else:
                self.buf[:-1] = self.buf[1:]
                self.buf[-1] = s

            for i, r in enumerate(self.buf):
                self.movepos(i+1,0)
                print r[:self.ncol].ljust(self.ncol)

    def movepos(self, row, col):
        stdout.write("\x1b[%d;%dH" % (row, col))
        
if __name__ == "__main__":
    # An exemple
    t = zeroterm()   
    
    
    t.write('CAN Package Analysis', 1, 1)
    t.write('ELM327:', 2, 1)

    #obd.logger.setLevel(obd.logging.DEBUG)    
        
    try:
        while True:
            connection = obd.OBD("/dev/rfcomm0",baudrate=500000, protocol="6")
            if (connection.status()==OBDStatus.CAR_CONNECTED):
                t.write('OK  ', 2, 8)
                break
            else:
                t.write('Erro', 2, 8)
                connection.close()
          
        #connection.interface.write(b"ATPP0CSV08")    
        
        #This command places the ELM327 into a bus monitoring mode 
        connection.interface.write(b"ATMA")
        text_file = open("Output.txt", "w")

        #For known packages, it is possible to sort them  
        pos={'170':4,'165':5,'200':6,'201':7,'430':8,'422':9,'420':10,'4FF':11,'630':12,'040':13,'046':14}
        Count={}
        cont_pos=14
        Filtro=True
        
        while True:
            
            b=connection.interface.Read_line().decode()

            text_file.write(str(time.time())+" : "+b+"\r\n")

            b=b.split(" ")
            try:
                row=pos[b[0]]
            except:
                if (Filtro==False):
                    cont_pos+=1
                    row=pos[b[0]]=cont_pos
                else:
                    row=0
            finally:
                if (row<>0):                    
                    t.write(b[0], row, 1)
                    col=2
                    for s in b[1:]:
                        col=col+3
                        t.write(s, row, col)
                        t.write(" ", row, col+2)
                        
                    q=[" " for c in range(60-col)]
                    q=''.join(q)
                    t.write(q, row, col)
            
            try:
                Q=Count[b[0]]
            except:
                Q=Count[b[0]]=0                
            finally:
                Count[b[0]]=Q+1
                row=1
                col=60
                for s in sorted(Count.items(),key=itemgetter(1),reverse=True):
                    t.write("        ", row, col)
                    t.write(s[0], row, col)                    
                    t.write(s[1], row, col+8)
                    row+=1
                    
            #This section have packages discovered when I did an analysis on the communication from my Ford Focus       
            
            if (b[0]=="420") and (len(b)>=10):
                temperatura = int(b[1],16)-40
                t.write("Temperature: "+str(temperatura)+" ", 1, 90)
            if (b[0]=="430") and (len(b)>=10):
                Nivel = (int(b[1],16)*256.0+int(b[2],16))/65536.0
                Freio = (b[7]=="20")
                t.write("Fuel Level: %.2f"%(Nivel*100)+"%", 2, 90)
                t.write("Hand Brake: "+str(Freio)+" ", 3, 90)     
            if (b[0]=="201") and (len(b)>=10):
                RPM = (int(b[1],16)*256.0+int(b[2],16))/4.0
                t.write("RPM: "+str(RPM)+"    ", 4, 90)
                VSS = ((int(b[5],16)*256.0+int(b[6],16)*1.0)-10000.0)/100.0
                t.write("Velocity: %.2f"%VSS+"    ", 5, 90)  
                Acel = int(b[7],16)*100.0/255.0
                t.write("Accelerator: %.2f"%Acel+"    ", 6, 90)   
            if (b[0]=="4FF") and (len(b)>=10) and (b[1]=="10"):
                temp = int(b[5],16)-40
                t.write("External Temperature: "+str(temp), 7, 90)
            if (b[0]=="422"):
                if (len(b)>=8):
                    Acel = (int(b[1],16)*256+int(b[6],16))*100.0/65536.0
                else:
                    Acel = int(b[1],16)*256*100.0/65536.0
                t.write("Accelerator 2: %.2f"%Acel+"    ", 8, 90)
                
            if (b[0]=="4FF") and (len(b)>=10):
                pos2={'10':0,'11':1,'32':2,'33':3,'34':4}
                col=90                    
                for s in b[1:]:
                    t.write(s, 30+pos2[b[1]], col)
                    t.write(" ", 30+pos2[b[1]], col+2)
                    col=col+3

    except KeyboardInterrupt:
        connection.interface.send(b"ATZ")
        text_file.close()
        exit()

