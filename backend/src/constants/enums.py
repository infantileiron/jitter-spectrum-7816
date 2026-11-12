from enum import Enum
class Role(str,Enum):
 admin="admin"
 analyst="analyst"
 viewer="viewer"
class RunStatus(str,Enum):
 queued="queued"
 running="running"
 completed="completed"
 failed="failed"
class Detrend(str,Enum):
 mean="mean"
 linear="linear"
class FFTWindow(str,Enum):
 hann="hann"
 boxcar="boxcar"
