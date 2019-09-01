import re
fileInput='TestSourceCodeE.s43' #file name to be compiled goes here
fileNameSearch=re.search('TestSourceCode[a-fA-F]',fileInput)
objFileOutput=fileNameSearch.group(0)+'.txt'
listFileOutput=fileNameSearch.group(0)+'.lst'
class Line:
    def __init__(self,txt):
        self.txt=str(txt)
        self.lineNumber=0
        self.memAddress=0
        self.opCode=0x0000000
        self.addressingData=[0,0,0,0]
        self.adbwas=0
        self.instructionData=[]
        self.end=0
        self.labelOrVar=0 #1 equals label, 2 equals var
        self.isJump=0
        self.isEqu=0
        self.isCall=0
    def setMemAddress(self,memAddress):
        self.memAddress=memAddress
    def setlineNumber(self,lineNumber):
        self.lineNumber=lineNumber
def checkIfVar(line):
    if 'EQU' in line.txt:
        line.isEqu=1
        return False
    elif 'ORG' in line.txt:
        return True
    elif 'DB' in line.txt:
        return True
    elif 'DS' in line.txt:
        return True
    elif 'DW' in line.txt:
        return True
    elif 'ERROR' in line.txt:
        return False
    else:
        return False
def checkIfEqu(line):
    if ' EQU ' in line.txt:
        line.isEqu=1
        return True
    else:
        return False
def validateLabel(list,line,varOrLabel): #check the list for the text string, also checks label length
    temp=line.txt.strip(" ")
    temp=line.txt.split()
    temp=temp[0]
    if varOrLabel==1:
        labelRules=re.search('[A-za-z][A-Za-z0-9_]+$',temp) #checks that label starts only with letter, and only contains letters, numbers, and underscores
        if labelRules==None:
            line.txt=line.txt+" ERROR INVALID LABEL" 
            return True
        elif len(temp)>23:
            line.txt=line.txt+" ERROR LABEL MAY ONLY BE 24 CHARACTERS LONG"
            return True
        elif isinList(labels,temp)==True:
            line.txt=line.txt+" ERROR DUPLICATE LABEL"
            return True
        else:
            return False #add li to symbol table
    elif varOrLabel==0:
        labelRules=re.search('^[A-Za-z][A-Za-z0-9]+$',temp) #checks that label starts only with letter, and only contains letters, numbers, and underscores
        if labelRules==None:
            line.txt=line.txt+" ERROR INVALID VAR NAME"   
            return True
        elif len(temp)>23:
            line.txt=line.txt+" ERROR VAR MAY ONLY BE 24 CHARACTERS LONG"
            return True
        elif isinList(labels,temp)==True: #DB is equivalent to initalizing, you only do it once
            line.txt=line.txt+" ERROR DUPLICATE VAR"
            return True
        else:
            return False #add li to symbol table
def validateEqu(line):
    temp=line.txt.strip(" ")
    temp=line.txt.split()
    temp=temp[0]
    labelRules=re.search('^[A-F][A-F0-9_]+$',temp) #checks that label starts only with letter, and only contains letters, numbers, and underscores and is only uppercase
    if re.search==None:
        line.txt="ERROR INVALID CONSTANT NAME" 
def isinList(list,string):
    for line in list:            
            temp=line.txt.strip(" ")
            temp=line.txt.split()
            temp=temp[0]
          #  print("Comparing to:" + temp)
            if string==temp:
                return True
