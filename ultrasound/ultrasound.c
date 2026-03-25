#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/gpio/consumer.h>
#include <linux/delay.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/mod_devicetable.h>


MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Ultrasound distance sensor driver");
MODULE_AUTHOR("Joseph Joud");
MODULE_VERSION("1.0");
//MODULE_SUPPORTED_DEVICE("HC-SR04"); // Does not work ! idk why but whatever

// Constants 
static int major;
static int busy = 0;
int timeout = 100000;

static const struct of_device_id ultrasound_dt[] = {
    { .compatible = "insa,ultrasound" },
    {}
};

MODULE_DEVICE_TABLE(of, ultrasound_dt);


static int ultrasound_probe(struct platform_device *pdev);
static int ultrasound_remove(struct platform_device *pdev);
static int dev_open(struct inode *ino, struct file *fp);
static int dev_release(struct inode *ino, struct file *fp);
static ssize_t dev_read(struct file *fp, char __user *buf, size_t n, loff_t *of);

// Structure Driver
static struct platform_driver ultrasound_driver = {
    .driver = {
        .name = "ultrasound",
        .of_match_table = ultrasound_dt,
    },
    .probe  = ultrasound_probe,
    .remove = ultrasound_remove,
};

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = dev_open,
    .read = dev_read,
    .release = dev_release,
};

struct gpios {                  // PROBABLY NOT NEEDED
    struct gpio_desc *trig_gpio;
    struct gpio_desc *echo_gpio;
};

static struct gpios *us_gpios;

//opening of the chardev
static int dev_open(struct inode *ino, struct file *fp) {
    if (busy) {
        return -EBUSY;
    }
    busy = 1;
    return 0;
}

//closing of the chardev
static int dev_release(struct inode *ino, struct file *fp) {
    busy = 0;
    return 0;
}

//Probe = initialization of all driver structures (GPIOs, character device, etc.)
static int ultrasound_probe(struct platform_device *pdev) {
    struct device *dev = &pdev->dev;

    us_gpios = devm_kzalloc(dev, sizeof(struct gpios), GFP_KERNEL);
    if (!us_gpios) {
        dev_err(dev, "Erreur d'allocation memoire\n");
        return -ENOMEM;
    }

    //GPIOs 
    us_gpios->trig_gpio = devm_gpiod_get(dev, "trigger", GPIOD_OUT_LOW);
    us_gpios->echo_gpio = devm_gpiod_get(dev, "echo", GPIOD_IN);

    if (IS_ERR(us_gpios->trig_gpio) || IS_ERR(us_gpios->echo_gpio)) {
        dev_err(dev, "Erreur GPIO (probably Dts related)\n");
        return -EINVAL;
    }

    //Chardev registering
    major = register_chrdev(0, "DUsound", &fops);
    if (major < 0) return major;

    dev_info(dev, "Ultrasound probed! Major = %d\n", major);
    return 0;
}

static ssize_t dev_read(struct file *fp, char __user *buf, size_t n, loff_t *of) {
    int result = 0;
    int i;

    if (*of > 0) return 0; //*of is the offset in the chardev file, we use it to know if we already read something or not (since we only have one int to read, we can just check if of > 0 

   
    if (!us_gpios) return -ENODEV; //checking gpios is defined properly

    // Trigger 10us 
    gpiod_set_value(us_gpios->trig_gpio, 1);
    udelay(10);
    gpiod_set_value(us_gpios->trig_gpio, 0);

    // Echo (waiting for start of echo signal)
    while (gpiod_get_value(us_gpios->echo_gpio) == 0 && timeout--) {
        cpu_relax(); // defined as 10 nops in buildroot/output/build/linux-6.9.8/arch/arm/include/asm/vdso/processor.h (lowers cpu usge while waiting)
    } 

    // Measure
    for (i = 0; i < 1000000; i++) {
        if (gpiod_get_value(us_gpios->echo_gpio) == 0) break;
        udelay(1); // replace with passive waiting ?
    }
    result = i; 
    result = (result * 340) / 1000000; // in mm

    if (copy_to_user(buf, &result, sizeof(result))) return -EFAULT;
    *of += sizeof(result);
    return sizeof(result);
}


static int ultrasound_remove(struct platform_device *pdev) { 
    unregister_chrdev(major, "DUsound");
    return 0;
    //TODO ?? : free gpios etc ... 
}

module_platform_driver(ultrasound_driver); //macro magique