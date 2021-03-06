import numpy as np
import math
from PIL import Image

def read_data_string(bits):
    """
    Given: bit string of the data (LSB first)
    Return: data (np array of numbers)
    See definition of numbers in write_data_string.py
    sorry I'm so rusty in python
    """
    m = 1080
    n = 1920

    TYPE = bits[0] #HDD (0) or HIO (1)

    if TYPE: #HIO
        PN = bits[1] + 2*bits[2] + 4*bits[3] + 8*bits[4] + 16*bits[5]
        YD = bits[6] #YOLO detected handrail?
        MD = bits[7] #MASK detected handrail?

        #YOLO bounding box
        YBBX1 = (m/16) * (0.5 + bits[ 8] + 2*bits[ 9] + 4*bits[10] + 8*bits[11])
        YBBY1 = (n/16) * (0.5 + bits[12] + 2*bits[13] + 4*bits[14] + 8*bits[15])
        YBBX2 = (m/16) * (0.5 + bits[16] + 2*bits[17] + 4*bits[18] + 8*bits[19])
        YBBY2 = (n/16) * (0.5 + bits[20] + 2*bits[21] + 4*bits[22] + 8*bits[23])
        #MASK bounding box
        MBBX1 = (m/16) * (0.5 + bits[24] + 2*bits[25] + 4*bits[26] + 8*bits[27])
        MBBY1 = (n/16) * (0.5 + bits[28] + 2*bits[29] + 4*bits[30] + 8*bits[31])
        MBBX2 = (m/16) * (0.5 + bits[32] + 2*bits[33] + 4*bits[34] + 8*bits[35])
        MBBY2 = (n/16) * (0.5 + bits[36] + 2*bits[37] + 4*bits[38] + 8*bits[39])

        c_map  = np.array([ 0,10,20,25,30,35,40,45,50,53,56,59,62,65,68,71,74,76,78,80,82,84,86,88,90,92,94,95,96,97,98, 99])
        c_map2 = np.array([10,20,25,30,35,40,45,50,53,56,59,62,65,68,71,74,76,78,80,82,84,86,88,90,92,94,95,96,97,98,99,100])
        c_map = 0.5*(c_map + c_map2)
        temp = bits[40] + 2*bits[41] + 4*bits[42] + 8*bits[43] + 16*bits[44]
        CY = c_map[temp]
        temp = bits[45] + 2*bits[46] + 4*bits[47] + 8*bits[48] + 16*bits[49]
        CM = c_map[temp]

        #grayscale values
        Q30 = (256/16) * (0.5 + bits[50] + 2*bits[51] + 4*bits[52] + 8*bits[53])
        Q50 = (256/16) * (0.5 + bits[54] + 2*bits[55] + 4*bits[56] + 8*bits[57])
        Q70 = (256/16) * (0.5 + bits[58] + 2*bits[59] + 4*bits[60] + 8*bits[61])
        Q90 = (256/16) * (0.5 + bits[62] + 2*bits[63] + 4*bits[64] + 8*bits[65])

        #pixel value
        PIX = np.zeros((3,), dtype=int)
        PIX[0] = (256/64) * (0.5 + bits[66] + 2*bits[67] + 4*bits[68] + 8*bits[69] + 16*bits[70] + 32*bits[71])
        PIX[1] = (256/64) * (0.5 + bits[72] + 2*bits[73] + 4*bits[74] + 8*bits[75] + 16*bits[76] + 32*bits[77])
        PIX[2] = (256/64) * (0.5 + bits[78] + 2*bits[79] + 4*bits[80] + 8*bits[81] + 16*bits[82] + 32*bits[83])

        TEMP = (64 / 16) *(0.5 + bits[84] + 2*bits[85] + 4*bits[86] + 8*bits[87])

        data = np.zeros((23,), dtype=float)
        data[ 0] = TYPE
        data[ 1] = PN
        data[ 2] = YD
        data[ 3] = MD
        data[ 4] = YBBX1
        data[ 5] = YBBY1
        data[ 6] = YBBX2
        data[ 7] = YBBY2
        data[ 8] = MBBX1
        data[ 9] = MBBY1
        data[10] = MBBX2
        data[11] = MBBY2
        data[12] = CY
        data[13] = CM
        data[14] = Q30
        data[15] = Q50
        data[16] = Q70
        data[17] = Q90
        data[18] = PIX[0]
        data[19] = PIX[1]
        data[20] = PIX[2]
        data[21] = TEMP

    else: #HDD data
        XN = bits[1] + 2*bits[2] + 4*bits[3] + 8*bits[4] + 16*bits[5]

        WXA = -25+(50/256)*(0.5+bits[ 6]+2*bits[ 7]+4*bits[ 8]+8*bits[ 9]+16*bits[10]+32*bits[11]+64*bits[12]+128*bits[13])
        WXB = -25+(50/256)*(0.5+bits[14]+2*bits[15]+4*bits[16]+8*bits[17]+16*bits[18]+32*bits[19]+64*bits[20]+128*bits[21])
        WXC = -25+(50/256)*(0.5+bits[22]+2*bits[23]+4*bits[24]+8*bits[25]+16*bits[26]+32*bits[27]+64*bits[28]+128*bits[29])
        WYA = -25+(50/512)*(0.5+bits[30]+2*bits[31]+4*bits[32]+8*bits[33]+16*bits[34]+32*bits[35]+64*bits[36]+128*bits[37]+256*bits[38])
        WYB = -25+(50/512)*(0.5+bits[39]+2*bits[40]+4*bits[41]+8*bits[42]+16*bits[43]+32*bits[44]+64*bits[45]+128*bits[46]+256*bits[47])
        WYC = -25+(50/512)*(0.5+bits[48]+2*bits[49]+4*bits[50]+8*bits[51]+16*bits[52]+32*bits[53]+64*bits[54]+128*bits[55]+256*bits[56])
        WZA = -25+(50/256)*(0.5+bits[57]+2*bits[58]+4*bits[59]+8*bits[60]+16*bits[61]+32*bits[62]+64*bits[63]+128*bits[64])
        WZB = -25+(50/256)*(0.5+bits[65]+2*bits[66]+4*bits[67]+8*bits[68]+16*bits[69]+32*bits[70]+64*bits[71]+128*bits[72])
        WZC = -25+(50/256)*(0.5+bits[73]+2*bits[74]+4*bits[75]+8*bits[76]+16*bits[77]+32*bits[78]+64*bits[79]+128*bits[80])

        CD = (3000 / 32) * (0.5 + bits[81] + 2*bits[82] + 4*bits[83] + 8*bits[84] + 16*bits[85])
        TEMP = (64 /  4) * (0.5 + bits[86] + 2*bits[87])

        data = np.zeros((14,), dtype=float)
        data[ 0] = TYPE
        data[ 1] = XN
        data[ 2] = WXA
        data[ 3] = WXB
        data[ 4] = WXC
        data[ 5] = WYA
        data[ 6] = WYB
        data[ 7] = WYC
        data[ 8] = WZA
        data[ 9] = WZB
        data[10] = WZC
        data[11] = CD
        data[12] = TEMP

    #checksum - same for both 
    cs = np.sum(bits[0:87])
    cs1 = (cs % 2)
    cs2 = (cs % 4)>1.5
    CS = (cs1 == bits[88]) and (cs2 == bits[89])
    data[data.size-1] = CS
    return data