#Phase 3 todo:
#scan for registers and insert them in single operand, and inc dec instructions (done for inc and dec)
#also scan and insert registers for indexed mode (done)
#generate additional instruction data from the value of labels, format it, and append it
#swap the bytes in everything as necessarry to display properly
#add inc/dec case to operand searching, maybe move it to jumps(done)
#compare all operands to iar, but everything except jump looks fine, just need to grab additional data now
#still need to pull index value
def Scan(line,type,labelDict,validRegisters,doubleOperand,jump,singleOperand,currentMemAddress): #type 0 indicates label before code. type -1 indicates no label before code
    tempText=line.txt.strip(" ")
    tempText=tempText.split()
    discoveredOperation=0
    Ad=0
    Ab=0
    As=0
    #tempText=tempText.strip()
    #if len(tempText)<=1:
    #    return currentMemAddress
    numWordsInstruction=0
    tempVal=0

   
        
    if len(tempText)>2:
        tempText[type+2]=tempText[type+2].strip(',')

    if tempText[type+1] in doubleOperand: #valid double operand instruction
            operand=type+1
            val=operand+1
            count=0
            line.opCode=doubleOperand[tempText[operand]][0] #gets the 0th element of the tuple in the operand dictionary, hopefully
            #print(line.memAddress)

            #if.b grab LSB of val and 0 out the rest
            #do addressing mode stuff here
            ### tempText[0] is label
            if tempText[type+1]== 'inc' or tempText[type+1]== 'dec':
                line.opCode=doubleOperand[tempText[operand]][0]
                line.opCode+=doubleOperand[tempText[operand]][1]<<4
                reg=re.search('R?[0-1][0-5]',tempText[val])
                if reg.group(0) in validRegisters:
                    line.opCode+=validRegisters[reg.group(0)]
                else:
                    line.txt=line.txt+ ' ERROR: ATTEMPTED TO INC OR DEC INVALID REGISTER'
                discoveredOperation=1
            else:
                validFormat=re.search('[a-zA-z0-9#&]+, [a-zA-z0-9#&]+',line.txt)
                validFormat2=re.search('[0-9]+\([a-zA-z0-9#&]+\), [0-9+]\([a-zA-z0-9#&]+\)',line.txt)

                for i in range (0,2):
                    
                    #find source addressing mode first
                    #indexedMode=re.search() #regulare expression for indexed value
                    if len(tempText)<=2 and i==0:
                        line.txt=line.txt + 'ERROR: MISSING OPERAND'
                        break
                   
                    elif validFormat or validFormat2:
                        print() 
                    else:
                        if 'ERROR: MISSING OPERAND' in line.txt:
                            print()
                        else:
                            line.txt=line.txt+' ERROR: MISSING OPERAND'
                    if tempText[val] in validRegisters:
                        if count==0: #checks source first
                            line.addressingData[2]=0
                            line.addressingData[3]=0
                            line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                            line.adbwas+=0
                            line.opCode+=validRegisters[tempText[val]]<<8 #should be S Reg for double operand, so grab the register number, shift it left 8 times
                        elif count==1: #then check dest
                            line.addressingData[0]=0
                            line.adbwas+=0
                            line.opCode+=validRegisters[tempText[val]] #D reg.
                            #line.addressingData[3]=0
                        #source addressing mode= register
                        #we'll want to add the register value into OpCode
                        #inc and dec are special cases, ignore the source
                        numWordsInstruction+=0 #source is a register so no additional data in insturction so far
                    elif '#' in tempText[val]: #checking if source is immediately addressed
                        #check if tempText[2] is a valid label, summation of labels, or some other weird garbage
                        if '+' in tempText[val]:
                            summedAddrVal=0
                            splitAdd=tempText[val].split('+')
                            #loc=splitAdd.index('+')
                            if splitAdd[0].strip('#') in labelDict: #valid label
                                #would get memory address of label here and add it into data
                                numWordsInstruction+=1
                                summedAddrVal+=labelDict[splitAdd[0].strip('#')]
                                if count==0:
                                    line.addressingData[2]=1
                                    line.addressingData[3]=1
                                    line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                                    line.adbwas=0x3+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                elif count==1:
                                    line.txt='Cannot Use Immediate Addressing On Destination'
                            elif re.search('^(0[xX])?[A-Fa-f0-9]+$',splitAdd[0].strip('#')) :
                                numWordsInstruction+=1
                                strippedVal=re.search('^(0[xX])?[A-Fa-f0-9]+$',splitAdd[0].strip('#')).group(0) #should be str
                                line.instructionData.append(hex(int(strippedVal,16)))#get the immediate value
                                #this only comes up if Label+val, so dont worry about it for now, I guess
                                #also, dont forget to account for non hex vals
                                if count==0:
                                    line.addressingData[2]=1
                                    line.addressingData[3]=1
                                    line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                                    line.adbwas=0x3+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                elif count==1:
                                    line.txt='Cannot Use Immediate Addressing On Destination'
                            if splitAdd[1].strip(',') in labelDict: #valid label
                                #would get memory address of label here and add it into data
                                numWordsInstruction=1
                                summedAddrVal+=labelDict[splitAdd[1].strip(',')]
                                line.instructionData.append(format(summedAddrVal,'04X')) #add sum to instruction word
                                if count==0:
                                    line.addressingData[2]=1
                                    line.addressingData[3]=1
                                    line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                                    line.adbwas=0x3+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                elif count==1:
                                    line.txt='Cannot Use Immediate Addressing On Destination'
                            elif re.search('^(0[xX])?[A-Fa-f0-9]+$',splitAdd[1].strip(',')) :
                                  numWordsInstruction+=1
                                  strippedVal=re.search('^(0[xX])?[A-Fa-f0-9]+$',splitAdd[0].strip('#')).group(0) #should be str
                                  line.instructionData.append(format(int(strippedVal,16)),'04X')
                                  if count==0:
                                        line.addressingData[2]=1
                                        line.addressingData[3]=1
                                        line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value                               
                                        line.adbwas=0x3+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form

                                  elif count==1:
                                        line.txt='Cannot Use Immediate Addressing On Destination'
                                #this only comes up if Label+val, so dont worry about it for now, I guess
                        else:
                            split=tempText[val].strip("#,") # get rid of the hash
                            if split in labelDict:
                                #valid label, grab its memory address and add it to instruction data
                                #this is gonna be a problem if we try to jump to a program label we've yet to set. dunno how to fix that
                                #line.instructionData.append(labelDict[split]) #go ahead and store the value/mem Address here
                                numWordsInstruction+=1
                                if count==0:
                                    line.addressingData[2]=0
                                    line.addressingData[3]=1
                                    line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                                    line.adbwas=0x3+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                    if line.isEqu==0:
                                        line.instructionData.append(format(labelDict[split],'04X'))
                                elif count==1:
                                    line.txt=line.txt+' ERROR:INVALID DESTINATION ADDRESSING MODE'
                            else:
                                print(split)
                                regEx=re.search('^(0[xX])?[A-Fa-f0-9]+$',split) #checks if its a constant value hopefully
                                if regEx: # if not null
                                    numWordsInstruction+=1
                                   # print(split+'Immediate Value Identified')
                                    
                                    if count==0:
                                        line.addressingData[2]=0
                                        line.addressingData[3]=1
                                        line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                                        line.adbwas=0x3+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                        line.instructionData.append(format(int(split,16),'04X'))
                                    elif count==1:
                                        line.txt=line.txt+' ERROR:INVALID DESTINATION ADDRESSING MODE'
                                else:
                                    regEx=re.search('^0x{[A-Fa-f0-9]+$}',split) #checks if its a constant value hopefully
                                    if regEx:
                                            numWordsInstruction+=1
                                            
                                            if count==0:
                                                    line.instructionData[0]=format(hex(int(split,16)),'04X')
                                                    line.addressingData[2]=0
                                                    line.addressingData[3]=1
                                                    line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                                                    line.adbwas=0x3+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                            elif count==1:
                                                    line.txt=line.txt+' ERROR:INVALID DESTINATION ADDRESSING MODE'
                                    else:
                                        line.txt=line.txt+'ERROR: INVALID IMMEDIATE SOURCE VALUE'
                                        #break
                                        #not a valid label or number so throw an error
                    elif '&' in tempText[val]: 
                        tempAbsVal=tempText[val].strip('&')    
                        regEx=re.search('^(0[xX])?[A-Fa-f0-9]+$',tempAbsVal)
                        decAddress=re.search('^[0-9]+$',tempAbsVal)
                        if tempAbsVal in labelDict:
                            #valid label, pull the label out, increment the numWordsInstruction by 1
                            numWordsInstruction+=1
                            line.instructionData.append(format(labelDict[tempAbsVal],'04X')) #get val or mem Address and add it to instruction data
                            if count==0:
                                    line.addressingData[2]=0
                                    line.addressingData[3]=1
                                    line.addressingData[1]=tempText[operand][1] #b/w value
                                    line.adbwas=0x1+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                            elif count==1:
                                    line.addressingData[0]=1
                                    line.adbwas+=8
                        elif regEx: #valid hex addressing mode
                            numWordsInstruction+=1
                            line.insturctionData.append(format(hex(int(labelDict[tempAbsVal],16)),'04X'))
                            if count==0:
                                line.addressingData[2]=0
                                line.addressingData[3]=1
                                line.addressingData[1]=tempText[operand][1] #b/w value
                                line.adbwas=0x1+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                            elif count==1:
                                line.addressingData[0]=1
                                line.adbwas+=8
                        elif decAddress:
                            numWordsInstruction+=1
                            line.instructionData.append(format(hex(int(labelDict[tempAbsVal],16)),'04X'))
                            if count==0:
                                    line.addressingData[2]=0
                                    line.addressingData[3]=1
                                    line.addressingData[1]=tempText[operand][1] #b/w value
                                    line.adbwas=0x1+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                            elif count==1:
                                    line.addressingData[0]=1
                                    line.adbwas+=8
                        else:
                            line.txt=line.txt+' ERROR:INVALID ABSOLUTE ADDRESS'
                    #look for absolute mdoe
                    elif re.search('^[A-Fa-f0-9]+\(R?[0-1][0-5]\)',tempText[val]):       #look for indexed mode with hex index
                        #print('Successfull Index Mode match')
                        reg=re.search('R?[0-1][0-5]',tempText[val])
                        index=re.search('^[A-Fa-f0-9]+',tempText[val]).group(0)
                        
                        if count==0: #check if first char is 0, if it is only add to instruction word if evaluating operands
                                    line.addressingData[2]=0
                                    line.addressingData[3]=1
                                    line.addressingData[1]=doubleOperand[tempText[operand]][1] #b/w value
                                    line.adbwas=0x1+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                    line.opCode+=validRegisters[reg.group(0)]<<8
                                    if re.search('^[0]+\(R?[0-1][0-5]\)',tempText[val]):
                                            numWordsInstruction+=0 #0th index on first case, this gets optimized out for wahtever reason
                                            line.addressingData[2]=0    #looks like 0(RX) on source register gets treated as register mode in IAR
                                            line.addressingData[3]=0
                                    else:
                                        numWordsInstruction+=1
                                        line.instructionData.append(format(int(index,16),'04X'))

                        elif count==1:
                                    line.addressingData[0]=1
                                    line.adbwas+=8
                                    numWordsInstruction+=1
                                    line.opCode+=validRegisters[reg.group(0)]
                                    line.instructionData.append(format(int(index,16),'04X'))

                    elif re.search('^[A-Fa-f0-9]+\(R?[0-1][0-5]\)',tempText[val]):       #I think this loop is probably identical and can be removed
                       # print('Successfull Index Mode match')
                        reg=re.search('R?[0-1][0-5]',tempText[val])
                        index=re.search('^[A-Fa-f0-9]+',tempText[val]).group(0)
                        if count==0:
                                    line.addressingData[2]=0
                                    line.addressingData[3]=1
                                    line.addressingData[1]=doubleOperand[tempText[operand]][1]
                                    line.adbwas=0x1+4*doubleOperand[tempText[operand]][1] # should get adbwas value in numeric form
                                    line.opCode+=validRegisters[reg.group(0)]<<8
                                    if re.search('^[0]+\(R?[0-1][0-5]\)',tempText[val]):
                                            numWordsInstruction+=0
                                    else:
                                        numWordsInstruction+=1
                                        line.instructionData.append(format(int(index,16),'04X'))
                        elif count==1:
                                    line.addressingData[0]=1
                                    line.adbwas+=8
                                    numWordsInstruction+=1
                                    line.opCode+=validRegisters[reg.group(0)]
                                    line.instructionData.append(format(int(index,16),'04X'))
                        #else invlaid source mode error
                    val+=1
                    count+=1
            #end loop here
            #print(outboundMemAddress)
          
            line.opCode+=line.adbwas<<4
            discoveredOperation=1
            line.opCode=format(line.opCode,'04X')
    if discoveredOperation==0:
            tempVal=singleOperandScan(line,type,labelDict,singleOperand,currentMemAddress)
            numWordsInstruction=tempVal
            if numWordsInstruction==0:
                tempVal=jumpScan(line,type,labelDict,jump,currentMemAddress)
                numWordsInstruction=tempVal
                discoveredOperation=1
                line.opCode=format(line.opCode,'04X')
                return int(currentMemAddress+2*numWordsInstruction)
                if numWordsInstruction==0:
                    line.txt=line.txt+' ERROR:INVALID OPERAND OR INSTRUCTION'

        
    outboundMemAddress=currentMemAddress+2*numWordsInstruction+2
    return int(outboundMemAddress)
