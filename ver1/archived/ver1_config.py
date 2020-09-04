#!/usr/bin/env python

RingSpareBay = 1
NonRingSpareBay = 1 
TempBracket = 1
TrayPaper = 1
WrappingPaper = 1
WrappingSealer = 1
PrintedListWrapper = 1
A4Paper = 1
IndicatorDispenser = 1
StickerTag = 1

def CheckConsumables():
    #Add data grabbing codes here:
    
    #
    ConsumablesDict = {'RingSpareBay' : RingSpareBay, 'NonRingSpareBay' : NonRingSpareBay, 'TempBracket' : TempBracket, 'TrayPaper' : TrayPaper, 'WrappingPaper' : WrappingPaper, 'WrappingSealer' : WrappingSealer, 'PrintedListWrapper' : PrintedListWrapper, 'A4Paper' : A4Paper, 'IndicatorDispenser' : IndicatorDispenser, 'StickerTag' : StickerTag}
    i = 0
    for x in ConsumablesDict:
        i += ConsumablesDict[x]
    if (i == 10):
        return True
    else:
        return False

TrayWithInstruments = 1
Cover = 1
Container = 1
MagilsTube = 1

def CheckWetBayTray():
    #Add data grabbing codes here:
    
    #
    if(TrayWithInstruments):
        return True
    else:
        return False
def CheckDryBayCover():
    #Add data grabbing codes here:
    
    #
    if(Cover):
        return True
    else:
        return False
def CheckDryBayContainer():
    #Add data grabbing codes here:
    
    #
    if(Container):
        return True
    else:
        return False
def CheckMagilsTube():
    #Add data grabbing codes here:
    
    #
    if(MagilsTube):
        return True
    else:
        return False
