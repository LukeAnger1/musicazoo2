import shmooze.lib.service as service
import shmooze.settings as settings
import os
import signal
import math

try:
    import alsaaudio
except:
    alsaaudio = None

try:
    import osax
except:
    osax = None

exp=0.6 # approximate

def human_to_computer(val):
	return int(100*(float(val)/100)**exp)

def computer_to_human(val):
	return int(100*(float(val)/100)**(1.0/exp))

class Volume(service.JSONCommandProcessor, service.Service):
    port=settings.ports["vol"]

    def __init__(self):
        print("=" * 60)
        print(f"[VOLUME] Starting Volume server on port {settings.ports['vol']}")
        print("[VOLUME] Volume started.")

        if alsaaudio:
            print("[VOLUME] Using ALSA audio mixer (Linux)")
            self.mixer=alsaaudio.Mixer(control='PCM')
        elif osax:
            print("[VOLUME] Using OSAX audio control (macOS)")
            self.mixer = osax.OSAX()
        else:
            print("[VOLUME] WARNING: Unable to control volume - no audio library available")

        # JSONCommandService handles all of the low-level TCP connection stuff.
        super(Volume, self).__init__()
        print("=" * 60)

    @service.coroutine
    def get_vol(self):
        if alsaaudio:
            v=self.mixer.getvolume()[0]
        elif osax:
            v=self.mixer.get_volume_settings()[osax.k.output_volume]
        else:
            v=0
        print(f"[VOLUME] get_vol called, returning: {computer_to_human(v)}")
        raise service.Return({'vol': computer_to_human(v)})

    @service.coroutine
    def set_vol(self,vol):
        print(f"[VOLUME] set_vol called with volume: {vol}")
        v=human_to_computer(vol)
        if alsaaudio:
            self.mixer.setvolume(v)
            print(f"[VOLUME] Volume set to {v} using ALSA")
        elif osax:
            self.mixer.set_volume(output_volume=v)
            print(f"[VOLUME] Volume set to {v} using OSAX")
        else:
            print(f"[VOLUME] Setting fake volume: {v} (no audio library)")
        raise service.Return({})

    def shutdown(self):
        service.ioloop.stop()

    commands={
        'set_vol': set_vol,
        'get_vol': get_vol
    }

vol = Volume()

def shutdown_handler(signum,frame):
    print()
    print("Received signal, attempting graceful shutdown...")
    service.ioloop.add_callback_from_signal(vol.shutdown)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

service.ioloop.start()