def singleOperandScan(line,type,labelDict,singleOperand,currentMemAddress): #only valid infor here is function call labels this should probably be called as
##strip out each line into array of Line objects
 numWordsInstruction=0
 tempText=line.txt #emulated call technically supports more opcodes but it dosent come up in any of the code so far
 tempText=tempText.strip(' ')
 tempText=tempText.split()
 if tempText[type+1] in singleOperand: #valid double operand instruction
            line.opCode=format(singleOperand[tempText[type+1]],'04X') #gets the 0th element of the tuple in the operand dictionary, hopefully
            
            #print(line.memAddress)
            #if.b grab LSB of val and 0 out the rest
            #do addressing mode stuff here
            operand=type+1
            ### tempText[0] is label
           
            if  line.memAddress!='000000': #intermediate instruction not directly following a known memory address
                currentMemAddress=int(line.memAddress,16)
                print(line.memAddress)
            else:
                line.memAddress=format(currentMemAddress,'06X')
            #find source addressing mode first
            #indexedMode=re.search() #regulare expression for indexed value
            if operand+1<len(tempText):
                if tempText[operand+1].strip('#') in labelDict:
                    #source addressing mode= register
                    #we'll want to add the register value into OpCode
                    #inc and dec are special cases, ignore the source
                    numWordsInstruction+=1 #source is a register so no additional data in insturction so far
                    #if tempText[type+1]==call:

                    line.instructionData.append(format(labelDict[tempText[operand+1].strip('#')],'04X'))
                    if line.instructionData[0]=='0000':
                        line.instructionData.remove('0000')
                    line.isCall=1
            else: return 1    
            #end loop here
            outboundMemAddress=currentMemAddress+2*numWordsInstruction
            print(outboundMemAddress)
            return int(numWordsInstruction)
 else: 
    return 0
