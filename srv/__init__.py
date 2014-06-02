
from . import AZ7722, DG1022U, ODP3032, TG124A, TH1951
import atexit
atexit.register(AZ7722.AZ7722_stop)
atexit.register(TG124A.tg_usb_dispose)

