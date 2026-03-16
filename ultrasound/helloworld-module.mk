ULTRASOUND_VERSION = 1.0
ULTRASOUND_SITE = package/ultrasound
ULTRASOUND_SITE_METHOD = local

ULTRASOUND_MODULE_MAKE_OPTS = KERNELDIR=$(LINUX_DIR)

# L'ordre est important :
$(eval $(kernel-module))
$(eval $(generic-package))