def jumpScan(line,type,labelDict,jumps,currentMemAddress): #only valid to jump to labels
    numWordsInstruction=0
    tempText=line.txt.strip(' ')
    tempText=tempText.split()
    offset=0
    #offset = (pcNew-PcOld-2)/2
    #offset caps at 9 bits, signed 9 bit int
    #looks like this gets ingored for jz/jnz though
    if tempText[type+1] in jumps: #valid double operand instruction
                line.opCode=jumps[tempText[type+1]][0] #gets the 0th element of the tuple in the operand dictionary, hopefully
                #print(line.memAddress)
                #if.b grab LSB of val and 0 out the rest
                #do addressing mode stuff here
                operand=type+1
                ### tempText[0] is label
                numWordsInstruction=0
           
                if  line.memAddress!='000000': #intermediate instruction not directly following a known memory address
                    currentMemAddress=int(line.memAddress,16)
                    print(line.memAddress)
                else:
                    line.memAddress=format(currentMemAddress,'06X')
                #find source addressing mode first
                #indexedMode=re.search() #regulare expression for indexed value
                if tempText[type+2] in labelDict:
                    #source addressing mode= register
                    #we'll want to add the register value into OpCode
                    #inc and dec are special cases, ignore the source
                    numWordsInstruction+=1 #source is a register so no additional data in insturction so far
                    destination=labelDict[tempText[type+2]] #pc new
                    if currentMemAddress<=destination and line.isJump==1:
                        offset=int((destination-currentMemAddress-2)/2)
                    elif currentMemAddress>destination and line.isJump==1:
                        offset=int((destination-currentMemAddress-2)/2)
                    if offset<=512*16 and offset>=-511*16 and line.isJump==1:
                        line.instructionData.append(offset)
                    elif line.isJump==1:
                        line.txt=line.txt+" ERROR INVALID OFFSET SIZE"
                    line.isJump=1
                else:
                    line.txt+=' ERROR: INVALID JUMP DESTINATION'
                #end loop here
                outboundMemAddress=currentMemAddress+2*numWordsInstruction
                print(outboundMemAddress)
                return int(numWordsInstruction)
    else:
        line.txt=line.txt+' ERROR: INVALID INSTRUCTION'
        return 0

with open(fileInput,"r") as inFile: #use "w" to write
#    inFileContents=inFile.read()
# print(inFileContents)
    inLines = []
    labels = []
    labeltxt = []
    count=0
    knownMemAddress=0
    currentMemAddress=0x0000
    inLines.append(Line(inFile.readline()))
    inLines[0].txt=inLines[0].txt.strip()
    for line in inFile:
        inLines.append(Line(line.strip('\n\r')))
        count+=1
        #print(inLines[count].str)
