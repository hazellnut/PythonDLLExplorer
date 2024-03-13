from ctypes import WinDLL
import ctypes

tc_dll = WinDLL("C:/TwinCAT\AdsApi/TcAdsDll/x64\TcAdsDll.dll")


class SAdsVersion(ctypes.Structure):
    """Struct containing ADS version information."""

    _fields_ = [("version", ctypes.c_ubyte), ("revision", ctypes.c_ubyte), ("build", ctypes.c_uint16)]



class NetId(ctypes.Structure):
    """Create structure for net id"""
    # _pack_ = 1
    _fields_ = [
        ("b",ctypes.c_ubyte * 6)
    ]


class Addr(ctypes.Structure):
    """create structure for AMS address"""
    # _pack_ = 1
    _fields_ = [("netId", NetId),
            ("port",ctypes.c_uint16)]




AdsSyncReadStateReqProto = ctypes.WINFUNCTYPE(
    ctypes.c_long,
    ctypes.c_long,
    ctypes.POINTER(Addr),
    ctypes.POINTER(ctypes.c_uint16),
    ctypes.POINTER(ctypes.c_uint16)
)


AdsPortOpenProto = ctypes.WINFUNCTYPE(
    int,
    ctypes.c_void_p
)


AdsPortCloseProto = ctypes.WINFUNCTYPE(
    ctypes.c_long,
    ctypes.c_void_p
)



AdsPortOpen = AdsPortOpenProto(("AdsPortOpenEx",tc_dll),None)
nAddr = Addr()
pAddr = ctypes.pointer(nAddr)

AdsPortClose = AdsPortCloseProto(("AdsPortCloseEx",tc_dll),None)
portno = AdsPortOpen(None)
# AdsGetLocalAddress = tc_dll.AdsGetLocalAddressEx
# err = AdsGetLocalAddress(portno,pAddr)

netId = NetId()
ams_addr = [192,168,20,48,2,1]
# for i,_ in enumerate(netId.b):
#     netId.b[i] = ams_addr[i]

netId.b = (ctypes.c_ubyte *6)(*ams_addr)
nAddr = Addr()
nAddr.netId = netId
nAddr.port = 65535
adsportno = portno
pAddr = ctypes.pointer(nAddr)
# AdsSyncReadStateParams = (1,"port",0),(1,"pAddr",0),(1,"pAdsState",0),(1,"pDeviceState",0)



# char_data = bytearray([192,168,20,48,1,1])
# L = len(char_data)
# netId.b = (ctypes.c_ubyte * L)  (*char_data)
# nAddr.AmsNetId = netId
# nAddr.port = ctypes.c_uint16(801)

# AdsSyncReadStateReq = AdsSyncReadStateReqProto(("AdsSyncReadStateReqEx",tc_dll),AdsSyncReadStateParams)
AdsSyncReadStateReq = tc_dll.AdsSyncReadStateReqEx

AdsState = ctypes.c_uint16()
DeviceState = ctypes.c_uint16()
pAdsState = ctypes.pointer(AdsState)
pDeviceState = ctypes.pointer(DeviceState)
# AddrPointer = ctypes.pointer(nAddr)

# pDeviceStatePtr = (ctypes.Pointer(ctypes.c_short))
# pDeviceStatePtr = ctypes.byref(pDeviceState)

errorcode = AdsSyncReadStateReq(portno,pAddr,pAdsState,pDeviceState)




AdsGetDllVersionProto = ctypes.WINFUNCTYPE(SAdsVersion,ctypes.c_void_p)
dllversionfunc = AdsGetDllVersionProto(("AdsGetDllVersion",tc_dll),None)




returnval = dllversionfunc(None)


AdsPortClose(None)
if errorcode:
    print(f"error: {errorcode}")
else:
    print(AdsState.value)
    print(DeviceState.value)