lineNumber=0;
for line in inLines:
    lineNumber+=1

    temp2=line.txt.strip(" ")
    temp2=line.txt.split()  
    if line.txt[:1]==';': #this is a comment line, iterate the line number and move on
        if knownMemAddress==0:
            line.setMemAddress(format(0x0000,'06X'))
        elif knownMemAddress==1:
            line.setMemAddress(format(currentMemAddress,'06X'))
        line.setlineNumber(lineNumber)
    elif line.txt[:1]==' ': #blank line, means theres code
        #other opcode logic goes in here, may want to make it a function later
        if " ORG " in line.txt:
            currentMemAddress=int(line.txt[(line.txt.find("0x")):(line.txt.find("0x")+6)],16) #address needs to be stripped off as hex or int
            line.setMemAddress(format(currentMemAddress,'06X'))   
            line.labelOrVar
           # print(currentMemAddress)
            knownMemAddress=1
        elif " DW " in line.txt: #or other thing that goes on when DW RESET happens
                        if currentMemAddress % 2 ==0: #even address
                            temp=line.txt.strip(" ")
                            temp=line.txt.split()
                            temp=temp[1]
                            currentMemAddress+=2  
                        else:
                            temp=currentMemAddress+1
                            currentMemAddress=temp# odd adress, increment to even then set
                            line.memAddress=format(currentMemAddress,'06X')
                            temp=currentMemAddress+2
                            currentMemAddress=temp
                        #validateLabel(labels,line)
                        knownMemAddress=1
        elif " END " in line.txt:  
           line.setMemAddress(format(currentMemAddress,'06X'))
           line.end=1
        elif knownMemAddress==1 and line.txt.isspace(): #empty line, no mem address change
            line.setMemAddress(format(currentMemAddress,'06X'))
        elif knownMemAddress==1 and line.txt.isspace()!=1: #nonempty line check if exclusively comment
            temp=line.txt.strip(" ")
            temp=line.txt.split()
          #  print (temp)
            if(temp[0]==';'): #blank line with a comment
                line.setMemAddress(format(currentMemAddress,'06X'))
            else: # this will need to go away aventually
                line.setMemAddress(format(0x0000,'06X'))
                knownMemAddress=0
        else:
            line.setMemAddress(format(0x0000,'06X'))
            knownMemAddress=0
        #gonna have to do more adressing garbage here
    elif line.txt=='':
        if knownMemAddress==1:
            line.setMemAddress(format(currentMemAddress,'06X'))
        else:
            line.setMemAddress(format(0x0000,'06X'))


    elif line.txt[:1]!=' ' and line.txt[:2]!='': #non space character, aka label
             #print("Non Space Line, supposedly" + line.txt)
             if " DB " in line.txt: #RAM variable byte
                if validateLabel(labels,line,0)==False:             
                    line.memAddress=format(currentMemAddress,'06X')
                    currentMemAddress+=1       
                    knownMemAddress=1
                    labels.append(line)
                else:# do not process incorrect labels
                    #labels.append(line)
                    line.memAddress=format(currentMemAddress,'06X')
             elif " DW " in line.txt: #RAM variable word
                 if validateLabel(labels,line,0)==False:             
                    if currentMemAddress % 2 ==0: #even address
                        line.memAddress=format(currentMemAddress,'06X')
                        currentMemAddress+=2  
                    else:
                        temp=currentMemAddress+1
                        currentMemAddress=temp# odd adress, increment to even then set
                        line.memAddress=format(currentMemAddress,'06X')
                        temp=currentMemAddress+2
                        currentMemAddress=temp
                    validateLabel(labels,line,0)          #MOVDED THIS FROM  LOOP  
                    knwonMemAddress=1
                    labels.append(line)
             elif " DS " in line.txt: #Declare Storage
                 if validateLabel(labels,line,0)==False:             
                     line.memAddress=format(currentMemAddress,'06X')
                     temp=line.txt.strip(" ")
                     temp=line.txt.split()
                     #print(temp)
                     currentMemAddress+=int(temp[2]) #add storage size
                     knownMemAddress==1
                     labels.append(line)
             elif " EQU " in line.txt: #constant
                if validateLabel(labels,line,1)==False:                 
                     temp=line.txt.strip(" ")
                     temp=line.txt.split()
                     #print(temp)
                     if(len(temp)==3): #using a constant, not an adressing mode for adressing
                        line.setMemAddress(format(int(temp[2],16),'06X')) #grab the constant out and set it in the mem address location
                        labels.append(line) #add line to symbol table
                     elif('$' in temp): #using some kind of adress mode, this one looks for $ specifically
                         if(temp[temp.index('$')+1]=='-'): #$-label
                                for i in labels:
                                    if temp[temp.index('$')+2] in i.txt: #grab label from matching labe
                                       line.setMemAddress(format(currentMemAddress-int(i.memAddress,16),'06X'))
                                       labels.append(line)
                                       break
                     line.isEqu=1

             else: #we are not a EQU,DB,DS,or DW, evaulate if code is following the label that would change the address
                temp=line.txt.strip(" ") 
                if temp.isspace!=True:
                    temp=line.txt.split()
                    temp=temp[0]
                    #print(line.txt)
                    if(knownMemAddress==1):
                        line.memAddress=format(currentMemAddress,'06X') #cuurentMemAddress needs to go here next phase
                    else:
                        line.memAddress=format(0x0000,'06X')
                    if len(temp)>1: #there is more than just the label here, eg code
                        knownMemAddress=0
                    if validateLabel(labels,line,1)==False:
                        labels.append(line)
    line.setlineNumber(lineNumber)
    #########################################END PHASE 1############################
doubleOperand={'add':(0x5000,0),'add.w':(0x5000,0),'add.b':(0x5000,1),'and':(0xF000,0),'and.w':(0xF000,0),'and.b':(0xF000,1),
               'bic':(0xC000,0),'bic.w':(0xC000,0),'bic.b':(0xC000,1),'bis':(0xD000,0),'bis.w':(0xD000,0),'bis.b':(0xD000,1),
               'bit':(0xB000,0),'bit.w':(0xB000,0),'bit.b':(0xB000,1),'cmp':(0x9000,0),'cmp.w':(0x9000,0),'cmp.b':(0x9000,1),
               'mov':(0x4000,0),'mov.w':(0x4000,0),'mov.b':(0x4000,1),'inc':(0x5300,1),'dec':(0x8300,1)} 
                #all valid 2 operand instructions to be hashed (includes inc dec emulated instructions)
                #opcodes aren't byte swapped yet
singleOperand={'call':(0x12B0),'ret':(0x4130)} #call needs to store subroutine location which is branched to/loaded by ret may be B0 according to assmebler
#best guess is that 12B0 is some emulated instruction replacing the call from the family guide
#call should include label adress symbolic mode style, bet ret just uses the opcode
jumps={'jnz':(0x2400,0),'jz':(0x2800,0)} # these starting values disagree with the datasheet, but they seem to be what IAR uses. data sheet says 2000,2400

labelDict={}
#jumps store the label address and do not accept immediate adressing
validRegisters={'R0':0x0,'R1':0x1,'R2':0x2,'R3':0x3,'R4':0x4,'R5':0x5,'R6':0x6,'R7':0x7,
                'R8':0x8,'R9':0x9,'R10':0xA,'R11':0xB,'R12':0xC,'R13':0xD,'R14':0xE,
                'R15':0xF,'PC':0x0,'SP':0x1,'SR':0x2} #dictionary of allowable register values as well as PC, SP, and SR labels (check on SR being valid label)
for line in labels: #strip them semi colons out of the label dict
        temp=line.txt.strip(" ")
        temp=line.txt.split()
        temp[0]=temp[0].strip(':')
        labelDict[temp[0]]=int(line.memAddress,16) #create a dictionary keyed to the label containing value/mem address

currentMemAddress=000000    
foundEnd=0
for line in inLines:
    #tempText=line.txt.split(',')
    #tempText=tempText.strip()
  #print(line.txt)
    if line.end==1: #dont process anything further than this
        line.opCode=format(line.opCode,'04X')
        foundEnd=1
        break;
    if line.txt=="ERROR DUPLICATE LABEL": #error catching
        #dont try to process this
        line.txt="ERROR DUPLICATE LABEL: ADDRESSES AFTER THIS POINT MAY BE INVALID"
        if  line.memAddress!='000000': # org statement of some kind, mem address is already calculated, so leave it lone
            currentMemAddress=int(line.memAddress,16)
            print(format(currentMemAddress,'06X'))
        else:
            line.memAddress=format(currentMemAddress,'06X')
    if line.txt[:1]!=' ' and line.txt[:1]!=';' and checkIfVar(line) or ' ORG ' in line.txt:
        if  line.memAddress!='000000': # org statement of some kind, mem address is already calculated, so leave it alone     
            if ' DS ' in line.txt:
                temp=line.txt.strip(" ")
                temp=line.txt.split()
                currentMemAddress=int(line.memAddress,16)+int(temp[2])
            else:
                currentMemAddress=int(line.memAddress,16)
                print(format(currentMemAddress,'06X'))
        else:
            line.memAddress=format(currentMemAddress,'06X')
    elif line.txt[:1]!=' ' and line.txt[:1]!=';' and checkIfEqu(line): #if equ statement, we dont want to pull the mem address
      validateEqu(line)
    elif line.txt[:1]!=' ' and line.txt[:1]!=';' and line.txt[:1]!='': #this has got to be a label that is not an org or equ
                line.memAddress=format(currentMemAddress,'06X')
                strippedText=line.txt.strip(" ")
                strippedText=line.txt.split()
                if len(strippedText)<=1: #just a label, no instruction
                    line.memAddress=format(currentMemAddress,'06X')
                else:
                    if strippedText[0] in doubleOperand or strippedText[0] in jumps or strippedText[0] in singleOperand:
                        line.text="ERROR CANNOT HAVE INSTRUCTION IN LEFTMOST COLUMN"
                    else:
                        tempVal=Scan(line,0,labelDict,validRegisters,doubleOperand,jumps,singleOperand,currentMemAddress)
                        currentMemAddress=tempVal
    elif line.txt[:1]=='' or line.txt[:1]==';': #blank lines or comment
            if len(line.txt.strip())>0:
                if line.txt[:1]!=';':
                    line.txt=line.txt + ' ERROR: INVALID LEFT COLUMN'
            line.memAddress=format(currentMemAddress,'06X')
    else: #intruction here
        line.memAddress=format(currentMemAddress,'06X')
        strippedText=line.txt.strip(" ")
        strippedText=line.txt.split()
        columnCheck=re.search('^ [a-zA-Z]',line.txt)
        if columnCheck:
                line.txt=line.txt + ' ERROR: INVALID COLUMN'
        elif  line.txt.isspace():
                line.memAddress=format(currentMemAddress,'06X')
        elif strippedText[0]==';': #just a label, no instruction
            line.memAddress=format(currentMemAddress,'06X')
        else:
            if  strippedText[0]=='DB': #RAM variable byte
                #if validateLabel(labels,line,0)==False:             
                line.memAddress=format(currentMemAddress,'06X')
                currentMemAddress+=1       
                #knownMemAddress=1
                #labels.append(line)
                #else:# do not process incorrect labels
                    #labels.append(line)
                 #   line.memAddress=format(currentMemAddress,'06X') 
            elif strippedText[0]=='DW':
                line.memAddress=format(currentMemAddress,'06X')
                currentMemAddress+=2 
            else:
                tempVal=Scan(line,-1,labelDict,validRegisters,doubleOperand,jumps,singleOperand,currentMemAddress)
                currentMemAddress=tempVal
    if line.opCode==0:
        line.opCode=format(line.opCode,'04X')
for line in labels: #catch label values again
    temp=line.txt.strip(" ")
    temp=line.txt.split()
    temp[0]=temp[0].strip(':')
    labelDict[temp[0]]=int(line.memAddress,16) #create a dictionary keyed to the label containing value/mem address
for line in inLines:

    if line.isJump==1 and line.txt[:1]!=' ':
        tempVal=jumpScan(line,0,labelDict,jumps,int(line.memAddress,16))
    elif line.isJump==1 and line.txt[:1]==' ':
        tempVal=jumpScan(line,-1,labelDict,jumps,int(line.memAddress,16))
    if line.isJump==1:
        if line.instructionData: #there is instruction data
            line.opCode+=line.instructionData[0] #off set is calculated in words, mem is adressed in bytes
            line.opCode=format(line.opCode,'04X')
            line.instructionData.remove(line.instructionData[0])
    if line.isCall==1 and line.txt[:1]!=' ':
        tempVal=singleOperandScan(line,0,labelDict,singleOperand,int(line.memAddress,16))
    elif line.isCall==1 and line.txt[:1]==' ':
        tempVal=singleOperandScan(line,-1,labelDict,singleOperand,int(line.memAddress,16))
for line in inLines: #find DW,DB, encode them
    if line.txt[:1]!=';' and line.txt[:2]!='': #non space character, aka label
             #print("Non Space Line, supposedly" + line.txt)
             if " DB " in line.txt: #RAM variable byte
                temp=line.txt.strip('')
                temp=line.txt.split()
                if len(temp)>=3:
                    varVal=re.search('^\'.\'',temp[2])   #this is looking for an ascii char val encoding 
                    if varVal:  #get ascii value and encode it 
                        val=format(ord(temp[2].strip('\'')),'02X')
                    else:
                        if len(temp[2].strip('\''))>1: #trying to encode more than a byte, grab it and ignore it
                            temp[2]=list(temp[2])[1]
                            line.txt=line.txt+'\t'+'WARNING:ATTEMPTENTING TO WRITE >1 B INTO BYTE ADDRESS'
                        val=format(int(temp[2],16),'02X')
                elif temp[1] in labelDict: #DW RESET Case
                    val=foramt(labelDict[temp[1]],'02X')
                elif re.search('^\'.\'',temp[1]):
                    val=format(ord(temp[1].strip('\'')),'02X')
                line.opCode=val
             elif " DW " in line.txt: #RAM variable word
                temp=line.txt.strip('')
                temp=line.txt.split()
                if len(temp)>=3:
                    varVal=re.search('^\'.{2}\'',temp[2])   #this is looking for an ascii char val encoding 
                    if varVal:  #get ascii value and encode it 
                        val=format(ord(temp[2].strip('\'')),'04X')
                    elif temp[1] in labelDict:
                            val=format(labelDict[temp[1]],'04X')
                    else:    
                        if len(temp[2].strip('\''))>2: #trying to encode more than a byte, grab it and ignore it
                            temp[2]=list(temp[2])[0]
                            line.txt=line.txt+'\t'+'WARNING:ATTEMPTENTING TO WRITE >1 W INTO WORD ADDRESS'
                        val=format(int(temp[2],16),'04X') 
                    line.opCode=val
                #add in size value for DS here
             elif ' DS ' in line.txt:
                temp=line.txt.strip('')
                temp=line.txt.split()
                if len(temp)>=3:
                    varVal=re.search('^\'.{2}\'',temp[2])   #this is looking for an ascii char val encoding 
                    if varVal:  #get ascii value and encode it 
                        val=format(ord(temp[2].strip('\'')),'04X')
                    elif temp[1] in labelDict:
                            val=format(labelDict[temp[1]],'04X')
                    else:    
                        if len(temp[2].strip('\''))>2: #trying to encode more than a byte, grab it and ignore it
                            temp[2]=list(temp[2])[0]
                            line.txt=line.txt+'\t'+'WARNING:ATTEMPTENTING TO WRITE >1 W INTO WORD ADDRESS'
                        val=format(int(temp[2],16),'04X')  
                line.opCode=val      
    elif ' DB ' in line.txt:
        temp=line.txt.strip('')
        temp=line.txt.split()
        if len(temp)>=3:
            varVal=re.search('^\'.\'',temp[2])   #this is looking for an ascii char val encoding 
            if varVal:  #get ascii value and encode it 
                val=format(ord(temp[2].strip('\'')),'02X')
            else:
                if len(temp[2].strip('\''))>1: #trying to encode more than a byte, grab it and ignore it
                    temp[2]=list(temp[2])[1]
                    line.txt=line.txt+'\t'+'WARNING:ATTEMPTENTING TO WRITE >1 B INTO BYTE ADDRESS'
                val=format(int(temp[2],16),'02X')
        elif temp[1] in labelDict: #DW RESET Case
            val=foramt(labelDict[temp[1]],'02X')
        line.opCode=val
for line in inLines:
    #concatenate opcodes to address data here
    #swaps opcode bytes to format stored in memory
    if line.opCode:
        count=0
        tempOpcode=[]
        for char in line.opCode:
            tempOpcode.append(char)
        if len(tempOpcode)==4:
            tempOpcode[0],tempOpcode[1],tempOpcode[2],tempOpcode[3]=tempOpcode[2],tempOpcode[3],tempOpcode[0],tempOpcode[1] #swap bytes
            line.opCode="".join(tempOpcode)
    for data in line.instructionData:
        tempData=[]
        for char in data:
            tempData.append(char)
        tempData[0],tempData[1],tempData[2],tempData[3]=tempData[2],tempData[3],tempData[0],tempData[1]
        tempData="".join(tempData)
        line.instructionData="".join(tempData)
        line.opCode="".join([line.opCode,line.instructionData])

        #currentMemAddress=tempVal
    #if line.instructionData:
    #    for i in range(0,len(line.instructionData)):
    #        line.instructionData[i]=format(line.instructionData[i],'06X')

        #tempVal=Scan(line,0,labelDict,validRegisters,doubleOperand,jumps,singleOperand,currentMemAddress)
        #if tempVal:
        #    currentMemAddres=tempVal     
        #TODO:
        #1. shift actual labels and memory address into a dictionary (Done probably)
        #2.Isolate instruction from string in line.txt, check for valid instruction and retrieve opcode and b/w data (Also done, probably)
        #3.Identify As/Ad and use that information to create a valid instruction and determine instruction data length(register, indexed absolute and immediate modes)
        #4.Update memory address of all 0x0000 addressed lines done
        #5.Create predifined system constants such as R15 and P1DIR that can be used to generate valid instruction dat
##return each line into the output file

objFileArray=['CarterConlin','00','FF00AA55']
orgLocations=[]
count=1
opcodes=0
secondCount=1
numBytes=0
sectionNum=1
sectionSizes=[]
numOpCodes=[]
for line in inLines: #generate obj file
    #obj file should be a huge byte array, we just need to scan through, find orgs, and cast opcodes/instruction data to hex then to valid ascii byte values
    #dont forget checksum
    #dont forget obj file needs byte numbres
    #this should just find orgs and count the number of bytes in each segment    
    if 'ORG' in line.txt or 'END' in line.txt :
        #catch orgs here
        print(line.memAddress)
        if 'END' in line.txt:
            sectionSizes.append(numBytes)
            numOpCodes.append(opcodes)
            opcodes=0
            numBytes=0
        else:
            orgLocations.append(count)
            sectionSizes.append(numBytes)
            numOpCodes.append(opcodes)
            opcodes=0
            numBytes=0
            objFileArray.append(format(int(line.memAddress,16),'04X'))
    elif line.opCode!='0000' or 'DB' in line.txt or 'DW' in line.txt and 'ERROR' not in line.txt: #should catch DBs etc, as well as instructions
        temp=len(list(str(line.opCode)))
        numBytes+=int(temp/2)
        opcodes+=1
    elif 'DS' in line.txt:
        count=0 #swap the DS bytes back
        tempOpcode=[]
        temp2=[]
        for char in line.opCode:
            tempOpcode.append(char)
        if len(tempOpcode)==4:
            tempOpcode[0],tempOpcode[1],tempOpcode[2],tempOpcode[3]=tempOpcode[2],tempOpcode[3],tempOpcode[0],tempOpcode[1] #swap bytes
            temp2="".join(tempOpcode)
        opcodes+=1
        numBytes+=int(temp2,16)
    count+=1
insertionIndex=0
sectionIndex=0
assemble=1
##############NEED TO SAVE DB AND DS VALUES AND ENCODE THEM AS OPCODE
for line in inLines:#second pass
    if 'ERROR:' in line.txt:
        assemble=0
    if line.end==1:
        break
    if secondCount in orgLocations:
        if sectionNum==1:
            objFileArray.insert(4,format(sectionSizes[sectionNum],'04X'))
            #objFileArray.insert(5,'FF00AA55')
            insertionIndex=5
        else:
            sectionIndex=0
            objFileArray.insert(insertionIndex+numOpCodes[sectionNum-1],'FF00AA55')
            if insertionIndex+numOpCodes[sectionNum-1]+2 < len(objFileArray):
                objFileArray.insert(insertionIndex+numOpCodes[sectionNum-1]+2,format(sectionSizes[sectionNum],'04X'))
            else:
                objFileArray.append(format(sectionSizes[sectionNum],'04X'))
            #objFileArray.insert(6+sectionSizes[sectionNum],'FF00AA55')
            insertionIndex=insertionIndex+numOpCodes[sectionNum-1]+3
        sectionNum+=1
    elif line.opCode!='0000'  and 'ERROR' not in line.txt:
        if insertionIndex+sectionIndex<len(objFileArray): #insert into the list
            objFileArray.insert(insertionIndex+sectionIndex,line.opCode)
            sectionIndex+=1
        else:#end of list, append value
            objFileArray.append(line.opCode)
            sectionIndex+=1
    elif 'DB' in line.txt or 'DW' in line.txt  and 'ERROR' not in line.txt: #catch if DB and DW are declared 0
        if insertionIndex+sectionIndex<len(objFileArray): #insert into the list
            objFileArray.insert(insertionIndex+sectionIndex,line.opCode)
            sectionIndex+=1
        else:#end of list, append value
            objFileArray.append(line.opCode)
            sectionIndex+=1
    #if secondCount==4+sectionSizes[sectionNum]:
    #    objFileArray.append('FF00AA55')
    secondCount+=1
objFileArray.append('FFAA5500')
if assemble==1:
    with open(objFileOutput,'w') as output:
        for string in objFileArray:
            print(string+'\n')
            output.write(string)
        output.close()
    checksumString=''
    for string in objFileArray:
        checksumString=string+checksumString
    checksum=0
    for char in list(checksumString):
        checksum+=ord(char)
    with open(objFileOutput,'a') as output:
        output.write(format(checksum,'04X'))
        output.close()
with open(listFileOutput,"w") as outFile:
    for line in inLines:
        if line.opCode != '0000' or 'DB' in line.txt or 'DS' in line.txt or 'DW' in line.txt:
            outFile.write(str(line.lineNumber)+'\t'+str(line.memAddress)+'\t'+str(line.opCode)+'\t'+line.txt+'\n')
        else:
            outFile.write(str(line.lineNumber)+'\t'+str(line.memAddress)+'\t'+'\t'+'\t'+line.txt+'\n')
        print(str(line.lineNumber)+'\t'+str(line.memAddress)+'\t'+str(line.opCode)+'\t'+line.txt)
    if foundEnd==0:
        outFile.write("-------------------------ERROR: FOUND NO END STATEMENT-----------------------------")

labels=sorted(labels,key=lambda Line: Line.txt)
with open(listFileOutput,"a+") as outFile:
    outFile.write("{:<30}\t\t{}\n".format("Name","Value/Offset"))
    for line in labels:
        temp=line.txt.strip(" ")
        temp=line.txt.split()
        line.txt=temp[0]
        outFile.write("{:<30}\t\t{}\n".format(line.txt,str(line.memAddress)))
        print("{:<30}\t\t{}\n".format(line.txt,str(line.memAddress)))
    
       
    outFile.write("{:<10} {} {}\n".format("Instruction",'opcode',"b/w"))
    for instruction,(opcode, bw) in doubleOperand.items():
        #outFile.write("{:<30}\t\t{}\t\t{}\n".format(instruction,opcode,bw)
        outFile.write(instruction+' '+str(opcode)+'\t'+str(bw)+'\n')
    for instruction,opcode in singleOperand.items():
        #outFile.write("{:<30}\t\t{}\t\t{}\n".format(instruction,opcode,bw)
        outFile.write(instruction+' '+str(opcode)+'\n')
    for instruction,(opcode, bw) in doubleOperand.items():
        #outFile.write("{:<30}\t\t{}\t\t{}\n".format(instruction,opcode,bw)
        outFile.write(instruction+' '+str(opcode)+'\t'+str(bw)+'\n')
    outFile.write('Line Numbers \ AdBWAs Addressing Info \n')
    for line in inLines:
        outFile.write(str(line.lineNumber)+'\t'+str(line.addressingData)+'\n')










